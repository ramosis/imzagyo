from flask import Blueprint

ai_bp = Blueprint(
    \'ai\',
    __name__,
    template_folder=\'templates\',
    static_folder=\'static\',
    static_url_path=\'/static/ai\'
)

from . import routes
