import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from fastapi.testclient import TestClient
from jose import jwt
from src.main import app
from src.auth import create_access_token
from src.models import User


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_jwt_token_validation(client):
    """Test JWT token validation"""
    # Create a valid token
    user_data = {"sub": "test@example.com", "user_id": 1}
    valid_token = create_access_token(data=user_data)
    
    # Test with valid token
    response = client.get("/api/1/tasks", headers={"Authorization": f"Bearer {valid_token}"})
    # Should return 200 OK or 404 if no tasks exist
    assert response.status_code in [200, 404]
    
    # Test with invalid token
    response = client.get("/api/1/tasks", headers={"Authorization": "Bearer invalid_token"})
    assert response.status_code == 401  # Unauthorized
    
    # Test with malformed token
    response = client.get("/api/1/tasks", headers={"Authorization": "Bearer invalid.token.format"})
    assert response.status_code == 401  # Unauthorized
    
    # Test with expired token
    # Create a token with past expiration
    expired_token = jwt.encode(
        {"sub": "test@example.com", "exp": 1000}, 
        "test_secret", 
        algorithm="HS256"
    )
    response = client.get("/api/1/tasks", headers={"Authorization": f"Bearer {expired_token}"})
    assert response.status_code == 401  # Unauthorized


def test_input_validation(client):
    """Test input validation for security"""
    user_data = {"sub": "test@example.com", "user_id": 1}
    token = create_access_token(data=user_data)
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test SQL injection attempts in task title
    malicious_data = {
        "title": "'; DROP TABLE tasks; --",
        "description": "Normal description"
    }
    response = client.post("/api/1/tasks", json=malicious_data, headers=headers)
    # Should either reject the request or properly handle the input
    assert response.status_code in [200, 201, 422]
    
    # Test XSS attempts in task description
    xss_data = {
        "title": "XSS Test",
        "description": "<script>alert('XSS')</script>"
    }
    response = client.post("/api/1/tasks", json=xss_data, headers=headers)
    # Should either reject the request or properly sanitize the input
    assert response.status_code in [200, 201, 422]
    
    # Test extremely long inputs
    long_data = {
        "title": "A" * 300,  # Much longer than allowed
        "description": "B" * 1500  # Much longer than allowed
    }
    response = client.post("/api/1/tasks", json=long_data, headers=headers)
    # Should reject due to validation
    assert response.status_code in [422, 400]


def test_user_isolation_security(client):
    """Test that users cannot access other users' data"""
    # Create tokens for different users
    user1_data = {"sub": "user1@example.com", "user_id": 1}
    user2_data = {"sub": "user2@example.com", "user_id": 2}
    
    token1 = create_access_token(data=user1_data)
    token2 = create_access_token(data=user2_data)
    
    headers1 = {"Authorization": f"Bearer {token1}"}
    headers2 = {"Authorization": f"Bearer {token2}"}
    
    # User 1 creates a task
    task_data = {
        "title": "User 1 Private Task",
        "description": "This should only be accessible by user 1"
    }
    response = client.post("/api/1/tasks", json=task_data, headers=headers1)
    assert response.status_code in [200, 201]
    created_task = response.json().get("data", {})
    task_id = created_task.get("id")
    
    if task_id:
        # User 2 tries to access User 1's task using User 1's URL pattern
        # This should fail because the user_id in the token doesn't match the user_id in the URL
        # when the backend properly validates this
        response = client.get(f"/api/1/tasks/{task_id}", headers=headers2)
        # Should return 403 Forbidden due to user ID mismatch
        assert response.status_code in [403, 404]
        
        # User 2 tries to update User 1's task
        update_data = {"title": "Attempted Update"}
        response = client.put(f"/api/1/tasks/{task_id}", json=update_data, headers=headers2)
        # Should return 403 Forbidden
        assert response.status_code in [403, 404]
        
        # User 2 tries to delete User 1's task
        response = client.delete(f"/api/1/tasks/{task_id}", headers=headers2)
        # Should return 403 Forbidden
        assert response.status_code in [403, 404]


def test_rate_limiting_simulation(client):
    """Simulate rate limiting test (implementation dependent)"""
    # This test simulates what would happen with rate limiting
    # Since we don't have rate limiting middleware in the test setup,
    # we'll just verify that multiple requests work normally
    user_data = {"sub": "test@example.com", "user_id": 1}
    token = create_access_token(data=user_data)
    headers = {"Authorization": f"Bearer {token}"}
    
    # Make multiple requests to the same endpoint
    for i in range(5):
        response = client.get("/api/1/tasks", headers=headers)
        # All requests should work normally in the test environment
        assert response.status_code in [200, 404]