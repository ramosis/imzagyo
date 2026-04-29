from flask import Blueprint

crm_bp = Blueprint(
    'crm',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/static/crm'
)

from . import routes
