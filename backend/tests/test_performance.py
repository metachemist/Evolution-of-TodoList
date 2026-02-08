import time
import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from fastapi.testclient import TestClient
from src.main import app
from src.auth import create_access_token


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_api_response_times(client):
    """Test API response times to ensure they meet performance requirements"""
    # Create a token for testing
    user_data = {"sub": "test@example.com", "user_id": 1}
    token = create_access_token(data=user_data)
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test GET /api/{user_id}/tasks response time
    start_time = time.time()
    response = client.get("/api/1/tasks", headers=headers)
    end_time = time.time()
    response_time = (end_time - start_time) * 1000  # Convert to milliseconds
    
    # API should respond within 2 seconds (2000ms) for 95% of requests
    assert response_time < 2000, f"GET /api/1/tasks took {response_time}ms, which is too slow"
    
    # Test POST /api/{user_id}/tasks response time
    task_data = {
        "title": "Performance Test Task",
        "description": "Task for performance testing"
    }
    start_time = time.time()
    response = client.post("/api/1/tasks", json=task_data, headers=headers)
    end_time = time.time()
    response_time = (end_time - start_time) * 1000
    
    assert response_time < 2000, f"POST /api/1/tasks took {response_time}ms, which is too slow"
    
    # If task was created successfully, test GET /api/{user_id}/tasks/{id} response time
    if response.status_code in [200, 201]:
        task_id = response.json().get("data", {}).get("id")
        if task_id:
            start_time = time.time()
            response = client.get(f"/api/1/tasks/{task_id}", headers=headers)
            end_time = time.time()
            response_time = (end_time - start_time) * 1000
            
            assert response_time < 2000, f"GET /api/1/tasks/{task_id} took {response_time}ms, which is too slow"


def test_concurrent_requests_performance(client):
    """Test performance under concurrent requests"""
    import threading
    import queue
    
    # Create a token for testing
    user_data = {"sub": "test@example.com", "user_id": 1}
    token = create_access_token(data=user_data)
    headers = {"Authorization": f"Bearer {token}"}
    
    # Queue to store response times
    response_times = queue.Queue()
    
    def make_request():
        start_time = time.time()
        response = client.get("/api/1/tasks", headers=headers)
        end_time = time.time()
        response_time = (end_time - start_time) * 1000
        response_times.put(response_time)
    
    # Create multiple threads to simulate concurrent requests
    threads = []
    num_requests = 10
    
    for _ in range(num_requests):
        thread = threading.Thread(target=make_request)
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    # Check that all requests completed within acceptable time
    total_time = 0
    while not response_times.empty():
        response_time = response_times.get()
        assert response_time < 2000, f"A request took {response_time}ms, which is too slow"
        total_time += response_time
    
    avg_response_time = total_time / num_requests
    print(f"Average response time for {num_requests} concurrent requests: {avg_response_time:.2f}ms")


def test_large_payload_handling(client):
    """Test handling of larger payloads"""
    # Create a token for testing
    user_data = {"sub": "test@example.com", "user_id": 1}
    token = create_access_token(data=user_data)
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create a task with a large description
    large_description = "A" * 900  # Close to the 1000 char limit
    task_data = {
        "title": "Large Payload Test Task",
        "description": large_description
    }
    
    start_time = time.time()
    response = client.post("/api/1/tasks", json=task_data, headers=headers)
    end_time = time.time()
    response_time = (end_time - start_time) * 1000
    
    # Should handle large payloads efficiently
    assert response_time < 2000, f"POST with large payload took {response_time}ms, which is too slow"
    assert response.status_code in [200, 201, 422]  # Either succeeds or fails validation appropriately


def test_multiple_task_operations_performance(client):
    """Test performance when performing multiple task operations"""
    # Create a token for testing
    user_data = {"sub": "test@example.com", "user_id": 1}
    token = create_access_token(data=user_data)
    headers = {"Authorization": f"Bearer {token}"}
    
    # Measure time to create multiple tasks
    start_time = time.time()
    
    task_ids = []
    for i in range(5):
        task_data = {
            "title": f"Performance Test Task {i}",
            "description": f"Task {i} for performance testing"
        }
        response = client.post("/api/1/tasks", json=task_data, headers=headers)
        if response.status_code in [200, 201]:
            task_id = response.json().get("data", {}).get("id")
            if task_id:
                task_ids.append(task_id)
    
    create_time = (time.time() - start_time) * 1000
    
    # Creating multiple tasks should be reasonably fast
    assert create_time < 5000, f"Creating 5 tasks took {create_time}ms, which is too slow"
    
    # Measure time to retrieve all tasks
    start_time = time.time()
    response = client.get("/api/1/tasks", headers=headers)
    read_time = (time.time() - start_time) * 1000
    
    assert read_time < 2000, f"Reading tasks took {read_time}ms, which is too slow"
    
    # Clean up: measure time to delete created tasks
    start_time = time.time()
    for task_id in task_ids:
        client.delete(f"/api/1/tasks/{task_id}", headers=headers)
    
    delete_time = (time.time() - start_time) * 1000
    assert delete_time < 3000, f"Deleting {len(task_ids)} tasks took {delete_time}ms, which is too slow"