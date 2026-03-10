from flask import Blueprint, request, jsonify
from database import get_db_connection
import json

integrations_bp = Blueprint('integrations', __name__)

# Platform tanımları
PLATFORMS = {
    'listing': [
        {'key': 'sahibinden', 'name': 'Sahibinden.com', 'icon': 'fa-house-laptop', 'color': '#FFD100'},
        {'key': 'hepsiemlak', 'name': 'Hepsiemlak.com', 'icon': 'fa-building', 'color': '#E31E24'},
        {'key': 'emlakjet', 'name': 'Emlakjet.com', 'icon': 'fa-jet-fighter', 'color': '#0066CC'},
        {'key': 'n11emlak', 'name': 'N11 Emlak', 'icon': 'fa-cart-shopping', 'color': '#7B2D8E'},
    ],
    'social': [
        {'key': 'instagram', 'name': 'Instagram', 'icon': 'fa-instagram', 'color': '#E4405F', 'brand': True},
        {'key': 'facebook', 'name': 'Facebook', 'icon': 'fa-facebook', 'color': '#1877F2', 'brand': True},
        {'key': 'youtube', 'name': 'YouTube', 'icon': 'fa-youtube', 'color': '#FF0000', 'brand': True},
        {'key': 'tiktok', 'name': 'TikTok', 'icon': 'fa-tiktok', 'color': '#000000', 'brand': True},
        {'key': 'linkedin', 'name': 'LinkedIn', 'icon': 'fa-linkedin', 'color': '#0A66C2', 'brand': True},
        {'key': 'x_twitter', 'name': 'X (Twitter)', 'icon': 'fa-x-twitter', 'color': '#000000', 'brand': True},
        {'key': 'reddit', 'name': 'Reddit', 'icon': 'fa-reddit-alien', 'color': '#FF4500', 'brand': True},
    ],
    'design': [
        {'key': 'canva', 'name': 'Canva', 'icon': 'fa-palette', 'color': '#00C4CC'},
    ]
}

# İlan sitelerine özel şablonlar
TEMPLATES = {
    'sahibinden': {
        'title': '{baslik1} - {lokasyon}',
        'description': '''🏠 {baslik1}

📍 Konum: {lokasyon}
💰 Fiyat: {fiyat}
🛏️ Oda Sayısı: {oda}
📐 Alan: {alan}
🏢 Kat: {kat}

{hikaye}

📞 İmza Gayrimenkul
🌐 www.imzagayrimenkul.com''',
    },
    'instagram': {
        'title': '{baslik1}',
        'description': '''✨ {baslik1}

📍 {lokasyon}
💰 {fiyat}
🛏️ {oda} | 📐 {alan}

{hikaye}

🏠 Detaylı bilgi için link bio'da!

#emlak #gayrimenkul #satılık #kiralık #{lokasyon_tag} #imzagayrimenkul #luxuryrealestate #property #ev #daire #villa #yatırım''',
    },
    'facebook': {
        'title': '🏠 {baslik1} - {fiyat}',
        'description': '''{baslik1}

📍 {lokasyon}
💰 Fiyat: {fiyat}
🛏️ {oda} | 📐 {alan} | 🏢 {kat}

{hikaye}

📞 İletişim için mesaj atın veya arayın!
🌐 www.imzagayrimenkul.com''',
    },
    'youtube': {
        'title': '{baslik1} | Sanal Tur | İmza Gayrimenkul',
        'description': '''🏠 {baslik1} - Sanal Tur

📍 Konum: {lokasyon}
💰 Fiyat: {fiyat}
🛏️ Oda: {oda} | 📐 Alan: {alan}

{hikaye}

═══════════════════════
📞 İletişim: İmza Gayrimenkul
🌐 www.imzagayrimenkul.com
═══════════════════════

#emlak #gayrimenkul #sanaltour #imzagayrimenkul''',
    },
    'linkedin': {
        'title': '{baslik1} | İmza Gayrimenkul Portföyü',
        'description': '''🏢 Yeni Portföy: {baslik1}

Konum: {lokasyon}
Segment: Premium
Fiyat: {fiyat}

{hikaye}

Bu mülk hakkında detaylı bilgi almak veya yatırım danışmanlığı için bizimle iletişime geçin.

#Gayrimenkul #Yatırım #İmzaGayrimenkul #RealEstate''',
    },
    'x_twitter': {
        'title': '',
        'description': '''🏠 {baslik1}
📍 {lokasyon} | 💰 {fiyat}
🛏️ {oda} | 📐 {alan}

Detaylı bilgi 👇
#emlak #gayrimenkul #imzagayrimenkul''',
    },
    'tiktok': {
        'title': '{baslik1} 🏠 #emlak #ev',
        'description': '''Bu evi görmelisiniz! 😍

📍 {lokasyon}
💰 {fiyat}
🛏️ {oda} oda | 📐 {alan}

#emlak #gayrimenkul #evturu #satılıkev #kiralıkev #imzagayrimenkul #fyp''',
    },
    'hepsiemlak': {
        'title': '{baslik1} - {lokasyon}',
        'description': '''{baslik1}

Konum: {lokasyon}
Fiyat: {fiyat}
Oda Sayısı: {oda}
Alan: {alan}
Kat: {kat}

{hikaye}

İmza Gayrimenkul - Güvenilir Emlak Danışmanlığı''',
    },
    'emlakjet': {
        'title': '{baslik1}',
        'description': '''{baslik1} - {lokasyon}

Fiyat: {fiyat}
Oda: {oda} | Alan: {alan} | Kat: {kat}

{hikaye}

İmza Gayrimenkul''',
    },
    'canva': {
        'title': '{baslik1}',
        'description': '{fiyat} | {lokasyon} | {oda} | {alan}',
    },
    'reddit': {
        'title': '[Satılık] {baslik1} - {lokasyon} | {fiyat}',
        'description': '''**{baslik1}**

**Konum:** {lokasyon}
**Fiyat:** {fiyat}
**Oda:** {oda} | **Alan:** {alan} | **Kat:** {kat}

---

{hikaye}

---

*İmza Gayrimenkul | Profesyonel Emlak Danışmanlığı*
🌐 www.imzagayrimenkul.com''',
    }
}

