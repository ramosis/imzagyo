from flask import request, jsonify, g
from modules.auth.decorators import require_inner_circle, login_required
from . import crm_bp
from .repository import LeadRepository, PipelineRepository
from .service import PipelineService

@crm_bp.route('/pipeline/leads', methods=['GET'])
@require_inner_circle
def get_pipeline_leads():
    stages = PipelineRepository.get_stages()
    # Simplified lead fetching for pipeline
    from modules.auth.service import AuthService
    user = AuthService.get_current_user()
    leads = LeadRepository.get_leads_for_user(user['id'], user['role'], user.get('circle', 'inner'))
    
    processed_stages = PipelineService.get_processed_pipeline(stages, leads)
    return jsonify(processed_stages), 200

@crm_bp.route('/pipeline/stages', methods=['GET'])
@require_inner_circle
def get_stages():
    stages = PipelineRepository.get_stages()
    return jsonify(stages), 200

@crm_bp.route('/leads/<int:lead_id>/move', methods=['PUT'])
@login_required
def move_lead(lead_id):
    data = request.json
    new_stage_id = data.get('stage_id')
    reason = data.get('reason', 'Manuel geçiş')
    if not new_stage_id: return jsonify({'error': 'stage_id required'}), 400
    
    if PipelineRepository.update_lead_stage(lead_id, new_stage_id, g.user['id'], reason):
        return jsonify({'status': 'success'})
    return jsonify({'error': 'Lead not found'}), 404
