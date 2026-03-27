from flask import Blueprint, url_for, request, jsonify, redirect
from authlib.integrations.flask_client import OAuth
import os
import secrets
from shared.database import get_db_connection
from api.auth import JWT_SECRET, get_app_route_for_role, INNER_ROLES, hash_password
import jwt

social_auth_bp = Blueprint('social_auth', __name__)
oauth = OAuth()

def setup_oauth(app):
    """OAuth istemcisini yapılandırır ve sağlayıcıları kaydeder."""
    oauth.init_app(app)
    
    # Provider: Google
    oauth.register(
        name='google',
        client_id=os.getenv('GOOGLE_CLIENT_ID'),
        client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={
            'scope': 'openid email profile'
        }
    )
    
    # Provider: Facebook (Şimdilik yer tutucu - benzer şekilde kaydedilecek)
    # oauth.register(
    #     name='facebook',
    #     client_id=os.getenv('FACEBOOK_CLIENT_ID'),
    #     client_secret=os.getenv('FACEBOOK_CLIENT_SECRET'),
    #     api_base_url='https://graph.facebook.com/',
    #     access_token_url='https://graph.facebook.com/oauth/access_token',
    #     authorize_url='https://www.facebook.com/dialog/oauth',
    #     client_kwargs={'scope': 'email public_profile'}
    # )

@social_auth_bp.route('/api/auth/login/<provider>')
def login(provider):
    """Belirtilen sosyal medya platformuna giriş işlemini başlatır."""
    client = oauth.create_client(provider)
    if not client:
        return jsonify({"error": f"Sağlayıcı bulunamadı: {provider}"}), 404
        
    redirect_uri = url_for('social_auth.authorize', provider=provider, _external=True)
    return client.authorize_redirect(redirect_uri)

@social_auth_bp.route('/api/auth/callback/<provider>')
def authorize(provider):
    """Sosyal ağdan gelen onayı işler ve kullanıcıyı oluşturur veya giriş yaptırır."""
    client = oauth.create_client(provider)
    if not client:
        return jsonify({"error": f"Sağlayıcı bulunamadı: {provider}"}), 404
        
    token = client.authorize_access_token()
    
    # Kullanıcı bilgilerini çıkart
    email = None
    social_id = None
    picture = None
    
    if provider == 'google':
        user_info = token.get('userinfo')
        if not user_info:
            user_info = client.parse_id_token(token, nonce=None)            
        email = user_info.get('email')
        social_id = user_info.get('sub')
        picture = user_info.get('picture')
    else:
        # Facebook vb diğer sağlayıcılar buraya eklenecek
        pass
        
    if not email:
        return jsonify({"error": "Sosyal hesap bir e-posta adresi sağlamadı!"}), 400

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE email = ? OR (social_provider = ? AND social_id = ?)', 
                        (email, provider, social_id)).fetchone()
    
    if not user:
        # Yeni Kullanıcı Oluştur
        base_username = email.split('@')[0]
        username = base_username
        counter = 1
        
        # Kullanıcı adı çakışmasını engelle
        while conn.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone():
            username = f"{base_username}{counter}"
            counter += 1
            
        random_password = hash_password(secrets.token_hex(16))
        
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (username, password_hash, role, email, social_provider, social_id, profile_pic)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (username, random_password, 'standart', email, provider, social_id, picture))
        conn.commit()
        user_id = cursor.lastrowid
        user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    else:
        # Mevcut Kullanıcı (sadece username ile kayıt olmuşsa social verileri ekle)
        if not user['social_provider']:
            conn.execute('''
                UPDATE users SET email = ?, social_provider = ?, social_id = ?, profile_pic = ?
                WHERE id = ?
            ''', (email, provider, social_id, picture, user['id']))
            conn.commit()

    conn.close()
    
    user_role = user['role']
    # Basit Portal Token'ı oluştur
    custom_token = f"token-{user['id']}"
    
    # Giriş başarılı ekrana veya popup kapatıcı koda yönlendirilebilir
    # Şimdilik ana sayfaya token ile yönlendiriyoruz (Frontend bu token'ı yakalamalı)
    return redirect(f"/?login_success=1&token={custom_token}&role={user_role}")
