from typing import Optional, List, Dict, Any
from shared.database import get_db
# from .service import AuthService  # REMOVED TO BREAK CIRCULAR IMPORT

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
        with get_db() as conn:
            username = data.get('username')
            role = data.get('role')
            email = data.get('email')
            raw_password = data.get('password') or data.get('password_hash')
            from .service import AuthService
            pwd_hash = AuthService.hash_password(raw_password)
            is_admin = data.get('is_admin', 0)
            
            cursor = conn.execute(
                'INSERT INTO users (username, password_hash, role, email, is_admin) VALUES (?,?,?,?,?)',
                (username, pwd_hash, role, email, is_admin)
            )
            user_id = cursor.lastrowid
            
            # CRM Sync
            if role in ['kiraci', 'vip', 'muteahhit', 'standart', 'broker']:
                category_map = {
                    'kiraci': 'tenant', 'vip': 'client', 'muteahhit': 'partner', 
                    'standart': 'client', 'broker': 'partner'
                }
                try:
                    conn.execute('''
                        INSERT INTO contacts (name, category, source_table, source_id, notes)
                        VALUES (?, ?, 'users', ?, ?)
                    ''', (username, category_map.get(role, 'other'), user_id, f"Kullanıcı oluşturuldu. Rol: {role}"))
                except: pass
                
            conn.commit()
            return user_id

    @staticmethod
    def update(user_id: int, data: Dict[str, Any]) -> bool:
        with get_db() as conn:
            fields = []
            values = []
            
            if 'username' in data:
                fields.append("username=?")
                values.append(data['username'])
            
            if 'role' in data:
                fields.append("role=?")
                values.append(data['role'])
            
            if 'is_admin' in data:
                fields.append("is_admin=?")
                values.append(data['is_admin'])
                
            raw_password = data.get('password') or data.get('password_hash')
            if raw_password:
                from .service import AuthService
                fields.append("password_hash=?")
                values.append(AuthService.hash_password(raw_password))
            
            if not fields: return False
            
            values.append(user_id)
            cursor = conn.execute(f'UPDATE users SET {", ".join(fields)} WHERE id=?', values)
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def delete(user_id: int) -> bool:
        with get_db() as conn:
            cursor = conn.execute('DELETE FROM users WHERE id=?', (user_id,))
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def get_or_create_social_user(email: str, provider: str, social_id: str, picture: str = None) -> int:
        from shared.database import get_db_connection
        import secrets
        from .service import UnifiedAuthService
        
        with get_db_connection() as conn:
            # Check user_identities first
            identity = conn.execute(
                'SELECT user_id FROM user_identities WHERE provider = ? AND provider_id = ? AND deleted_at IS NULL',
                (provider, social_id)
            ).fetchone()
            
            if identity:
                return identity['user_id']
                
            # Check if a user with this email already exists
            user = conn.execute('SELECT id FROM users WHERE email = ?', (email,)).fetchone()
            
            if user:
                user_id = user['id']
                # Link this identity to existing user
                UnifiedAuthService.link_identity(user_id, provider, social_id, email, True)
                return user_id
                
            # If completely new user, create it
            base_username = email.split('@')[0]
            username = base_username
            counter = 1
            while conn.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone():
                username = f"{base_username}{counter}"
                counter += 1
            
            from .service import AuthService
            pwd_hash = AuthService.hash_password(secrets.token_hex(16))
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (username, password_hash, role, email, email_verified)
                VALUES (?, ?, ?, ?, ?)
            ''', (username, pwd_hash, 'standart', email, 1))
            conn.commit() # Commit so UnifiedAuthService can reference it
            user_id = cursor.lastrowid
            
        # Link this identity to newly created user
        UnifiedAuthService.link_identity(user_id, provider, social_id, email, True)
        
        return user_id
