import json
from datetime import datetime
from typing import Dict, Any, Optional, List
import os
from jinja2 import Template
from flask import current_app
from modules.finance.contract_repository import (
    ContractRepository, ContractTemplateRepository, PartyRepository
)
from shared.mail_service import send_email

class ContractService:
    @staticmethod
    def create_contract(data: Dict[str, Any], created_by: int) -> Dict[str, Any]:
        """Yeni sözleşme oluştur"""
        # Sözleşme numarası üret
        contract_number = ContractRepository.generate_contract_number()
        
        # Varsayılan şablon al
        template = ContractTemplateRepository.get_default(data['contract_type'])
        if not template:
            # Fallback to by type if no default is marked
            templates = ContractTemplateRepository.get_by_type(data['contract_type'])
            if templates:
                template = templates[0]
            else:
                raise ValueError(f"No template found for type: {data['contract_type']}")
        
        # İçerik oluştur (Jinja2 ile)
        content = ContractService._render_template(template.html_template, data)
        
        # Veritabanına kaydet
        contract_data = {
            **data,
            'contract_number': contract_number,
            'template_id': template.id,
            'content': content,
            'content_json': json.dumps(data),
            'created_by': created_by
        }
        
        contract = ContractRepository.create(contract_data)
        
        # Tarafları kaydet
        for party in data.get('parties', []):
            PartyRepository.create(contract.id, party)
        
        # Komisyon hesapla
        if data.get('commission_rate'):
            commission = data['price'] * (data['commission_rate'] / 100)
            ContractRepository.update(contract.id, {'commission_amount': commission})
        
        return {
            'id': contract.id,
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
        """Sözleşmeyi PDF'e dönüştür (Simplified/Placeholder)"""
        contract = ContractRepository.get_by_id(contract_id)
        if not contract:
            raise ValueError("Contract not found")
        
        # Ensure directory exists
        path = f"uploads/contracts/{contract.contract_number}.pdf"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        # Simulate PDF creation
        with open(path, 'w', encoding='utf-8') as f:
            f.write(contract.content)
            
        return path
    
    @staticmethod
    def send_for_signature(contract_id: int, send_method: str = 'email') -> bool:
        """Sözleşmeyi imzaya gönder"""
        contract = ContractRepository.get_by_id(contract_id)
        parties = PartyRepository.get_by_contract(contract_id)
        
        pdf_path = ContractService.generate_pdf(contract_id)
        
        for party in parties:
            if party.email and send_method == 'email':
                # Simplified mail sending
                try:
                    send_email(
                        recipient=party.email,
                        subject=f"İmza Gerekiyor: Sözleşme #{contract.contract_number}",
                        body_html=f"Merhaba {party.full_name}, lütfen sözleşmeyi imzalayınız: /contracts/sign/{contract_id}/party/{party.id}"
                    )
                except Exception as e:
                    print(f"Mail send error: {e}")
        
        ContractRepository.update(contract_id, {'status': 'sent'})
        return True
    
    @staticmethod
    def sign_contract(contract_id: int, party_id: int, signature_data: Dict[str, Any]) -> bool:
        """Sözleşmeyi imzala"""
        # Tarafı imzala
        PartyRepository.sign(party_id, signature_data)
        
        # Sözleşme durumunu güncelle
        parties = PartyRepository.get_by_contract(contract_id)
        all_signed = all(p.is_signed for p in parties)
        
        if all_signed:
            ContractRepository.update(contract_id, {
                'status': 'signed',
                'is_signed': True,
                'signing_date': datetime.utcnow().isoformat()
            })
        
        return True
    
    @staticmethod
    def calculate_commission(price: float, commission_type: str = 'standard') -> Dict[str, float]:
        """Komisyon hesapla"""
        rates = {
            'standard': 0.03,      # %3
            'premium': 0.025,      # %2.5
            'enterprise': 0.02,    # %2
            'kiralama': 1.0        # 1 kira bedeli
        }
        
        rate = rates.get(commission_type, 0.03)
        
        if commission_type == 'kiralama':
            commission = price
        else:
            commission = price * rate
        
        return {
            'price': price,
            'commission_rate': rate * 100 if commission_type != 'kiralama' else 100,
            'commission_amount': commission,
            'net_to_owner': price - commission if commission_type != 'kiralama' else price
        }
