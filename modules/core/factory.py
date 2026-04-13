import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_cors import CORS
from flask_compress import Compress
from flasgger import Swagger
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
import structlog
from dotenv import load_dotenv

from shared.extensions import db, cache, limiter, babel, csrf, socketio, migrate
import shared.models # Ensure all models are loaded
from shared.database import init_db, doldur_ornek_veriler

def create_app(init_database=False):
    load_dotenv()
    # Path adjustment for the new location (modules/core/)
    app = Flask(__name__, template_folder='../../pages', static_folder='../../static')
    
    # Configuration (Dynamic paths for local, CI, and Docker)
    DB_DIR = os.environ.get("DB_DIR", os.path.join(os.getcwd(), "data"))
    os.makedirs(DB_DIR, exist_ok=True)
    DB_NAME = os.path.join(DB_DIR, "imza_database.db")
    
    # Robust SQLAlchemy URI construction with strict validation
    db_env_url = os.environ.get("DATABASE_URL", "").strip()
    
    # If the URL is empty or looks like a placeholder (doesn't contain ://), use fallback
    if not db_env_url or "://" not in db_env_url:
        # Fallback to local SQLite with absolute path (guaranteed 4 slashes on Linux)
        abs_db_path = os.path.abspath(DB_NAME)
        # SQLite absolute paths on Linux: sqlite:////app/data/imza_database.db
        app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{abs_db_path}"
        app.logger.info(f"Using default SQLite path: {app.config['SQLALCHEMY_DATABASE_URI']}")
    else:
        # User provided an explicit valid-looking URL
        app.config['SQLALCHEMY_DATABASE_URI'] = db_env_url
        app.logger.info("Using DATABASE_URL from environment.")
        
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key")
    app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024 # Increased for portfolio media
    app.config['UPLOAD_FOLDER'] = 'uploads'
    
    # Sentry & Monitoring (Robust initialization to prevent app crash)
    sentry_dsn = os.getenv("SENTRY_DSN")
    if sentry_dsn and "your-dsn" not in sentry_dsn: # Ignore placeholders
        try:
            sentry_sdk.init(
                dsn=sentry_dsn,
                integrations=[FlaskIntegration()],
                traces_sample_rate=0.2,
                environment="production" if os.getenv("FLASK_DEBUG") == "False" else "development",
            )
            app.logger.info("Sentry başarıyla başlatıldı.")
        except Exception as e:
            app.logger.warning(f"Sentry başlatılamadı (Geçersiz DSN: {sentry_dsn}). Hata: {e}")
    else:
        app.logger.info("Sentry initialization skipped (DSN missing or placeholder).")

    # Logging (Dynamic logs directory)
    log_dir = os.environ.get("LOG_DIR", os.path.join(os.getcwd(), "logs"))
    os.makedirs(log_dir, exist_ok=True)
    handler = RotatingFileHandler(os.path.join(log_dir, "app.log"), maxBytes=5*1024*1024, backupCount=5)
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(os.getenv("LOG_LEVEL", "INFO"))

    # Updated CORS for the new structure
    CORS(app, resources={r"/api/*": {"origins": "*"}}) # Loosened for development, will harden in security phase
    Compress().init_app(app)
    
    @app.after_request
    def add_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        return response
    
    # Initialize Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)
    limiter.init_app(app)
    babel.init_app(app)
    csrf.init_app(app)
    socketio.init_app(app)
    
    # Swagger
    swagger_config = {
        "headers": [], "static_url_path": "/flasgger_static",
        "swagger_ui": True, "specs_route": "/api/docs",
        "specs": [{"endpoint": 'apispec_1', "route": '/apispec_1.json', "rule_filter": lambda rule: True, "model_filter": lambda tag: True}]
    }
    Swagger(app, config=swagger_config)

    # Register Blueprints from their updated modular paths
    from .routes import main_bp # Moved alongside factory
    from modules.auth.routes import auth_bp
    from modules.portfolio import portfolio_bp
    from modules.crm import crm_bp
    from modules.finance import finance_bp
    from modules.media import media_bp
    from modules.ai import ai_bp
    from modules.legal import legal_bp
    from modules.automation import automation_bp
    from modules.integration import integration_bp
    from modules.finance.contract_routes import contract_bp
    from modules.maintenance import maintenance_bp
    from modules.compass import compass_bp
    from modules.neighborhood import neighborhood_bp
    from modules.cms import cms_bp
    from modules.notification import notification_bp
    from modules.auth.service import setup_oauth
    
    setup_oauth(app)
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(portfolio_bp, url_prefix='/api/v1')
    app.register_blueprint(crm_bp, url_prefix='/api/v1')
    app.register_blueprint(finance_bp, url_prefix='/api/v1/finance')
    app.register_blueprint(neighborhood_bp, url_prefix='/api/neighborhood')
    app.register_blueprint(media_bp, url_prefix='/api/v1/media')
    app.register_blueprint(cms_bp, url_prefix='/api/v1/cms')
    app.register_blueprint(notification_bp, url_prefix='/api/v1/notices')
    app.register_blueprint(ai_bp, url_prefix='/api/v1/ai')
    app.register_blueprint(legal_bp, url_prefix='/api/v1/legal')
    app.register_blueprint(automation_bp, url_prefix='/api/v1/automation')
    app.register_blueprint(integration_bp, url_prefix='/api/v1/integration')
    app.register_blueprint(contract_bp, url_prefix='/api/v1/contracts')
    app.register_blueprint(maintenance_bp, url_prefix='/api/v1/maintenance')
    app.register_blueprint(compass_bp, url_prefix='/api/v1/compass')

    if init_database:
        with app.app_context():
            init_db()
            doldur_ornek_veriler()
        
    return app
