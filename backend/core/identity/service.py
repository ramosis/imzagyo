import os
import datetime
import hashlib
import jwt
import bcrypt
from flask import request, jsonify, g
from backend.app.extensions import limiter
import json

def get_jwt_secret():
    return os.environ.get("JWT_SECRET", "dev-secret-key")

# Permission Map
PERMISSIONS = {
    'admin': ['*'],
    'super_admin': ['*'],
    'broker': ['*'],
    'danisman': ['portfolio.view', 'portfolio.create', 'leads.view', 'leads.edit'],
    'employee': ['portfolio.view', 'leads.view'],
    'contractor': ['portfolio.view', 'projects.view'],
    'owner': ['portfolio.view'],
    'tenant': ['portfolio.view'],
    'partner': ['portfolio.view', 'projects.view'],
    'vip': ['portfolio.view'],
    'm_sahibi': ['portfolio.view'],
    'kiraci': ['portfolio.view'],
    'standart': ['portfolio.view']
}

INNER_ROLES = ["admin", "super_admin", "broker", "danisman", "m_sahibi"]

class IdentityService:
    @staticmethod
    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    @staticmethod
    def verify_password(plain_password: str, stored_hash: str, user_id: int = None) -> bool:
        if not stored_hash or not plain_password:
            return False
            
        if stored_hash.startswith('$2b$') or stored_hash.startswith('$2a$') or stored_hash.startswith('$2y$'):
            try:
                return bcrypt.checkpw(plain_password.encode('utf-8'), stored_hash.encode('utf-8'))
            except ValueError:
                return False
        else:
            # Legacy SHA256 Fallback
            legacy_hash = hashlib.sha256(plain_password.encode('utf-8')).hexdigest()
            if legacy_hash == stored_hash:
                if user_id:
                    # Seamless Migration
                    new_hash = IdentityService.hash_password(plain_password)
                    from shared.database import get_db_connection
                    with get_db_connection() as conn:
                        conn.execute('UPDATE users SET password_hash = ? WHERE id = ?', (new_hash, user_id))
                return True
            return False

    @staticmethod
    def get_current_user():
        token = request.headers.get('Authorization')
        if not token:
            return None
            
        if token.startswith('Bearer ey'):
            jwt_token = token.split(' ')[1]
            try:
                payload = jwt.decode(jwt_token, get_jwt_secret(), algorithms=["HS256"])
                user_id = payload.get('user_id')
                if user_id:
                    from shared.database import get_db_connection
                    with get_db_connection() as conn:
                        user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
                        if user:
                            user_dict = dict(user)
                            user_dict['circle'] = payload.get('circle')
                            user_dict['app_route'] = payload.get('app_route')
                            return user_dict
            except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
                return None
        return None

    @staticmethod
    def has_permission(role: str, permission: str) -> bool:
        if not role in PERMISSIONS:
            return False
        user_perms = PERMISSIONS[role]
        return '*' in user_perms or permission in user_perms

    @staticmethod
    def get_app_route_for_role(role: str) -> str:
        if role in INNER_ROLES:
            return "both"
        elif role in ["vip"]:
            return "investment"
        return "neighborhood"

from authlib.integrations.flask_client import OAuth
oauth = OAuth()

def setup_oauth(app):
    oauth.init_app(app)
    google_id = os.getenv('GOOGLE_CLIENT_ID')
    google_secret = os.getenv('GOOGLE_CLIENT_SECRET')
    if google_id and google_secret:
        try:
            oauth.register(
                name='google',
                client_id=google_id,
                client_secret=google_secret,
                server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
                client_kwargs={'scope': 'openid email profile'}
            )
        except Exception as e:
            app.logger.error(f"Google OAuth register error: {e}")

class UnifiedIdentityService:
    @staticmethod
    def audit_log(user_id: int, action: str, details: dict):
        from shared.database import get_db_connection
        with get_db_connection() as conn:
            conn.execute('INSERT INTO auth_audit_log (user_id, action, details) VALUES (?, ?, ?)', 
                         (user_id, action, json.dumps(details)))

    @staticmethod
    def link_identity(user_id: int, provider: str, provider_id: str, email: str, is_verified: bool = False):
        from shared.database import get_db_connection
        with get_db_connection() as conn:
            existing = conn.execute('SELECT * FROM user_identities WHERE provider = ? AND provider_id = ? AND deleted_at IS NULL',
                                    (provider, provider_id)).fetchone()
            if existing: return
            
            count = conn.execute('SELECT COUNT(*) FROM user_identities WHERE user_id = ? AND deleted_at IS NULL', (user_id,)).fetchone()[0]
            is_primary = count == 0
            conn.execute('INSERT INTO user_identities (user_id, provider, provider_id, email, is_verified, is_primary) VALUES (?,?,?,?,?,?)',
                         (user_id, provider, provider_id, email, is_verified, is_primary))
            UnifiedIdentityService.audit_log(user_id, 'link', {'provider': provider, 'email': email})

    @staticmethod
    def get_user_identities(user_id: int):
        from shared.database import get_db_connection
        with get_db_connection() as conn:
            rows = conn.execute('SELECT * FROM user_identities WHERE user_id = ? AND deleted_at IS NULL', (user_id,)).fetchall()
            return [dict(r) for r in rows]
