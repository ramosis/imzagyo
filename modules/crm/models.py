from shared.extensions import db
import datetime as dt

class Lead(db.Model):
    __tablename__ = 'leads'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    source = db.Column(db.String(50), nullable=True) # website, sahibinden, etc.
    interest_property_id = db.Column(db.String(50), db.ForeignKey('portfoyler.id', ondelete='SET NULL'), nullable=True)
    campaign_id = db.Column(db.String(50), nullable=True)
    assigned_user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    status = db.Column(db.String(20), default='new')
    segment = db.Column(db.String(50), nullable=True) # yatirimci, owner, buyer, etc.
    action_type = db.Column(db.String(20), nullable=True) # buy, rent, sell, lease
    ai_score = db.Column(db.Integer, default=0)
    score_x = db.Column(db.Integer, default=50) # Alım Gücü (0-100)
    score_y = db.Column(db.Integer, default=50) # Aciliyet/Sıcaklık (0-100)
    score_z = db.Column(db.Integer, default=50) # Portföy Uyumu (0-100)
    last_contacted_at = db.Column(db.DateTime, nullable=True)
    tags = db.Column(db.Text, nullable=True) # JSON list
    notes = db.Column(db.Text, nullable=True)
    pipeline_stage_id = db.Column(db.Integer, db.ForeignKey('pipeline_stages.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=dt.datetime.utcnow)

class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    property_id = db.Column(db.String(50), db.ForeignKey('portfoyler.id', ondelete='SET NULL'), nullable=True)
    client_name = db.Column(db.String(100), nullable=True)
    client_phone = db.Column(db.String(50), nullable=True)
    datetime = db.Column(db.String(50), nullable=True) # YYYY-MM-DD HH:MM
    purpose = db.Column(db.String(100), default='gosterim')
    notes = db.Column(db.Text, nullable=True)
    assigned_user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    pipeline_stage_id = db.Column(db.Integer, db.ForeignKey('pipeline_stages.id', ondelete='SET NULL'), nullable=True)
    original_datetime = db.Column(db.String(50), nullable=True)
    reschedule_count = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='pending') # pending, confirmed, completed, cancelled
    created_at = db.Column(db.DateTime, default=dt.datetime.utcnow)

class PipelineStage(db.Model):
    __tablename__ = 'pipeline_stages'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    order_index = db.Column(db.Integer, default=0)
    color = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=dt.datetime.utcnow)

class PipelineHistory(db.Model):
    __tablename__ = 'pipeline_history'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lead_id = db.Column(db.Integer, db.ForeignKey('leads.id', ondelete='CASCADE'), nullable=False)
    old_stage_id = db.Column(db.Integer, db.ForeignKey('pipeline_stages.id', ondelete='SET NULL'), nullable=True)
    new_stage_id = db.Column(db.Integer, db.ForeignKey('pipeline_stages.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    reason = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=dt.datetime.utcnow)

class LeadInteraction(db.Model):
    __tablename__ = 'lead_interactions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lead_id = db.Column(db.Integer, db.ForeignKey('leads.id', ondelete='CASCADE'), nullable=True)
    session_id = db.Column(db.String(100), nullable=True)
    tool_name = db.Column(db.String(50), nullable=True) # roi_calculator, etc.
    data_json = db.Column(db.Text, nullable=True) # JSON stored as text
    created_at = db.Column(db.DateTime, default=dt.datetime.utcnow)

class MessageTemplate(db.Model):
    __tablename__ = 'message_templates'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    segment = db.Column(db.String(50), nullable=False) # yatirimci, acil, etc.
    context_type = db.Column(db.String(50), nullable=False) # property, general
    template_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=dt.datetime.utcnow)

class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    address = db.Column(db.Text, nullable=True)
    occupation = db.Column(db.String(100), nullable=True)
    availability_time = db.Column(db.String(100), nullable=True)
    family_size = db.Column(db.Integer, nullable=True)
    age = db.Column(db.Integer, nullable=True)
    political_view = db.Column(db.String(100), nullable=True)
    religious_view = db.Column(db.String(100), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    birthdate = db.Column(db.String(20), nullable=True) # YYYY-MM-DD
    category = db.Column(db.String(50), default='general', nullable=False)
    source_table = db.Column(db.String(50), nullable=True) # 'leads', 'users' etc
    source_id = db.Column(db.Integer, nullable=True)
    tags = db.Column(db.Text, nullable=True) # JSON list
    created_at = db.Column(db.DateTime, default=dt.datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('source_table', 'source_id', name='uix_contact_source'),)

class PurchasingPower(db.Model):
    __tablename__ = 'purchasing_power'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    cash_amount = db.Column(db.Float, default=0.0)
    credit_amount = db.Column(db.Float, default=0.0)
    barter_total = db.Column(db.Float, default=0.0)
    total_power = db.Column(db.Float, default=0.0)
    details_json = db.Column(db.Text, nullable=True) # JSON stored as text
    created_at = db.Column(db.DateTime, default=dt.datetime.utcnow)
