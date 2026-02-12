# Implementation Plan: FastAPI Todo Backend

**Branch**: `001-fastapi-todo-backend` | **Date**: 2026-02-11 | **Spec**: @specs/1-specify/phase-2/feature-01-fastapi-todo-backend.md
**Input**: Feature specification for multi-user Todo REST API with FastAPI, SQLModel, and Neon PostgreSQL

## Summary

Build a persistent, multi-user Todo REST API using FastAPI, SQLModel ORM, and Neon PostgreSQL. The API will provide full CRUD operations for tasks with proper user isolation, authentication middleware placeholder, and structured error responses. The implementation will follow REST architecture with JSON responses only.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: FastAPI (latest stable), SQLModel, Pydantic, Neon PostgreSQL driver
**Storage**: PostgreSQL database hosted on Neon
**Testing**: pytest for unit/integration tests
**Target Platform**: Linux server environment
**Project Type**: Backend API service
**Performance Goals**: 95% of requests respond within 500ms under normal load (up to 100 concurrent users)
**Constraints**: <500ms p95 response time, support 10,000 tasks per user, 100 concurrent users
**Scale/Scope**: Multi-user system supporting 10,000+ tasks per user

## Constitution Check

This implementation plan adheres to the Todo Evolution Constitution by:
- Following the SDD Loop (Specification → Plan → Tasks → Implement)
- Supporting the mandatory monorepo structure with proper backend/ directory
- Ensuring traceability to task IDs in `specs/3-tasks/`
- Aligning with the technology stack requirements (FastAPI, SQLModel, PostgreSQL)
- Maintaining security and privacy standards (user isolation, JWT validation)

## Project Structure

### Documentation (this feature)

```text
specs/2-plan/phase-2/
├── phase-2-fastapi-todo-backend.md    # This file
├── api-specs/
│   ├── rest-endpoints.md
│   ├── mcp-tools.md
│   └── websocket-events.md
├── db-schema/
│   ├── schema-v1.md
│   ├── schema-v2.md
│   └── migrations.md
└── ui-design/
    ├── components.md
    ├── pages.md
    └── chatkit-integration.md
```

### Source Code (repository root)

```text
backend/
├── CLAUDE.md                    # Backend-specific Claude instructions
├── pyproject.toml              # Project dependencies and configuration
├── alembic/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       └── 001_initial_models.py
├── src/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entry point
│   ├── database.py             # Database connection and session management
│   ├── models/                 # SQLModel database models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── task.py
│   ├── schemas/                # Pydantic schemas for validation and serialization
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── task.py
│   │   └── common.py
│   ├── routes/                 # API route handlers
│   │   ├── __init__.py
│   │   ├── tasks.py
│   │   └── auth.py
│   ├── services/               # Business logic layer
│   │   ├── __init__.py
│   │   ├── task_service.py
│   │   └── user_service.py
│   ├── middleware/             # Custom middleware
│   │   ├── __init__.py
│   │   └── auth_middleware.py
│   └── utils/                  # Utility functions
│       ├── __init__.py
│       ├── auth.py
│       └── helpers.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_main.py
│   ├── test_models.py
│   ├── test_schemas.py
│   ├── test_routes/
│   │   ├── __init__.py
│   │   ├── test_tasks.py
│   │   └── test_auth.py
│   └── test_services/
│       ├── __init__.py
│       └── test_task_service.py
├── .env.example               # Environment variables template
└── docker/
    ├── backend.Dockerfile
    └── docker-compose.yml
```

## Architecture Components

### 1. Database Layer
- **SQLModel Models**: User and Task models with proper relationships
  - User model: id (UUID), email (unique), hashed_password, created_at, updated_at
  - Task model: id (UUID), title (max 255), description (max 5000, optional), is_completed, created_at, updated_at, owner_id (FK to User)
  - Proper indexing on foreign keys and frequently queried fields
- **Connection Management**: Async database connection with connection pooling
- **Session Dependency**: FastAPI dependency for database sessions
  - Function signature: `async def get_db_session() -> AsyncSession`
  - Handles session creation and cleanup
- **Migrations**: Alembic for database schema migrations
  - Initial migration (001_initial_models.py) to create User and Task tables
  - Auto-generation of migration files using Alembic
  - Environment configuration for different environments (dev, staging, prod)

### 2. Authentication & Authorization Layer
- **JWT Token Extraction**: From Authorization header as Bearer token
- **User ID Dependency**: `get_current_user_id` function to extract user ID
  - Function signature: `async def get_current_user_id(authorization: str = Header(...)) -> str`
  - Extracts JWT from "Authorization: Bearer <token>" header
  - Validates token signature and expiration
  - Returns user ID from token claims
- **Access Validation**: Verify user_id in URL path matches authenticated user
- **Database Verification**: Confirm task ownership through database lookup
- **Auth Middleware**: Custom middleware to handle authentication flow
  - Intercepts requests to protected endpoints
  - Validates JWT tokens
  - Attaches user context to request

