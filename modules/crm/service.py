from typing import Dict, Any, List
import structlog
from shared.schemas import lead_schema
from shared.extensions import socketio, db
from .repository import LeadRepository

logger = structlog.get_logger(__name__)

class LeadService:
    @staticmethod
    def calculate_and_create(data: Dict[str, Any]) -> Dict[str, Any]:
        from shared.utils import sanitize_input
        
        # 1. Sanitize and Validate
        try:
            sanitized_data = sanitize_input(data)
            validated_data = lead_schema.load(sanitized_data)
            logger.info("lead_validation_success", name=validated_data.get('name'))
        except Exception as e:
            logger.error("lead_validation_failed", error=str(e), data=data)
            raise e

        # 2. Check for Duplicates
        phone = validated_data.get('phone')
        email = validated_data.get('email')
        existing_lead = LeadRepository.get_by_phone_or_email(phone=phone, email=email)
        
        # 3. AI Score Logic (Behavioral and Profile scoring)
        from modules.ai.routes import calculate_intent_score
        session_id = data.get('session_id')
        behavior_score = calculate_intent_score(session_id)[0] if session_id else 0
        ai_score = min(100, (10 + behavior_score + (20 if phone else 0) + (15 if email else 0)))
        validated_data['ai_score'] = ai_score

        # 4. Create or Update
        if existing_lead:
            logger.info("lead_duplicate_found", lead_id=existing_lead.id, action="updating")
            # Update interest or notes without losing existing data
            if validated_data.get('interest_property_id'):
                existing_lead.interest_property_id = validated_data['interest_property_id']
            if validated_data.get('notes'):
                existing_lead.notes = (existing_lead.notes or "") + f"\n[Update {existing_lead.created_at}]: " + validated_data['notes']
            existing_lead.ai_score = ai_score
            db.session.commit()
            lead_id = existing_lead.id
        else:
            logger.info("lead_creation_started", name=validated_data.get('name'))
            new_lead = LeadRepository.create(validated_data)
            lead_id = new_lead.id
            logger.info("lead_created_success", lead_id=lead_id)

        # 5. Notifications & Real-time Updates
        if validated_data.get('assigned_user_id'):
            from shared.notifications import create_notification
            create_notification(validated_data['assigned_user_id'], 'system', 'Yeni Aday', f"Aday atandı: {validated_data.get('name')}")
        
        try:
            socketio.emit('new_lead', {'id': lead_id, 'name': validated_data.get('name')}, namespace='/')
        except Exception as e:
            logger.warning("socketio_emit_failed", error=str(e))
            
        # Return serialized lead data
        return lead_schema.dump(LeadRepository.get_by_id(lead_id))

class PipelineService:
    @staticmethod
    def get_processed_pipeline(stages: List[Any], leads: List[Any]) -> List[Dict[str, Any]]:
        # Map stage IDs to labels if needed, or rely on ORM relationships
        result = []
        for stage in stages:
            stage_dict = {
                "id": stage.id,
                "name": stage.name,
                "color": stage.color,
                "leads": []
            }
            # Filter leads belonging to this stage
            stage_leads = [l for l in leads if l.pipeline_stage_id == stage.id]
            for l in stage_leads:
                l_data = lead_schema.dump(l)
                l_data['status_label'] = stage.name
                stage_dict['leads'].append(l_data)
            result.append(stage_dict)
        return result
