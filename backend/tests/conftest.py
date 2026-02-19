from __future__ import annotations

import sys
from pathlib import Path
from typing import AsyncGenerator, AsyncIterator
from uuid import UUID, uuid4

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

# Task: T064 — stabilize backend test execution for async SQLite engine fixtures
_BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(_BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(_BACKEND_ROOT))

# Ensure metadata is fully populated before create_all/drop_all.
from src.models.task import Task  # noqa: F401
from src.models.user import User  # noqa: F401
from src.database import get_db_session
from src.main import app
from src.utils.token import create_token

_TEST_DATABASE_URL = "sqlite+aiosqlite://"


@pytest_asyncio.fixture(scope="function")
async def async_engine() -> AsyncIterator[AsyncEngine]:
    """
    Provide a self-contained async in-memory SQLite engine per test.

    - Uses StaticPool so all sessions in a test share the same in-memory DB.
    - Enables SQLite FK enforcement so ON DELETE CASCADE is exercised at runtime.
    """
    engine = create_async_engine(
        _TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    @event.listens_for(engine.sync_engine, "connect")
    def _enable_sqlite_fk(dbapi_connection, _connection_record) -> None:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    try:
        yield engine
    finally:
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.drop_all)
        await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def db_session(async_engine: AsyncEngine) -> AsyncIterator[AsyncSession]:
    """Create one async session bound to the test engine and close it safely."""
    session_factory = async_sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with session_factory() as session:
        try:
            yield session
        finally:
            if session.in_transaction():
                await session.rollback()


@pytest_asyncio.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create an async HTTP client with DB dependency override."""

    async def _override_db() -> AsyncGenerator[AsyncSession, None]:
        yield db_session

    app.dependency_overrides[get_db_session] = _override_db
    transport = ASGITransport(app=app)
    try:
        async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
            yield ac
    finally:
        app.dependency_overrides.pop(get_db_session, None)


def make_auth_header(user_id: str | None = None, email: str = "test@example.com") -> dict:
    """Generate a Bearer token header for a given (or random) user_id."""
    uid_str = user_id or str(uuid4())
    token = create_token(UUID(uid_str), email)
    return {"Authorization": f"Bearer {token}"}
