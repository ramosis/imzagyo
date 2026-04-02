from typing import List, Dict, Any, Optional
from shared.extensions import db
from modules.crm.models import Lead, Appointment, Contact, PipelineStage, PipelineHistory
from modules.portfolio.models import PortfolioListing
from modules.auth.models import User
from sqlalchemy import or_

class LeadRepository:
    """Handles database operations for Leads using SQLAlchemy ORM."""
    
    @staticmethod
    def get_leads_for_user(user_id: int, role: str, circle: str) -> List[Lead]:
        query = db.session.query(Lead)
        
        if circle == 'outer':
            # View leads interested in the user's properties
            query = query.join(PortfolioListing, Lead.interest_property_id == PortfolioListing.id)\
                         .filter(PortfolioListing.owner_id == user_id)
        elif role not in ['admin', 'super_admin']:
            # Regular users only see their assigned leads
            query = query.filter(Lead.assigned_user_id == user_id)
            
        return query.order_by(Lead.ai_score.desc(), Lead.created_at.desc()).all()

    @staticmethod
    def get_by_id(lead_id: int) -> Optional[Lead]:
        return db.session.get(Lead, lead_id)

    @staticmethod
    def get_by_phone_or_email(phone: str = None, email: str = None) -> Optional[Lead]:
        if not phone and not email:
            return None
        filters = []
        if phone:
            filters.append(Lead.phone == phone)
        if email:
            filters.append(Lead.email == email)
        return Lead.query.filter(or_(*filters)).first()

    @staticmethod
    def create(data: Dict[str, Any]) -> Lead:
        lead = Lead(**data)
        db.session.add(lead)
        db.session.commit()
        return lead

    @staticmethod
    def update(lead_id: int, data: Dict[str, Any]) -> Optional[Lead]:
        lead = db.session.get(Lead, lead_id)
        if lead:
            for key, value in data.items():
                if hasattr(lead, key):
                    setattr(lead, key, value)
            db.session.commit()
        return lead

    @staticmethod
    def delete(lead_id: int) -> bool:
        lead = db.session.get(Lead, lead_id)
        if lead:
            db.session.delete(lead)
            db.session.commit()
            return True
        return False

class AppointmentRepository:
    """Handles database operations for Appointments using SQLAlchemy ORM."""
    
    @staticmethod
    def get_all() -> List[Appointment]:
        return Appointment.query.order_by(Appointment.created_at.desc()).all()

    @staticmethod
    def create(data: Dict[str, Any]) -> Appointment:
        appointment = Appointment(**data)
        db.session.add(appointment)
        db.session.commit()
        return appointment

class PipelineRepository:
    """Handles database operations for Pipeline Stages and History."""
    
    @staticmethod
    def get_stages() -> List[PipelineStage]:
        return PipelineStage.query.order_by(PipelineStage.order_index).all()

    @staticmethod
    def update_lead_stage(lead_id: int, new_stage_id: int, user_id: int, reason: str = 'Manuel geçiş') -> bool:
        lead = db.session.get(Lead, lead_id)
        if not lead:
            return False
            
        old_stage_id = lead.pipeline_stage_id
        lead.pipeline_stage_id = new_stage_id
        
        history = PipelineHistory(
            lead_id=lead_id,
            old_stage_id=old_stage_id,
            new_stage_id=new_stage_id,
            user_id=user_id,
            reason=reason
        )
        
        db.session.add(history)
        db.session.commit()
        return True

class ContactRepository:
    """Handles database operations for Contacts using SQLAlchemy ORM."""
    
    @staticmethod
    def get_all() -> List[Contact]:
        return Contact.query.order_by(Contact.name).all()

    @staticmethod
    def get_by_id(contact_id: int) -> Optional[Contact]:
        return db.session.get(Contact, contact_id)

    @staticmethod
    def create(data: Dict[str, Any]) -> Contact:
        contact = Contact(**data)
        db.session.add(contact)
        db.session.commit()
        return contact

    @staticmethod
    def update(contact_id: int, data: Dict[str, Any]) -> Optional[Contact]:
        contact = db.session.get(Contact, contact_id)
        if contact:
            for key, value in data.items():
                if hasattr(contact, key):
                    setattr(contact, key, value)
            db.session.commit()
        return contact

    @staticmethod
    def delete(contact_id: int) -> bool:
        contact = db.session.get(Contact, contact_id)
        if contact:
            db.session.delete(contact)
            db.session.commit()
            return True
        return False
