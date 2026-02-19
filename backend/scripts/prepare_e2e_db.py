# Task: T050 | Prepare isolated SQLite database for Playwright E2E orchestration
from __future__ import annotations

import os
from datetime import datetime, timezone
from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlmodel import Session, create_engine, select

from src.models.user import User
from src.services.auth_service import hash_password

_DEFAULT_E2E_EMAIL = "e2e@example.com"
_DEFAULT_E2E_PASSWORD = "TestPassword123!"


def _to_sync_sqlite_url(database_url: str) -> str:
    """Convert sqlite+aiosqlite URL to sqlite URL for synchronous prep."""
    if database_url.startswith("sqlite+aiosqlite:///"):
        return "sqlite:///" + database_url.removeprefix("sqlite+aiosqlite:///")
    if database_url.startswith("sqlite:///"):
        return database_url
    raise RuntimeError(
        "E2E setup only supports sqlite URLs (sqlite+aiosqlite:///... or sqlite:///...)."
    )


def _sqlite_db_path(sync_sqlite_url: str) -> Path:
    raw_path = sync_sqlite_url.removeprefix("sqlite:///")
    return Path(raw_path).resolve()


def reset_database_file(sync_sqlite_url: str) -> None:
    db_path = _sqlite_db_path(sync_sqlite_url)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    if db_path.exists():
        db_path.unlink()
    db_path.touch()


def run_migrations(sync_sqlite_url: str) -> None:
    backend_root = Path(__file__).resolve().parents[1]
    config = Config(str(backend_root / "alembic.ini"))
    config.set_main_option("script_location", str(backend_root / "alembic"))
    previous_database_url = os.getenv("DATABASE_URL")
    try:
        # alembic/env.py reads DATABASE_URL from process env.
        os.environ["DATABASE_URL"] = sync_sqlite_url
        command.upgrade(config, "head")
    finally:
        if previous_database_url is None:
            os.environ.pop("DATABASE_URL", None)
        else:
            os.environ["DATABASE_URL"] = previous_database_url


def seed_e2e_user(sync_sqlite_url: str, email: str, password: str) -> None:
    engine = create_engine(sync_sqlite_url)
    try:
        with Session(engine) as session:
            existing_user = session.exec(select(User).where(User.email == email)).first()
            if existing_user:
                return
            now = datetime.now(timezone.utc)
            session.add(
                User(
                    email=email,
                    hashed_password=hash_password(password),
                    created_at=now,
                    updated_at=now,
                )
            )
            session.commit()
    finally:
        engine.dispose()


def main() -> None:
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL is required for E2E database setup.")

    seed_email = os.getenv("E2E_USER_EMAIL", _DEFAULT_E2E_EMAIL)
    seed_password = os.getenv("E2E_USER_PASSWORD", _DEFAULT_E2E_PASSWORD)
    sync_sqlite_url = _to_sync_sqlite_url(database_url)

    print(f"[prepare_e2e_db] resetting database at {sync_sqlite_url}", flush=True)
    reset_database_file(sync_sqlite_url)
    print("[prepare_e2e_db] applying Alembic migrations", flush=True)
    run_migrations(sync_sqlite_url)
    print(f"[prepare_e2e_db] seeding user {seed_email}", flush=True)
    seed_e2e_user(sync_sqlite_url, seed_email, seed_password)
    print("[prepare_e2e_db] done", flush=True)


if __name__ == "__main__":
    main()
