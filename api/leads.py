from typing import Optional, List, Dict, Any
from flask import Blueprint, request, jsonify, g
from shared.database import get_db
import json
from .schemas import lead_schema, ValidationError
from .auth import get_current_user, require_permission
from shared.utils import api_error, invalidate_entity_cache
from shared.extensions import socketio
import sqlite3

leads_bp = Blueprint('leads', __name__)

class LeadRepository:
    """Handles low-level SQL operations for Leads (Section 5.3)."""
    
    @staticmethod
    def get_leads_for_user(user_id: int, role: str, circle: str) -> List[Dict[str, Any]]:
        with get_db() as conn:
            if circle == 'outer':
                query = '''
                    SELECT l.*, p.baslik1 as property_title, u.username as assigned_to
                    FROM leads l
                    LEFT JOIN portfoyler p ON l.interest_property_id = p.id
                    LEFT JOIN users u ON l.assigned_user_id = u.id
                    WHERE p.owner_id = ?
                    ORDER BY l.ai_score DESC, l.created_at DESC
                '''
                rows = conn.execute(query, (user_id,)).fetchall()
            elif role in ['admin', 'super_admin']:
                query = '''
                    SELECT l.*, p.baslik1 as property_title, u.username as assigned_to
                    FROM leads l
                    LEFT JOIN portfoyler p ON l.interest_property_id = p.id
                    LEFT JOIN users u ON l.assigned_user_id = u.id
                    ORDER BY l.ai_score DESC, l.created_at DESC
                '''
                rows = conn.execute(query).fetchall()
            else:
                query = '''
                    SELECT l.*, p.baslik1 as property_title, u.username as assigned_to
                    FROM leads l
                    LEFT JOIN portfoyler p ON l.interest_property_id = p.id
                    LEFT JOIN users u ON l.assigned_user_id = u.id
                    WHERE l.assigned_user_id = ?
                    ORDER BY l.ai_score DESC, l.created_at DESC
                '''
                rows = conn.execute(query, (user_id,)).fetchall()
            return [dict(r) for r in rows]

    @staticmethod
    def get_by_id(lead_id: int) -> Optional[Dict[str, Any]]:
        with get_db() as conn:
            query = '''
                SELECT l.*, p.baslik1 as property_title, u.username as assigned_to
                FROM leads l
                LEFT JOIN portfoyler p ON l.interest_property_id = p.id
                LEFT JOIN users u ON l.assigned_user_id = u.id
                WHERE l.id = ?
            '''
            row = conn.execute(query, (lead_id,)).fetchone()
            return dict(row) if row else None

    @staticmethod
    def create(data: Dict[str, Any]) -> int:
        with get_db() as conn:
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['?' for _ in data])
            query = f"INSERT INTO leads ({columns}) VALUES ({placeholders})"
            cursor = conn.execute(query, list(data.values()))
            conn.commit()
            invalidate_entity_cache('lead')
            return cursor.lastrowid

    @staticmethod
    def update(lead_id: int, data: Dict[str, Any]) -> bool:
        with get_db() as conn:
            fields = [f"{k}=?" for k in data.keys()]
            if not fields: return False
            values = list(data.values()) + [lead_id]
            try:
                cursor = conn.execute(f'UPDATE leads SET {", ".join(fields)} WHERE id=?', values)
                conn.commit()
                invalidate_entity_cache('lead')
                return cursor.rowcount > 0
            except sqlite3.Error as e:
                # The get_db context manager will automatically rollback on exception.
                # We log the error here for debugging purposes.
                print(f"DATABASE ERROR in LeadRepository.update: {e}")
                # Re-raise or return False, depending on desired error handling.
                # For now, we let the exception propagate to be handled by the service layer.
                raise

    @staticmethod
    def delete(lead_id: int) -> bool:
        with get_db() as conn:
            cursor = conn.execute('DELETE FROM leads WHERE id=?', (lead_id,))
            conn.commit()
            return cursor.rowcount > 0

