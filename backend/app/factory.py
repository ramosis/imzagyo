import os
import logging
import sentry_sdk
import structlog
from flask import Flask, jsonify
from sentry_sdk.integrations.flask import FlaskIntegration
from .extensions import db, migrate, cache, limiter, babel, csrf, socketio, login_manager, compress
from .config import config_map

from backend.shared.services.logger import configure_logging

def create_app(config_name='development'):
    config_class = config_map.get(config_name, config_map['development'])
    
    # Configure logging
    configure_logging()
    
    # Sentry Initialization (Production only)
    if config_name == 'production' and os.getenv('SENTRY_DSN'):
        sentry_sdk.init(
            dsn=os.getenv('SENTRY_DSN'),
            integrations=[FlaskIntegration()],
            traces_sample_rate=0.1,
            environment=config_name
        )

    app = Flask(__name__, 
                template_folder='../../frontend/pages',
                static_folder='../../frontend/static')
    
    # Load configuration
    app.config.from_object(config_class)
    
    # Initialize Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)
    limiter.init_app(app)
    babel.init_app(app)
    csrf.init_app(app)
    socketio.init_app(app)
    login_manager.init_app(app)
    compress.init_app(app)
    
    @app.after_request
    def add_cache_headers(response):
        """Add cache headers for static files."""
        if request.path.startswith('/static/'):
            # CSS/JS: 1 hafta cache
            if request.path.endswith(('.css', '.js')):
                response.headers['Cache-Control'] = 'public, max-age=604800'
            # Images: 1 ay cache
            elif request.path.endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg')):
                response.headers['Cache-Control'] = 'public, max-age=2592000'
        return response

    # Error Handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Internal server error"}), 500
    
    # 🧱 REGISTER CORE MODULES
    register_core_modules(app)
    
    # ⭐ REGISTER ADDONS
    enabled_addons = os.environ.get("ENABLED_ADDONS", "ai,legal,mobile").split(",")
    register_addons(app, enabled_addons)
    
    return app

def register_core_modules(app):
    from .routes import main_bp
    from backend.core.identity.auth import auth_bp
    from backend.core.properties.portfolio import portfolio_bp
    from backend.core.sales.crm import crm_bp
    from backend.core.sales.finance import finance_bp
    from backend.core.neighborhood import neighborhood_bp
    from backend.core.sales.marketing import marketing_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(portfolio_bp, url_prefix='/api/v1/portfolio')
    app.register_blueprint(crm_bp, url_prefix='/api/v1/crm')
    app.register_blueprint(finance_bp, url_prefix='/api/v1/finance')
    app.register_blueprint(neighborhood_bp, url_prefix='/api/v1/neighborhood')
    app.register_blueprint(marketing_bp, url_prefix='/api/v1/marketing')

def register_addons(app, enabled_addons):
    """Dynamic addon loading based on configuration."""
    for addon in enabled_addons:
        addon = addon.strip()
        if not addon: continue
        
        try:
            if addon == 'ai':
                from backend.addons.ai import ai_bp
                app.register_blueprint(ai_bp, url_prefix='/ai')
            elif addon == 'legal':
                from backend.addons.legal import legal_bp
                app.register_blueprint(legal_bp, url_prefix='/legal')
            elif addon == 'mobile':
                from backend.addons.mobile import mobile_bp
                app.register_blueprint(mobile_bp, url_prefix='/mobile')
        except ImportError as e:
            app.logger.error(f"Failed to load addon {addon}: {e}")
