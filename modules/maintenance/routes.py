from flask import request, jsonify
from shared.database import get_db
from modules.auth.decorators import require_inner_circle
from . import maintenance_bp

@maintenance_bp.route('/tickets', methods=['GET'])
@require_inner_circle
def get_tickets():
    with get_db() as conn:
        tickets = conn.execute('SELECT * FROM maintenance_tickets ORDER BY created_at DESC').fetchall()
    return jsonify([dict(t) for t in tickets])

@maintenance_bp.route('/tickets', methods=['POST'])
@require_inner_circle
def create_ticket():
    data = request.json
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute('INSERT INTO maintenance_tickets (property_id, title, description, priority, status) VALUES (?,?,?,?,?)',
                    (data.get('property_id'), data.get('title'), data.get('description'), 
                     data.get('priority', 'medium'), 'open'))
        conn.commit()
    return jsonify({'status': 'created'}), 201
