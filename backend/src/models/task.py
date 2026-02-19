# Task: T006 — Task SQLModel (owner relationship and timestamps)
# Spec: @specs/1-specify/phase-2/feature-03-auth-db-monorepo.md (FR-018, FR-019)
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import Column, Enum as SAEnum, Index, event
from sqlmodel import Field, SQLModel

from src.utils.datetime_utils import to_naive_utc, utcnow_naive


class TaskPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class TaskStatus(str, Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class Task(SQLModel, table=True):
    """
    Task model representing a todo item with title, optional description, 
    completion status, timestamps, and relationship to a User owner.
    """
    __table_args__ = (
        Index('idx_task_owner_id', 'owner_id'),  # Index on foreign key
        Index('idx_task_created_at', 'created_at'),  # Index on frequently queried field
        Index('idx_task_is_completed', 'is_completed'),  # Index on frequently queried field
        Index('idx_task_priority', 'priority'),  # Index on frequently queried field
        Index('idx_task_status', 'status'),  # Index on frequently queried field
    )
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(nullable=False, max_length=255)
    description: Optional[str] = Field(default=None, max_length=5000)
    is_completed: bool = Field(default=False)
    priority: TaskPriority = Field(
        default=TaskPriority.MEDIUM,
        sa_column=Column(
            SAEnum(TaskPriority, name="task_priority", native_enum=False),
            nullable=False,
            default=TaskPriority.MEDIUM,
        ),
    )
    due_date: Optional[datetime] = Field(default=None)
    focus_minutes: int = Field(default=0, ge=0)
    status: TaskStatus = Field(
        default=TaskStatus.TODO,
        sa_column=Column(
            SAEnum(TaskStatus, name="task_status", native_enum=False),
            nullable=False,
            default=TaskStatus.TODO,
        ),
    )
    created_at: datetime = Field(default_factory=utcnow_naive)
    updated_at: datetime = Field(default_factory=utcnow_naive)
    
    # Foreign key to User
    owner_id: UUID = Field(
        foreign_key="user.id",
        ondelete="CASCADE",
        nullable=False,
        index=True,
    )


@event.listens_for(Task, "before_insert")
def _normalize_task_timestamps_on_insert(_mapper, _connection, target: Task) -> None:
    if target.created_at is None:
        target.created_at = utcnow_naive()
    else:
        target.created_at = to_naive_utc(target.created_at)

    if target.updated_at is None:
        target.updated_at = utcnow_naive()
    else:
        target.updated_at = to_naive_utc(target.updated_at)

    if target.due_date is not None:
        target.due_date = to_naive_utc(target.due_date)


@event.listens_for(Task, "before_update")
def _normalize_task_timestamps_on_update(_mapper, _connection, target: Task) -> None:
    # Normalize without forcing value churn on every flush.
    if target.created_at is not None and target.created_at.tzinfo is not None:
        target.created_at = to_naive_utc(target.created_at)

    if target.updated_at is None:
        target.updated_at = utcnow_naive()
    elif target.updated_at.tzinfo is not None:
        target.updated_at = to_naive_utc(target.updated_at)

    if target.due_date is not None and target.due_date.tzinfo is not None:
        target.due_date = to_naive_utc(target.due_date)
