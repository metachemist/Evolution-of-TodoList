"""Initial migration for User and Task models

Revision ID: 001_initial_models
Revises: 
Create Date: 2026-02-07 18:30:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from datetime import datetime

# revision identifiers, used by Alembic.
revision: str = '001_initial_models'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create users table
    op.create_table('user',
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('first_name', sa.String(), nullable=True),
        sa.Column('last_name', sa.String(), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)

    # Create tasks table
    op.create_table('task',
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('completed', sa.Boolean(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_task_user_id'), 'task', ['user_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_task_user_id'), table_name='task')
    op.drop_table('task')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')