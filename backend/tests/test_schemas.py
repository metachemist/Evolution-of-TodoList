import pytest
from uuid import uuid4
from datetime import datetime, timezone

from src.schemas import (
    TaskCreate, TaskUpdate, TaskResponse,
    ErrorResponse, UserResponse, TokenResponse,
    UserCreate, UserLogin,
)


def test_task_create_schema():
    task = TaskCreate(title="Test Task", description="A description")
    assert task.title == "Test Task"
    assert task.description == "A description"


def test_task_create_optional_description():
    task = TaskCreate(title="Only title")
    assert task.description is None


def test_task_update_schema():
    update = TaskUpdate(title="New title")
    assert update.title == "New title"
    assert update.description is None


def test_task_response_schema():
    uid = uuid4()
    now = datetime.now(timezone.utc)
    resp = TaskResponse(
        id=uid, title="T", description=None,
        is_completed=False, created_at=now, updated_at=now, owner_id=uid,
    )
    assert resp.id == uid
    assert resp.is_completed is False
    assert resp.created_at == now


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
