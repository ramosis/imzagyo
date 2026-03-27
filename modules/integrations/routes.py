from flask import request, jsonify
from shared.database import get_db
from modules.auth.decorators import require_inner_circle
from . import integrations_bp

PLATFORMS = {
    'listing': [{'key': 'sahibinden', 'name': 'Sahibinden.com'}, {'key': 'hepsiemlak', 'name': 'Hepsiemlak.com'}],
    'social': [{'key': 'instagram', 'name': 'Instagram'}, {'key': 'facebook', 'name': 'Facebook'}]
}

@integrations_bp.route('/platforms', methods=['GET'])
def get_platforms():
    return jsonify(PLATFORMS)

@integrations_bp.route('/connections', methods=['GET'])
@require_inner_circle
def get_connections():
    with get_db() as conn:
        connections = conn.execute('SELECT * FROM platform_connections ORDER BY platform').fetchall()
    return jsonify([dict(c) for c in connections])

@integrations_bp.route('/publish/generate', methods=['POST'])
@require_inner_circle
def generate_listing():
    data = request.json
    property_id = data.get('property_id')
    platform = data.get('platform')
    with get_db() as conn:
        prop = conn.execute('SELECT * FROM portfoyler WHERE id = ?', (property_id,)).fetchone()
    if not prop: return jsonify({'error': 'Not found'}), 404
    # Simple template logic for brevity
    return jsonify({'title': f"{prop['baslik1']} - {platform}", 'description': prop['hikaye']})

# MLS (formerly mls.py)
@integrations_bp.route('/mls/sync', methods=['POST'])
@require_inner_circle
def sync_mls():
    # External MLS synchronization logic
    return jsonify({'status': 'sync_started'})
