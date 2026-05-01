from backend.app.extensions import db
from datetime import datetime

class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255))
    phone = db.Column(db.String(50))
    category = db.Column(db.String(50)) # lead, client, partner, tenant
    source = db.Column(db.String(100)) # web, social, referral
    status = db.Column(db.String(50), default='new')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Note(db.Model):
    __tablename__ = 'contact_notes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id', ondelete='CASCADE'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=True)
    client_id = db.Column(db.Integer, db.ForeignKey('contacts.id'), nullable=False)
    agent_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    type = db.Column(db.String(50)) # sale, lease
    status = db.Column(db.String(50), default='open') # open, closed, cancelled
    price = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    events = db.relationship('TransactionEvent', backref='transaction', lazy=True, cascade='all, delete-orphan')
    documents = db.relationship('Document', backref='transaction', lazy=True, cascade='all, delete-orphan')

class TransactionEvent(db.Model):
    __tablename__ = 'transaction_events'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.id', ondelete='CASCADE'), nullable=False)
    title_tr = db.Column(db.String(255), nullable=False)
    title_en = db.Column(db.String(255))
    description_tr = db.Column(db.Text)
    description_en = db.Column(db.Text)
    type = db.Column(db.String(50)) # milestone, update, document_added
    icon = db.Column(db.String(50), default='fa-circle') # fontawesome icon
    event_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_public = db.Column(db.Boolean, default=True) # Müşteri görebilir mi?

class Document(db.Model):
    __tablename__ = 'documents'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    file_url = db.Column(db.String(255), nullable=False)
    file_size = db.Column(db.String(50)) # e.g. "2.4 MB"
    file_type = db.Column(db.String(50)) # e.g. "pdf", "jpg"
    category = db.Column(db.String(50)) # contract, title_deed, id_card
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
