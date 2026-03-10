import os
from flask import Blueprint, request, jsonify
import google.generativeai as genai
from api.auth import require_inner_circle

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
