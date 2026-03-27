from datetime import datetime
from flask import request, jsonify
from shared.database import get_db
from modules.auth.decorators import login_required
from . import crm_bp

# Contact Directory
@crm_bp.route('/contacts', methods=['GET'])
@login_required
def get_contacts():
    category = request.args.get('category')
    with get_db() as conn:
        query = 'SELECT * FROM contacts'
        params = []
        if category:
            query += ' WHERE category = ?'
            params.append(category)
        query += ' ORDER BY name ASC'
        contacts = conn.execute(query, params).fetchall()
    return jsonify([dict(row) for row in contacts])

@crm_bp.route('/contacts', methods=['POST'])
@login_required
def add_contact():
    data = request.json
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO contacts (name, phone, email, address, occupation, category, tags, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (data.get('name'), data.get('phone'), data.get('email'), data.get('address'), 
              data.get('occupation'), data.get('category', 'general'), data.get('tags'), data.get('notes')))
        conn.commit()
    return jsonify({"status": "created"}), 201

# Staff Tracking
@crm_bp.route('/tracking/update', methods=['POST'])
def update_location():
    data = request.json
    if not all([data.get('staff_id'), data.get('lat'), data.get('lng')]):
        return jsonify({"error": "Missing fields"}), 400
    with get_db() as conn:
        conn.execute('INSERT INTO staff_locations (staff_id, staff_name, lat, lng, status) VALUES (?, ?, ?, ?, ?)',
                     (data['staff_id'], data.get('staff_name'), data['lat'], data['lng'], data.get('status', 'Active')))
        conn.commit()
    return jsonify({"message": "Location updated"}), 201

@crm_bp.route('/tracking/live', methods=['GET'])
@login_required
def get_live_locations():
    with get_db() as conn:
        locations = conn.execute('''
            SELECT * FROM staff_locations WHERE id IN (SELECT MAX(id) FROM staff_locations GROUP BY staff_id) AND status = 'Active'
        ''').fetchall()
    return jsonify([dict(l) for l in locations]), 200
