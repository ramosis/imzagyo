from flask import request, jsonify
from modules.auth.decorators import require_permission
from . import portfolio_bp
from .repository import ValuationRepository

@portfolio_bp.route('/valuations', methods=['GET'])
def get_valuations():
    rows = ValuationRepository.get_all()
    return jsonify([dict(r) for r in rows])

@portfolio_bp.route('/valuations', methods=['POST'])
@require_permission('admin')
def add_valuation():
    try:
        data = request.json
        ValuationRepository.create(data)
        return jsonify({"success": True}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
