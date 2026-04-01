from typing import List, Dict, Any, Optional
from shared.database import get_db
from shared.utils import invalidate_entity_cache

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
            safe_data = {k: v for k, v in data.items() if str(k).isidentifier()}
            if not safe_data: return 0
            
            columns = ', '.join(safe_data.keys())
            placeholders = ', '.join(['?' for _ in safe_data])
            cursor = conn.execute(f"INSERT INTO leads ({columns}) VALUES ({placeholders})", list(safe_data.values()))
            conn.commit()
            invalidate_entity_cache('lead')
            return cursor.lastrowid

    @staticmethod
    def update(lead_id: int, data: Dict[str, Any]) -> bool:
        with get_db() as conn:
            safe_data = {k: v for k, v in data.items() if str(k).isidentifier()}
            fields = [f"{k}=?" for k in safe_data.keys()]
            if not fields: return False
            values = list(safe_data.values()) + [lead_id]
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

class AppointmentRepository:
    """Handles low-level SQL operations for Appointments."""
    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        with get_db() as conn:
            rows = conn.execute('SELECT * FROM appointments ORDER BY appointment_date DESC').fetchall()
            return [dict(r) for r in rows]

    @staticmethod
    def create(data: Dict[str, Any]) -> int:
        with get_db() as conn:
            safe_data = {k: v for k, v in data.items() if str(k).isidentifier()}
            if not safe_data: return 0
            columns = ', '.join(safe_data.keys())
            placeholders = ', '.join(['?' for _ in safe_data])
            cursor = conn.execute(f"INSERT INTO appointments ({columns}) VALUES ({placeholders})", list(safe_data.values()))
            conn.commit()
            return cursor.lastrowid

class ContactRepository:
    """Handles low-level SQL operations for CRM Contacts."""
    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        with get_db() as conn:
            rows = conn.execute('SELECT * FROM contacts ORDER BY name ASC').fetchall()
            return [dict(r) for r in rows]

    @staticmethod
    def create(data: Dict[str, Any]) -> int:
        with get_db() as conn:
            safe_data = {k: v for k, v in data.items() if str(k).isidentifier()}
            if not safe_data: return 0
            columns = ', '.join(safe_data.keys())
            placeholders = ', '.join(['?' for _ in safe_data])
            cursor = conn.execute(f"INSERT INTO contacts ({columns}) VALUES ({placeholders})", list(safe_data.values()))
            conn.commit()
            return cursor.lastrowid

class PipelineRepository:
    """Handles low-level SQL operations for Pipeline Stages and History."""
    @staticmethod
    def get_stages() -> List[Dict[str, Any]]:
        with get_db() as conn:
            rows = conn.execute('SELECT * FROM pipeline_stages ORDER BY order_index').fetchall()
            return [dict(s) for s in rows]

    @staticmethod
    def get_stage_history(lead_id: int) -> List[Dict[str, Any]]:
        with get_db() as conn:
            rows = conn.execute('SELECT * FROM pipeline_history WHERE lead_id = ? ORDER BY changed_at DESC', (lead_id,)).fetchall()
            return [dict(r) for r in rows]

    @staticmethod
    def update_lead_stage(lead_id: int, new_stage_id: int, user_id: int, reason: str = 'Manuel geçiş') -> bool:
        with get_db() as conn:
            lead = conn.execute('SELECT pipeline_stage_id FROM leads WHERE id = ?', (lead_id,)).fetchone()
            if not lead: return False
            old_stage_id = lead['pipeline_stage_id']
            conn.execute('UPDATE leads SET pipeline_stage_id = ? WHERE id = ?', (new_stage_id, lead_id))
            conn.execute('INSERT INTO pipeline_history (lead_id, old_stage_id, new_stage_id, user_id, reason) VALUES (?, ?, ?, ?, ?)', 
                         (lead_id, old_stage_id, new_stage_id, user_id, reason))
            conn.commit()
            return True
