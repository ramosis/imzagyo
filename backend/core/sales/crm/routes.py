from . import crm_bp\nfrom flask import Blueprint, request, jsonify, g
from backend.shared.database import get_db_connection
from backend.core.identity.auth.decorators import require_permission
from .service import CRMService

crm_bp = Blueprint('crm', __name__)

@crm_bp.route('/api/v1/leads', methods=['GET'])
@require_permission('danisman')
def get_leads():
    leads = CRMService.get_all_leads()
    return jsonify(leads), 200

@crm_bp.route('/api/v1/leads', methods=['POST'])
def add_lead():
    data = request.json
    lead_id = CRMService.create_lead(data)
    return jsonify({'id': lead_id, 'status': 'created'}), 201

@crm_bp.route('/api/v1/pipeline', methods=['GET'])
@require_permission('danisman')
def get_pipeline():
    pipeline = CRMService.get_pipeline_data()
    return jsonify(pipeline), 200
