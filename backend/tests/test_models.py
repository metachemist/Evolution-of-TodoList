import pytest
from src.models.user import User
from src.models.task import Task
from uuid import uuid4
from datetime import datetime


def test_user_model():
    """Test the User model."""
    user_id = uuid4()
    user = User(
        id=user_id,
        email="test@example.com",
        hashed_password="hashed_password",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    assert user.id == user_id
    assert user.email == "test@example.com"
    assert user.hashed_password == "hashed_password"


def test_task_model():
    """Test the Task model."""
    task_id = uuid4()
    user_id = uuid4()
    task = Task(
        id=task_id,
        title="Test Task",
        description="Test Description",
        is_completed=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        owner_id=user_id
    )
    
    assert task.id == task_id
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.is_completed is False
    assert task.owner_id == user_id