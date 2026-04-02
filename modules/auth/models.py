from shared.extensions import db
import datetime as dt

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True)
    email_verified = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    merged_into = db.Column(db.Integer, nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    role = db.Column(db.String(50), nullable=False) # Roles: admin, super_admin, etc.
    social_provider = db.Column(db.String(20), nullable=True)
    social_id = db.Column(db.String(255), nullable=True)
    profile_pic = db.Column(db.Text, nullable=True)

    identities = db.relationship('UserIdentity', backref='user', lazy=True, cascade='all, delete-orphan')
    tokens = db.relationship('RefreshToken', backref='user', lazy=True, cascade='all, delete-orphan')

class RefreshToken(db.Model):
    __tablename__ = 'refresh_tokens'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    token = db.Column(db.String(255), unique=True, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    revoked = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=dt.datetime.utcnow)

class UserIdentity(db.Model):
    __tablename__ = 'user_identities'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    provider = db.Column(db.String(20), nullable=False) # local, google, facebook
    provider_id = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    is_primary = db.Column(db.Boolean, default=False)
    deleted_at = db.Column(db.DateTime, nullable=True)

class AuthAuditLog(db.Model):
    __tablename__ = 'auth_audit_log'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    action = db.Column(db.String(100), nullable=False)
    details = db.Column(db.Text, nullable=True) # JSON stored as text
    created_at = db.Column(db.DateTime, default=dt.datetime.utcnow)

class PasswordReset(db.Model):
    __tablename__ = 'password_resets'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    token = db.Column(db.String(255), nullable=False)
    expiry = db.Column(db.DateTime, nullable=False)
    used = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=dt.datetime.utcnow)
