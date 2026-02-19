# Task: T005 — User model timestamp consistency checks
# Task: T006 — Task model timestamp consistency checks
import pytest
from datetime import datetime, timezone
from uuid import uuid4

from sqlmodel import select

from src.models.task import Task, TaskPriority, TaskStatus
from src.models.user import User
from src.utils.datetime_utils import utcnow_naive


def test_user_model():
    """Test the User model."""
    user_id = uuid4()
    user = User(
        id=user_id,
        email="test@example.com",
        hashed_password="hashed_password",
        created_at=utcnow_naive(),
        updated_at=utcnow_naive(),
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
        priority=TaskPriority.HIGH,
        due_date=None,
        focus_minutes=15,
        status=TaskStatus.IN_PROGRESS,
        created_at=utcnow_naive(),
        updated_at=utcnow_naive(),
        owner_id=user_id,
    )
    
    assert task.id == task_id
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.is_completed is False
    assert task.priority == TaskPriority.HIGH
    assert task.focus_minutes == 15
    assert task.status == TaskStatus.IN_PROGRESS
    assert task.owner_id == user_id


@pytest.mark.asyncio
async def test_delete_user_cascades_tasks(db_session):
    """Deleting a user must remove owned tasks via DB-level ON DELETE CASCADE."""
    user = User(
        email="cascade@test.com",
        hashed_password="hashed_password",
        created_at=utcnow_naive(),
        updated_at=utcnow_naive(),
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    db_session.add_all(
        [
            Task(title="Task A", owner_id=user.id),
            Task(title="Task B", owner_id=user.id),
        ]
    )
    await db_session.commit()

    await db_session.delete(user)
    await db_session.commit()

    result = await db_session.exec(select(Task).where(Task.owner_id == user.id))
    assert result.all() == []


@pytest.mark.asyncio
async def test_aware_timestamps_are_normalized_on_commit(db_session):
    """Aware timestamps are normalized to naive UTC before DB persistence."""
    aware_now = datetime.now(timezone.utc)

    user = User(
        email="tz-normalize@test.com",
        hashed_password="hashed_password",
        created_at=aware_now,
        updated_at=aware_now,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    assert user.created_at.tzinfo is None
    assert user.updated_at.tzinfo is None

    task = Task(
        title="tz normalize",
        owner_id=user.id,
        created_at=aware_now,
        updated_at=aware_now,
    )
    db_session.add(task)
    await db_session.commit()
    await db_session.refresh(task)

    assert task.created_at.tzinfo is None
    assert task.updated_at.tzinfo is None
