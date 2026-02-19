# Task: T064 — align task service tests with AuthService hashing contract
import pytest
from uuid import uuid4

from src.models.user import User
from src.models.task import Task
from src.services.task_service import (
    create_task, get_tasks, get_task_by_id,
    update_task, delete_task, toggle_completion,
)
from src.services.user_service import get_user_by_id
from src.services.auth_service import hash_password as get_password_hash


@pytest.mark.asyncio
async def test_create_task(db_session):
    """create_task persists and returns a Task with correct fields."""
    user = User(email="svc_create@test.com", hashed_password=get_password_hash("pw"))
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    task = await create_task(db_session, str(user.id), "My Task", "Description")
    assert task.title == "My Task"
    assert task.description == "Description"
    assert task.owner_id == user.id
    assert task.is_completed is False
    assert task.id is not None


@pytest.mark.asyncio
async def test_get_tasks(db_session):
    """get_tasks returns only the specified user's tasks."""
    user = User(email="svc_list@test.com", hashed_password=get_password_hash("pw"))
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    await create_task(db_session, str(user.id), "Task 1", None)
    await create_task(db_session, str(user.id), "Task 2", None)

    tasks = await get_tasks(db_session, str(user.id))
    assert len(tasks) == 2
    assert all(t.owner_id == user.id for t in tasks)


@pytest.mark.asyncio
async def test_get_tasks_pagination(db_session):
    """get_tasks respects skip and limit parameters."""
    user = User(email="svc_page@test.com", hashed_password=get_password_hash("pw"))
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    for i in range(5):
        await create_task(db_session, str(user.id), f"Task {i}", None)

    tasks = await get_tasks(db_session, str(user.id), skip=0, limit=3)
    assert len(tasks) == 3

    tasks = await get_tasks(db_session, str(user.id), skip=3, limit=10)
    assert len(tasks) == 2


@pytest.mark.asyncio
async def test_get_task_by_id(db_session):
    """get_task_by_id returns the correct task or None."""
    user = User(email="svc_get@test.com", hashed_password=get_password_hash("pw"))
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    task = await create_task(db_session, str(user.id), "Find", None)
    found = await get_task_by_id(db_session, str(user.id), str(task.id))
    assert found is not None
    assert found.id == task.id

    not_found = await get_task_by_id(db_session, str(user.id), str(uuid4()))
    assert not_found is None


@pytest.mark.asyncio
async def test_update_task(db_session):
    """update_task changes only provided fields."""
    user = User(email="svc_upd@test.com", hashed_password=get_password_hash("pw"))
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    task = await create_task(db_session, str(user.id), "Old", "Old desc")
    original_updated_at = task.updated_at
    updated = await update_task(db_session, str(user.id), str(task.id), "New", None)
    assert updated is not None
    assert updated.title == "New"
    assert updated.description == "Old desc"  # unchanged since we passed None
    assert updated.updated_at.tzinfo is None
    assert updated.updated_at >= original_updated_at


@pytest.mark.asyncio
async def test_delete_task(db_session):
    """delete_task returns True on success, False if not found."""
    user = User(email="svc_del@test.com", hashed_password=get_password_hash("pw"))
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    task = await create_task(db_session, str(user.id), "Delete Me", None)
    assert await delete_task(db_session, str(user.id), str(task.id)) is True
    assert await delete_task(db_session, str(user.id), str(task.id)) is False


@pytest.mark.asyncio
async def test_toggle_completion(db_session):
    """toggle_completion flips is_completed."""
    user = User(email="svc_tog@test.com", hashed_password=get_password_hash("pw"))
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    task = await create_task(db_session, str(user.id), "Toggle", None)
    assert task.is_completed is False

    toggled = await toggle_completion(db_session, str(user.id), str(task.id))
    assert toggled.is_completed is True
    assert toggled.updated_at.tzinfo is None

    toggled_back = await toggle_completion(db_session, str(user.id), str(task.id))
    assert toggled_back.is_completed is False
    assert toggled_back.updated_at.tzinfo is None


@pytest.mark.asyncio
async def test_get_user_by_id(db_session):
    """get_user_by_id returns the user or None."""
    user = User(email="svc_usr@test.com", hashed_password=get_password_hash("pw"))
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    found = await get_user_by_id(db_session, str(user.id))
    assert found is not None
    assert found.email == "svc_usr@test.com"

    not_found = await get_user_by_id(db_session, str(uuid4()))
    assert not_found is None
