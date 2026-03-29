from typing import List, Dict, Any, Optional
import uuid
import json
from shared.database import get_db

class PortfolioRepository:
    """Handles low-level SQL operations for Portfolios."""
    @staticmethod
    def get_all(filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        with get_db() as conn:
            query = 'SELECT * FROM portfoyler'
            params = []
            if filters:
                if filters.get('owner_id'):
                    query += ' WHERE owner_id = ?'
                    params.append(filters['owner_id'])
            rows = conn.execute(query, params).fetchall()
            return [dict(row) for row in rows]

    @staticmethod
    def get_by_id(portfolio_id: str) -> Optional[Dict[str, Any]]:
        with get_db() as conn:
            row = conn.execute('SELECT * FROM portfoyler WHERE id = ?', (portfolio_id,)).fetchone()
            return dict(row) if row else None

    @staticmethod
    def create(data: Dict[str, Any]) -> str:
        with get_db() as conn:
            if not data.get('id'):
                data['id'] = str(uuid.uuid4())
            if 'ozellikler_arr' in data:
                data['ozellikler'] = json.dumps(data.pop('ozellikler_arr'))
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['?' for _ in data])
            conn.execute(f"INSERT INTO portfoyler ({columns}) VALUES ({placeholders})", list(data.values()))
            conn.commit()
            return data['id']

    @staticmethod
    def update(portfolio_id: str, update_data: Dict[str, Any]) -> bool:
        with get_db() as conn:
            if 'ozellikler_arr' in update_data:
                update_data['ozellikler'] = json.dumps(update_data.pop('ozellikler_arr'))
            fields = [f"{k} = ?" for k in update_data.keys()]
            if not fields: return False
            values = list(update_data.values()) + [portfolio_id]
            cursor = conn.execute(f"UPDATE portfoyler SET {', '.join(fields)} WHERE id = ?", values)
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def get_owner_id(portfolio_id: str) -> Optional[int]:
        with get_db() as conn:
            row = conn.execute('SELECT owner_id FROM portfoyler WHERE id = ?', (portfolio_id,)).fetchone()
            return row['owner_id'] if row else None

    @staticmethod
    def delete(portfolio_id: str) -> bool:
        with get_db() as conn:
            cursor = conn.execute('DELETE FROM portfoyler WHERE id = ?', (portfolio_id,))
            conn.commit()
            return cursor.rowcount > 0

class HeroRepository:
    """Handles low-level SQL operations for Hero Slides."""
    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        with get_db() as conn:
            rows = conn.execute('SELECT * FROM hero_slides ORDER BY sira ASC').fetchall()
            return [dict(row) for row in rows]

    @staticmethod
    def get_by_id(slide_id: int) -> Optional[Dict[str, Any]]:
        with get_db() as conn:
            row = conn.execute('SELECT * FROM hero_slides WHERE id = ?', (slide_id,)).fetchone()
            return dict(row) if row else None

    @staticmethod
    def create(data: Dict[str, Any]) -> int:
        with get_db() as conn:
            cursor = conn.execute('''
                INSERT INTO hero_slides 
                (resim_url, alt_baslik, baslik_satir1, baslik_satir2, buton1_metin, buton2_metin, buton2_link, sira)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data.get('resim_url', ''), data.get('alt_baslik', ''),
                data.get('baslik_satir1', ''), data.get('baslik_satir2', ''),
                data.get('buton1_metin', ''), data.get('buton2_metin', ''),
                data.get('buton2_link', ''), data.get('sira', 0)
            ))
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def update(slide_id: int, data: Dict[str, Any]) -> bool:
        with get_db() as conn:
            cursor = conn.execute('''
                UPDATE hero_slides SET 
                    resim_url = ?, alt_baslik = ?, 
                    baslik_satir1 = ?, baslik_satir2 = ?, 
                    buton1_metin = ?, buton2_metin = ?, 
                    buton2_link = ?, sira = ?
                WHERE id = ?
            ''', (
                data.get('resim_url', ''), data.get('alt_baslik', ''),
                data.get('baslik_satir1', ''), data.get('baslik_satir2', ''),
                data.get('buton1_metin', ''), data.get('buton2_metin', ''),
                data.get('buton2_link', ''), data.get('sira', 0),
                slide_id
            ))
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def delete(slide_id: int) -> bool:
        with get_db() as conn:
            cursor = conn.execute('DELETE FROM hero_slides WHERE id = ?', (slide_id,))
            conn.commit()
            return cursor.rowcount > 0

class NeighborhoodRepository:
    """Handles low-level SQL operations for Neighborhoods."""
    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        with get_db() as conn:
            rows = conn.execute('SELECT * FROM neighborhoods ORDER BY name ASC').fetchall()
            return [dict(row) for row in rows]

    @staticmethod
    def create(data: Dict[str, Any]) -> int:
        with get_db() as conn:
            cursor = conn.execute('''
                INSERT INTO neighborhoods (name, city, district, description, image_url)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                data.get('name', ''), data.get('city', ''),
                data.get('district', ''), data.get('description', ''),
                data.get('image_url', '')
            ))
            conn.commit()
            return cursor.lastrowid

class ProjectRepository:
    """Handles low-level SQL operations for Projects."""
    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        with get_db() as conn:
            rows = conn.execute('SELECT * FROM projects ORDER BY created_at DESC').fetchall()
            return [dict(row) for row in rows]

    @staticmethod
    def create(data: Dict[str, Any]) -> int:
        with get_db() as conn:
            cursor = conn.execute('''
                INSERT INTO projects (name, description, status, location, image_url)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                data.get('name', ''), data.get('description', ''),
                data.get('status', 'Planning'), data.get('location', ''),
                data.get('image_url', '')
            ))
            conn.commit()
            return cursor.lastrowid

class ValuationRepository:
    """Handles low-level SQL operations for Valuations."""
    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        with get_db() as conn:
            rows = conn.execute('SELECT * FROM valuations ORDER BY created_at DESC').fetchall()
            return [dict(row) for row in rows]

    @staticmethod
    def create(data: Dict[str, Any]) -> int:
        with get_db() as conn:
            cursor = conn.execute('''
                INSERT INTO valuations (property_id, client_name, estimated_value, notes)
                VALUES (?, ?, ?, ?)
            ''', (
                data.get('property_id'), data.get('client_name', ''),
                data.get('estimated_value', 0), data.get('notes', '')
            ))
            conn.commit()
            return cursor.lastrowid
