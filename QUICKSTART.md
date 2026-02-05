# Todo Evolution - Phase 1 Console App

## Overview

A sophisticated command-line todo application featuring both traditional CLI and interactive TUI modes. Built with Python, Typer, and Rich for a professional user experience.

## Installation

1. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage Modes

### Interactive TUI Mode (Recommended)
Launch the interactive menu-driven interface with rich table visualizations:

```bash
python -m src.main
```

Features:
- Professional menu-driven interface (press 1-6 for options)
- Rich table display with ID, Status, Title, and Created At columns
- Color-coded status indicators (Green for completed, Yellow for pending)
- Clear screen between actions for optimal UX

### Traditional CLI Mode
Command-line interface for script integration and power users:

#### Add a task
```bash
python -m src.main add "Buy groceries" --description "Milk, eggs, bread"
```

#### List all tasks
```bash
python -m src.main list-tasks
```

#### Filter tasks by status
```bash
python -m src.main list-tasks --status pending
python -m src.main list-tasks -s completed
```

#### Update a task
```bash
python -m src.main update 1 --title "Buy weekly groceries" -d "Milk, eggs, bread, fruits"
```

#### Mark a task as complete
```bash
python -m src.main complete 1
```

#### Delete a task
```bash
python -m src.main delete 1
```

## Key Features

### Interactive TUI
- ✅ Professional menu-driven interface with single-key navigation
- ✅ Rich table visualizations with color-coded status indicators
- ✅ Dynamic table rendering with ID, Status, Title, Created At columns
- ✅ Color scheme: Green for completed tasks, Yellow for pending tasks
- ✅ Clean screen transitions for enhanced user experience

### Traditional CLI
- ✅ Full command-line functionality with intuitive syntax
- ✅ Support for both long and short form options (e.g., --status/-s, --title/-t)
- ✅ Proper exit codes (0=success, 1=error, 2=usage error)
- ✅ Comprehensive error handling with user-friendly messages

### Data Validation
- ✅ Title validation: ≤ 255 characters, non-empty
- ✅ Description validation: ≤ 1000 characters
- ✅ Proper error messages for invalid inputs
- ✅ Human-readable timestamp formatting

### Testing & Quality
- ✅ 39 comprehensive tests with 100% pass rate
- ✅ Full test coverage for models, business logic, and CLI
- ✅ Type hints throughout the codebase
- ✅ PEP 8 compliant code standards

## Architecture

- **Core Logic**: `src/core/models.py` and `src/core/task_manager.py`
- **CLI Interface**: `src/cli/main.py` with Typer framework
- **Interactive UI**: `src/cli/interactive.py` with Rich library
- **Entry Point**: `src/main.py` with mode detection logic
- **Testing**: `src/tests/` with comprehensive unit and integration tests

## Technologies

- **Language**: Python 3.12+
- **CLI Framework**: Typer for intuitive command-line interfaces
- **UI Library**: Rich for professional tables and styling
- **Testing**: Pytest for comprehensive test coverage
- **Code Quality**: Black for formatting, MyPy for type checking

## Running Tests

```bash
python -m pytest src/tests/ -v
```

All 39 tests should pass successfully.