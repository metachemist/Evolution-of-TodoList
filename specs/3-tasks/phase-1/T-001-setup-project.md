# T-001: Setup Project Structure for Console Todo App

## Task Description
Create the foundational project structure for the Phase 1 Console Todo application as specified in the implementation plan. This includes setting up the directory structure, initializing the Python project, and configuring dependencies.

## Implementation Plan Reference
Based on: `@specs/2-plan/phase-1-console.md` - Project Structure section

## Requirements
- Create the src/ directory with proper subdirectories (core/, cli/, tests/)
- Initialize Python project with required dependencies (typer, pytest, black, mypy)
- Set up proper __init__.py files throughout the structure
- Configure requirements.txt with all necessary packages

## Files to Create/Modify
- requirements.txt
- src/__init__.py
- src/core/__init__.py
- src/cli/__init__.py
- src/tests/__init__.py

## Dependencies
None - this is a foundational task

## Acceptance Criteria
- [ ] Project directory structure matches the implementation plan
- [ ] requirements.txt includes typer, pytest, black, mypy
- [ ] All __init__.py files exist in proper locations
- [ ] Project can be initialized with pip install -r requirements.txt