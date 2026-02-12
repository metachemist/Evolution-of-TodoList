# Tasks: FastAPI Todo Backend

**Feature**: Multi-User Todo REST API with FastAPI, SQLModel, and Neon PostgreSQL
**Branch**: `001-fastapi-todo-backend`
**Created**: 2026-02-11
**Spec**: @specs/1-specify/phase-2/feature-01-fastapi-todo-backend.md
**Plan**: @specs/2-plan/phase-2/phase-2-fastapi-todo-backend.md

## Implementation Strategy

Build a persistent, multi-user Todo REST API using FastAPI, SQLModel ORM, and Neon PostgreSQL. Implementation follows an incremental approach with each user story forming a complete, independently testable increment.

**MVP Scope**: User Story 1 - Basic task management (create, read, update, delete) with user isolation.

## Dependencies

- User Story 2 (Secure Task Access) requires Authentication & Authorization Setup (Phase 3) and User Story 1 (Manage Personal Tasks) to be complete
- User Story 3 (Error Handling) can be implemented in parallel with other stories but requires foundational setup and authentication
- Authentication & Authorization Setup (Phase 3) requires Foundational Phase (Phase 2) to be complete

## Parallel Execution Examples

- Database models and authentication utilities can be developed in parallel (during Phase 2 and Phase 3)
- Individual CRUD endpoints can be developed in parallel after authentication setup (Phase 4)
- Unit tests can be written in parallel with feature development
- Schema definitions can be created in parallel during Phase 4

---

## Phase 1: Setup

Initialize project structure and dependencies.

- [X] T001 Create project directory structure in backend/
- [X] T002 Initialize pyproject.toml with FastAPI, SQLModel, Pydantic dependencies
- [X] T003 Set up basic configuration files (.env.example, .gitignore)
- [X] T004 Create CLAUDE.md with backend-specific instructions

---

## Phase 2: Foundational

Set up foundational components required by all user stories.

- [X] T005 Create User SQLModel with id (UUID), email (unique), hashed_password, created_at, updated_at
- [X] T006 Create Task SQLModel with id (UUID), title (max 255), description (max 5000, optional), is_completed, timestamps, owner_id (FK to User)
- [X] T007 Set up async database connection with Neon PostgreSQL
- [X] T008 Implement get_db_session() dependency function with proper session creation and cleanup
- [X] T009 Initialize Alembic for database migrations
- [X] T010 Create initial migration (001_initial_models.py) to create User and Task tables
- [X] T011 Configure Alembic environment for different environments (dev, staging, prod)
- [X] T012 Install project dependencies using pyproject.toml
- [X] T013 Create main.py with FastAPI app initialization
- [X] T014 Set up basic configuration and middleware
- [X] T015 Implement health check endpoint
- [X] T016 Configure CORS and other basic settings
- [X] T017 Run initial database migration
- [X] T018 Set up test database configuration

---

## Phase 3: Authentication & Authorization Setup

Set up authentication infrastructure required for all user stories.

**Goal**: Implement JWT-based authentication and user isolation to ensure users can only access their own tasks.

**Independent Test**: Can be tested by verifying that JWT tokens are properly extracted and validated, and that user IDs are correctly extracted from tokens.

- [X] T019 Implement JWT token extraction from Authorization header as Bearer token in src/utils/auth.py
- [X] T020 Create get_current_user_id function with signature: `async def get_current_user_id(authorization: str = Header(...)) -> str` in src/utils/auth.py
- [X] T021 Add token validation (signature and expiration) in src/utils/auth.py
- [X] T022 Return user ID from token claims in src/utils/auth.py
- [X] T023 Implement auth middleware to intercept requests to protected endpoints in src/middleware/auth_middleware.py
- [X] T024 Add JWT token validation in middleware in src/middleware/auth_middleware.py
- [X] T025 Attach user context to request in middleware in src/middleware/auth_middleware.py
- [X] T026 Implement global exception handler for consistent responses in src/main.py
- [X] T027 Create custom error response format implementation in src/utils/helpers.py

---

## Phase 4: [US1] Manage Personal Tasks

