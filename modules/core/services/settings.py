from modules.core.models import SystemSetting
from shared.extensions import db

class SettingsService:
    """Central service for managing system-wide dynamic settings."""

    _cache = {}

    @staticmethod
    def get(key: str, default=None):
        """Retrieves a setting value by key with in-memory caching."""
        if key in SettingsService._cache:
            return SettingsService._cache[key]
            
        try:
            setting = SystemSetting.query.filter_by(key=key).first()
            val = setting.value if setting else default
            SettingsService._cache[key] = val
            return val
        except Exception as e:
            print(f"ERROR: Could not fetch setting ({key}): {e}")
            return default

    @staticmethod
    def set(key: str, value, category: str = 'general'):
        """Updates or creates a setting and invalidates cache."""
        try:
            setting = SystemSetting.query.filter_by(key=key).first()
            if setting:
                setting.value = str(value)
            else:
                setting = SystemSetting(key=key, value=str(value), category=category)
                db.session.add(setting)
            db.session.commit()
            # Clear cache to reflect change in next get()
            if key in SettingsService._cache:
                del SettingsService._cache[key]
            return True
        except Exception as e:
            db.session.rollback()
            print(f"ERROR: Could not save setting ({key}): {e}")
            return False
