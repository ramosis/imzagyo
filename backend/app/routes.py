from flask import Blueprint, send_from_directory, request

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    host = request.headers.get('Host', '')
    if 'mahalle' in host:
        return send_from_directory('../../frontend/neighborhood/pages', 'index.html')
    return send_from_directory('../../frontend/investment/pages', 'index.html')

@main_bp.route('/portal')
def portal():
    return send_from_directory('../../frontend/portal/pages', 'index.html')

@main_bp.route('/pipeline')
def pipeline_page():
    return send_from_directory('../../frontend/portal/pages', 'pipeline.html')
