from flask import Blueprint, request, jsonify, g
from marshmallow import ValidationError
from datetime import datetime

from modules.contracts.service import ContractService
from modules.contracts.repository import ContractRepository, PartyRepository
from modules.auth.decorators import login_required, require_permission
from shared.schemas import contract_schema, ContractCreateSchema

from . import contracts_bp

@contracts_bp.route('/', methods=['GET'])
@login_required
@require_permission('contracts.view')
def get_contracts():
    """Sözleşme listesi"""
    filters = {
        'status': request.args.get('status'),
        'contract_type': request.args.get('type'),
        'created_by': g.user['id'] if not g.user.get('role') == 'admin' else None
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
    """Tekil sözleşme detayı"""
    contract = ContractRepository.get_by_id(contract_id)
    if not contract:
        return jsonify({'error': 'Contract not found'}), 404
    
    # Yetki kontrolü
    if not g.user.get('role') == 'admin' and contract['created_by'] != g.user['id']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    parties = PartyRepository.get_by_contract(contract_id)
    contract['parties'] = parties
    
    return jsonify(contract), 200

@contracts_bp.route('/', methods=['POST'])
@login_required
@require_permission('contracts.create')
def create_contract():
    """Yeni sözleşme oluştur"""
    try:
        schema = ContractCreateSchema()
        data = schema.load(request.json)
        
        result = ContractService.create_contract(data, g.user['id'])
        
        return jsonify(result), 201
        
    except ValidationError as err:
        return jsonify({'error': 'Validation failed', 'details': err.messages}), 400
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@contracts_bp.route('/<int:contract_id>/pdf', methods=['GET'])
@login_required
@require_permission('contracts.view')
def generate_pdf(contract_id):
    """Sözleşme PDF'i oluştur"""
    try:
        pdf_path = ContractService.generate_pdf(contract_id)
        return jsonify({
            'pdf_url': pdf_path,
            'download_url': f'/uploads/contracts/{pdf_path.split("/")[-1]}'
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@contracts_bp.route('/<int:contract_id>/send', methods=['POST'])
@login_required
@require_permission('contracts.send')
def send_for_signature(contract_id):
    """İmza için gönder"""
    try:
        data = request.json or {}
        ContractService.send_for_signature(
            contract_id, 
            send_method=data.get('method', 'email')
        )
        return jsonify({'message': 'Contract sent for signature'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@contracts_bp.route('/<int:contract_id>/sign/party/<int:party_id>', methods=['POST'])
def sign_contract(contract_id, party_id):
    """Sözleşmeyi imzala (Public endpoint - auth gerekmez, token ile)"""
    try:
        signature_data = {
            'ip': request.remote_addr,
            'user_agent': request.user_agent.string,
            'timestamp': datetime.utcnow().isoformat(),
            'signature_image': request.json.get('signature_image')
        }
        
        ContractService.sign_contract(contract_id, party_id, signature_data)
        return jsonify({'message': 'Contract signed successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@contracts_bp.route('/<int:contract_id>', methods=['PUT'])
@login_required
@require_permission('contracts.edit')
def update_contract(contract_id):
    """Sözleşme güncelle"""
    contract = ContractRepository.get_by_id(contract_id)
    if not contract:
        return jsonify({'error': 'Contract not found'}), 404
        
    if contract['status'] != 'draft':
        return jsonify({'error': 'Only draft contracts can be updated'}), 400
    
    data = request.json
    if ContractRepository.update(contract_id, data):
        return jsonify({'message': 'Updated'}), 200
    return jsonify({'error': 'Update failed'}), 500

@contracts_bp.route('/<int:contract_id>', methods=['DELETE'])
@login_required
@require_permission('contracts.delete')
def delete_contract(contract_id):
    """Sözleşme sil"""
    contract = ContractRepository.get_by_id(contract_id)
    if not contract:
        return jsonify({'error': 'Contract not found'}), 404
        
    if contract['status'] in ['signed', 'active']:
        return jsonify({'error': 'Cannot delete signed/active contracts'}), 400
    
    ContractRepository.delete(contract_id)
    return jsonify({'message': 'Deleted'}), 200

@contracts_bp.route('/templates', methods=['GET'])
@login_required
def get_templates():
    """Şablon listesi"""
    from modules.contracts.repository import ContractTemplateRepository
    
    contract_type = request.args.get('type')
    templates = ContractTemplateRepository.get_by_type(contract_type or 'kiralama')
    
    return jsonify(templates), 200

@contracts_bp.route('/calculate-commission', methods=['POST'])
@login_required
def calculate_commission():
    """Komisyon hesapla"""
    data = request.json
    result = ContractService.calculate_commission(
        price=data.get('price', 0),
        commission_type=data.get('type', 'standard')
    )
    return jsonify(result), 200
