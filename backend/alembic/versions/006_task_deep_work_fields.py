"""Add task priority, due_date, focus_minutes, and status fields.

Revision ID: 006_task_deep_work_fields
Revises: 005_owner_fk_cascade
Create Date: 2026-02-19

Task: T066 — Deep work task model upgrade (priority, due date, status, focus minutes)
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "006_task_deep_work_fields"
down_revision = "005_owner_fk_cascade"
branch_labels = None
depends_on = None

_TASK_TABLE = "task"
_PRIORITY_ENUM = sa.Enum("LOW", "MEDIUM", "HIGH", name="task_priority", native_enum=False)
_STATUS_ENUM = sa.Enum("TODO", "IN_PROGRESS", "DONE", name="task_status", native_enum=False)


def upgrade() -> None:
    with op.batch_alter_table(_TASK_TABLE) as batch_op:
        batch_op.add_column(
            sa.Column(
                "priority",
                _PRIORITY_ENUM,
                nullable=False,
                server_default="MEDIUM",
            )
        )
        batch_op.add_column(sa.Column("due_date", sa.DateTime(), nullable=True))
        batch_op.add_column(
            sa.Column(
                "focus_minutes",
                sa.Integer(),
                nullable=False,
                server_default="0",
            )
        )
        batch_op.add_column(
            sa.Column(
                "status",
                _STATUS_ENUM,
                nullable=False,
                server_default="TODO",
            )
        )

    dialect = op.get_bind().dialect.name
    if dialect == "sqlite":
        op.execute("UPDATE task SET status = 'DONE' WHERE is_completed = 1")
    else:
        op.execute("UPDATE task SET status = 'DONE' WHERE is_completed = true")

    op.create_index("idx_task_priority", _TASK_TABLE, ["priority"])
    op.create_index("idx_task_status", _TASK_TABLE, ["status"])


def downgrade() -> None:
    op.drop_index("idx_task_status", table_name=_TASK_TABLE)
    op.drop_index("idx_task_priority", table_name=_TASK_TABLE)

    with op.batch_alter_table(_TASK_TABLE) as batch_op:
        batch_op.drop_column("status")
        batch_op.drop_column("focus_minutes")
        batch_op.drop_column("due_date")
        batch_op.drop_column("priority")
