from flask import Blueprint

automation_bp = Blueprint('automation', __name__)

from . import routes
from . import hr_routes
