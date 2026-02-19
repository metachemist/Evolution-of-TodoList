# Task: T023 — TaskService user-scoped queries and mutations
from datetime import datetime
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
from uuid import UUID

from ..models.task import Task, TaskPriority, TaskStatus
from src.schemas.task import TaskOverviewResponse
from src.utils.datetime_utils import to_naive_utc, utcnow_naive


async def create_task(
    db: AsyncSession,
    user_id: str,
    title: str,
    description: str | None,
    priority: TaskPriority,
    due_date: datetime | None,
    status: TaskStatus,
) -> Task:
    """
    Create a new task for the specified user.
    """
    task = Task(
        title=title,
        description=description,
        priority=priority,
        due_date=to_naive_utc(due_date) if due_date is not None else None,
        focus_minutes=0,
        status=status,
        is_completed=status == TaskStatus.DONE,
        owner_id=UUID(user_id),
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
    priority: TaskPriority | None,
    due_date: datetime | None,
    status: TaskStatus | None,
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
    if priority is not None:
        task.priority = priority
    if due_date is not None:
        task.due_date = to_naive_utc(due_date)
    if status is not None:
        task.status = status
        task.is_completed = status == TaskStatus.DONE
    task.updated_at = utcnow_naive()

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
    task.status = TaskStatus.DONE if task.is_completed else TaskStatus.TODO
    task.updated_at = utcnow_naive()
    
    await db.commit()
    await db.refresh(task)
    
    return task


async def get_tasks_overview(db: AsyncSession, user_id: str) -> TaskOverviewResponse:
    """
    Return aggregate deep-work metrics for the specified user's tasks.
    """
    statement = select(Task).where(Task.owner_id == UUID(user_id))
    result = await db.exec(statement)
    tasks = result.all()

    total_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if task.status == TaskStatus.DONE)
    in_progress_tasks = sum(1 for task in tasks if task.status == TaskStatus.IN_PROGRESS)
    now = utcnow_naive()
    overdue_tasks = sum(
        1
        for task in tasks
        if task.due_date is not None and task.due_date < now and task.status != TaskStatus.DONE
    )
    total_focus_minutes = sum(task.focus_minutes for task in tasks)
    completion_rate = round((completed_tasks / total_tasks) * 100, 2) if total_tasks > 0 else 0.0

    return TaskOverviewResponse(
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        in_progress_tasks=in_progress_tasks,
        overdue_tasks=overdue_tasks,
        total_focus_minutes=total_focus_minutes,
        completion_rate=completion_rate,
    )


async def add_focus_minutes(
    db: AsyncSession,
    user_id: str,
    task_id: str,
    minutes: int,
) -> Task | None:
    """
    Add focused minutes to a task owned by the specified user.
    """
    statement = select(Task).where(
        Task.id == UUID(task_id),
        Task.owner_id == UUID(user_id),
    )
    result = await db.exec(statement)
    task = result.first()

    if not task:
        return None

    task.focus_minutes += minutes
    if task.status == TaskStatus.TODO:
        task.status = TaskStatus.IN_PROGRESS
    task.updated_at = utcnow_naive()

    await db.commit()
    await db.refresh(task)
    return task
