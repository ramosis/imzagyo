from flask import request, jsonify
from shared.extensions import db
from . import notification_bp
from .models import Notification
from modules.auth.decorators import login_required
from flask import g

@notification_bp.route('/', methods=['GET'])
@login_required
def get_notifications():
    # Fetch notifications targeted at the user's role OR 'all'
    user_role = getattr(g.user, 'role', 'guest')
    
    notifications = Notification.query.filter(
        (Notification.target_role == user_role) | 
        (Notification.target_role == 'all')
    ).order_by(Notification.created_at.desc()).limit(50).all()
    
    return jsonify([{
        'id': n.id,
        'title': n.title,
        'message': n.message,
        'type': n.type,
        'created_at': n.created_at.isoformat(),
        'status': n.status
    } for n in notifications]), 200

@notification_bp.route('/unread-count', methods=['GET'])
@login_required
def get_unread_count():
    user_role = getattr(g.user, 'role', 'guest')
    count = Notification.query.filter(
        ((Notification.target_role == user_role) | (Notification.target_role == 'all')),
        (Notification.status == 'unread')
    ).count()
    return jsonify({'unread_count': count}), 200

@notification_bp.route('/', methods=['POST'])
@login_required
def create_notice():
    # Only admins can create general notices
    if not getattr(g.user, 'is_admin', False):
        return jsonify({'error': 'Unauthorized'}), 403
        
    data = request.json
    if not data or 'title' not in data or 'message' not in data:
        return jsonify({'error': 'Title and message are required'}), 400
        
    new_notice = Notification(
        user_id=g.user.id,
        type=data.get('type', 'announcement'),
        title=data['title'],
        message=data['message'],
        target_role=data.get('target_role', 'all') # tenant, owner, agent, all
    )
    
    db.session.add(new_notice)
    db.session.commit()
    return jsonify({'id': new_notice.id, 'status': 'created'}), 201
