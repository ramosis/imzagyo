import pytest
import os
import tempfile
from app import app as flask_app
from database import init_db, DB_NAME

@pytest.fixture
def app():
    # Setup temporary database
    db_fd, db_path = tempfile.mkstemp()
    flask_app.config['TESTING'] = True
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    flask_app.config['WTF_CSRF_ENABLED'] = False # Disable CSRF for easier testing

    with flask_app.app_context():
        # Override the global DB_NAME in database module if possible
        import database
        original_db = database.DB_NAME
        database.DB_NAME = db_path
        init_db()
        yield flask_app
        database.DB_NAME = original_db

    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def auth_header(client):
    """Helper to get a valid JWT header."""
    # This would call login or use a master token
    return {'Authorization': 'Bearer master-test-token-if-configured'}
