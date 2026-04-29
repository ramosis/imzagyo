from backend.app.extensions import db
from datetime import datetime

class AuditLog(db.Model):
    """Tracking all sensitive data changes and admin actions."""
    __tablename__ = 'audit_logs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    action = db.Column(db.String(100), nullable=False)
    entity_type = db.Column(db.String(50), nullable=False)
    entity_id = db.Column(db.String(50), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    old_data = db.Column(db.Text, nullable=True) # JSON stored as text
    new_data = db.Column(db.Text, nullable=True) # JSON stored as text
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
