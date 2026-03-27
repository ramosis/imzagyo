from datetime import datetime
from flask import request, jsonify, g
from shared.database import get_db
from modules.auth.decorators import login_required, require_inner_circle
from . import crm_bp

PURPOSE_MAP = {
    'gosterim': 'Portföy Gösterimi', 'sozlesme': 'Sözleşme İmzası',
    'kapora': 'Kapora Görüşmesi', 'expertiz': 'Expertiz / Değerleme',
    'sanal_tur': 'Sanal Tur', 'diger': 'Diğer'
}

@crm_bp.route('/appointments', methods=['GET'])
@login_required
def get_appointments():
    user = g.user
    with get_db() as conn:
        if user['role'] == 'admin':
            query = 'SELECT a.*, p.baslik1, u.username FROM appointments a LEFT JOIN portfoyler p ON a.property_id = p.id LEFT JOIN users u ON a.user_id = u.id ORDER BY a.datetime DESC'
            records = conn.execute(query).fetchall()
        else:
            query = 'SELECT a.*, p.baslik1, u.username FROM appointments a LEFT JOIN portfoyler p ON a.property_id = p.id LEFT JOIN users u ON a.user_id = u.id WHERE a.assigned_user_id = ? OR a.user_id = ? ORDER BY a.datetime DESC'
            records = conn.execute(query, (user['id'], user['id'])).fetchall()
    result = []
    for r in records:
        d = dict(r)
        d['purpose_label'] = PURPOSE_MAP.get(d.get('purpose', ''), d.get('purpose', ''))
        result.append(d)
    return jsonify(result), 200

@crm_bp.route('/appointments', methods=['POST'])
@login_required
def add_appointment():
    data = request.json
    assigned_user_id = data.get('assigned_user_id', g.user['id'])
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO appointments (user_id, property_id, client_name, client_phone, datetime, purpose, notes, assigned_user_id, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (g.user['id'], data.get('property_id'), data.get('client_name'), data.get('client_phone'), 
              data.get('datetime'), data.get('purpose', 'gosterim'), data.get('notes', ''), assigned_user_id, 'pending'))
        conn.commit()
    return jsonify({'status': 'created'}), 201

@crm_bp.route('/shifts/<int:user_id>', methods=['GET'])
@require_inner_circle
def get_user_shifts(user_id):
    with get_db() as conn:
        shifts = conn.execute('SELECT * FROM user_shifts WHERE user_id = ? ORDER BY day_of_week', (user_id,)).fetchall()
    return jsonify([dict(s) for s in shifts])

@crm_bp.route('/shifts/<int:user_id>', methods=['POST'])
@require_inner_circle
def set_user_shifts(user_id):
    data = request.json
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute('DELETE FROM user_shifts WHERE user_id = ?', (user_id,))
        for shift in data:
            cur.execute('INSERT INTO user_shifts (user_id, day_of_week, start_time, end_time, is_off) VALUES (?,?,?,?,?)',
                        (user_id, shift.get('day_of_week'), shift.get('start_time', '09:00'), shift.get('end_time', '18:00'), shift.get('is_off', 0)))
        conn.commit()
    return jsonify({'status': 'shifts_saved'}), 200
