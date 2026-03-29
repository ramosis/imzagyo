from datetime import datetime
from shared.extensions import db

class Portfolio(db.Model):
    __tablename__ = 'portfoyler'
    id = db.Column(db.String(50), primary_key=True)
    koleksiyon = db.Column(db.String(100))
    baslik1 = db.Column(db.String(200))
    baslik2 = db.Column(db.String(200))
    lokasyon = db.Column(db.String(255))
    fiyat = db.Column(db.String(50))
    hikaye = db.Column(db.Text)
    ozellikler = db.Column(db.JSON)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
