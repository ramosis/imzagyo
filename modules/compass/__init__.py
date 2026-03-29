from flask import Blueprint

compass_bp = Blueprint('compass', __name__)

from . import routes
