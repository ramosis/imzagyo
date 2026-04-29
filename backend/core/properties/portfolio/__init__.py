from flask import Blueprint

portfolio_bp = Blueprint(
    'portfolio',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/static/portfolio'
)

from . import routes
