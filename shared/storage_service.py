import os
import sqlite3
from typing import Optional

# Path to the SQLite database (same as shared.database uses)
DB_URL = os.environ.get('DATABASE_URL', 'data/imza_database.db')
DB_NAME = DB_URL.replace('sqlite:///', '').replace('sqlite://', '')

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

class BaseProvider:
    """Abstract base class for storage providers."""
    def save(self, file_storage, destination_path: str) -> str:
        raise NotImplementedError

    def url(self, stored_path: str) -> str:
        raise NotImplementedError

class LocalProvider(BaseProvider):
    """Stores files on the local filesystem under a configured upload directory."""
    def __init__(self, base_path: str):
        self.base_path = base_path
        os.makedirs(self.base_path, exist_ok=True)

    def save(self, file_storage, destination_path: str) -> str:
        """Save an uploaded file (Werkzeug FileStorage) to the local path.
        Returns the relative path that can be used to serve the file.
        """
        full_path = os.path.join(self.base_path, destination_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        file_storage.save(full_path)
        return os.path.relpath(full_path, start=os.getcwd())

    def url(self, stored_path: str) -> str:
        return f"/static/{stored_path.replace(os.sep, '/')}"

class StorageManager:
    """Facade that selects the appropriate provider based on system settings."""
    def __init__(self):
        self._provider = None
        self._load_provider()

    def _load_provider(self):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT value FROM system_settings WHERE key='storage_provider'")
        row = cur.fetchone()
        provider = row['value'] if row else 'local'
        if provider == 'local':
            cur.execute("SELECT value FROM system_settings WHERE key='upload_path'")
            upload_row = cur.fetchone()
            upload_path = upload_row['value'] if upload_row else 'static/uploads/contracts'
            self._provider = LocalProvider(base_path=upload_path)
        else:
            raise NotImplementedError(f"Storage provider '{provider}' is not implemented yet.")
        conn.close()

    @property
    def provider(self) -> BaseProvider:
        return self._provider

    def save_file(self, file_storage, sub_path: str) -> str:
        return self.provider.save(file_storage, sub_path)

    def file_url(self, stored_path: str) -> str:
        return self.provider.url(stored_path)
