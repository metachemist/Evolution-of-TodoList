from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import AsyncGenerator, AsyncIterator, Iterator, Any
from uuid import UUID, uuid4

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

# Task: T064 — stabilize backend test execution for async SQLite engine fixtures
_BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(_BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(_BACKEND_ROOT))

# Keep tests hermetic: avoid external Redis usage from backend/.env.
# load_dotenv() in src.database uses override=False by default, so pre-setting
# an empty value here prevents loading backend/.env REDIS_URL during tests.
os.environ["REDIS_URL"] = ""
# Avoid domain-scoped cookies that won't be stored by httpx test client
# (base_url uses testserver, not localhost).
os.environ["COOKIE_DOMAIN"] = ""

# Ensure metadata is fully populated before create_all/drop_all.
from src.models.task import Task  # noqa: F401
from src.models.user import User  # noqa: F401
from src.database import get_db_session
from src.main import app
from src.utils.token import create_token

_TEST_DATABASE_URL = "sqlite://"


class AsyncSessionAdapter:
    """
    Async-shaped adapter over a sync SQLModel Session for tests.

    This keeps route/service signatures untouched (`await db.exec(...)`) while
    avoiding aiosqlite runtime instability in this environment.
    """

    def __init__(self, session: Session) -> None:
        self._session = session

    def __getattr__(self, item: str) -> Any:
        return getattr(self._session, item)

    async def exec(self, statement):
        return self._session.exec(statement)

    async def commit(self) -> None:
        self._session.commit()

    async def refresh(self, instance) -> None:
        self._session.refresh(instance)

    async def delete(self, instance) -> None:
        self._session.delete(instance)

    async def rollback(self) -> None:
        self._session.rollback()

    async def get(self, entity, ident):
        return self._session.get(entity, ident)


@pytest.fixture(scope="function")
def sync_engine() -> Iterator[Engine]:
    """
    Provide a self-contained in-memory SQLite engine per test.

    - Uses StaticPool so all sessions in a test share the same in-memory DB.
    - Enables SQLite FK enforcement so ON DELETE CASCADE is exercised at runtime.
    """
    engine = create_engine(
        _TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    @event.listens_for(engine, "connect")
    def _enable_sqlite_fk(dbapi_connection, _connection_record) -> None:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    SQLModel.metadata.create_all(engine)

    try:
        yield engine
    finally:
        SQLModel.metadata.drop_all(engine)
        engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def db_session(sync_engine: Engine) -> AsyncIterator[AsyncSessionAdapter]:
    """Create one async-shaped session wrapper bound to the test engine."""
    with Session(sync_engine) as session:
        adapter = AsyncSessionAdapter(session)
        try:
            yield adapter
        finally:
            if session.in_transaction():
                session.rollback()


@pytest_asyncio.fixture(scope="function")
async def client(db_session: AsyncSessionAdapter) -> AsyncGenerator[AsyncClient, None]:
    """Create an async HTTP client with DB dependency override."""

    async def _override_db() -> AsyncGenerator[AsyncSessionAdapter, None]:
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
