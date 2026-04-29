from backend.app.extensions import db
from datetime import datetime

class Announcement(db.Model):
    __tablename__ = 'announcements'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50)) # duyuru, etkinlik, uyari
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Facility(db.Model):
    __tablename__ = 'neighborhood_facilities'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(50)) # havuz, spor_salonu, park
    status = db.Column(db.String(50), default='open')

class Reservation(db.Model):
    __tablename__ = 'facility_reservations'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    facility_id = db.Column(db.Integer, db.ForeignKey('neighborhood_facilities.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), default='confirmed')
