from typing import Optional, List, Dict, Any
from shared.database import get_db

class PropertyRepository:
    @staticmethod
    def get_all(filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        with get_db() as conn:
            query = 'SELECT * FROM portfolios WHERE deleted_at IS NULL'
            params = []
            if filters and 'owner_id' in filters:
                query += ' AND owner_id = ?'
                params.append(filters['owner_id'])
            rows = conn.execute(query, params).fetchall()
            return [dict(r) for r in rows]

    @staticmethod
    def get_by_id(property_id: str) -> Optional[Dict[str, Any]]:
        with get_db() as conn:
            row = conn.execute('SELECT * FROM portfolios WHERE id = ? AND deleted_at IS NULL', (property_id,)).fetchone()
            return dict(row) if row else None

    @staticmethod
    def update(property_id: str, data: Dict[str, Any]) -> bool:
        with get_db() as conn:
            fields = []
            values = []
            for k, v in data.items():
                fields.append(f"{k}=?")
                values.append(v)
            if not fields: return False
            values.append(property_id)
            cursor = conn.execute(f'UPDATE portfolios SET {", ".join(fields)} WHERE id=?', values)
            conn.commit()
            return cursor.rowcount > 0
            
    @staticmethod
    def delete(property_id: str) -> bool:
        with get_db() as conn:
            cursor = conn.execute('UPDATE portfolios SET deleted_at = CURRENT_TIMESTAMP WHERE id=?', (property_id,))
            conn.commit()
            return cursor.rowcount > 0
