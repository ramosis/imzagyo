from typing import Optional, List, Dict, Any
from flask import Blueprint, request, jsonify, g
from database import get_db
import json
from api.utils import sanitize_input
from .schemas import lead_schema, ValidationError
from .auth import get_current_user, require_permission
from extensions import socketio

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
                    JOIN portfoyler p ON l.interest_property_id = p.id
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
            return cursor.lastrowid

    @staticmethod
    def update(lead_id: int, data: Dict[str, Any]) -> bool:
        with get_db() as conn:
            fields = [f"{k}=?" for k in data.keys()]
            if not fields: return False
            values = list(data.values()) + [lead_id]
            cursor = conn.execute(f'UPDATE leads SET {", ".join(fields)} WHERE id=?', values)
            conn.commit()
            return cursor.rowcount > 0

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

@leads_bp.route('/api/leads', methods=['GET'])
def get_leads():
    user = get_current_user()
    if not user: return jsonify([]), 401
    return jsonify(LeadRepository.get_leads_for_user(user['id'], user['role'], user.get('circle', 'outer'))), 200

@leads_bp.route('/api/leads/<int:id>', methods=['GET'])
def get_lead(id):
    lead = LeadRepository.get_by_id(id)
    return jsonify(lead) if lead else (jsonify({'error': 'Lead not found'}), 404)

@leads_bp.route('/api/leads', methods=['POST'])
def add_lead():
    try:
        lead = LeadService.calculate_and_create(request.json)
        return jsonify(lead), 201
    except ValidationError as err:
        return jsonify({"error": "Geçersiz veri", "details": err.messages}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@leads_bp.route('/api/leads/<int:id>', methods=['PUT'])
@require_permission('leads.edit')
def update_lead(id):
    if LeadRepository.update(id, request.json):
        return jsonify({'status': 'updated'}), 200
    return jsonify({'error': 'Lead not found'}), 404

@leads_bp.route('/api/leads/<int:id>', methods=['DELETE'])
@require_permission('leads.delete')
def delete_lead(id):
    if LeadRepository.delete(id):
        return jsonify({'status': 'deleted'}), 200
    return jsonify({'error': 'Lead not found'}), 404

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
