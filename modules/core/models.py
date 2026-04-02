from shared.extensions import db
from datetime import datetime

class HeroSlide(db.Model):
    """Hero section slider configuration."""
    __tablename__ = 'hero_slides'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    resim_url = db.Column(db.Text, nullable=False)
    alt_baslik = db.Column(db.String(255), nullable=True)
    baslik_satir1 = db.Column(db.String(255), nullable=True)
    baslik_satir2 = db.Column(db.String(255), nullable=True)
    buton1_metin = db.Column(db.String(100), nullable=True)
    buton2_metin = db.Column(db.String(100), nullable=True)
    buton2_link = db.Column(db.Text, nullable=True)
    sira = db.Column(db.Integer, default=0)

class SystemSetting(db.Model):
    """Dynamic site settings (Demo/Placeholder/Live modes etc)."""
    __tablename__ = 'system_settings'
    key = db.Column(db.String(100), primary_key=True)
    value = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text, nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class UserInteraction(db.Model):
    """Tracking user behavior for analytics."""
    __tablename__ = 'user_interactions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    session_id = db.Column(db.String(100), nullable=True)
    url = db.Column(db.Text, nullable=True)
    event_type = db.Column(db.String(50), nullable=True) 
    element_id = db.Column(db.String(100), nullable=True)
    value = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class IncomingDoc(db.Model):
    """Handling documents from external sources (WhatsApp/Email)."""
    __tablename__ = 'incoming_docs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    source = db.Column(db.String(50), nullable=True) 
    sender = db.Column(db.String(100), nullable=True)
    file_path = db.Column(db.Text, nullable=True)
    file_type = db.Column(db.String(20), nullable=True) 
    content = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='new')
    pipeline_stage_id = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
