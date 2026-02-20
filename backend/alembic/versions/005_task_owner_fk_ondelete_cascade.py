"""Set task.owner_id foreign key to ON DELETE CASCADE.

Revision ID: 005_owner_fk_cascade
Revises: 004_owner_id_not_null
Create Date: 2026-02-18

Task: T026 (schema hardening follow-up) — align task ownership FK behavior
Spec: @specs/1-specify/phase-2/feature-03-auth-db-monorepo.md (user data isolation lifecycle)
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = "005_owner_fk_cascade"
down_revision = "004_owner_id_not_null"
branch_labels = None
depends_on = None

_TASK_TABLE = "task"
_USER_TABLE = "user"
_OWNER_COLUMN = "owner_id"
_FK_NAME = "fk_task_owner_id_user_id"


def _find_owner_fk() -> dict | None:
    """Return the FK metadata for task.owner_id -> user.id, if present."""
    inspector = sa.inspect(op.get_bind())
    for fk in inspector.get_foreign_keys(_TASK_TABLE):
        if (
            fk.get("referred_table") == _USER_TABLE
            and fk.get("constrained_columns") == [_OWNER_COLUMN]
        ):
            return fk
    return None


def upgrade() -> None:
    if op.get_bind().dialect.name == "sqlite":
        # SQLite cannot reliably alter existing FK constraints in-place.
        # Keep this as a no-op for SQLite E2E databases.
        return
    fk = _find_owner_fk()
    if fk:
        options = fk.get("options") or {}
        ondelete = (options.get("ondelete") or "").upper()
        if ondelete == "CASCADE":
            return
        fk_name = fk.get("name")
        if fk_name:
            op.drop_constraint(fk_name, _TASK_TABLE, type_="foreignkey")

    op.create_foreign_key(
        _FK_NAME,
        _TASK_TABLE,
        _USER_TABLE,
        [_OWNER_COLUMN],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    if op.get_bind().dialect.name == "sqlite":
        return
    fk = _find_owner_fk()
    if fk and fk.get("name"):
        op.drop_constraint(fk["name"], _TASK_TABLE, type_="foreignkey")

    op.create_foreign_key(
        _FK_NAME,
        _TASK_TABLE,
        _USER_TABLE,
        [_OWNER_COLUMN],
        ["id"],
    )
