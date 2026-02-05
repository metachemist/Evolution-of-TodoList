"""
Task model representing a single item in the user's todo list.
"""

from datetime import datetime
from typing import Optional


class Task:
    def __init__(self, id: int, title: str, description: Optional[str] = None, status: str = "pending"):
        """
        Initialize a Task instance.

        Args:
            id: Unique identifier for the task
            title: Task title (required, max 255 characters)
            description: Task description (optional, max 1000 characters)
            status: Task status ("pending" or "completed", default: "pending")
        """
        self.id = id
        self.title = self._validate_title(title)
        self.description = self._validate_description(description)
        self.status = status
        self.created_at = datetime.now()

    def _validate_title(self, title: str) -> str:
        """Validate title length and non-empty requirement."""
        if not title or not title.strip():
            raise ValueError("Title cannot be empty")
        if len(title) > 255:
            raise ValueError(f"Title exceeds maximum length of 255 characters: {len(title)} provided")
        return title.strip()

    def _validate_description(self, description: Optional[str]) -> Optional[str]:
        """Validate description length if provided."""
        if description is None:
            return None
        if len(description) > 1000:
            raise ValueError(f"Description exceeds maximum length of 1000 characters: {len(description)} provided")
        return description

    def update_title(self, title: str) -> None:
        """Update task title with validation."""
        self.title = self._validate_title(title)

    def update_description(self, description: Optional[str]) -> None:
        """Update task description with validation."""
        self.description = self._validate_description(description)

    def mark_completed(self) -> None:
        """Mark task as completed."""
        self.status = "completed"

    def to_dict(self) -> dict:
        """Convert task to dictionary representation."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }

    def __str__(self) -> str:
        """String representation of the task."""
        return f"Task(id={self.id}, title='{self.title}', status='{self.status}')"

    def __repr__(self) -> str:
        """Developer-friendly representation of the task."""
        return f"Task(id={self.id}, title='{self.title}', description='{self.description}', status='{self.status}', created_at={self.created_at})"