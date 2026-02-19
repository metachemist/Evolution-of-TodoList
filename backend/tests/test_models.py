import pytest
from src.models.user import User
from src.models.task import Task
from uuid import uuid4
from datetime import datetime, timezone
from sqlmodel import select


def test_user_model():
    """Test the User model."""
    user_id = uuid4()
    user = User(
        id=user_id,
        email="test@example.com",
        hashed_password="hashed_password",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
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
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        owner_id=user_id
    )
    
    assert task.id == task_id
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.is_completed is False
    assert task.owner_id == user_id


@pytest.mark.asyncio
async def test_delete_user_cascades_tasks(db_session):
    """Deleting a user must remove owned tasks via DB-level ON DELETE CASCADE."""
    user = User(
        email="cascade@test.com",
        hashed_password="hashed_password",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
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
