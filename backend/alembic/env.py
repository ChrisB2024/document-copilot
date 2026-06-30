"""
This file is meant to be the bridge between Alembic, your app settings,
your sqlalchemy models, and the real Supabase Postgres database.
"""

from logging.config import fileConfig

from sqlalchemy import create_engine, pool

from alembic import context

from app.config import settings
from app.database.models import Base

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

# return the DB connection string Alembic should use
def get_database_url() -> str:
    return settings.sqlalchemy_database_url

# configure Alembic without opening a real DB connection
def run_migrations_offline() -> None:
    context.configure(
        url=get_database_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()

# connect to the actual database and apply or inspect migrations
def run_migrations_online() -> None:
    connectable = create_engine(
        get_database_url(),
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