class LeadService:
    """Handles business logic, AI scoring, and notifications for Leads (Section 5.3)."""

    @staticmethod
    def calculate_and_create(data: Dict[str, Any]) -> Dict[str, Any]:
        # 1. Sanitization & Validation (Audit Section 6.2)
        sanitized_data = sanitize_input(data)
        validated_data = lead_schema.load(sanitized_data)
        
        # 2. AI Intent Scoring
        from .lmetrics import calculate_intent_score
        session_id = data.get('session_id')
        behavior_score = 0
        if session_id:
            behavior_score, _ = calculate_intent_score(session_id)

        ai_score = 10
        if validated_data.get('phone'): ai_score += 20
        if validated_data.get('email'): ai_score += 15
        if validated_data.get('interest_property_id'): ai_score += 25
        if validated_data.get('source') == 'referans': ai_score += 10
        ai_score = min(100, ai_score + behavior_score)
        
        validated_data['ai_score'] = ai_score

        # 3. Persistence
        lead_id = LeadRepository.create(validated_data)
        
        # 4. Notifications & Side Effects
        assigned_user_id = validated_data.get('assigned_user_id')
        if assigned_user_id:
            from .notifications import create_notification
            msg_title = '🔥 SICAK FIRSAT!' if ai_score >= 70 else 'Yeni Aday Atandı'
            create_notification(assigned_user_id, 'system', msg_title, f"{validated_data.get('name')} aday (%{ai_score}) size atandı.")
        
        # 5. Real-Time Notification (Phase 4)
        try:
            socketio.emit('new_lead', {
                'id': lead_id,
                'name': validated_data.get('name'),
                'ai_score': validated_data.get('ai_score'),
                'source': validated_data.get('source')
            }, namespace='/')
        except Exception as e:
            print(f"WebSocket Error: {e}")

        return LeadRepository.get_by_id(lead_id)

# --- SPECIALIZED LEAD ROUTES (Moved from app.py) ---

@leads_bp.route('/matrix', methods=['GET'])
def get_leads_matrix():
    # Filtre Parametrelerini Al
    min_match = request.args.get('min_match', type=int) 
    segment = request.args.get('segment') 
    prop_type = request.args.get('type') 

    with get_db() as conn:
        query = '''
            SELECT l.id, l.name, l.score_x, l.score_y, l.score_z, l.segment, l.status, p.alt_tip
            FROM leads l
            LEFT JOIN portfoyler p ON l.interest_property_id = p.id
            WHERE l.status NOT IN ('lost', 'converted')
        '''
        params = []
        if min_match:
            query += ' AND l.score_z >= ?'
            params.append(min_match)
        if segment:
            query += ' AND l.segment = ?'
            params.append(segment)
        if prop_type:
            query += ' AND p.alt_tip = ?'
            params.append(prop_type)

        leads = conn.execute(query, params).fetchall()
        
        result = []
        for l in leads:
            result.append({
                "id": l['id'],
                "name": l['name'],
                "x": l['score_x'],
                "y": l['score_y'],
                "z": l['score_z'],
                "segment": l['segment'],
                "status": l['status'],
                "looking_for": l['alt_tip']
            })
        return jsonify(result)

@leads_bp.route('/<int:id>/score', methods=['POST'])
def update_lead_score(id):
    data = request.json
    with get_db() as conn:
        lead = conn.execute('SELECT score_x, score_y, score_z FROM leads WHERE id = ?', (id,)).fetchone()
        if not lead:
            return jsonify({"error": "Lead not found"}), 404
            
        new_x, new_y, new_z = lead['score_x'], lead['score_y'], lead['score_z']
        action = data.get('action')
        
        if action == 'roi_calculator':
            new_x = min(100, new_x + 10)
            new_y = min(100, new_y + 5)
            new_z = min(100, new_z + 5)
        elif action == 'urgent_form':
            new_y = min(100, new_y + 30)
        elif action == 'luxury_view':
            new_x = min(100, new_x + 5)
            new_z = min(100, new_z + 10)
        
        conn.execute('UPDATE leads SET score_x = ?, score_y = ?, score_z = ? WHERE id = ?', (new_x, new_y, new_z, id))
        conn.commit()
        return jsonify({"status": "updated", "new_scores": {"x": new_x, "y": new_y, "z": new_z}})

@leads_bp.route('/call-list', methods=['GET'])
def get_call_list():
    limit = request.args.get('limit', default=20, type=int)
    days_threshold = request.args.get('days', default=3, type=int)
    
    with get_db() as conn:
        query = '''
            SELECT *, 
                (score_x + score_y + IFNULL(score_z, 50)) / 3 as avg_score,
                CASE 
                    WHEN last_contacted_at IS NULL THEN 1 
                    WHEN segment = 'buyuk_balik' AND date(last_contacted_at) < date('now', '-7 days') THEN 1
                    WHEN date(last_contacted_at) < date('now', '-' || ? || ' days') THEN 2 
                    ELSE 3 
                END as priority_group
            FROM leads 
            WHERE status NOT IN ('lost', 'converted')
            ORDER BY priority_group ASC, (CASE WHEN segment = 'buyuk_balik' THEN 1 ELSE 0 END) DESC, avg_score DESC 
            LIMIT ?
        '''
        leads = conn.execute(query, (days_threshold, limit)).fetchall()
        return jsonify([dict(row) for row in leads])

