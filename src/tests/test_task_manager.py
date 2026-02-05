"""
Unit tests for the TaskManager class.
"""

import pytest
from src.core.task_manager import TaskManager
from src.core.models import Task


def test_add_task():
    """Test adding a new task."""
    tm = TaskManager()

    task = tm.add_task("Test title", "Test description")

    assert task.id == 1
    assert task.title == "Test title"
    assert task.description == "Test description"
    assert task.status == "pending"
    assert len(tm.get_all_tasks()) == 1


def test_add_task_default_description():
    """Test adding a task with no description."""
    tm = TaskManager()

    task = tm.add_task("Test title")

    assert task.id == 1
    assert task.title == "Test title"
    assert task.description is None
    assert task.status == "pending"


def test_get_all_tasks():
    """Test getting all tasks."""
    tm = TaskManager()
    tm.add_task("Task 1")
    tm.add_task("Task 2")

    tasks = tm.get_all_tasks()

    assert len(tasks) == 2
    assert tasks[0].title == "Task 1"
    assert tasks[1].title == "Task 2"


def test_get_tasks_by_status():
    """Test getting tasks filtered by status."""
    tm = TaskManager()
    task1 = tm.add_task("Pending task")
    task2 = tm.add_task("Completed task")
    tm.mark_complete(task2.id)

    pending_tasks = tm.get_tasks_by_status("pending")
    completed_tasks = tm.get_tasks_by_status("completed")

    assert len(pending_tasks) == 1
    assert pending_tasks[0].title == "Pending task"
    assert len(completed_tasks) == 1
    assert completed_tasks[0].title == "Completed task"


def test_update_task():
    """Test updating an existing task."""
    tm = TaskManager()
    original_task = tm.add_task("Original title", "Original description")

    updated_task = tm.update_task(original_task.id, "New title", "New description")

    assert updated_task is not None
    assert updated_task.title == "New title"
    assert updated_task.description == "New description"


def test_update_task_partial():
    """Test updating only title or description."""
    tm = TaskManager()
    original_task = tm.add_task("Original title", "Original description")

    # Update only the title
    updated_task = tm.update_task(original_task.id, title="New title")

    assert updated_task is not None
    assert updated_task.title == "New title"
    assert updated_task.description == "Original description"  # Should remain unchanged

    # Update only the description
    original_task2 = tm.add_task("Another task", "Another description")
    updated_task2 = tm.update_task(original_task2.id, description="Updated description")

    assert updated_task2 is not None
    assert updated_task2.title == "Another task"  # Should remain unchanged
    assert updated_task2.description == "Updated description"


def test_update_nonexistent_task():
    """Test updating a task that doesn't exist."""
    tm = TaskManager()

    result = tm.update_task(999, "New title")

    assert result is None


def test_mark_complete():
    """Test marking a task as complete."""
    tm = TaskManager()
    task = tm.add_task("Test task")

    completed_task = tm.mark_complete(task.id)

    assert completed_task is not None
    assert completed_task.status == "completed"


def test_mark_complete_nonexistent():
    """Test marking a nonexistent task as complete."""
    tm = TaskManager()

    result = tm.mark_complete(999)

    assert result is None


def test_delete_task():
    """Test deleting an existing task."""
    tm = TaskManager()
    task = tm.add_task("Test task")

    success = tm.delete_task(task.id)

    assert success is True
    assert len(tm.get_all_tasks()) == 0


def test_delete_nonexistent_task():
    """Test deleting a task that doesn't exist."""
    tm = TaskManager()

    success = tm.delete_task(999)

    assert success is False


def test_get_task():
    """Test getting a specific task by ID."""
    tm = TaskManager()
    task = tm.add_task("Test task")

    retrieved_task = tm.get_task(task.id)

    assert retrieved_task is not None
    assert retrieved_task.id == task.id
    assert retrieved_task.title == "Test task"


def test_get_nonexistent_task():
    """Test getting a task that doesn't exist."""
    tm = TaskManager()

    result = tm.get_task(999)

    assert result is None


def test_validate_task_data_valid():
    """Test that valid task data passes validation."""
    tm = TaskManager()

    result = tm.validate_task_data("Valid title", "Valid description")

    assert result is True


def test_validate_task_data_empty_title():
    """Test that empty title fails validation."""
    tm = TaskManager()

    with pytest.raises(ValueError, match="Title cannot be empty"):
        tm.validate_task_data("", "Valid description")


def test_validate_task_data_whitespace_only_title():
    """Test that whitespace-only title fails validation."""
    tm = TaskManager()

    with pytest.raises(ValueError, match="Title cannot be empty"):
        tm.validate_task_data("   ", "Valid description")


def test_validate_task_data_long_title():
    """Test that long title fails validation."""
    tm = TaskManager()
    long_title = "x" * 256

    with pytest.raises(ValueError, match="Title exceeds maximum length"):
        tm.validate_task_data(long_title, "Valid description")


def test_validate_task_data_long_description():
    """Test that long description fails validation."""
    tm = TaskManager()
    long_description = "x" * 1001

    with pytest.raises(ValueError, match="Description exceeds maximum length"):
        tm.validate_task_data("Valid title", long_description)


def test_id_assignment():
    """Test that IDs are assigned sequentially."""
    tm = TaskManager()
    task1 = tm.add_task("First task")
    task2 = tm.add_task("Second task")
    task3 = tm.add_task("Third task")

    assert task1.id == 1
    assert task2.id == 2
    assert task3.id == 3