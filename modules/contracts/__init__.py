from flask import Blueprint

contracts_bp = Blueprint('contracts', __name__)

# Import routes to register them with the blueprint
from . import routes
