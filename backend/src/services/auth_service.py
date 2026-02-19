# Task: T012 — AuthService validation methods (normalize_email, validate_email_format, validate_password)
# Task: T013 — AuthService data methods (hash_password, verify_password, create_user, get_user_by_email)
# Spec: @specs/1-specify/phase-2/feature-03-auth-db-monorepo.md (FR-001, FR-002, FR-012, FR-013)
# ADR: @history/adr/0011-auth-session-transport-and-contract.md (Argon2id params)
import re

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHashError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models.user import User
from src.utils.error_mapper import ValidationError, PasswordValidationError

# ---------------------------------------------------------------------------
# Argon2id hasher — Benchmark result: hash ≤ 250ms, verify ≤ 250ms on dev hardware.
# Parameters fixed at baseline (time_cost=3, memory_cost=65536 KiB, parallelism=2).
# Per ADR-0011: never lower these parameters without a new ADR.
# ---------------------------------------------------------------------------
_ph = PasswordHasher(time_cost=3, memory_cost=65536, parallelism=2)

_EMAIL_RE = re.compile(
    r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$"
)


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------

def normalize_email(email: str) -> str:
    """Lowercase and strip whitespace from an email address (FR-012)."""
    return email.lower().strip()


def validate_email_format(email: str) -> None:
    """
    Raise ValidationError if the email does not match a basic RFC-5321 pattern.
    Must be called on the already-normalized (lowercase) email.
    """
    if not _EMAIL_RE.match(email):
        raise ValidationError()


def validate_password(password: str) -> None:
    """
    Enforce password policy (FR-012):
    - Minimum 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit

    Each rule is checked independently so the error message is consistent.
    Raises PasswordValidationError if any rule fails.
    """
    if (
        len(password) < 8
        or not any(c.isupper() for c in password)
        or not any(c.islower() for c in password)
        or not any(c.isdigit() for c in password)
    ):
        raise PasswordValidationError()


# ---------------------------------------------------------------------------
# Password hashing
# ---------------------------------------------------------------------------

def hash_password(password: str) -> str:
    """
    Hash a plain-text password with Argon2id.
    Returns an encoded Argon2 hash string safe to store in the database.
    Per FR-013: passwords MUST never be stored in plain text.
    """
    return _ph.hash(password)


def verify_password(hashed: str, password: str) -> bool:
    """
    Verify a plain-text password against an Argon2id hash.
    Returns True on match, False on mismatch.
    Never raises — exceptions from argon2-cffi are caught and treated as mismatch.
    """
    try:
        return _ph.verify(hashed, password)
    except (VerifyMismatchError, VerificationError, InvalidHashError):
        return False


# ---------------------------------------------------------------------------
# Database operations
# ---------------------------------------------------------------------------

async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    """Look up a user by their normalized email address."""
    statement = select(User).where(User.email == email)
    result = await db.exec(statement)
    return result.first()


async def get_user_by_id(db: AsyncSession, user_id: str) -> User | None:
    """Look up a user by their UUID (string form acceptable for SQLModel UUID field)."""
    from uuid import UUID as _UUID
    statement = select(User).where(User.id == _UUID(user_id))
    result = await db.exec(statement)
    return result.first()


async def create_user(db: AsyncSession, email: str, hashed_password: str) -> User:
    """
    Persist a new User with an already-hashed password.
    The caller is responsible for hashing via hash_password() before calling this.
    """
    user = User(email=email, hashed_password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
