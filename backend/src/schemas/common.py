# Task: T031 — Common API response schemas
from pydantic import BaseModel
from typing import Any, Optional


class ErrorResponse(BaseModel):
    """Schema for structured error responses."""
    success: bool = False
    data: Optional[Any] = None
    error: dict


class TokenResponse(BaseModel):
    """Schema for authentication token responses."""
    access_token: str
    token_type: str = "bearer"
