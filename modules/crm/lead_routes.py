import urllib.parse
from flask import request, jsonify
from shared.database import get_db
from shared.utils import api_error
from shared.schemas import lead_schema, ValidationError
from modules.auth.decorators import require_permission, login_required
from modules.auth.service import AuthService
from . import crm_bp
from .repository import LeadRepository
from .service import LeadService

@crm_bp.route('/leads', methods=['GET'])
@login_required
def get_leads():
    user = AuthService.get_current_user()
    
    # Extract filters from query params
    filters = {
        'source': request.args.get('source'),
        'status': request.args.get('status'),
        'min_score': request.args.get('min_score'),
        'pipeline': request.args.get('pipeline') # 'all', 'true', 'false'
    }
    # Remove None values
    filters = {k: v for k, v in filters.items() if v is not None}
    
    leads = LeadRepository.get_leads_for_user(user['id'], user['role'], user.get('circle', 'outer'), filters=filters)
    return jsonify(lead_schema.dump(leads, many=True)), 200

@crm_bp.route('/leads/<int:id>', methods=['GET'])
@login_required
def get_lead(id):
    lead = LeadRepository.get_by_id(id)
    if not lead: return api_error("NOT_FOUND", "Lead not found", 404)
    return jsonify(lead_schema.dump(lead)), 200

@crm_bp.route('/leads', methods=['POST'])
def add_lead():
    try:
        lead = LeadService.calculate_and_create(request.json)
        return jsonify(lead_schema.dump(lead)), 201
    except ValidationError as err:
        return api_error("VALIDATION_ERROR", "Invalid data", details=err.messages)
    except Exception as e:
        return api_error("SERVER_ERROR", str(e), 500)

@crm_bp.route('/leads/<int:id>', methods=['PUT'])
@require_permission('leads.edit')
def update_lead(id):
    if LeadRepository.update(id, request.json):
        return jsonify({'status': 'updated'}), 200
    return api_error("NOT_FOUND", "Lead not found", 404)

@crm_bp.route('/leads/<int:id>/whatsapp-template', methods=['GET'])
@login_required
def get_whatsapp_template(id):
    property_id = request.args.get('property_id')
    with get_db() as conn:
        lead = conn.execute('SELECT * FROM leads WHERE id = ?', (id,)).fetchone()
        if not lead: return jsonify({"error": "Lead not found"}), 404
        prop = conn.execute('SELECT baslik1 as title, fiyat as price FROM portfoyler WHERE id = ?', (property_id,)).fetchone() if property_id else None
        
        name = lead['name'].split(' ')[0]
        msg = f"Merhaba {name}, ilgilendiğiniz portföy hakkında bilgi vermek isterim."
        if prop: msg += f" ({prop['title']})"
        
        phone = lead['phone'].replace(' ', '').replace('-', '')
        if phone.startswith('0'): phone = '9' + phone
        elif not phone.startswith('9'): phone = '90' + phone
        
        whatsapp_url = f"https://wa.me/{phone}?text={urllib.parse.quote(msg)}"
        return jsonify({"whatsapp_link": whatsapp_url, "message_text": msg})
