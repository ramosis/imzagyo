from typing import List, Dict, Any
from .repository import NeighborhoodRepository

class NeighborhoodService:
    @staticmethod
    def get_announcements() -> List[Dict[str, Any]]:
        return NeighborhoodRepository.get_announcements()

    @staticmethod
    def get_facilities() -> List[Dict[str, Any]]:
        return NeighborhoodRepository.get_facilities()
