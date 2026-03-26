from flask import Blueprint, request, jsonify
from database import get_db_connection

maintenance_bp = Blueprint('maintenance', __name__)

def admin_required(f):
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or (not token.startswith('Bearer token-') and token != 'Bearer admin-token'):
            return jsonify({'error': 'Unauthorized'}), 403
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@maintenance_bp.route('/api/maintenance', methods=['GET'])
@admin_required
def get_maintenance():
    conn = get_db_connection()
    query = '''
        SELECT m.*, p.baslik1, p.refNo
        FROM maintenance_requests m
        LEFT JOIN portfoyler p ON m.property_id = p.id
    '''
    records = conn.execute(query).fetchall()
    conn.close()
    return jsonify([dict(r) for r in records]), 200

@maintenance_bp.route('/api/maintenance', methods=['POST'])
@admin_required
def add_maintenance():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO maintenance_requests (property_id, description, scheduled_date, status)
        VALUES (?,?,?,?)
    ''', (
        data.get('property_id'), data.get('description'), data.get('scheduled_date'), data.get('status', 'planned')
    ))
    conn.commit()
    conn.close()
    return jsonify({'status': 'created'}), 201

@maintenance_bp.route('/api/maintenance/<int:id>', methods=['PUT'])
@admin_required
def update_maintenance(id):
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        UPDATE maintenance_requests SET property_id=?, user_id=?, request_date=?, description=?, status=? WHERE id=?
    ''', (
        data.get('property_id'), data.get('user_id'), data.get('request_date'), data.get('description'), data.get('status'), id
    ))
    conn.commit()
    conn.close()
    return jsonify({'status': 'updated'}), 200

@maintenance_bp.route('/api/maintenance/<int:id>', methods=['DELETE'])
@admin_required
def delete_maintenance(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM maintenance_requests WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'deleted'}), 200
