from flask import Blueprint, jsonify, request
import sqlite3
import os

lmetrics_bp = Blueprint('lmetrics', __name__)

DB_NAME = 'imza_emlak.db'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def calculate_intent_score(session_id):
    """Belirli bir session için detaylı niyet skoru hesaplar."""
    conn = get_db_connection()
    interactions = conn.execute('''
        SELECT event_type, element_id, value, url 
        FROM user_interactions 
        WHERE session_id = ?
    ''', (session_id,)).fetchall()
    conn.close()

    if not interactions:
        return 0, "Bilinmiyor"

    score = 0
    categories = {} # URL bazlı ilgi alanı tespiti

    for i in interactions:
        etype = i['event_type']
        eid = i['element_id']
        url = i['url'] or ""

        # Kategori Tespiti (URL'den anahtar kelime avı)
        if 'villa' in url.lower(): categories['Villa'] = categories.get('Villa', 0) + 1
        if 'rezidans' in url.lower() or 'daire' in url.lower(): categories['Rezidans'] = categories.get('Rezidans', 0) + 1
        if 'bogaz' in url.lower() or 'sariyer' in url.lower(): categories['Boğaz Hattı'] = categories.get('Boğaz Hattı', 0) + 1
        if 'yatirim' in url.lower(): categories['Yatırımlık'] = categories.get('Yatırımlık', 0) + 1

        # Puanlama
        if etype == 'click':
            score += 15
            if eid and ('whatsapp' in eid.lower() or 'book' in eid.lower() or 'pay' in eid.lower()):
                score += 30 # Kritik aksiyon
        elif etype == 'scroll':
            val = int(i['value']) if i['value'] and i['value'].isdigit() else 0
            if val >= 75: score += 15
            elif val >= 50: score += 10
        elif etype == 'stay':
            score += 5
        elif etype == 'pageview':
            score += 2

    # En baskın kategoriyi bul
    top_interest = "Genel"
    if categories:
        top_interest = max(categories, key=categories.get)

    return min(score, 100), top_interest

@lmetrics_bp.route('/api/lmetrics/collect', methods=['POST'])
def collect_interaction():
    """Kullanıcı etkileşim verilerini toplar."""
    data = request.json
    session_id = data.get('session_id')
    url = data.get('url')
    event_type = data.get('event_type')
    element_id = data.get('element_id')
    value = data.get('value')

    if not all([session_id, event_type]):
        return jsonify({"error": "session_id ve event_type zorunludur"}), 400

    conn = get_db_connection()
    conn.execute('''
        INSERT INTO user_interactions (session_id, url, event_type, element_id, value)
        VALUES (?, ?, ?, ?, ?)
    ''', (session_id, url, event_type, element_id, value))
    
    # Lead ile eşleşmişse lead_id'yi bull ve lead_interactions'a da pasif kayıt atabiliriz 
    # Ama user_interactions üzerinden join yapmak daha temiz.
    
    conn.commit()
    conn.close()

    return jsonify({"status": "success"}), 201

@lmetrics_bp.route('/api/lmetrics/analysis/<int:lead_id>', methods=['GET'])
def analyze_lead_lmetrics(lead_id):
    """Bir lead'in dijital niyet analizini yapar."""
    conn = get_db_connection()
    # Lead'in session_id'sini bul (lead_interactions veya directly from leads if we added it)
    # database.py lead tablosuna session_id eklememişiz ama lead_interactions'da var.
    session_row = conn.execute('SELECT session_id FROM lead_interactions WHERE lead_id = ? LIMIT 1', (lead_id,)).fetchone()
    
    if not session_row:
        conn.close()
        return jsonify({"error": "Bu aday için dijital iz bulunamadı"}), 404
    
    session_id = session_row['session_id']
    score, interest = calculate_intent_score(session_id)
    
    # Timeline
    timeline = conn.execute('''
        SELECT event_type, url, timestamp, element_id, value 
        FROM user_interactions 
        WHERE session_id = ? 
        ORDER BY timestamp DESC LIMIT 50
    ''', (session_id,)).fetchall()
    
    conn.close()
    
    return jsonify({
        "lead_id": lead_id,
        "session_id": session_id,
        "intent_score": score,
        "top_interest": interest,
        "timeline": [dict(t) for t in timeline]
    }), 200