@leads_bp.route('/<int:id>/log-call', methods=['POST'])
def log_call(id):
    with get_db() as conn:
        conn.execute('UPDATE leads SET last_contacted_at = CURRENT_TIMESTAMP, status = "contacted" WHERE id = ?', (id,))
        conn.commit()
        return jsonify({"status": "success", "message": "Görüşme kaydedildi."})

@leads_bp.route('/<int:id>/whatsapp-template', methods=['GET'])
def get_whatsapp_template(id):
    property_id = request.args.get('property_id')
    with get_db() as conn:
        lead = conn.execute('SELECT * FROM leads WHERE id = ?', (id,)).fetchone()
        if not lead:
            return jsonify({"error": "Müşteri bulunamadı"}), 404

        prop = None
        if property_id:
            # Standardization Fix (Phase 14)
            prop = conn.execute('SELECT id, baslik1 as title, fiyat as price, lokasyon as location FROM portfoyler WHERE id = ?', (property_id,)).fetchone()

        name = lead['name'].split(' ')[0]
        segment = lead['segment']
        context_type = 'property' if prop else 'general'
        
        template_row = conn.execute(
            'SELECT template_text FROM message_templates WHERE segment = ? AND context_type = ?', 
            (segment, context_type)
        ).fetchone()
        
        if not template_row:
            template_row = conn.execute(
                'SELECT template_text FROM message_templates WHERE segment = ? AND context_type = ?', 
                ('default', 'general')
            ).fetchone()
        
        raw_text = template_row['template_text'] if template_row else "Merhaba {name}, İmza Gayrimenkul'den ulaşıyorum."
        message_text = raw_text.replace('{name}', name)
        if prop:
            message_text = message_text.replace('{property_title}', prop.get('title', 'Bu portföy'))
            message_text = message_text.replace('{property_price}', str(prop.get('price', '')))
            message_text = message_text.replace('{property_location}', prop.get('location', ''))

        phone = lead['phone']
        if phone:
            phone = phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
            if phone.startswith('0'): phone = '9' + phone
            elif not phone.startswith('90'): phone = '90' + phone
            
        import urllib.parse
        encoded_message = urllib.parse.quote(message_text)
        whatsapp_url = f"https://wa.me/{phone}?text={encoded_message}"
        
        return jsonify({
            "lead_name": lead['name'],
            "segment": segment,
            "message_text": message_text,
            "whatsapp_link": whatsapp_url
        })

@leads_bp.route('', methods=['GET'])
def get_leads():
    user = get_current_user()
    if not user: return api_error("UNAUTHORIZED", "Authentication required", status_code=401)
    leads_data = LeadRepository.get_leads_for_user(user['id'], user['role'], user.get('circle', 'outer'))
    return jsonify(lead_schema.dump(leads_data, many=True)), 200

@leads_bp.route('/<int:id>', methods=['GET'])
def get_lead(id):
    lead = LeadRepository.get_by_id(id)
    if not lead:
        return api_error("NOT_FOUND", "Lead not found", status_code=404)
    return jsonify(lead_schema.dump(lead)), 200

@leads_bp.route('', methods=['POST'])
def add_lead():
    try:
        lead = LeadService.calculate_and_create(request.json)
        return jsonify(lead_schema.dump(lead)), 201
    except ValidationError as err:
        return api_error("VALIDATION_ERROR", "Invalid lead data", details=err.messages)
    except Exception as e:
        return api_error("SERVER_ERROR", str(e), status_code=500)

@leads_bp.route('/<int:id>', methods=['PUT'])
@require_permission('leads.edit')
def update_lead(id):
    if LeadRepository.update(id, request.json):
        return jsonify({'status': 'updated'}), 200
    return api_error("NOT_FOUND", "Lead not found", status_code=404)

@leads_bp.route('/<int:id>', methods=['DELETE'])
@require_permission('leads.delete')
def delete_lead(id):
    if LeadRepository.delete(id):
        return jsonify({'status': 'deleted'}), 200
    return api_error("NOT_FOUND", "Lead not found", status_code=404)

@leads_bp.route('/<int:id>/interactions', methods=['GET'])
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

@leads_bp.route('/<int:id>/footprint', methods=['GET'])
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
