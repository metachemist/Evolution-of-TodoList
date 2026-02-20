# Task: T006 — Async SQLAlchemy DB configuration for PostgreSQL/Neon
# Task: T007 — Alembic environment configuration compatibility
# Spec: @specs/1-specify/phase-2/feature-03-auth-db-monorepo.md (FR-018)
from sqlalchemy.engine import make_url
from sqlalchemy.exc import ArgumentError


def normalize_asyncpg_database_url(database_url: str) -> str:
    """
    Normalize asyncpg URLs so common Neon DSNs work with SQLAlchemy asyncpg.

    asyncpg accepts `ssl=...`, while many hosted providers/documentation snippets
    provide `sslmode=...`. SQLAlchemy forwards query params to asyncpg.connect()
    as kwargs, so we rewrite sslmode->ssl for asyncpg driver URLs.
    """
    try:
        parsed_url = make_url(database_url)
    except ArgumentError:
        return database_url

    if parsed_url.drivername != "postgresql+asyncpg":
        return database_url

    query = dict(parsed_url.query)
    sslmode = query.get("sslmode")
    if sslmode and "ssl" not in query:
        query["ssl"] = sslmode
        query.pop("sslmode", None)
        return str(parsed_url.set(query=query))

    return database_url
