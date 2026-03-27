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
    
    # Legacy Blueprints
    from api.portfolio import portfolio_bp
    from api.contracts import contracts_bp
    from api.taxes import taxes_bp
    from api.maintenance import maintenance_bp
    from api.notifications import notifications_bp
    from api.ai import ai_bp
    from api.appointments import appointments_bp
    from api.finance import finance_bp
    from api.hero import hero_bp
    from api.contract_templates import contract_templates_bp
    from api.parties import parties_bp
    from api.leads import leads_bp
    from api.expenses import expenses_bp
    from api.social_auth import social_auth_bp
    from api.integrations import integrations_bp
    from api.documents import documents_bp
    from api.purchasing_power import purchasing_power_bp
    from api.settings import settings_bp
    from api.campaigns import campaigns_bp
    from api.hr import hr_bp
    from api.contacts import contacts_bp
    from api.tracking import tracking_bp
    from api.lmetrics import lmetrics_bp
    from api.neighborhood import neighborhood_bp
    from api.projects import projects_bp
    from api.pipeline import pipeline_bp
    from api.automation import automation_bp
    from api.media import media_bp
    from api.appraisal import appraisal_bp
    from api.inspection import inspection_bp
    from api.mls import mls_bp
    from api.compass import compass_bp
    from api.seo import seo_bp
    from api.verification import verification_bp
    from api.analytics import analytics_bp
    from api.valuation import valuation_bp
    from api.team import team_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')

    bps = [
        (portfolio_bp, 'portfolios'), (contracts_bp, 'contracts'), (taxes_bp, 'taxes'),
        (maintenance_bp, 'maintenance'), (notifications_bp, 'notifications'),
        (ai_bp, 'ai'), (appointments_bp, 'appointments'),
        (finance_bp, 'finance'), (hero_bp, 'hero'), 
        (contract_templates_bp, 'contracts/templates'), (parties_bp, 'parties'),
        (leads_bp, 'leads'), (expenses_bp, 'expenses'), (social_auth_bp, 'auth/social'),
        (integrations_bp, 'integrations'), (documents_bp, 'documents'),
        (purchasing_power_bp, 'purchasing-power'), (settings_bp, 'settings'),
        (campaigns_bp, 'campaigns'), (hr_bp, 'hr'), (contacts_bp, 'contacts'),
        (tracking_bp, 'tracking'), (lmetrics_bp, 'analytics/lmetrics'),
        (neighborhood_bp, 'neighborhoods'), (projects_bp, 'projects'),
        (pipeline_bp, 'pipeline'), (automation_bp, 'automation'),
        (media_bp, 'media'), (appraisal_bp, 'appraisal'),
        (inspection_bp, 'inspection'), (mls_bp, 'mls'), (compass_bp, 'compass'),
        (seo_bp, 'seo'), (verification_bp, 'verification'),
        (analytics_bp, 'analytics'), (valuation_bp, 'valuation'),
        (team_bp, 'team')
    ]
    for bp, prefix in bps:
        app.register_blueprint(bp, url_prefix=f'/api/v1/{prefix}')
    
    # Local File Serving (Legacy Fallback)
    @app.route('/uploads/<path:filename>')
    def serve_uploads(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    # Initialize DB
    with app.app_context():
        init_db()
        doldur_ornek_veriler()
        
    return app
