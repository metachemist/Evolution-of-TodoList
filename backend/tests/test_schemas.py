import pytest
from src.schemas.task import TaskCreate, TaskUpdate, TaskResponse, ErrorResponse, UserResponse
from uuid import uuid4
from datetime import datetime


def test_task_create_schema():
    """Test the TaskCreate schema."""
    task_create = TaskCreate(title="Test Task", description="Test Description")
    
    assert task_create.title == "Test Task"
    assert task_create.description == "Test Description"


def test_task_update_schema():
    """Test the TaskUpdate schema."""
    task_update = TaskUpdate(title="Updated Task", description="Updated Description")
    
    assert task_update.title == "Updated Task"
    assert task_update.description == "Updated Description"


def test_task_response_schema():
    """Test the TaskResponse schema."""
    task_response = TaskResponse(
        id=str(uuid4()),
        title="Test Task",
        description="Test Description",
        is_completed=False,
        created_at=datetime.utcnow().isoformat(),
        updated_at=datetime.utcnow().isoformat(),
        owner_id=str(uuid4())
    )
    
    assert task_response.id is not None
    assert task_response.title == "Test Task"
    assert task_response.description == "Test Description"
    assert task_response.is_completed is False
    assert task_response.owner_id is not None


def test_error_response_schema():
    """Test the ErrorResponse schema."""
    error_response = ErrorResponse(
        success=False,
        data=None,
        error={"code": "TEST_ERROR", "message": "Test error message"}
    )
    
    assert error_response.success is False
    assert error_response.data is None
    assert "code" in error_response.error
    assert "message" in error_response.error


def test_user_response_schema():
    """Test the UserResponse schema."""
    user_response = UserResponse(
        id=str(uuid4()),
        email="test@example.com",
        created_at=datetime.utcnow().isoformat(),
        updated_at=datetime.utcnow().isoformat()
    )
    
    assert user_response.id is not None
    assert user_response.email == "test@example.com"