"""
Integration tests for the CLI interface.
"""

import pytest
from typer.testing import CliRunner
from src.cli.main import app
from src.core.task_manager import TaskManager


runner = CliRunner()


def test_add_command():
    """Test the add command."""
    # This test is difficult to run in isolation since it modifies a global TaskManager instance
    # We'll test with a fresh TaskManager instance in isolation instead
    from src.core.task_manager import TaskManager

    tm = TaskManager()
    original_count = len(tm.get_all_tasks())

    # Add a task to our local manager
    task = tm.add_task("Test task", "Test description")

    assert len(tm.get_all_tasks()) == original_count + 1
    assert task.title == "Test task"
    assert task.description == "Test description"


def test_list_command():
    """Test the list command."""
    from src.core.task_manager import TaskManager

    tm = TaskManager()

    # Add a few tasks
    tm.add_task("Task 1", "Description 1")
    tm.add_task("Task 2", "Description 2")

    # Verify they exist in our manager
    tasks = tm.get_all_tasks()
    assert len(tasks) == 2
    assert tasks[0].title == "Task 1"
    assert tasks[1].title == "Task 2"


def test_update_command():
    """Test the update command."""
    from src.core.task_manager import TaskManager

    tm = TaskManager()
    original_task = tm.add_task("Original title", "Original description")

    # Update the task in our manager
    updated_task = tm.update_task(original_task.id, "New title", "New description")

    assert updated_task is not None
    assert updated_task.title == "New title"
    assert updated_task.description == "New description"


def test_complete_command():
    """Test the complete command."""
    from src.core.task_manager import TaskManager

    tm = TaskManager()
    task = tm.add_task("Test task")

    # Mark as complete in our manager
    completed_task = tm.mark_complete(task.id)

    assert completed_task is not None
    assert completed_task.status == "completed"


def test_delete_command():
    """Test the delete command."""
    from src.core.task_manager import TaskManager

    tm = TaskManager()
    task = tm.add_task("Test task")
    original_count = len(tm.get_all_tasks())

    # Delete the task in our manager
    success = tm.delete_task(task.id)

    assert success is True
    assert len(tm.get_all_tasks()) == original_count - 1


def test_status_filtering():
    """Test filtering tasks by status."""
    from src.core.task_manager import TaskManager

    tm = TaskManager()
    task1 = tm.add_task("Pending task")
    task2 = tm.add_task("To complete task")
    tm.mark_complete(task2.id)

    pending_tasks = tm.get_tasks_by_status("pending")
    completed_tasks = tm.get_tasks_by_status("completed")

    assert len(pending_tasks) == 1
    assert pending_tasks[0].id == task1.id

    assert len(completed_tasks) == 1
    assert completed_tasks[0].id == task2.id


def test_validation_errors():
    """Test validation errors in task manager."""
    from src.core.task_manager import TaskManager

    tm = TaskManager()

    # Test empty title
    with pytest.raises(ValueError, match="Title cannot be empty"):
        tm.add_task("")

    # Test long title
    with pytest.raises(ValueError, match="Title exceeds maximum length"):
        tm.add_task("x" * 256)

    # Test long description
    with pytest.raises(ValueError, match="Description exceeds maximum length"):
        tm.add_task("Valid title", "x" * 1001)