from functools import wraps
from flask import Blueprint, request, jsonify, g
from database import get_db_connection
import hashlib
import jwt
import os
import datetime
import bcrypt
from extensions import limiter

auth_bp = Blueprint('auth', __name__)

# Geliştirme ortamı için geçici bir JWT secret key. Prod. için .env'den alınmalıdır.
JWT_SECRET = os.environ.get("JWT_SECRET", "imza-super-secret-key-2026")

def hash_password(password):
    """Yeni oluşturulan şifreler için bcrypt kullanır."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password, stored_hash, user_id=None):
    """Şifre doğrulaması yapar ve eski tip SHA256 şifreleri anında bcrypt'e günceller."""
    if stored_hash.startswith('$2b$') or stored_hash.startswith('$2a$') or stored_hash.startswith('$2y$'):
        try:
            return bcrypt.checkpw(plain_password.encode('utf-8'), stored_hash.encode('utf-8'))
        except ValueError:
            return False
    else:
        # Legacy SHA256 Fallback
        legacy_hash = hashlib.sha256(plain_password.encode('utf-8')).hexdigest()
        if legacy_hash == stored_hash:
            # Seamless Migration: Bcrypt ile re-hash ve DB update
            if user_id:
                new_hash = hash_password(plain_password)
                conn = get_db_connection()
                try:
                    conn.execute('UPDATE users SET password_hash = ? WHERE id = ?', (new_hash, user_id))
                    conn.commit()
                finally:
                    conn.close()
            return True
        return False

INNER_ROLES = ["admin", "super_admin", "broker", "danisman"]

# Permission Map (ÖNERİ-005)
PERMISSIONS = {
    'admin': ['*'],
    'super_admin': ['*'],
    'broker': ['*'],
    'danisman': ['portfolio.view', 'portfolio.create', 'leads.view', 'leads.edit'],
    'contractor': ['portfolio.view', 'projects.view'],
    'm_sahibi': ['portfolio.view'],
    'kiraci': ['portfolio.view'],
    'standart': ['portfolio.view']
}

def has_permission(role, permission):
    if not role in PERMISSIONS:
        return False
    user_perms = PERMISSIONS[role]
    return '*' in user_perms or permission in user_perms

def require_permission(permission):
    from functools import wraps
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user = get_current_user()
            if not user or not has_permission(user.get('role'), permission):
                return jsonify({'error': f'Forbidden - Missing permission: {permission}'}), 403
            g.user = user
            return f(*args, **kwargs)
        return wrapper
    return decorator

def get_current_user():
    token = request.headers.get('Authorization')
    if not token:
        return None
        
    # Bypass Tokens (Sadece Geliştirme/Test için, .env'den yönetilmeli)
    MASTER_TOKEN = os.environ.get("MASTER_AUTH_TOKEN")
    if MASTER_TOKEN and token == f'Bearer {MASTER_TOKEN}':
        return {'id': 1, 'role': 'admin', 'username': 'admin', 'circle': 'inner', 'app_route': 'both'}
    
    # Simple Web Token (Custom Format)
    if token.startswith('Bearer token-'):
        user_id = token.split('token-')[1]
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        conn.close()
        if user:
            user_dict = dict(user)
            user_dict['circle'] = 'inner' if user['role'] in INNER_ROLES else 'outer'
            user_dict['app_route'] = get_app_route_for_role(user['role'])
            return user_dict
            
    # JWT Mobile Token
    if token.startswith('Bearer ey'):
        jwt_token = token.split(' ')[1]
        try:
            payload = jwt.decode(jwt_token, JWT_SECRET, algorithms=["HS256"])
            user_id = payload.get('user_id')
            if user_id:
                conn = get_db_connection()
                user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
                conn.close()
                if user:
                    user_dict = dict(user)
                    user_dict['circle'] = payload.get('circle')
                    user_dict['app_route'] = payload.get('app_route')
                    return user_dict
        except jwt.ExpiredSignatureError:
            return None # Handle token expiration appropriately
        except jwt.InvalidTokenError:
            return None
            
    return None

def get_app_route_for_role(role):
    """Belirli bir role sahip kullanıcının hangi uygulamalara girebileceğini belirler."""
    if role in ["admin", "super_admin", "broker", "danisman", "m_sahibi"]:
        return "both" # Hem Yatırım hem Mahalle
    elif role in ["vip"]:
        return "investment" # Sadece Yatırım App
    elif role in ["kiraci", "standart"]:
        return "neighborhood" # Sadece Mahalle App
    return "neighborhood" # Default fallback

