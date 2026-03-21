""" 
Main Application Entry Point
Initializes the Flask app, registers blueprints, and defines core frontend and upload routes.
"""
from flask import Flask, send_from_directory, jsonify, request
import sqlite3
import json
import os
import time
import urllib.parse
from dotenv import load_dotenv

load_dotenv()

from werkzeug.utils import secure_filename
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from marshmallow import Schema, fields, validate, ValidationError
from database import init_db, doldur_ornek_veriler, DB_NAME, get_db_connection
from api.portfolio import portfolio_bp
from api.users import users_bp
from api.contracts import contracts_bp
from api.taxes import taxes_bp
from api.maintenance import maintenance_bp
from api.appointments import appointments_bp
from api.auth import auth_bp
from api.finance import finance_bp
from api.hero import hero_bp
from api.contract_templates import contract_templates_bp
from api.parties import parties_bp
from api.leads import leads_bp
from api.expenses import expenses_bp
from api.integrations import integrations_bp
from api.documents import documents_bp
from api.purchasing_power import purchasing_power_bp
from api.settings import settings_bp
from api.campaigns import campaigns_bp
from api.hr import hr_bp
from api.contacts import contacts_bp
from api.tracking import tracking_bp
from api.lmetrics import lmetrics_bp
from api.notifications import notifications_bp
from api.ai import ai_bp
from api.neighborhood import neighborhood_bp
from api.projects import projects_bp
from api.pipeline import pipeline_bp
from api.automation import automation_bp
from api.media import media_bp
from api.appraisal import appraisal_bp
app = Flask(__name__, static_folder=None)

# Rate Limiter Yapılandırması
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["10000 per day", "2000 per hour"],
    storage_uri="memory://",
)

# --- VERİ DOĞRULAMA ŞEMALARI (MARSHMALLOW) ---
# Şemalar merkezi olarak api/schemas.py dosyasına taşındı.

