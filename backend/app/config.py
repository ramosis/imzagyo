import os
from dotenv import load_dotenv

# .env dosyasını yükle
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '../../infrastructure/config/.env'))

class Config:
    """Base config."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///data/imza_database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Domain'ler
    INVESTMENT_DOMAIN = os.getenv('INVESTMENT_DOMAIN', 'localhost:5000')
    NEIGHBORHOOD_DOMAIN = os.getenv('NEIGHBORHOOD_DOMAIN', 'localhost:5000')
    
    # Addon'lar
    ENABLED_ADDONS = os.getenv('ENABLED_ADDONS', '').split(',')
    
    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-dev-secret')
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600))
    
    # Upload
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

class DevelopmentConfig(Config):
    """Development config."""
    DEBUG = True
    TESTING = False

class StagingConfig(Config):
    """Staging config."""
    DEBUG = False
    TESTING = False
    # Staging-specific settings

class ProductionConfig(Config):
    """Production config."""
    DEBUG = False
    TESTING = False
    
    # Security headers
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Strict CORS
    CORS_ORIGINS = [
        'https://imzaemlak.com',
        'https://www.imzaemlak.com',
        'https://imzamahalle.com',
        'https://www.imzamahalle.com'
    ]

config_map = {
    'development': DevelopmentConfig,
    'staging': StagingConfig,
    'production': ProductionConfig
}
