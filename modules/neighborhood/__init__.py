from flask import Blueprint

neighborhood_bp = Blueprint('neighborhood', __name__)

from . import routes
