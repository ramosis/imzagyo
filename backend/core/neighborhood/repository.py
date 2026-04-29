from typing import List, Dict, Any
from backend.shared.database import get_db_connection

class NeighborhoodRepository:
    @staticmethod
    def get_announcements() -> List[Dict[str, Any]]:
        with get_db_connection() as conn:
            rows = conn.execute("SELECT * FROM announcements ORDER BY created_at DESC").fetchall()
            return [dict(r) for r in rows]

    @staticmethod
    def get_facilities() -> List[Dict[str, Any]]:
        with get_db_connection() as conn:
            rows = conn.execute("SELECT * FROM neighborhood_facilities").fetchall()
            return [dict(r) for r in rows]
