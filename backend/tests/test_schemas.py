import pytest
from uuid import uuid4
from datetime import datetime, timezone

from src.schemas import (
    TaskCreate, TaskUpdate, TaskResponse,
    FocusSessionRequest, TaskOverviewResponse,
    ErrorResponse, UserResponse, TokenResponse,
    UserCreate, UserLogin,
)


def test_task_create_schema():
    task = TaskCreate(
        title="Test Task",
        description="A description",
        priority="HIGH",
        status="IN_PROGRESS",
    )
    assert task.title == "Test Task"
    assert task.description == "A description"
    assert task.priority == "HIGH"
    assert task.status == "IN_PROGRESS"


def test_task_create_optional_description():
    task = TaskCreate(title="Only title")
    assert task.description is None
    assert task.priority == "MEDIUM"
    assert task.status == "TODO"


def test_task_update_schema():
    update = TaskUpdate(title="New title", priority="LOW", status="DONE")
    assert update.title == "New title"
    assert update.description is None
    assert update.priority == "LOW"
    assert update.status == "DONE"


def test_task_response_schema():
    uid = uuid4()
    now = datetime.now(timezone.utc)
    resp = TaskResponse(
        id=uid, title="T", description=None,
        is_completed=False,
        priority="MEDIUM",
        due_date=None,
        focus_minutes=0,
        status="TODO",
        created_at=now,
        updated_at=now,
        owner_id=uid,
    )
    assert resp.id == uid
    assert resp.is_completed is False
    assert resp.created_at == now


def test_focus_session_request_schema():
    payload = FocusSessionRequest(minutes=25)
    assert payload.minutes == 25


def test_task_overview_response_schema():
    overview = TaskOverviewResponse(
        total_tasks=10,
        completed_tasks=5,
        in_progress_tasks=3,
        overdue_tasks=2,
        total_focus_minutes=250,
        completion_rate=50.0,
    )
    assert overview.total_tasks == 10
    assert overview.completion_rate == 50.0


def test_error_response_schema():
    err = ErrorResponse(
        success=False, data=None,
        error={"code": "TEST_ERROR", "message": "Something went wrong"},
    )
    assert err.success is False
    assert err.error["code"] == "TEST_ERROR"


def test_user_response_schema():
    uid = uuid4()
    now = datetime.now(timezone.utc)
    resp = UserResponse(id=uid, email="a@b.com", created_at=now, updated_at=now)
    assert resp.email == "a@b.com"
    assert resp.id == uid


def test_token_response_schema():
    tok = TokenResponse(access_token="abc123")
    assert tok.access_token == "abc123"
    assert tok.token_type == "bearer"


def test_user_create_schema():
    uc = UserCreate(email="user@example.com", password="secret123")
    assert uc.email == "user@example.com"
    assert uc.password == "secret123"


def test_user_login_schema():
    ul = UserLogin(email="user@example.com", password="secret123")
    assert ul.email == "user@example.com"
