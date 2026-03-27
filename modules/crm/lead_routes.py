import json
import sqlite3
import urllib.parse
from typing import Optional, List, Dict, Any
from flask import request, jsonify, g
from shared.database import get_db
from shared.extensions import socketio
from shared.utils import api_error, invalidate_entity_cache
from shared.schemas import lead_schema, ValidationError
from modules.auth.decorators import require_permission, login_required
from modules.auth.service import AuthService
from . import crm_bp

class LeadRepository:
    """Handles low-level SQL operations for Leads."""
    @staticmethod
    def get_leads_for_user(user_id: int, role: str, circle: str) -> List[Dict[str, Any]]:
        with get_db() as conn:
            if circle == 'outer':
                query = 'SELECT l.*, p.baslik1 as property_title, u.username as assigned_to FROM leads l LEFT JOIN portfoyler p ON l.interest_property_id = p.id LEFT JOIN users u ON l.assigned_user_id = u.id WHERE p.owner_id = ? ORDER BY l.ai_score DESC, l.created_at DESC'
                rows = conn.execute(query, (user_id,)).fetchall()
            elif role in ['admin', 'super_admin']:
                query = 'SELECT l.*, p.baslik1 as property_title, u.username as assigned_to FROM leads l LEFT JOIN portfoyler p ON l.interest_property_id = p.id LEFT JOIN users u ON l.assigned_user_id = u.id ORDER BY l.ai_score DESC, l.created_at DESC'
                rows = conn.execute(query).fetchall()
            else:
                query = 'SELECT l.*, p.baslik1 as property_title, u.username as assigned_to FROM leads l LEFT JOIN portfoyler p ON l.interest_property_id = p.id LEFT JOIN users u ON l.assigned_user_id = u.id WHERE l.assigned_user_id = ? ORDER BY l.ai_score DESC, l.created_at DESC'
                rows = conn.execute(query, (user_id,)).fetchall()
            return [dict(r) for r in rows]

    @staticmethod
    def get_by_id(lead_id: int) -> Optional[Dict[str, Any]]:
        with get_db() as conn:
            query = 'SELECT l.*, p.baslik1 as property_title, u.username as assigned_to FROM leads l LEFT JOIN portfoyler p ON l.interest_property_id = p.id LEFT JOIN users u ON l.assigned_user_id = u.id WHERE l.id = ?'
            row = conn.execute(query, (lead_id,)).fetchone()
            return dict(row) if row else None

    @staticmethod
    def create(data: Dict[str, Any]) -> int:
        with get_db() as conn:
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['?' for _ in data])
            cursor = conn.execute(f"INSERT INTO leads ({columns}) VALUES ({placeholders})", list(data.values()))
            conn.commit()
            invalidate_entity_cache('lead')
            return cursor.lastrowid

    @staticmethod
    def update(lead_id: int, data: Dict[str, Any]) -> bool:
        with get_db() as conn:
            fields = [f"{k}=?" for k in data.keys()]
            if not fields: return False
            values = list(data.values()) + [lead_id]
            cursor = conn.execute(f'UPDATE leads SET {", ".join(fields)} WHERE id=?', values)
            conn.commit()
            invalidate_entity_cache('lead')
            return cursor.rowcount > 0

    @staticmethod
    def delete(lead_id: int) -> bool:
        with get_db() as conn:
            cursor = conn.execute('DELETE FROM leads WHERE id=?', (lead_id,))
            conn.commit()
            return cursor.rowcount > 0

class LeadService:
    @staticmethod
    def calculate_and_create(data: Dict[str, Any]) -> Dict[str, Any]:
        from shared.utils import sanitize_input
        validated_data = lead_schema.load(sanitize_input(data))
        
        # AI Logic
        from modules.ai.routes import calculate_intent_score
        session_id = data.get('session_id')
        behavior_score = calculate_intent_score(session_id)[0] if session_id else 0
        ai_score = min(100, (10 + behavior_score + (20 if validated_data.get('phone') else 0) + (15 if validated_data.get('email') else 0)))
        validated_data['ai_score'] = ai_score

        lead_id = LeadRepository.create(validated_data)
        
        # Notify
        if validated_data.get('assigned_user_id'):
            from shared.notifications import create_notification
            create_notification(validated_data['assigned_user_id'], 'system', 'Yeni Aday', f"Aday assigned.")
        
        try:
            socketio.emit('new_lead', {'id': lead_id, 'name': validated_data.get('name')}, namespace='/')
        except: pass
        return LeadRepository.get_by_id(lead_id)

@crm_bp.route('/leads', methods=['GET'])
@login_required
def get_leads():
    user = AuthService.get_current_user()
    leads = LeadRepository.get_leads_for_user(user['id'], user['role'], user.get('circle', 'outer'))
    return jsonify(lead_schema.dump(leads, many=True)), 200

@crm_bp.route('/leads/<int:id>', methods=['GET'])
@login_required
def get_lead(id):
    lead = LeadRepository.get_by_id(id)
    if not lead: return api_error("NOT_FOUND", "Lead not found", 404)
    return jsonify(lead_schema.dump(lead)), 200

@crm_bp.route('/leads', methods=['POST'])
def add_lead():
    try:
        lead = LeadService.calculate_and_create(request.json)
        return jsonify(lead_schema.dump(lead)), 201
    except ValidationError as err:
        return api_error("VALIDATION_ERROR", "Invalid data", details=err.messages)
    except Exception as e:
        return api_error("SERVER_ERROR", str(e), 500)

@crm_bp.route('/leads/<int:id>', methods=['PUT'])
@require_permission('leads.edit')
def update_lead(id):
    if LeadRepository.update(id, request.json):
        return jsonify({'status': 'updated'}), 200
    return api_error("NOT_FOUND", "Lead not found", 404)

@crm_bp.route('/leads/<int:id>/whatsapp-template', methods=['GET'])
@login_required
def get_whatsapp_template(id):
    property_id = request.args.get('property_id')
    with get_db() as conn:
        lead = conn.execute('SELECT * FROM leads WHERE id = ?', (id,)).fetchone()
        if not lead: return jsonify({"error": "Lead not found"}), 404
        prop = conn.execute('SELECT baslik1 as title, fiyat as price FROM portfoyler WHERE id = ?', (property_id,)).fetchone() if property_id else None
        
        name = lead['name'].split(' ')[0]
        msg = f"Merhaba {name}, ilgilendiğiniz portföy hakkında bilgi vermek isterim."
        if prop: msg += f" ({prop['title']})"
        
        phone = lead['phone'].replace(' ', '').replace('-', '')
        if phone.startswith('0'): phone = '9' + phone
        elif not phone.startswith('9'): phone = '90' + phone
        
        whatsapp_url = f"https://wa.me/{phone}?text={urllib.parse.quote(msg)}"
        return jsonify({"whatsapp_link": whatsapp_url, "message_text": msg})
