import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
    
    # DB Configuration
    db_env_url = os.environ.get("DATABASE_URL", "").strip()
    if db_env_url and "://" in db_env_url:
        SQLALCHEMY_DATABASE_URI = db_env_url
    else:
        # Fallback to local SQLite
        db_path = os.path.join(os.getcwd(), "data", "imza_database.db")
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.abspath(db_path)}"

class ProductionConfig(Config):
    FLASK_DEBUG = False

class DevelopmentConfig(Config):
    FLASK_DEBUG = True

config_by_name = {
    "dev": DevelopmentConfig,
    "prod": ProductionConfig
}
