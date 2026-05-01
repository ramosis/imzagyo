from backend.app.extensions import db
from datetime import datetime

class MessageTemplate(db.Model):
    __tablename__ = 'marketing_templates'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(50), nullable=False) # email, sms, whatsapp
    subject = db.Column(db.String(255))
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class AutomationRule(db.Model):
    __tablename__ = 'marketing_rules'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    trigger = db.Column(db.String(100), nullable=False) # lead_created, appointment_created, property_added, status_changed
    action = db.Column(db.String(100), nullable=False) # send_email, send_sms, send_whatsapp
    template_id = db.Column(db.Integer, db.ForeignKey('marketing_templates.id'))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Campaign(db.Model):
    __tablename__ = 'marketing_campaigns'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(50), nullable=False) # manual, automated
    channel = db.Column(db.String(50), nullable=False) # email, sms, whatsapp
    target_group = db.Column(db.String(100)) # all, leads, owners, tenants
    sent_count = db.Column(db.Integer, default=0)
    status = db.Column(db.String(50), default='draft') # draft, sending, completed, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
