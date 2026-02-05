"""
TaskManager handles the business logic for task operations (CRUD operations) with validation.
"""

from typing import List, Optional
from .models import Task


class TaskManager:
    def __init__(self):
        """Initialize the TaskManager with an empty in-memory list."""
        self._tasks: List[Task] = []
        self._next_id = 1

    def add_task(self, title: str, description: Optional[str] = None) -> Task:
        """
        Add a new task with validation.

        Args:
            title: Task title (required, max 255 characters)
            description: Task description (optional, max 1000 characters)

        Returns:
            The created Task instance
        """
        self.validate_task_data(title, description)
        task = Task(id=self._next_id, title=title, description=description)
        self._tasks.append(task)
        self._next_id += 1
        return task

    def get_all_tasks(self) -> List[Task]:
        """
        Get all tasks.

        Returns:
            List of all tasks
        """
        return self._tasks.copy()

    def get_tasks_by_status(self, status: str) -> List[Task]:
        """
        Get tasks filtered by status.

        Args:
            status: Status to filter by ("pending" or "completed")

        Returns:
            List of tasks with the specified status
        """
        return [task for task in self._tasks if task.status == status]

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Optional[Task]:
        """
        Update an existing task with validation.

        Args:
            task_id: ID of the task to update
            title: New title (optional)
            description: New description (optional)

        Returns:
            Updated Task instance or None if task not found
        """
        task = self.get_task(task_id)
        if task is None:
            return None

        if title is not None:
            self.validate_task_data(title, description)
            task.update_title(title)

        if description is not None:
            # If title isn't changing, we validate against the existing title
            temp_title = task.title if title is None else title
            self.validate_task_data(temp_title, description)
            task.update_description(description)

        return task

    def mark_complete(self, task_id: int) -> Optional[Task]:
        """
        Mark a task as complete.

        Args:
            task_id: ID of the task to mark complete

        Returns:
            Updated Task instance or None if task not found
        """
        task = self.get_task(task_id)
        if task:
            task.mark_completed()
            return task
        return None

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task.

        Args:
            task_id: ID of the task to delete

        Returns:
            True if task was deleted, False if not found
        """
        task = self.get_task(task_id)
        if task:
            self._tasks.remove(task)
            return True
        return False

    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Get a task by ID.

        Args:
            task_id: ID of the task to retrieve

        Returns:
            Task instance or None if not found
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def validate_task_data(self, title: str, description: Optional[str] = None) -> bool:
        """
        Validate task data according to constraints.

        Args:
            title: Task title to validate
            description: Task description to validate (optional)

        Returns:
            True if data is valid, raises exception if not
        """
        if not title or not title.strip():
            raise ValueError("Title cannot be empty")

        if len(title) > 255:
            raise ValueError(f"Title exceeds maximum length of 255 characters: {len(title)} provided")

        if description and len(description) > 1000:
            raise ValueError(f"Description exceeds maximum length of 1000 characters: {len(description)} provided")

        return True