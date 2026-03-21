from flask import Blueprint, request, jsonify
from database import get_db_connection
from api.auth import get_current_user

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
    
    listings = conn.execute(query, params).fetchall()
    conn.close()
    
    return jsonify([dict(l) for l in listings]), 200

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