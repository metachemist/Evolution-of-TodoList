import pytest
from uuid import uuid4

from src.models.user import User
from src.models.task import Task
from src.utils.auth import get_password_hash
from tests.conftest import make_auth_header, make_auth_cookie


@pytest.mark.asyncio
async def test_get_tasks_returns_200(client, db_session):
    """GET /api/{user_id}/tasks returns 200 with an empty list for a new user."""
    user = User(email="tasks@test.com", hashed_password=get_password_hash("pw"))
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    headers = make_auth_header(str(user.id))
    resp = await client.get(f"/api/{user.id}/tasks", headers=headers)
    assert resp.status_code == 200
    assert resp.json() == []


@pytest.mark.asyncio
async def test_create_task_returns_201(client, db_session):
    """POST /api/{user_id}/tasks creates a task and returns 201."""
    user = User(email="create@test.com", hashed_password=get_password_hash("pw"))
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    headers = make_auth_header(str(user.id))
    resp = await client.post(
        f"/api/{user.id}/tasks",
        json={"title": "New Task", "description": "Details"},
        headers=headers,
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "New Task"
    assert data["description"] == "Details"
    assert data["is_completed"] is False
    assert data["owner_id"] == str(user.id)


@pytest.mark.asyncio
async def test_get_single_task(client, db_session):
    """GET /api/{user_id}/tasks/{task_id} returns the task."""
    user = User(email="single@test.com", hashed_password=get_password_hash("pw"))
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    task = Task(title="Find Me", owner_id=user.id)
    db_session.add(task)
    await db_session.commit()
    await db_session.refresh(task)

    headers = make_auth_header(str(user.id))
    resp = await client.get(f"/api/{user.id}/tasks/{task.id}", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["title"] == "Find Me"


@pytest.mark.asyncio
async def test_update_task(client, db_session):
    """PUT /api/{user_id}/tasks/{task_id} updates the task."""
    user = User(email="update@test.com", hashed_password=get_password_hash("pw"))
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    task = Task(title="Old Title", owner_id=user.id)
    db_session.add(task)
    await db_session.commit()
    await db_session.refresh(task)

    headers = make_auth_header(str(user.id))
    resp = await client.put(
        f"/api/{user.id}/tasks/{task.id}",
        json={"title": "New Title"},
        headers=headers,
    )
    assert resp.status_code == 200
    assert resp.json()["title"] == "New Title"


@pytest.mark.asyncio
async def test_delete_task(client, db_session):
    """DELETE /api/{user_id}/tasks/{task_id} returns 204."""
    user = User(email="delete@test.com", hashed_password=get_password_hash("pw"))
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    task = Task(title="Delete Me", owner_id=user.id)
    db_session.add(task)
    await db_session.commit()
    await db_session.refresh(task)

    headers = make_auth_header(str(user.id))
    resp = await client.delete(f"/api/{user.id}/tasks/{task.id}", headers=headers)
    assert resp.status_code == 204


@pytest.mark.asyncio
async def test_toggle_completion(client, db_session):
    """PATCH /api/{user_id}/tasks/{task_id}/complete toggles is_completed."""
    user = User(email="toggle@test.com", hashed_password=get_password_hash("pw"))
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    task = Task(title="Toggle Me", owner_id=user.id)
    db_session.add(task)
    await db_session.commit()
    await db_session.refresh(task)
    assert task.is_completed is False

    headers = make_auth_header(str(user.id))
    resp = await client.patch(f"/api/{user.id}/tasks/{task.id}/complete", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["is_completed"] is True


@pytest.mark.asyncio
async def test_error_response_format(client):
    """Error responses follow the {success, data, error} structure."""
    fake_uid = str(uuid4())
    resp = await client.get(f"/api/{fake_uid}/tasks", headers=make_auth_header(fake_uid))
    assert resp.status_code == 404
    body = resp.json()
    # Global exception handler wraps errors in {success, data, error} format
    assert body["success"] is False
    assert "error" in body
    assert "code" in body["error"]


@pytest.mark.asyncio
async def test_pagination_defaults(client, db_session):
    """GET /tasks respects pagination query params."""
    user = User(email="page@test.com", hashed_password=get_password_hash("pw"))
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    # Create 25 tasks
    for i in range(25):
        db_session.add(Task(title=f"Task {i}", owner_id=user.id))
    await db_session.commit()

    headers = make_auth_header(str(user.id))

    # Default should return 20
    resp = await client.get(f"/api/{user.id}/tasks", headers=headers)
    assert resp.status_code == 200
    assert len(resp.json()) == 20

    # Explicit limit=5
    resp = await client.get(f"/api/{user.id}/tasks?limit=5", headers=headers)
    assert len(resp.json()) == 5

    # skip=20 should return remaining 5
    resp = await client.get(f"/api/{user.id}/tasks?skip=20", headers=headers)
    assert len(resp.json()) == 5


@pytest.mark.asyncio
async def test_get_tasks_with_cookie_auth(client, db_session):
    """GET /api/{user_id}/tasks works with cookie-based auth."""
    user = User(email="cookie-tasks@test.com", hashed_password=get_password_hash("pw"))
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    task = Task(title="Cookie Task", owner_id=user.id)
    db_session.add(task)
    await db_session.commit()

    cookies = make_auth_cookie(str(user.id))
    resp = await client.get(f"/api/{user.id}/tasks", cookies=cookies)
    assert resp.status_code == 200
    assert len(resp.json()) == 1
    assert resp.json()[0]["title"] == "Cookie Task"
