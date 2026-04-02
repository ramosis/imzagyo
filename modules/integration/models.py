from shared.extensions import db
import datetime as dt

class PlatformConnection(db.Model):
    __tablename__ = 'platform_connections'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    platform = db.Column(db.String(50), nullable=False) # sahibinden, instagram, etc.
    platform_type = db.Column(db.String(50), nullable=False) # listing, social
    display_name = db.Column(db.String(100), nullable=True)
    api_key = db.Column(db.String(255), nullable=True)
    api_secret = db.Column(db.String(255), nullable=True)
    access_token = db.Column(db.Text, nullable=True)
    account_url = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='manual') # active, manual, disconnected
    created_at = db.Column(db.DateTime, default=dt.datetime.utcnow)

class Publication(db.Model):
    __tablename__ = 'publications'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    property_id = db.Column(db.String(50), db.ForeignKey('portfoyler.id'), nullable=False)
    platform_id = db.Column(db.Integer, db.ForeignKey('platform_connections.id'), nullable=True)
    platform_name = db.Column(db.String(50), nullable=False)
    content_type = db.Column(db.String(50), nullable=True) # listing, story, post
    generated_text = db.Column(db.Text, nullable=True)
    listing_url = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='draft') # draft, published, failed
    published_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=dt.datetime.utcnow)
