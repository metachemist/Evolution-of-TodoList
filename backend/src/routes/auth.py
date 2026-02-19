# Task: T015 — POST /api/auth/register
# Task: T016 — POST /api/auth/login
# Task: T017 — POST /api/auth/logout
# Task: T018 — GET /api/auth/me
# Spec: @specs/1-specify/phase-2/feature-03-auth-db-monorepo.md (FR-001–FR-016, FR-012)
# Contracts: @specs/2-plan/phase-2/api-specs/auth-and-task-contracts.md
import os

from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlmodel.ext.asyncio.session import AsyncSession

from src.database import get_db_session
from src.services.auth_service import (
    normalize_email,
    validate_email_format,
    validate_password,
    hash_password,
    verify_password,
    get_user_by_email,
    get_user_by_id,
    create_user,
)
from src.utils.token import create_token, decode_token
from src.utils.error_mapper import (
    EmailAlreadyExistsError,
    InvalidCredentialsError,
    UnauthorizedError,
)

router = APIRouter(tags=["auth"])

_COOKIE_SECURE = os.getenv("COOKIE_SECURE", "false").lower() == "true"
_COOKIE_DOMAIN = os.getenv("COOKIE_DOMAIN", None)
_COOKIE_MAX_AGE = int(os.getenv("ACCESS_TOKEN_EXPIRE_SECONDS", "86400"))


# ---------------------------------------------------------------------------
# Request schemas
# ---------------------------------------------------------------------------

class RegisterRequest(BaseModel):
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


# ---------------------------------------------------------------------------
# Cookie helper
# ---------------------------------------------------------------------------

def _set_auth_cookie(response: Response, token: str) -> None:
    """Attach the httpOnly auth cookie to a response (FR-003, SEC-001)."""
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=_COOKIE_SECURE,
        samesite="lax",
        max_age=_COOKIE_MAX_AGE,
        path="/",
        domain=_COOKIE_DOMAIN,
    )


def _clear_auth_cookie(response: Response) -> None:
    """Clear the httpOnly auth cookie (FR-010)."""
    response.set_cookie(
        key="access_token",
        value="",
        httponly=True,
        secure=_COOKIE_SECURE,
        samesite="lax",
        max_age=0,
        path="/",
        domain=_COOKIE_DOMAIN,
    )


# ---------------------------------------------------------------------------
# POST /api/auth/register
# ---------------------------------------------------------------------------

@router.post("/register", status_code=201)
async def register(
    body: RegisterRequest,
    db: AsyncSession = Depends(get_db_session),
) -> JSONResponse:
    """Register a new user; set httpOnly cookie; return token in body for non-browser clients."""
    # Normalize + validate (FR-012)
    email = normalize_email(body.email)
    validate_email_format(email)   # raises ValidationError → 400 via global handler
    validate_password(body.password)  # raises PasswordValidationError → 400

    # Duplicate check (FR-001)
    existing = await get_user_by_email(db, email)
    if existing:
        raise EmailAlreadyExistsError()

    # Hash + persist
    hashed = hash_password(body.password)
    user = await create_user(db, email, hashed)

    # Issue token
    token = create_token(user.id, user.email)

    response = JSONResponse(
        status_code=201,
        content={
            "success": True,
            "data": {"access_token": token, "token_type": "bearer"},
            "error": None,
        },
    )
    _set_auth_cookie(response, token)
    return response


# ---------------------------------------------------------------------------
# POST /api/auth/login
# ---------------------------------------------------------------------------

@router.post("/login", status_code=200)
async def login(
    body: LoginRequest,
    db: AsyncSession = Depends(get_db_session),
) -> JSONResponse:
    """Authenticate; set httpOnly cookie; return token in body for non-browser clients."""
    email = normalize_email(body.email)
    user = await get_user_by_email(db, email)

    # Do not distinguish missing user vs wrong password (avoid user enumeration)
    if not user or not verify_password(user.hashed_password, body.password):
        raise InvalidCredentialsError()

    token = create_token(user.id, user.email)

    response = JSONResponse(
        status_code=200,
        content={
            "success": True,
            "data": {"access_token": token, "token_type": "bearer"},
            "error": None,
        },
    )
    _set_auth_cookie(response, token)
    return response


# ---------------------------------------------------------------------------
# POST /api/auth/logout
# ---------------------------------------------------------------------------

@router.post("/logout", status_code=200)
async def logout() -> JSONResponse:
    """
    Clear the auth cookie. Always returns 200 regardless of cookie state (FR-010).
    No DB query required — stateless logout.
    """
    response = JSONResponse(
        status_code=200,
        content={"success": True, "data": {"logged_out": True}, "error": None},
    )
    _clear_auth_cookie(response)
    return response


# ---------------------------------------------------------------------------
# GET /api/auth/me
# ---------------------------------------------------------------------------

@router.get("/me", status_code=200)
async def me(
    request: Request,
    db: AsyncSession = Depends(get_db_session),
) -> JSONResponse:
    """
    Return the authenticated user's id and email.
    Auth precedence: Bearer header first, then access_token cookie.
    Raises SessionExpiredError or InvalidTokenError (both → 401) via global handler.
    """
    token: str | None = None

    # 1. Check Authorization header
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header[7:]

    # 2. Fall back to cookie
    if not token:
        token = request.cookies.get("access_token")

    if not token:
        raise UnauthorizedError()

    # Raises SessionExpiredError or InvalidTokenError on failure (FR-004)
    payload = decode_token(token)
    user_id: str = payload.get("sub", "")

    user = await get_user_by_id(db, user_id)
    if not user:
        raise UnauthorizedError()

    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "data": {"id": str(user.id), "email": user.email},
            "error": None,
        },
    )
