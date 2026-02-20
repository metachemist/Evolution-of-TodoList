# Tasks: Authentication & Persistent Storage

**Feature**: Phase 2 Part 3 — Secure Multi-User Isolation and Persistent Storage
**Branch**: `007-auth-db-monorepo`
**Created**: 2026-02-15
**Revised**: 2026-02-15 (v3 — F01–F05 remediation: T011 dep fix, T031 middleware redesign, T024 cookie-forwarding fix, T040+T041 added for PERF-002/PERF-005)
**Spec**: @specs/1-specify/phase-2/feature-03-auth-db-monorepo.md
**Plan**: @specs/2-plan/phase-2/phase-2-auth-db-monorepo.md

## Implementation Strategy

Extend the existing FastAPI backend and Next.js frontend with real authentication, user-scoped task isolation, PostgreSQL persistence, and durable schema migrations. The backend gains Argon2id password hashing, HS256 JWT tokens issued as httpOnly cookies, and a two-layer authorization guard (403 path mismatch → 404 ownership miss). The frontend installs `better-auth` and tightens session validation in middleware. Rate limiting and the centralized error catalog ship in the polish phase.

**MVP Scope**: User Story 1 (Registration & Login) + User Story 3 (Persistent Storage) — delivers a working authenticated backend with durable data.

## Task Count

41 tasks across 7 phases | avg ~20–25 min per task

## Dependencies

- Phase 1 (T001–T003) must precede Phase 2 — contract freeze before any code
- Phase 2 (T004–T011): [P] group first, then T008, then T009 sequentially
- Phase 3 (T012–T018): T012 → T013 sequential (same file); T014 parallel; T015 → T016 → T017 → T018 sequential (same file); all require Phase 2
- Phase 4 (T019–T023): T019 → T020 → T021 sequential; T022+T023 parallel after T019; requires Phase 3
- Phase 5 (T024–T025): requires Phase 4 (auth guard must exist before session expiry UX)
- Phase 6 (T026–T028): T026 requires Phase 2 migrations (T008, T009) + Phase 4 ownership model locked; T027 after T026; T028 parallel
- Phase 7 (T029–T039): requires all story phases complete

## Parallel Execution Examples

```bash
# Phase 2 — launch [P] tasks together, then T011 after T010:
Task: "User model in backend/src/models/user.py"               # T004 [P]
Task: "Task model update in backend/src/models/task.py"        # T005 [P]
Task: "database.py async engine + get_db"                      # T006 [P]
Task: "alembic init + alembic.ini + env.py"                   # T007 [P]
Task: "Error mapper in backend/src/utils/error_mapper.py"      # T010 [P]
# After T010 completes:
Task: "CORS + global exception handler in backend/src/main.py" # T011 (depends on T010)

# Phase 3 — JWT helper parallel with AuthService:
Task: "AuthService validation in backend/src/services/auth_service.py" # T012
Task: "JWT helper in backend/src/utils/token.py"                        # T014

# Phase 4 — TaskService updates parallel after T019:
Task: "TaskService.create_task user_id"         # T022
Task: "TaskService user-scoped queries"         # T023

# Phase 7 — test files parallel:
Task: "Task auth tests in test_tasks_auth.py"              # T034
Task: "AuthService unit tests in test_auth_service.py"     # T035
Task: "Session overhead benchmark in test_session_overhead.py" # T040
Task: "Data volume test in test_task_volume.py"            # T041
Task: "backend/CLAUDE.md update"                           # T038
Task: "frontend/CLAUDE.md update"                          # T039
```

---

## Phase 1: Setup

**Purpose**: Contract freeze artifact and environment setup before any code lands.

