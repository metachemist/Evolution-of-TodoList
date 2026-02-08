from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any, Optional
from datetime import datetime
from sqlmodel import Session, select
from ..models import Task, TaskCreate, TaskUpdate, TaskPublic, User
from ..db import get_session
from ..auth import get_current_user


router = APIRouter(prefix="/mcp/tools", tags=["mcp-tools"])


@router.post("/create_task")
async def mcp_create_task(
    user_id: int,
    title: str,
    description: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> Dict[str, Any]:
    """
    MCP tool for creating a new task for the authenticated user.
    
    Args:
        user_id: The ID of the user creating the task
        title: The title of the task
        description: Optional description of the task
        current_user: The authenticated user
        session: Database session
    
    Returns:
        Dictionary with success status and task data
    """
    # Verify that the user_id matches the authenticated user's ID
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Access denied: Cannot create tasks for another user")
    
    # Validate input
    if not title or len(title.strip()) == 0:
        raise HTTPException(status_code=400, detail="Title is required and cannot be empty")
    
    if len(title) > 200:
        raise HTTPException(status_code=400, detail="Title exceeds maximum length of 200 characters")
    
    if description and len(description) > 1000:
        raise HTTPException(status_code=400, detail="Description exceeds maximum length of 1000 characters")
    
    # Create the task
    task = Task(
        title=title.strip(),
        description=description,
        user_id=user_id,
        completed=False
    )
    
    session.add(task)
    await session.commit()
    await session.refresh(task)
    
    # Prepare response
    response_data = {
        "success": True,
        "data": {
            "id": task.id,
            "user_id": task.user_id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat()
        },
        "metadata": {
            "tool_name": "create_task",
            "timestamp": datetime.utcnow().isoformat(),
            "execution_time_ms": 0  # Placeholder, actual timing would be measured
        }
    }
    
    return response_data


@router.post("/get_user_tasks")
async def mcp_get_user_tasks(
    user_id: int,
    limit: int = 20,
    offset: int = 0,
    completed: Optional[bool] = None,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> Dict[str, Any]:
    """
    MCP tool for retrieving all tasks for the specified user.
    
    Args:
        user_id: The ID of the user whose tasks to retrieve
        limit: Number of tasks to return per page (default: 20, max: 100)
        offset: Number of tasks to skip (for pagination, default: 0)
        completed: Filter by completion status (true/false/all, default: None)
        current_user: The authenticated user
        session: Database session
    
    Returns:
        Dictionary with success status and tasks data
    """
    # Verify that the user_id matches the authenticated user's ID
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Access denied: Cannot access another user's tasks")
    
    # Validate parameters
    if limit <= 0 or limit > 100:
        raise HTTPException(status_code=400, detail="Limit must be between 1 and 100")
    
    if offset < 0:
        raise HTTPException(status_code=400, detail="Offset must be greater than or equal to 0")
    
    # Build query
    query = select(Task).where(Task.user_id == user_id)
    
    # Apply completion filter if specified
    if completed is not None:
        query = query.where(Task.completed == completed)
    
    # Apply ordering and pagination
    query = query.order_by(Task.created_at.desc()).offset(offset).limit(limit)
    
    result = await session.execute(query)
    tasks = result.scalars().all()
    
    # Count total tasks for pagination metadata
    count_query = select(Task).where(Task.user_id == user_id)
    if completed is not None:
        count_query = count_query.where(Task.completed == completed)
    
    count_result = await session.execute(count_query)
    total_count = len(count_result.scalars().all())
    
    # Convert tasks to dict format
    tasks_list = []
    for task in tasks:
        tasks_list.append({
            "id": task.id,
            "user_id": task.user_id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat()
        })
    
    # Prepare response
    response_data = {
        "success": True,
        "data": {
            "tasks": tasks_list,
            "pagination": {
                "total": total_count,
                "limit": limit,
                "offset": offset,
                "has_more": (offset + limit) < total_count
            }
        },
        "metadata": {
            "tool_name": "get_user_tasks",
            "timestamp": datetime.utcnow().isoformat(),
            "execution_time_ms": 0  # Placeholder, actual timing would be measured
        }
    }
    
    return response_data


@router.post("/get_task")
async def mcp_get_task(
    user_id: int,
    task_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> Dict[str, Any]:
    """
    MCP tool for retrieving a specific task by ID for the specified user.
    
    Args:
        user_id: The ID of the user who owns the task
        task_id: The ID of the task to retrieve
        current_user: The authenticated user
        session: Database session
    
    Returns:
        Dictionary with success status and task data
    """
    # Verify that the user_id matches the authenticated user's ID
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Access denied: Cannot access another user's tasks")
    
    # Query for the specific task
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    result = await session.execute(statement)
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Prepare response
    response_data = {
        "success": True,
        "data": {
            "id": task.id,
            "user_id": task.user_id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat()
        },
        "metadata": {
            "tool_name": "get_task",
            "timestamp": datetime.utcnow().isoformat(),
            "execution_time_ms": 0  # Placeholder, actual timing would be measured
        }
    }
    
    return response_data


@router.post("/update_task")
async def mcp_update_task(
    user_id: int,
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    completed: Optional[bool] = None,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> Dict[str, Any]:
    """
    MCP tool for updating an existing task for the authenticated user.
    
    Args:
        user_id: The ID of the user who owns the task
        task_id: The ID of the task to update
        title: Optional new title for the task
        description: Optional new description for the task
        completed: Optional new completion status for the task
        current_user: The authenticated user
        session: Database session
    
    Returns:
        Dictionary with success status and updated task data
    """
    # Verify that the user_id matches the authenticated user's ID
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Access denied: Cannot update another user's tasks")
    
    # Query for the specific task
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    result = await session.execute(statement)
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Update the task with the provided data
    if title is not None:
        if len(title.strip()) == 0:
            raise HTTPException(status_code=400, detail="Title cannot be empty")
        
        if len(title) > 200:
            raise HTTPException(status_code=400, detail="Title exceeds maximum length of 200 characters")
        
        task.title = title.strip()
    
    if description is not None:
        if len(description) > 1000:
            raise HTTPException(status_code=400, detail="Description exceeds maximum length of 1000 characters")
        
        task.description = description
    
    if completed is not None:
        task.completed = completed
    
    task.updated_at = datetime.utcnow()
    session.add(task)
    await session.commit()
    await session.refresh(task)
    
    # Prepare response
    response_data = {
        "success": True,
        "data": {
            "id": task.id,
            "user_id": task.user_id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat()
        },
        "metadata": {
            "tool_name": "update_task",
            "timestamp": datetime.utcnow().isoformat(),
            "execution_time_ms": 0  # Placeholder, actual timing would be measured
        }
    }
    
    return response_data


@router.post("/delete_task")
async def mcp_delete_task(
    user_id: int,
    task_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> Dict[str, Any]:
    """
    MCP tool for deleting a specific task for the authenticated user.
    
    Args:
        user_id: The ID of the user who owns the task
        task_id: The ID of the task to delete
        current_user: The authenticated user
        session: Database session
    
    Returns:
        Dictionary with success status and message
    """
    # Verify that the user_id matches the authenticated user's ID
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Access denied: Cannot delete another user's tasks")
    
    # Query for the specific task
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    result = await session.execute(statement)
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    session.delete(task)
    await session.commit()
    
    # Prepare response
    response_data = {
        "success": True,
        "data": {
            "message": "Task deleted successfully"
        },
        "metadata": {
            "tool_name": "delete_task",
            "timestamp": datetime.utcnow().isoformat(),
            "execution_time_ms": 0  # Placeholder, actual timing would be measured
        }
    }
    
    return response_data


@router.post("/toggle_task_completion")
async def mcp_toggle_task_completion(
    user_id: int,
    task_id: int,
    completed: bool,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> Dict[str, Any]:
    """
    MCP tool for toggling or setting the completion status of a task.
    
    Args:
        user_id: The ID of the user who owns the task
        task_id: The ID of the task to update
        completed: The new completion status for the task
        current_user: The authenticated user
        session: Database session
    
    Returns:
        Dictionary with success status and updated task data
    """
    # Verify that the user_id matches the authenticated user's ID
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Access denied: Cannot modify another user's tasks")
    
    # Query for the specific task
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    result = await session.execute(statement)
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Update the completion status
    task.completed = completed
    task.updated_at = datetime.utcnow()
    
    session.add(task)
    await session.commit()
    await session.refresh(task)
    
    # Prepare response
    response_data = {
        "success": True,
        "data": {
            "id": task.id,
            "user_id": task.user_id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat()
        },
        "metadata": {
            "tool_name": "toggle_task_completion",
            "timestamp": datetime.utcnow().isoformat(),
            "execution_time_ms": 0  # Placeholder, actual timing would be measured
        }
    }
    
    return response_data