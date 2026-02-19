"""Enforce task.owner_id NOT NULL constraint

Revision ID: 004_owner_id_not_null
Revises: 003_delete_orphan_tasks
Create Date: 2026-02-15

Task: T026 (part 2) — FR-019, US6
Spec: @specs/1-specify/phase-2/feature-03-auth-db-monorepo.md (FR-019)
ADR: @history/adr/0014-schema-first-migration-with-orphan-cleanup.md

In this codebase, owner_id has been NOT NULL since migration 001.
This migration is included for spec compliance and to document the intent explicitly.
Running op.alter_column on an already-NOT-NULL column is idempotent.
"""
import sqlalchemy as sa
from alembic import op

revision = "004_owner_id_not_null"
down_revision = "003_delete_orphan_tasks"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Ensure owner_id is NOT NULL (no orphaned tasks remain after migration 003).
    # This is idempotent — the column is already NOT NULL in this codebase.
    if op.get_bind().dialect.name == "sqlite":
        # SQLite does not support ALTER COLUMN ... SET NOT NULL directly.
        # owner_id is already NOT NULL from 001_initial_models, so this remains
        # a no-op for SQLite test databases.
        return
    op.alter_column("task", "owner_id", nullable=False, existing_type=sa.Uuid())


def downgrade() -> None:
    # Schema rollback: make owner_id nullable again (data deleted in 003 is NOT restored)
    if op.get_bind().dialect.name == "sqlite":
        # SQLite downgrade is a no-op to avoid unsupported ALTER COLUMN syntax.
        return
    op.alter_column("task", "owner_id", nullable=True, existing_type=sa.Uuid())
