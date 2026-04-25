from flask import Blueprint

properties_bp = Blueprint(
    'properties', 
    __name__,
    template_folder='templates',
    static_folder='static',
    url_prefix='/api/v1/properties'
)

from . import routes
