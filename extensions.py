from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from flask_babel import Babel
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
import os

# Initialize extensions without app
socketio = SocketIO(cors_allowed_origins="*", message_queue=os.getenv("REDIS_URL", "redis://localhost:6379/0"))
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["10000 per day", "2000 per hour"],
    storage_uri="memory://"
)

cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
babel = Babel()
csrf = CSRFProtect()
db = SQLAlchemy()
