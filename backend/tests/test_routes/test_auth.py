# Task: T032 — Register endpoint test scenarios
# Task: T033 — Login/logout/me endpoint test scenarios + error catalog exactness
# Spec: @specs/1-specify/phase-2/feature-03-auth-db-monorepo.md (FR-001–FR-016, Error Message Catalog)
import time
from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest
from jose import jwt

from src.utils.token import _SECRET_KEY, _ALGORITHM


# ── Helpers ──────────────────────────────────────────────────────────────────

REGISTER_URL = "/api/auth/register"
LOGIN_URL = "/api/auth/login"
LOGOUT_URL = "/api/auth/logout"
ME_URL = "/api/auth/me"

VALID_EMAIL = "testuser@example.com"
VALID_PASSWORD = "SecurePass1"


def _make_expired_token(user_id: str, email: str) -> str:
    """Issue a JWT that is already past its expiry."""
    payload = {
        "sub": user_id,
        "email": email,
        "exp": datetime.now(tz=timezone.utc) - timedelta(seconds=1),
    }
    return jwt.encode(payload, _SECRET_KEY, algorithm=_ALGORITHM)


def _make_tampered_token() -> str:
    """Return a syntactically valid JWT with a wrong signature."""
    payload = {"sub": str(uuid4()), "email": "x@y.com", "exp": int(time.time()) + 3600}
    return jwt.encode(payload, "wrong-secret-key", algorithm="HS256")


def _make_signed_token_with_malformed_sub() -> str:
    """Return a correctly signed token whose sub claim is not a UUID."""
    payload = {
        "sub": "not-a-uuid",
        "email": "x@y.com",
        "exp": int(time.time()) + 3600,
    }
    return jwt.encode(payload, _SECRET_KEY, algorithm=_ALGORITHM)


# ── Registration (T032) ───────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_register_success(client):
    """201 with wrapped body and httpOnly cookie set."""
    resp = await client.post(REGISTER_URL, json={"email": VALID_EMAIL, "password": VALID_PASSWORD})
    assert resp.status_code == 201
    body = resp.json()
    assert body["success"] is True
    assert "access_token" in body["data"]
    assert body["data"]["token_type"] == "bearer"
    assert body["error"] is None
    assert "access_token" in resp.cookies


@pytest.mark.asyncio
async def test_register_duplicate_email(client):
    """409 EMAIL_ALREADY_EXISTS with exact catalog message."""
    await client.post(REGISTER_URL, json={"email": VALID_EMAIL, "password": VALID_PASSWORD})
    resp = await client.post(REGISTER_URL, json={"email": VALID_EMAIL, "password": VALID_PASSWORD})
    assert resp.status_code == 409
    body = resp.json()
    assert body["success"] is False
    assert body["error"]["code"] == "EMAIL_ALREADY_EXISTS"
    assert body["error"]["message"] == "An account with this email already exists. Please log in instead."


@pytest.mark.asyncio
async def test_register_invalid_email_format(client):
    """400 VALIDATION_ERROR with exact email message."""
    resp = await client.post(REGISTER_URL, json={"email": "not-an-email", "password": VALID_PASSWORD})
    assert resp.status_code == 400
    body = resp.json()
    assert body["error"]["code"] == "VALIDATION_ERROR"
    assert body["error"]["message"] == "Please enter a valid email address."


@pytest.mark.asyncio
async def test_register_password_too_short(client):
    """400 VALIDATION_ERROR for password < 8 chars."""
    resp = await client.post(REGISTER_URL, json={"email": "short@example.com", "password": "Ab1"})
    assert resp.status_code == 400
    assert resp.json()["error"]["code"] == "VALIDATION_ERROR"


@pytest.mark.asyncio
async def test_register_password_missing_uppercase(client):
    """400 VALIDATION_ERROR for password without uppercase."""
    resp = await client.post(REGISTER_URL, json={"email": "upper@example.com", "password": "alllower1"})
    assert resp.status_code == 400
    body = resp.json()
    assert body["error"]["code"] == "VALIDATION_ERROR"
    assert "uppercase" in body["error"]["message"]


@pytest.mark.asyncio
async def test_register_email_normalized_to_lowercase(client):
    """Email is normalized to lowercase before storage."""
    await client.post(REGISTER_URL, json={"email": "CAPS@EXAMPLE.COM", "password": VALID_PASSWORD})
    resp = await client.post(LOGIN_URL, json={"email": "caps@example.com", "password": VALID_PASSWORD})
    assert resp.status_code == 200


# ── Login (T033) ──────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_login_success(client):
    """200 with cookie and wrapped body."""
    await client.post(REGISTER_URL, json={"email": VALID_EMAIL, "password": VALID_PASSWORD})
    resp = await client.post(LOGIN_URL, json={"email": VALID_EMAIL, "password": VALID_PASSWORD})
    assert resp.status_code == 200
    body = resp.json()
    assert body["success"] is True
    assert "access_token" in body["data"]
    assert "access_token" in resp.cookies


