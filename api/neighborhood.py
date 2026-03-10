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