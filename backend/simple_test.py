#!/usr/bin/env python3
"""Simple test to check if models can be imported"""

try:
    from src.models import User, Task, UserCreate, TaskCreate
    print("SUCCESS: Models imported successfully!")
    
    # Try creating a simple user
    user = User(email="test@example.com", hashed_password="test")
    print(f"SUCCESS: Created user with email {user.email}")
    
    # Try creating a simple task
    task = Task(title="Test task", user_id=1)
    print(f"SUCCESS: Created task with title '{task.title}'")
    
    print("All basic functionality works!")
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()