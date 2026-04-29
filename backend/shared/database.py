import sqlite3
import os
from contextlib import contextmanager
from flask import current_app

def get_db_path():
    # Attempt to get from config, fallback to default
    try:
        uri = current_app.config.get('SQLALCHEMY_DATABASE_URI', '')
        if 'sqlite:///' in uri:
            return uri.replace('sqlite:///', '')
    except:
        pass
    return os.path.join(os.getcwd(), "data", "imza_database.db")

@contextmanager
def get_db_connection():
    path = get_db_path()
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

@contextmanager
def get_db():
    """Alias for get_db_connection to match existing imports."""
    with get_db_connection() as conn:
        yield conn
