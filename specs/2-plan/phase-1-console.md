# Phase 1 Console App - Technical Implementation Plan

## Overview

This document outlines the technical strategy for implementing the Phase 1 Console App based on the requirements defined in `feature-01-task-crud.md`. This phase focuses on building a Python-based command-line todo application with in-memory storage.

## Requirements Reference

- **Feature Specification**: `@specs/1-specify/features/feature-01-task-crud.md`
- **Constitution Reference**: `@constitution.md` (Sections 2 - Technology Stack, 6 - Database Design)

## Tech Stack

### Primary Language
- **Python 3.13+**: Core application language with modern features and performance optimizations

### CLI Framework
- **Typer**: Modern Python library for building beautiful command-line interfaces with minimal code
  - Alternative: Built-in `argparse` (if Typer proves problematic)

### Data Storage
- **In-Memory List**: Python native list for storing Task objects during runtime
- **JSON serialization**: For potential temporary persistence (optional)

### Additional Libraries
- **Datetime**: For timestamp management
- **Rich**: For interactive tables and styling (added for interactive TUI)
- **Standard Library**: Built-in modules for file operations, data validation, etc.

## Architecture

### Core Components

#### 1. Task Model
- **Module**: `src/core/models.py`
- **Class**: `Task`
- **Responsibilities**: Represent individual tasks with id, title, description, status, and timestamps
- **Attributes**:
  - `id: int` - Unique identifier
  - `title: str` - Task title (required, max 255 characters)
  - `description: str | None` - Task description (optional, max 1000 characters)
  - `status: str` - Task status ("pending", "completed")
  - `created_at: datetime` - Creation timestamp (displayed in human-readable format)

#### 2. Task Manager
- **Module**: `src/core/task_manager.py`
- **Class**: `TaskManager`
- **Responsibilities**: Business logic for task operations (CRUD operations) with validation
- **Methods**:
  - `add_task(title: str, description: str = None) -> Task` - Validates title length (≤255 chars) and non-empty
  - `get_all_tasks() -> List[Task]`
  - `get_tasks_by_status(status: str) -> List[Task]`
  - `update_task(task_id: int, title: str = None, description: str = None) -> Task` - Validates title length if provided
  - `mark_complete(task_id: int) -> Task`
  - `delete_task(task_id: int) -> bool`
  - `get_task(task_id: int) -> Task | None`
  - `validate_task_data(title: str, description: str = None) -> bool` - Validates title/description constraints

#### 3. CLI Module
- **Module**: `src/cli/main.py`
- **Responsibilities**: Command-line interface and user interaction
- **Commands**:
  - `todo add "title" --description "desc" | -d "desc"` - Add a new task
  - `todo list` - List all tasks
  - `todo list --status completed|pending | -s completed|pending` - Filter by status
  - `todo update id --title "new title" | -t "new title" --description "new desc" | -d "new desc"` - Update task
  - `todo complete id` - Mark task as complete
  - `todo delete id` - Delete task
  - `todo --help | -h` - Show help
- **Error Handling**: Proper exit codes (0=success, 1=general error, 2=usage error) and error messages to stderr

#### 4. Interactive TUI Module
- **Module**: `src/cli/interactive.py`
- **Responsibilities**: Interactive menu-driven interface with table visualizations
- **Logic**: `while True` loop that accepts single-key inputs (1-6) for navigation
- **Table Schema**: Use `rich.table.Table` to render task lists with columns: ID, Status, Title, Created At
- **Visual Design**: Color-coded status (Green for "completed", Yellow for "pending"), clear screen between actions

### Project Structure
```
src/
├── __init__.py
├── core/
│   ├── __init__.py
│   ├── models.py          # Task class definition
│   └── task_manager.py    # TaskManager class with business logic
├── cli/
│   ├── __init__.py
│   └── main.py           # CLI interface using Typer
└── tests/
    ├── __init__.py
    ├── test_models.py    # Unit tests for Task model
    ├── test_task_manager.py  # Unit tests for TaskManager
    └── test_cli.py       # Integration tests for CLI
```

## Implementation Strategy

### Phase 1a: Core Models
1. Implement the `Task` class with proper validation (title length ≤ 255, description length ≤ 1000)
2. Write unit tests for the Task model

### Phase 1b: Business Logic
1. Implement the `TaskManager` class with all required methods
2. Implement validation methods (`validate_task_data`)
3. Write comprehensive unit tests for all TaskManager methods

### Phase 1c: CLI Interface
1. Implement the CLI using Typer with support for both long and short form options
2. Connect CLI commands to TaskManager methods
3. Add proper error handling, exit codes, and user feedback
4. Implement human-readable timestamp display

### Phase 1d: Testing and Validation
1. Complete integration tests
2. Manual testing of all CLI commands
3. Validation of error handling and exit codes
4. Performance validation (response time < 100ms)

## Dependencies

### Runtime Dependencies
- Python 3.13+
- Typer library
- Rich library (for interactive TUI and tables)

### Development Dependencies
- pytest for testing
- black for code formatting
- mypy for type checking

## Quality Assurance

### Code Quality
- Type hints for all functions and methods
- Proper error handling with meaningful messages and appropriate exit codes
- Input validation with length constraints (title ≤ 255, description ≤ 1000)
- Human-readable timestamp display
- Consistent naming conventions (PEP 8)

### Testing
- Unit tests for all core logic (models, task manager)
- Integration tests for CLI functionality with both long and short form options
- Error handling and exit code validation tests
- Target: 70%+ code coverage for Phase I

### Performance
- All operations should complete in < 100ms
- Memory usage should be efficient for 10,000+ tasks

## Error Handling and Validation

- Input validation for all user inputs with length constraints (title ≤ 255 chars, description ≤ 1000 chars)
- Comprehensive error handling with user-friendly error messages
- Proper exit codes: 0 for success, 1 for general errors, 2 for usage errors
- Error messages sent to stderr as appropriate
- Invalid operations (invalid IDs, empty titles, etc.) handled gracefully with clear messages

## Security Considerations

- Input validation for all user inputs
- No external data sources or network calls (in-memory only)
- No authentication required for Phase I

## Success Criteria

- All CLI commands function as specified in the feature requirements
- Task operations complete within performance targets
- Code follows Python best practices and type hinting
- All tests pass with adequate coverage
- User can perform all CRUD operations successfully