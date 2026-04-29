from typing import List, Dict, Any
from backend.shared.database import get_db_connection

class CRMRepository:
    @staticmethod
    def get_leads() -> List[Dict[str, Any]]:
        with get_db_connection() as conn:
            rows = conn.execute("SELECT * FROM contacts WHERE category = 'lead'").fetchall()
            return [dict(r) for r in rows]

    @staticmethod
    def create_lead(data: Dict[str, Any]) -> int:
        with get_db_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO contacts (name, email, phone, category, source) VALUES (?, ?, ?, 'lead', ?)",
                (data.get('name'), data.get('email'), data.get('phone'), data.get('source'))
            )
            return cursor.lastrowid
