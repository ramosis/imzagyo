# wsgi.py (production)
from backend.app.factory import create_app
application = create_app('production')