- [X] T001 Draft `specs/2-plan/phase-2/api-specs/auth-and-task-contracts.md` — Part 1: full endpoint matrix for `/api/auth/register`, `/api/auth/login`, `/api/auth/logout`, `/api/auth/me`, and all six task routes (`GET/POST /api/{user_id}/tasks`, `GET/PATCH/DELETE /api/{user_id}/tasks/{task_id}`); auth precedence rule (Bearer header checked first, httpOnly cookie second); document which routes are public vs protected
- [X] T002 Complete `specs/2-plan/phase-2/api-specs/auth-and-task-contracts.md` — Part 2: add error catalog mapping table (all 11 entries with HTTP status, code, and exact message); CORS allowlist setting (`CORS_ORIGIN` env var, `credentials: true`, no wildcard); contract-freeze checklist (endpoint matrix ✓, auth precedence ✓, error catalog ✓, CORS ✓ — mark all four before implementation begins)
- [X] T003 [P] Update `backend/.env.example` with `DATABASE_URL`, `SECRET_KEY`, `CORS_ORIGIN`, `COOKIE_DOMAIN`, `REDIS_URL`; update `frontend/.env.example` with any auth-specific vars; run `npm install better-auth` in `frontend/` and confirm entry added to `package.json`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Database models, migrations framework, CORS, and error infrastructure that ALL user stories depend on.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

**Parallel group** (T004–T007, T010 have no inter-dependencies — start all together):

- [X] T004 [P] Create async `User` SQLAlchemy model in `backend/src/models/user.py`: `id: Mapped[UUID]` (pk, default=uuid4), `email: Mapped[str]` (unique, not null, max 255), `hashed_password: Mapped[str]` (not null), `created_at: Mapped[datetime]` (server_default=now()); `tasks: Mapped[list["Task"]]` relationship with `cascade="all, delete-orphan"`, `back_populates="owner"`
- [X] T005 [P] Update `Task` SQLAlchemy model in `backend/src/models/task.py`: add `user_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("users.id"), nullable=True, index=True)`; add `owner: Mapped[Optional["User"]] = relationship(back_populates="tasks")`; no other changes to existing columns or route contracts
- [X] T006 [P] Configure async SQLAlchemy in `backend/src/database.py`: `create_async_engine(DATABASE_URL, pool_size=10, max_overflow=20, echo=False)`; `AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)`; `async def get_db() -> AsyncGenerator[AsyncSession, None]` dependency with `async with AsyncSessionLocal() as session: yield session`
- [X] T007 [P] Initialize Alembic: run `alembic init backend/alembic` from repo root; set `sqlalchemy.url` in `backend/alembic.ini` to `%(DATABASE_URL)s`; update `backend/alembic/env.py` to use `run_async_migrations` pattern with the async engine from `database.py` and import all models for autogenerate
- [X] T010 [P] Implement centralized error mapper in `backend/src/utils/error_mapper.py`: define `AppException(code: str, message: str, status_code: int)` base class; add all 11 subclasses (`EmailAlreadyExistsError`, `InvalidCredentialsError`, `ValidationError`, `SessionExpiredError`, `InvalidTokenError`, `TaskNotFoundError`, `UnauthorizedError`, `ForbiddenError`, `RateLimitedError`, `InternalError`, `ServiceUnavailableError`) with codes and exact catalog messages; implement `map_exception_to_response(exc: AppException) -> JSONResponse` returning `{"success": false, "data": null, "error": {"code": ..., "message": ...}}`

**Sequential after T010** (T011 imports `AppException` from T010 — cannot run in parallel):

- [X] T011 Configure CORS and global error handling in `backend/src/main.py` (depends on T010): add `CORSMiddleware(allow_origins=[settings.CORS_ORIGIN], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])` — no wildcard origin; register `@app.exception_handler(AppException)` wired to `map_exception_to_response`; no ad-hoc error strings in any route handler

**Sequential after parallel group** (T008 needs T004+T007; T009 needs T005+T008):

- [X] T008 Create Alembic migration `backend/alembic/versions/001_create_users_table.py`: `op.create_table("users", sa.Column("id", UUID, primary_key=True, default=uuid4), sa.Column("email", sa.String(255), nullable=False), sa.Column("hashed_password", sa.Text, nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()))`; `op.create_index("ix_users_email", "users", ["email"], unique=True)`; `downgrade()` drops index then table
- [X] T009 Create Alembic migration `backend/alembic/versions/002_add_user_id_to_tasks.py` (depends on 001 applied): `op.add_column("tasks", sa.Column("user_id", UUID, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=True))`; `op.create_index("ix_tasks_user_id", "tasks", ["user_id"])`; `downgrade()` drops index then column

**Checkpoint**: DB models, migrations framework, CORS, and error infrastructure all exist. User story implementation can begin.

---

## Phase 3: User Story 1 + User Story 3 — Registration, Login & Persistent Storage (Priority: P1) 🎯 MVP

