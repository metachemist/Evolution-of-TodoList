from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime
from src.models import Task, TaskCreate, TaskUpdate, TaskPublic
from src.db import get_session
from src.auth.auth_handler import get_current_user
from src.models import User

router = APIRouter(tags=["tasks"])


@router.get("/api/tasks", response_model=List[TaskPublic])
async def get_user_tasks(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    """
    Retrieve all tasks for the authenticated user with pagination support.
    Tasks are ordered by creation date (most recent first).
    """
    # Query tasks for the authenticated user with pagination and ordering
    statement = (
        select(Task)
        .where(Task.user_id == current_user.id)
        .order_by(Task.created_at.desc())
        .offset(offset)
        .limit(limit)
    )
    
    result = await session.exec(statement)
    tasks = result.all()

    return tasks


@router.get("/api/tasks/{task_id}", response_model=TaskPublic)
async def get_single_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Retrieve a specific task by ID for the authenticated user.
    """
    # Query for the specific task belonging to the authenticated user
    statement = select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    result = await session.exec(statement)
    task = result.first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.post("/api/tasks", response_model=TaskPublic)
async def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Create a new task for the authenticated user.
    """
    # Create the task with the authenticated user's ID
    task_data_dict = task_data.model_dump()
    task = Task(**task_data_dict)
    task.user_id = current_user.id

    session.add(task)
    await session.commit()
    await session.refresh(task)

    return task


@router.put("/api/tasks/{task_id}", response_model=TaskPublic)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Update a specific task for the authenticated user.
    """
    # Query for the specific task belonging to the authenticated user
    statement = select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    result = await session.exec(statement)
    task = result.first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Update the task with the provided data
    for field, value in task_data.model_dump(exclude_unset=True).items():
        setattr(task, field, value)

    task.updated_at = datetime.utcnow()
    session.add(task)
    await session.commit()
    await session.refresh(task)

    return task


@router.delete("/api/tasks/{task_id}")
async def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Delete a specific task for the authenticated user.
    """
    # Query for the specific task belonging to the authenticated user
    statement = select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    result = await session.exec(statement)
    task = result.first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    await session.delete(task)
    await session.commit()

    return {"message": "Task deleted successfully"}


@router.patch("/api/tasks/{task_id}/complete", response_model=TaskPublic)
async def toggle_task_completion(
    task_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Toggle or set the completion status of a task for the authenticated user.
    """
    # Query for the specific task belonging to the authenticated user
    statement = select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    result = await session.exec(statement)
    task = result.first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Toggle the completion status
    task.completed = not task.completed
    task.updated_at = datetime.utcnow()

    session.add(task)
    await session.commit()
    await session.refresh(task)

    return task