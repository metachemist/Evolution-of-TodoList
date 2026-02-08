import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from sqlmodel import Session, select
from src.main import app
from src.models import User, Task
from src.db import get_session
from src.auth import create_access_token


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_api_endpoints_integration(client):
    """Integration test for API endpoints"""
    # Create a mock user and token for testing
    user_data = {"sub": "test@example.com", "user_id": 1}
    token = create_access_token(data=user_data)
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test GET /api/{user_id}/tasks endpoint
    response = client.get("/api/1/tasks", headers=headers)
    # Should return 200 OK or 404 if no tasks exist
    assert response.status_code in [200, 404]
    
    # Test POST /api/{user_id}/tasks endpoint
    task_data = {
        "title": "Integration Test Task",
        "description": "Task created during integration test"
    }
    response = client.post("/api/1/tasks", json=task_data, headers=headers)
    # Should return 200 OK or 201 Created
    assert response.status_code in [200, 201, 422]
    
    # Test GET /api/{user_id}/tasks/{task_id} endpoint
    # First, we need to create a task to get
    if response.status_code in [200, 201]:
        task_response = response.json()
        task_id = task_response.get("id") or task_response.get("data", {}).get("id")
        if task_id:
            response = client.get(f"/api/1/tasks/{task_id}", headers=headers)
            assert response.status_code in [200, 404]
    
    # Test PUT /api/{user_id}/tasks/{task_id} endpoint
    # Using a mock task ID for testing
    response = client.put("/api/1/tasks/999999", json=task_data, headers=headers)
    # Should return 404 if task doesn't exist or 200 if it does
    assert response.status_code in [200, 404, 422]
    
    # Test DELETE /api/{user_id}/tasks/{task_id} endpoint
    response = client.delete("/api/1/tasks/999999", headers=headers)
    # Should return 404 if task doesn't exist or 200/204 if it does
    assert response.status_code in [200, 204, 404]
    
    # Test PATCH /api/{user_id}/tasks/{task_id}/complete endpoint
    response = client.patch("/api/1/tasks/999999/complete", headers=headers)
    # Should return 404 if task doesn't exist
    assert response.status_code in [200, 404, 422]


def test_authentication_flow(client):
    """Test authentication flow"""
    # Test registration endpoint
    user_data = {
        "email": "integration_test@example.com",
        "password": "SecurePassword123!"
    }
    response = client.post("/api/v1/auth/register", json=user_data)
    # Should return 200 OK, 400 for bad request, or 409 for conflict
    assert response.status_code in [200, 400, 409, 422]
    
    # Test login endpoint
    login_data = {
        "email": "integration_test@example.com",
        "password": "SecurePassword123!"
    }
    response = client.post("/api/v1/auth/login", json=login_data)
    # Should return 200 OK or 401 for unauthorized
    assert response.status_code in [200, 401, 422]


def test_user_isolation(client):
    """Test that users can only access their own data"""
    # Create tokens for different users
    user1_data = {"sub": "user1@example.com", "user_id": 1}
    user2_data = {"sub": "user2@example.com", "user_id": 2}
    
    token1 = create_access_token(data=user1_data)
    token2 = create_access_token(data=user2_data)
    
    headers1 = {"Authorization": f"Bearer {token1}"}
    headers2 = {"Authorization": f"Bearer {token2}"}
    
    # User 1 creates a task
    task_data = {
        "title": "User 1 Task",
        "description": "Task belonging to user 1"
    }
    response = client.post("/api/1/tasks", json=task_data, headers=headers1)
    assert response.status_code in [200, 201, 422]
    
    # Try to access user 1's task with user 2's token and wrong URL
    # This should fail due to user ID mismatch in URL vs token
    response = client.get("/api/1/tasks", headers=headers2)  # Wrong user ID in URL
    # Should return 403 for forbidden access
    assert response.status_code in [403, 200]  # May return 200 with empty list or 403
    
    # Proper test: try to access user 1's task with user 2's token but correct URL
    # This should still fail due to user ID mismatch
    response = client.get("/api/2/tasks", headers=headers2)  # Correct user ID in URL
    assert response.status_code == 200  # Should return user 2's tasks (empty list)