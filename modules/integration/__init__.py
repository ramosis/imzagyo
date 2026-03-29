from flask import Blueprint

integration_bp = Blueprint('integration', __name__)

from modules.integration import routes
