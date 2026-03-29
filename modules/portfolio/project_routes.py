from flask import request, jsonify
from modules.auth.decorators import require_permission
from . import portfolio_bp
from .repository import ProjectRepository

@portfolio_bp.route('/projects', methods=['GET'])
def get_projects():
    rows = ProjectRepository.get_all()
    return jsonify([dict(r) for r in rows])

@portfolio_bp.route('/projects', methods=['POST'])
@require_permission('admin')
def add_project():
    try:
        data = request.json
        ProjectRepository.create(data)
        return jsonify({"success": True}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
