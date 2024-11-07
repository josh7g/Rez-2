from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import os
import sys
from dotenv import load_dotenv

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Import the models
from models import db

# this is the Alembic Config object
config = context.config

# Setup logging
if config.config_file_name is not None:
    try:
        fileConfig(config.config_file_name)
    except Exception as e:
        print(f"Warning: Error configuring logging: {e}")
        import logging
        logging.basicConfig(level=logging.INFO)

# Set SQLAlchemy URL
config.set_main_option('sqlalchemy.url', os.getenv('DATABASE_URL', '').replace('postgres://', 'postgresql://'))

# Add model's MetaData object
target_metadata = db.metadata

def run_migrations_offline() -> None:
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

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # Handle the database URL
    configuration = config.get_section(config.config_ini_section)
    if not configuration:
        configuration = {}
    configuration["sqlalchemy.url"] = config.get_main_option("sqlalchemy.url")

    connectable = engine_from_config(
        configuration,
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