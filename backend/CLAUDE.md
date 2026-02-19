# Backend Development Guidelines

## Project Overview
This is a FastAPI-based backend for a multi-user Todo application using SQLModel ORM and Neon PostgreSQL. The API provides full CRUD operations for tasks with proper user isolation and authentication middleware.

## Tech Stack
- **Framework**: FastAPI (latest stable)
- **ORM**: SQLModel
- **Database**: PostgreSQL (Neon)
- **Validation**: Pydantic
- **Authentication**: JWT tokens

## Architecture
- **Models**: SQLModel classes in `src/models/`
- **Schemas**: Pydantic classes for validation in `src/schemas/`
- **Routes**: API endpoints in `src/routes/`
- **Services**: Business logic in `src/services/`
- **Middleware**: Custom middleware in `src/middleware/`
- **Utils**: Helper functions in `src/utils/`

## Key Patterns
1. **Dependency Injection**: Use FastAPI's dependency system
2. **Separation of Concerns**: Keep business logic in services, not route handlers
3. **Async Operations**: Use async/await for I/O operations
4. **Error Handling**: Use consistent error response format
5. **Authentication**: All endpoints require JWT validation

## File Structure
```
backend/
├── pyproject.toml          # Dependencies and configuration
├── src/
│   ├── main.py             # FastAPI app entry point
│   ├── database.py         # Database connection and session management
│   ├── models/             # SQLModel database models
│   ├── schemas/            # Pydantic schemas for validation
│   ├── routes/             # API route handlers
│   ├── services/           # Business logic layer
│   ├── middleware/         # Custom middleware
│   └── utils/              # Utility functions
├── tests/                  # Test files
├── alembic/                # Database migrations
├── docker/                 # Docker configuration
├── .env.example           # Environment variables template
└── .gitignore
```

## Important Implementation Notes
- All database operations should be async
- Use UUID primary keys for User and Task models
- Implement proper user isolation (users can only access their own tasks)
- Follow REST conventions for endpoint design
- Use consistent error response format: `{success: boolean, data: any, error: object}`
- Implement proper validation with Pydantic schemas
- Character limits: Title (255 chars), Description (5000 chars)

## Security Considerations
- Validate JWT tokens on every request
- Verify user_id in URL path matches JWT claims
- Return 401 for missing/invalid tokens
- Return 403 for authorization failures
- Sanitize all user inputs to prevent injection attacks

## Feature 007: Auth & DB Patterns (Task: T038)

### Password Hashing — Argon2id
- Library: `argon2-cffi` via `from argon2 import PasswordHasher`
- Fixed params: `time_cost=3, memory_cost=65536, parallelism=2`
- **Never lower these params without a new ADR** (see ADR-0011)
- Hash func: `src/services/auth_service.py::hash_password()`

### JWT Format — HS256
- Library: `python-jose` (`from jose import jwt`)
- Token: `{"sub": str(user.id), "email": user.email, "exp": now + 86400s}`
- 24-hour absolute expiry — no refresh token flow
- Token helpers: `src/utils/token.py::create_token()`, `decode_token()`
- `decode_token` raises `SessionExpiredError` (401) or `InvalidTokenError` (401) — never returns None

### Cookie Settings
- `httponly=True, secure=COOKIE_SECURE env var, samesite="lax", max_age=86400, path="/"`
- `COOKIE_SECURE=false` in dev (localhost); `true` in production
- Cookie helper: `src/routes/auth.py::_set_auth_cookie()`, `_clear_auth_cookie()`

### Auth Dependency
- `require_authenticated_user` in `src/middleware/auth.py` — use as FastAPI Depends()
- Reads Bearer header first, then access_token cookie
- Returns full `User` ORM object; raises `AppException` subclass (never `HTTPException`)

### Two-Layer Authorization (SEC-003 + SEC-004)
- Call `_enforce_user_id_match(user_id, current_user)` at top of task route handlers
- **Layer 1**: if `str(user_id) != str(current_user.id)` → raise `ForbiddenError()` (no DB query)
- **Layer 2**: if task not found for user → raise `TaskNotFoundError()` (via service returning None)
- Do NOT raise 403 at service layer — only in route handlers before DB queries

### Error Mapper Rule
- **Never** construct ad-hoc error strings in route handlers
- Always raise an `AppException` subclass from `src/utils/error_mapper.py`
- All 12 error types are defined there with exact catalog messages
- Global handler in `main.py::app_exception_handler()` converts to wrapped JSON

### Rate Limiting
- Middleware: `src/middleware/rate_limit.py::RateLimitMiddleware`
- **F02**: Middleware runs before Depends(); read JWT directly from header/cookie in middleware
- Authenticated: 1000 req/hr by `rate:user:{user_id}:{epoch_hour}`
- Unauthenticated: 100 req/hr by `rate:ip:{ip}:{epoch_hour}`
- Redis-backed in production; InMemoryAdapter fallback when REDIS_URL absent

### Task Traceability
- Every new file must include: `# Task: T0XX — <one-line description>`
- ORM only: never write raw SQL (constitution requirement)

### Migration Run Order
- 001_initial_models → 002_add_performance_indexes → 003_delete_orphan_tasks → 004_owner_id_not_null → 005_owner_fk_cascade
- Run via: `alembic upgrade head` (Docker CMD does this automatically)

## Test Commands (Reliable Imports)

- Run from backend directory: `cd backend`
- Either command is supported:
  - `poetry run pytest`
  - `python -m pytest` (when backend env is activated, e.g. `poetry shell`)
- Import reliability is enforced by:
  - `pythonpath = ["."]` in `backend/pyproject.toml`
  - path bootstrap in `backend/tests/conftest.py`
