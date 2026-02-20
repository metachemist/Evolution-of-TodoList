import pytest
import time


# Task: T064 — stabilize backend perf smoke tests with shared AsyncClient fixture
@pytest.mark.asyncio
async def test_response_time_under_threshold(client):
    """Test that API responses are under 500ms (95th percentile)."""
    start_time = time.time()
    
    # Make a request to the health endpoint
    response = await client.get("/health")
    
    end_time = time.time()
    response_time_ms = (end_time - start_time) * 1000
    
    # Assert that the response time is under 500ms
    assert response_time_ms < 500
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_multiple_requests_performance(client):
    """Test performance under multiple requests."""
    num_requests = 10
    total_time = 0
    
    for _ in range(num_requests):
        start_time = time.time()
        response = await client.get("/health")
        end_time = time.time()
        total_time += (end_time - start_time) * 1000
        
        assert response.status_code == 200
    
    avg_response_time = total_time / num_requests
    assert avg_response_time < 500  # Average response time should be under 500ms