**Goal**: New users can register; returning users can log in and log out. All credentials and user records are stored in PostgreSQL and survive restarts.

**Independent Test**: `POST /api/auth/register` → restart backend → `POST /api/auth/login` → `GET /api/auth/me` — all three succeed with 201/200 and correct wrapped response bodies.

**Note on US3**: User Story 3 (Persistent Data Storage) acceptance criteria are satisfied structurally by Phase 2 (PostgreSQL-backed schema) + this phase (user records written via SQLAlchemy). US3 acceptance tests verify persistence by restarting the app and re-querying.

### Implementation for User Story 1 + User Story 3

- [X] T012 [US1] Implement `AuthService` validation methods in `backend/src/services/auth_service.py`: `normalize_email(email: str) -> str` (`.lower().strip()`); `validate_email_format(email: str) -> None` (regex or `email-validator` lib; raises `ValidationError` on fail); `validate_password(password: str) -> None` (raises `ValidationError` if len < 8, no uppercase, no lowercase, or no digit — separate check per rule for exact catalog message)
- [X] T013 [US1] Add `AuthService` data methods to `backend/src/services/auth_service.py`: `hash_password(password: str) -> str` using `argon2.PasswordHasher(time_cost=3, memory_cost=65536, parallelism=2).hash(password)`; add docstring with benchmark result showing hash+verify ≤ 300ms on target hardware; `verify_password(hashed: str, password: str) -> bool` using `ph.verify()`; `async def create_user(db: AsyncSession, email: str, hashed_password: str) -> User`; `async def get_user_by_email(db: AsyncSession, email: str) -> User | None`
- [X] T014 [P] [US1] Implement JWT helper in `backend/src/utils/token.py`: `create_token(user_id: UUID, email: str) -> str` signs HS256 payload `{"sub": str(user_id), "email": email, "exp": now() + timedelta(seconds=86400)}` using `settings.SECRET_KEY`; `decode_token(token: str) -> dict` verifies signature and exp — raises `SessionExpiredError` on `jwt.ExpiredSignatureError`, raises `InvalidTokenError` on any other decode failure
- [X] T015 [US1] Implement `POST /api/auth/register` in `backend/src/routes/auth.py`: parse `RegisterRequest(email: str, password: str)` Pydantic model; call `normalize_email` + `validate_email_format` + `validate_password` (400 on any fail); call `get_user_by_email` (409 `EmailAlreadyExistsError` if present); call `hash_password`; persist via `create_user`; call `create_token`; set `Set-Cookie: access_token=<token>; HttpOnly; Secure; SameSite=Lax; Max-Age=86400; Path=/`; return 201 `{"success": true, "data": {"access_token": "<token>", "token_type": "bearer"}, "error": null}`
- [X] T016 [US1] Implement `POST /api/auth/login` in `backend/src/routes/auth.py`: parse `LoginRequest(email: str, password: str)`; normalize email; call `get_user_by_email` (raise `InvalidCredentialsError` if absent — do not distinguish missing vs wrong credentials); call `verify_password` (raise `InvalidCredentialsError` on fail); call `create_token`; set same cookie as register; return 200 `{"success": true, "data": {"access_token": "<token>", "token_type": "bearer"}, "error": null}`
- [X] T017 [US1] Implement `POST /api/auth/logout` in `backend/src/routes/auth.py`: clear cookie via `Set-Cookie: access_token=; HttpOnly; Secure; SameSite=Lax; Max-Age=0; Path=/`; always return 200 `{"success": true, "data": {"logged_out": true}, "error": null}` regardless of whether a valid cookie was present
- [X] T018 [US1] Implement `GET /api/auth/me` in `backend/src/routes/auth.py`: extract token from `Authorization: Bearer <token>` header first, then `access_token` cookie; call `decode_token` (raises `SessionExpiredError` or `InvalidTokenError` on failure → 401 via global handler); fetch user from DB by `sub` claim; return 200 `{"success": true, "data": {"id": "<uuid>", "email": "<str>"}, "error": null}`

**Checkpoint**: All four auth endpoints functional with PostgreSQL. Register + restart + login succeeds (US3 verified).

---

## Phase 4: User Story 5 + User Story 2 — Unauthenticated Protection & Task Ownership (Priority: P2/P1)