UPLOAD_FOLDER = os.path.join(app.root_path, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Register API blueprints
app.register_blueprint(portfolio_bp)
app.register_blueprint(users_bp)
app.register_blueprint(contracts_bp)
app.register_blueprint(taxes_bp)
app.register_blueprint(maintenance_bp)
app.register_blueprint(notifications_bp)
app.register_blueprint(ai_bp)
app.register_blueprint(appointments_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(finance_bp)
app.register_blueprint(hero_bp)
app.register_blueprint(contract_templates_bp)
app.register_blueprint(parties_bp)
app.register_blueprint(leads_bp)
app.register_blueprint(expenses_bp)
app.register_blueprint(integrations_bp)
app.register_blueprint(documents_bp)
app.register_blueprint(purchasing_power_bp)
app.register_blueprint(settings_bp)
app.register_blueprint(campaigns_bp)
app.register_blueprint(hr_bp)
app.register_blueprint(contacts_bp)
app.register_blueprint(tracking_bp)
app.register_blueprint(lmetrics_bp)
app.register_blueprint(neighborhood_bp)
app.register_blueprint(projects_bp)
app.register_blueprint(pipeline_bp)
app.register_blueprint(automation_bp)
app.register_blueprint(media_bp)
app.register_blueprint(appraisal_bp)

@app.after_request
def add_header(r):
    # Geliştirme sürecinde tüm cache'i kapatıyoruz
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    return r

# CORS Ayarları
CORS(app)

# İlk çalışmada DB oluştur
init_db()
# Örnek veriler sadece DB boşsa veya geliştirme ortamındaysa basılmalı
# (Bu fonksiyon genellikle içindeki kontrollerle zaten idempotenttir ama yine de buraya not düşüldü)
doldur_ornek_veriler()


# === FRONTEND STATİK SAYFALAR ===

@app.route('/')
def index():
    host = request.headers.get('Host', '')
    if 'imzamahalle.com' in host:
        return send_from_directory('pages', 'mahalle.html')
    return send_from_directory('pages', 'anasayfa.html')

@app.route('/portal')
def portal():
    return send_from_directory('pages', 'portal.html')

@app.route('/pipeline')
def pipeline():
    return send_from_directory('pages', 'pipeline.html')

@app.route('/mahalle')
def mahalle():
    return send_from_directory('pages', 'mahalle.html')

@app.route('/<path:path>')
def serve_file(path):
    # Ana dizini belirle (app.py'nin olduğu yer)
    base_dir = os.path.abspath(os.path.dirname(__file__))
    pages_dir = os.path.join(base_dir, 'pages')
    
    # 1. API isteklerini atla
    if path.startswith('api/'):
        return "Not Found", 404
    
    # 2. HTML dosyalarını pages/ klasöründen servis et
    # Hem .html eklenmiş hem eklenmemiş halini kontrol et
    clean_path = path.lower()
    file_name = clean_path if clean_path.endswith('.html') else f"{clean_path}.html"
    full_html_path = os.path.join(pages_dir, file_name)
    
    if os.path.exists(full_html_path) and os.path.isfile(full_html_path):
        # --- DİNAMİK SEO ENJEKSİYONU (Faz 2) ---
        if clean_path == 'detay' or clean_path == 'detay.html':
            prop_id = request.args.get('id')
            if prop_id:
                try:
                    conn = get_db_connection()
                    prop = conn.execute('SELECT * FROM portfoyler WHERE id = ?', (prop_id,)).fetchone()
                    conn.close()
                    
                    if prop:
                        with open(full_html_path, 'r', encoding='utf-8') as f:
                            html_content = f.read()
                        
                        lang = request.args.get('lang', 'tr').lower()
                        
                        # Dil bazlı içerik seçimi
                        title_key = 'baslik1'
                        loc_key = 'lokasyon'
                        if lang == 'en' and prop['baslik1_en']: 
                            title_key = 'baslik1_en'
                            loc_key = 'lokasyon_en'
                        elif lang == 'ar' and prop['baslik1_ar']:
                            title_key = 'baslik1_ar'
                            loc_key = 'lokasyon_ar'

                        title = f"{prop[title_key]} | İmza Gayrimenkul"
                        base_desc = "İstanbul'un en seçkin portföyleri."
                        if prop[loc_key]:
                            base_desc = f"{prop[loc_key]} lokasyonunda lüks portföy."
                        
                        desc = f"{base_desc} - {prop['fiyat']}."
                        image = prop['resim_hero'] or "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?q=80&w=1200"
                        
                        html_content = html_content.replace('<title>Boğaz Manzaralı Villa | İmza Gayrimenkul</title>', f'<title>{title}</title>')
                        html_content = html_content.replace('content="İmza Gayrimenkul ile hayalinizdeki portföyü keşfedin."', f'content="{desc}"')
                        html_content = html_content.replace('content="İmza Gayrimenkul | Lüks Portföy"', f'content="{title}"')
                        html_content = html_content.replace('content="Detaylı bilgi için tıklayın."', f'content="{desc}"')
                        html_content = html_content.replace('content="https://images.unsplash.com/photo-1600585154340-be6161a56a0c?q=80&w=1200"', f'content="{image}"')
                        
                        return html_content
                except Exception as e:
                    print(f"SEO Injection Hatası: {e}")
        
        return send_from_directory(pages_dir, file_name)

    # 3. Diğer statik dosyaları (js, css, img) root'tan servis et
    full_static_path = os.path.join(base_dir, path)
    if os.path.exists(full_static_path) and os.path.isfile(full_static_path):
        return send_from_directory(base_dir, path)

    # 4. Hiçbir şey bulunamazsa 404 sayfasına gönder
    return send_from_directory(pages_dir, '404.html'), 404

@app.route('/robots.txt')
def robots():
    return send_from_directory(app.root_path, 'robots.txt')

@app.route('/sitemap.xml')
def sitemap():
    conn = get_db_connection()
    portfoyler = conn.execute('SELECT id, updated_at FROM portfoyler').fetchall()
    conn.close()

    base_url = "https://imzaemlak.com" # Gerçek domain ile güncellenmeli
    pages = [
        {'loc': f"{base_url}/", 'changefreq': 'daily', 'priority': '1.0'},
        {'loc': f"{base_url}/kurumsal", 'changefreq': 'monthly', 'priority': '0.5'},
        {'loc': f"{base_url}/ekip", 'changefreq': 'monthly', 'priority': '0.5'},
        {'loc': f"{base_url}/araclar", 'changefreq': 'monthly', 'priority': '0.5'},
    ]

    for p in portfoyler:
        pages.append({
            'loc': f"{base_url}/detay?id={p['id']}",
            'changefreq': 'weekly',
            'priority': '0.8'
        })

    sitemap_xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    sitemap_xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    
    for page in pages:
        sitemap_xml.append('  <url>')
        sitemap_xml.append(f'    <loc>{page["loc"]}</loc>')
        sitemap_xml.append(f'    <changefreq>{page["changefreq"]}</changefreq>')
        sitemap_xml.append(f'    <priority>{page["priority"]}</priority>')
        sitemap_xml.append('  </url>')
    
    sitemap_xml.append('</urlset>')
    
    return "\n".join(sitemap_xml), 200, {'Content-Type': 'application/xml'}

@app.errorhandler(404)
def page_not_found(e):
    return send_from_directory('pages', '404.html'), 404

# === API UÇ NOKTALARI (ENDPOINTS) ===

from api.auth import get_current_user

# Tüm portföyleri getir
@app.route('/api/portfoyler', methods=['GET'])
def get_portfoyler():
    user = get_current_user()
    conn = get_db_connection()
    
    # Outer Circle (Örn. Müteahhit, Karacı vb.) sadece kendi ilanlarını/mülklerini görebilir
    if user and user.get('circle') == 'outer':
        portfoyler = conn.execute('SELECT * FROM portfoyler WHERE owner_id = ?', (user['id'],)).fetchall()
    else:
        # Inner Circle veya Public (anasayfa) erişimi 
        portfoyler = conn.execute('SELECT * FROM portfoyler').fetchall()
        
    conn.close()
    
    # SQLite Row nesnelerini dictionary'e çevir
    result = []
    lang = request.args.get('lang', 'tr').lower()

    for p in portfoyler:
        d = dict(p)
        # Dil bazlı içerik ezme (Phase 4)
        if lang == 'en' and d.get('baslik1_en'):
            d['baslik1'] = d['baslik1_en']
            d['baslik2'] = d['baslik2_en'] or d['baslik2']
            d['lokasyon'] = d['lokasyon_en'] or d['lokasyon']
            d['hikaye'] = d['hikaye_en'] or d['hikaye']
        elif lang == 'ar' and d.get('baslik1_ar'):
            d['baslik1'] = d['baslik1_ar']
            d['baslik2'] = d['baslik2_ar'] or d['baslik2']
            d['lokasyon'] = d['lokasyon_ar'] or d['lokasyon']
            d['hikaye'] = d['hikaye_ar'] or d['hikaye']

        if d['ozellikler']:
            d['ozellikler'] = json.loads(d['ozellikler'])
        result.append(d)
        
    return jsonify(result)

# Tek bir portföy getir (id ile)
@app.route('/api/portfoyler/<id>', methods=['GET'])
def get_portfoy(id):
    conn = get_db_connection()
    portfoy = conn.execute('SELECT * FROM portfoyler WHERE id = ?', (id,)).fetchone()
    conn.close()
    
    if portfoy is None:
        return jsonify({"error": "Portföy bulunamadı"}), 404
        
    d = dict(portfoy)
    lang = request.args.get('lang', 'tr').lower()

    # Dil bazlı içerik ezme (Phase 4)
    if lang == 'en' and d.get('baslik1_en'):
        d['baslik1'] = d['baslik1_en']
        d['baslik2'] = d['baslik2_en'] or d['baslik2']
        d['lokasyon'] = d['lokasyon_en'] or d['lokasyon']
        d['hikaye'] = d['hikaye_en'] or d['hikaye']
    elif lang == 'ar' and d.get('baslik1_ar'):
        d['baslik1'] = d['baslik1_ar']
        d['baslik2'] = d['baslik2_ar'] or d['baslik2']
        d['lokasyon'] = d['lokasyon_ar'] or d['lokasyon']
        d['hikaye'] = d['hikaye_ar'] or d['hikaye']

    if d['ozellikler']:
        d['ozellikler'] = json.loads(d['ozellikler'])
        
    return jsonify(d)

# Tüm ekibi getir
@app.route('/api/ekip', methods=['GET'])
def get_ekip():
    conn = get_db_connection()
    ekip = conn.execute('SELECT * FROM ekip').fetchall()
    conn.close()
    
    result = []
    for e in ekip:
        d = dict(e)
        if d.get('detaylar'):
            d['detaylar'] = json.loads(d['detaylar'])
        if d.get('uzmanlikAlanlari'):
            d['uzmanlikAlanlari'] = json.loads(d['uzmanlikAlanlari'])
        result.append(d)
        
    return jsonify(result)

# Lokal Dosya Yükleme (Upload) Uç Noktası
@app.route('/api/upload-image', methods=['POST'])
def upload_image():
    token = request.headers.get('Authorization')
    if not token or (not token.startswith('Bearer token-') and token != 'Bearer admin-token'):
        return jsonify({'error': 'Unauthorized'}), 403

    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400

    if file:
        filename = secure_filename(file.filename)
        safe_filename = f"{int(time.time())}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], safe_filename)
        file.save(filepath)
        file_url = f"/uploads/{safe_filename}"
        return jsonify({'url': file_url}), 200

# Yüklenen Lokal Dosyaları Servis Et (Public)
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# --- TODO: MOBİL UYGULAMA VE SATIŞ HUNİSİ API PLANLAMASI ---
# 1. Endpoint: GET /api/pipeline
#    - İşlev: Müşterileri (Leads) aşamalarına (Pipeline Stages) göre gruplayarak getirir (Kanban görünümü).
#
# 2. Endpoint: POST /api/leads/<id>/move
#    - İşlev: Müşteriyi bir aşamadan diğerine taşır ve tarihçeye log atar.
#
# 3. Endpoint: POST /api/leads/<id>/checkin
#    - İşlev: Saha personelinin konum bazlı check-in yapmasını sağlar (GPS verisi ile).
# -----------------------------------------------------------

# --- KARTEZYEN SİSTEM API ---

# Matris Verilerini Getir
@app.route('/api/leads/matrix', methods=['GET'])
def get_leads_matrix():
    # Filtre Parametrelerini Al
    min_match = request.args.get('min_match', type=int) # Örn: 60 (%60 ve üzeri uyum)
    segment = request.args.get('segment') # Örn: 'butce_odakli' (Temkinli)
    prop_type = request.args.get('type') # Örn: 'Villa'

    conn = get_db_connection()
    
    # Dinamik Sorgu Oluştur
    query = '''
        SELECT l.id, l.name, l.score_x, l.score_y, l.score_z, l.segment, l.status, p.alt_tip
        FROM leads l
        LEFT JOIN portfoyler p ON l.interest_property_id = p.id
        WHERE l.status NOT IN ('lost', 'converted')
    '''
    params = []

    if min_match:
        query += ' AND l.score_z >= ?'
        params.append(min_match)
    
    if segment:
        query += ' AND l.segment = ?'
        params.append(segment)
        
    if prop_type:
        query += ' AND p.alt_tip = ?'
        params.append(prop_type)

    leads = conn.execute(query, params).fetchall()
    conn.close()
    
    result = []
    for l in leads:
        result.append({
            "id": l['id'],
            "name": l['name'],
            "x": l['score_x'], # Alım Gücü
            "y": l['score_y'], # Aciliyet
            "z": l['score_z'], # Portföy Uyumu (Bubble Size)
            "segment": l['segment'],
            "status": l['status'],
            "looking_for": l['alt_tip'] # Ne arıyor?
        })
    return jsonify(result)

# Etkileşime Göre Puan Güncelle (Simülasyon)
@app.route('/api/leads/<int:id>/score', methods=['POST'])
def update_lead_score(id):
    data = request.json
    # Örn: { "action": "roi_calculator_used" } veya { "action": "high_budget_view" }
    
    conn = get_db_connection()
    lead = conn.execute('SELECT score_x, score_y, score_z FROM leads WHERE id = ?', (id,)).fetchone()
    
    if not lead:
        conn.close()
        return jsonify({"error": "Lead not found"}), 404
        
    new_x = lead['score_x']
    new_y = lead['score_y']
    new_z = lead['score_z']
    
    action = data.get('action')
    
    # Basit Puanlama Algoritması
    if action == 'roi_calculator':
        new_x = min(100, new_x + 10) # Yatırımcı profili, bütçe puanı artar
        new_y = min(100, new_y + 5)  # İlgileniyor, aciliyet biraz artar
        new_z = min(100, new_z + 5)  # Finansal araç kullanan genelde bizim portföye uygundur
    elif action == 'urgent_form':
        new_y = min(100, new_y + 30) # "Hemen Ara" dedi, aciliyet fırlar
    elif action == 'luxury_view':
        new_x = min(100, new_x + 5)  # Pahalı eve baktı
        new_z = min(100, new_z + 10) # Lüks portföyümüze bakıyorsa uyum yüksektir
    
    conn.execute('UPDATE leads SET score_x = ?, score_y = ?, score_z = ? WHERE id = ?', (new_x, new_y, new_z, id))
    conn.commit()
    conn.close()
    
    return jsonify({"status": "updated", "new_scores": {"x": new_x, "y": new_y, "z": new_z}})

# --- ARAMA LİSTESİ OLUŞTURUCU (CALL LIST BUILDER) ---

@app.route('/api/leads/call-list', methods=['GET'])
def get_call_list():
    # Parametreler
    limit = request.args.get('limit', default=20, type=int)
    days_threshold = request.args.get('days', default=3, type=int) # Kaç gündür aranmayanlar öncelikli?
    
    conn = get_db_connection()
    
    # ALGORİTMA:
    # 1. Hiç aranmamışlar (last_contacted_at IS NULL) -> En Yüksek Öncelik
    # 2. Puanı yüksek olup, X gündür aranmayanlar -> İkinci Öncelik
    # 3. Genel Puan Sıralaması (Ortalama Skor)
    
    query = '''
        SELECT *, 
            (score_x + score_y + IFNULL(score_z, 50)) / 3 as avg_score,
            CASE 
                WHEN last_contacted_at IS NULL THEN 1 -- Hiç aranmamış (En Acil)
                
                -- "Büyük Balık" (VIP/Stratejik): İhtimal düşük olsa bile (Urgency düşük), 
                -- kendisini "özel" hissettirmek için 7 günde bir mutlaka aranmalı/yazılmalı.
                WHEN segment = 'buyuk_balik' AND date(last_contacted_at) < date('now', '-7 days') THEN 1
                
                WHEN date(last_contacted_at) < date('now', '-' || ? || ' days') THEN 2 -- Unutulmuş (Acil)
                ELSE 3 -- Rutin
            END as priority_group
        FROM leads 
        WHERE status NOT IN ('lost', 'converted')
        ORDER BY 
            priority_group ASC, -- Önce acil gruplar
            (CASE WHEN segment = 'buyuk_balik' THEN 1 ELSE 0 END) DESC, -- Öncelik grubunda Büyük Balıklar en üste
            avg_score DESC -- Kendi içinde puanı yüksek olanlar
        LIMIT ?
    '''
    
    leads = conn.execute(query, (days_threshold, limit)).fetchall()
    conn.close()
    
    result = [dict(row) for row in leads]
    return jsonify(result)

@app.route('/api/leads/<int:id>/log-call', methods=['POST'])
def log_call(id):
    # Danışman "Aradım" butonuna bastığında bu çalışır.
    conn = get_db_connection()
    
    # Son görüşme tarihini güncelle
    conn.execute('''
        UPDATE leads 
        SET last_contacted_at = CURRENT_TIMESTAMP, status = 'contacted' 
        WHERE id = ?
    ''', (id,))
    
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": "Görüşme kaydedildi, müşteri listede alta kaydırıldı."})

# --- WHATSAPP AKILLI MESAJ OLUŞTURUCU ---

@app.route('/api/leads/<int:id>/whatsapp-template', methods=['GET'])
def get_whatsapp_template(id):
    # Opsiyonel: Belirli bir portföy hakkında konuşulacaksa ID'si
    property_id = request.args.get('property_id')
    
    conn = get_db_connection()
    lead = conn.execute('SELECT * FROM leads WHERE id = ?', (id,)).fetchone()
    
    prop = None
    if property_id:
        prop = conn.execute('SELECT * FROM portfoyler WHERE id = ?', (property_id,)).fetchone()
    
    conn.close()
    
    if not lead:
        return jsonify({"error": "Müşteri bulunamadı"}), 404

    # Müşteri Bilgileri
    name = lead['name'].split(' ')[0] # Sadece ilk isim (Samimiyet için)
    segment = lead['segment']
    
    # Veritabanından Şablon Çekme
    context_type = 'property' if prop else 'general'
    
    conn = get_db_connection()
    template_row = conn.execute(
        'SELECT template_text FROM message_templates WHERE segment = ? AND context_type = ?', 
        (segment, context_type)
    ).fetchone()
    
    # Eğer özel şablon yoksa varsayılanı çek
    if not template_row:
        template_row = conn.execute(
            'SELECT template_text FROM message_templates WHERE segment = ? AND context_type = ?', 
            ('default', 'general')
        ).fetchone()
    conn.close()
    
    raw_text = template_row['template_text'] if template_row else "Merhaba {name}, İmza Gayrimenkul'den ulaşıyorum."
    
    # Dinamik Değişkenleri Doldur
    message_text = raw_text.replace('{name}', name)
    if prop:
        message_text = message_text.replace('{property_title}', prop.get('baslik1', 'Bu portföy'))
        message_text = message_text.replace('{property_price}', prop.get('fiyat', ''))
        message_text = message_text.replace('{property_location}', prop.get('lokasyon', ''))

    # Telefon Numarası Temizleme (90532... formatına çevirme)
    phone = lead['phone']
    if phone:
        phone = phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        if phone.startswith('0'):
            phone = '9' + phone
        elif not phone.startswith('90'):
            phone = '90' + phone
            
    # WhatsApp Linki Oluşturma (URL Encode)
    encoded_message = urllib.parse.quote(message_text)
    whatsapp_url = f"https://wa.me/{phone}?text={encoded_message}"
    
    return jsonify({
        "lead_name": lead['name'],
        "segment": segment,
        "message_text": message_text,
        "whatsapp_link": whatsapp_url
    })

if __name__ == '__main__':
    # Flask sunucusunu başlat
    # Flask sunucusunu başlat (Docker için 0.0.0.0'a bağlamak şart)
    app.run(debug=True, host='0.0.0.0', port=8000)
