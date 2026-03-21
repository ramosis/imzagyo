from flask import Blueprint, jsonify, request, g
from database import get_db_connection
from api.auth import require_inner_circle, login_required
import json

hr_bp = Blueprint('hr', __name__)

# --- PERSONEL MESAİ YÖNETİMİ ---

@hr_bp.route('/api/hr/shifts', methods=['GET'])
@require_inner_circle
def get_shifts():
    """Tüm personelin veya belirli bir personelin mesai programını getirir."""
    user_id = request.args.get('user_id')
    conn = get_db_connection()
    
    if user_id:
        shifts = conn.execute('SELECT * FROM user_shifts WHERE user_id = ?', (user_id,)).fetchall()
    else:
        shifts = conn.execute('''
            SELECT s.*, u.username 
            FROM user_shifts s
            JOIN users u ON s.user_id = u.id
        ''').fetchall()
    
    conn.close()
    return jsonify([dict(row) for row in shifts])

@hr_bp.route('/api/hr/shifts', methods=['POST'])
@require_inner_circle
def add_shift():
    """Yeni bir mesai kaydı ekler veya günceller."""
    data = request.json
    user_id = data.get('user_id')
    day_of_week = data.get('day_of_week') # 0-6 (Pazartesi-Pazar)
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    is_off = data.get('is_off', 0)

    if not all([user_id, day_of_week is not None, start_time, end_time]):
        return jsonify({'error': 'Eksik veri'}), 400

    conn = get_db_connection()
    conn.execute('''
        INSERT OR REPLACE INTO user_shifts (user_id, day_of_week, start_time, end_time, is_off)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, day_of_week, start_time, end_time, is_off))
    conn.commit()
    conn.close()
    
    return jsonify({'status': 'success', 'message': 'Mesai kaydı güncellendi'}), 201

# --- PERSONEL HAKEDİŞ VE KOMİSYON TAKİBİ ---

@hr_bp.route('/api/hr/commissions', methods=['GET'])
@require_inner_circle
def get_commissions():
    """Personel hakedişlerini listeler."""
    user_id = request.args.get('user_id')
    status = request.args.get('status') # 'pending', 'paid'
    
    conn = get_db_connection()
    query = '''
        SELECT c.*, u.username, ct.property_id
        FROM commissions c
        JOIN users u ON c.user_id = u.id
        LEFT JOIN contracts ct ON c.contract_id = ct.id
        WHERE 1=1
    '''
    params = []
    
    if user_id:
        query += ' AND c.user_id = ?'
        params.append(user_id)
    if status:
        query += ' AND c.status = ?'
        params.append(status)
        
    commissions = conn.execute(query, params).fetchall()
    conn.close()
    
    return jsonify([dict(row) for row in commissions])

@hr_bp.route('/api/hr/performance', methods=['GET'])
@require_inner_circle
def get_performance():
    """Personel performans özetini getirir."""
    conn = get_db_connection()
    
    # Basit bir performans metriği: Tamamlanan randevular ve aktif ilanlar
    performance = conn.execute('''
        SELECT 
            u.id, u.username, u.role,
            (SELECT COUNT(*) FROM appointments WHERE assigned_user_id = u.id AND status = 'completed') as completed_appointments,
            (SELECT COUNT(*) FROM portfoyler WHERE danisman_isim LIKE '%' || u.username || '%') as active_listings
        FROM users u
        WHERE u.role IN ('admin', 'broker', 'danisman')
    ''').fetchall()
    
    conn.close()
    return jsonify([dict(row) for row in performance])
