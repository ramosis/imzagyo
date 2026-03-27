from flask import Blueprint, request, jsonify
from shared.database import get_db_connection

taxes_bp = Blueprint('taxes', __name__)

def admin_required(f):
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or (not token.startswith('Bearer token-') and token != 'Bearer admin-token'):
            return jsonify({'error': 'Unauthorized'}), 403
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@taxes_bp.route('/api/taxes', methods=['GET'])
@admin_required
def get_taxes():
    conn = get_db_connection()
    query = '''
        SELECT t.*, p.baslik1, p.refNo 
        FROM taxes t
        LEFT JOIN portfoyler p ON t.property_id = p.id
    '''
    taxes = conn.execute(query).fetchall()
    conn.close()
    return jsonify([dict(t) for t in taxes]), 200

@taxes_bp.route('/api/taxes', methods=['POST'])
@admin_required
def add_tax():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO taxes (property_id, tax_type, amount, due_date, status)
        VALUES (?,?,?,?,?)
    ''', (
        data.get('property_id'), data.get('tax_type'), data.get('amount'), data.get('due_date'), data.get('status')
    ))
    conn.commit()
    conn.close()
    return jsonify({'status': 'created'}), 201

@taxes_bp.route('/api/taxes/<int:id>', methods=['PUT'])
@admin_required
def update_tax(id):
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        UPDATE taxes SET property_id=?, tax_type=?, amount=?, due_date=?, status=? WHERE id=?
    ''', (
        data.get('property_id'), data.get('tax_type'), data.get('amount'), data.get('due_date'), data.get('status'), id
    ))
    conn.commit()
    conn.close()
    return jsonify({'status': 'updated'}), 200

@taxes_bp.route('/api/taxes/<int:id>', methods=['DELETE'])
@admin_required
def delete_tax(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM taxes WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'deleted'}), 200