**Goal**: Every task endpoint rejects unauthenticated requests (401). Authenticated users see only their own tasks. `{user_id}` path mismatch returns 403 with no DB query; unowned `{task_id}` returns 404.

**Independent Test**: Create User A and User B. With User A cookie: `GET /api/{user_b_id}/tasks` → 403. `GET /api/{user_a_id}/tasks/{user_b_task_id}` → 404. Without cookie: any task endpoint → 401.

### Implementation for User Story 5 + User Story 2

- [X] T019 [US5] Implement `require_authenticated_user` FastAPI dependency in `backend/src/middleware/auth.py`: (1) check `Authorization` header — if present, strip `Bearer ` prefix and call `decode_token`; (2) else check `access_token` httpOnly cookie and call `decode_token`; (3) if neither present, raise `UnauthorizedError`; on `SessionExpiredError` re-raise; on `InvalidTokenError` re-raise; fetch `User` from DB via `sub` claim; return `User` object as `current_user`
- [X] T020 [US5] Apply `current_user: User = Depends(require_authenticated_user)` to all six task route handlers in `backend/src/routes/tasks.py`: `list_tasks`, `create_task`, `get_task`, `update_task`, `delete_task`, and any additional task routes; unauthenticated requests now receive 401 via global exception handler
- [X] T021 [US2] Add `enforce_user_id_match` guard to each task route handler in `backend/src/routes/tasks.py` immediately after `current_user` is resolved: `if str(user_id) != str(current_user.id): raise ForbiddenError()` — no DB query at this layer; guard fires before any `TaskService` call
- [X] T022 [P] [US2] Update `TaskService.create_task` in `backend/src/services/task_service.py`: add `user_id: UUID` as required parameter; set `task.user_id = user_id` before `db.add(task)`; update call site in the route handler to pass `current_user.id`
- [X] T023 [P] [US2] Update `TaskService.get_tasks`, `get_task`, `update_task`, `delete_task` in `backend/src/services/task_service.py`: add `user_id: UUID` parameter to each; append `.where(Task.user_id == user_id)` to all ORM queries; raise `TaskNotFoundError` (404) when row absent under that user's scope — never raise 403 at the service layer

**Checkpoint**: Two-layer authorization active. Unauthenticated → 401. Path mismatch → 403 (no DB query). Unowned task → 404.

---

## Phase 5: User Story 4 — Secure Session Management (Priority: P2)

**Goal**: Sessions expire 24 hours after login with no activity extension. Frontend detects expiry on next request and redirects to `/login?reason=session_expired`. Explicit logout ends the session immediately.

**Independent Test**: Log in; manually forge a JWT with `exp = now() - 1 second` (signed with `SECRET_KEY`); send it as Bearer header to `GET /api/auth/me` → 401 SESSION_EXPIRED; frontend redirects to `/login?reason=session_expired` and banner renders.

### Implementation for User Story 4

- [X] T024 [US4] Update `frontend/src/middleware.ts` (F05 fix — Next.js Edge middleware runs server-side; `credentials: 'include'` does NOT auto-forward client cookies in a server fetch; must extract and forward explicitly): on requests to `/dashboard`, extract `access_token` cookie value via `request.cookies.get("access_token")`; call `fetch(process.env.NEXT_PUBLIC_API_URL + "/api/auth/me", { headers: { Cookie: "access_token=" + cookieValue }, cache: "no-store" })`; on 401 response (or if cookie is absent) redirect to `/login?reason=session_expired`; on 200 response allow through; redirect authenticated users (200) away from `/login` and `/register` to `/dashboard`; pass all other routes through unchanged
- [X] T025 [US4] In `frontend/src/app/(auth)/login/page.tsx`: add conditional banner that renders the spec-exact message `"Your session has expired. Please log in again."` when `searchParams.reason === "session_expired"` is present (WCAG: `role="alert"`, `aria-live="polite"`); verify `frontend/src/lib/api-client.ts` 401 handler calls `router.push("/login?reason=session_expired")` and `queryClient.clear()` — add if missing from feature-02 implementation

**Checkpoint**: Expired sessions detected on next request; banner rendered with exact catalog message. Explicit logout clears cookie (verified in Phase 3).

---

## Phase 6: User Story 6 — Data Migration from Pre-Auth System (Priority: P1)

