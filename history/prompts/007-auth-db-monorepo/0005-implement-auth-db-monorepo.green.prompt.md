---
id: "0005"
title: implement-auth-db-monorepo
stage: green
date: 2026-02-15
surface: claude-code
model: claude-sonnet-4-5-20250929
feature: 007-auth-db-monorepo
branch: 007-auth-db-monorepo
user: metachemist
command: /sp.implement
labels: [green, auth, jwt, argon2, cookies, rate-limiting, migrations, fastapi, nextjs]
links:
  spec: specs/1-specify/phase-2/feature-03-auth-db-monorepo.md
  plan: specs/2-plan/phase-2/phase-2-auth-db-monorepo.md
  tasks: specs/3-tasks/phase-2/auth-db-tasks.md
  ticket: ""
  adr: "history/adr/0011-auth-session-transport-and-contract.md"
  pr: ""
files:
  - backend/src/utils/error_mapper.py
  - backend/src/utils/token.py
  - backend/src/services/auth_service.py
  - backend/src/routes/auth.py
  - backend/src/middleware/auth.py
  - backend/src/middleware/rate_limit.py
  - backend/src/routes/tasks.py
  - backend/src/main.py
  - backend/alembic/versions/002_add_performance_indexes.py
  - backend/alembic/versions/003_delete_orphan_tasks.py
  - backend/alembic/versions/004_enforce_tasks_owner_id_not_null.py
  - backend/docker/backend.Dockerfile
  - backend/docker/docker-compose.yml
  - backend/tests/test_routes/test_auth.py
  - backend/tests/test_routes/test_tasks_auth.py
  - backend/tests/test_services/test_auth_service.py
  - backend/tests/test_routes/test_tasks.py
  - backend/tests/test_performance/test_session_overhead.py
  - backend/tests/test_performance/test_task_volume.py
  - backend/tests/load/locustfile.py
  - backend/tests/conftest.py
  - backend/CLAUDE.md
  - frontend/src/middleware.ts
  - frontend/src/app/(auth)/login/page.tsx
  - frontend/CLAUDE.md
  - specs/2-plan/phase-2/api-specs/auth-and-task-contracts.md
  - specs/2-plan/phase-2/db-schema/auth-storage-schema.md
  - specs/2-plan/phase-2/db-schema/auth-migration-plan.md
  - specs/3-tasks/phase-2/auth-db-tasks.md
tests:
  - backend/tests/test_routes/test_auth.py (17 tests)
  - backend/tests/test_routes/test_tasks_auth.py (9 tests)
  - backend/tests/test_services/test_auth_service.py (17 tests)
  - backend/tests/test_routes/test_tasks.py (8 tests)
  - backend/tests/test_performance/test_session_overhead.py (PERF-002)
  - backend/tests/test_performance/test_task_volume.py (PERF-005)
---

## Prompt

/sp.implement — Execute all 41 tasks across 7 phases for feature `007-auth-db-monorepo` (Authentication & Persistent Storage). Session continued from a prior context window where tool calls were initially rejected.

## Response

Implemented all 41 tasks across 7 phases for the `007-auth-db-monorepo` feature. Final test suite: **77/77 PASSED**.

### Phase 1 — Setup (T001–T003)
- Created `specs/2-plan/phase-2/api-specs/auth-and-task-contracts.md` (contract freeze: endpoint matrix, auth precedence, error catalog with 12 entries, CORS config, rate-limit policy, two-layer authorization flow)
- Updated both `.env.example` files with new vars (`CORS_ORIGIN`, `COOKIE_DOMAIN`, `REDIS_URL`, `ACCESS_TOKEN_EXPIRE_SECONDS`, `BETTER_AUTH_SECRET`, `BETTER_AUTH_URL`)
- Installed `better-auth` (npm) and `argon2-cffi`, `redis[asyncio]` (poetry)

### Phase 2 — Foundational (T004–T011)
- Models (`user`, `task`) confirmed compatible with existing SQLModel schema (singular table names)
- Created `backend/src/utils/error_mapper.py`: 12 `AppException` subclasses with exact catalog messages; `map_exception_to_response` returning `{success, data, error}` envelope
- Fixed `backend/src/main.py`: CORS wildcard → `CORS_ORIGIN` env var; registered `AppException` global handler; added `RateLimitMiddleware`
- Created `backend/alembic/versions/002_add_performance_indexes.py`: 4 indexes (`ix_user_email`, `ix_task_owner_id`, `ix_task_is_completed`, `ix_task_created_at`) with `if_not_exists=True` for idempotency

