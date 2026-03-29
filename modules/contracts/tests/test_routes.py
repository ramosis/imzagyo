import pytest
import json
from datetime import datetime, timedelta

def test_create_contract(client, admin_auth):
    """Sözleşme oluşturma testi"""
    data = {
        'property_id': 'bogaz-villa',
        'price': 5000.0,
        'currency': 'TRY',
        'commission_rate': 3.0,
        'start_date': datetime.now().strftime('%Y-%m-%d'),
        'end_date': (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d'),
        'parties': [
            {
                'party_type': 'landlord',
                'full_name': 'Ahmet Yılmaz',
                'tc_no': '12345678901',
                'phone': '5551234567',
                'email': 'ahmet@example.com'
            },
            {
                'party_type': 'tenant',
                'full_name': 'Mehmet Demir',
                'tc_no': '10987654321',
                'phone': '5559876543',
                'email': 'mehmet@example.com'
            }
        ]
    }
    
    # Pre-seed a template to avoid ValueError
    from shared.database import get_db_connection
    with get_db_connection() as conn:
        conn.execute('''
            INSERT OR IGNORE INTO contract_templates (name, contract_type, html_template, is_default)
            VALUES (?, ?, ?, ?)
        ''', ('Kiralama Şablonu', 'kiralama', '<h1>Test Template</h1>', 1))
        conn.commit()

    response = client.post('/api/v1/contracts/', 
                          data=json.dumps(data),
                          content_type='application/json',
                          headers=admin_auth)
    
    assert response.status_code == 201
    assert 'contract_number' in response.get_json()
    assert response.get_json()['status'] == 'draft'

def test_get_contracts(client, admin_auth):
    """Sözleşme listesi testi"""
    response = client.get('/api/v1/contracts/', headers=admin_auth)
    assert response.status_code == 200
    assert 'data' in response.get_json()

def test_calculate_commission(client, admin_auth):
    """Komisyon hesaplama testi"""
    data = {
        'price': 1000000.0,
        'type': 'standard'
    }
    
    response = client.post('/api/v1/contracts/calculate-commission',
                          data=json.dumps(data),
                          content_type='application/json',
                          headers=admin_auth)
    
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['commission_amount'] == 30000.0  # %3
    assert json_data['commission_rate'] == 3.0
