from flask import Blueprint, jsonify, request
import sqlite3
import datetime
from .auth import require_inner_circle, get_current_user

campaigns_bp = Blueprint('campaigns', __name__)

def get_db_connection():
    conn = sqlite3.connect('imza_database.db')
    conn.row_factory = sqlite3.Row
    return conn

# MAİL GÖNDERME SİMÜLASYONU (Test / Log Mode)
def send_dummy_email(recipient_email, recipient_name, subject, content_html, campaign_type):
    """
    Seçenek C: Gerçek bir SMTP sunucusuna bağlanmak yerine gönderimi simüle eder.
    Production ortamına geçildiğinde bu fonksiyon smtplib veya SendGrid API ile değiştirilecektir.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"""
    ================== E-POSTA GÖNDERİLDİ ==================
    Zaman: {timestamp}
    Tür: {campaign_type.upper()}
    Alıcı: {recipient_name} <{recipient_email}>
    Konu: {subject}
    --------------------------------------------------------
    İçerik Uzunluğu: {len(content_html)} karakter
    ========================================================
    """
    print(log_message)
    return True # Başarılı kabul et

@campaigns_bp.route('/api/campaigns', methods=['GET'])
@require_inner_circle
def get_campaigns():
    conn = get_db_connection()
    campaigns = conn.execute('''
        SELECT c.*, u.username as creator_name,
               (SELECT COUNT(*) FROM campaign_logs WHERE campaign_id = c.id) as total_sent
        FROM campaigns c
        LEFT JOIN users u ON c.created_by = u.id
        ORDER BY c.created_at DESC
    ''').fetchall()
    conn.close()
    return jsonify([dict(c) for c in campaigns])

@campaigns_bp.route('/api/campaigns', methods=['POST'])
@require_inner_circle
def create_campaign():
    data = request.json
    title = data.get('title')
    subject = data.get('subject')
    content_html = data.get('content_html')
    target_audience = data.get('target_audience')
    campaign_type = data.get('campaign_type', 'newsletter')
    
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401
    
    if not all([title, subject, content_html, target_audience]):
        return jsonify({'error': 'Eksik veri'}), 400

    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO campaigns (title, subject, content_html, target_audience, campaign_type, created_by, status)
            VALUES (?, ?, ?, ?, ?, ?, 'sending')
        ''', (title, subject, content_html, target_audience, campaign_type, user['id']))
        campaign_id = cursor.lastrowid
        
        # Hedef kitleye göre alıcıları belirle (Basit Demo: user tablosundan çek veya Leads'ten)
        # Gerçek senaryoda burada karmaşık filtrelemeler olur
        recipients = []
        if target_audience == 'all_users':
            users = cursor.execute("SELECT id, username, 'example@temp.com' as email FROM users WHERE role != 'admin'").fetchall()
            recipients = [{'email': u['email'], 'name': u['username']} for u in users]
        elif target_audience == 'leads':
            leads = cursor.execute("SELECT name, email FROM leads WHERE email IS NOT NULL").fetchall()
            recipients = [{'email': l['email'], 'name': l['name']} for l in leads]
        elif target_audience == 'test':
            # Sadece test amaçlı login olan kullanıcıya gönder
            recipients = [{'email': 'demo_test@imzagayrimenkul.local', 'name': 'IMZA Test User'}]
            
        success_count = 0
        for rec in recipients:
            email = rec['email']
            name = rec['name']
            
            # MAİLİ GÖNDER (SİMÜLASYON)
            success = send_dummy_email(email, name, subject, content_html, campaign_type)
            status = 'sent' if success else 'failed'
            if success: success_count += 1
            
            # LOG KAYIT
            cursor.execute('''
                INSERT INTO campaign_logs (campaign_id, recipient_email, recipient_name, status, sent_at)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (campaign_id, email, name, status))
            
        # Kampanya durumunu tamamlandı yap
        cursor.execute("UPDATE campaigns SET status = 'completed' WHERE id = ?", (campaign_id,))
        conn.commit()
        
        return jsonify({'message': f'Kampanya başarıyla {success_count} kişiye gönderildi.', 'id': campaign_id}), 201
        
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()
