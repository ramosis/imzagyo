from flask import Blueprint, request, jsonify
from database import get_db_connection
import json
from .auth import hash_password

users_bp = Blueprint('users', __name__)

@users_bp.route('/api/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    users = conn.execute('SELECT id, username, role FROM users').fetchall()
    conn.close()
    result = [dict(u) for u in users]
    return jsonify(result)

@users_bp.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        raw_password = data.get('password') or data.get('password_hash') # Frontend'den gelen ham şifre
        pwd_hash = hash_password(raw_password)
        cur.execute('INSERT INTO users (username, password_hash, role) VALUES (?,?,?)',
                    (data.get('username'), pwd_hash, data.get('role')))
        user_id = cur.lastrowid
        role = data.get('role')

        # --- REHBERE (CONTACTS) SENKRONİZE ET ---
        if role in ['kiraci', 'vip', 'muteahhit', 'standart', 'broker']:
            category_map = {
                'kiraci': 'tenant',
                'vip': 'client',
                'muteahhit': 'partner',
                'standart': 'client',
                'broker': 'partner'
            }
            try:
                cur.execute('''
                    INSERT INTO contacts (name, category, source_table, source_id, notes)
                    VALUES (?, ?, 'users', ?, ?)
                ''', (data.get('username'), category_map.get(role, 'other'), user_id, f"Sistem kullanıcısı olarak oluşturuldu. Rol: {role}"))
            except cur.IntegrityError:
                pass # Zaten varsa geç

        conn.commit()
        return jsonify({'status': 'created', 'user_id': user_id}), 201
    finally:
        conn.close()

@users_bp.route('/api/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    raw_password = data.get('password') or data.get('password_hash')
    if raw_password:
        pwd_hash = hash_password(raw_password)
        cur.execute('UPDATE users SET username=?, password_hash=?, role=? WHERE id=?',
                    (data.get('username'), pwd_hash, data.get('role'), id))
    else:
        cur.execute('UPDATE users SET username=?, role=? WHERE id=?',
                    (data.get('username'), data.get('role'), id))
    conn.commit()
    conn.close()
    return jsonify({'status': 'updated'}), 200

@users_bp.route('/api/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM users WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'deleted'}), 200
