from flask import Blueprint, jsonify, request
import sqlite3
import os

tracking_bp = Blueprint('tracking', __name__)

DB_NAME = 'imza_emlak.db'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

@tracking_bp.route('/api/tracking/update', methods=['POST'])
def update_location():
    """Personel konumunu günceller."""
    data = request.json
    staff_id = data.get('staff_id')
    staff_name = data.get('staff_name')
    lat = data.get('lat')
    lng = data.get('lng')
    status = data.get('status', 'Active')

    if not all([staff_id, lat, lng]):
        return jsonify({"error": "staff_id, lat ve lng zorunludur"}), 400

    conn = get_db_connection()
    conn.execute('''
        INSERT INTO staff_locations (staff_id, staff_name, lat, lng, status)
        VALUES (?, ?, ?, ?, ?)
    ''', (staff_id, staff_name, lat, lng, status))
    conn.commit()
    conn.close()

    return jsonify({"message": "Konum güncellendi"}), 201

@tracking_bp.route('/api/tracking/live', methods=['GET'])
def get_live_locations():
    """Tüm aktif personellerin son konumlarını getirir."""
    conn = get_db_connection()
    # Her personel için en son (en büyük ID'li) kaydı getir
    locations = conn.execute('''
        SELECT * FROM staff_locations 
        WHERE id IN (SELECT MAX(id) FROM staff_locations GROUP BY staff_id)
        AND status = 'Active'
    ''').fetchall()
    conn.close()

    return jsonify([dict(l) for l in locations]), 200

@tracking_bp.route('/api/tracking/history/<int:staff_id>', methods=['GET'])
def get_staff_history(staff_id):
    """Belirli bir personelin geçmiş rotasını getirir."""
    date_filter = request.args.get('date') # Örn: 2026-03-23
    
    conn = get_db_connection()
    query = 'SELECT * FROM staff_locations WHERE staff_id = ?'
    params = [staff_id]
    
    if date_filter:
        query += ' AND date(timestamp) = ?'
        params.append(date_filter)
        
    query += ' ORDER BY timestamp ASC LIMIT 500' # Rota çizimi için kronolojik sıra
    
    history = conn.execute(query, params).fetchall()
    conn.close()

    return jsonify([dict(h) for h in history]), 200
