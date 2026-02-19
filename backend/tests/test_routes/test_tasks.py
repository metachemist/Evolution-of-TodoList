import pytest
from datetime import timedelta
from uuid import uuid4

from src.models.user import User
from src.models.task import Task, TaskStatus
from src.services.auth_service import hash_password as get_password_hash
from tests.conftest import make_auth_header
from src.utils.datetime_utils import utcnow_naive


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
    body = resp.json()
    assert body["success"] is True
    assert body["error"] is None
    assert body["data"] == []


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
    body = resp.json()
    assert body["success"] is True
    assert body["error"] is None
    data = body["data"]
    assert data["title"] == "New Task"
    assert data["description"] == "Details"
    assert data["is_completed"] is False
    assert data["priority"] == "MEDIUM"
    assert data["status"] == "TODO"
    assert data["focus_minutes"] == 0
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
    body = resp.json()
    assert body["success"] is True
    assert body["error"] is None
    assert body["data"]["title"] == "Find Me"


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
    body = resp.json()
    assert body["success"] is True
    assert body["error"] is None
    assert body["data"]["title"] == "New Title"


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
    body = resp.json()
    assert body["success"] is True
    assert body["error"] is None
    assert body["data"]["is_completed"] is True
    assert body["data"]["status"] == "DONE"


@pytest.mark.asyncio
async def test_error_response_format(client, db_session):
    """Error responses follow the {success, data, error} structure."""
    # Create a real user so the auth guard passes
    user = User(email="errfmt@test.com", hashed_password=get_password_hash("SecurePass1"))
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    # Request a non-existent task — should 404 with the wrapped error envelope
    headers = make_auth_header(str(user.id), email="errfmt@test.com")
    fake_task_id = str(uuid4())
    resp = await client.get(f"/api/{user.id}/tasks/{fake_task_id}", headers=headers)
    assert resp.status_code == 404
    body = resp.json()
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
    assert len(resp.json()["data"]) == 20

    # Explicit limit=5
    resp = await client.get(f"/api/{user.id}/tasks?limit=5", headers=headers)
    assert len(resp.json()["data"]) == 5

    # skip=20 should return remaining 5
    resp = await client.get(f"/api/{user.id}/tasks?skip=20", headers=headers)
    assert len(resp.json()["data"]) == 5


@pytest.mark.asyncio
async def test_invalid_task_id_returns_422_envelope(client, db_session):
    """Invalid UUID path params are rejected with 422 envelope response."""
    user = User(email="invaliduuid@test.com", hashed_password=get_password_hash("pw"))
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    headers = make_auth_header(str(user.id))
    resp = await client.get(f"/api/{user.id}/tasks/not-a-uuid", headers=headers)
    assert resp.status_code == 422
    body = resp.json()
    assert body["success"] is False
    assert body["data"] is None
    assert body["error"]["code"] == "VALIDATION_ERROR"


@pytest.mark.asyncio
async def test_create_task_whitespace_title_returns_422_envelope(client, db_session):
    """Whitespace-only title is stripped then rejected by min_length validation."""
    user = User(email="whitespace@test.com", hashed_password=get_password_hash("pw"))
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    headers = make_auth_header(str(user.id))
    resp = await client.post(
        f"/api/{user.id}/tasks",
        json={"title": "   ", "description": "valid"},
        headers=headers,
    )
    assert resp.status_code == 422
    body = resp.json()
    assert body["success"] is False
    assert body["data"] is None
    assert body["error"]["code"] == "VALIDATION_ERROR"


@pytest.mark.asyncio
async def test_get_tasks_overview_returns_200(client, db_session):
    """GET /api/tasks/overview returns aggregate progress metrics for current user."""
    user = User(email="overview@test.com", hashed_password=get_password_hash("pw"))
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    now = utcnow_naive()
    task_done = Task(title="Done", owner_id=user.id, status=TaskStatus.DONE, is_completed=True, focus_minutes=30)
    task_in_progress = Task(title="Progress", owner_id=user.id, status=TaskStatus.IN_PROGRESS, focus_minutes=20)
    task_overdue = Task(
        title="Overdue",
        owner_id=user.id,
        status=TaskStatus.TODO,
        due_date=now - timedelta(days=1),
    )
    db_session.add_all([task_done, task_in_progress, task_overdue])
    await db_session.commit()

    headers = make_auth_header(str(user.id))
    resp = await client.get("/api/tasks/overview", headers=headers)
    assert resp.status_code == 200
    body = resp.json()
    assert body["success"] is True
    assert body["error"] is None
    assert body["data"]["total_tasks"] == 3
    assert body["data"]["completed_tasks"] == 1
    assert body["data"]["in_progress_tasks"] == 1
    assert body["data"]["overdue_tasks"] == 1
    assert body["data"]["total_focus_minutes"] == 50


@pytest.mark.asyncio
async def test_post_focus_adds_minutes(client, db_session):
    """POST /api/tasks/{task_id}/focus increments focus_minutes and returns updated task."""
    user = User(email="focus@test.com", hashed_password=get_password_hash("pw"))
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    task = Task(title="Focus task", owner_id=user.id, focus_minutes=5, status=TaskStatus.TODO)
    db_session.add(task)
    await db_session.commit()
    await db_session.refresh(task)

    headers = make_auth_header(str(user.id))
    resp = await client.post(
        f"/api/tasks/{task.id}/focus",
        json={"minutes": 25},
        headers=headers,
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["success"] is True
    assert body["error"] is None
    assert body["data"]["focus_minutes"] == 30
    assert body["data"]["status"] == "IN_PROGRESS"


@pytest.mark.asyncio
async def test_post_focus_rejects_invalid_minutes(client, db_session):
    """POST /api/tasks/{task_id}/focus validates minutes bounds with VALIDATION_ERROR envelope."""
    user = User(email="focus-invalid@test.com", hashed_password=get_password_hash("pw"))
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    task = Task(title="Focus invalid", owner_id=user.id)
    db_session.add(task)
    await db_session.commit()
    await db_session.refresh(task)

    headers = make_auth_header(str(user.id))
    resp = await client.post(
        f"/api/tasks/{task.id}/focus",
        json={"minutes": 0},
        headers=headers,
    )
    assert resp.status_code == 422
    body = resp.json()
    assert body["success"] is False
    assert body["data"] is None
    assert body["error"]["code"] == "VALIDATION_ERROR"


@pytest.mark.asyncio
async def test_create_task_rejects_past_due_date(client, db_session):
    """POST /api/{user_id}/tasks rejects past due_date with VALIDATION_ERROR envelope."""
    user = User(email="pastdue@test.com", hashed_password=get_password_hash("pw"))
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    headers = make_auth_header(str(user.id))
    resp = await client.post(
        f"/api/{user.id}/tasks",
        json={
            "title": "Past due",
            "due_date": (utcnow_naive() - timedelta(hours=1)).isoformat(),
        },
        headers=headers,
    )
    assert resp.status_code == 422
    body = resp.json()
    assert body["success"] is False
    assert body["data"] is None
    assert body["error"]["code"] == "VALIDATION_ERROR"
