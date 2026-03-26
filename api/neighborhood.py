from flask import Blueprint, request, jsonify
from database import get_db_connection
from api.auth import get_current_user
from api.mail_service import send_email
import urllib.request
import urllib.error
import re
from datetime import datetime
import os
import threading

neighborhood_bp = Blueprint('neighborhood', __name__)

# A simple auth decorator (can be replaced with a more robust one)
def admin_required(f):
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        # This is a placeholder. Use a proper token validation system.
        if not token or (not token.startswith('Bearer token-') and token != 'Bearer admin-token'):
            return jsonify({'error': 'Unauthorized'}), 403
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@neighborhood_bp.route('/api/neighborhood/businesses', methods=['GET'])
def get_businesses():
    """
    Get a list of local businesses (esnaf).
    Query Params:
        - category: Filter by business category (e.g., 'Tesisatçı')
        - approved_only: 'true' to only get 'İmza Onaylı' businesses.
    """
    category = request.args.get('category')
    approved_only = request.args.get('approved_only', 'true').lower() == 'true'

    conn = get_db_connection()
    query = 'SELECT * FROM businesses WHERE 1=1'
    params = []

    if approved_only:
        query += ' AND is_approved = 1'
    
    if category:
        query += ' AND category = ?'
        params.append(category)

    query += ' ORDER BY rating DESC, name ASC'
    
    businesses = conn.execute(query, params).fetchall()
    conn.close()
    
    return jsonify([dict(b) for b in businesses]), 200

@neighborhood_bp.route('/api/neighborhood/businesses/<int:id>', methods=['GET'])
def get_business(id):
    """Get details of a single business."""
    conn = get_db_connection()
    business = conn.execute('SELECT * FROM businesses WHERE id = ?', (id,)).fetchone()
    conn.close()
    if business is None:
        return jsonify({'error': 'Business not found'}), 404
    return jsonify(dict(business)), 200

@neighborhood_bp.route('/api/neighborhood/businesses', methods=['POST'])
@admin_required
def add_business():
    """Add a new business (Admin only)."""
    data = request.json
    if not data or not data.get('name') or not data.get('category'):
        return jsonify({'error': 'Name and category are required'}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO businesses (name, category, description, phone, address, logo_url, is_approved)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['name'],
        data['category'],
        data.get('description'),
        data.get('phone'),
        data.get('address'),
        data.get('logo_url'),
        data.get('is_approved', True)
    ))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    
    return jsonify({'status': 'created', 'id': new_id}), 201

@neighborhood_bp.route('/api/neighborhood/listings', methods=['GET'])
def get_neighborhood_listings():
    """Mahalle bazlı ilanları getirir."""
    limit = request.args.get('limit', 6)
    mahalle_id = request.args.get('mahalle_id')
    
    conn = get_db_connection()
    query = 'SELECT * FROM portfoyler'
    params = []
    
    if mahalle_id:
        query += ' WHERE mahalle_id = ?'
        params.append(mahalle_id)
        
    query += ' ORDER BY id DESC LIMIT ?'
    params.append(limit)
    
    portfoyler = conn.execute(query, params).fetchall()
    conn.close()
    
    return jsonify([dict(p) for p in portfoyler]), 200