**Goal**: Any tasks without a `user_id` are hard-deleted. `user_id` becomes NOT NULL in schema. Migration runbook and schema docs are written. `alembic upgrade head` runs automatically on deploy (FR-018).

**Independent Test**: Insert `INSERT INTO tasks (..., user_id) VALUES (..., NULL)` directly. Run migrations 003+004. Verify the null row is gone. Verify `INSERT INTO tasks (..., user_id) VALUES (..., NULL)` now raises a NOT NULL constraint violation.

### Implementation for User Story 6

- [X] T026 [US6] Create two Alembic migrations in `backend/alembic/versions/`: (1) `003_delete_orphan_tasks.py` — `op.execute("DELETE FROM tasks WHERE user_id IS NULL")`; add comment `# IRREVERSIBLE: orphaned task deletion cannot be rolled back — see auth-migration-plan.md`; `downgrade()` raises `NotImplementedError("Orphan task deletion is intentionally irreversible. Schema rollback only — see auth-migration-plan.md")`; (2) `004_enforce_tasks_user_id_not_null.py` — `op.alter_column("tasks", "user_id", nullable=False)`; `downgrade()` runs `op.alter_column("tasks", "user_id", nullable=True)`
- [X] T027 [US6] Add `alembic upgrade head` to backend deployment entrypoint: if using Docker, update `backend/Dockerfile` CMD or `docker-compose.yml` backend service command to run migrations before starting the server (e.g. `sh -c "alembic upgrade head && uvicorn ..."`); verify the entrypoint command runs migrations idempotently on a clean DB and on a DB already at head — satisfies FR-018
- [X] T028 [P] [US6] Create `specs/2-plan/phase-2/db-schema/auth-storage-schema.md` documenting final `users` table (cols, types, constraints, indexes) and final `tasks` table (all cols including `user_id` FK, indexes on `user_id` + `email` + `completed`); AND create `specs/2-plan/phase-2/db-schema/auth-migration-plan.md` documenting migration sequence (001→004), per-migration reversibility, rollback playbook (`alembic downgrade -1` for 004 and 002; 003 irreversible — document explicitly), and `docker compose run backend alembic upgrade head` run instructions

**Checkpoint**: Zero tasks with null `user_id`. Schema enforces NOT NULL. Migrations run automatically on deploy. Runbook written.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Rate limiting, error catalog exactness verified via tests, test coverage, load test, accessibility, and CLAUDE.md updates.

