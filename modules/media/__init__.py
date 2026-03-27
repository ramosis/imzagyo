from flask import Blueprint

media_bp = Blueprint('media', __name__)

from . import routes
from . import document_routes