### 3. Service Layer
- **Task Service**: Business logic for task operations with specific functions:
  - create_task(db: AsyncSession, user_id: str, title: str, description: str | None) -> Task
  - get_tasks(db: AsyncSession, user_id: str) -> List[Task]
  - get_task_by_id(db: AsyncSession, user_id: str, task_id: int) -> Task | None
  - update_task(db: AsyncSession, user_id: str, task_id: int, title: str, description: str | None) -> Task | None
  - delete_task(db: AsyncSession, user_id: str, task_id: int) -> bool
  - toggle_completion(db: AsyncSession, user_id: str, task_id: int) -> Task | None
- **User Service**: Business logic for user operations:
  - get_user_by_id(db: AsyncSession, user_id: str) -> User | None
- **Separation of Concerns**: Keep business logic separate from route handlers

### 4. API Layer (Routes)
- **REST Endpoints**: Under `/api/{user_id}/` prefix
- **CRUD Operations**: Full CRUD for tasks with proper HTTP methods
  - GET /api/{user_id}/tasks - Retrieve all tasks for user
  - POST /api/{user_id}/tasks - Create new task
  - GET /api/{user_id}/tasks/{id} - Retrieve specific task
  - PUT /api/{user_id}/tasks/{id} - Update task details
  - DELETE /api/{user_id}/tasks/{id} - Delete task
  - PATCH /api/{user_id}/tasks/{id}/complete - Toggle completion status
- **Validation**: Pydantic schema validation for all inputs
- **Error Handling**: Consistent error responses using middleware

### 5. Error Handling & Validation
- **Pydantic Schemas**: For request/response validation
  - TaskCreate: For creating new tasks (title, optional description)
  - TaskUpdate: For updating existing tasks (optional title, optional description)
  - TaskResponse: For returning task data (id, title, description, is_completed, timestamps, owner_id)
  - ErrorResponse: For structured error responses (code, message, details)
  - UserResponse: For returning user data (id, email, timestamps)
- **Custom Exceptions**: For different error scenarios
- **Global Exception Handler**: For consistent error responses
- **Validation Constraints**: Character limits for title (255) and description (5000)

## Implementation Phases

### Phase 1: Foundation Setup
1. Project structure and dependencies setup
2. Database connection and models implementation
3. Basic FastAPI application structure
4. Initial testing framework

### Phase 2: Core API Implementation
1. Authentication middleware implementation
2. Task CRUD operations implementation
3. User isolation and access control
4. Response format consistency

### Phase 3: Advanced Features & Testing
1. Error handling and validation
2. Performance optimizations
3. Comprehensive testing (unit, integration)
4. Documentation and deployment setup

## Dependencies Between Components

### High-Level Dependencies
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   API Layer     │───▶│  Service Layer   │───▶│  Database Layer │
│   (routes)      │    │ (business logic) │    │   (models)      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │
         ▼
