from flask import Blueprint

contracts_bp = Blueprint('contracts', __name__)

from modules.contracts import routes
