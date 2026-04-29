import os
import logging
from flask import Flask
from .extensions import db, migrate, cache, limiter, babel, csrf, socketio, login_manager
from .config import config_by_name

def create_app(config_name="dev"):
    # Point to frontend directory relative to this file
    # backend/app/factory.py -> backend/app -> backend -> root -> frontend
    app = Flask(__name__, 
                template_folder='../../frontend/pages',
                static_folder='../../frontend/static')
    
    # Load configuration
    app.config.from_object(config_by_name[config_name])
    
    # Initialize Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)
    limiter.init_app(app)
    babel.init_app(app)
    csrf.init_app(app)
    socketio.init_app(app)
    login_manager.init_app(app)
    
    # 🧱 REGISTER CORE MODULES
    register_core_modules(app)
    
    # ⭐ REGISTER ADDONS
    enabled_addons = os.environ.get("ENABLED_ADDONS", "ai,legal,mobile").split(",")
    register_addons(app, enabled_addons)
    
    return app

def register_core_modules(app):
    from .routes import main_bp
    app.register_blueprint(main_bp)

    """Core modules that are essential for the system."""
    from backend.core.identity.auth import auth_bp
    from backend.core.properties.portfolio import portfolio_bp
    from backend.core.sales.crm import crm_bp
    from backend.core.sales.finance import finance_bp
    from backend.core.neighborhood import neighborhood_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(portfolio_bp)
    app.register_blueprint(crm_bp, url_prefix='/crm')
    app.register_blueprint(finance_bp, url_prefix='/finance')
    app.register_blueprint(neighborhood_bp, url_prefix='/neighborhood')

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

