from flask import Blueprint

legal_bp = Blueprint('legal', __name__)

from . import routes
from . import party_routes
from . import inspection_routes
