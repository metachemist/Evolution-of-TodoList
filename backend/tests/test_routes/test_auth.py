import pytest

from src.models.user import User
from src.utils.auth import get_password_hash
from tests.conftest import make_auth_header, make_auth_cookie


@pytest.mark.asyncio
async def test_register_creates_user(client):
    """POST /api/auth/register returns 201 with access_token."""
    resp = await client.post(
        "/api/auth/register",
        json={"email": "new@user.com", "password": "securepass"},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_register_duplicate_email(client, db_session):
    """POST /api/auth/register returns 409 when email already exists."""
    user = User(email="dup@user.com", hashed_password=get_password_hash("pw"))
    db_session.add(user)
    await db_session.commit()

    resp = await client.post(
        "/api/auth/register",
        json={"email": "dup@user.com", "password": "anotherpass"},
    )
    assert resp.status_code == 409


@pytest.mark.asyncio
async def test_login_valid_credentials(client, db_session):
    """POST /api/auth/login returns 200 with access_token for valid credentials."""
    user = User(email="login@user.com", hashed_password=get_password_hash("correctpw"))
    db_session.add(user)
    await db_session.commit()

    resp = await client.post(
        "/api/auth/login",
        json={"email": "login@user.com", "password": "correctpw"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_credentials(client, db_session):
    """POST /api/auth/login returns 401 for invalid credentials."""
    user = User(email="bad@user.com", hashed_password=get_password_hash("realpass"))
    db_session.add(user)
    await db_session.commit()

    resp = await client.post(
        "/api/auth/login",
        json={"email": "bad@user.com", "password": "wrongpass"},
    )
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_login_nonexistent_user(client):
    """POST /api/auth/login returns 401 for non-existent email."""
    resp = await client.post(
        "/api/auth/login",
        json={"email": "nobody@user.com", "password": "whatever"},
    )
    assert resp.status_code == 401


# --- Cookie auth tests ---


@pytest.mark.asyncio
async def test_register_sets_cookie(client):
    """POST /api/auth/register sets an httpOnly access_token cookie."""
    resp = await client.post(
        "/api/auth/register",
        json={"email": "cookie-reg@user.com", "password": "securepass"},
    )
    assert resp.status_code == 201
    set_cookie = resp.headers.get("set-cookie")
    assert set_cookie is not None
    assert "access_token=" in set_cookie
    assert "httponly" in set_cookie.lower()


@pytest.mark.asyncio
async def test_login_sets_cookie(client, db_session):
    """POST /api/auth/login sets an httpOnly access_token cookie."""
    user = User(email="cookie-login@user.com", hashed_password=get_password_hash("pw"))
    db_session.add(user)
    await db_session.commit()

    resp = await client.post(
        "/api/auth/login",
        json={"email": "cookie-login@user.com", "password": "pw"},
    )
    assert resp.status_code == 200
    set_cookie = resp.headers.get("set-cookie")
    assert set_cookie is not None
    assert "access_token=" in set_cookie
    assert "httponly" in set_cookie.lower()


@pytest.mark.asyncio
async def test_me_with_bearer_token(client, db_session):
    """GET /api/auth/me returns user info when using Bearer token auth."""
    user = User(email="me-bearer@user.com", hashed_password=get_password_hash("pw"))
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    headers = make_auth_header(str(user.id))
    resp = await client.get("/api/auth/me", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == str(user.id)
    assert data["email"] == "me-bearer@user.com"


@pytest.mark.asyncio
async def test_me_with_cookie(client, db_session):
    """GET /api/auth/me returns user info when using cookie auth."""
    user = User(email="me-cookie@user.com", hashed_password=get_password_hash("pw"))
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    cookies = make_auth_cookie(str(user.id))
    resp = await client.get("/api/auth/me", cookies=cookies)
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == str(user.id)
    assert data["email"] == "me-cookie@user.com"


@pytest.mark.asyncio
async def test_me_unauthenticated(client):
    """GET /api/auth/me returns 401 when no auth is provided."""
    resp = await client.get("/api/auth/me")
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_logout_clears_cookie(client):
    """POST /api/auth/logout clears the access_token cookie."""
    resp = await client.post("/api/auth/logout")
    assert resp.status_code == 200
    data = resp.json()
    assert data["message"] == "Logged out successfully"
    set_cookie = resp.headers.get("set-cookie")
    assert set_cookie is not None
    assert "access_token=" in set_cookie
    # Cookie should be cleared (max-age=0 or expires in the past)
    assert 'max-age=0' in set_cookie.lower() or '01 jan 1970' in set_cookie.lower()
