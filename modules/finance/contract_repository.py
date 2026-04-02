from typing import List, Optional, Dict, Any
from datetime import datetime
from shared.extensions import db
from modules.finance.models import Contract, ContractTemplate, ContractClause, ContractParty

class ContractRepository:
    @staticmethod
    def create(data: Dict[str, Any]) -> Contract:
        contract = Contract(
            contract_number=data.get('contract_number') or ContractRepository.generate_contract_number(),
            contract_type=data['contract_type'],
            property_id=data.get('property_id'),
            lead_id=data.get('lead_id'),
            landlord_id=data.get('landlord_id'),
            tenant_id=data.get('tenant_id'),
            buyer_id=data.get('buyer_id'),
            seller_id=data.get('seller_id'),
            price=data['price'],
            currency=data.get('currency', 'TRY'),
            commission_rate=data.get('commission_rate', 0),
            commission_amount=data.get('commission_amount', 0),
            start_date=data.get('start_date'),
            end_date=data.get('end_date'),
            template_id=data.get('template_id'),
            content=data.get('content'),
            content_json=data.get('content_json'),
            created_by=data['created_by'],
            status='draft'
        )
        db.session.add(contract)
        db.session.commit()
        return contract
    
    @staticmethod
    def get_by_id(contract_id: int) -> Optional[Contract]:
        return Contract.query.get(contract_id)
    
    @staticmethod
    def get_all(filters: Dict[str, Any] = None, limit: int = 100, offset: int = 0) -> List[Contract]:
        query = Contract.query
        
        if filters:
            if filters.get('status'):
                query = query.filter_by(status=filters['status'])
            if filters.get('contract_type'):
                query = query.filter_by(contract_type=filters['contract_type'])
            if filters.get('created_by'):
                query = query.filter_by(created_by=filters['created_by'])
        
        return query.order_by(Contract.created_at.desc()).limit(limit).offset(offset).all()
    
    @staticmethod
    def update(contract_id: int, data: Dict[str, Any]) -> bool:
        contract = Contract.query.get(contract_id)
        if not contract:
            return False
            
        allowed_fields = ['status', 'content', 'content_json', 'is_signed', 
                         'signed_by_landlord', 'signed_by_tenant', 'price',
                         'start_date', 'end_date', 'signing_date', 'signature_data',
                         'pdf_path', 'pdf_url']
        
        for key, value in data.items():
            if key in allowed_fields:
                setattr(contract, key, value)
        
        db.session.commit()
        return True
    
    @staticmethod
    def delete(contract_id: int) -> bool:
        contract = Contract.query.get(contract_id)
        if contract:
            db.session.delete(contract)
            db.session.commit()
            return True
        return False

    @staticmethod
    def generate_contract_number() -> str:
        count = Contract.query.count() + 1
        return f"IMZ-{datetime.now().year}-{count:05d}"

class ContractTemplateRepository:
    @staticmethod
    def get_by_type(contract_type: str) -> List[ContractTemplate]:
        return ContractTemplate.query.filter_by(contract_type=contract_type, is_active=True).all()
    
    @staticmethod
    def get_default(contract_type: str) -> Optional[ContractTemplate]:
        return ContractTemplate.query.filter_by(contract_type=contract_type, is_default=True).first()

class PartyRepository:
    @staticmethod
    def create(contract_id: int, party_data: Dict[str, Any]) -> ContractParty:
        party = ContractParty(
            contract_id=contract_id,
            party_type=party_data['party_type'],
            full_name=party_data['full_name'],
            tc_no=party_data.get('tc_no'),
            phone=party_data.get('phone'),
            email=party_data.get('email'),
            address=party_data.get('address')
        )
        db.session.add(party)
        db.session.commit()
        return party
    
    @staticmethod
    def get_by_contract(contract_id: int) -> List[ContractParty]:
        return ContractParty.query.filter_by(contract_id=contract_id).all()
    
    @staticmethod
    def sign(party_id: int, signature_data: Dict[str, Any]) -> bool:
        party = ContractParty.query.get(party_id)
        if party:
            party.is_signed = True
            party.signed_at = datetime.utcnow()
            party.signature_ip = signature_data.get('ip')
            db.session.commit()
            return True
        return False
