from typing import List, Dict, Any, Optional
from backend.shared.database import db_session
from .models import Property

class PropertyRepository:
    @staticmethod
    def get_all(filters: Dict[str, Any] = None, lang: str = 'tr') -> List[Dict[str, Any]]:
        query = db_session.query(Property).filter_by(is_active=True)
        # Filtering logic would go here
        rows = query.all()
        return [{
            'id': r.id,
            'title': getattr(r, f'title_{lang}'),
            'price': r.price,
            'location': getattr(r, f'location_{lang}'),
            'type': r.type
        } for r in rows]

    @staticmethod
    def get_by_id(property_id: int, lang: str = 'tr') -> Optional[Dict[str, Any]]:
        r = db_session.query(Property).get(property_id)
        if not r: return None
        return {
            'id': r.id,
            'title': getattr(r, f'title_{lang}'),
            'price': r.price,
            'location': getattr(r, f'location_{lang}'),
            'type': r.type,
            'description': getattr(r, f'description_{lang}')
        }

    @staticmethod
    def get_featured(lang: str = 'tr') -> List[Dict[str, Any]]:
        rows = db_session.query(Property).filter_by(is_featured=True, is_active=True).limit(6).all()
        return [{
            'id': r.id,
            'title': getattr(r, f'title_{lang}'),
            'price': r.price,
            'location': getattr(r, f'location_{lang}'),
            'type': r.type
        } for r in rows]

    @staticmethod
    def create(data: Dict[str, Any]) -> int:
        new_prop = Property(
            title_tr=data.get('title'),
            price=data.get('price'),
            location_tr=data.get('location'),
            type=data.get('type')
        )
        db_session.add(new_prop)
        db_session.commit()
        return new_prop.id
