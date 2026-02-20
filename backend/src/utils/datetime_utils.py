# Task: T005 — User SQLModel foundational fields
# Task: T006 — Task SQLModel foundational fields
# Task: T023 — Task service timestamp mutation safety
# Spec: @specs/1-specify/phase-2/feature-03-auth-db-monorepo.md (FR-018, FR-019)
from __future__ import annotations

from datetime import datetime, timezone


def utcnow_naive() -> datetime:
    """
    Return current UTC time as timezone-naive.

    The current Postgres schema uses TIMESTAMP WITHOUT TIME ZONE for
    created_at/updated_at fields, so DB-bound values must be naive.
    """
    return datetime.now(timezone.utc).replace(tzinfo=None)


def to_naive_utc(value: datetime) -> datetime:
    """
    Normalize any datetime to naive UTC.

    - Aware values are converted to UTC and stripped of tzinfo.
    - Naive values are returned unchanged.
    """
    if value.tzinfo is None:
        return value
    return value.astimezone(timezone.utc).replace(tzinfo=None)
