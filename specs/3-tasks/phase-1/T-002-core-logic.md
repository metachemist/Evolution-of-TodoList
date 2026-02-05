# T-002: Implement Core Logic (Task Model and TaskManager)

## Task Description
Implement the core data model (Task) and business logic (TaskManager) components as specified in the implementation plan. This includes proper validation, error handling, and adherence to the defined entity specifications.

## Implementation Plan Reference
Based on: `@specs/2-plan/phase-1-console.md` - Core Components section (Task Model and Task Manager)

## Requirements
- Implement Task class with all specified attributes (id, title, description, status, created_at)
- Implement proper validation (title ≤ 255 chars, description ≤ 1000 chars, non-empty title)
- Implement TaskManager with all CRUD methods
- Add validation helper methods to TaskManager
- Write unit tests for both components

## Files to Create/Modify
- src/core/models.py
- src/core/task_manager.py
- src/tests/test_models.py
- src/tests/test_task_manager.py

## Dependencies
- T-001: Setup Project Structure must be completed first

## Acceptance Criteria
- [ ] Task class implements all required attributes with proper validation
- [ ] TaskManager implements all CRUD methods with proper validation
- [ ] All validation requirements (length, non-empty) are enforced
- [ ] Unit tests cover all validation scenarios
- [ ] Human-readable timestamp formatting is implemented