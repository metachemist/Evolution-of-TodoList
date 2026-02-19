from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional
from datetime import datetime
from uuid import UUID

from src.models.task import TaskPriority, TaskStatus
from src.utils.datetime_utils import to_naive_utc, utcnow_naive


class TaskCreate(BaseModel):
    """Schema for creating new tasks."""
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, min_length=1, max_length=5000)
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM)
    due_date: Optional[datetime] = None
    status: TaskStatus = Field(default=TaskStatus.TODO)

    @field_validator("due_date")
    @classmethod
    def validate_due_date_not_in_past(cls, value: datetime | None) -> datetime | None:
        if value is None:
            return None
        normalized = to_naive_utc(value)
        if normalized < utcnow_naive():
            raise ValueError("Due date cannot be in the past.")
        return normalized


class TaskUpdate(BaseModel):
    """Schema for updating existing tasks."""
    model_config = ConfigDict(str_strip_whitespace=True)

    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, min_length=1, max_length=5000)
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None
    status: Optional[TaskStatus] = None

    @field_validator("due_date")
    @classmethod
    def normalize_due_date(cls, value: datetime | None) -> datetime | None:
        if value is None:
            return None
        return to_naive_utc(value)


class FocusSessionRequest(BaseModel):
    """Schema for recording focused minutes on a task."""
    minutes: int = Field(ge=1, le=240)


class TaskOverviewResponse(BaseModel):
    """Schema for dashboard task progress overview metrics."""
    total_tasks: int
    completed_tasks: int
    in_progress_tasks: int
    overdue_tasks: int
    total_focus_minutes: int
    completion_rate: float


class TaskResponse(BaseModel):
    """Schema for returning task data."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: Optional[str]
    is_completed: bool
    priority: TaskPriority
    due_date: Optional[datetime]
    focus_minutes: int
    status: TaskStatus
    created_at: datetime
    updated_at: datetime
    owner_id: UUID