- [X] T029 Define `RateLimitAdapter` protocol and `InMemoryAdapter` in `backend/src/middleware/rate_limit.py`: `class RateLimitAdapter(Protocol)` with `async def increment(self, key: str, limit: int, window_seconds: int) -> bool` (returns `True` if request allowed, `False` if limit exceeded); `InMemoryAdapter` using `dict[str, (count, reset_at)]` — thread-safe for single-process dev/test use; used when `REDIS_URL` is absent
- [X] T030 Implement `RedisAdapter` in `backend/src/middleware/rate_limit.py`: uses `redis.asyncio`; `increment` calls `INCR key` then `EXPIRE key window_seconds` (only on first increment, i.e., when `INCR` returns 1); key scheme: authenticated `rate:user:{user_id}:{epoch_hour}`, unauthenticated `rate:ip:{ip}:{epoch_hour}`; limits: 1000/hr authenticated, 100/hr unauthenticated; instantiate from `REDIS_URL` env var; fall back to `InMemoryAdapter` if URL absent
- [X] T031 Classify routes and wire rate-limit middleware in `backend/src/main.py` (F02 fix — middleware runs before Depends(), so current_user is never in request.state at middleware time): define `UNAUTHENTICATED_PATHS = {"/api/auth/login", "/api/auth/register"}`; `RateLimitMiddleware.dispatch()` extracts the JWT token directly — check `Authorization: Bearer <token>` header first, then `access_token` cookie; call `decode_token(token)` to get `sub` (user_id) for the rate-limit key; on any decode failure fall back to IP-based key (treat as unauthenticated); key scheme: authenticated `rate:user:{user_id}:{epoch_hour}` (limit 1000), unauthenticated `rate:ip:{ip}:{epoch_hour}` (limit 100); raises `RateLimitedError` (429) if `adapter.increment` returns `False`; register middleware after CORS middleware in main.py
- [X] T032 [US1] Write register test scenarios in `backend/tests/test_routes/test_auth.py`: register success (201, cookie set, body `{success: true, data: {access_token, token_type}}`); duplicate email (409 EMAIL_ALREADY_EXISTS + exact message); invalid email format (400 VALIDATION_ERROR + exact message); password < 8 chars (400 VALIDATION_ERROR); password missing uppercase (400 VALIDATION_ERROR); email normalized to lowercase before storage
- [X] T033 Write login/logout/me test scenarios extending `backend/tests/test_routes/test_auth.py`: login success (200, cookie set); wrong credentials (401 INVALID_CREDENTIALS + exact message); email case-insensitive login (`User@Test.com` same as `user@test.com`); logout always 200 (with valid cookie, with invalid cookie, with no cookie); me with valid cookie (200, `{id, email}`); me with expired token (401 SESSION_EXPIRED + exact message); me with tampered token (401 INVALID_TOKEN + exact message); — these scenarios also verify error catalog exactness, replacing removed T027
- [X] T034 [P] Write task authorization integration tests in `backend/tests/test_routes/test_tasks_auth.py`: unauthenticated `GET/POST/PATCH/DELETE` any task route → 401 UNAUTHORIZED; User A token + User B `{user_id}` path → 403 FORBIDDEN; User A token + User A `{user_id}` path + task owned by User B → 404 TASK_NOT_FOUND; User A creates task → User B lists `GET /api/{user_b_id}/tasks` and task does not appear (cross-user isolation)
- [X] T035 [P] Write `AuthService` unit tests in `backend/tests/test_services/test_auth_service.py`: `normalize_email` lowercases and strips whitespace; invalid email format raises `ValidationError`; password < 8 chars raises `ValidationError`; password missing uppercase raises `ValidationError`; password missing digit raises `ValidationError`; `hash_password` output is Argon2 encoded string (not plaintext); `verify_password` returns `True` on match and `False` on mismatch
- [X] T036 Write Locust load test in `backend/tests/load/locustfile.py`: define `AuthUser(HttpUser)` task set with `register` (unique email per user via `f"user_{self.user_id}@test.com"`), `login`, `me`; write `backend/tests/load/README.md` with exact run command: `locust -f tests/load/locustfile.py --users 100 --spawn-rate 10 --run-time 60s --host http://localhost:8000`; note target environment is `docker compose up` (backend + postgres); acceptance criterion is p95 ≤ 300ms
- [X] T040 [P] Write session-validation overhead benchmark in `backend/tests/test_performance/test_session_overhead.py` (covers PERF-002): use `pytest-benchmark` or `time.perf_counter` to call `decode_token(valid_token)` followed by `get_user_by_email(db, email)` in a loop of 100 iterations; assert mean round-trip ≤ 50ms; this measures the incremental cost added by `require_authenticated_user` on every protected request — satisfies PERF-002 ("session validation MUST add no more than 50ms overhead")
- [X] T041 [P] Write data-volume integration test in `backend/tests/test_performance/test_task_volume.py` (covers PERF-005): seed 10,000 task rows for a single user via direct `AsyncSession` bulk insert (not via API); call `GET /api/{user_id}/tasks` (list all) and `GET /api/{user_id}/tasks/{first_id}` and `GET /api/{user_id}/tasks/{last_id}` with the user's auth cookie; assert each response arrives within 300ms; verifies PERF-005 ("persistent storage MUST support at least 10,000 tasks per user without performance degradation")
- [X] T037 [P] Run Playwright + axe-core accessibility audit on `/login` and `/register` pages following pattern in `frontend/tests/e2e/`; fix any critical or serious violations (WCAG 2.1 AA: labels, keyboard nav, contrast, screen-reader announcements); record zero-violation result in test output
- [X] T038 [P] Update `backend/CLAUDE.md`: add auth section covering Argon2id params (time_cost=3, memory_cost=65536, parallelism=2), JWT format (HS256, `exp=now+86400`, `sub=user_id`), cookie settings (HttpOnly/Secure/SameSite=Lax/Max-Age=86400), `require_authenticated_user` Depends() usage, `enforce_user_id_match` guard pattern, error mapper rule (never ad-hoc messages), ORM-only DB access, task traceability comment format (`# Task: T0XX — description`)
- [X] T039 [P] Update `frontend/CLAUDE.md`: add auth section covering `better-auth` package role, `credentials: "include"` required on all fetch calls, session expiry handling (401 → `router.push("/login?reason=session_expired")` + `queryClient.clear()`), middleware session check pattern (`/api/auth/me` server-side), task traceability comment format

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately; T001→T002 sequential (same doc); T003 parallel
- **Foundational (Phase 2)**: Requires Phase 1 — **BLOCKS all user story phases**
  - T004, T005, T006, T007, T010 in parallel
  - T011 after T010 (imports AppException — F01 fix)
  - T008 after T004 + T007
  - T009 after T005 + T008
