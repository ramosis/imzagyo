from flask import Blueprint, request, jsonify
from shared.database import get_db_connection
from api.auth import require_inner_circle

settings_bp = Blueprint('settings_bp', __name__)

@settings_bp.route('/api/settings', methods=['GET'])
def get_settings():
    conn = get_db_connection()
    settings = conn.execute('SELECT key, value, description FROM site_settings').fetchall()
    conn.close()
    
    result = {s['key']: {'value': s['value'], 'description': s['description']} for s in settings}
    return jsonify(result)

@settings_bp.route('/api/settings', methods=['POST'])
@require_inner_circle
def update_settings():
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
        
    conn = get_db_connection()
    try:
        for key, value in data.items():
            conn.execute('UPDATE site_settings SET value = ?, updated_at = CURRENT_TIMESTAMP WHERE key = ?', (value, key))
        conn.commit()
        return jsonify({'message': 'Settings updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()
