# Task: T014 — JWT helper: create_token and decode_token
# Spec: @specs/1-specify/phase-2/feature-03-auth-db-monorepo.md (FR-009, SESS-001)
# ADR: @history/adr/0011-auth-session-transport-and-contract.md
import os
from datetime import datetime, timedelta, timezone
from uuid import UUID

from jose import jwt, ExpiredSignatureError, JWTError

from src.utils.error_mapper import SessionExpiredError, InvalidTokenError

_SECRET_KEY: str = os.getenv("SECRET_KEY", "change-this-secret-in-production-min-32-chars")
_ALGORITHM: str = "HS256"
_TOKEN_LIFETIME_SECONDS: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_SECONDS", "86400"))


def create_token(user_id: UUID, email: str) -> str:
    """
    Issue an HS256 JWT valid for 24 hours (absolute expiry, no refresh).
    Payload: sub=str(user_id), email=email, exp=now()+86400s.
    """
    now = datetime.now(tz=timezone.utc)
    payload = {
        "sub": str(user_id),
        "email": email,
        "exp": now + timedelta(seconds=_TOKEN_LIFETIME_SECONDS),
        "iat": now,
    }
    return jwt.encode(payload, _SECRET_KEY, algorithm=_ALGORITHM)


def decode_token(token: str) -> dict:
    """
    Verify the JWT signature and expiry.

    Returns the decoded payload dict (includes 'sub' and 'email').

    Raises:
        SessionExpiredError — when the token signature is valid but exp has passed.
        InvalidTokenError  — when the token is malformed, has an invalid signature,
                             or is otherwise undecodable.
    """
    try:
        payload = jwt.decode(token, _SECRET_KEY, algorithms=[_ALGORITHM])
        sub = payload.get("sub")
        if not isinstance(sub, str):
            raise InvalidTokenError()
        try:
            UUID(sub)
        except (TypeError, ValueError):
            raise InvalidTokenError()
        return payload
    except ExpiredSignatureError:
        raise SessionExpiredError()
    except JWTError:
        raise InvalidTokenError()
