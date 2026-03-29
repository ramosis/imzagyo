from flask import Blueprint

crm_bp = Blueprint('crm', __name__)

from . import lead_routes
from . import pipeline_routes
from . import appointment_routes
from . import contact_routes