┌─────────────────┐
│ Auth Middleware │
│ (user isolation)│
└─────────────────┘
```

### Detailed Dependencies
1. **API Layer** depends on:
   - Service Layer for business logic
   - Authentication middleware for user validation
   - Pydantic schemas for input/output validation

2. **Service Layer** depends on:
   - Database models for data operations
   - Database session for persistence
   - Authentication layer for user context

3. **Database Layer** depends on:
   - SQLModel for ORM functionality
   - Database connection configuration

4. **Authentication Layer** depends on:
   - Database models to verify user ownership
   - JWT libraries for token handling

## Design Decisions

### 1. Database Design
- **UUID Primary Keys**: Using UUIDs for both User and Task models for better security and distributed systems compatibility
- **Foreign Key Relationships**: Task.owner_id references User.id with proper indexing
- **Timestamps**: Automatic created_at and updated_at fields on both models
- **Character Limits**: Title (255 chars), Description (5000 chars) as specified

### 2. Authentication & Authorization
- **Bearer Token Authentication**: Extract JWT from Authorization header
- **Dual Verification**: Both URL path comparison AND database ownership check
- **Dependency Injection**: Using FastAPI's dependency system for user validation
- **Placeholder for Future**: Authentication details to be implemented in future phases

### 3. API Design
- **RESTful Architecture**: Following REST conventions with proper HTTP methods
- **Consistent Response Format**: All responses follow the same structure with success/data/error pattern
- **User ID in Path**: All endpoints include user_id in path for explicit routing
- **Structured Error Responses**: Consistent error format with code, message, and details

### 4. Service Layer Architecture
- **Separation of Concerns**: Business logic separated from route handlers
- **Reusable Functions**: Service functions can be used across multiple endpoints
- **Transaction Management**: Proper handling of database transactions
- **Error Propagation**: Clear error handling from service to API layer

### 5. Error Handling Strategy
- **Centralized Error Handling**: Global exception handlers for consistent responses
- **Validation at Multiple Levels**: Input validation at API and service layers
- **Structured Error Responses**: Following the specified error format
- **Logging**: Proper logging of errors for debugging and monitoring

## Security Considerations

### 1. User Isolation
- **Ownership Verification**: Every operation validates that user owns the resource
- **Path Parameter Validation**: Verify user_id in URL matches authenticated user
- **Database-Level Checks**: Confirm ownership through database lookup

### 2. Input Validation
- **Schema Validation**: All inputs validated using Pydantic schemas
- **Character Limits**: Enforced at both API and database levels
- **Sanitization**: Input sanitization to prevent injection attacks

### 3. Authentication
- **JWT Token Validation**: Verify token validity and expiration
- **Secure Storage**: Passwords stored using bcrypt or equivalent
- **Transport Security**: All APIs should be served over HTTPS

## Performance Considerations

### 1. Database Optimization
- **Proper Indexing**: Indexes on foreign keys and frequently queried fields
- **Connection Pooling**: Efficient database connection management
- **Query Optimization**: Avoid N+1 queries with proper JOINs when needed

### 2. API Performance
- **Response Caching**: Consider caching for frequently accessed data
- **Pagination**: Implement pagination for large result sets (future enhancement)
- **Rate Limiting**: Per-user rate limiting to prevent abuse

### 3. Resource Management
- **Async Operations**: Use async/await for I/O operations
- **Memory Efficiency**: Efficient serialization and deserialization
- **Connection Management**: Proper cleanup of database connections

## Testing Strategy

### 1. Unit Tests
- **Models**: Test database model validations and relationships
- **Services**: Test business logic functions in isolation
- **Utilities**: Test helper functions and utilities

### 2. Integration Tests
- **API Routes**: Test API endpoints with real database connections
- **Authentication**: Test authentication and authorization flows
- **Error Handling**: Test error scenarios and responses

### 3. Test Coverage
- **Target**: 70%+ test coverage for business logic
- **Critical Paths**: Ensure all authentication and authorization paths are tested
- **Edge Cases**: Test boundary conditions and error scenarios

## Deployment Considerations

### 1. Environment Configuration
- **Environment Variables**: Database credentials, JWT secrets, etc.
- **Configuration Management**: Separate configs for dev, staging, prod
- **Secrets Management**: Secure handling of sensitive information

### 2. Infrastructure
- **Containerization**: Docker container for consistent deployment
- **Database Migrations**: Automated migration handling during deployment
- **Health Checks**: API endpoints for monitoring service health

### 3. Monitoring
- **Logging**: Structured logging for debugging and monitoring
- **Metrics**: Performance and usage metrics
- **Error Tracking**: Centralized error reporting and alerting

## Parallel Development Opportunities

### Phase 1: Foundation Setup
- **Parallel Tasks**:
  - Database models and connection setup can be developed simultaneously
  - Project structure and dependency setup can happen in parallel with basic app creation
  - Initial testing framework can be set up while other components are being built

### Phase 2: Core API Implementation
- **Parallel Tasks**:
  - Authentication middleware can be developed alongside API routes
  - Individual CRUD operations (Create, Read, Update, Delete) can be developed in parallel by different developers
  - Service layer functions can be developed in parallel with corresponding API endpoints
  - User isolation and access control can be implemented alongside individual endpoints

### Phase 3: Advanced Features & Testing
- **Parallel Tasks**:
  - Unit tests can be written in parallel with feature development (TDD approach)
  - Integration tests can be developed as API endpoints are completed
  - Performance optimizations can happen while other features are being tested
  - Documentation can be created in parallel with implementation

## Risk Assessment & Mitigation

### High-Risk Areas
1. **Authentication Implementation**: Complex security requirements
   - *Mitigation*: Thorough code reviews, security-focused testing, use proven libraries

2. **Database Performance**: Supporting 10,000+ tasks per user
   - *Mitigation*: Early performance testing, proper indexing, query optimization

3. **User Isolation**: Ensuring users can only access their own data
   - *Mitigation*: Comprehensive authorization tests, database-level constraints, dual verification approach

### Medium-Risk Areas
1. **Concurrent User Handling**: Supporting 100 concurrent users
   - *Mitigation*: Load testing, connection pooling, async operations

2. **Error Handling Consistency**: Maintaining uniform error responses
   - *Mitigation*: Centralized error handling, clear error response contracts

## Team Coordination Strategy

### API Contract Definition
- Define Pydantic schemas early to enable parallel development
- Establish clear endpoint contracts before implementation begins
- Use shared documentation to ensure consistency

### Integration Points
- Regular integration meetings to ensure components work together
- Continuous integration with automated testing
- Shared database schema documentation

### Development Workflow
- Use feature flags for incomplete features
- Implement in small, testable increments
- Conduct regular code reviews focusing on security and performance