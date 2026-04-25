from flask import Blueprint
import os

# Define the Identity (Auth) Blueprint
# It has its own templates and static folders for isolation
identity_bp = Blueprint(
    'identity', 
    __name__,
    template_folder='templates',
    static_folder='static',
    url_prefix='/api/v1/auth'
)

from . import routes
