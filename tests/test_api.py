import pytest
import json

def test_health_check(client):
    """Test the newly added health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'

def test_security_headers(client):
    """Test if security headers are present in responses."""
    response = client.get('/health')
    assert response.headers['X-Content-Type-Options'] == 'nosniff'
    assert response.headers['X-Frame-Options'] == 'DENY'

def test_auth_protected_route(client):
    """Ensure sensitive routes return 401 without token."""
    response = client.get('/api/v1/leads')
    assert response.status_code == 401

def test_portfolio_listing_v1(client, admin_auth):
    """Test standard portfolio listing via v1 API."""
    response = client.get('/api/v1/portfolios', headers=admin_auth)
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_portfolio_validation_v1(client, admin_auth):
    """Test Marshmallow validation for portfolio creation in v1."""
    # Missing required field 'title' (standardized name)
    bad_data = {"ref_no": "TEST-1", "category": "Arsa"}
    response = client.post('/api/v1/portfolios', 
                           data=json.dumps(bad_data),
                           content_type='application/json',
                           headers=admin_auth)
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data or 'details' in data