@neighborhood_bp.route('/api/neighborhood/pharmacies/duty', methods=['GET'])
def get_duty_pharmacies():
    """Kütahya Eczacı Odası web sitesinden anlık nöbetçi eczaneleri çeker."""
    try:
        url = "https://www.kutahyaeo.org.tr/nobetci-eczaneler/30"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8')

        pharmacies = []
        
        # Regex to match the typical structure of the Kutahya Eczacı Odası page
        # The page has patterns like: <h4>NAME - DISTRICT</h4><p>ADDRESS <a href="tel:PHONE">
        matches = re.finditer(r'<h4[^>]*>(.*?)</h4>(.*?)(?=<h4|$)', html, re.DOTALL | re.IGNORECASE)
        
        for match in matches:
            name_raw = match.group(1).strip()
            # Ignore unrelated h4 tags like Cookie warnings
            if "Çerez" in name_raw or "OBEN" in name_raw:
                continue
                
            block = match.group(2)
            
            # Extract phone
            phone_match = re.search(r'href=["\']tel:([^"\']+)["\']', block, re.IGNORECASE)
            phone = phone_match.group(1).strip() if phone_match else ""
            
            # Extract maps link to get coordinates
            maps_match = re.search(r'href=["\']https://maps\.google\.com/maps\?q=([^"\']+)["\']', block, re.IGNORECASE)
            lat, lng = None, None
            if maps_match:
                coords = maps_match.group(1).split(',')
                if len(coords) == 2:
                    lat, lng = coords[0].strip(), coords[1].strip()
            
            # Clean up address by removing HTML tags
            # Address is usually the text before the phone link
            addr_text = re.sub(r'<[^>]+>', ' ', block).strip()
            # Remove phone number from address if it leaked
            if phone:
                addr_text = addr_text.replace(phone, '').strip()
            # Remove redundant whitespaces
            addr_text = re.sub(r'\s+', ' ', addr_text).strip()
            
            # Remove the appended " Haritada görüntülemek için tıklayınız..." text
            addr_text = addr_text.replace("Haritada görüntülemek için tıklayınız...", "").strip()
            
            if name_raw:
                pharmacies.append({
                    "name": name_raw,
                    "address": addr_text,
                    "phone": phone,
                    "latitude": lat,
                    "longitude": lng,
                    "is_duty": True
                })

        # Fallback if parsing completely fails but we know the site is up
        if not pharmacies:
            raise ValueError("Kayıt bulunamadı veya site yapısı değişmiş olabilir.")

        return jsonify({
            "status": "success",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "data": pharmacies
        }), 200

    except Exception as e:
        # Hata durumunda loglama yapılabilir, şimdilik mock veri veya hata dönüyoruz
        return jsonify({
            "status": "error",
            "message": f"Nöbetçi eczaneler alınırken hata oluştu: {str(e)}",
            "data": []
        }), 500

@neighborhood_bp.route('/api/neighborhood/relocation-guide', methods=['GET'])
def get_relocation_guide():
    """Yeni taşınanlar için rehber verilerini getirir."""
    return jsonify({
        'resmi': [
            {'title': 'Elektrik Aboneliği', 'provider': 'EnerjiSA', 'link': 'https://www.enerjisa.com.tr', 'status': 'Abonelik Gerekli'},
            {'title': 'Su Aboneliği', 'provider': 'İSKİ', 'link': 'https://www.iski.istanbul', 'status': 'Abonelik Gerekli'},
            {'title': 'Doğalgaz Aboneliği', 'provider': 'İGDAŞ', 'link': 'https://www.igdas.istanbul', 'status': 'Abonelik Gerekli'}
        ],
        'altyapi': [
            {'title': 'İnternet/Fiber', 'provider': 'Türk Telekom / Superonline', 'desc': 'Binada fiber altyapı mevcuttur.'},
            {'title': 'Çöp Toplama', 'desc': 'Hafta içi her gün 22:00-23:00 arası kapıdan alınmaktadır.'}
        ],
        'hizmetler': [
            {'title': 'Sucu', 'name': 'Erikli Maslak', 'phone': '444 0 222'},
            {'title': 'Nakliye', 'name': 'Bakırcı Lojistik', 'phone': '0212 999 88 77'}
        ]
    }), 200

# --- PROPERTY & APARTMENT MANAGEMENT ---

@neighborhood_bp.route('/api/neighborhood/my-unit', methods=['GET'])
def get_my_unit():
    """Kullanıcının dairesine ait borç ve aidat bilgilerini getirir."""
    unit_id = request.args.get('unit_id', default=1, type=int) # Demo için
    conn = get_db_connection()
    unit = conn.execute('SELECT * FROM property_units WHERE id = ?', (unit_id,)).fetchone()
    dues = conn.execute('SELECT * FROM dues_payments WHERE unit_id = ? ORDER BY period DESC', (unit_id,)).fetchall()
    conn.close()
    
    if not unit:
        return jsonify({"error": "Ünite bulunamadı"}), 404
        
    return jsonify({
        'unit': dict(unit),
        'payments': [dict(d) for d in dues]
    }), 200

