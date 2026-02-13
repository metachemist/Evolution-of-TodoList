import pytest
from uuid import uuid4

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from httpx import ASGITransport, AsyncClient

from src.main import app
from src.database import get_db_session
from src.utils.auth import create_access_token


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def async_engine():
    """Create an async in-memory SQLite engine for testing."""
    engine = create_async_engine(
        "sqlite+aiosqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
    await engine.dispose()


@pytest.fixture
async def db_session(async_engine):
    """Create an async database session for testing."""
    async_session = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session


@pytest.fixture
async def client(db_session):
    """Create an async test client with overridden DB dependency."""

    async def _override_db():
        yield db_session

    app.dependency_overrides[get_db_session] = _override_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac
    app.dependency_overrides.clear()


def make_auth_header(user_id: str | None = None) -> dict:
    """Generate a Bearer token header for a given (or random) user_id."""
    uid = user_id or str(uuid4())
    token = create_access_token(data={"sub": uid})
    return {"Authorization": f"Bearer {token}"}


def make_auth_cookie(user_id: str | None = None) -> dict:
    """Generate an auth cookie dict for a given (or random) user_id."""
    uid = user_id or str(uuid4())
    token = create_access_token(data={"sub": uid})
    return {"access_token": token}
