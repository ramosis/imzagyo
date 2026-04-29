from typing import List, Dict, Any, Optional
from .repository import PropertyRepository

class PropertyService:
    @staticmethod
    def get_filtered_properties(filters: Dict[str, Any], lang: str = 'tr') -> List[Dict[str, Any]]:
        # Business logic for filtering and translation mapping
        return PropertyRepository.get_all(filters, lang)

    @staticmethod
    def get_property_by_id(property_id: int, lang: str = 'tr') -> Optional[Dict[str, Any]]:
        return PropertyRepository.get_by_id(property_id, lang)
