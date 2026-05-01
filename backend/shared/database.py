from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import os
from contextlib import contextmanager

# DATABASE_URL ortam değişkeninden al
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///data/imza_database.db')

# Engine oluştur (PostgreSQL için pool ayarları)
if DATABASE_URL.startswith('postgresql'):
    engine = create_engine(
        DATABASE_URL,
        pool_size=10,
        max_overflow=20,
        pool_timeout=30,
        pool_recycle=1800,
        echo=False
    )
else:
    # SQLite (development fallback)
    engine = create_engine(
        DATABASE_URL,
        connect_args={'check_same_thread': False}
    )

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Scoped session (thread-safe)
db_session = scoped_session(SessionLocal)

# Base class
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)

@contextmanager
def get_db_connection():
    """Context manager for database sessions."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_db():
    """Alias for get_db_connection to match existing imports."""
    with get_db_connection() as db:
        yield db
