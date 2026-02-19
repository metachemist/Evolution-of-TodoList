# Task: T064 — async SQLite fixture smoke test for pytest reliability
from __future__ import annotations

import pytest

from src.models.user import User


@pytest.mark.asyncio
async def test_db_fixture_round_trip(db_session):
    user = User(email="fixture@example.com", hashed_password="hash")
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    fetched = await db_session.get(User, user.id)
    assert fetched is not None
    assert fetched.email == "fixture@example.com"
