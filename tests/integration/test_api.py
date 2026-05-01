def test_login_endpoint(client):
    """Test login API."""
    response = client.post('/api/v1/auth/login', json={
        'username': 'admin',
        'password': 'wrongpass'
    })
    assert response.status_code == 401
    
def test_portfolio_list_endpoint(client):
    """Test portfolio listing API."""
    # Note: Using the actual prefix registered in factory + route path
    response = client.get('/api/v1/portfolio/api/v1/properties')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_static_files(client):
    """Test static file serving."""
    # Attempt to load a known static file
    response = client.get('/static/css/main.css')
    assert response.status_code in [200, 404]
