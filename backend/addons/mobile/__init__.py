from flask import Blueprint

mobile_bp = Blueprint(
    \'mobile_api\',
    __name__,
    template_folder=\'templates\',
    static_folder=\'static\',
    static_url_path=\'/static/mobile_api\'
)

from . import routes
