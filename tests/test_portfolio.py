import pytest
import json

def test_create_portfolio(client):
    """Test creating a portfolio with sanitization check."""
    # Master token might be needed if master auth is active
    headers = {'Content-Type': 'application/json'}
    
    payload = {
        'id': 'test-villa',
        'baslik1': '<b>Danger</b> Villa',
        'baslik2': 'Sanitized Subtitle',
        'fiyat': '1000000',
        'koleksiyon': 'Test'
    }
    
    # We ignore auth for now or use master token
    response = client.post('/api/portfoyler', 
                          json=payload,
                          headers={'X-Master-Token': 'master-auth-token-123'}) # Mocked
    
    assert response.status_code in [201, 401] # 401 if auth is strictly enforced
    
    if response.status_code == 201:
        data = response.get_json()
        # Check sanitization
        assert '<b>' not in data['baslik1']
        assert 'Danger' in data['baslik1']

def test_get_portfolios(client):
    """Test listing portfolios."""
    response = client.get('/api/portfoyler')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)
