"""Initial models

Revision ID: 001_initial_models
Revises: 
Create Date: 2026-02-11 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers
revision = '001_initial_models'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Timestamp policy:
    # Store created_at/updated_at as TIMESTAMP WITHOUT TIME ZONE.
    # Application code normalizes all DB-bound timestamps to naive UTC.
    # Create user table
    op.create_table('user',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    
    # Create task table
    op.create_table('task',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.String(length=5000), nullable=True),
        sa.Column('is_completed', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('owner_id', sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    # Drop task table first (due to foreign key)
    op.drop_table('task')
    
    # Drop user table
    op.drop_table('user')