@neighborhood_bp.route('/api/neighborhood/expenses', methods=['GET'])
def get_apartment_expenses():
    """Apartman/Site yönetiminin şeffaf harcama listesini getirir."""
    mahalle_id = request.args.get('mahalle_id', default=1, type=int)
    conn = get_db_connection()
    expenses = conn.execute('SELECT * FROM apartment_expenses WHERE mahalle_id = ? ORDER BY expense_date DESC', (mahalle_id,)).fetchall()
    conn.close()
    
    return jsonify([dict(e) for e in expenses]), 200

# --- CONCIERGE SERVICES ---

@neighborhood_bp.route('/api/neighborhood/shuttle', methods=['GET'])
def get_shuttle_schedule():
    """Servis saatlerini getirir."""
    conn = get_db_connection()
    schedule = conn.execute('SELECT * FROM shuttle_schedule').fetchall()
    conn.close()
    return jsonify([dict(s) for s in schedule]), 200

@neighborhood_bp.route('/api/neighborhood/facilities', methods=['GET'])
def get_facilities():
    """Sitedeki tesisleri listeler."""
    conn = get_db_connection()
    facilities = conn.execute('SELECT * FROM neighborhood_facilities').fetchall()
    conn.close()
    return jsonify([dict(f) for f in facilities]), 200