Enable users to create, view, update, and delete their personal tasks through the API.

**Goal**: A user can create, view, update, and delete their personal tasks through an API. They should be able to mark tasks as completed and see only their own tasks.

**Independent Test**: Can be fully tested by creating a user, adding tasks, viewing them, updating them, and deleting them. Delivers the core value of a todo app.

- [X] T028 [P] Create TaskCreate schema (title, optional description) in src/schemas/task.py
- [X] T029 [P] Create TaskUpdate schema (optional title, optional description) in src/schemas/task.py
- [X] T030 [P] Create TaskResponse schema (id, title, description, is_completed, timestamps, owner_id) in src/schemas/task.py
- [X] T031 [P] Create ErrorResponse schema (code, message, details) in src/schemas/common.py
- [X] T032 [P] Create UserResponse schema (id, email, timestamps) in src/schemas/user.py
- [X] T033 [P] Implement create_task function in src/services/task_service.py
- [X] T034 [P] Implement get_tasks function in src/services/task_service.py
- [X] T035 [P] Implement get_task_by_id function in src/services/task_service.py
- [X] T036 [P] Implement update_task function in src/services/task_service.py
- [X] T037 [P] Implement delete_task function in src/services/task_service.py
- [X] T038 [P] Implement toggle_completion function in src/services/task_service.py
- [X] T039 [P] Implement get_user_by_id function in src/services/user_service.py
- [X] T040 Implement GET /api/{user_id}/tasks endpoint to retrieve all tasks for user in src/routes/tasks.py
- [X] T041 Implement POST /api/{user_id}/tasks endpoint to create new task in src/routes/tasks.py
- [X] T042 Implement GET /api/{user_id}/tasks/{id} endpoint to retrieve specific task in src/routes/tasks.py
- [X] T043 Implement PUT /api/{user_id}/tasks/{id} endpoint to update task details in src/routes/tasks.py
- [X] T044 Implement DELETE /api/{user_id}/tasks/{id} endpoint to delete task in src/routes/tasks.py
- [X] T045 Implement PATCH /api/{user_id}/tasks/{id}/complete endpoint to toggle completion status in src/routes/tasks.py

---

## Phase 5: [US2] Secure Task Access

Ensure users can only access their own tasks and receive appropriate error messages when trying to access others' tasks.

**Goal**: A user should only be able to access their own tasks and should receive appropriate error messages when trying to access others' tasks.

**Independent Test**: Can be tested by attempting to access tasks owned by different users and verifying appropriate access controls.

- [X] T046 Implement user isolation verification (both path and database checks) in src/routes/tasks.py
- [X] T047 Update all task endpoints to validate user ownership in src/routes/tasks.py

---

## Phase 6: [US3] Error Handling

Provide clear, structured error responses when users encounter errors.

**Goal**: When users encounter errors (validation, authentication, etc.), the system should return clear, structured error responses.

**Independent Test**: Can be tested by triggering various error conditions and verifying appropriate error responses.

- [X] T048 Add comprehensive input validation with Pydantic schemas in all route handlers
- [X] T049 Test all error scenarios and response formats in tests/test_routes/test_tasks.py
- [X] T050 Implement proper database indexing strategy on foreign keys and frequently queried fields
- [X] T051 Optimize queries to prevent N+1 problems in src/services/task_service.py

---

## Phase 7: Polish & Cross-Cutting Concerns

Final implementation touches and cross-cutting concerns.

- [X] T052 Write unit tests for all service layer functions in tests/test_services/
- [X] T053 Create integration tests for all API endpoints in tests/test_routes/
- [X] T054 Implement security-focused tests for user isolation in tests/test_security.py
- [X] T055 Add performance tests to validate response times in tests/test_performance.py
- [X] T056 Create API documentation with examples in docs/api.md
- [X] T057 Set up Docker configuration for backend in docker/backend.Dockerfile
- [X] T058 Prepare deployment scripts and environment setup in docker/docker-compose.yml
- [X] T059 Document operational procedures in docs/operations.md
- [X] T060 Run full test suite and verify all functionality
- [X] T061 Perform final code review and documentation verification