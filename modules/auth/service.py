import os
import datetime
import hashlib
import jwt
import bcrypt
from flask import request, jsonify, g
from shared.database import get_db_connection
from shared.extensions import limiter

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

class AuthService:
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
                    new_hash = AuthService.hash_password(plain_password)
                    with get_db_connection() as conn:
                        conn.execute('UPDATE users SET password_hash = ? WHERE id = ?', (new_hash, user_id))
                        # conn.commit() - get_db context manager handles commit
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
        if role in ["admin", "super_admin", "broker", "danisman", "m_sahibi"]:
            return "both"
        elif role in ["vip"]:
            return "investment"
        return "neighborhood"

from authlib.integrations.flask_client import OAuth
oauth = OAuth()

def setup_oauth(app):
    """Configures OAuth client and registers providers."""
    oauth.init_app(app)
    
    oauth.register(
        name='google',
        client_id=os.getenv('GOOGLE_CLIENT_ID'),
        client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={
            'scope': 'openid email profile'
        }
    )
