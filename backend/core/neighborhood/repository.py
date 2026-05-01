from typing import List, Dict, Any
from backend.shared.database import db_session
from .models import Announcement, Facility

class NeighborhoodRepository:
    @staticmethod
    def get_announcements() -> List[Dict[str, Any]]:
        rows = db_session.query(Announcement).order_by(Announcement.created_at.desc()).all()
        return [{
            'id': r.id,
            'title': r.title,
            'content': r.content,
            'category': r.category,
            'created_at': r.created_at.isoformat()
        } for r in rows]

    @staticmethod
    def get_facilities() -> List[Dict[str, Any]]:
        rows = db_session.query(Facility).all()
        return [{
            'id': r.id,
            'name': r.name,
            'type': r.type,
            'status': r.status
        } for r in rows]
