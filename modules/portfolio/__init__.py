from flask import Blueprint

portfolio_bp = Blueprint('portfolio', __name__)

# Import routes to register them with the blueprint
# These will be imported inside the factory or here
from . import routes
from . import hero_routes
from . import project_routes
from . import neighborhood_routes
