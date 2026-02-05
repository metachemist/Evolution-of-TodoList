#!/usr/bin/env python3
"""
Interactive TUI for the todo application using Rich for tables and styling.
"""

import os
import sys
import inspect
# Get the directory containing this file and add src to the path
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from typing import Optional
import typer
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, IntPrompt
from core.task_manager import TaskManager
from core.models import Task

console = Console()
task_manager = TaskManager()


def clear_screen():
    """Clear the screen for better UX."""
    os.system('cls' if os.name == 'nt' else 'clear')


def display_menu():
    """Display the main menu options."""
    console.print("\n[bold blue]Todo List Manager - Interactive Mode[/bold blue]")
    console.print("[bold]Please select an option:[/bold]")
    console.print("1. Add Task")
    console.print("2. List Tasks")
    console.print("3. Update Task")
    console.print("4. Complete Task")
    console.print("5. Delete Task")
    console.print("6. Exit")
    console.print()


def display_tasks_table(tasks: list[Task], title: str = "Tasks"):
    """Display tasks in a rich table format."""
    if not tasks:
        console.print("[yellow]No tasks found.[/yellow]")
        return

    table = Table(title=title, show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", width=5)
    table.add_column("Status", min_width=10)
    table.add_column("Title", min_width=20)
    table.add_column("Created At", min_width=20)
    table.add_column("Description", min_width=20)

    for task in tasks:
        status_color = "green" if task.status == "completed" else "yellow"
        status_text = f"[{status_color}]{task.status}[/{status_color}]"
        table.add_row(
            str(task.id),
            status_text,
            task.title,
            task.created_at.strftime('%Y-%m-%d %H:%M'),
            task.description or ""
        )

    console.print(table)


def add_task_interactive():
    """Interactive task addition."""
    console.print("\n[bold]Adding a new task:[/bold]")
    title = Prompt.ask("Enter task title")

    description_input = Prompt.ask("Enter task description (optional, press Enter to skip)", default="")
    description = description_input if description_input.strip() else None

    try:
        task = task_manager.add_task(title, description)
        console.print(f"[green]Task '{task.title}' added successfully with ID {task.id}[/green]")
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")


def list_tasks_interactive():
    """Interactive task listing."""
    console.print("\n[bold]Listing tasks:[/bold]")

    choice = Prompt.ask("Filter by status? ([blue]a[/blue]ll/[blue]p[/blue]ending/[blue]c[/blue]ompleted, default=all)",
                       default="a", choices=["a", "p", "c"])

    if choice == "p":
        tasks = task_manager.get_tasks_by_status("pending")
        display_tasks_table(tasks, "Pending Tasks")
    elif choice == "c":
        tasks = task_manager.get_tasks_by_status("completed")
        display_tasks_table(tasks, "Completed Tasks")
    else:
        tasks = task_manager.get_all_tasks()
        display_tasks_table(tasks, "All Tasks")


def update_task_interactive():
    """Interactive task update."""
    console.print("\n[bold]Updating a task:[/bold]")

    if not task_manager.get_all_tasks():
        console.print("[yellow]No tasks available to update.[/yellow]")
        return

    display_tasks_table(task_manager.get_all_tasks(), "Available Tasks")

    try:
        task_id = IntPrompt.ask("Enter task ID to update")
        task = task_manager.get_task(task_id)

        if not task:
            console.print(f"[red]Task with ID {task_id} not found.[/red]")
            return

        console.print(f"Current task: {task.title}")

        new_title = Prompt.ask(f"Enter new title (current: '{task.title}', press Enter to keep current)", default=task.title)
        if new_title == task.title:
            new_title = None  # No change needed

        current_desc = task.description or ""
        new_description = Prompt.ask(f"Enter new description (current: '{current_desc}', press Enter to keep current)",
                                    default=current_desc)
        if new_description == current_desc:
            new_description = None  # No change needed

        # Only update if there's something to update
        if new_title is not None or new_description is not None:
            # If we're keeping the current title, pass the actual current title, not the unchanged value
            title_for_update = new_title if new_title != task.title else None
            desc_for_update = new_description if new_description != task.description else None

            updated_task = task_manager.update_task(task_id, title_for_update, desc_for_update)
            if updated_task:
                console.print(f"[green]Task '{updated_task.title}' updated successfully[/green]")
            else:
                console.print(f"[red]Failed to update task with ID {task_id}[/red]")
        else:
            console.print("[blue]No changes made to the task.[/blue]")

    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
    except Exception as e:
        console.print(f"[red]Invalid input: {e}[/red]")


def complete_task_interactive():
    """Interactive task completion."""
    console.print("\n[bold]Completing a task:[/bold]")

    pending_tasks = task_manager.get_tasks_by_status("pending")
    if not pending_tasks:
        console.print("[yellow]No pending tasks to complete.[/yellow]")
        return

    display_tasks_table(pending_tasks, "Pending Tasks")

    try:
        task_id = IntPrompt.ask("Enter task ID to mark as complete")
        task = task_manager.get_task(task_id)

        if not task:
            console.print(f"[red]Task with ID {task_id} not found.[/red]")
            return

        completed_task = task_manager.mark_complete(task_id)
        if completed_task:
            console.print(f"[green]Task '{completed_task.title}' marked as complete[/green]")
        else:
            console.print(f"[red]Failed to mark task with ID {task_id} as complete[/red]")

    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
    except Exception as e:
        console.print(f"[red]Invalid input: {e}[/red]")


def delete_task_interactive():
    """Interactive task deletion."""
    console.print("\n[bold]Deleting a task:[/bold]")

    all_tasks = task_manager.get_all_tasks()
    if not all_tasks:
        console.print("[yellow]No tasks available to delete.[/yellow]")
        return

    display_tasks_table(all_tasks, "Available Tasks")

    try:
        task_id = IntPrompt.ask("Enter task ID to delete")
        task = task_manager.get_task(task_id)

        if not task:
            console.print(f"[red]Task with ID {task_id} not found.[/red]")
            return

        confirm = Prompt.ask(f"Are you sure you want to delete '{task.title}'? ([red]y[/red]/[green]n[/green])",
                            choices=["y", "n"], default="n")

        if confirm.lower() == "y":
            success = task_manager.delete_task(task_id)
            if success:
                console.print(f"[green]Task '{task.title}' deleted successfully[/green]")
            else:
                console.print(f"[red]Failed to delete task with ID {task_id}[/red]")
        else:
            console.print("[blue]Task deletion cancelled.[/blue]")

    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
    except Exception as e:
        console.print(f"[red]Invalid input: {e}[/red]")


def interactive_main():
    """Main interactive loop."""
    clear_screen()
    console.print("[bold green]Welcome to the Interactive Todo List Manager![/bold green]")

    while True:
        display_menu()

        try:
            choice = Prompt.ask("Enter your choice (1-6)", choices=["1", "2", "3", "4", "5", "6"], default="6")

            if choice == "1":
                clear_screen()
                add_task_interactive()
            elif choice == "2":
                clear_screen()
                list_tasks_interactive()
            elif choice == "3":
                clear_screen()
                update_task_interactive()
            elif choice == "4":
                clear_screen()
                complete_task_interactive()
            elif choice == "5":
                clear_screen()
                delete_task_interactive()
            elif choice == "6":
                console.print("[bold blue]Goodbye![/bold blue]")
                break

            # Pause to let user see the result before clearing the screen again
            if choice != "6":
                input("\nPress Enter to continue...")
                clear_screen()

        except KeyboardInterrupt:
            console.print("\n[bold blue]Goodbye![/bold blue]")
            break
        except Exception as e:
            console.print(f"[red]An unexpected error occurred: {e}[/red]")
            input("Press Enter to continue...")
            clear_screen()


if __name__ == "__main__":
    interactive_main()