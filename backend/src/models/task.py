from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import Index


class Task(SQLModel, table=True):
    """
    Task model representing a todo item with title, optional description, 
    completion status, timestamps, and relationship to a User owner.
    """
    __table_args__ = (
        Index('idx_task_owner_id', 'owner_id'),  # Index on foreign key
        Index('idx_task_created_at', 'created_at'),  # Index on frequently queried field
        Index('idx_task_is_completed', 'is_completed'),  # Index on frequently queried field
    )
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(nullable=False, max_length=255)
    description: Optional[str] = Field(default=None, max_length=5000)
    is_completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Foreign key to User
    owner_id: UUID = Field(
        foreign_key="user.id",
        ondelete="CASCADE",
        nullable=False,
        index=True,
    )
