from typing import List, Dict, Any
from .repository import CRMRepository

class CRMService:
    @staticmethod
    def get_all_leads() -> List[Dict[str, Any]]:
        return CRMRepository.get_leads()

    @staticmethod
    def create_lead(data: Dict[str, Any]) -> int:
        return CRMRepository.create_lead(data)

    @staticmethod
    def get_pipeline_data() -> Dict[str, Any]:
        leads = CRMRepository.get_leads()
        # Logic to group leads by stage
        return {"stages": ["new", "contacted", "qualified", "closed"], "data": leads}
