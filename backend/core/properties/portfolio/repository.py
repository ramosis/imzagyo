from typing import List, Dict, Any, Optional
from backend.shared.database import get_db_connection

class PropertyRepository:
    @staticmethod
    def get_all(filters: Dict[str, Any] = None, lang: str = 'tr') -> List[Dict[str, Any]]:
        with get_db_connection() as conn:
            query = "SELECT * FROM properties WHERE is_active = 1"
            # Filtering logic would go here
            rows = conn.execute(query).fetchall()
            return [dict(r) for r in rows]

    @staticmethod
    def get_by_id(property_id: int, lang: str = 'tr') -> Optional[Dict[str, Any]]:
        with get_db_connection() as conn:
            row = conn.execute("SELECT * FROM properties WHERE id = ?", (property_id,)).fetchone()
            return dict(row) if row else None

    @staticmethod
    def get_featured(lang: str = 'tr') -> List[Dict[str, Any]]:
        with get_db_connection() as conn:
            rows = conn.execute("SELECT * FROM properties WHERE is_featured = 1 AND is_active = 1 LIMIT 6").fetchall()
            return [dict(r) for r in rows]

    @staticmethod
    def create(data: Dict[str, Any]) -> int:
        with get_db_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO properties (title_tr, price, location_tr, type) VALUES (?, ?, ?, ?)",
                (data.get('title'), data.get('price'), data.get('location'), data.get('type'))
            )
            return cursor.lastrowid
