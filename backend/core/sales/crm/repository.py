from typing import List, Dict, Any
from backend.shared.database import db_session
from .models import Contact

class CRMRepository:
    @staticmethod
    def get_leads() -> List[Dict[str, Any]]:
        leads = db_session.query(Contact).filter_by(category='lead').all()
        return [{
            'id': l.id,
            'name': l.name,
            'email': l.email,
            'phone': l.phone,
            'status': l.status,
            'source': l.source
        } for l in leads]

    @staticmethod
    def create_lead(data: Dict[str, Any]) -> int:
        new_lead = Contact(
            name=data.get('name'),
            email=data.get('email'),
            phone=data.get('phone'),
            category='lead',
            source=data.get('source')
        )
        db_session.add(new_lead)
        db_session.commit()
        return new_lead.id
