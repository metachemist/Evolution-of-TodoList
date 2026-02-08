import pytest
from sqlmodel import Session, select
from datetime import datetime
from unittest.mock import MagicMock
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.models import User, Task, UserCreate, TaskCreate, TaskUpdate
from src.auth import create_access_token, verify_password, get_password_hash


def test_user_model_creation():
    """Test creating a user model instance"""
    user_data = {
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User",
        "hashed_password": "hashed_password"
    }
    
    user = User(**user_data)
    
    assert user.email == "test@example.com"
    assert user.first_name == "Test"
    assert user.last_name == "User"
    assert user.hashed_password == "hashed_password"
    assert user.id is None  # ID will be assigned by DB


def test_task_model_creation():
    """Test creating a task model instance"""
    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "completed": False,
        "user_id": 1
    }
    
    task = Task(**task_data)
    
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.completed is False
    assert task.user_id == 1
    assert task.id is None  # ID will be assigned by DB
    assert isinstance(task.created_at, datetime)
    assert isinstance(task.updated_at, datetime)


def test_user_create_model_validation():
    """Test UserCreate model validation"""
    user_create = UserCreate(
        email="test@example.com",
        password="SecurePassword123!",
        first_name="Test",
        last_name="User"
    )
    
    assert user_create.email == "test@example.com"
    assert user_create.password == "SecurePassword123!"
    assert user_create.first_name == "Test"
    assert user_create.last_name == "User"


def test_task_create_model_validation():
    """Test TaskCreate model validation"""
    task_create = TaskCreate(
        title="Test Task",
        description="Test Description"
    )
    
    assert task_create.title == "Test Task"
    assert task_create.description == "Test Description"


def test_task_update_model_validation():
    """Test TaskUpdate model validation"""
    task_update = TaskUpdate(
        title="Updated Task",
        description="Updated Description",
        completed=True
    )
    
    assert task_update.title == "Updated Task"
    assert task_update.description == "Updated Description"
    assert task_update.completed is True


def test_password_hashing():
    """Test password hashing and verification"""
    plain_password = "SecurePassword123!"
    hashed = get_password_hash(plain_password)
    
    assert verify_password(plain_password, hashed)
    assert not verify_password("wrong_password", hashed)


def test_jwt_token_creation():
    """Test JWT token creation and decoding"""
    user_data = {"sub": "test@example.com", "user_id": 1}
    token = create_access_token(data=user_data)
    
    assert isinstance(token, str)
    assert len(token) > 0