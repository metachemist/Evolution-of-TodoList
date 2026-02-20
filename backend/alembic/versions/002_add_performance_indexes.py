"""Add performance indexes for email, owner_id, and task query fields

Revision ID: 002_add_performance_indexes
Revises: 001_initial_models
Create Date: 2026-02-15

Task: T008 — PERF-004 — ensure indexes exist on all FK and frequently queried fields.
The 001 migration creates tables but does not explicitly create the named indexes
that the SQLModel __table_args__ definitions reference.
"""
from alembic import op

revision = "002_add_performance_indexes"
down_revision = "001_initial_models"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Index on user.email for fast login lookup (unique constraint implies one index,
    # but we add an explicit named index for ORM compatibility)
    op.create_index("ix_user_email", "user", ["email"], unique=True, if_not_exists=True)

    # Index on task.owner_id for fast per-user task queries (PERF-004, US2 isolation)
    op.create_index("ix_task_owner_id", "task", ["owner_id"], if_not_exists=True)

    # Index on task.is_completed for filtered list queries
    op.create_index("ix_task_is_completed", "task", ["is_completed"], if_not_exists=True)

    # Index on task.created_at for newest-first ordering
    op.create_index("ix_task_created_at", "task", ["created_at"], if_not_exists=True)


def downgrade() -> None:
    op.drop_index("ix_task_created_at", table_name="task", if_exists=True)
    op.drop_index("ix_task_is_completed", table_name="task", if_exists=True)
    op.drop_index("ix_task_owner_id", table_name="task", if_exists=True)
    op.drop_index("ix_user_email", table_name="user", if_exists=True)
