from flask import Blueprint, request, jsonify
from database import get_db_connection
import json
from .schemas import lead_schema, ValidationError

leads_bp = Blueprint('leads', __name__)


@leads_bp.route('/api/leads', methods=['GET'])
def get_leads():
    from .auth import get_current_user
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
    
    # --- VERİ DOĞRULAMA (Faz 1) ---
    try:
        validated_data = lead_schema.load(data)
    except ValidationError as err:
        return jsonify({"error": "Geçersiz veri", "details": err.messages}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    # --- AKILLI PUANLAMA (LMetrics Entegrasyonu) ---
    from .lmetrics import calculate_intent_score
    
    session_id = data.get('session_id')
    behavior_score = 0
    if session_id:
        behavior_score, _ = calculate_intent_score(session_id)

    ai_score = 10  # Temel skor
    if data.get('phone'):
        ai_score += 20
    if data.get('email'):
        ai_score += 15
    if data.get('interest_property_id'):
        ai_score += 25
    if data.get('source') == 'referans':
        ai_score += 10
    
    # Davranış puanını ekle (Ağırlıklı)
    ai_score = min(100, ai_score + behavior_score)

    try:
        cur.execute('''
            INSERT INTO leads (name, phone, email, source, interest_property_id, campaign_id, assigned_user_id, status, ai_score, notes, tags)
            VALUES (?,?,?,?,?,?,?,?,?,?,?)
        ''', (
            validated_data.get('name'),
            validated_data.get('phone'),
            validated_data.get('email'),
            validated_data.get('source', 'portal'),
            validated_data.get('interest_property_id'),
            validated_data.get('campaign_id'),
            validated_data.get('assigned_user_id'),
            validated_data.get('status', 'new'),
            ai_score,
            validated_data.get('notes'),
            validated_data.get('tags')
        ))
        lead_id = cur.lastrowid

        # --- Akıllı Bildirim: Danışmana Bilgi Ver ---
        assigned_user_id = validated_data.get('assigned_user_id')
        if assigned_user_id:
            from .notifications import create_notification
            try:
                msg_title = '🔥 SICAK FIRSAT!' if ai_score >= 70 else 'Yeni Aday Atandı'
                create_notification(
                    assigned_user_id,
                    'ai_alert' if ai_score >= 70 else 'system',
                    msg_title,
                    f"{validated_data.get('name')} adlı aday %{ai_score} ilgi puanı ile size atandı."
                )
            except: pass

        # --- DİJİTAL AYAK İZİ EŞLEŞTİRME ---
        # Kullanıcının anonim iken yaptığı işlemleri (session_id) bu yeni lead'e bağla
        session_id = validated_data.get('session_id')
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
        data_json = item.get('data_json')
        if data_json:
            try:
                item['data'] = json.loads(str(data_json))
            except:
                item['data'] = {}
        result.append(item)
        
    return jsonify(result)

@leads_bp.route('/api/leads/<int:id>/footprint', methods=['GET'])
def get_lead_footprint(id):
    """
    Adayın tüm dijital yolculuğunu (CRM + L-Metrics + Pipeline Geçmişi) kronolojik döner. (Unified Timeline)
    """
    conn = get_db_connection()
    try:
        # 1. Lead bilgilerini doğrula
        lead = conn.execute('SELECT name, ai_score, created_at, notes FROM leads WHERE id = ?', (id,)).fetchone()
        if not lead:
            return jsonify({'error': 'Lead not found'}), 404

        timeline = []

        # 1.1 Lead Oluşturulması ve Notlar
        timeline.append({
            'type': 'system',
            'timestamp': lead['created_at'],
            'title': 'Aday Sisteme Eklendi',
            'description': lead['notes'] if lead['notes'] else 'Sisteme yeni aday kaydı oluşturuldu.'
        })

        # 2. Pipeline Geçmişi
        ph_rows = conn.execute('''
            SELECT ph.created_at, ps.name as stage_name, u.username as user_name, ph.reason
            FROM pipeline_history ph
            JOIN pipeline_stages ps ON ph.new_stage_id = ps.id
            LEFT JOIN users u ON ph.user_id = u.id
            WHERE ph.lead_id = ?
        ''', (id,)).fetchall()
        
        for row in ph_rows:
            timeline.append({
                'type': 'pipeline',
                'timestamp': row['created_at'],
                'title': f"Aşama: {row['stage_name']}",
                'description': f"{row['user_name'] or 'Sistem'} tarafından taşındı. {row['reason'] or ''}"
            })

        # 3. Lead Etkileşimleri (Hesaplama araçları vs)
        interactions = conn.execute('''
            SELECT * FROM lead_interactions 
            WHERE lead_id = ?
        ''', (id,)).fetchall()
        
        session_ids = set()
        for row in interactions:
            item = dict(row)
            if item.get('session_id'):
                session_ids.add(item['session_id'])
            
            data_json = item.get('data_json')
            data_info = ""
            if data_json:
                try: 
                    jd = json.loads(str(data_json))
                    data_info = " | ".join([f"{k}: {v}" for k, v in jd.items()][:3])
                except: pass
            
            timeline.append({
                'type': 'tool',
                'timestamp': item['created_at'],
                'title': f"Araç: {item['tool_name']}",
                'description': data_info or 'Etkileşim algılandı.'
            })
            
        # 4. Sayfa Görüntülemeleri (user_interactions)
        for sid in session_ids:
            ui_rows = conn.execute('''
                SELECT timestamp as created_at, url, event_type, value
                FROM user_interactions
                WHERE session_id = ? AND event_type IN ('stay', 'click')
            ''', (sid,)).fetchall()
            for row in ui_rows:
                label = "Sayfa İncelemesi" if row['event_type'] == 'stay' else "Tıklama Etkileşimi"
                desc = row['url']
                val = row['value']
                if val:
                    desc += f" ({val} sn)" if row['event_type'] == 'stay' else f" ({val})"
                    
                timeline.append({
                    'type': 'lmetrics',
                    'timestamp': row['created_at'],
                    'title': label,
                    'description': desc
                })

        # Kronolojik sıralama (Yeniden Eskiye)
        timeline.sort(key=lambda x: x['timestamp'], reverse=True)

        return jsonify({
            'lead_name': lead['name'],
            'ai_score': lead['ai_score'],
            'timeline': timeline
        }), 200
    finally:
        conn.close()