### Phase 3 — US1+US3: Auth & Persistence (T012–T018)
- Rewrote `backend/src/services/auth_service.py`: Argon2id (time_cost=3, memory_cost=65536, parallelism=2), email normalization, email/password validation with catalog-exact error messages, full async ORM queries
- Created `backend/src/utils/token.py`: `create_token()` + `decode_token()` — raises `SessionExpiredError` / `InvalidTokenError` (never returns None)
- Rewrote `backend/src/routes/auth.py`: all 4 endpoints (`register`, `login`, `logout`, `me`) with httpOnly cookie (`Set-Cookie: access_token=...; HttpOnly; Secure; SameSite=Lax; Max-Age=86400; Path=/`), `{success, data, error}` response envelope throughout

### Phase 4 — US5+US2: Auth Guard & Task Isolation (T019–T023)
- Created `backend/src/middleware/auth.py`: `require_authenticated_user` FastAPI Depends() — Bearer header takes precedence over cookie; raises typed `AppException` subclasses (never `HTTPException`)
- Rewrote `backend/src/routes/tasks.py`: all 6 routes use `Depends(require_authenticated_user)`; `_enforce_user_id_match()` guard raises `ForbiddenError()` before any DB query (Layer 1); task ownership miss raises `TaskNotFoundError()` (Layer 2)

### Phase 5 — US4: Session Expiry UX (T024–T025)
- **F05 fix**: Rewrote `frontend/src/middleware.ts` to explicitly forward `Cookie: access_token=<value>` in server-side fetch (`credentials: 'include'` is ignored in Next.js Edge middleware)
- Added `role="alert" aria-live="polite"` session-expired banner on `/login` page when `?reason=session_expired`

### Phase 6 — US6: Data Migration (T026–T028)
- Created migrations `003_delete_orphan_tasks.py` (irreversible orphan DELETE) and `004_enforce_tasks_owner_id_not_null.py` (NOT NULL enforcement)
- Updated Docker CMD to run `alembic upgrade head` before uvicorn
- Added Redis service to `docker-compose.yml` with healthcheck; added all new env vars
- Created `auth-storage-schema.md` and `auth-migration-plan.md` in `specs/2-plan/phase-2/db-schema/`

### Phase 7 — Polish (T029–T041)
- Created `backend/src/middleware/rate_limit.py`: `RateLimitAdapter` Protocol, `InMemoryAdapter` (asyncio.Lock, window expiry), `RedisAdapter` (INCR+EXPIRE pattern), `RateLimitMiddleware` with **F02 fix** (JWT extracted directly from header/cookie — middleware never reads from `request.state`)
- Wrote all test files: 17 auth route tests (T032+T033), 9 task auth integration tests (T034), 17 auth service unit tests (T035), Locust load test (T036), PERF-002 session overhead benchmark (T040), PERF-005 10K-task volume test (T041)
- Updated `backend/CLAUDE.md` and `frontend/CLAUDE.md` with auth patterns and task traceability

### Key Bugs Fixed During Implementation
1. **`test_error_response_format`** (401 vs 404): Old test used fake user_id in token; new `require_authenticated_user` looks up user in DB → 401. Fixed: create real user, request non-existent task_id → 404.
2. **Import breakage in `test_tasks.py`**: `from src.utils.auth import get_password_hash` → `from src.services.auth_service import hash_password as get_password_hash`
3. **conftest.py token API change**: `create_access_token(data={"sub": uid})` → `create_token(UUID(uid_str), email)` from new `src.utils.token`
4. **Table name mismatch**: Task plan assumed `users`/`tasks` (plural); existing SQLModel uses `user`/`task` (singular). All migrations adapted accordingly.

### Architectural Remediations Applied (v3 tasks)
- **F01**: T011 `[P]` tag removed — depends on T010 (AppException)
- **F02**: Rate-limit middleware extracts JWT directly, not from `request.state`
- **F03**: Error catalog exactness verified via test assertions in T033 (not a separate task)
- **F04**: T040 added (PERF-002 session overhead ≤ 50ms)
- **F05**: T024 rewritten — explicit `Cookie:` header forwarding in Edge middleware
- **T041**: Added for PERF-005 (10,000 tasks/user volume test, ≤ 300ms)
