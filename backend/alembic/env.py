from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from sqlalchemy.engine.url import make_url

from alembic import context
from app.core.config import settings
from app.models.user import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here for 'autogenerate' support
target_metadata = Base.metadata


def get_sync_database_url() -> str:
    """Convert async database URL to sync URL for Alembic."""
    url = make_url(settings.DATABASE_URL)
    sync_driver = (
        url.drivername.replace("+asyncpg", "+psycopg2").replace("+aiosqlite", "")
    )
    return str(url.set(drivername=sync_driver))


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = get_sync_database_url()
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
    sync_url = get_sync_database_url()
    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = sync_url

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
