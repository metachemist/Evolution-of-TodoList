# Task: T006 — Async SQLAlchemy DB configuration for PostgreSQL/Neon
# Task: T007 — Alembic environment configuration compatibility
from sqlalchemy.engine import make_url

from src.utils.db_url import normalize_asyncpg_database_url


def test_normalize_asyncpg_database_url_maps_sslmode_to_ssl() -> None:
    raw_url = "postgresql+asyncpg://user:pass@db.example.com/todo?sslmode=require"

    normalized_url = normalize_asyncpg_database_url(raw_url)
    parsed_url = make_url(normalized_url)

    assert parsed_url.query.get("ssl") == "require"
    assert "sslmode" not in parsed_url.query


def test_normalize_asyncpg_database_url_leaves_other_drivers_unchanged() -> None:
    raw_url = "postgresql+psycopg://user:pass@db.example.com/todo?sslmode=require"

    normalized_url = normalize_asyncpg_database_url(raw_url)

    assert normalized_url == raw_url
