import asyncio
import os
from dotenv import load_dotenv
from logging.config import fileConfig

load_dotenv()
from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlalchemy import engine_from_config, pool
from alembic import context
from sqlmodel import SQLModel

# Import all models to ensure they're registered with SQLAlchemy
from src.models.user import User
from src.models.task import Task
from src.utils.db_url import normalize_asyncpg_database_url

# this is the Alembic Config object
config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set target metadata
target_metadata = SQLModel.metadata

# Task: T007 — Alembic environment configuration compatibility
# Normalize asyncpg URL query params (e.g., sslmode -> ssl) before engine creation.
raw_database_url = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost/todo_dev")
config.set_main_option("sqlalchemy.url", normalize_asyncpg_database_url(raw_database_url))


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


def do_run_migrations(connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Run migrations using an async engine."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_sync_migrations() -> None:
    """Run migrations using a synchronous engine (used for sqlite:/// URLs)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        do_run_migrations(connection)

    connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    url = config.get_main_option("sqlalchemy.url")
    if url.startswith("sqlite:///"):
        run_sync_migrations()
        return
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
