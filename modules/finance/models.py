from shared.extensions import db
import datetime as dt

class Contract(db.Model):
    __tablename__ = 'contracts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    contract_number = db.Column(db.String(100), unique=True, nullable=False)
    contract_type = db.Column(db.String(50), nullable=False) # Kira, Satış, vb.
    status = db.Column(db.String(20), default='draft') # draft, prepared, sent, viewed, signed, cancelled, finalized
    property_id = db.Column(db.String(50), db.ForeignKey('portfoyler.id', ondelete='SET NULL'), nullable=True)
    lead_id = db.Column(db.Integer, db.ForeignKey('leads.id', ondelete='SET NULL'), nullable=True)
    landlord_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    price = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), default='TRY')
    commission_rate = db.Column(db.Float, default=0.0)
    commission_amount = db.Column(db.Float, default=0.0)
    start_date = db.Column(db.String(20), nullable=True) # YYYY-MM-DD
    end_date = db.Column(db.String(20), nullable=True)
    signing_date = db.Column(db.String(20), nullable=True)
    template_id = db.Column(db.Integer, db.ForeignKey('contract_templates.id', ondelete='SET NULL'), nullable=True)
    content = db.Column(db.Text, nullable=True)
    content_json = db.Column(db.Text, nullable=True) # JSON stored as text
    pdf_path = db.Column(db.Text, nullable=True)
    pdf_url = db.Column(db.Text, nullable=True)
    sent_at = db.Column(db.DateTime, nullable=True)
    viewed_at = db.Column(db.DateTime, nullable=True)
    signed_at = db.Column(db.DateTime, nullable=True)
    is_signed = db.Column(db.Boolean, default=False)
    signed_by_landlord = db.Column(db.Boolean, default=False)
    signed_by_tenant = db.Column(db.Boolean, default=False)
    signed_by_buyer = db.Column(db.Boolean, default=False)
    signed_by_seller = db.Column(db.Boolean, default=False)
    signature_data = db.Column(db.Text, nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    created_at = db.Column(db.DateTime, default=dt.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=dt.datetime.utcnow, onupdate=dt.datetime.utcnow)

    # Relationships
    template = db.relationship('ContractTemplate', backref='contracts_finance')
    clauses = db.relationship('ContractClause', secondary='contract_clause_links', backref='contracts_finance')
    parties = db.relationship('ContractParty', backref='contract', cascade='all, delete-orphan')

class ContractTemplate(db.Model):
    __tablename__ = 'contract_templates'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    contract_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    html_template = db.Column(db.Text, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_default = db.Column(db.Boolean, default=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    created_at = db.Column(db.DateTime, default=dt.datetime.utcnow)

class ContractClause(db.Model):
    __tablename__ = 'contract_clauses'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    clause_type = db.Column(db.String(50), nullable=True)
    usage_count = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    created_at = db.Column(db.DateTime, default=dt.datetime.utcnow)

class ContractClauseLink(db.Model):
    __tablename__ = 'contract_clause_links'
    contract_id = db.Column(db.Integer, db.ForeignKey('contracts.id', ondelete='CASCADE'), primary_key=True)
    clause_id = db.Column(db.Integer, db.ForeignKey('contract_clauses.id', ondelete='CASCADE'), primary_key=True)

class ContractParty(db.Model):
    __tablename__ = 'parties'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    contract_id = db.Column(db.Integer, db.ForeignKey('contracts.id', ondelete='CASCADE'), nullable=False)
    party_type = db.Column(db.String(20), nullable=False) # Seller, Buyer, Landlord, Tenant
    full_name = db.Column(db.String(100), nullable=False)
    tc_no = db.Column(db.String(20), nullable=True)
    phone = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    address = db.Column(db.Text, nullable=True)
    is_signed = db.Column(db.Boolean, default=False)
    signed_at = db.Column(db.DateTime, nullable=True)
    signature_ip = db.Column(db.String(50), nullable=True)

class Tax(db.Model):
    __tablename__ = 'taxes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    property_id = db.Column(db.String(50), db.ForeignKey('portfoyler.id', ondelete='CASCADE'), nullable=False)
    tax_type = db.Column(db.String(50), nullable=True) # Emlak Vergisi, Aidat, etc.
    amount = db.Column(db.Float, nullable=True)
    due_date = db.Column(db.String(20), nullable=True) # YYYY-MM-DD
    status = db.Column(db.String(20), default='Ödenmedi') # Ödendi, Ödenmedi, Gecikmiş
    created_at = db.Column(db.DateTime, default=dt.datetime.utcnow)

class DuesPayment(db.Model):
    __tablename__ = 'dues_payments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lease_id = db.Column(db.Integer, db.ForeignKey('leases.id', ondelete='CASCADE'), nullable=True)
    property_unit_id = db.Column(db.Integer, db.ForeignKey('property_units.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    payment_type = db.Column(db.String(20), default='AIDAT') # AIDAT, DEMIRBAS, etc.
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='Ödenmedi')
    due_date = db.Column(db.String(20), nullable=False)
    paid_date = db.Column(db.String(20), nullable=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=dt.datetime.utcnow)

class ApartmentExpense(db.Model):
    __tablename__ = 'apartment_expenses'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    property_id = db.Column(db.String(50), db.ForeignKey('portfoyler.id', ondelete='CASCADE'), nullable=False)
    expense_type = db.Column(db.String(50), nullable=True) # Temizlik, Bakım, etc.
    amount = db.Column(db.Float, nullable=False)
    expense_date = db.Column(db.String(20), nullable=False)
    invoice_file = db.Column(db.Text, nullable=True) # URL
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=dt.datetime.utcnow)

class StaffExpense(db.Model):
    __tablename__ = 'expenses'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    category = db.Column(db.String(50), nullable=True) # yemek, yakıt, temsil...
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    receipt_image = db.Column(db.Text, nullable=True)
    date = db.Column(db.String(20), nullable=True)
    status = db.Column(db.String(20), default='pending') # pending, approved, rejected
    created_at = db.Column(db.DateTime, default=dt.datetime.utcnow)

class UserShift(db.Model):
    __tablename__ = 'user_shifts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    day_of_week = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.String(10), nullable=False)
    end_time = db.Column(db.String(10), nullable=False)
    is_off = db.Column(db.Boolean, default=False)

class Commission(db.Model):
    __tablename__ = 'commissions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    contract_id = db.Column(db.Integer, db.ForeignKey('contracts.id', ondelete='CASCADE'), nullable=True)
    amount = db.Column(db.Float, nullable=False)
    rate = db.Column(db.Float, nullable=True)
    description = db.Column(db.Text, nullable=True)
    month = db.Column(db.String(20), nullable=True)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=dt.datetime.utcnow)

class Campaign(db.Model):
    __tablename__ = 'campaigns'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    content_html = db.Column(db.Text, nullable=False)
    target_audience = db.Column(db.String(50), nullable=False) # all, vip, leads
    campaign_type = db.Column(db.String(50), default='newsletter')
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    status = db.Column(db.String(20), default='draft') # draft, sent, archived
    created_at = db.Column(db.DateTime, default=dt.datetime.utcnow)

class CampaignLog(db.Model):
    __tablename__ = 'campaign_logs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.id', ondelete='CASCADE'), nullable=False)
    recipient_email = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20), default='sent') # sent, failed, opened
    sent_at = db.Column(db.DateTime, default=dt.datetime.utcnow)