def require_inner_circle(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        user = get_current_user()
        if not user or user.get('circle') != 'inner':
            return jsonify({'error': 'Unauthorized - Inner Circle Only'}), 403
        g.user = user
        return f(*args, **kwargs)
    return wrapper

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        user = get_current_user()
        if not user:
            return jsonify({'error': 'Unauthorized'}), 401
        g.user = user
        return f(*args, **kwargs)
    return wrapper

@auth_bp.route('/api/login', methods=['POST'])
@limiter.limit("10 per minute")
def login():
    """Web (Admin) Portalı için Basit Login"""
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Missing credentials'}), 400
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    if user is None:
        return jsonify({'error': 'Invalid username or password'}), 401
    
    if not verify_password(password, user['password_hash'], user['id']):
        return jsonify({'error': 'Invalid username or password'}), 401
    
    user_role = user['role']
    circle = "inner" if user_role in INNER_ROLES else "outer"
    token = f"token-{user['id']}"
    
    return jsonify({
        'token': token, 
        'role': user_role,
        'circle': circle,
        'username': user['username']
    }), 200

@auth_bp.route('/api/mobile/login', methods=['POST'])
@limiter.limit("10 per minute")
def mobile_login():
    """Mobil Uygulamalar için JWT tabanlı Login"""
    data = request.json
    username = data.get('username')
    password = data.get('password')
    requested_app = data.get('app_type') # 'investment' veya 'neighborhood'

    if not username or not password or not requested_app:
        return jsonify({'error': 'Missing credentials or app_type'}), 400
        
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    
    if user is None or not verify_password(password, user['password_hash'], user['id']):
        return jsonify({'error': 'Invalid username or password'}), 401
        
    user_role = user['role']
    circle = "inner" if user_role in INNER_ROLES else "outer"
    authorized_apps = get_app_route_for_role(user_role)
    
    # App giriş izni kontrolü
    if authorized_apps != 'both' and authorized_apps != requested_app:
        app_names = {"investment": "İmza Gayrimenkul & Yatırım", "neighborhood": "İmza Mahalle"}
        return jsonify({'error': f'Yetkisiz Giriş. Rolünüz ({user_role}) {app_names.get(requested_app)} uygulaması için yetkili değil.'}), 403

    # JWT Payload Oluşturma
    payload = {
        'user_id': user['id'],
        'username': user['username'],
        'role': user_role,
        'circle': circle,
        'app_route': requested_app,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30) # 30 gün geçerli
    }
    
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    
    return jsonify({
        'token': token, 
        'role': user_role,
        'circle': circle,
        'username': user['username'],
        'app_route': authorized_apps
    }), 200
import secrets

@auth_bp.route('/api/auth/request-reset', methods=['POST'])
@limiter.limit("3 per hour")
def request_reset():
    """Şifre sıfırlama talebi oluşturur ve e-posta gönderir."""
    data = request.json
    email = data.get('email')
    if not email:
        return jsonify({'error': 'E-posta adresi gerekli'}), 400
        
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    
    if user:
        # Token oluştur (32 karakterlik güvenli bir dize)
        token = secrets.token_urlsafe(32)
        expiry = (datetime.datetime.utcnow() + datetime.timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')
        
        # Mevcut kullanılmamış token'ları geçersiz kıl
        conn.execute('UPDATE password_resets SET used = 1 WHERE user_id = ?', (user['id'],))
        
        # Yeni token'ı kaydet
        conn.execute('INSERT INTO password_resets (user_id, token, expiry) VALUES (?, ?, ?)',
                     (user['id'], token, expiry))
        conn.commit()
        
        # E-posta gönder (Arka planda gönderilmesi daha iyidir ama şimdilik senkron)
        from api.mail_service import send_password_reset_email
        success, msg = send_password_reset_email(email, token, user['username'])
        
        if not success:
            conn.close()
            # Gerçekte güvenlik için hata mesajı detaylı verilmemeli ama geliştirme için veriyoruz
            return jsonify({'error': 'E-posta gönderilemedi', 'details': msg}), 500
            
    conn.close()
    
    # Güvenlik için kullanıcı olsa da olmasa da "Eğer kayıtlıysanız e-posta gönderildi" mesajı verilir
    return jsonify({'message': 'Şifre sıfırlama talimatları e-posta adresinize gönderildi.'}), 200

@auth_bp.route('/api/auth/reset-password', methods=['POST'])
def reset_password():
    """Token ile şifreyi sıfırlar."""
    data = request.json
    token = data.get('token')
    new_password = data.get('password')
    
    if not token or not new_password:
        return jsonify({'error': 'Token ve yeni şifre gereklidir'}), 400
        
    conn = get_db_connection()
    now = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    
    reset_req = conn.execute('''
        SELECT * FROM password_resets 
        WHERE token = ? AND used = 0 AND expiry > ?
    ''', (token, now)).fetchone()
    
    if not reset_req:
        conn.close()
        return jsonify({'error': 'Geçersiz veya süresi dolmuş token'}), 400
        
    # Şifreyi güncelle
    new_hash = hash_password(new_password)
    conn.execute('UPDATE users SET password_hash = ? WHERE id = ?', (new_hash, reset_req['user_id']))
    
    # Token'ı kullanıldı olarak işaretle
    conn.execute('UPDATE password_resets SET used = 1 WHERE id = ?', (reset_req['id'],))
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Şifreniz başarıyla güncellendi.'}), 200
