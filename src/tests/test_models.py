"""
Unit tests for the Task model.
"""

import pytest
from datetime import datetime
from src.core.models import Task


def test_task_creation_valid():
    """Test creating a valid Task instance."""
    task = Task(id=1, title="Test task", description="Test description", status="pending")

    assert task.id == 1
    assert task.title == "Test task"
    assert task.description == "Test description"
    assert task.status == "pending"


def test_task_creation_default_status():
    """Test creating a Task with default status."""
    task = Task(id=1, title="Test task")

    assert task.status == "pending"


def test_task_title_validation_empty():
    """Test that empty title raises ValueError."""
    with pytest.raises(ValueError, match="Title cannot be empty"):
        Task(id=1, title="")


def test_task_title_validation_whitespace_only():
    """Test that whitespace-only title raises ValueError."""
    with pytest.raises(ValueError, match="Title cannot be empty"):
        Task(id=1, title="   ")


def test_task_title_validation_too_long():
    """Test that title exceeding 255 characters raises ValueError."""
    long_title = "x" * 256
    with pytest.raises(ValueError, match="Title exceeds maximum length"):
        Task(id=1, title=long_title)


def test_task_description_validation_too_long():
    """Test that description exceeding 1000 characters raises ValueError."""
    long_description = "x" * 1001
    with pytest.raises(ValueError, match="Description exceeds maximum length"):
        Task(id=1, title="Test", description=long_description)


def test_task_update_title():
    """Test updating task title."""
    task = Task(id=1, title="Original title")

    task.update_title("New title")

    assert task.title == "New title"


def test_task_update_title_validation():
    """Test validation when updating task title."""
    task = Task(id=1, title="Original title")

    with pytest.raises(ValueError, match="Title cannot be empty"):
        task.update_title("")


def test_task_update_description():
    """Test updating task description."""
    task = Task(id=1, title="Test title", description="Original description")

    task.update_description("New description")

    assert task.description == "New description"


def test_task_mark_completed():
    """Test marking task as completed."""
    task = Task(id=1, title="Test title", status="pending")

    task.mark_completed()

    assert task.status == "completed"


def test_task_to_dict():
    """Test converting task to dictionary."""
    task = Task(id=1, title="Test title", description="Test description", status="pending")
    result = task.to_dict()

    assert result["id"] == 1
    assert result["title"] == "Test title"
    assert result["description"] == "Test description"
    assert result["status"] == "pending"
    assert "created_at" in result
    assert isinstance(result["created_at"], str)


def test_task_str_representation():
    """Test string representation of task."""
    task = Task(id=1, title="Test title", status="pending")

    assert "Task(id=1, title='Test title', status='pending')" in str(task)


def test_task_repr_representation():
    """Test developer-friendly representation of task."""
    task = Task(id=1, title="Test title", description="Test description", status="pending")

    repr_str = repr(task)

    assert "Task(id=1, title='Test title', description='Test description', status='pending'" in repr_str