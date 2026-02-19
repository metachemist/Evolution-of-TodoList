# Task: T019 — require_authenticated_user FastAPI Depends() dependency
# Spec: @specs/1-specify/phase-2/feature-03-auth-db-monorepo.md (FR-004, FR-011, SEC-002)
# ADR: @history/adr/0011-auth-session-transport-and-contract.md (Bearer > cookie precedence)
from fastapi import Depends, Request
from sqlmodel.ext.asyncio.session import AsyncSession

from src.database import get_db_session
from src.models.user import User
from src.services.auth_service import get_user_by_id
from src.utils.token import decode_token
from src.utils.error_mapper import UnauthorizedError


async def require_authenticated_user(
    request: Request,
    db: AsyncSession = Depends(get_db_session),
) -> User:
    """
    FastAPI Depends()-based auth guard that resolves the current authenticated user.

    Auth precedence (ADR-0011):
      1. Authorization: Bearer <token>  — for non-browser clients
      2. access_token httpOnly cookie   — for browser clients

    Returns the User ORM object so route handlers can access user.id, user.email, etc.

    Raises:
        UnauthorizedError   — no credential present
        SessionExpiredError — valid-format token but past expiry
        InvalidTokenError   — malformed or tampered token
    All raised exceptions are subclasses of AppException and handled by the global handler.
    """
    token: str | None = None

    # 1. Bearer header takes precedence
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header[7:]

    # 2. Fallback to httpOnly cookie
    if not token:
        token = request.cookies.get("access_token")

    if not token:
        raise UnauthorizedError()

    # Raises SessionExpiredError or InvalidTokenError on bad token
    payload = decode_token(token)
    user_id: str = payload.get("sub", "")

    user = await get_user_by_id(db, user_id)
    if not user:
        # Token signed correctly but user deleted — treat as unauthorized
        raise UnauthorizedError()

    return user