@neighborhood_bp.route('/api/neighborhood/reservations', methods=['POST'])
def create_reservation():
    """Tesis rezervasyonu oluşturur."""
    data = request.json
    if not data or 'facility_id' not in data or 'date' not in data:
        return jsonify({'error': 'Eksik veri'}), 400
        
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO neighborhood_reservations (facility_id, user_name, reservation_date, time_slot)
        VALUES (?, ?, ?, ?)
    ''', (data['facility_id'], data.get('name', 'Misafir'), data['date'], data.get('time', '12:00')))
    
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({'status': 'confirmed', 'id': new_id}), 201

@neighborhood_bp.route('/api/neighborhood/reservations/calendar', methods=['GET'])
def get_reservation_calendar():
    """Belirli bir tesis ve tarih aralığı/hafta için rezervasyonları getirir."""
    facility_id = request.args.get('facility_id')
    start_date = request.args.get('start_date') # Örn: 2026-03-23
    end_date = request.args.get('end_date')     # Örn: 2026-03-29

    if not all([facility_id, start_date, end_date]):
        return jsonify({'error': 'facility_id, start_date ve end_date zorunludur'}), 400

    conn = get_db_connection()
    reservations = conn.execute('''
        SELECT id, reservation_date, time_slot, status 
        FROM neighborhood_reservations 
        WHERE facility_id = ? AND reservation_date BETWEEN ? AND ?
    ''', (facility_id, start_date, end_date)).fetchall()
    conn.close()

    return jsonify([dict(r) for r in reservations]), 200

# --- APARTMENT POLLS & VOTING ---

@neighborhood_bp.route('/api/neighborhood/polls', methods=['GET'])
def get_polls():
    """Mahalle/Apartman anketlerini listeler."""
    mahalle_id = request.args.get('mahalle_id', default=1, type=int)
    conn = get_db_connection()
    polls = conn.execute('SELECT * FROM apartment_polls WHERE mahalle_id = ? ORDER BY created_at DESC', (mahalle_id,)).fetchall()
    
    results = []
    for p in polls:
        poll_dict = dict(p)
        # Oylama istatistiklerini getir
        votes = conn.execute('SELECT selected_option, COUNT(*) as count FROM poll_votes WHERE poll_id = ? GROUP BY selected_option', (p['id'],)).fetchall()
        poll_dict['stats'] = {v['selected_option']: v['count'] for v in votes}
        poll_dict['total_votes'] = sum(v['count'] for v in votes)
        results.append(poll_dict)
        
    conn.close()
    return jsonify(results), 200

@neighborhood_bp.route('/api/neighborhood/polls/vote', methods=['POST'])
def cast_vote():
    """Ankete oy verir."""
    data = request.json
    if not data or 'poll_id' not in data or 'option' not in data:
        return jsonify({'error': 'Poll ID and option are required'}), 400
        
    user_name = data.get('user_name', 'Mahalle Sakini')
    
    conn = get_db_connection()
    # Mükerrer oy kontrolü (Demo için basitçe kullanıcı adına göre)
    already_voted = conn.execute('SELECT id FROM poll_votes WHERE poll_id = ? AND user_name = ?', (data['poll_id'], user_name)).fetchone()
    
    if already_voted:
        conn.close()
        return jsonify({'error': 'Zaten oy verdiniz'}), 403
        
    conn.execute('INSERT INTO poll_votes (poll_id, user_name, selected_option) VALUES (?, ?, ?)', 
                 (data['poll_id'], user_name, data['option']))
    conn.commit()
    conn.close()
    
    return jsonify({'status': 'voted'}), 201

@neighborhood_bp.route('/api/neighborhood/expenses', methods=['GET'])
def get_detailed_expenses():
    """Apartman harcamalarının detaylı listesini getirir."""
    # Demo için 'bogaz-villa' mülkünü baz alıyoruz
    property_id = request.args.get('property_id', default='bogaz-villa')
    conn = get_db_connection()
    expenses = conn.execute('''
        SELECT id, expense_type as title, amount, expense_date, description, invoice_file as receipt_url 
        FROM apartment_expenses 
        WHERE property_id = ? 
        ORDER BY expense_date DESC
    ''', (property_id,)).fetchall()
    conn.close()
    return jsonify([dict(r) for r in expenses]), 200

# --- MAHALLE BAZLI İLANLAR ---

@neighborhood_bp.route('/api/neighborhood/demands', methods=['POST'])
def create_demand():
    """Yeni bir mahalle talebi (Gayrimenkul, Hizmet vb.) oluşturur."""
    data = request.json
    if not data or not data.get('type') or not data.get('content'):
        return jsonify({'error': 'Type and content are required'}), 400
        
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO neighborhood_demands (type, content, user_name, user_phone)
        VALUES (?, ?, ?, ?)
    ''', (data['type'], data['content'], data.get('user_name'), data.get('user_phone')))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    
    # E-posta Bildirimi Gönder (Asenkron)
    try:
        admin_email = os.environ.get("ADMIN_EMAIL", "info@imzagayrimenkul.com")
        subject = f"Yeni Mahalle Talebi: {data['type']}"
        body = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 10px;">
            <h2 style="color: #D4AF37; text-align: center;">Yeni İmza Mahalle Talebi</h2>
            <p><strong>Talep Türü:</strong> {data['type']}</p>
            <p><strong>Ad Soyad:</strong> {data.get('user_name', 'Bilinmiyor')}</p>
            <p><strong>Telefon:</strong> {data.get('user_phone', 'Bilinmiyor')}</p>
            <hr style="border: 0; border-top: 1px solid #eeeeee; margin: 20px 0;">
            <p><strong>Detaylar:</strong></p>
            <p style="background-color: #f9f9f9; padding: 15px; border-radius: 5px;">{data['content']}</p>
            <p style="font-size: 12px; color: #777777; text-align: center; margin-top: 30px;">
                Talebi yönetmek için İmza Portal'a giriş yapın.
            </p>
        </div>
        """
        threading.Thread(target=send_email, args=(subject, admin_email, body)).start()
    except Exception as e:
        print(f"E-posta bildirim hatası: {e}")
        
    return jsonify({'status': 'created', 'id': new_id}), 201

@neighborhood_bp.route('/api/neighborhood/demands', methods=['GET'])
@admin_required
def get_demands():
    """Tüm mahalle taleplerini listeler (Admin Only)."""
    conn = get_db_connection()
    demands = conn.execute('SELECT * FROM neighborhood_demands ORDER BY created_at DESC').fetchall()
    conn.close()
    return jsonify([dict(d) for d in demands]), 200

# --- ESNAF BAŞVURUSU (PUBLIC REGISTRATION) ---

@neighborhood_bp.route('/api/neighborhood/businesses/register', methods=['POST'])
def register_business():
    """Esnafın kendi başvurusunu yapması (Onaysız olarak kaydedilir)."""
    data = request.json
    if not data or not data.get('name') or not data.get('category'):
        return jsonify({'error': 'Name and category are required'}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO businesses (name, category, description, phone, address, is_approved)
        VALUES (?, ?, ?, ?, ?, 0)
    ''', (
        data['name'],
        data['category'],
        data.get('description'),
        data.get('phone'),
        data.get('address')
    ))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    
    return jsonify({'status': 'registered', 'id': new_id, 'message': 'Başvurunuz alındı, onay bekliyor.'}), 201

@neighborhood_bp.route('/api/neighborhood/businesses/<int:id>', methods=['PUT'])
@admin_required
def update_business(id):
    """Update a business (Admin only)."""
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    # This is a simplified update. A real-world app might update fields selectively.
    cur.execute('''
        UPDATE businesses SET name=?, category=?, description=?, phone=?, address=?, logo_url=?, is_approved=?
        WHERE id = ?
    ''', (
        data.get('name'), data.get('category'), data.get('description'), data.get('phone'),
        data.get('address'), data.get('logo_url'), data.get('is_approved'), id
    ))
    conn.commit()
    conn.close()
    if cur.rowcount == 0:
        return jsonify({'error': 'Business not found'}), 404
    return jsonify({'status': 'updated'}), 200

@neighborhood_bp.route('/api/neighborhood/businesses/<int:id>', methods=['DELETE'])
@admin_required
def delete_business(id):
    """Delete a business (Admin only)."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM businesses WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    if cur.rowcount == 0:
        return jsonify({'error': 'Business not found'}), 404
    return jsonify({'status': 'deleted'}), 200

