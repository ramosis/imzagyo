import os
import logging
from flask import Flask
from .extensions import db, migrate, cache, limiter, babel, csrf, socketio, login_manager
from .config import config_by_name

def create_app(config_name="dev"):
    app = Flask(__name__)
    
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
    
    # 🧱 REGISTER CORE MODULES (Always active)
    # These will be moved to backend.core in Step 3
    # For now, we'll keep the registration logic flexible
    register_core_modules(app)
    
    # ⭐ REGISTER ADDONS (Optional/Dynamic)
    enabled_addons = os.environ.get("ENABLED_ADDONS", "ai,compass,media").split(",")
    register_addons(app, enabled_addons)
    
    return app

def register_core_modules(app):
    """Core modules that are essential for the system."""
    # Placeholder for Step 3 moves
    pass

def register_addons(app, enabled_addons):
    """Dynamic addon loading based on configuration."""
    for addon in enabled_addons:
        addon = addon.strip()
        if not addon: continue
        # Example: try to import and register blueprint
        # We will implement the actual import logic in Step 4
        pass
