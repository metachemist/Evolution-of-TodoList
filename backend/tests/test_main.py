# Task: T064 — stabilize backend test execution with shared AsyncClient fixture
import pytest


@pytest.mark.asyncio
async def test_root_endpoint(client):
    """Test the root endpoint."""
    response = await client.get("/")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["error"] is None
    assert "message" in body["data"]


@pytest.mark.asyncio
async def test_health_endpoint(client):
    """Test the health check endpoint."""
    response = await client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["error"] is None
    assert body["data"]["status"] == "healthy"


@pytest.mark.asyncio
async def test_nonexistent_route_returns_envelope(client):
    """Unknown paths return envelope-wrapped 404 errors."""
    response = await client.get("/nonexistent")
    assert response.status_code == 404
    body = response.json()
    assert body["success"] is False
    assert body["data"] is None
    assert body["error"]["code"] == "NOT_FOUND"


@pytest.mark.asyncio
async def test_wrong_method_returns_envelope(client):
    """Method mismatch returns envelope-wrapped 405 errors."""
    response = await client.post("/api/auth/me")
    assert response.status_code == 405
    body = response.json()
    assert body["success"] is False
    assert body["data"] is None
    assert body["error"]["code"] == "HTTP_ERROR"
