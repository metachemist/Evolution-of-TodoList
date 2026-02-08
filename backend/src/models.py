from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr

# 1. REMOVED 'sa_type=str' from everywhere. SQLModel infers this automatically.

class UserBase(SQLModel):
    # Field(...) is enough. No need for sa_type=str
    email: EmailStr = Field(unique=True, index=True) 
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class UserCreate(UserBase):
    password: str

class UserUpdate(SQLModel):
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)

class UserPublic(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    completed: bool = Field(default=False)

class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class TaskCreate(TaskBase):
    pass

class TaskUpdate(SQLModel):
    # Removed sa_type=str and sa_type=bool
    title: Optional[str] = Field(default=None, min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    completed: Optional[bool] = Field(default=None)

class TaskPublic(TaskBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime