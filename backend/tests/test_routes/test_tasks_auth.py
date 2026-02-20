# Task: T034 — Task authorization integration tests (two-layer authorization)
# Spec: @specs/1-specify/phase-2/feature-03-auth-db-monorepo.md (FR-005–FR-007, SEC-003, SEC-004, TEST-003)
# ADR: @history/adr/0013-two-layer-authorization-semantics.md
import pytest
from uuid import uuid4

import src.middleware.rate_limit as rate_limit_module
from src.models.user import User
from src.services.auth_service import hash_password
from tests.conftest import make_auth_header

REGISTER_URL = "/api/auth/register"
LOGIN_URL = "/api/auth/login"


async def _register_and_login(client, email: str, password: str = "SecurePass1") -> dict:
    """Register a user and return the auth data from the login response."""
    reg = await client.post(REGISTER_URL, json={"email": email, "password": password})
    assert reg.status_code == 201
    token = reg.json()["data"]["access_token"]
    # Get user id via /me
    me = await client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    return {"token": token, "user_id": me.json()["data"]["id"]}


# ── Unauthenticated requests (FR-011) ─────────────────────────────────────────

@pytest.mark.asyncio
async def test_list_tasks_unauthenticated(client):
    """GET /api/{user_id}/tasks without auth → 401 UNAUTHORIZED."""
    fake_id = str(uuid4())
    resp = await client.get(f"/api/{fake_id}/tasks")
    assert resp.status_code == 401
    assert resp.json()["error"]["code"] == "UNAUTHORIZED"


@pytest.mark.asyncio
async def test_create_task_unauthenticated(client):
    """POST /api/{user_id}/tasks without auth → 401."""
    fake_id = str(uuid4())
    resp = await client.post(f"/api/{fake_id}/tasks", json={"title": "Test"})
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_update_task_unauthenticated(client):
    """PATCH /api/{user_id}/tasks/{task_id} without auth → 401."""
    fake_id = str(uuid4())
    resp = await client.patch(f"/api/{fake_id}/tasks/{uuid4()}/complete")
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_delete_task_unauthenticated(client):
    """DELETE /api/{user_id}/tasks/{task_id} without auth → 401."""
    fake_id = str(uuid4())
    resp = await client.delete(f"/api/{fake_id}/tasks/{uuid4()}")
    assert resp.status_code == 401


# ── Layer 1: {user_id} path mismatch → 403 (SEC-003) ─────────────────────────

@pytest.mark.asyncio
async def test_403_on_user_id_path_mismatch(client):
    """User A token + User B path → 403 FORBIDDEN."""
    user_a = await _register_and_login(client, "user_a@example.com")
    user_b = await _register_and_login(client, "user_b@example.com")

    resp = await client.get(
        f"/api/{user_b['user_id']}/tasks",
        headers={"Authorization": f"Bearer {user_a['token']}"},
    )
    assert resp.status_code == 403
    assert resp.json()["error"]["code"] == "FORBIDDEN"


@pytest.mark.asyncio
async def test_create_task_forbidden_for_other_user(client):
    """POST to another user's task path → 403."""
    user_a = await _register_and_login(client, "create_a@example.com")
    user_b = await _register_and_login(client, "create_b@example.com")

    resp = await client.post(
        f"/api/{user_b['user_id']}/tasks",
        json={"title": "Injected"},
        headers={"Authorization": f"Bearer {user_a['token']}"},
    )
    assert resp.status_code == 403


# ── Layer 2: task owned by other user → 404 (SEC-004) ────────────────────────

@pytest.mark.asyncio
async def test_404_on_cross_user_task_access(client):
    """User A accesses User A's path but a task that belongs to User B → 404."""
    user_a = await _register_and_login(client, "task_a@example.com")
    user_b = await _register_and_login(client, "task_b@example.com")

    # User B creates a task
    b_task = await client.post(
        f"/api/{user_b['user_id']}/tasks",
        json={"title": "B's task"},
        headers={"Authorization": f"Bearer {user_b['token']}"},
    )
    assert b_task.status_code == 201
    b_task_id = b_task.json()["data"]["id"]

    # User A tries to access User B's task via User A's path (user_id matches, task doesn't)
    resp = await client.get(
        f"/api/{user_a['user_id']}/tasks/{b_task_id}",
        headers={"Authorization": f"Bearer {user_a['token']}"},
    )
    assert resp.status_code == 404
    assert resp.json()["error"]["code"] == "TASK_NOT_FOUND"


# ── Cross-user isolation (TEST-003) ───────────────────────────────────────────

@pytest.mark.asyncio
async def test_task_list_isolation(client):
    """User A's task list does not include User B's tasks."""
    user_a = await _register_and_login(client, "iso_a@example.com")
    user_b = await _register_and_login(client, "iso_b@example.com")

    # User B creates a task
    await client.post(
        f"/api/{user_b['user_id']}/tasks",
        json={"title": "B's private task"},
        headers={"Authorization": f"Bearer {user_b['token']}"},
    )

    # User A lists their tasks — B's task must not appear
    resp = await client.get(
        f"/api/{user_a['user_id']}/tasks",
        headers={"Authorization": f"Bearer {user_a['token']}"},
    )
    assert resp.status_code == 200
    task_titles = [t["title"] for t in resp.json()["data"]]
    assert "B's private task" not in task_titles


@pytest.mark.asyncio
async def test_own_task_accessible(client):
    """User A can access their own task."""
    user_a = await _register_and_login(client, "own_a@example.com")

    create_resp = await client.post(
        f"/api/{user_a['user_id']}/tasks",
        json={"title": "My own task"},
        headers={"Authorization": f"Bearer {user_a['token']}"},
    )
    assert create_resp.status_code == 201
    task_id = create_resp.json()["data"]["id"]

    get_resp = await client.get(
        f"/api/{user_a['user_id']}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {user_a['token']}"},
    )
    assert get_resp.status_code == 200
    assert get_resp.json()["data"]["title"] == "My own task"


@pytest.mark.asyncio
async def test_rate_limiter_returns_429_when_limit_exceeded(client, db_session, monkeypatch):
    """Authenticated requests return 429 envelope when user rate limit is exceeded."""
    monkeypatch.setattr(rate_limit_module, "_AUTHENTICATED_LIMIT", 1)

    user = User(email="ratelimit@test.com", hashed_password=hash_password("SecurePass1"))
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    headers = make_auth_header(str(user.id), email=user.email)

    first = await client.get(f"/api/{user.id}/tasks", headers=headers)
    second = await client.get(f"/api/{user.id}/tasks", headers=headers)

    assert first.status_code == 200
    assert second.status_code == 429
    body = second.json()
    assert body["success"] is False
    assert body["data"] is None
    assert body["error"]["code"] == "RATE_LIMITED"
