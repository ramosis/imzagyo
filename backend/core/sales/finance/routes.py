from . import finance_bp\nfrom flask import Blueprint, request, jsonify
from backend.shared.database import get_db_connection
from backend.core.identity.auth.decorators import require_permission

finance_bp = Blueprint('finance', __name__)

@finance_bp.route('/api/v1/expenses', methods=['GET'])
@require_permission('admin')
def get_expenses():
    with get_db_connection() as conn:
        rows = conn.execute("SELECT * FROM expenses ORDER BY date DESC").fetchall()
        return jsonify([dict(r) for r in rows]), 200

@finance_bp.route('/api/v1/revenue', methods=['GET'])
@require_permission('admin')
def get_revenue():
    # Revenue logic would go here
    return jsonify({'total_revenue': 0, 'currency': 'TRY'}), 200
