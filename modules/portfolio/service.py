from typing import Dict, Any
from shared.utils import sanitize_input, sanitize_html
from shared.schemas import portfolio_schema
# from modules.ai.routes import translate_content  # REMOVED TO BREAK CIRCULAR IMPORT
from .repository import PortfolioRepository

class PortfolioService:
    @staticmethod
    def process_and_create(data: Dict[str, Any]) -> Dict[str, Any]:
        sanitized_data = sanitize_input(data)
        validated_data = portfolio_schema.load(sanitized_data)
        if 'hikaye' in validated_data:
             validated_data['hikaye'] = sanitize_html(validated_data['hikaye'])
        
        target_fields = ['baslik1', 'baslik2', 'lokasyon', 'hikaye']
        for field in target_fields:
            if field in validated_data:
                from modules.ai.routes import translate_content
                source = validated_data[field]
                validated_data[f'{field}_en'] = translate_content(source, 'İngilizce')
                validated_data[f'{field}_ar'] = translate_content(source, 'Arapça')
        
        new_id = PortfolioRepository.create(validated_data)
        return PortfolioRepository.get_by_id(new_id)

    @staticmethod
    def can_manage_portfolio(user: Dict[str, Any], portfolio_id: str) -> bool:
        if user.get('role') in ['admin', 'super_admin', 'broker']:
            return True
        owner_id = PortfolioRepository.get_owner_id(portfolio_id)
        return owner_id == user.get('id')
