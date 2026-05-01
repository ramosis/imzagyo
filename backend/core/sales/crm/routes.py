from . import crm_bp
from flask import Blueprint, request, jsonify, g
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

# --- CUSTOMER PORTAL API ---

@crm_bp.route('/api/v1/customer/transactions', methods=['GET'])
def get_customer_transactions():
    """Müşterinin dahil olduğu tüm işlemleri listeler."""
    # current_user'dan contact_id'yi bulmamız lazım
    # Şimdilik g.user üzerinden user_id ile eşleşen contact'ı buluyoruz
    user = getattr(g, 'user', None)
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401
    
    from .models import Contact, Transaction
    from backend.shared.database import db_session
    
    contact = db_session.query(Contact).filter_by(user_id=user['id']).first()
    if not contact:
        return jsonify({'error': 'Customer record not found'}), 404
        
    transactions = db_session.query(Transaction).filter_by(client_id=contact.id).all()
    
    return jsonify([{
        'id': t.id,
        'type': t.type,
        'status': t.status,
        'price': t.price,
        'created_at': t.created_at.isoformat()
    } for t in transactions]), 200

@crm_bp.route('/api/v1/customer/transactions/<int:id>/timeline', methods=['GET'])
def get_transaction_timeline(id):
    """Belirli bir işlemin zaman çizelgesini getirir."""
    user = getattr(g, 'user', None)
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401
        
    from .models import Contact, Transaction, TransactionEvent
    from backend.shared.database import db_session
    
    # Güvenlik kontrolü: İşlem bu müşteriye mi ait?
    contact = db_session.query(Contact).filter_by(user_id=user['id']).first()
    transaction = db_session.query(Transaction).get(id)
    
    if not transaction or (transaction.client_id != contact.id and user['role'] != 'admin'):
        return jsonify({'error': 'Access denied'}), 403
        
    events = db_session.query(TransactionEvent).filter_by(transaction_id=id, is_public=True).order_by(TransactionEvent.event_date.asc()).all()
    
    return jsonify([{
        'id': e.id,
        'title': e.title_tr,
        'description': e.description_tr,
        'date': e.event_date.isoformat(),
        'type': e.type,
        'icon': e.icon
    } for e in events]), 200

@crm_bp.route('/api/v1/customer/transactions/<int:id>/documents', methods=['GET'])
def get_transaction_documents(id):
    """Müşterinin belirli bir işleme ait dökümanlarını getirir."""
    user = getattr(g, 'user', None)
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401
        
    from .models import Contact, Transaction, Document
    from backend.shared.database import db_session
    
    contact = db_session.query(Contact).filter_by(user_id=user['id']).first()
    transaction = db_session.query(Transaction).get(id)
    
    if not transaction or (transaction.client_id != contact.id and user['role'] != 'admin'):
        return jsonify({'error': 'Access denied'}), 403
        
    documents = db_session.query(Document).filter_by(transaction_id=id).all()
    
    return jsonify([{
        'id': d.id,
        'title': d.title,
        'url': d.file_url,
        'size': d.file_size,
        'type': d.file_type,
        'category': d.category,
        'created_at': d.created_at.isoformat()
    } for d in documents]), 200
