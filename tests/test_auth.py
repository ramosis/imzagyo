import pytest
import json
from api.auth import AuthService
from database import get_db

def test_login_success(client, app):
    """Test standard admin login."""
    response = client.post('/api/login', json={
        'username': 'admin',
        'password': 'admin123'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 'token' in data
    assert data['role'] == 'admin'

def test_login_invalid_credentials(client):
    """Test login with wrong password."""
    response = client.post('/api/login', json={
        'username': 'admin',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401
    assert 'error' in response.get_json()

def test_protected_route_no_token(client):
    """Test accessing protected route without JWT."""
    response = client.get('/api/portfoyler')
    # If using @require_permission, it should return 401/403
    # Portfolio list might be public, but let's check a protected one
    response = client.post('/api/portfoyler', json={})
    assert response.status_code in [401, 403]
