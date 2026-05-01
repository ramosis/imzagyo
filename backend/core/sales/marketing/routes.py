from flask import Blueprint, request, jsonify
from .models import MessageTemplate, AutomationRule, Campaign
from backend.app.extensions import db

marketing_bp = Blueprint('marketing', __name__)

# --- TEMPLATES ---
@marketing_bp.route('/templates', methods=['GET'])
def get_templates():
    templates = MessageTemplate.query.all()
    return jsonify([{
        'id': t.id,
        'name': t.name,
        'type': t.type,
        'subject': t.subject,
        'content': t.content,
        'created_at': t.created_at.isoformat()
    } for t in templates])

@marketing_bp.route('/templates', methods=['POST'])
def create_template():
    data = request.get_json()
    new_template = MessageTemplate(
        name=data.get('name'),
        type=data.get('type'),
        subject=data.get('subject', ''),
        content=data.get('content')
    )
    db.session.add(new_template)
    db.session.commit()
    return jsonify({'message': 'Şablon başarıyla oluşturuldu', 'id': new_template.id}), 201

# --- RULES ---
@marketing_bp.route('/rules', methods=['GET'])
def get_rules():
    rules = AutomationRule.query.all()
    return jsonify([{
        'id': r.id,
        'name': r.name,
        'trigger': r.trigger,
        'action': r.action,
        'template_id': r.template_id,
        'is_active': r.is_active
    } for r in rules])

@marketing_bp.route('/rules', methods=['POST'])
def create_rule():
    data = request.get_json()
    new_rule = AutomationRule(
        name=data.get('name'),
        trigger=data.get('trigger'),
        action=data.get('action'),
        template_id=data.get('template_id'),
        is_active=data.get('is_active', True)
    )
    db.session.add(new_rule)
    db.session.commit()
    return jsonify({'message': 'Kural başarıyla oluşturuldu', 'id': new_rule.id}), 201

# --- CAMPAIGNS ---
@marketing_bp.route('/campaigns', methods=['GET'])
def get_campaigns():
    campaigns = Campaign.query.order_by(Campaign.created_at.desc()).all()
    return jsonify([{
        'id': c.id,
        'title': c.title,
        'type': c.type,
        'channel': c.channel,
        'target_group': c.target_group,
        'sent_count': c.sent_count,
        'status': c.status,
        'created_at': c.created_at.isoformat()
    } for c in campaigns])
