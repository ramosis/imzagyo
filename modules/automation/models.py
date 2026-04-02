from shared.extensions import db
import datetime as dt

class AutomationRule(db.Model):
    __tablename__ = 'automations'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    trigger_event = db.Column(db.String(50), nullable=False) # new_lead, property_sold, etc.
    is_active = db.Column(db.Boolean, default=True)
    last_run = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=dt.datetime.utcnow)

class AutomationLog(db.Model):
    __tablename__ = 'automation_logs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rule_id = db.Column(db.Integer, db.ForeignKey('automations.id'), nullable=True)
    lead_id = db.Column(db.Integer, db.ForeignKey('leads.id'), nullable=True)
    action_taken = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='success')
    created_at = db.Column(db.DateTime, default=dt.datetime.utcnow)
