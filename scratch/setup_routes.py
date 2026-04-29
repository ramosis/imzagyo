import os

routes_content = """from flask import Blueprint, send_from_directory, request

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
"""

os.makedirs('backend/app', exist_ok=True)
with open('backend/app/routes.py', 'w', encoding='utf-8') as f:
    f.write(routes_content)

factory_path = 'backend/app/factory.py'
with open(factory_path, 'r', encoding='utf-8') as f:
    content = f.read()

if 'from .routes import main_bp' not in content:
    content = content.replace('def register_core_modules(app):', 'def register_core_modules(app):\n    from .routes import main_bp\n    app.register_blueprint(main_bp)\n')

with open(factory_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Routes and factory updated")
