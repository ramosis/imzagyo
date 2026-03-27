from flask import Blueprint, request, jsonify
from shared.database import get_db_connection

contract_templates_bp = Blueprint('contract_templates', __name__)

def admin_required(f):
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or (not token.startswith('Bearer token-') and token != 'Bearer admin-token'):
            return jsonify({'error': 'Unauthorized'}), 403
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@contract_templates_bp.route('/api/contract-templates', methods=['GET'])
@admin_required
def get_templates():
    conn = get_db_connection()
    templates = conn.execute('SELECT * FROM contract_templates').fetchall()
    conn.close()
    return jsonify([dict(t) for t in templates]), 200

@contract_templates_bp.route('/api/contract-templates/<int:template_id>/clauses', methods=['GET'])
@admin_required
def get_clauses(template_id):
    conn = get_db_connection()
    clauses = conn.execute('SELECT * FROM contract_clauses WHERE template_id = ? ORDER BY sort_order', (template_id,)).fetchall()
    conn.close()
    return jsonify([dict(c) for c in clauses]), 200

@contract_templates_bp.route('/api/prepared-contracts', methods=['POST'])
@admin_required
def save_prepared_contract():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO prepared_contracts (property_id, template_id, user_id, content_json, status)
        VALUES (?,?,?,?,?)
    ''', (
        data.get('property_id'),
        data.get('template_id'),
        data.get('user_id'),
        data.get('content_json'),
        data.get('status', 'draft')
    ))
    new_id = cur.lastrowid
    conn.commit()
    conn.close()
    return jsonify({'id': new_id, 'status': 'saved'}), 201

@contract_templates_bp.route('/api/prepared-contracts', methods=['GET'])
@admin_required
def get_prepared_contracts():
    conn = get_db_connection()
    query = '''
        SELECT pc.*, p.baslik1 as property_title, p.refNo, ct.name as template_name
        FROM prepared_contracts pc
        JOIN portfoyler p ON pc.property_id = p.id
        JOIN contract_templates ct ON pc.template_id = ct.id
        ORDER BY pc.created_at DESC
    '''
    contracts = conn.execute(query).fetchall()
    conn.close()
    return jsonify([dict(c) for c in contracts]), 200
