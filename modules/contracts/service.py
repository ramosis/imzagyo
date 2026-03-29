import json
from datetime import datetime
from typing import Dict, Any, Optional, List
from jinja2 import Template
from modules.contracts.repository import (
    ContractRepository, ContractTemplateRepository, PartyRepository
)

class ContractService:
    @staticmethod
    def create_contract(data: Dict[str, Any], created_by: int) -> Dict[str, Any]:
        """Yeni sözleşme oluştur"""
        # Sözleşme numarası üret
        contract_number = ContractRepository.generate_contract_number()
        
        # Varsayılan şablon al
        template = ContractTemplateRepository.get_default(data['contract_type'])
        if not template:
            raise ValueError(f"No default template found for type: {data['contract_type']}")
        
        # İçerik oluştur (Jinja2 ile)
        content = ContractService._render_template(template['html_template'], data)
        
        # Veritabanına kaydet
        contract_data = {
            **data,
            'contract_number': contract_number,
            'template_id': template['id'],
            'content': content,
            'content_json': json.dumps(data),
            'created_by': created_by
        }
        
        contract_id = ContractRepository.create(contract_data)
        
        # Tarafları kaydet
        for party in data.get('parties', []):
            PartyRepository.create(contract_id, party)
        
        return {
            'id': contract_id,
            'contract_number': contract_number,
            'status': 'draft'
        }
    
    @staticmethod
    def _render_template(template_html: str, data: Dict[str, Any]) -> str:
        """Jinja2 template render et"""
        template = Template(template_html)
        return template.render(**data)
    
    @staticmethod
    def generate_pdf(contract_id: int) -> str:
        """Sözleşmeyi PDF'e dönüştür (Simulated for now)"""
        contract = ContractRepository.get_by_id(contract_id)
        if not contract:
            raise ValueError("Contract not found")
        
        # Gerçek PDF kütüphanesi (pdfkit/reportlab) eklenebilir
        return f"contracts/pdf/{contract['contract_number']}.pdf"
