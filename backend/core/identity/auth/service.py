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
    'customer': ['customer.portal'], # Sadece kendi portalını görebilir
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
                    from backend.shared.database import db_session
                    from .models import User
                    user = db_session.query(User).get(user_id)
                    if user:
                        user.password_hash = new_hash
                        db_session.commit()
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
                    from backend.shared.database import db_session
                    from .models import User
                    user = db_session.query(User).get(user_id)
                    if user:
                        # Convert to dict for legacy compatibility if needed, 
                        # or keep as object. Most routes expect dict.
                        user_dict = {
                            'id': user.id,
                            'username': user.username,
                            'role': user.role,
                            'is_admin': user.is_admin,
                            'email': user.email
                        }
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
        elif role in ["customer"]:
            return "customer_portal" # New route for customers
        return "neighborhood"

class UnifiedAuthService:
    @staticmethod
    def audit_log(user_id: int, action: str, details: dict):
        from backend.shared.database import db_session
        from .models import AuthAuditLog
        log = AuthAuditLog(user_id=user_id, action=action, details=json.dumps(details))
        db_session.add(log)
        db_session.commit()

    @staticmethod
    def link_identity(user_id: int, provider: str, provider_id: str, email: str, is_verified: bool = False):
        from backend.shared.database import db_session
        from .models import UserIdentity
        
        existing = db_session.query(UserIdentity).filter_by(
            provider=provider, provider_id=provider_id, deleted_at=None
        ).first()
        
        if existing:
            if existing.user_id != user_id:
                raise Exception("Bu hesap başka bir kullanıcıya bağlı.")
            return 
        
        count = db_session.query(UserIdentity).filter_by(user_id=user_id, deleted_at=None).count()
        is_primary = count == 0

        new_identity = UserIdentity(
            user_id=user_id, provider=provider, provider_id=provider_id, 
            email=email, is_verified=is_verified, is_primary=is_primary
        )
        db_session.add(new_identity)
        db_session.commit()
        
        UnifiedAuthService.audit_log(user_id, 'link', {'provider': provider, 'email': email})

    @staticmethod
    def unlink_identity(user_id: int, identity_id: int):
        from backend.shared.database import db_session
        from .models import UserIdentity
        
        identity = db_session.query(UserIdentity).filter_by(id=identity_id, user_id=user_id, deleted_at=None).first()
        
        if not identity:
            raise Exception("Kimlik bulunamadı veya zaten silinmiş.")
            
        if identity.is_primary:
            raise Exception("Ana kimlik silinemez. Önce başka bir kimliği ana yapın.")

        identity.deleted_at = datetime.datetime.utcnow()
        identity.is_primary = False
        db_session.commit()
        
        UnifiedAuthService.audit_log(user_id, 'unlink', {'provider': identity.provider, 'identity_id': identity_id})

    @staticmethod
    def set_primary_identity(user_id: int, identity_id: int):
        from backend.shared.database import db_session
        from .models import UserIdentity
        
        identity = db_session.query(UserIdentity).filter_by(id=identity_id, user_id=user_id, deleted_at=None).first()
        if not identity:
            raise Exception("Geçerli bir kimlik bulunamadı.")
            
        db_session.query(UserIdentity).filter_by(user_id=user_id).update({UserIdentity.is_primary: False})
        identity.is_primary = True
        db_session.commit()
        
        UnifiedAuthService.audit_log(user_id, 'set_primary', {'provider': identity.provider, 'identity_id': identity_id})

    @staticmethod
    def get_user_identities(user_id: int):
        from backend.shared.database import db_session
        from .models import UserIdentity
        identities = db_session.query(UserIdentity).filter_by(user_id=user_id, deleted_at=None).all()
        return [{
            'id': i.id, 'provider': i.provider, 'provider_id': i.provider_id,
            'email': i.email, 'is_verified': i.is_verified, 'is_primary': i.is_primary
        } for i in identities]
            
    @staticmethod
    def get_audit_logs(user_id: int = None, limit: int = 50):
        from backend.shared.database import db_session
        from .models import AuthAuditLog
        
        query = db_session.query(AuthAuditLog)
        if user_id:
            query = query.filter_by(user_id=user_id)
        
        logs = query.order_by(AuthAuditLog.created_at.desc()).limit(limit).all()
        return [{
            'id': l.id, 'user_id': l.user_id, 'action': l.action, 
            'details': l.details, 'created_at': l.created_at.isoformat()
        } for l in logs]
