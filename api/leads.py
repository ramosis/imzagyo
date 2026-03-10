from flask import Blueprint, request, jsonify
from database import get_db_connection
import json

leads_bp = Blueprint('leads', __name__)


@leads_bp.route('/api/leads', methods=['GET'])
def get_leads():
    from api.auth import get_current_user
    user = get_current_user()
    if not user:
        return jsonify([]), 401
        
    conn = get_db_connection()
    
    if user.get('circle') == 'outer':
        # Outer circle: Sadece kendi mülküne ait lead'leri görsün
        query = '''
            SELECT l.*, p.baslik1 as property_title, u.username as assigned_to
            FROM leads l
            JOIN portfoyler p ON l.interest_property_id = p.id
            LEFT JOIN users u ON l.assigned_user_id = u.id
            WHERE p.owner_id = ?
            ORDER BY l.ai_score DESC, l.created_at DESC
        '''
        leads = conn.execute(query, (user['id'],)).fetchall()
    else:
        # Inner circle
        if user['role'] in ['admin', 'super_admin']:
            query = '''
                SELECT l.*, p.baslik1 as property_title, u.username as assigned_to
                FROM leads l
                LEFT JOIN portfoyler p ON l.interest_property_id = p.id
                LEFT JOIN users u ON l.assigned_user_id = u.id
                ORDER BY l.ai_score DESC, l.created_at DESC
            '''
            leads = conn.execute(query).fetchall()
        else:
            query = '''
                SELECT l.*, p.baslik1 as property_title, u.username as assigned_to
                FROM leads l
                LEFT JOIN portfoyler p ON l.interest_property_id = p.id
                LEFT JOIN users u ON l.assigned_user_id = u.id
                WHERE l.assigned_user_id = ?
                ORDER BY l.ai_score DESC, l.created_at DESC
            '''
            leads = conn.execute(query, (user['id'],)).fetchall()

    conn.close()
    return jsonify([dict(l) for l in leads]), 200

@leads_bp.route('/api/leads/<int:id>', methods=['GET'])
def get_lead(id):
    conn = get_db_connection()
    # Join ile detaylı bilgi çekelim
    query = '''
        SELECT l.*, p.baslik1 as property_title, u.username as assigned_to
        FROM leads l
        LEFT JOIN portfoyler p ON l.interest_property_id = p.id
        LEFT JOIN users u ON l.assigned_user_id = u.id
        WHERE l.id = ?
    '''
    lead = conn.execute(query, (id,)).fetchone()
    conn.close()
    
    if lead:
        return jsonify(dict(lead))
    else:
        return jsonify({'error': 'Lead not found'}), 404

@leads_bp.route('/api/leads', methods=['POST'])
def add_lead():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()

    # Basit bir AI skoru hesaplama (demo amaçlı)
    ai_score = 30  # Temel skor
    if data.get('phone'):
        ai_score += 20
    if data.get('email'):
        ai_score += 15
    if data.get('interest_property_id'):
        ai_score += 25
    if data.get('source') == 'referans':
        ai_score += 10

    try:
        cur.execute('''
            INSERT INTO leads (name, phone, email, source, interest_property_id, assigned_user_id, status, ai_score, notes, tags)
            VALUES (?,?,?,?,?,?,?,?,?,?)
        ''', (
            data.get('name'),
            data.get('phone'),
            data.get('email'),
            data.get('source', 'portal'),
            data.get('interest_property_id'),
            data.get('assigned_user_id'),
            data.get('status', 'new'),
            ai_score,
            data.get('notes'),
            data.get('tags')
        ))
        lead_id = cur.lastrowid

        # --- DİJİTAL AYAK İZİ EŞLEŞTİRME ---
        # Kullanıcının anonim iken yaptığı işlemleri (session_id) bu yeni lead'e bağla
        session_id = data.get('session_id')
        if session_id:
            cur.execute('UPDATE lead_interactions SET lead_id = ? WHERE session_id = ?', (lead_id, session_id))

        # --- REHBERE (CONTACTS) SENKRONİZE ET ---
        try:
            notes_for_contact = f"Potansiyel müşteri formundan geldi. Kaynak: {data.get('source', 'portal')}. Not: {data.get('notes', '')}"
            cur.execute('''
                INSERT INTO contacts (name, phone, email, category, source_table, source_id, tags, notes)
                VALUES (?, ?, ?, 'lead', 'leads', ?, ?, ?)
            ''', (
                data.get('name'), data.get('phone'), data.get('email'),
                lead_id, data.get('tags'), notes_for_contact.strip()
            ))
        except cur.IntegrityError:
            # Zaten varsa, belki notları güncelleyebiliriz ama şimdilik geçiyoruz.
            pass

        conn.commit()
        return jsonify({'id': lead_id, 'ai_score': ai_score}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@leads_bp.route('/api/leads/<int:id>', methods=['PUT'])
def update_lead(id):
    data = request.json
    conn = get_db_connection()
    
    # Dinamik güncelleme sorgusu oluştur
    fields = []
    values = []
    allowed_cols = ['name', 'phone', 'email', 'source', 'interest_property_id', 'assigned_user_id', 'status', 'notes', 'tags', 'ai_score']
    
    for col in allowed_cols:
        if col in data:
            fields.append(f"{col}=?")
            values.append(data[col])
            
    if fields:
        values.append(id)
        conn.execute(f'UPDATE leads SET {", ".join(fields)} WHERE id=?', tuple(values))
        
    conn.commit()
    conn.close()
    return jsonify({'status': 'updated'}), 200

@leads_bp.route('/api/leads/<int:id>', methods=['DELETE'])
def delete_lead(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM leads WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'deleted'}), 200

@leads_bp.route('/api/leads/<int:id>/interactions', methods=['GET'])
def get_lead_interactions(id):
    conn = get_db_connection()
    interactions = conn.execute('''
        SELECT * FROM lead_interactions 
        WHERE lead_id = ? 
        ORDER BY created_at DESC
    ''', (id,)).fetchall()
    conn.close()
    
    result = []
    for row in interactions:
        item = dict(row)
        if item.get('data_json'):
            try:
                item['data'] = json.loads(item['data_json'])
            except:
                item['data'] = {}
        result.append(item)
        
    return jsonify(result)
