from modules.core.models import SystemSetting
from shared.extensions import db

class SettingsService:
    """Central service for managing system-wide dynamic settings."""

    @staticmethod
    def get(key: str, default=None):
        """Retrieves a setting value by key."""
        try:
            setting = SystemSetting.query.filter_by(key=key).first()
            return setting.value if setting else default
        except Exception as e:
            print(f"ERROR: Could not fetch setting ({key}): {e}")
            return default

    @staticmethod
    def set(key: str, value, category: str = 'general'):
        """Updates or creates a setting."""
        try:
            setting = SystemSetting.query.filter_by(key=key).first()
            if setting:
                setting.value = str(value)
            else:
                setting = SystemSetting(key=key, value=str(value), category=category)
                db.session.add(setting)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"ERROR: Could not save setting ({key}): {e}")
            return False
