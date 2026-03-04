# Task: T039 — User service helpers
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Optional
from uuid import UUID
from ..models.user import User


async def get_user_by_id(db: AsyncSession, user_id: str) -> User | None:
    """
    Get a user by their ID.
    """
    statement = select(User).where(User.id == UUID(user_id))
    result = await db.exec(statement)
    return result.first()
