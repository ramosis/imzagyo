from flask import Blueprint

finance_bp = Blueprint('finance', __name__)

from . import routes
from . import expense_routes
from . import tax_routes
