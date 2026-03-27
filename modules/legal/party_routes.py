from flask import request, jsonify
from shared.database import get_db
from modules.auth.decorators import require_inner_circle
from . import legal_bp

# Party Management
@legal_bp.route('/parties', methods=['GET'])
@require_inner_circle
def get_parties():
    with get_db() as conn:
        parties = conn.execute('SELECT * FROM parties ORDER BY name').fetchall()
    return jsonify([dict(p) for p in parties])

@legal_bp.route('/parties', methods=['POST'])
@require_inner_circle
def add_party():
    data = request.json
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute('INSERT INTO parties (name, tc_no, vkn, phone, email, address, party_type) VALUES (?,?,?,?,?,?,?)',
                    (data.get('name'), data.get('tc_no'), data.get('vkn'), data.get('phone'), 
                     data.get('email'), data.get('address'), data.get('party_type')))
        conn.commit()
    return jsonify({'status': 'created'}), 201

# Inspection Reports
@legal_bp.route('/inspections', methods=['GET'])
@require_inner_circle
def get_inspections():
    with get_db() as conn:
        inspections = conn.execute('''
            SELECT i.*, p.baslik1, u.username 
            FROM inspections i 
            LEFT JOIN portfoyler p ON i.property_id = p.id 
            LEFT JOIN users u ON i.inspector_id = u.id
        ''').fetchall()
    return jsonify([dict(i) for i in inspections])
