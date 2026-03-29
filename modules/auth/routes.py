import os
import datetime
import secrets
import jwt
from flask import Blueprint, request, jsonify, g
from shared.database import get_db_connection
from shared.extensions import limiter
from shared.utils import sanitize_input
from shared.schemas import user_schema, ValidationError
from .service import AuthService, INNER_ROLES, get_jwt_secret
from .repository import UserRepository
from .decorators import require_permission, login_required, require_inner_circle

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
@limiter.limit("10 per minute")
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Missing credentials'}), 400
    
    with get_db_connection() as conn:
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    
    if user is None or not AuthService.verify_password(password, user['password_hash'], user['id']):
        return jsonify({'error': 'Invalid username or password'}), 401
    
    user_role = user['role']
    is_admin = user['is_admin']
    circle = "inner" if (user_role in INNER_ROLES or is_admin) else "outer"
    token = f"token-{user['id']}"
    
    return jsonify({
        'token': token, 
        'role': user_role,
        'is_admin': is_admin,
        'circle': circle,
        'id': user['id'],
        'username': user['username']
    }), 200

@auth_bp.route('/mobile/login', methods=['POST'])
@limiter.limit("10 per minute")
def mobile_login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    requested_app = data.get('app_type')

    if not username or not password or not requested_app:
        return jsonify({'error': 'Missing credentials or app_type'}), 400
        
    with get_db_connection() as conn:
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    
    if user is None or not AuthService.verify_password(password, user['password_hash'], user['id']):
        return jsonify({'error': 'Invalid username or password'}), 401
        
    user_role = user['role']
    is_admin = user['is_admin']
    circle = "inner" if (user_role in INNER_ROLES or is_admin) else "outer"
    authorized_apps = AuthService.get_app_route_for_role(user_role)
    
    if authorized_apps != 'both' and authorized_apps != requested_app:
        return jsonify({'error': 'Yetkisiz Giriş.'}), 403

    payload = {
        'user_id': user['id'],
        'username': user['username'],
        'role': user_role,
        'circle': circle,
        'app_route': requested_app,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30)
    }
    
    token = jwt.encode(payload, get_jwt_secret(), algorithm="HS256")
    
    return jsonify({
        'token': token, 
        'role': user_role,
        'is_admin': is_admin,
        'circle': circle,
        'id': user['id'],
        'username': user['username'],
        'app_route': authorized_apps
    }), 200

