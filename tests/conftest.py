import pytest
from backend.app.factory import create_app
from backend.app.extensions import db

@pytest.fixture
def app():
    """Create application for testing."""
    app = create_app('testing')
    
    # Test config overrides
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """Test client."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """CLI test runner."""
    return app.test_cli_runner()

@pytest.fixture
def auth_headers(client):
    """Get auth token for tests."""
    # Create test user and login
    # Note: This requires a registered user. In a real scenario, you'd create one here.
    # For now, this is a placeholder based on your template.
    try:
        response = client.post('/api/v1/auth/login', json={
            'email': 'test@imza.com',
            'password': 'testpass123'
        })
        token = response.json.get('access_token')
        return {'Authorization': f'Bearer {token}'} if token else {}
    except:
        return {}
