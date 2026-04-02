import os
from flask import current_app
from shared.extensions import db
from modules.core.services.settings import SettingsService
from modules.auth.models import User

# Re-exporting for backward compatibility during migration
def get_setting(key, default=None):
    return SettingsService.get(key, default)

def set_setting(key, value, category='general'):
    return SettingsService.set(key, value, category)

def init_db():
    """Unified Database Initialization: Using SQLAlchemy ORM."""
    # Core Table Creation
    db.create_all()
    
    # Admin Seeding
    try:
        from modules.auth.service import AuthService
        if not User.query.filter_by(username='admin').first():
            hashed_pw = AuthService.hash_password('admin123')
            admin = User(
                username='admin', 
                password_hash=hashed_pw, 
                role='super_admin', 
                is_admin=True,
                email_verified=True
            )
            db.session.add(admin)
            db.session.commit()
            print("INFO: Initial admin user created successfully.")
    except Exception as e:
        db.session.rollback()
        print(f"WARNING: Could not seed admin user: {e}")

def doldur_ornek_veriler():
    """Sample data loader - can be expanded as needed."""
    if os.environ.get("FLASK_DEBUG") == "True":
        # Placeholder for future sample data (listings, neighborhoods, etc.)
        pass

# Legacy sqlite3 helpers (Keeping for strict backward compatibility where ORM is not yet fully used)
import sqlite3
DB_URL = os.environ.get("DATABASE_URL", "/app/data/imza_database.db")
DB_NAME = DB_URL.replace("sqlite://", "").lstrip("/")
if "/app/" in DB_URL or DB_URL.startswith("sqlite:////"):
    DB_NAME = "/" + DB_NAME

def get_db_connection():
    if DB_NAME != ":memory:":
        os.makedirs(os.path.dirname(DB_NAME), exist_ok=True)
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

from contextlib import contextmanager
@contextmanager
def get_db():
    conn = get_db_connection()
    try:
        yield conn
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()
