from typing import Optional, List, Dict, Any
from shared.database import get_db
from .service import AuthService

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
