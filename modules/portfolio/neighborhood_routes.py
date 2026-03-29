from flask import request, jsonify
from modules.auth.decorators import require_permission
from . import portfolio_bp
from .repository import NeighborhoodRepository

@portfolio_bp.route('/neighborhoods', methods=['GET'])
def get_neighborhoods():
    rows = NeighborhoodRepository.get_all()
    return jsonify([dict(r) for r in rows])

@portfolio_bp.route('/neighborhoods', methods=['POST'])
@require_permission('admin')
def add_neighborhood():
    try:
        data = request.json
        NeighborhoodRepository.create(data)
        return jsonify({"success": True}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
