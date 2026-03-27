import pytest
import json

def test_create_and_get_portfolio_v1(client, admin_auth):
    """Test full cycle of creating and retrieving a portfolio via V1 API (Standardized)."""
    new_portfolio = {
        "ref_no": "LUX-999",
        "title": "Bozüyük Luxury Villa",
        "listing_category": "Satılık",
        "category": "Konut",
        "price": 15000000.0,
        "location": "Bozüyük, Bilecik",
        "rooms": "5+2",
        "area": "450 m²"
    }
    
    # 1. Create
    res_post = client.post('/api/v1/portfolios', 
                           data=json.dumps(new_portfolio),
                           content_type='application/json',
                           headers=admin_auth)
    assert res_post.status_code == 201
    created_id = res_post.get_json()['id']
    
    # 2. Get
    res_get = client.get(f'/api/v1/portfolios/{created_id}', headers=admin_auth)
    assert res_get.status_code == 200
    data = res_get.get_json()
    assert data['title'] == "Bozüyük Luxury Villa"
    assert data['price'] == 15000000.0

def test_get_portfolios(client):
    """Test listing portfolios."""
    response = client.get('/api/portfoyler')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)
