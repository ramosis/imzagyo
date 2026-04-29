from backend.app.extensions import db
from datetime import datetime

class Property(db.Model):
    __tablename__ = 'properties'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title_tr = db.Column(db.String(255), nullable=False)
    title_en = db.Column(db.String(255))
    description_tr = db.Column(db.Text)
    description_en = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), default='TRY')
    location_tr = db.Column(db.String(255))
    location_en = db.Column(db.String(255))
    type = db.Column(db.String(50)) # satilik, kiralik
    category = db.Column(db.String(50)) # konut, ticari, arsa
    is_active = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    images = db.relationship('PropertyImage', backref='property', lazy=True, cascade='all, delete-orphan')

class PropertyImage(db.Model):
    __tablename__ = 'property_images'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id', ondelete='CASCADE'), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    is_main = db.Column(db.Boolean, default=False)
    order = db.Column(db.Integer, default=0)