@integrations_bp.route('/api/platforms', methods=['GET'])
def get_platforms():
    """Tüm desteklenen platformları döndür."""
    return jsonify(PLATFORMS), 200

@integrations_bp.route('/api/integrations', methods=['GET'])
def get_connections():
    """Kayıtlı platform bağlantılarını getir."""
    conn = get_db_connection()
    connections = conn.execute('SELECT * FROM platform_connections ORDER BY platform_type, platform').fetchall()
    conn.close()
    return jsonify([dict(c) for c in connections]), 200

@integrations_bp.route('/api/integrations', methods=['POST'])
def add_connection():
    """Yeni platform bağlantısı ekle."""
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO platform_connections (platform, platform_type, display_name, api_key, api_secret, access_token, account_url, status)
        VALUES (?,?,?,?,?,?,?,?)
    ''', (
        data.get('platform'),
        data.get('platform_type', 'listing'),
        data.get('display_name'),
        data.get('api_key', ''),
        data.get('api_secret', ''),
        data.get('access_token', ''),
        data.get('account_url', ''),
        data.get('status', 'manual')
    ))
    conn.commit()
    conn.close()
    return jsonify({'status': 'connected'}), 201

@integrations_bp.route('/api/integrations/<int:id>', methods=['DELETE'])
def delete_connection(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM platform_connections WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'deleted'}), 200

@integrations_bp.route('/api/publish/generate', methods=['POST'])
def generate_listing():
    """Seçilen portföy ve platform için ilan metni oluştur."""
    data = request.json
    property_id = data.get('property_id')
    platform = data.get('platform')

    if not property_id or not platform:
        return jsonify({'error': 'property_id ve platform gereklidir.'}), 400

    conn = get_db_connection()
    prop = conn.execute('SELECT * FROM portfoyler WHERE id = ?', (property_id,)).fetchone()
    conn.close()

    if not prop:
        return jsonify({'error': 'Portföy bulunamadı.'}), 404

    prop = dict(prop)
    template = TEMPLATES.get(platform, TEMPLATES['sahibinden'])

    # Lokasyon tag'i oluştur (hashtag için)
    lokasyon_tag = (prop.get('lokasyon', '') or '').replace(' ', '').replace(',', '').replace('/', '').lower()

    # Şablonu mülk verileriyle doldur
    try:
        title = template['title'].format(
            baslik1=prop.get('baslik1', ''),
            lokasyon=prop.get('lokasyon', ''),
            fiyat=prop.get('fiyat', ''),
            oda=prop.get('oda', ''),
            alan=prop.get('alan', ''),
            kat=prop.get('kat', ''),
            hikaye=prop.get('hikaye', ''),
            lokasyon_tag=lokasyon_tag
        )
        description = template['description'].format(
            baslik1=prop.get('baslik1', ''),
            lokasyon=prop.get('lokasyon', ''),
            fiyat=prop.get('fiyat', ''),
            oda=prop.get('oda', ''),
            alan=prop.get('alan', ''),
            kat=prop.get('kat', ''),
            hikaye=prop.get('hikaye', ''),
            lokasyon_tag=lokasyon_tag
        )
    except KeyError as e:
        title = prop.get('baslik1', '')
        description = f"Şablon hatası: {e}"

    return jsonify({
        'platform': platform,
        'property_id': property_id,
        'title': title,
        'description': description,
        'image': prop.get('resim_hero', ''),
        'property': {
            'baslik1': prop.get('baslik1'),
            'lokasyon': prop.get('lokasyon'),
            'fiyat': prop.get('fiyat'),
            'oda': prop.get('oda'),
            'alan': prop.get('alan'),
        }
    }), 200

@integrations_bp.route('/api/publish', methods=['POST'])
def save_publication():
    """Paylaşımı kaydet."""
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO publications (property_id, platform_id, platform_name, content_type, generated_text, listing_url, status, published_at)
        VALUES (?,?,?,?,?,?,?,datetime('now'))
    ''', (
        data.get('property_id'),
        data.get('platform_id'),
        data.get('platform_name'),
        data.get('content_type', 'listing'),
        data.get('generated_text', ''),
        data.get('listing_url', ''),
        data.get('status', 'published')
    ))
    conn.commit()
    pub_id = cur.lastrowid
    conn.close()
    return jsonify({'id': pub_id, 'status': 'published'}), 201

@integrations_bp.route('/api/publications', methods=['GET'])
def get_publications():
    """Tüm paylaşım geçmişini getir."""
    conn = get_db_connection()
    pubs = conn.execute('''
        SELECT pub.*, p.baslik1, p.lokasyon, p.fiyat
        FROM publications pub
        LEFT JOIN portfoyler p ON pub.property_id = p.id
        ORDER BY pub.created_at DESC
    ''').fetchall()
    conn.close()
    return jsonify([dict(p) for p in pubs]), 200
