""" 
Parties API Module
Provides endpoints for managing contract parties (clients, sellers, etc.).
"""
from flask import Blueprint, jsonify, request
from database import get_db_connection

parties_bp = Blueprint('parties', __name__, url_prefix='/api/parties')

# Basit yetkilendirme kontrolü
def check_auth():
    token = request.headers.get('Authorization')
    # Basit token kontrolü (portfolio.py ile uyumlu)
    if not token or (not token.startswith('Bearer token-') and token != 'Bearer admin-token'):
        return False
    return True

# Tüm tarafları listele
@parties_bp.route('', methods=['GET'])
def get_parties():
    if not check_auth(): return jsonify({'error': 'Unauthorized'}), 403
    conn = get_db_connection()
    parties = conn.execute('SELECT * FROM parties').fetchall()
    conn.close()
    
    result = [dict(p) for p in parties]
    return jsonify(result)

# TC Kimlik No veya Vergi Numarası ile taraf ara
@parties_bp.route('/search', methods=['GET'])
def search_party():
    if not check_auth(): return jsonify({'error': 'Unauthorized'}), 403
    identity_number = request.args.get('identity')
    
    if not identity_number:
        return jsonify({"error": "TC Kimlik No veya Vergi Numarası gereklidir"}), 400
    
    conn = get_db_connection()
    # Önce bireysel (tc_no) kontrol et
    party = conn.execute('SELECT * FROM parties WHERE tc_no = ?', (identity_number,)).fetchone()
    
    # Bulamazsan kurumsal (vkn) olarak kontrol et
    if party is None:
        party = conn.execute('SELECT * FROM parties WHERE vkn = ?', (identity_number,)).fetchone()
    
    conn.close()
    
    if party is None:
        return jsonify({"message": "Taraf bulunamadı"}), 404
    
    return jsonify(dict(party))

# Yeni taraf ekle
@parties_bp.route('', methods=['POST'])
def add_party():
    if not check_auth(): return jsonify({'error': 'Unauthorized'}), 403
    data = request.get_json()
    
    # Gerekli alanlar kontrolü
    if not data.get('name') or (not data.get('tc_no') and not data.get('vkn')):
        return jsonify({"error": "İsim ve TC Kimlik No veya Vergi Numarası gereklidir"}), 400
    
    conn = get_db_connection()

    try:
        cursor = conn.cursor()
        # Aynı TC veya VKN ile kayıt var mı kontrol et
        if data.get('tc_no'):
            existing = cursor.execute('SELECT id FROM parties WHERE tc_no = ?', (data.get('tc_no'),)).fetchone()
            if existing:
                return jsonify({"error": "Bu TC Kimlik Numarası zaten kayıtlı"}), 409
        elif data.get('vkn'):
            existing = cursor.execute('SELECT id FROM parties WHERE vkn = ?', (data.get('vkn'),)).fetchone()
            if existing:
                return jsonify({"error": "Bu Vergi Numarası zaten kayıtlı"}), 409
        
        # Yeni tarafı ekle
        cursor.execute('''
            INSERT INTO parties (tc_no, vkn, party_type, name, phone, email, address)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('tc_no'),
            data.get('vkn'),
            data.get('party_type', 'individual'),  # Varsayılan olarak bireysel
            data.get('name'),
            data.get('phone'),
            data.get('email'),
            data.get('address')
        ))
        party_id = cursor.lastrowid

        # --- REHBERE (CONTACTS) SENKRONİZE ET ---
        try:
            notes_for_contact = f"Sözleşme tarafı olarak eklendi. Tip: {data.get('party_type', 'individual')}"
            cursor.execute('''
                INSERT INTO contacts (name, phone, email, address, category, source_table, source_id, notes)
                VALUES (?, ?, ?, ?, 'client', 'parties', ?, ?)
            ''', (
                data.get('name'), data.get('phone'), data.get('email'), data.get('address'),
                party_id, notes_for_contact
            ))
        except cursor.IntegrityError:
            pass # Zaten varsa geç

        conn.commit()
        
        # Eklenen tarafı geri döndür
        new_party = conn.execute('SELECT * FROM parties WHERE id = ?', (party_id,)).fetchone()
        return jsonify(dict(new_party)), 201
        
    except Exception as e:
        conn.rollback()
        return jsonify({"error": "Taraf eklenirken bir hata oluştu: " + str(e)}), 500
    finally:
        conn.close()

# Belirli bir tarafı getir
@parties_bp.route('/<int:id>', methods=['GET'])
def get_party(id):
    if not check_auth(): return jsonify({'error': 'Unauthorized'}), 403
    conn = get_db_connection()
    party = conn.execute('SELECT * FROM parties WHERE id = ?', (id,)).fetchone()
    conn.close()
    
    if party is None:
        return jsonify({"error": "Taraf bulunamadı"}), 404
        
    return jsonify(dict(party))

# Tarafı güncelle
@parties_bp.route('/<int:id>', methods=['PUT'])
def update_party(id):
    if not check_auth(): return jsonify({'error': 'Unauthorized'}), 403
    data = request.get_json()
    
    conn = get_db_connection()
    # Tarafın varlığını kontrol et
    existing = conn.execute('SELECT id FROM parties WHERE id = ?', (id,)).fetchone()
    if not existing:
        conn.close()
        return jsonify({"error": "Taraf bulunamadı"}), 404
    
    try:
        # Güncelleme işlemi
        conn.execute('''
            UPDATE parties SET
                tc_no = ?,
                vkn = ?,
                party_type = ?,
                name = ?,
                phone = ?,
                email = ?,
                address = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (
            data.get('tc_no'),
            data.get('vkn'),
            data.get('party_type'),
            data.get('name'),
            data.get('phone'),
            data.get('email'),
            data.get('address'),
            id
        ))
        
        conn.commit()
        # Güncellenmiş tarafı geri döndür
        updated_party = conn.execute('SELECT * FROM parties WHERE id = ?', (id,)).fetchone()
        conn.close()
        
        return jsonify(dict(updated_party))
        
    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({"error": "Taraf güncellenirken bir hata oluştu: " + str(e)}), 500

# Tarafı sil
@parties_bp.route('/<int:id>', methods=['DELETE'])
def delete_party(id):
    if not check_auth(): return jsonify({'error': 'Unauthorized'}), 403
    conn = get_db_connection()
    # Tarafın varlığını kontrol et
    existing = conn.execute('SELECT id FROM parties WHERE id = ?', (id,)).fetchone()
    if not existing:
        conn.close()
        return jsonify({"error": "Taraf bulunamadı"}), 404
    
    try:
        conn.execute('DELETE FROM parties WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        return jsonify({"message": "Taraf başarıyla silindi"})
        
    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({"error": "Taraf silinirken bir hata oluştu: " + str(e)}), 500