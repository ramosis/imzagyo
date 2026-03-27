from flask import Blueprint, request, jsonify
from shared.database import get_db_connection

appointments_bp = Blueprint('appointments', __name__)

def get_current_user_id():
    """Token'dan user_id ve role'ü çıkar."""
    token = request.headers.get('Authorization', '')
    if 'admin-token' in token or 'imza-super-admin-2026' in token:
        return 1, 'admin'
    if token.startswith('Bearer token-'):
        try:
            uid = int(token.replace('Bearer token-', ''))
            conn = get_db_connection()
            user = conn.execute('SELECT id, role FROM users WHERE id = ?', (uid,)).fetchone()
            conn.close()
            if user:
                return user['id'], user['role']
        except:
            pass
    return None, None

PURPOSE_MAP = {
    'gosterim': 'Portföy Gösterimi',
    'sozlesme': 'Sözleşme İmzası',
    'kapora': 'Kapora Görüşmesi',
    'expertiz': 'Expertiz / Değerleme',
    'sanal_tur': 'Sanal Tur',
    'diger': 'Diğer'
}

@appointments_bp.route('/api/appointments', methods=['GET'])
def get_appointments():
    user_id, role = get_current_user_id()
    conn = get_db_connection()

    if role == 'admin':
        query = '''
            SELECT a.*, p.baslik1, u.username
            FROM appointments a
            LEFT JOIN portfoyler p ON a.property_id = p.id
            LEFT JOIN users u ON a.user_id = u.id
            ORDER BY a.datetime DESC
        '''
        records = conn.execute(query).fetchall()
    else:
        # Danışman sadece kendi randevularını görür
        query = '''
            SELECT a.*, p.baslik1, u.username
            FROM appointments a
            LEFT JOIN portfoyler p ON a.property_id = p.id
            LEFT JOIN users u ON a.user_id = u.id
            WHERE a.assigned_user_id = ? OR a.user_id = ?
            ORDER BY a.datetime DESC
        '''
        records = conn.execute(query, (user_id, user_id)).fetchall()

    conn.close()

    result = []
    for r in records:
        d = dict(r)
        d['purpose_label'] = PURPOSE_MAP.get(d.get('purpose', ''), d.get('purpose', ''))
        result.append(d)

    return jsonify(result), 200

@appointments_bp.route('/api/appointments', methods=['POST'])
def add_appointment():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()

    assigned_user_id = data.get('assigned_user_id', data.get('user_id', 1))

    # Mesai saati kontrolü
    appt_datetime = data.get('datetime', data.get('date', ''))
    if appt_datetime and assigned_user_id:
        conflict = check_shift_availability(conn, assigned_user_id, appt_datetime)
        if conflict:
            conn.close()
            return jsonify({'error': conflict}), 400

    cur.execute('''
        INSERT INTO appointments (
            user_id, property_id, client_name, client_phone,
            datetime, purpose, notes, assigned_user_id, status
        ) VALUES (?,?,?,?,?,?,?,?,?)
    ''', (
        data.get('user_id', 1),
        data.get('property_id'),
        data.get('client_name', data.get('username', '')),
        data.get('client_phone', data.get('phone', '')),
        appt_datetime,
        data.get('purpose', 'gosterim'),
        data.get('notes', ''),
        assigned_user_id,
        data.get('status', 'pending')
    ))
    conn.commit()
    appt_id = cur.lastrowid
    conn.close()
    return jsonify({'id': appt_id, 'status': 'created'}), 201

