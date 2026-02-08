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


def test_task_crud_operations(client):
    """Test all task CRUD operations"""
    # Create a token for testing
    user_data = {"sub": "test@example.com", "user_id": 1}
    token = create_access_token(data=user_data)
    headers = {"Authorization": f"Bearer {token}"}
    
    # CREATE: Test creating a new task
    task_data = {
        "title": "Test Task for CRUD",
        "description": "Testing CRUD operations"
    }
    response = client.post("/api/1/tasks", json=task_data, headers=headers)
    assert response.status_code in [200, 201]  # Created successfully
    created_task = response.json()["data"]
    assert created_task["title"] == "Test Task for CRUD"
    assert created_task["description"] == "Testing CRUD operations"
    assert created_task["completed"] is False
    task_id = created_task["id"]
    
    # READ: Test getting all tasks
    response = client.get(f"/api/1/tasks", headers=headers)
    assert response.status_code == 200
    tasks = response.json()["data"]["tasks"]
    assert len(tasks) >= 1
    assert any(task["id"] == task_id for task in tasks)
    
    # READ: Test getting a specific task
    response = client.get(f"/api/1/tasks/{task_id}", headers=headers)
    assert response.status_code == 200
    task = response.json()["data"]
    assert task["id"] == task_id
    assert task["title"] == "Test Task for CRUD"
    
    # UPDATE: Test updating a task
    updated_data = {
        "title": "Updated Test Task",
        "description": "Updated description for CRUD test",
        "completed": True
    }
    response = client.put(f"/api/1/tasks/{task_id}", json=updated_data, headers=headers)
    assert response.status_code == 200
    updated_task = response.json()["data"]
    assert updated_task["id"] == task_id
    assert updated_task["title"] == "Updated Test Task"
    assert updated_task["completed"] is True
    
    # READ: Verify the update worked
    response = client.get(f"/api/1/tasks/{task_id}", headers=headers)
    assert response.status_code == 200
    task = response.json()["data"]
    assert task["title"] == "Updated Test Task"
    assert task["completed"] is True
    
    # PATCH: Test toggling completion status
    response = client.patch(f"/api/1/tasks/{task_id}/complete", headers=headers)
    assert response.status_code == 200
    patched_task = response.json()["data"]
    assert patched_task["id"] == task_id
    assert patched_task["completed"] is False  # Should be toggled back to False
    
    # DELETE: Test deleting the task
    response = client.delete(f"/api/1/tasks/{task_id}", headers=headers)
    assert response.status_code in [200, 204]  # 204 No Content is also acceptable
    
    # READ: Verify the task was deleted
    response = client.get(f"/api/1/tasks/{task_id}", headers=headers)
    assert response.status_code == 404  # Task should not be found


def test_task_validation(client):
    """Test task validation"""
    user_data = {"sub": "test@example.com", "user_id": 1}
    token = create_access_token(data=user_data)
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test creating a task with missing title (should fail validation)
    invalid_task_data = {
        "title": "",  # Empty title should fail
        "description": "A task with an empty title"
    }
    response = client.post("/api/1/tasks", json=invalid_task_data, headers=headers)
    assert response.status_code in [422, 400]  # Validation error
    
    # Test creating a task with too long title (should fail validation)
    long_title = "A" * 201  # Exceeds 200 character limit
    invalid_task_data = {
        "title": long_title,
        "description": "A task with a very long title"
    }
    response = client.post("/api/1/tasks", json=invalid_task_data, headers=headers)
    assert response.status_code in [422, 400]  # Validation error
    
    # Test creating a task with too long description (should fail validation)
    long_desc = "A" * 1001  # Exceeds 1000 character limit
    invalid_task_data = {
        "title": "Valid title",
        "description": long_desc
    }
    response = client.post("/api/1/tasks", json=invalid_task_data, headers=headers)
    assert response.status_code in [422, 400]  # Validation error


def test_task_pagination(client):
    """Test task pagination functionality"""
    user_data = {"sub": "test@example.com", "user_id": 1}
    token = create_access_token(data=user_data)
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create multiple tasks for pagination testing
    for i in range(5):
        task_data = {
            "title": f"Paginated Task {i}",
            "description": f"Description for task {i}"
        }
        response = client.post("/api/1/tasks", json=task_data, headers=headers)
        assert response.status_code in [200, 201]
    
    # Test pagination with limit and offset
    response = client.get("/api/1/tasks?limit=3&offset=0", headers=headers)
    assert response.status_code == 200
    data = response.json()["data"]
    assert len(data["tasks"]) <= 3
    assert "pagination" in data
    assert data["pagination"]["limit"] == 3
    assert data["pagination"]["offset"] == 0
    
    # Test pagination with offset
    response = client.get("/api/1/tasks?limit=3&offset=3", headers=headers)
    assert response.status_code == 200
    data = response.json()["data"]
    # Should get remaining tasks (or empty if we only created 5 total)
    assert len(data["tasks"]) <= 3
    assert data["pagination"]["offset"] == 3