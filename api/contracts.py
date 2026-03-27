from flask import Blueprint, request, jsonify
from shared.database import get_db_connection
import sqlite3
import json

contracts_bp = Blueprint('contracts', __name__)

def admin_required(f):
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or (not token.startswith('Bearer token-') and token != 'Bearer admin-token'):
            return jsonify({'error': 'Unauthorized'}), 403
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@contracts_bp.route('/api/contracts', methods=['GET'])
@admin_required
def get_contracts():
    conn = get_db_connection()
    # Join with users, portfoyler, and parties to get full information
    query = '''
        SELECT c.*, p.baslik1, p.refNo, u.username, u.role,
               sp.name as seller_name, bp.name as buyer_name
        FROM contracts c
        LEFT JOIN portfoyler p ON c.property_id = p.id
        LEFT JOIN users u ON c.user_id = u.id
        LEFT JOIN parties sp ON c.seller_id = sp.id
        LEFT JOIN parties bp ON c.buyer_id = bp.id
        ORDER BY c.created_at DESC
    '''
    contracts = conn.execute(query).fetchall()
    conn.close()
    return jsonify([dict(c) for c in contracts]), 200

@contracts_bp.route('/api/contracts', methods=['POST'])
@admin_required
def add_contract():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    user_id = data.get('user_id', 1)
    
    cur.execute('''
        INSERT INTO contracts (
            property_id, user_id, seller_id, buyer_id, contract_type, special_conditions, status
        )
        VALUES (?,?,?,?,?,?,?)
    ''', (
        data.get('property_id'), 
        user_id, 
        data.get('seller_id'), 
        data.get('buyer_id'), 
        data.get('contract_type'),
        data.get('special_conditions'),
        data.get('status', 'draft')
    ))
    conn.commit()
    conn.close()
    return jsonify({'status': 'created'}), 201

@contracts_bp.route('/api/contracts/<int:id>', methods=['PUT'])
@admin_required
def update_contract(id):
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        UPDATE contracts SET property_id=?, user_id=?, start_date=?, end_date=?, type=? WHERE id=?
    ''', (
        data.get('property_id'), data.get('user_id'), data.get('start_date'), data.get('end_date'), data.get('type'), id
    ))
    conn.commit()
    conn.close()
    return jsonify({'status': 'updated'}), 200

@contracts_bp.route('/api/contracts/<int:id>', methods=['DELETE'])
@admin_required
def delete_contract(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM contracts WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'deleted'}), 200

# Contract builder endpoints for wizard
@contracts_bp.route('/api/contract-builder/properties', methods=['GET'])
@admin_required
def get_properties_for_builder():
    """Get all properties for contract builder dropdown"""
    conn = get_db_connection()
    properties = conn.execute('SELECT id, baslik1, refNo, lokasyon, resim_hero FROM portfoyler ORDER BY baslik1').fetchall()
    conn.close()
    return jsonify([dict(prop) for prop in properties]), 200

@contracts_bp.route('/api/contract-builder/parties', methods=['GET'])
@admin_required
def get_parties_for_builder():
    """Get all parties for contract builder dropdown"""
    conn = get_db_connection()
    parties = conn.execute('SELECT id, tc_no, vkn, name, party_type FROM parties ORDER BY name').fetchall()
    conn.close()
    return jsonify([dict(party) for party in parties]), 200

@contracts_bp.route('/api/contract-builder/templates', methods=['GET'])
@admin_required
def get_contract_templates():
    """Get available contract templates"""
    conn = get_db_connection()
    templates = conn.execute('SELECT id, name, description FROM contract_templates ORDER BY name').fetchall()
    conn.close()
    return jsonify([dict(template) for template in templates]), 200

# Prepared contracts endpoints for wizard
@contracts_bp.route('/api/prepared-contracts', methods=['POST'])
def save_prepared_contract():
    """Save a prepared contract as draft"""
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Save the prepared contract with draft status
    cur.execute('''
        INSERT INTO prepared_contracts (
            property_id, template_id, user_id, content_json, status, seller_parties, buyer_parties
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('property_id'),
        data.get('template_id'),
        data.get('user_id'),
        json.dumps(data.get('content_json', {})),
        'draft',
        json.dumps(data.get('seller_parties', [])),
        json.dumps(data.get('buyer_parties', []))
    ))
    conn.commit()
    contract_id = cur.lastrowid
    conn.close()
    
    return jsonify({'id': contract_id, 'message': 'Contract saved as draft'}), 201

@contracts_bp.route('/api/prepared-contracts/<int:contract_id>', methods=['PUT'])
def update_prepared_contract(contract_id):
    """Update a prepared contract draft"""
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Update the prepared contract
    cur.execute('''
        UPDATE prepared_contracts SET
            property_id = ?,
            template_id = ?,
            user_id = ?,
            content_json = ?,
            seller_parties = ?,
            buyer_parties = ?
        WHERE id = ?
    ''', (
        data.get('property_id'),
        data.get('template_id'),
        data.get('user_id'),
        json.dumps(data.get('content_json', {})),
        json.dumps(data.get('seller_parties', [])),
        json.dumps(data.get('buyer_parties', [])),
        contract_id
    ))
    conn.commit()
    conn.close()
    
    return jsonify({'id': contract_id, 'message': 'Contract updated'}), 200

@contracts_bp.route('/api/prepared-contracts/<int:contract_id>', methods=['GET'])
def get_prepared_contract(contract_id):
    """Get a prepared contract by ID"""
    conn = get_db_connection()
    contract = conn.execute(
        'SELECT * FROM prepared_contracts WHERE id = ?', 
        (contract_id,)
    ).fetchone()
    conn.close()
    
    if contract:
        # Parse JSON fields
        contract_dict = dict(contract)
        contract_dict['content_json'] = json.loads(contract_dict['content_json']) if contract_dict['content_json'] else {}
        contract_dict['seller_parties'] = json.loads(contract_dict['seller_parties']) if contract_dict['seller_parties'] else []
        contract_dict['buyer_parties'] = json.loads(contract_dict['buyer_parties']) if contract_dict['buyer_parties'] else []
        return jsonify(contract_dict), 200
    else:
        return jsonify({'error': 'Contract not found'}), 404

@contracts_bp.route('/api/prepared-contracts/drafts', methods=['GET'])
def get_draft_contracts():
    """Get all draft contracts for a user"""
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id parameter is required'}), 400
        
    conn = get_db_connection()
    drafts = conn.execute(
        'SELECT * FROM prepared_contracts WHERE user_id = ? AND status = "draft" ORDER BY created_at DESC', 
        (user_id,)
    ).fetchall()
    conn.close()
    
    # Parse JSON fields for each draft
    draft_list = []
    for draft in drafts:
        draft_dict = dict(draft)
        draft_dict['content_json'] = json.loads(draft_dict['content_json']) if draft_dict['content_json'] else {}
        draft_dict['seller_parties'] = json.loads(draft_dict['seller_parties']) if draft_dict['seller_parties'] else []
        draft_dict['buyer_parties'] = json.loads(draft_dict['buyer_parties']) if draft_dict['buyer_parties'] else []
        draft_list.append(draft_dict)
    
    return jsonify(draft_list), 200

@contracts_bp.route('/api/prepared-contracts/<int:contract_id>/finalize', methods=['POST'])
def finalize_prepared_contract(contract_id):
    """Finalize a prepared contract (change status from draft to finalized)"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Update the contract status to finalized
    cur.execute('''
        UPDATE prepared_contracts SET status = 'finalized' WHERE id = ?
    ''', (contract_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'id': contract_id, 'message': 'Contract finalized'}), 200
