from flask import Blueprint, request, jsonify
from modules.auth.decorators import require_permission
from .service import FinanceService

finance_tax_bp = Blueprint('finance_tax', __name__)

@finance_tax_bp.route('/calculate', methods=['POST'])
@require_permission('finance.view')
def calculate_tax():
    data = request.json
    if not data or 'price' not in data:
        return jsonify({'error': 'Price and type are required'}), 400
        
    try:
        result = FinanceService.calculate_tax(
            price=data.get('price', 0),
            tax_type=data.get('type', 'kdv')
        )
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
