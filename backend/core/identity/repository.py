from typing import Optional, List, Dict, Any
from shared.database import get_db

class UserRepository:
    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        with get_db() as conn:
            rows = conn.execute('SELECT id, username, role, email, is_admin, profile_pic FROM users').fetchall()
            return [dict(r) for r in rows]

    @staticmethod
    def get_by_id(user_id: int) -> Optional[Dict[str, Any]]:
        with get_db() as conn:
            row = conn.execute('SELECT id, username, role, email, is_admin, profile_pic FROM users WHERE id = ?', (user_id,)).fetchone()
            return dict(row) if row else None

    @staticmethod
    def create(data: Dict[str, Any]) -> int:
        from .service import IdentityService
        with get_db() as conn:
            username = data.get('username')
            role = data.get('role')
            email = data.get('email')
            raw_password = data.get('password') or data.get('password_hash')
            pwd_hash = IdentityService.hash_password(raw_password)
            is_admin = data.get('is_admin', 0)
            
            cursor = conn.execute(
                'INSERT INTO users (username, password_hash, role, email, is_admin) VALUES (?,?,?,?,?)',
                (username, pwd_hash, role, email, is_admin)
            )
            user_id = cursor.lastrowid
            conn.commit()
            return user_id

    @staticmethod
    def get_or_create_social_user(email: str, provider: str, social_id: str, picture: str = None) -> int:
        from shared.database import get_db_connection
        import secrets
        from .service import UnifiedIdentityService, IdentityService
        
        with get_db_connection() as conn:
            identity = conn.execute(
                'SELECT user_id FROM user_identities WHERE provider = ? AND provider_id = ? AND deleted_at IS NULL',
                (provider, social_id)
            ).fetchone()
            
            if identity: return identity['user_id']
                
            user = conn.execute('SELECT id FROM users WHERE email = ?', (email,)).fetchone()
            if user:
                user_id = user['id']
                UnifiedIdentityService.link_identity(user_id, provider, social_id, email, True)
                return user_id
                
            base_username = email.split('@')[0]
            pwd_hash = IdentityService.hash_password(secrets.token_hex(16))
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, password_hash, role, email, email_verified) VALUES (?, ?, ?, ?, ?)', 
                           (base_username, pwd_hash, 'standart', email, 1))
            conn.commit()
            user_id = cursor.lastrowid
            
        UnifiedIdentityService.link_identity(user_id, provider, social_id, email, True)
        return user_id
