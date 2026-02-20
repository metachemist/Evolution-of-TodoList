# Task: T064 — align security tests with AuthService hashing contract
import pytest
from uuid import uuid4

from src.models.user import User
from src.models.task import Task
from src.services.auth_service import hash_password as get_password_hash
from tests.conftest import make_auth_header


@pytest.mark.asyncio
async def test_unauthorized_access_no_token(client):
    """Protected endpoints return 401/422 without an Authorization header."""
    resp = await client.get("/api/some-user-id/tasks")
    assert resp.status_code in [401, 422]


@pytest.mark.asyncio
async def test_invalid_token_handling(client):
    """An invalid Bearer token returns 401."""
    resp = await client.get(
        "/api/some-user-id/tasks",
        headers={"Authorization": "Bearer totally-invalid-token"},
    )
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_user_isolation(client, db_session):
    """Users cannot access another user's tasks (returns 403)."""
    user_a = User(email="a@iso.com", hashed_password=get_password_hash("pw"))
    user_b = User(email="b@iso.com", hashed_password=get_password_hash("pw"))
    db_session.add_all([user_a, user_b])
    await db_session.commit()
    await db_session.refresh(user_a)
    await db_session.refresh(user_b)

    # Create a task for user A
    task = Task(title="A's task", owner_id=user_a.id)
    db_session.add(task)
    await db_session.commit()

    # User B tries to access user A's tasks
    headers_b = make_auth_header(str(user_b.id))
    resp = await client.get(f"/api/{user_a.id}/tasks", headers=headers_b)
    assert resp.status_code == 403
