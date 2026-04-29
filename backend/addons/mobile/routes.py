from flask import Blueprint, request, jsonify
from backend.core.identity.auth.service import AuthService

mobile_bp = Blueprint('mobile_api', __name__)

@mobile_bp.route('/api/v1/mobile/status', methods=['GET'])
def get_status():
    return jsonify({'status': 'active', 'version': '1.0.0'}), 200

@mobile_bp.route('/api/v1/mobile/config', methods=['GET'])
def get_config():
    return jsonify({
        'api_url': 'https://api.imzaemlak.com/api/v1',
        'socket_url': 'https://api.imzaemlak.com'
    }), 200
