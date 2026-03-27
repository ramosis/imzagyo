from flask import Blueprint, request, jsonify
from shared.database import get_db
from .auth import require_inner_circle, get_current_user

notifications_bp = Blueprint('notifications', __name__)

@notifications_bp.route('', methods=['GET'])
def get_notifications():
    """Kullanıcının okunmamış bildirimlerini getirir."""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401
    
    with get_db() as conn:
        notifications = conn.execute('''
            SELECT * FROM notifications 
            WHERE user_id = ? 
            ORDER BY created_at DESC 
            LIMIT 20
        ''', (user['id'],)).fetchall()
    
    return jsonify([dict(n) for n in notifications]), 200

@notifications_bp.route('/<int:id>/read', methods=['PUT'])
def mark_as_read(id):
    """Bildirimi okundu olarak işaretler."""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401
    
    with get_db() as conn:
        cur = conn.execute('''
            UPDATE notifications 
            SET status = 'read' 
            WHERE id = ? AND user_id = ?
        ''', (id, user['id']))
        conn.commit()
    
    if cur.rowcount == 0:
        return jsonify({'error': 'Notification not found or access denied'}), 404
    return jsonify({'status': 'success'}), 200
        
@notifications_bp.route('/read-all', methods=['POST'])
def mark_all_as_read():
    """Tüm bildirimleri okundu olarak işaretler."""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401
    
    with get_db() as conn:
        conn.execute('''
            UPDATE notifications 
            SET status = 'read' 
            WHERE user_id = ? AND status = 'unread'
        ''', (user['id'],))
        conn.commit()
    
    return jsonify({'status': 'all marked as read'}), 200

# Yardımcı fonksiyon: Diğer modüllerden bildirim oluşturmak için
def create_notification(user_id, n_type, title, message):
    with get_db() as conn:
        conn.execute('''
            INSERT INTO notifications (user_id, type, title, message)
            VALUES (?, ?, ?, ?)
        ''', (user_id, n_type, title, message))
        conn.commit()
