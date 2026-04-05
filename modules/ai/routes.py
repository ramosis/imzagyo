import os
import datetime
from flask import request, jsonify, g
from google import genai
from shared.database import get_db
from modules.auth.decorators import require_inner_circle, login_required
from . import ai_bp

def get_ai_client():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key: return None
    return genai.Client(api_key=api_key)

@ai_bp.route('/generate-summary', methods=['POST'])
@require_inner_circle
def generate_summary():
    data = request.json
    client = get_ai_client()
    if not client: return jsonify({"error": "AI Key missing"}), 500
    
    prompt = f"Lüks emlak uzmanı mısın? Şu özellikler için 2-3 paragraflık ilan açıklaması yaz: {data}"
    response = client.models.generate_content(model='gemini-1.5-flash', contents=prompt)
    return jsonify({"story": response.text.strip()}), 200

@ai_bp.route('/analyze-investor', methods=['POST'])
def analyze_investor():
    data = request.json
    choices = data.get('choices', {})
    scores = {"A": 0, "B": 0, "C": 0, "D": 0}
    for choice in choices.values():
        if choice in scores: scores[choice] += 1
    
    winning = max(scores, key=scores.get)
    profiles = {
        "A": {"title": "Vizyoner", "desc": "Kendi fırsatını yaratmayı seviyorsunuz."},
        "B": {"title": "Stratejik", "desc": "Güven ve istikrar odaklısınız."},
        "C": {"title": "Analitik", "desc": "Veri ve ROI sizin için her şey."},
        "D": {"title": "Detaycı", "desc": "Kusursuz planlama ve risk analizi."}
    }
    res = profiles.get(winning, profiles["B"])
    return jsonify({"winning_profile": winning, "public_title": res["title"], "public_desc": res["desc"]})

@ai_bp.route('/lmetrics/collect', methods=['POST'])
def collect_interaction():
    data = request.json
    with get_db() as conn:
        conn.execute('INSERT INTO user_interactions (session_id, url, event_type, element_id, value) VALUES (?,?,?,?,?)',
                     (data.get('session_id'), data.get('url'), data.get('event_type'), data.get('element_id'), data.get('value')))
        conn.commit()
    return jsonify({"status": "success"}), 201

_translation_cache = {}

def translate_content(text, target_lang):
    """Translates content using Gemini, with in-memory caching."""
    if not text: return ""
    
    cache_key = f"{target_lang}:{text[:50]}" # Simple key for caching
    if cache_key in _translation_cache:
        return _translation_cache[cache_key]

    client = get_ai_client()
    if not client: return text
    try:
        prompt = f"Sen profesyonel bir gayrimenkul çevirmenisin. Aşağıdaki Türkçe metni {target_lang} diline çevir: {text}"
        response = client.models.generate_content(model='gemini-1.5-flash', contents=prompt)
        result = response.text.strip()
        _translation_cache[cache_key] = result
        return result
    except Exception as e:
        print(f"AI Translation Error: {e}")
        return text

def calculate_intent_score(session_id):
    with get_db() as conn:
        interactions = conn.execute('SELECT event_type, url FROM user_interactions WHERE session_id = ?', (session_id,)).fetchall()
        if not interactions: return 0, "Bilinmiyor"
        score = sum(15 if i['event_type'] == 'click' else 5 for i in interactions)
        return min(score, 100), "Genel"

@ai_bp.route('/lmetrics/analysis/<int:lead_id>', methods=['GET'])
@require_inner_circle
def analyze_lead_lmetrics(lead_id):
    with get_db() as conn:
        session_row = conn.execute('SELECT session_id FROM lead_interactions WHERE lead_id = ? LIMIT 1', (lead_id,)).fetchone()
        if not session_row: return jsonify({"error": "No data"}), 404
        score, interest = calculate_intent_score(session_row['session_id'])
        return jsonify({"lead_id": lead_id, "score": score, "interest": interest})
