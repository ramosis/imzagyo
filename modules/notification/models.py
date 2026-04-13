from shared.extensions import db
from datetime import datetime

class Notification(db.Model):
    """Notification system for users and admins."""
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False) # pipeline, ai_alert, etc.
    title = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    target_role = db.Column(db.String(50), nullable=True) # tenant, owner, agent, all
    status = db.Column(db.String(20), default='unread') # unread, read
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
