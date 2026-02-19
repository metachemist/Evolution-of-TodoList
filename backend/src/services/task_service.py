# Task: T023 — TaskService user-scoped queries and mutations
from datetime import datetime

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
from uuid import UUID
from ..models.task import Task


def _utcnow_naive() -> datetime:
    """
    Return UTC time as a timezone-naive datetime.

    The current schema uses TIMESTAMP WITHOUT TIME ZONE, so sending aware
    datetimes (tzinfo=UTC) to asyncpg raises a bind error.
    """
    return datetime.utcnow()


async def create_task(db: AsyncSession, user_id: str, title: str, description: str | None) -> Task:
    """
    Create a new task for the specified user.
    """
    task = Task(
        title=title,
        description=description,
        owner_id=UUID(user_id)
    )
    
    db.add(task)
    await db.commit()
    await db.refresh(task)
    
    return task


async def get_tasks(db: AsyncSession, user_id: str, skip: int = 0, limit: int = 20) -> List[Task]:
    """
    Get paginated tasks for the specified user, ordered by newest first.
    """
    statement = (
        select(Task)
        .where(Task.owner_id == UUID(user_id))
        .order_by(Task.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    result = await db.exec(statement)
    return result.all()


async def get_task_by_id(db: AsyncSession, user_id: str, task_id: str) -> Task | None:
    """
    Get a specific task by its ID for the specified user.
    """
    statement = select(Task).where(
        Task.id == UUID(task_id),
        Task.owner_id == UUID(user_id)
    )
    result = await db.exec(statement)
    return result.first()


async def update_task(
    db: AsyncSession,
    user_id: str,
    task_id: str,
    title: str | None,
    description: str | None,
) -> Task | None:
    """
    Update a specific task for the specified user.
    Only updates fields that are not None.
    """
    statement = select(Task).where(
        Task.id == UUID(task_id),
        Task.owner_id == UUID(user_id)
    )
    result = await db.exec(statement)
    task = result.first()

    if not task:
        return None

    if title is not None:
        task.title = title
    if description is not None:
        task.description = description
    task.updated_at = _utcnow_naive()

    await db.commit()
    await db.refresh(task)

    return task


async def delete_task(db: AsyncSession, user_id: str, task_id: str) -> bool:
    """
    Delete a specific task for the specified user.
    """
    statement = select(Task).where(
        Task.id == UUID(task_id),
        Task.owner_id == UUID(user_id)
    )
    result = await db.exec(statement)
    task = result.first()
    
    if not task:
        return False
    
    await db.delete(task)
    await db.commit()
    
    return True


async def toggle_completion(db: AsyncSession, user_id: str, task_id: str) -> Task | None:
    """
    Toggle the completion status of a specific task for the specified user.
    """
    statement = select(Task).where(
        Task.id == UUID(task_id),
        Task.owner_id == UUID(user_id)
    )
    result = await db.exec(statement)
    task = result.first()
    
    if not task:
        return None
    
    task.is_completed = not task.is_completed
    task.updated_at = _utcnow_naive()
    
    await db.commit()
    await db.refresh(task)
    
    return task
