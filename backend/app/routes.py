from flask import Blueprint, send_from_directory, request, make_response, jsonify
import os
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    host = request.headers.get('Host', '')
    if 'mahalle' in host:
        return send_from_directory('frontend/neighborhood/pages', 'index.html')
    return send_from_directory('frontend/investment/pages', 'index.html')

@main_bp.route('/portal')
def portal():
    return send_from_directory('frontend/portal/pages', 'portal-modular.html')

@main_bp.route('/portal/sections/<section_name>')
def portal_section(section_name):
    # Bu route, portal-modular.html tarafından fetch() ile çağrılacak HTML parçalarını sunar
    return send_from_directory('frontend/portal/pages/sections', f'{section_name}.html')

@main_bp.route('/portal/sections/modals/<modal_name>')
def portal_modal(modal_name):
    return send_from_directory('frontend/portal/pages/sections/modals', f'{modal_name}.html')

@main_bp.route('/pipeline')
def pipeline_page():
    return send_from_directory('frontend/portal/pages', 'pipeline.html')

@main_bp.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'version': '1.0.0',
        'timestamp': datetime.utcnow().isoformat()
    }), 200