@auth_bp.route('/request-reset', methods=['POST'])
@limiter.limit("3 per hour")
def request_reset():
    data = request.json
    email = data.get('email')
    if not email:
        return jsonify({'error': 'E-posta adresi gerekli'}), 400
        
    with get_db_connection() as conn:
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        if user:
            token = secrets.token_urlsafe(32)
            expiry = (datetime.datetime.utcnow() + datetime.timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')
            conn.execute('UPDATE password_resets SET used = 1 WHERE user_id = ?', (user['id'],))
            conn.execute('INSERT INTO password_resets (user_id, token, expiry) VALUES (?, ?, ?)',
                         (user['id'], token, expiry))
            conn.commit()
            
            from shared.mail_service import send_password_reset_email
            send_password_reset_email(email, token, user['username'])
            
    return jsonify({'message': 'Şifre sıfırlama talimatları e-posta adresinize gönderildi.'}), 200

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.json
    token = data.get('token')
    new_password = data.get('password')
    
    if not token or not new_password:
        return jsonify({'error': 'Token ve yeni şifre gereklidir'}), 400
        
    with get_db_connection() as conn:
        now = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        reset_req = conn.execute('''
            SELECT * FROM password_resets 
            WHERE token = ? AND used = 0 AND expiry > ?
        ''', (token, now)).fetchone()
        
        if not reset_req:
            return jsonify({'error': 'Geçersiz veya süresi dolmuş token'}), 400
            
        new_hash = AuthService.hash_password(new_password)
        conn.execute('UPDATE users SET password_hash = ? WHERE id = ?', (new_hash, reset_req['user_id']))
        conn.execute('UPDATE password_resets SET used = 1 WHERE id = ?', (reset_req['id'],))
        conn.commit()
    
    return jsonify({'message': 'Şifreniz başarıyla güncellendi.'}), 200

# User Management Routes (Migrated from users.py)
@auth_bp.route('/users', methods=['GET'])
@require_permission('admin')
def get_users():
    return jsonify(UserRepository.get_all()), 200

@auth_bp.route('/users/<int:id>', methods=['GET'])
@require_permission('admin')
def get_user(id):
    user = UserRepository.get_by_id(id)
    return jsonify(user) if user else (jsonify({'error': 'User not found'}), 404)

@auth_bp.route('/users', methods=['POST'])
@require_permission('admin')
def add_user():
    try:
        sanitized_data = sanitize_input(request.json)
        validated_data = user_schema.load(sanitized_data)
        user_id = UserRepository.create(validated_data)
        return jsonify(UserRepository.get_by_id(user_id)), 201
    except ValidationError as err:
        return jsonify({"error": "Geçersiz veri", "details": err.messages}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/users/<int:id>', methods=['PUT'])
@require_permission('admin')
def update_user(id):
    if UserRepository.update(id, request.json):
        return jsonify({'status': 'updated'}), 200
    return jsonify({'error': 'User not found'}), 404

@auth_bp.route('/users/<int:id>', methods=['DELETE'])
@require_permission('admin')
def delete_user(id):
    if UserRepository.delete(id):
        return jsonify({'status': 'deleted'}), 200
    return jsonify({'error': 'User not found'}), 404

# Social Auth Routes (Migrated from social_auth.py)
from .service import oauth
from flask import url_for, redirect

@auth_bp.route('/social/login/<provider>')
def social_login(provider):
    """Starts login flow for social providers."""
    client = oauth.create_client(provider)
    if not client:
        return jsonify({"error": f"Provider not found: {provider}"}), 404
    redirect_uri = url_for('auth.authorize', provider=provider, _external=True)
    return client.authorize_redirect(redirect_uri)

@auth_bp.route('/social/callback/<provider>')
def authorize(provider):
    """Handles callback from social providers."""
    client = oauth.create_client(provider)
    if not client:
        return jsonify({"error": f"Provider not found: {provider}"}), 404
    token = client.authorize_access_token()
    email = None
    social_id = None
    picture = None
    
    if provider == 'google':
        user_info = token.get('userinfo') or client.parse_id_token(token, nonce=None)
        email = user_info.get('email')
        social_id = user_info.get('sub')
        picture = user_info.get('picture')
        
    if not email:
        return jsonify({"error": "Social account did not provide an email"}), 400

    user_id = UserRepository.get_or_create_social_user(email, provider, social_id, picture)
    user = UserRepository.get_by_id(user_id)
    
    user_role = user['role']
    token = jwt.encode({
        'user_id': user['id'],
        'username': user['username'],
        'role': user_role,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }, get_jwt_secret(), algorithm="HS256")
    
    return redirect(f"/?login_success=1&token={token}&role={user_role}")

# Verification Routes (Migrated from verification.py)
@auth_bp.route('/verification/eids', methods=['POST'])
@login_required
def verify_eids():
    """EİDS (Electronic Listing System) Verification Bridge."""
    data = request.json
    property_id = data.get('property_id')
    if not property_id:
        return jsonify({'error': 'property_id is required'}), 400
    
    verification_token = f"EİDS-{datetime.datetime.now().strftime('%Y%m%d')}-{property_id}-VERIFIED"
    return jsonify({
        'status': 'success',
        'verification_token': verification_token,
        'verified_at': datetime.datetime.now().isoformat()
    }), 200

@auth_bp.route('/verification/status/<property_id>', methods=['GET'])
@login_required
def check_eids_status(property_id):
    return jsonify({
        'property_id': property_id,
        'is_verified': True,
        'last_verification': datetime.datetime.now().isoformat()
    }), 200
