from flask import Blueprint

finance_bp = Blueprint(
    'finance',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/static/finance'
)

from . import routes
