from typing import List, Optional, Dict, Any
from datetime import datetime
from shared.database import get_db_connection
from modules.contracts.models import Contract, ContractTemplate, ContractClause, PreparedContract, Party

class ContractRepository:
    @staticmethod
    def create(data: Dict[str, Any]) -> int:
        with get_db_connection() as conn:
            cursor = conn.execute('''
                INSERT INTO contracts (
                    contract_number, contract_type, property_id, lead_id,
                    landlord_id, tenant_id, buyer_id, seller_id,
                    price, currency, commission_rate, commission_amount,
                    start_date, end_date, template_id, content, content_json,
                    created_by, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data['contract_number'], data['contract_type'],
                data.get('property_id'), data.get('lead_id'),
                data.get('landlord_id'), data.get('tenant_id'),
                data.get('buyer_id'), data.get('seller_id'),
                data['price'], data.get('currency', 'TRY'),
                data.get('commission_rate', 0), data.get('commission_amount', 0),
                data.get('start_date'), data.get('end_date'),
                data.get('template_id'), data.get('content'),
                data.get('content_json'), data['created_by'], 'draft'
            ))
            conn.commit()
            return cursor.lastrowid
    
    @staticmethod
    def get_by_id(contract_id: int) -> Optional[Dict]:
        with get_db_connection() as conn:
            contract = conn.execute(
                'SELECT * FROM contracts WHERE id = ?', (contract_id,)
            ).fetchone()
            return dict(contract) if contract else None
    
    @staticmethod
    def get_all(filters: Dict[str, Any] = None, limit: int = 100, offset: int = 0) -> List[Dict]:
        query = 'SELECT * FROM contracts WHERE 1=1'
        params = []
        
        if filters:
            if filters.get('status'):
                query += ' AND status = ?'
                params.append(filters['status'])
            if filters.get('contract_type'):
                query += ' AND contract_type = ?'
                params.append(filters['contract_type'])
            if filters.get('created_by'):
                query += ' AND created_by = ?'
                params.append(filters['created_by'])
        
        query += ' ORDER BY created_at DESC LIMIT ? OFFSET ?'
        params.extend([limit, offset])
        
        with get_db_connection() as conn:
            contracts = conn.execute(query, params).fetchall()
            return [dict(c) for c in contracts]
    
    @staticmethod
    def update(contract_id: int, data: Dict[str, Any]) -> bool:
        allowed_fields = ['status', 'content', 'content_json', 'is_signed', 
                         'signed_by_landlord', 'signed_by_tenant', 'price',
                         'start_date', 'end_date', 'signing_date', 'signature_data']
        
        updates = []
        values = []
        for key, value in data.items():
            if key in allowed_fields:
                updates.append(f'{key} = ?')
                values.append(value)
        
        if not updates:
            return False
        
        values.append(contract_id)
        
        with get_db_connection() as conn:
            cursor = conn.execute(
                f'UPDATE contracts SET {", ".join(updates)}, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
                values
            )
            conn.commit()
            return cursor.rowcount > 0
    
    @staticmethod
    def delete(contract_id: int) -> bool:
        with get_db_connection() as conn:
            cursor = conn.execute('DELETE FROM contracts WHERE id = ?', (contract_id,))
            conn.commit()
            return cursor.rowcount > 0
    
    @staticmethod
    def get_by_id(contract_id: int) -> Optional[Dict]:
        with get_db_connection() as conn:
            contract = conn.execute('SELECT * FROM contracts WHERE id = ?', (contract_id,)).fetchone()
            return dict(contract) if contract else None

    @staticmethod
    def generate_contract_number() -> str:
        """IMZ-2024-00001 formatında numara üret"""
        with get_db_connection() as conn:
            result = conn.execute(
                "SELECT COUNT(*) as count FROM contracts"
            ).fetchone()
            count = result['count'] + 1
            return f"IMZ-{datetime.now().year}-{count:05d}"


class ContractTemplateRepository:
    @staticmethod
    def get_by_type(contract_type: str) -> List[Dict]:
        with get_db_connection() as conn:
            templates = conn.execute(
                'SELECT * FROM contract_templates WHERE contract_type = ? AND is_active = 1',
                (contract_type,)
            ).fetchall()
            return [dict(t) for t in templates]
    
    @staticmethod
    def get_default(contract_type: str) -> Optional[Dict]:
        with get_db_connection() as conn:
            template = conn.execute(
                'SELECT * FROM contract_templates WHERE contract_type = ? AND is_default = 1',
                (contract_type,)
            ).fetchone()
            return dict(template) if template else None


class PartyRepository:
    @staticmethod
    def create(contract_id: int, party_data: Dict[str, Any]) -> int:
        with get_db_connection() as conn:
            cursor = conn.execute('''
                INSERT INTO parties (contract_id, party_type, full_name, tc_no, phone, email, address)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                contract_id, party_data['party_type'], party_data['full_name'],
                party_data.get('tc_no'), party_data.get('phone'),
                party_data.get('email'), party_data.get('address')
            ))
            conn.commit()
            return cursor.lastrowid
    
    @staticmethod
    def get_by_contract(contract_id: int) -> List[Dict]:
        with get_db_connection() as conn:
            parties = conn.execute(
                'SELECT * FROM parties WHERE contract_id = ?', (contract_id,)
            ).fetchall()
            return [dict(p) for p in parties]
    
    @staticmethod
    def sign(party_id: int, signature_data: Dict[str, Any]) -> bool:
        with get_db_connection() as conn:
            cursor = conn.execute('''
                UPDATE parties 
                SET is_signed = 1, signed_at = CURRENT_TIMESTAMP, signature_ip = ?
                WHERE id = ?
            ''', (signature_data.get('ip'), party_id))
            conn.commit()
            return cursor.rowcount > 0
