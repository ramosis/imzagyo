import os
import datetime
from flask import Blueprint, request, jsonify
import google.generativeai as genai
from .auth import require_inner_circle

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/api/generate-summary', methods=['POST'])
@require_inner_circle
def generate_summary():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return jsonify({"error": "Lütfen sistem yöneticisinden GEMINI_API_KEY ortam değişkenini ayarlamasını isteyin."}), 500

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')

        lokasyon = data.get('il_ilce', '') + ' ' + data.get('mahalle', '')
        fiyat = data.get('fiyat', '')
        oda = data.get('oda', '')
        tip = data.get('alt_tip', '')
        ozellikler = data.get('ozellikler', '')
        
        prompt = f"""
Sen lüks ve profesyonel hizmet veren bir gayrimenkul (emlak) iletişim uzmanısın. Bize verilen şu gayrimenkul detayları için potansiyel alıcıları/kiracıları cezbedecek, prestijli, SEO uyumlu ve dikkat çekici 2-3 paragraflık bir ilan açıklaması (hikayesi) yazar mısın?

Özellikler:
- Tip: {tip}
- Lokasyon: {lokasyon}
- Oda Sayısı: {oda}
- Fiyat: {fiyat}
- Ekstra Özellikler: {ozellikler}

Lütfen sadece oluşturduğun metni (başka bir açıklama eklemeden) markdown formatı kullanmadan sade ve şık paragraflar halinde döndür. Ayrıca sonuna profesyonel bir çağrı (call-to-action) ekle.
"""
        response = model.generate_content(prompt)
        # response.text produces the generated output
        return jsonify({"story": response.text.strip()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def translate_content(text, target_lang):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        import logging
        logging.warning("AI_SERVICE: GEMINI_API_KEY NOT FOUND. Echoing original text.")
        return text # Anahtar yoksa orijinali dön

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
Sen profesyonel bir gayrimenkul çevirmenisin. Aşağıdaki Türkçe metni, emlak terminolojisine uygun, lüks ve çekici bir dille {target_lang} diline çevir.
Lütfen sadece çeviriyi döndür, başka hiçbir açıklama ekleme.

Metin:
{text}
"""
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"AI Çeviri Hatası ({target_lang}): {e}")
        return text

@ai_bp.route('/api/ai/auto-translate-portfolio', methods=['POST'])
@require_inner_circle
def auto_translate_portfolio():
    data = request.json
    fields_to_translate = ['baslik1', 'baslik2', 'lokasyon', 'hikaye']
    results = {}
    
    for field in fields_to_translate:
        val = data.get(field)
        if val:
            results[f"{field}_en"] = translate_content(val, "İngilizce")
            results[f"{field}_ar"] = translate_content(val, "Arapça")
            
    return jsonify(results), 200

# --- STRATEJİK YATIRIMCI ANALİZİ (DUNNING-KRUGER SHADOW) ---

@ai_bp.route('/api/ai/analyze-investor', methods=['POST'])
def analyze_investor():
    """
    Frontend'den gelen ham cevapları (A, B, C, D) analiz eder.
    Stratejik teşhis ve taktikler sadece burada (backend) bulunur.
    """
    data = request.json
    choices = data.get('choices', {}) # Örn: {"2": "A", "3": "C", ...}
    
    scores = {"A": 0, "B": 0, "C": 0, "D": 0}
    for q, choice in choices.items():
        if choice in scores:
            scores[choice] += 1
            
    # Kazanan profili bul
    winning_profile = max(scores, key=lambda k: scores[k])
    
    # Stratejik Veri Sözlüğü (SADECE BACKEND)
    profiles = {
        "A": {
            "public_title": "Vizyoner ve Lider Yatırımcı",
            "public_desc": "Kendi fırsatınızı yaratmayı ve vizyonunuzla gayrimenkule değer katmayı seviyorsunuz. Sizin hızınıza ayak uydurabilecek özel yetkili uzmanımızla portföyleri inceleyeceğiz.",
            "crm_diagnosis": "Dunning-Kruger eğiliminde. Piyasayı bildiğini sanıyor ama asıl amacı kontrolü elinde tutmak.",
            "crm_tactic": "Asla zıtlaşma. İtirazları pazar rakamlarıyla çürüt ama kararı o veriyormuş gibi hissettir.",
            "assigned_agent_type": "Tip 3 (Analist) / Tip 4 (PR Ustası)"
        },
        "B": {
            "public_title": "Stratejik ve Güven Odaklı",
            "public_desc": "Yatırım yaparken uzun vadeli huzuru ön planda tutuyorsunuz. Sürecin tüm operasyonel yükünü sizden alarak pürüzsüz bir deneyim yaşatacak A Sınıfı Rehber Danışmanımızla eşleştirildiniz.",
            "crm_diagnosis": "Kayıptan kaçınma güdüsü çok yüksek. Karar almaktan ve zarar etmekten korkuyor.",
            "crm_tactic": "Maksimum 2 seçenek sun. Başkalarının (sürünün) da oradan alıp karlı çıktığını söyle. Güven ver.",
            "assigned_agent_type": "Tip 2 (Empat / Rehber)"
        },
        "C": {
            "public_title": "Analitik ve Rasyonel",
            "public_desc": "Duygusal tahminler yerine size net amortisman süreleri, bölgesel ROI raporları ve excel tabloları sunacak finansal gayrimenkul uzmanımızla eşleştirildiniz.",
            "crm_diagnosis": "Duygusu yok, yatırım getirisi ve fırsat maliyetine odaklı.",
            "crm_tactic": "Manzara veya estetik övme. Excel ver, kira çarpanı ver, net teklif yap ve satışı kapat.",
            "assigned_agent_type": "Tip 1 (Kapanışçı) / Tip 3 (Analist)"
        },
        "D": {
            "public_title": "Detaycı ve Mükemmeliyetçi",
            "public_desc": "Kusursuz planlamaya inanıyor ve her şeyi güvence altına alıyorsunuz. Sizin için zemin etüdünden hukuki duruma kadar her detayı hazırlayacak Risk Analiz Ekibimizle eşleştirildiniz.",
            "crm_diagnosis": "Bilgili ama analiz felcine uğramış. Çok fazla detaya takıldığı için eyleme geçemiyor.",
            "crm_tactic": "Talep ettiği raporları önüne yığ, bilgisini onore et. Sonra inisiyatif alıp 'Hadi imzalıyoruz' diyerek itekle.",
            "assigned_agent_type": "Tip 3 (Analist) + Tip 1 (Broker)"
        }
    }
    
    result = profiles.get(winning_profile, profiles["B"])
    return jsonify({
        "winning_profile": winning_profile,
        "public_title": result["public_title"],
        "public_desc": result["public_desc"],
        "internal_data": { # Bu kısım normalde lead kaydedilirken kullanılacak
            "diagnosis": result["crm_diagnosis"],
            "tactic": result["crm_tactic"],
            "agent": result["assigned_agent_type"]
        }
    }), 200

@ai_bp.route('/api/ai/lead-insights/<int:id>', methods=['GET'])
@require_inner_circle
def lead_insights(id):
    """
    Belirli bir lead'in dijital ayak izlerini analiz eder ve AI özeti oluşturur.
    """
    from database import get_db_connection
    import json

    conn = get_db_connection()
    try:
        # 1. Lead bilgilerini ve etkileşimlerini al
        lead = conn.execute('SELECT * FROM leads WHERE id = ?', (id,)).fetchone()
        if not lead:
            return jsonify({"error": "Lead bulunamadı"}), 404

        interactions = conn.execute('''
            SELECT * FROM lead_interactions 
            WHERE lead_id = ? 
            ORDER BY created_at DESC 
            LIMIT 20
        ''', (id,)).fetchall()

        if not interactions:
            return jsonify({"insight": "Henüz yeterli etkileşim verisi yok."}), 200

        # 2. Etkileşim verilerini metinleştir
        interaction_log = ""
        for i in interactions:
            data = json.loads(i['data_json']) if i['data_json'] else {}
            interaction_log += f"- {i['created_at']}: {i['tool_name']} ({data.get('url', 'N/A')})\n"

        # 3. Gemini Prompt Hazırla
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            return jsonify({"insight": "AI servisi şu an devre dışı (API Anahtarı eksik)."}), 200

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')

        prompt = f"""
Sen bir gayrimenkul danışmanı asistanısın. Aşağıdaki verileri analiz ederek danışmana bu aday (lead) hakkında stratejik bir niyet özeti yazar mısın?

Aday İsmi: {lead['name']}
Mevcut Durumu: {lead['status']}
Etkileşim Geçmişi (Son 20 İşlem):
{interaction_log}

İstediğim özellikler:
1. Müşterinin şu anki niyetini (Alıcı mı, Kiracı mı, Yatırımcı mı?) tahmin et.
2. Hangi mülk tipi veya bölgeye ilgi gösterdiğini öne çıkar.
3. Maksimum 3 cümlelik, danışmana taktik veren profesyonel bir not yaz.

Lütfen sadece oluşturduğun notu döndür.
"""
        response = model.generate_content(prompt)
        insight_text = response.text.strip()

        return jsonify({
            "lead_id": id,
            "ai_score": lead['ai_score'],
            "insight": insight_text,
            "generated_at": datetime.datetime.now().isoformat()
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()