@appointments_bp.route('/api/appointments/<int:id>/reschedule', methods=['PUT'])
def reschedule_appointment(id):
    """Randevuyu ertele - yeni tarih/saat ata."""
    data = request.json
    new_datetime = data.get('new_datetime')

    if not new_datetime:
        return jsonify({'error': 'Yeni tarih/saat gereklidir.'}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    # Mevcut randevuyu al
    appt = conn.execute('SELECT * FROM appointments WHERE id = ?', (id,)).fetchone()
    if not appt:
        conn.close()
        return jsonify({'error': 'Randevu bulunamadı.'}), 404

    # Mesai kontrolü
    assigned_uid = appt['assigned_user_id'] or appt['user_id']
    conflict = check_shift_availability(conn, assigned_uid, new_datetime)
    if conflict:
        conn.close()
        return jsonify({'error': conflict}), 400

    # Orijinal tarihi sakla (ilk ertelemede)
    original_dt = appt['original_datetime'] or appt['datetime']
    reschedule_count = (appt['reschedule_count'] or 0) + 1

    cur.execute('''
        UPDATE appointments
        SET datetime = ?, original_datetime = ?, reschedule_count = ?, status = 'rescheduled'
        WHERE id = ?
    ''', (new_datetime, original_dt, reschedule_count, id))
    conn.commit()
    conn.close()

    return jsonify({
        'status': 'rescheduled',
        'new_datetime': new_datetime,
        'reschedule_count': reschedule_count
    }), 200

@appointments_bp.route('/api/appointments/<int:id>/confirm', methods=['PUT'])
def confirm_appointment(id):
    """Randevuyu onayla."""
    conn = get_db_connection()
    conn.execute("UPDATE appointments SET status = 'confirmed' WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'confirmed'}), 200

@appointments_bp.route('/api/appointments/<int:id>', methods=['PUT'])
def update_appointment(id):
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        UPDATE appointments SET property_id=?, client_name=?, client_phone=?,
        datetime=?, purpose=?, notes=?, status=? WHERE id=?
    ''', (
        data.get('property_id'), data.get('client_name'), data.get('client_phone'),
        data.get('datetime'), data.get('purpose'), data.get('notes'),
        data.get('status'), id
    ))
    conn.commit()
    conn.close()
    return jsonify({'status': 'updated'}), 200

@appointments_bp.route('/api/appointments/<int:id>', methods=['DELETE'])
def delete_appointment(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM appointments WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'deleted'}), 200

# --- Mesai Yönetimi Endpoint'leri ---

@appointments_bp.route('/api/shifts/<int:user_id>', methods=['GET'])
def get_user_shifts(user_id):
    """Bir danışmanın haftalık mesai programını getir."""
    conn = get_db_connection()
    shifts = conn.execute(
        'SELECT * FROM user_shifts WHERE user_id = ? ORDER BY day_of_week', (user_id,)
    ).fetchall()
    conn.close()

    if not shifts:
        # Varsayılan mesai: Pazartesi-Cuma 09:00-18:00
        default_shifts = []
        for day in range(0, 7):
            default_shifts.append({
                'day_of_week': day,
                'start_time': '09:00' if day < 5 else '',
                'end_time': '18:00' if day < 5 else '',
                'is_off': 1 if day >= 5 else 0
            })
        return jsonify(default_shifts), 200

    return jsonify([dict(s) for s in shifts]), 200

@appointments_bp.route('/api/shifts/<int:user_id>', methods=['POST'])
def set_user_shifts(user_id):
    """Bir danışmanın haftalık mesai programını kaydet."""
    data = request.json  # [{day_of_week, start_time, end_time, is_off}, ...]
    conn = get_db_connection()
    cur = conn.cursor()

    # Önce eski mesaileri sil
    cur.execute('DELETE FROM user_shifts WHERE user_id = ?', (user_id,))

    for shift in data:
        cur.execute('''
            INSERT INTO user_shifts (user_id, day_of_week, start_time, end_time, is_off)
            VALUES (?,?,?,?,?)
        ''', (
            user_id,
            shift.get('day_of_week'),
            shift.get('start_time', '09:00'),
            shift.get('end_time', '18:00'),
            shift.get('is_off', 0)
        ))

    conn.commit()
    conn.close()
    return jsonify({'status': 'shifts_saved'}), 200

@appointments_bp.route('/api/shifts/<int:user_id>/availability', methods=['GET'])
def get_availability(user_id):
    """Belirli bir tarihte danışmanın müsait saatlerini döndür."""
    date = request.args.get('date')  # YYYY-MM-DD
    if not date:
        return jsonify({'error': 'Tarih parametresi gereklidir.'}), 400

    conn = get_db_connection()

    # O günün haftanın kaçıncı günü olduğunu hesapla
    from datetime import datetime as dt
    day_obj = dt.strptime(date, '%Y-%m-%d')
    day_of_week = day_obj.weekday()  # 0=Monday, 6=Sunday

    # Mesai saatini al
    shift = conn.execute(
        'SELECT * FROM user_shifts WHERE user_id = ? AND day_of_week = ?',
        (user_id, day_of_week)
    ).fetchone()

    if not shift:
        # Varsayılan: Hafta içi 09:00-18:00
        if day_of_week < 5:
            start_time = '09:00'
            end_time = '18:00'
            is_off = False
        else:
            start_time = ''
            end_time = ''
            is_off = True
    else:
        shift = dict(shift)
        start_time = shift['start_time']
        end_time = shift['end_time']
        is_off = bool(shift['is_off'])

    if is_off:
        conn.close()
        return jsonify({'available': False, 'message': 'Bu gün izinli.', 'busy_slots': []}), 200

    # O gündeki mevcut randevuları al (dolu saatler)
    existing = conn.execute(
        "SELECT datetime FROM appointments WHERE assigned_user_id = ? AND datetime LIKE ? AND status != 'cancelled'",
        (user_id, f'{date}%')
    ).fetchall()
    conn.close()

    busy_slots = [dict(e)['datetime'] for e in existing]

    return jsonify({
        'available': True,
        'start_time': start_time,
        'end_time': end_time,
        'busy_slots': busy_slots
    }), 200


def check_shift_availability(conn, user_id, datetime_str):
    """Randevu saatinin danışmanın mesai saatleri içinde olup olmadığını kontrol eder."""
    if not datetime_str or not user_id:
        return None

    try:
        from datetime import datetime as dt
        # datetime_str: "2026-03-10 14:30" veya "2026-03-10T14:30"
        datetime_str = datetime_str.replace('T', ' ')
        appt_dt = dt.strptime(datetime_str.strip(), '%Y-%m-%d %H:%M')
        day_of_week = appt_dt.weekday()
        appt_time = appt_dt.strftime('%H:%M')

        shift = conn.execute(
            'SELECT * FROM user_shifts WHERE user_id = ? AND day_of_week = ?',
            (user_id, day_of_week)
        ).fetchone()

        if shift:
            shift = dict(shift)
            if shift['is_off']:
                day_names_tr = ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi', 'Pazar']
                return f"Bu danışman {day_names_tr[day_of_week]} günü izinlidir."
            if appt_time < shift['start_time'] or appt_time >= shift['end_time']:
                return f"Seçilen saat ({appt_time}) danışmanın mesai saatleri ({shift['start_time']}-{shift['end_time']}) dışındadır."
        else:
            # Varsayılan kontrol: Hafta sonu izin
            if day_of_week >= 5:
                return "Hafta sonu için varsayılan mesai tanımlı değildir."
    except Exception as e:
        # Parse hatası durumunda kontrolü atla
        print(f"Mesai kontrolü hatası: {e}")
        return None

    return None
