"""Delete pre-auth orphan tasks (tasks with no owner)

Revision ID: 003_delete_orphan_tasks
Revises: 002_add_performance_indexes
Create Date: 2026-02-15

Task: T026 (part 1) — FR-019, US6
Spec: @specs/1-specify/phase-2/feature-03-auth-db-monorepo.md (FR-019, US6 acceptance scenarios)
ADR: @history/adr/0014-schema-first-migration-with-orphan-cleanup.md

IRREVERSIBLE: Orphaned task deletion cannot be rolled back.
In this codebase, owner_id has been NOT NULL since migration 001, so no orphan tasks
should exist. This migration is included for spec compliance (FR-019) and as a safety
net in environments that may have had pre-auth data.

See auth-migration-plan.md for rollback playbook.
"""
from alembic import op

revision = "003_delete_orphan_tasks"
down_revision = "002_add_performance_indexes"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Delete any tasks with no owner (pre-auth orphans).
    # This is a no-op in this codebase since owner_id is NOT NULL since migration 001,
    # but is required by FR-019 for environments transitioning from a pre-auth schema.
    op.execute("DELETE FROM task WHERE owner_id IS NULL")
    # IRREVERSIBLE: orphaned task deletion cannot be rolled back — see auth-migration-plan.md


def downgrade() -> None:
    raise NotImplementedError(
        "Orphan task deletion is intentionally irreversible. "
        "Schema rollback only — see specs/2-plan/phase-2/db-schema/auth-migration-plan.md"
    )
