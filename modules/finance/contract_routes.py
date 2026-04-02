from flask import Blueprint, request, jsonify, g
from datetime import datetime
from modules.finance.contract_service import ContractService
from modules.finance.contract_repository import ContractRepository, PartyRepository
from modules.auth.decorators import login_required, require_permission

# Using the existing finance_bp would be possible, but separate contract_bp is cleaner for modular routing
contract_bp = Blueprint('contracts_new', __name__)

@contract_bp.route('/', methods=['GET'])
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
    
    # Transform to dict for JSON serialization
    serialized = []
    for c in contracts:
        serialized.append({
            'id': c.id,
            'contract_number': c.contract_number,
            'contract_type': c.contract_type,
            'status': c.status,
            'price': c.price,
            'currency': c.currency,
            'start_date': c.start_date,
            'end_date': c.end_date,
            'created_at': c.created_at.isoformat() if c.created_at else None
        })
    
    return jsonify({
        'data': serialized,
        'count': len(serialized)
    }), 200

@contract_bp.route('/<int:contract_id>', methods=['GET'])
@login_required
@require_permission('contracts.view')
def get_contract(contract_id):
    """Tekil sözleşme detayı"""
    contract = ContractRepository.get_by_id(contract_id)
    if not contract:
        return jsonify({'error': 'Contract not found'}), 404
    
    # Yetki kontrolü
    if not g.user.get('role') == 'admin' and contract.created_by != g.user['id']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    parties = PartyRepository.get_by_contract(contract_id)
    
    # Serialize
    data = {
        'id': contract.id,
        'contract_number': contract.contract_number,
        'contract_type': contract.contract_type,
        'status': contract.status,
        'content': contract.content,
        'price': contract.price,
        'currency': contract.currency,
        'parties': [{'id': p.id, 'full_name': p.full_name, 'party_type': p.party_type, 'is_signed': p.is_signed} for p in parties]
    }
    
    return jsonify(data), 200

@contract_bp.route('/', methods=['POST'])
@login_required
@require_permission('contracts.create')
def create_contract():
    """Yeni sözleşme oluştur"""
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        result = ContractService.create_contract(data, g.user['id'])
        return jsonify(result), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

@contract_bp.route('/<int:contract_id>/pdf', methods=['GET'])
@login_required
@require_permission('contracts.view')
def generate_pdf(contract_id):
    """Sözleşme PDF'i oluştur"""
    try:
        pdf_path = ContractService.generate_pdf(contract_id)
        return jsonify({
            'pdf_url': f'/{pdf_path}',
            'download_url': f'/api/v1/finance/contracts/{contract_id}/download'
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@contract_bp.route('/<int:contract_id>/send', methods=['POST'])
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

@contract_bp.route('/<int:contract_id>/sign/party/<int:party_id>', methods=['POST'])
def sign_contract(contract_id, party_id):
    """Sözleşmeyi imzala (Public endpoint)"""
    try:
        signature_data = {
            'ip': request.remote_addr,
            'user_agent': request.user_agent.string,
            'signature_image': request.json.get('signature_image')
        }
        
        ContractService.sign_contract(contract_id, party_id, signature_data)
        return jsonify({'message': 'Contract signed successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@contract_bp.route('/<int:contract_id>', methods=['DELETE'])
@login_required
@require_permission('contracts.delete')
def delete_contract(contract_id):
    """Sözleşme sil"""
    contract = ContractRepository.get_by_id(contract_id)
    if not contract:
        return jsonify({'error': 'Contract not found'}), 404
        
    if contract.status in ['signed', 'active']:
        return jsonify({'error': 'Cannot delete signed/active contracts'}), 400
    
    ContractRepository.delete(contract_id)
    return jsonify({'message': 'Deleted'}), 200

@contract_bp.route('/calculate-commission', methods=['POST'])
@login_required
def calculate_commission():
    """Komisyon hesapla"""
    data = request.json
    result = ContractService.calculate_commission(
        price=data.get('price', 0),
        commission_type=data.get('type', 'standard')
    )
    return jsonify(result), 200
