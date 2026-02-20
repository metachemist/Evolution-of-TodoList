from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import AsyncGenerator
import os
from dotenv import load_dotenv

from src.utils.db_url import normalize_asyncpg_database_url


# Task: T006 — Async SQLAlchemy DB configuration for PostgreSQL/Neon
# Load backend/.env for local development so uvicorn picks up DATABASE_URL/SECRET_KEY.
load_dotenv()

# Get database URL from environment, with a default for development.
DATABASE_URL = normalize_asyncpg_database_url(
    os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost/todo_dev")
)

# Safe engine defaults for long-lived runtime stability.
_ENGINE_KWARGS: dict = {
    "pool_pre_ping": True,
    "pool_recycle": int(os.getenv("DB_POOL_RECYCLE_SECONDS", "1800")),
}

if not DATABASE_URL.startswith("sqlite"):
    _ENGINE_KWARGS.update(
        {
            "pool_size": int(os.getenv("DB_POOL_SIZE", "5")),
            "max_overflow": int(os.getenv("DB_MAX_OVERFLOW", "10")),
            "pool_timeout": int(os.getenv("DB_POOL_TIMEOUT_SECONDS", "30")),
        }
    )

# Create async engine
async_engine = create_async_engine(DATABASE_URL, **_ENGINE_KWARGS)

# Create async session maker
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency function that provides database sessions.
    """
    async with AsyncSessionLocal() as session:
        yield session
