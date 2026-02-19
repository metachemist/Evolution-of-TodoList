# Task: T005 — User SQLModel (id/email/password/timestamps)
# Spec: @specs/1-specify/phase-2/feature-03-auth-db-monorepo.md (FR-018)
from __future__ import annotations

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Index, event
from sqlmodel import Field, SQLModel

from src.utils.datetime_utils import to_naive_utc, utcnow_naive


class User(SQLModel, table=True):
    """
    User model representing a registered user of the system.
    """
    __table_args__ = (
        Index('idx_user_email', 'email'),  # Index on frequently queried field
        Index('idx_user_created_at', 'created_at'),  # Index on frequently queried field
    )
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(max_length=255)
    hashed_password: str
    created_at: datetime = Field(default_factory=utcnow_naive)
    updated_at: datetime = Field(default_factory=utcnow_naive)


@event.listens_for(User, "before_insert")
def _normalize_user_timestamps_on_insert(_mapper, _connection, target: User) -> None:
    if target.created_at is None:
        target.created_at = utcnow_naive()
    else:
        target.created_at = to_naive_utc(target.created_at)

    if target.updated_at is None:
        target.updated_at = utcnow_naive()
    else:
        target.updated_at = to_naive_utc(target.updated_at)


@event.listens_for(User, "before_update")
def _normalize_user_timestamps_on_update(_mapper, _connection, target: User) -> None:
    # Normalize without forcing value churn on every flush.
    if target.created_at is not None and target.created_at.tzinfo is not None:
        target.created_at = to_naive_utc(target.created_at)

    if target.updated_at is None:
        target.updated_at = utcnow_naive()
    elif target.updated_at.tzinfo is not None:
        target.updated_at = to_naive_utc(target.updated_at)
