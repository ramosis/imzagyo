from flask import Blueprint, request, jsonify, g
from modules.contracts.service import ContractService
from modules.contracts.repository import ContractRepository, PartyRepository
from modules.auth.decorators import login_required, require_permission

contracts_bp = Blueprint('contracts', __name__)

@contracts_bp.route('/', methods=['GET'])
@login_required
@require_permission('contracts.view')
def get_contracts():
    filters = {
        'status': request.args.get('status'),
        'contract_type': request.args.get('type')
    }
    filters = {k: v for k, v in filters.items() if v}
    
    contracts = ContractRepository.get_all(
        filters=filters,
        limit=request.args.get('limit', 100, type=int),
        offset=request.args.get('offset', 0, type=int)
    )
    
    return jsonify({
        'data': contracts,
        'count': len(contracts)
    }), 200

@contracts_bp.route('/<int:contract_id>', methods=['GET'])
@login_required
@require_permission('contracts.view')
def get_contract(contract_id):
    contract = ContractRepository.get_by_id(contract_id)
    if not contract:
        return jsonify({'error': 'Contract not found'}), 404
    
    parties = PartyRepository.get_by_contract(contract_id)
    contract['parties'] = parties
    
    return jsonify(contract), 200

@contracts_bp.route('/', methods=['POST'])
@login_required
@require_permission('contracts.create')
def create_contract():
    try:
        data = request.json
        result = ContractService.create_contract(data, g.user['id'])
        return jsonify(result), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400
