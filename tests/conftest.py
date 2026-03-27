import pytest
import os
import tempfile

@pytest.fixture
def app():
    # Setup environment for tests
    os.environ['JWT_SECRET'] = 'test-jwt-secret'
    os.environ['FLASK_SECRET_KEY'] = 'test-flask-secret'
    os.environ['FLASK_DEBUG'] = 'True'

    # Setup temporary database
    db_fd, db_path = tempfile.mkstemp()
    
    # LATE IMPORTS to ensure DB_NAME can be overridden
    from shared import database
    database.DB_NAME = db_path
    
    from app.factory import create_app
    app = create_app()
    app.config['TESTING'] = True
    app.config['DEBUG'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    app.config['WTF_CSRF_ENABLED'] = False

    with app.app_context():
        # init_db() and doldur_ornek_veriler() are already called in create_app()
        # No need to seed manually here, as it causes IntegrityError
        yield app

    # Teardown
    os.close(db_fd)
    if os.path.exists(db_path):
        os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def admin_auth(app):
    import jwt
    import datetime
    from modules.auth.service import JWT_SECRET
    
    payload = {
        'user_id': 1,
        'username': 'admin',
        'role': 'admin',
        'circle': 'inner',
        'app_route': 'both',
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, JWT_SECRET or 'test-jwt-secret', algorithm="HS256")
    return {'Authorization': f'Bearer {token}'}
