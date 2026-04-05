from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from flask_babel import Babel
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO
import os

# Initialize extensions without app
# Disabled Redis message queue for now due to infrastructure lack in docker-compose.yml
# Use 'gevent' to match Gunicorn worker class for maximum stability
socketio = SocketIO(cors_allowed_origins="*", async_mode='gevent')
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["10000 per day", "100 per minute"],
    storage_uri="memory://"
)

cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
babel = Babel()
csrf = CSRFProtect()
db = SQLAlchemy()
migrate = Migrate()