- **US1+US3 (Phase 3)**: Requires Phase 2 complete
  - T012 → T013 sequential (same file, same class)
  - T014 parallel to T012/T013 (different file)
  - T015 → T016 → T017 → T018 sequential (same routes file)
- **US5+US2 (Phase 4)**: Requires Phase 3 complete (tokens must exist before enforcement)
  - T019 → T020 → T021 sequential
  - T022 + T023 parallel after T019
- **US4 (Phase 5)**: Requires Phase 4 complete
  - T024 → T025 sequential (same page/file)
- **US6 (Phase 6)**: Requires Phase 2 (alembic) + Phase 4 (ownership model locked)
  - T026 → T027 sequential; T028 parallel
- **Polish (Phase 7)**: Requires Phases 3–6 complete
  - T029 → T030 → T031 sequential (same middleware file, build on each other)
  - T032 → T033 sequential (same test file, extending it)
  - T034, T035, T036, T037, T038, T039, T040, T041 parallel

### Task Sizing Reference

| Phase | Tasks | Avg Size |
|-------|-------|----------|
| Phase 1 Setup | T001–T003 | 25 / 20 / 15 min |
| Phase 2 Foundational | T004–T011 | 20–25 min each |
| Phase 3 US1+US3 | T012–T018 | 20–30 min each |
| Phase 4 US5+US2 | T019–T023 | 20–25 min each |
| Phase 5 US4 | T024–T025 | 25 / 20 min |
| Phase 6 US6 | T026–T028 | 25 / 15 / 25 min |
| Phase 7 Polish | T029–T041 | 20–30 min each |

---

## Implementation Strategy

### MVP First (US1 + US3)

1. Complete Phase 1: Setup (T001–T003)
2. Complete Phase 2: Foundational (T004–T011)
3. Complete Phase 3: US1+US3 (T012–T018)
4. **STOP and VALIDATE**: `POST /api/auth/register` → restart backend → `POST /api/auth/login` → `GET /api/auth/me` all succeed
5. Deploy/demo if ready

### Incremental Delivery

1. Setup + Foundational → DB + CORS + error infrastructure ready
2. US1+US3 → Working auth endpoints with persistence → **MVP**
3. US2+US5 → Task ownership enforced → Two-user isolation verified
4. US4 → Session expiry UX wired → Full session lifecycle working
5. US6 → Migration executed + deploy hook active → DB schema hardened
6. Polish → Rate limits, full coverage, load test, a11y → Release ready

---

## Notes

- Every code file created in this feature MUST include a header comment: `# Task: T0XX — <one-line description>` per constitution traceability requirement
- [P] tasks operate on different files with no incomplete dependencies — safe to parallelize
- [US1]–[US6] labels map to user stories in `specs/1-specify/phase-2/feature-03-auth-db-monorepo.md`
- `better-auth` (frontend) and `PyJWT` (backend) share `SECRET_KEY` as the HS256 compatibility contract — see ADR @history/adr/0011-auth-session-transport-and-contract.md
- Migration 003 orphan deletion (T026) is intentionally irreversible — document before executing against any environment with real data
- Locust target environment (T036) is `docker compose up` (backend + postgres); never run load test against production
- T027 ("verify error catalog" from v1) was removed — error catalog exactness is now verified via test assertions in T033
- **v3 remediation (F01–F05)**: T011 [P] tag removed — it depends on T010 and must run after it; T031 rewritten so rate-limit middleware extracts JWT directly instead of reading from `request.state` (which Depends() never populates); T024 rewritten to explicitly forward the `access_token` cookie header in the server-side fetch call to `/api/auth/me`; T040 added for PERF-002 (session overhead benchmark); T041 added for PERF-005 (10,000 tasks/user volume test)