# --- KOMŞULUK DUVARI (WALL) ENDPOINTS ---

@neighborhood_bp.route('/api/neighborhood/posts', methods=['GET'])
def get_wall_posts():
    """
    Komşuluk duvarındaki gönderileri getirir.
    Query Params:
        - type: Filtreleme (satilik, etkinlik vb.)
        - limit: Kaç gönderi geleceği (default 20)
    """
    post_type = request.args.get('type')
    limit = request.args.get('limit', 20)
    
    conn = get_db_connection()
    query = '''
        SELECT p.id, p.user_id, p.type, p.content, p.image_url, p.created_at, u.username, u.role 
        FROM neighborhood_posts p
        LEFT JOIN users u ON p.user_id = u.id
        WHERE 1=1
    '''
    params = []
    
    if post_type:
        query += ' AND p.type = ?'
        params.append(post_type)
        
    query += ' ORDER BY p.created_at DESC LIMIT ?'
    params.append(limit)
    
    posts = conn.execute(query, params).fetchall()
    conn.close()
    
    return jsonify([dict(p) for p in posts]), 200

@neighborhood_bp.route('/api/neighborhood/posts', methods=['POST'])
def create_wall_post():
    """Yeni bir duvar gönderisi oluşturur."""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401
        
    data = request.json
    content = data.get('content')
    post_type = data.get('type')

    # İzin verilen gönderi tipleri (Sosyal medya karmaşasını önlemek için)
    allowed_types = ['ulasim', 'paylasim', 'yardim', 'duyuru']
    
    if not content or not post_type:
        return jsonify({'error': 'Content and type are required'}), 400
        
    if post_type not in allowed_types:
        return jsonify({'error': 'Invalid post type. Allowed: ' + ', '.join(allowed_types)}), 400
        
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO neighborhood_posts (user_id, type, content, image_url)
        VALUES (?, ?, ?, ?)
    ''', (user['id'], post_type, content, data.get('image_url')))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    
    return jsonify({'status': 'created', 'id': new_id}), 201

# --- MÜLK VE BİNA YÖNETİMİ (PROPERTY & UNIT MANAGEMENT) ---

@neighborhood_bp.route('/api/neighborhood/property/<property_id>/units', methods=['GET'])
def get_property_units(property_id):
    """Bir binaya (portföye) ait tüm bağımsız bölümleri (daire/dükkan) getirir."""
    conn = get_db_connection()
    units = conn.execute('''
        SELECT * FROM property_units
        WHERE property_id = ?
        ORDER BY unit_number ASC
    ''', (property_id,)).fetchall()
    
    # Her daire için aktif kiracı/sahip bilgisini de çekebiliriz
    result = []
    for u in units:
        unit_dict = dict(u)
        active_lease = conn.execute('''
            SELECT l.id, l.tenant_id, u.username as tenant_name, l.rent_amount, l.end_date
            FROM leases l
            JOIN users u ON l.tenant_id = u.id
            WHERE l.property_unit_id = ? AND l.status = 'Aktif'
            LIMIT 1
        ''', (unit_dict['id'],)).fetchone()
        
        if active_lease:
            unit_dict['active_lease'] = dict(active_lease)
        else:
            unit_dict['active_lease'] = None
            
        result.append(unit_dict)
        
    conn.close()
    return jsonify(result), 200

@neighborhood_bp.route('/api/neighborhood/property/<property_id>/units', methods=['POST'])
@admin_required
def add_property_unit(property_id):
    """Binaya yeni bir bağımsız bölüm (daire/dükkan) ekler."""
    data = request.json
    unit_number = data.get('unit_number')
    if not unit_number:
        return jsonify({'error': 'Daire/Kapı numarası zorunludur'}), 400
        
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO property_units (property_id, unit_number, floor, unit_type, area_sqm, status)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        property_id,
        unit_number,
        data.get('floor'),
        data.get('unit_type', 'Konut'),
        data.get('area_sqm'),
        data.get('status', 'Boş')
    ))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    
    return jsonify({'status': 'created', 'id': new_id}), 201


@neighborhood_bp.route('/api/neighborhood/property/<property_id>/cashbox', methods=['GET'])
def get_transparent_cashbox(property_id):
    """Şeffaf Kasa (Transparent Cash Box) raporunu getirir."""
    # Toplanan Aidatlar (dues_payments üzerinden)
    # Giderler (apartment_expenses üzerinden)
    conn = get_db_connection()
    
    # 1. Gelirler (Sadece Ödendi statüsündeki Aidat ve Demirbaşlar)
    incomes = conn.execute('''
        SELECT d.payment_type, SUM(d.amount) as total
        FROM dues_payments d
        JOIN property_units pu ON d.property_unit_id = pu.id
        WHERE pu.property_id = ? AND d.status = 'Ödendi'
        GROUP BY d.payment_type
    ''', (property_id,)).fetchall()
    
    total_income = sum([row['total'] for row in incomes]) if incomes else 0
    
    # 2. Giderler
    expenses = conn.execute('''
        SELECT expense_type, SUM(amount) as total
        FROM apartment_expenses
        WHERE property_id = ?
        GROUP BY expense_type
    ''', (property_id,)).fetchall()
    
    total_expense = sum([row['total'] for row in expenses]) if expenses else 0
    
    # 3. Son 5 İşlem (Özet Liste İçin)
    recent_transactions = []
    
    recent_incomes = conn.execute('''
        SELECT 'GELİR' as type, d.payment_type as category, d.amount, d.paid_date as date, u.username as source
        FROM dues_payments d
        JOIN property_units pu ON d.property_unit_id = pu.id
        JOIN users u ON d.user_id = u.id
        WHERE pu.property_id = ? AND d.status = 'Ödendi'
        ORDER BY d.paid_date DESC LIMIT 5
    ''', (property_id,)).fetchall()
    
    recent_exp = conn.execute('''
        SELECT 'GİDER' as type, expense_type as category, amount, expense_date as date, description as source
        FROM apartment_expenses
        WHERE property_id = ?
        ORDER BY expense_date DESC LIMIT 5
    ''', (property_id,)).fetchall()
    
    for inc in recent_incomes:
        recent_transactions.append(dict(inc))
    for exp in recent_exp:
        recent_transactions.append(dict(exp))
        
    # Tarihe göre sırala
    recent_transactions.sort(key=lambda x: x['date'], reverse=True)
    
    conn.close()
    
    return jsonify({
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': total_income - total_expense,
        'income_breakdown': [dict(i) for i in incomes],
        'expense_breakdown': [dict(e) for e in expenses],
        'recent_transactions': recent_transactions[:10]
    }), 200

@neighborhood_bp.route('/api/neighborhood/units/<unit_id>/leases', methods=['GET'])
def get_unit_leases(unit_id):
    """Bir bağımsız bölümün kira geçmişini ve aktif sözleşmesini getirir."""
    conn = get_db_connection()
    leases = conn.execute('''
        SELECT l.*, u.username as tenant_name, u.telefon as tenant_phone 
        FROM leases l
        JOIN users u ON l.tenant_id = u.id
        WHERE l.property_unit_id = ?
        ORDER BY l.start_date DESC
    ''', (unit_id,)).fetchall()
    conn.close()
    return jsonify([dict(row) for row in leases]), 200

@neighborhood_bp.route('/api/neighborhood/units/<unit_id>/leases', methods=['POST'])
@admin_required
def add_unit_lease(unit_id):
    """Yeni bir kira sözleşmesi başlatır."""
    data = request.json
    tenant_id = data.get('tenant_id')
    rent_amount = data.get('rent_amount')
    start_date = data.get('start_date')
    
    if not all([tenant_id, rent_amount, start_date]):
        return jsonify({'error': 'Kiracı, kira bedeli ve başlangıç tarihi zorunludur.'}), 400
        
    conn = get_db_connection()
    cur = conn.cursor()
    # Mevcut kirayı pasif et
    cur.execute('''
        UPDATE leases SET status = 'Sonlandı' 
        WHERE property_unit_id = ? AND status = 'Aktif'
    ''', (unit_id,))
    
    # Yeni kirayı ekle
    cur.execute('''
        INSERT INTO leases (property_unit_id, tenant_id, start_date, end_date, rent_amount, currency, payment_day, deposit_amount)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        unit_id, tenant_id, start_date,
        data.get('end_date'), rent_amount,
        data.get('currency', 'TRY'),
        data.get('payment_day', 1),
        data.get('deposit_amount', 0)
    ))
    
    # Daire durumunu güncelle
    cur.execute('UPDATE property_units SET status = "Dolu" WHERE id = ?', (unit_id,))
    
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    
    return jsonify({'status': 'created', 'id': new_id}), 201

