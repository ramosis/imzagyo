import json
from flask import request, jsonify, g
from shared.database import get_db
from modules.auth.decorators import require_inner_circle, login_required
from . import legal_bp

@legal_bp.route('/contracts', methods=['GET'])
@require_inner_circle
def get_contracts():
    with get_db() as conn:
        query = '''
            SELECT c.*, p.baslik1, p.refNo, u.username,
                   sp.name as seller_name, bp.name as buyer_name
            FROM contracts c
            LEFT JOIN portfoyler p ON c.property_id = p.id
            LEFT JOIN users u ON c.user_id = u.id
            LEFT JOIN parties sp ON c.seller_id = sp.id
            LEFT JOIN parties bp ON c.buyer_id = bp.id
            ORDER BY c.created_at DESC
        '''
        contracts = conn.execute(query).fetchall()
    return jsonify([dict(c) for c in contracts]), 200

@legal_bp.route('/contracts', methods=['POST'])
@login_required
def add_contract():
    data = request.json
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO contracts (property_id, user_id, seller_id, buyer_id, contract_type, special_conditions, status)
            VALUES (?,?,?,?,?,?,?)
        ''', (data.get('property_id'), g.user['id'], data.get('seller_id'), data.get('buyer_id'), 
              data.get('contract_type'), data.get('special_conditions'), 'draft'))
        conn.commit()
    return jsonify({'status': 'created'}), 201

@legal_bp.route('/templates', methods=['GET'])
def get_templates():
    with get_db() as conn:
        templates = conn.execute('SELECT * FROM contract_templates ORDER BY name').fetchall()
    return jsonify([dict(t) for t in templates])

@legal_bp.route('/prepared-contracts', methods=['POST'])
@login_required
def save_prepared_contract():
    data = request.json
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO prepared_contracts (property_id, template_id, user_id, content_json, status, seller_parties, buyer_parties)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (data.get('property_id'), data.get('template_id'), g.user['id'], 
              json.dumps(data.get('content_json', {})), 'draft', 
              json.dumps(data.get('seller_parties', [])), json.dumps(data.get('buyer_parties', []))))
        conn.commit()
    return jsonify({'id': cur.lastrowid}), 201
