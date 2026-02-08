import pytest
import sys
import os
# Add the src directory to the path so we can import from src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from datetime import datetime
from unittest.mock import patch
from src.main import app
from src.models import User, Task
from src.auth import create_access_token
from src.auth.auth_handler import get_current_user


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(bind=engine)
    with Session(engine) as session:
        yield session




@pytest.fixture(name="sample_user")
def sample_user_fixture(session: Session):
    user = User(
        email="test@example.com",
        first_name="Test",
        last_name="User",
        hashed_password="hashed_test_password",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


from sqlmodel import SQLModel
from sqlalchemy.engine import create_engine
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from src.db import get_session


@pytest.fixture(name="client")
def client_fixture(session):
    def get_session_override():
        yield session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="valid_token")
def valid_token_fixture(sample_user: User):
    # Create a valid JWT token for the sample user
    data = {"sub": str(sample_user.id)}
    token = create_access_token(data=data)
    return token


def test_create_task(client: TestClient, sample_user: User, valid_token: str):
    """Test creating a new task for a user."""
    headers = {"Authorization": f"Bearer {valid_token}"}
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "completed": False
    }
    
    response = client.post(f"/api/{sample_user.id}/tasks", json=task_data, headers=headers)
    assert response.status_code == 200
    
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "This is a test task"
    assert data["completed"] is False
    assert data["user_id"] == sample_user.id


def test_get_user_tasks(client: TestClient, sample_user: User, valid_token: str, session: Session):
    """Test retrieving all tasks for a user."""
    # Create a task first
    test_task = Task(
        title="Test Task",
        description="This is a test task",
        completed=False,
        user_id=sample_user.id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    session.add(test_task)
    session.commit()
    session.refresh(test_task)

    headers = {"Authorization": f"Bearer {valid_token}"}
    response = client.get(f"/api/{sample_user.id}/tasks", headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert len(data) >= 1
    assert any(task["id"] == test_task.id for task in data)


def test_get_single_task(client: TestClient, sample_user: User, valid_token: str, session: Session):
    """Test retrieving a single task for a user."""
    # Create a task first
    task = Task(
        title="Test Task",
        description="This is a test task",
        completed=False,
        user_id=sample_user.id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    
    headers = {"Authorization": f"Bearer {valid_token}"}
    response = client.get(f"/api/{sample_user.id}/tasks/{task.id}", headers=headers)
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == task.id
    assert data["title"] == "Test Task"


def test_update_task(client: TestClient, sample_user: User, valid_token: str, session: Session):
    """Test updating a task for a user."""
    # Create a task first
    task = Task(
        title="Original Task",
        description="Original description",
        completed=False,
        user_id=sample_user.id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    
    headers = {"Authorization": f"Bearer {valid_token}"}
    update_data = {
        "title": "Updated Task",
        "description": "Updated description",
        "completed": True
    }
    
    response = client.put(f"/api/{sample_user.id}/tasks/{task.id}", json=update_data, headers=headers)
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == task.id
    assert data["title"] == "Updated Task"
    assert data["description"] == "Updated description"
    assert data["completed"] is True


def test_delete_task(client: TestClient, sample_user: User, valid_token: str, session: Session):
    """Test deleting a task for a user."""
    # Create a task first
    task = Task(
        title="Test Task to Delete",
        description="This task will be deleted",
        completed=False,
        user_id=sample_user.id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    
    headers = {"Authorization": f"Bearer {valid_token}"}
    response = client.delete(f"/api/{sample_user.id}/tasks/{task.id}", headers=headers)
    assert response.status_code == 200
    
    # Verify the task was deleted
    response = client.get(f"/api/{sample_user.id}/tasks/{task.id}", headers=headers)
    assert response.status_code == 404


def test_toggle_task_completion(client: TestClient, sample_user: User, valid_token: str, session: Session):
    """Test toggling the completion status of a task."""
    # Create a task first
    task = Task(
        title="Test Task",
        description="This is a test task",
        completed=False,
        user_id=sample_user.id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    
    headers = {"Authorization": f"Bearer {valid_token}"}
    response = client.patch(f"/api/{sample_user.id}/tasks/{task.id}/complete", headers=headers)
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == task.id
    assert data["completed"] is True  # Should be toggled from False to True


def test_unauthorized_access_to_other_users_tasks(client: TestClient, sample_user: User, valid_token: str, session: Session):
    """Test that a user cannot access another user's tasks."""
    # Create another user
    other_user = User(
        email="other@example.com",
        first_name="Other",
        last_name="User",
        hashed_password="hashed_other_password",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    session.add(other_user)
    session.commit()
    session.refresh(other_user)
    
    # Create a task for the other user
    task = Task(
        title="Other User's Task",
        description="This belongs to another user",
        completed=False,
        user_id=other_user.id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    
    headers = {"Authorization": f"Bearer {valid_token}"}
    # Try to access other user's task
    response = client.get(f"/api/{other_user.id}/tasks/{task.id}", headers=headers)
    assert response.status_code == 403  # Forbidden