@pytest.mark.asyncio
async def test_login_wrong_password(client):
    """401 INVALID_CREDENTIALS with exact catalog message."""
    await client.post(REGISTER_URL, json={"email": VALID_EMAIL, "password": VALID_PASSWORD})
    resp = await client.post(LOGIN_URL, json={"email": VALID_EMAIL, "password": "WrongPass1"})
    assert resp.status_code == 401
    body = resp.json()
    assert body["error"]["code"] == "INVALID_CREDENTIALS"
    assert body["error"]["message"] == "Invalid email or password. Please try again."


@pytest.mark.asyncio
async def test_login_unknown_email(client):
    """401 INVALID_CREDENTIALS — same for missing and wrong credential (no enumeration)."""
    resp = await client.post(LOGIN_URL, json={"email": "nobody@example.com", "password": VALID_PASSWORD})
    assert resp.status_code == 401
    assert resp.json()["error"]["code"] == "INVALID_CREDENTIALS"


@pytest.mark.asyncio
async def test_login_email_case_insensitive(client):
    """Login succeeds when email casing differs from registration."""
    await client.post(REGISTER_URL, json={"email": "mixed@Example.com", "password": VALID_PASSWORD})
    resp = await client.post(LOGIN_URL, json={"email": "MIXED@EXAMPLE.COM", "password": VALID_PASSWORD})
    assert resp.status_code == 200


# ── Logout (T033) ─────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_logout_with_cookie(client):
    """200 with logged_out: true."""
    await client.post(REGISTER_URL, json={"email": VALID_EMAIL, "password": VALID_PASSWORD})
    resp = await client.post(LOGOUT_URL)
    assert resp.status_code == 200
    assert resp.json() == {"success": True, "data": {"logged_out": True}, "error": None}


@pytest.mark.asyncio
async def test_logout_without_cookie(client):
    """200 always — logout is idempotent (no cookie present)."""
    resp = await client.post(LOGOUT_URL)
    assert resp.status_code == 200
    assert resp.json()["data"]["logged_out"] is True


@pytest.mark.asyncio
async def test_logout_with_invalid_cookie(client):
    """200 even with a tampered cookie — stateless logout."""
    resp = await client.post(LOGOUT_URL, cookies={"access_token": "invalid.token.value"})
    assert resp.status_code == 200


# ── /me (T033) ────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_me_with_valid_bearer(client):
    """200 returns id and email via Bearer header."""
    reg = await client.post(REGISTER_URL, json={"email": VALID_EMAIL, "password": VALID_PASSWORD})
    token = reg.json()["data"]["access_token"]
    resp = await client.get(ME_URL, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    body = resp.json()
    assert body["success"] is True
    assert "id" in body["data"]
    assert body["data"]["email"] == VALID_EMAIL


@pytest.mark.asyncio
async def test_me_with_expired_token(client):
    """401 SESSION_EXPIRED with exact catalog message."""
    await client.post(REGISTER_URL, json={"email": VALID_EMAIL, "password": VALID_PASSWORD})
    expired = _make_expired_token(str(uuid4()), VALID_EMAIL)
    resp = await client.get(ME_URL, headers={"Authorization": f"Bearer {expired}"})
    assert resp.status_code == 401
    body = resp.json()
    assert body["error"]["code"] == "SESSION_EXPIRED"
    assert body["error"]["message"] == "Your session has expired. Please log in again."


@pytest.mark.asyncio
async def test_me_with_tampered_token(client):
    """401 INVALID_TOKEN with exact catalog message."""
    resp = await client.get(ME_URL, headers={"Authorization": f"Bearer {_make_tampered_token()}"})
    assert resp.status_code == 401
    body = resp.json()
    assert body["error"]["code"] == "INVALID_TOKEN"
    assert body["error"]["message"] == "Your session has expired. Please log in again."


@pytest.mark.asyncio
async def test_me_with_malformed_signed_sub_returns_invalid_token(client):
    """401 INVALID_TOKEN when token is signed but sub claim is malformed."""
    resp = await client.get(
        ME_URL,
        headers={"Authorization": f"Bearer {_make_signed_token_with_malformed_sub()}"},
    )
    assert resp.status_code == 401
    body = resp.json()
    assert body["error"]["code"] == "INVALID_TOKEN"


@pytest.mark.asyncio
async def test_me_no_auth(client):
    """401 UNAUTHORIZED when no token present."""
    resp = await client.get(ME_URL)
    assert resp.status_code == 401
    assert resp.json()["error"]["code"] == "UNAUTHORIZED"
