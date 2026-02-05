#!/usr/bin/env python3
"""
Command-line interface for the todo application using Typer.
"""

import sys
import os
import inspect
# Get the directory containing this file and add src to the path
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from typing import Optional
import typer
from core.task_manager import TaskManager
from core.models import Task

app = typer.Typer()
task_manager = TaskManager()


def display_tasks(tasks: list[Task]):
    """Display tasks in a table-like format."""
    if not tasks:
        typer.echo("No tasks found.")
        return

    # Print header
    typer.echo(f"{'ID':<4} {'Title':<30} {'Status':<10} {'Created At':<20} {'Description'}")
    typer.echo("-" * 80)

    # Print each task
    for task in tasks:
        title = task.title[:27] + "..." if len(task.title) > 30 else task.title
        description = task.description[:30] + "..." if task.description and len(task.description) > 30 else (task.description or "")
        typer.echo(f"{task.id:<4} {title:<30} {task.status:<10} {task.created_at.strftime('%Y-%m-%d %H:%M'):<20} {description}")


@app.command()
def add(
    title: str = typer.Argument(..., help="Task title"),
    description: Optional[str] = typer.Option(None, "-d", "--description", help="Task description")
):
    """
    Add a new task to the todo list.
    """
    try:
        task = task_manager.add_task(title, description)
        typer.echo(f"Task '{task.title}' added successfully with ID {task.id}")
    except ValueError as e:
        typer.echo(f"Error: {e}", err=True)
        sys.exit(1)


@app.command()
def list_tasks(
    status: Optional[str] = typer.Option(None, "-s", "--status", help="Filter tasks by status (pending or completed)")
):
    """
    List all tasks or filter by status.
    """
    try:
        if status:
            if status not in ["pending", "completed"]:
                typer.echo("Error: Status must be 'pending' or 'completed'", err=True)
                sys.exit(2)
            tasks = task_manager.get_tasks_by_status(status)
            typer.echo(f"Showing {status} tasks:")
        else:
            tasks = task_manager.get_all_tasks()
            typer.echo("All tasks:")

        display_tasks(tasks)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        sys.exit(1)


@app.command()
def update(
    task_id: int = typer.Argument(..., help="ID of the task to update"),
    title: Optional[str] = typer.Option(None, "-t", "--title", help="New title for the task"),
    description: Optional[str] = typer.Option(None, "-d", "--description", help="New description for the task")
):
    """
    Update an existing task.
    """
    try:
        task = task_manager.get_task(task_id)
        if not task:
            typer.echo(f"Error: Task with ID {task_id} not found", err=True)
            sys.exit(1)

        updated_task = task_manager.update_task(task_id, title, description)
        if updated_task:
            typer.echo(f"Task '{updated_task.title}' updated successfully")
        else:
            typer.echo(f"Failed to update task with ID {task_id}", err=True)
            sys.exit(1)
    except ValueError as e:
        typer.echo(f"Error: {e}", err=True)
        sys.exit(1)


@app.command()
def complete(
    task_id: int = typer.Argument(..., help="ID of the task to mark as complete")
):
    """
    Mark a task as complete.
    """
    try:
        task = task_manager.get_task(task_id)
        if not task:
            typer.echo(f"Error: Task with ID {task_id} not found", err=True)
            sys.exit(1)

        completed_task = task_manager.mark_complete(task_id)
        if completed_task:
            typer.echo(f"Task '{completed_task.title}' marked as complete")
        else:
            typer.echo(f"Failed to mark task with ID {task_id} as complete", err=True)
            sys.exit(1)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        sys.exit(1)


@app.command()
def delete(
    task_id: int = typer.Argument(..., help="ID of the task to delete")
):
    """
    Delete a task.
    """
    try:
        task = task_manager.get_task(task_id)
        if not task:
            typer.echo(f"Error: Task with ID {task_id} not found", err=True)
            sys.exit(1)

        success = task_manager.delete_task(task_id)
        if success:
            typer.echo(f"Task '{task.title}' deleted successfully")
        else:
            typer.echo(f"Failed to delete task with ID {task_id}", err=True)
            sys.exit(1)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    app()