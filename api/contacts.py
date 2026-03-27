from flask import Blueprint, request, jsonify
from shared.database import get_db_connection
from datetime import datetime

contacts_bp = Blueprint('contacts', __name__)

# Tüm kişileri getir
@contacts_bp.route('/api/contacts', methods=['GET'])
def get_contacts():
    category = request.args.get('category')
    conn = get_db_connection()

    query = 'SELECT id, name, phone, email, category, tags, occupation FROM contacts'
    params = []

    if category:
        query += ' WHERE category = ?'
        params.append(category)

    query += ' ORDER BY name ASC'

    contacts = conn.execute(query, params).fetchall()
    conn.close()
    return jsonify([dict(row) for row in contacts])

# Yeni kişi ekle
@contacts_bp.route('/api/contacts', methods=['POST'])
def add_contact():
    data = request.json
    conn = get_db_connection()

    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO contacts (
                name, phone, email, address, occupation,
                availability_time, family_size, age,
                political_view, religious_view, notes, birthdate,
                category, tags, source_table, source_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('name'),
            data.get('phone'),
            data.get('email'),
            data.get('address'),
            data.get('occupation'),
            data.get('availability_time'),
            data.get('family_size'),
            data.get('age'),
            data.get('political_view'),
            data.get('religious_view'),
            data.get('notes'),
            data.get('birthdate'),
            data.get('category', 'general'),
            data.get('tags'),
            data.get('source_table'),
            data.get('source_id')
        ))
        conn.commit()
        new_id = cursor.lastrowid
        return jsonify({"id": new_id, "message": "Kişi rehbere eklendi"}), 201
    except conn.IntegrityError:
        return jsonify({"error": "Bu kaynak zaten rehbere eklenmiş."}), 409
    finally:
        conn.close()

# Kişi sil
@contacts_bp.route('/api/contacts/<int:id>', methods=['DELETE'])
def delete_contact(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM contacts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Kişi silindi"}), 200

# Kişi detayını getir
@contacts_bp.route('/api/contacts/<int:id>', methods=['GET'])
def get_contact(id):
    conn = get_db_connection()
    contact = conn.execute('SELECT * FROM contacts WHERE id = ?', (id,)).fetchone()
    conn.close()
    
    if contact:
        return jsonify(dict(contact))
    else:
        return jsonify({"error": "Kişi bulunamadı"}), 404

# Yaklaşan doğum günlerini getir (Önümüzdeki 30 gün)
@contacts_bp.route('/api/contacts/birthdays', methods=['GET'])
def get_upcoming_birthdays():
    conn = get_db_connection()
    # Doğum tarihi girilmiş kişileri çek
    contacts = conn.execute('SELECT id, name, phone, birthdate, occupation FROM contacts WHERE birthdate IS NOT NULL AND birthdate != ""').fetchall()
    conn.close()
    
    upcoming = []
    today = datetime.now().date()
    
    for c in contacts:
        try:
            # Tarih formatı YYYY-MM-DD varsayılıyor
            bdate = datetime.strptime(c['birthdate'], '%Y-%m-%d').date()
            
            # Bu yılki doğum gününü hesapla
            this_year_bdate = bdate.replace(year=today.year)
            
            # Eğer bu yılki geçtiyse, sonraki yıla bak
            if this_year_bdate < today:
                next_bdate = bdate.replace(year=today.year + 1)
            else:
                next_bdate = this_year_bdate
            
            days_left = (next_bdate - today).days
            
            # 30 gün içinde olanları listeye ekle
            if 0 <= days_left <= 30:
                contact_dict = dict(c)
                contact_dict['days_left'] = days_left
                contact_dict['turning_age'] = next_bdate.year - bdate.year
                contact_dict['next_bdate_str'] = next_bdate.strftime('%d.%m.%Y')
                upcoming.append(contact_dict)
        except ValueError:
            continue # Hatalı tarih formatı varsa atla
            
    # En yakın tarihe göre sırala
    upcoming.sort(key=lambda x: x['days_left'])
    
    return jsonify(upcoming)