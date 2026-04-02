from shared.extensions import db
import datetime as dt

class MaintenanceRequest(db.Model):
    __tablename__ = 'maintenance_requests'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    property_id = db.Column(db.String(50), db.ForeignKey('portfoyler.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    title = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)
    priority = db.Column(db.String(20), default='Normal') # Düşük, Normal, Yüksek, Acil
    request_date = db.Column(db.DateTime, default=dt.datetime.utcnow)
    scheduled_date = db.Column(db.String(20), nullable=True) # YYYY-MM-DD
    status = db.Column(db.String(20), default='Açık') # Açık, İşlemde, Çözüldü, İptal

class PropertyUnit(db.Model):
    __tablename__ = 'property_units'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    property_id = db.Column(db.String(50), db.ForeignKey('portfoyler.id', ondelete='CASCADE'), nullable=False)
    unit_number = db.Column(db.String(50), nullable=False)
    floor = db.Column(db.String(20), nullable=True)
    unit_type = db.Column(db.String(50), default='Konut')
    area_sqm = db.Column(db.Float, nullable=True)
    status = db.Column(db.String(20), default='Boş') # Boş, Dolu, Tadilatta
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=dt.datetime.utcnow)

    leases = db.relationship('Lease', backref='unit', lazy=True, cascade='all, delete-orphan')

class Lease(db.Model):
    __tablename__ = 'leases'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    property_unit_id = db.Column(db.Integer, db.ForeignKey('property_units.id', ondelete='CASCADE'), nullable=False)
    tenant_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    start_date = db.Column(db.String(20), nullable=True) # YYYY-MM-DD
    end_date = db.Column(db.String(20), nullable=True)
    rent_amount = db.Column(db.Float, nullable=True)
    currency = db.Column(db.String(10), default='TRY')
    payment_day = db.Column(db.Integer, nullable=True)
    deposit_amount = db.Column(db.Float, nullable=True)
    status = db.Column(db.String(20), default='Aktif') # Aktif, Sonlandı
    contract_file = db.Column(db.Text, nullable=True) # URL
    created_at = db.Column(db.DateTime, default=dt.datetime.utcnow)
