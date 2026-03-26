from typing import Optional, List, Dict, Any
from flask import Blueprint, request, jsonify, g
from database import get_db
from api.utils import sanitize_input
from .schemas import user_schema, ValidationError
from .auth import hash_password, require_permission

users_bp = Blueprint('users', __name__)

class UserRepository:
    """Handles low-level SQL operations for Users (Section 5.3)."""
    
    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        with get_db() as conn:
            rows = conn.execute('SELECT id, username, role, email, profile_pic FROM users').fetchall()
            return [dict(r) for r in rows]

    @staticmethod
    def get_by_id(user_id: int) -> Optional[Dict[str, Any]]:
        with get_db() as conn:
            row = conn.execute('SELECT id, username, role, email, profile_pic FROM users WHERE id = ?', (user_id,)).fetchone()
            return dict(row) if row else None

    @staticmethod
    def create(data: Dict[str, Any]) -> int:
        with get_db() as conn:
            # 1. Prepare User Data
            username = data.get('username')
            role = data.get('role')
            email = data.get('email')
            raw_password = data.get('password') or data.get('password_hash')
            pwd_hash = hash_password(raw_password)
            
            # 2. Insert User
            cursor = conn.execute(
                'INSERT INTO users (username, password_hash, role, email) VALUES (?,?,?,?)',
                (username, pwd_hash, role, email)
            )
            user_id = cursor.lastrowid
            
            # 3. CRM Sync (Preserve Legacy Logic)
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
                
            raw_password = data.get('password') or data.get('password_hash')
            if raw_password:
                fields.append("password_hash=?")
                values.append(hash_password(raw_password))
            
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

class UserService:
    """Handles business logic and validation for Users (Section 5.3)."""

    @staticmethod
    def validate_and_create(data: Dict[str, Any]) -> Dict[str, Any]:
        # 1. Sanitization & Validation
        sanitized_data = sanitize_input(data)
        validated_data = user_schema.load(sanitized_data)
        
        # 2. Persistence
        user_id = UserRepository.create(validated_data)
        return UserRepository.get_by_id(user_id)

@users_bp.route('/api/users', methods=['GET'])
@require_permission('admin')
def get_users():
    return jsonify(UserRepository.get_all()), 200

@users_bp.route('/api/users/<int:id>', methods=['GET'])
@require_permission('admin')
def get_user(id):
    user = UserRepository.get_by_id(id)
    return jsonify(user) if user else (jsonify({'error': 'User not found'}), 404)

@users_bp.route('/api/users', methods=['POST'])
@require_permission('admin')
def add_user():
    try:
        user = UserService.validate_and_create(request.json)
        return jsonify(user), 201
    except ValidationError as err:
        return jsonify({"error": "Geçersiz veri", "details": err.messages}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@users_bp.route('/api/users/<int:id>', methods=['PUT'])
@require_permission('admin')
def update_user(id):
    if UserRepository.update(id, request.json):
        return jsonify({'status': 'updated'}), 200
    return jsonify({'error': 'User not found'}), 404

@users_bp.route('/api/users/<int:id>', methods=['DELETE'])
@require_permission('admin')
def delete_user(id):
    if UserRepository.delete(id):
        return jsonify({'status': 'deleted'}), 200
    return jsonify({'error': 'User not found'}), 404
