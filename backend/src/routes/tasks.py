# Task: T020 — Apply require_authenticated_user to all task routes (FR-011)
# Task: T021 — Add enforce_user_id_match guard before any DB query (SEC-003)
# Task: T022 — TaskService.create_task now receives current_user.id (FR-005)
# Task: T023 — TaskService user-scoped queries (FR-006, SEC-004)
# Spec: @specs/1-specify/phase-2/feature-03-auth-db-monorepo.md (FR-005–FR-007, SEC-003, SEC-004)
# ADR: @history/adr/0013-two-layer-authorization-semantics.md
from fastapi import APIRouter, Depends, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from uuid import UUID

from src.database import get_db_session
from src.models.user import User
from src.middleware.auth import require_authenticated_user
from src.services.task_service import (
    get_tasks, create_task, get_task_by_id, update_task,
    delete_task, toggle_completion,
)
from src.utils.error_mapper import ForbiddenError
from src.schemas.task import TaskCreate, TaskUpdate

router = APIRouter(tags=["tasks"])


def _enforce_user_id_match(user_id: str, current_user: User) -> None:
    """
    Two-layer authorization — Layer 1 (SEC-003):
    Raise ForbiddenError if {user_id} path param does not match authenticated user's id.
    Fires BEFORE any database query — no DB lookup happens on mismatch.
    """
    if str(user_id) != str(current_user.id):
        raise ForbiddenError()


@router.get("/tasks")
async def get_user_tasks(
    user_id: str,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    current_user: User = Depends(require_authenticated_user),
    db: AsyncSession = Depends(get_db_session),
) -> JSONResponse:
    """List tasks for the authenticated user (paginated, newest first)."""
    _enforce_user_id_match(user_id, current_user)
    tasks = await get_tasks(db, str(current_user.id), skip=skip, limit=limit)
    return JSONResponse(
        status_code=200,
        content=jsonable_encoder({"success": True, "data": tasks, "error": None}),
    )


@router.post("/tasks", status_code=201)
async def create_user_task(
    user_id: str,
    task_data: TaskCreate,
    current_user: User = Depends(require_authenticated_user),
    db: AsyncSession = Depends(get_db_session),
) -> JSONResponse:
    """Create a task owned by the authenticated user (FR-005)."""
    _enforce_user_id_match(user_id, current_user)
    task = await create_task(db, str(current_user.id), task_data.title, task_data.description)
    return JSONResponse(
        status_code=201,
        content=jsonable_encoder({"success": True, "data": task, "error": None}),
    )


@router.get("/tasks/{task_id}")
async def get_specific_task(
    user_id: str,
    task_id: UUID,
    current_user: User = Depends(require_authenticated_user),
    db: AsyncSession = Depends(get_db_session),
) -> JSONResponse:
    """
    Get a specific task.
    Two-layer authorization:
      Layer 1: ForbiddenError if user_id path ≠ current_user.id (no DB query)
      Layer 2: TaskNotFoundError (via service) if task_id not owned by user
    """
    _enforce_user_id_match(user_id, current_user)
    task = await get_task_by_id(db, str(current_user.id), str(task_id))
    if not task:
        from src.utils.error_mapper import TaskNotFoundError
        raise TaskNotFoundError()
    return JSONResponse(
        status_code=200,
        content=jsonable_encoder({"success": True, "data": task, "error": None}),
    )


@router.put("/tasks/{task_id}")
async def update_user_task(
    user_id: str,
    task_id: UUID,
    task_data: TaskUpdate,
    current_user: User = Depends(require_authenticated_user),
    db: AsyncSession = Depends(get_db_session),
) -> JSONResponse:
    """Update a task owned by the authenticated user."""
    _enforce_user_id_match(user_id, current_user)
    updated = await update_task(
        db,
        str(current_user.id),
        str(task_id),
        task_data.title,
        task_data.description,
    )
    if not updated:
        from src.utils.error_mapper import TaskNotFoundError
        raise TaskNotFoundError()
    return JSONResponse(
        status_code=200,
        content=jsonable_encoder({"success": True, "data": updated, "error": None}),
    )


@router.delete("/tasks/{task_id}", status_code=204)
async def delete_user_task(
    user_id: str,
    task_id: UUID,
    current_user: User = Depends(require_authenticated_user),
    db: AsyncSession = Depends(get_db_session),
) -> None:
    """Delete a task owned by the authenticated user."""
    _enforce_user_id_match(user_id, current_user)
    success = await delete_task(db, str(current_user.id), str(task_id))
    if not success:
        from src.utils.error_mapper import TaskNotFoundError
        raise TaskNotFoundError()


@router.patch("/tasks/{task_id}/complete")
async def toggle_task_completion(
    user_id: str,
    task_id: UUID,
    current_user: User = Depends(require_authenticated_user),
    db: AsyncSession = Depends(get_db_session),
) -> JSONResponse:
    """Toggle completion status of a task owned by the authenticated user."""
    _enforce_user_id_match(user_id, current_user)
    updated = await toggle_completion(db, str(current_user.id), str(task_id))
    if not updated:
        from src.utils.error_mapper import TaskNotFoundError
        raise TaskNotFoundError()
    return JSONResponse(
        status_code=200,
        content=jsonable_encoder({"success": True, "data": updated, "error": None}),
    )
