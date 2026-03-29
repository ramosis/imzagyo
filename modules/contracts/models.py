from datetime import datetime
from shared.extensions import db

class Contract(db.Model):
    __tablename__ = 'contracts'
    
    id = db.Column(db.Integer, primary_key=True)
    contract_number = db.Column(db.String(50), unique=True, nullable=False)
    contract_type = db.Column(db.String(50), nullable=False)  # kiralama, satis, komisyon
    status = db.Column(db.String(20), default='draft')  # draft, sent, signed, cancelled
    
    # İlişkili kayıtlar
    property_id = db.Column(db.Integer, db.ForeignKey('portfoyler.id'), nullable=True)
    lead_id = db.Column(db.Integer, db.ForeignKey('leads.id'), nullable=True)
    
    # Taraflar (Contacts modülünden)
    landlord_id = db.Column(db.Integer, db.ForeignKey('contacts.id'), nullable=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('contacts.id'), nullable=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('contacts.id'), nullable=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('contacts.id'), nullable=True)
    
    # Finansal detaylar
    price = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='TRY')
    commission_rate = db.Column(db.Float, default=0.0)  # % olarak
    commission_amount = db.Column(db.Float, default=0.0)
    
    # Tarihler
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    signing_date = db.Column(db.DateTime, nullable=True)
    
    # Sözleşme içeriği
    template_id = db.Column(db.Integer, db.ForeignKey('contract_templates.id'))
    content = db.Column(db.Text)  # HTML içerik
    content_json = db.Column(db.JSON)  # Değişkenler
    
    # E-imza
    is_signed = db.Column(db.Boolean, default=False)
    signature_data = db.Column(db.JSON)  # E-imza verileri
    
    # Meta
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Contract {self.contract_number}>'

class ContractTemplate(db.Model):
    __tablename__ = 'contract_templates'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contract_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    
    # Şablon içeriği
    html_template = db.Column(db.Text, nullable=False)  # Jinja2 template
    default_variables = db.Column(db.JSON)  # Varsayılan değişkenler
    
    # Durum
    is_active = db.Column(db.Boolean, default=True)
    is_default = db.Column(db.Boolean, default=False)
    
    # Meta
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Party(db.Model):
    __tablename__ = 'parties'
    
    id = db.Column(db.Integer, primary_key=True)
    contract_id = db.Column(db.Integer, db.ForeignKey('contracts.id'), nullable=False)
    
    # Taraf bilgileri
    party_type = db.Column(db.String(50), nullable=False)  # landlord, tenant, buyer, seller, agent
    full_name = db.Column(db.String(200), nullable=False)
    tc_no = db.Column(db.String(11))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    address = db.Column(db.Text)
    
    # İmza
    is_signed = db.Column(db.Boolean, default=False)
    signed_at = db.Column(db.DateTime)
    signature_ip = db.Column(db.String(45))
    
    contract = db.relationship('Contract', backref='parties')
