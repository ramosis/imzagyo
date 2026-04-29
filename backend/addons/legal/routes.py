from . import legal_bp
from flask import Blueprint, request, jsonify
from backend.shared.database import get_db_connection

legal_bp = Blueprint('legal', __name__)

@legal_bp.route('/api/v1/legal/contracts', methods=['GET'])
def get_legal_contracts():
    with get_db_connection() as conn:
        rows = conn.execute("SELECT * FROM contracts").fetchall()
        return jsonify([dict(r) for r in rows]), 200

@legal_bp.route('/api/v1/legal/compliance', methods=['GET'])
def check_compliance():
    return jsonify({'status': 'compliant', 'last_check': '2024-01-01'}), 200
