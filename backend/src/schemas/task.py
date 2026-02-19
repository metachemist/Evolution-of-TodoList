from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


class TaskCreate(BaseModel):
    """Schema for creating new tasks."""
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, min_length=1, max_length=5000)


class TaskUpdate(BaseModel):
    """Schema for updating existing tasks."""
    model_config = ConfigDict(str_strip_whitespace=True)

    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, min_length=1, max_length=5000)


class TaskResponse(BaseModel):
    """Schema for returning task data."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: Optional[str]
    is_completed: bool
    created_at: datetime
    updated_at: datetime
    owner_id: UUID