@neighborhood_bp.route('/api/neighborhood/dues', methods=['POST'])
@admin_required
def add_due_payment():
    """Yeni bir aidat, kira veya ek demirbaş borcu tahakkuk ettirir."""
    data = request.json
    property_unit_id = data.get('property_unit_id')
    amount = data.get('amount')
    due_date = data.get('due_date')
    payment_type = data.get('payment_type', 'AIDAT')
    
    if not all([property_unit_id, amount, due_date]):
        return jsonify({'error': 'Eksik bilgi girdiniz.'}), 400
        
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Dairenin aktif kiracısını bul
    active_lease = cur.execute('''
        SELECT id, tenant_id FROM leases 
        WHERE property_unit_id = ? AND status = 'Aktif' LIMIT 1
    ''', (property_unit_id,)).fetchone()
    
    user_id = data.get('user_id')
    lease_id = None
    if active_lease:
        user_id = user_id or active_lease['tenant_id']
        lease_id = active_lease['id']
        
    if not user_id:
        # Eğer manuel atanmadıysa ve aktif kiracı yoksa hata verir
        return jsonify({'error': 'Bu daire için sorumlu bir kullanıcı bulunamadı.'}), 400
        
    cur.execute('''
        INSERT INTO dues_payments (lease_id, property_unit_id, user_id, payment_type, amount, due_date, description)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        lease_id, property_unit_id, user_id, payment_type, amount, due_date, data.get('description')
    ))
    
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    
    return jsonify({'status': 'created', 'id': new_id}), 201