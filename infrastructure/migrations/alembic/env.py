import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# Proje kökünü path'e ekle
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

# Flask uygulamasını ve db nesnesini import et
from backend.app.factory import create_app
from backend.app.extensions import db

# Tüm modelleri import et (Alembic'in tabloları görmesi için)
from backend.core.identity.auth.models import User
from backend.core.properties.portfolio.models import Property, PropertyImage
# Diğer modeller de buraya eklenmeli

# Alembic config
config = context.config

# Flask config'den DATABASE_URL al
app = create_app(os.getenv('FLASK_ENV', 'development'))
db_url = app.config.get('SQLALCHEMY_DATABASE_URI')
config.set_main_option('sqlalchemy.url', db_url)

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Target metadata
target_metadata = db.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
