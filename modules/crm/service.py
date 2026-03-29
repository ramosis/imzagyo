from typing import Dict, Any, List
from shared.schemas import lead_schema
from shared.extensions import socketio

from .repository import LeadRepository

class LeadService:
    @staticmethod
    def calculate_and_create(data: Dict[str, Any]) -> Dict[str, Any]:
        from shared.utils import sanitize_input
        validated_data = lead_schema.load(sanitize_input(data))
        
        # AI Logic
        from modules.ai.routes import calculate_intent_score
        session_id = data.get('session_id')
        behavior_score = calculate_intent_score(session_id)[0] if session_id else 0
        ai_score = min(100, (10 + behavior_score + (20 if validated_data.get('phone') else 0) + (15 if validated_data.get('email') else 0)))
        validated_data['ai_score'] = ai_score

        lead_id = LeadRepository.create(validated_data)
        
        # Notify
        if validated_data.get('assigned_user_id'):
            from shared.notifications import create_notification
            create_notification(validated_data['assigned_user_id'], 'system', 'Yeni Aday', f"Aday assigned.")
        
        try:
            socketio.emit('new_lead', {'id': lead_id, 'name': validated_data.get('name')}, namespace='/')
        except: pass
        return LeadRepository.get_by_id(lead_id)

class PipelineService:
    @staticmethod
    def get_processed_pipeline(stages: List[Dict[str, Any]], leads: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        status_map = {1: 'New', 2: 'Contacted', 3: 'Proposal', 4: 'Proposal', 5: 'Closed'}
        
        processed_leads = []
        for l in leads:
            lead_dict = dict(l)
            lead_dict['intent_category'] = "Genel"
            processed_leads.append(lead_dict)

        for stage in stages:
            stage['leads'] = []
            for l in processed_leads:
                mapped_status = status_map.get(l['pipeline_stage_id'], 'New')
                if mapped_status.lower() == stage['name'].lower() or (stage['id'] == l['pipeline_stage_id']):
                    l['status_label'] = mapped_status
                    stage['leads'].append(l)
        return stages
