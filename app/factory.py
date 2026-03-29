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

from shared.extensions import db, cache, limiter, babel, csrf, socketio
from shared.database import init_db, doldur_ornek_veriler

def create_app():
    app = Flask(__name__, template_folder='../pages', static_folder='../static')
    
    # Configuration
    DB_NAME = "data/imza_database.db"
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key")
    app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
    app.config['UPLOAD_FOLDER'] = 'uploads'
    
    # Sentry & Monitoring
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN"),
        integrations=[FlaskIntegration()],
        traces_sample_rate=0.2,
        environment="production" if os.getenv("FLASK_DEBUG") == "False" else "development",
    )

    # Logging
    log_dir = os.path.join(app.root_path, "..", "logs")
    os.makedirs(log_dir, exist_ok=True)
    handler = RotatingFileHandler(os.path.join(log_dir, "app.log"), maxBytes=5*1024*1024, backupCount=5)
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(os.getenv("LOG_LEVEL", "INFO"))

    # CORS & Middleware
    CORS(app, resources={r"/api/*": {"origins": ["https://imzagyo.com"]}})
    Compress().init_app(app)
    
    # Initialize Extensions
    db.init_app(app)
    cache.init_app(app)
    limiter.init_app(app)
    babel.init_app(app)
    csrf.init_app(app)
    # socketio.init_app(app) # Initialized via shared/extensions.py
    
    # Swagger
    swagger_config = {
        "headers": [], "static_url_path": "/flasgger_static",
        "swagger_ui": True, "specs_route": "/api/docs",
        "specs": [{"endpoint": 'apispec_1', "route": '/apispec_1.json', "rule_filter": lambda rule: True, "model_filter": lambda tag: True}]
    }
    Swagger(app, config=swagger_config)

    # Register Blueprints
    from app.routes import main_bp
    from modules.auth.routes import auth_bp
    from modules.portfolio import portfolio_bp
    from modules.crm import crm_bp
    from modules.finance import finance_bp
    from modules.media import media_bp
    from modules.ai import ai_bp
    from modules.legal import legal_bp
    from modules.automation import automation_bp
    from modules.integration import integration_bp
    from modules.contracts.routes import contracts_bp
    from modules.maintenance import maintenance_bp
    from modules.compass import compass_bp
    from modules.finance.tax_routes import finance_tax_bp
    from modules.auth.service import setup_oauth
    
    setup_oauth(app)
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(portfolio_bp, url_prefix='/api/v1') # Routes: /portfolios, /hero
    app.register_blueprint(crm_bp, url_prefix='/api/v1') # Routes: /leads, /pipeline
    app.register_blueprint(finance_bp, url_prefix='/api/v1/finance')
    app.register_blueprint(media_bp, url_prefix='/api/v1/media')
    app.register_blueprint(ai_bp, url_prefix='/api/v1/ai')
    app.register_blueprint(legal_bp, url_prefix='/api/v1/legal')
    app.register_blueprint(automation_bp, url_prefix='/api/v1/automation')
    app.register_blueprint(integration_bp, url_prefix='/api/v1/integration')
    app.register_blueprint(contracts_bp, url_prefix='/api/v1/contracts')
    app.register_blueprint(maintenance_bp, url_prefix='/api/v1/maintenance')
    app.register_blueprint(compass_bp, url_prefix='/api/v1/compass')
    app.register_blueprint(finance_tax_bp, url_prefix='/api/v1/finance/tax')
    
    # Local File Serving (Legacy Fallback)
    @app.route('/uploads/<path:filename>')
    def serve_uploads(filename):
        from flask import send_from_directory
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    # Initialize DB
    with app.app_context():
        init_db()
        doldur_ornek_veriler()
        
    return app
