# Implementation Plan: Phase 2 Part 3 - Authentication & Persistent Storage

**Branch**: `007-auth-db-monorepo` | **Date**: 2026-02-15 | **Spec**: @specs/1-specify/phase-2/feature-03-auth-db-monorepo.md
**Input**: Feature specification for secure multi-user isolation and persistent storage.

## Summary

Implement Phase 2 Part 3 by extending the existing FastAPI backend and Next.js frontend with secure authentication, strict user-level task isolation, session management, and durable PostgreSQL persistence. The approach preserves existing task contracts from feature-01 while introducing auth and migration capabilities required by the current specification.

## Technical Approach for Structuring Project

### Monorepo Structure Decision

Use the existing mandatory monorepo layout and keep all Phase II implementation in `backend/` and `frontend/`, with architecture docs in `specs/2-plan/phase-2/`.

```text
specs/2-plan/phase-2/
├── phase-2-fastapi-todo-backend.md
├── phase-2-auth-db-monorepo.md        # This file
├── api-specs/
│   └── auth-and-task-contracts.md      # To be created during implementation
├── db-schema/
│   ├── auth-storage-schema.md          # To be created during implementation
│   └── auth-migration-plan.md          # To be created during implementation
└── ui-design/
    └── auth-flows.md                   # To be created during implementation
```

```text
backend/
├── src/
│   ├── models/                         # User, Task, auth/session-related model details
│   ├── routes/                         # /api/auth/* and protected /api/{user_id}/tasks/*
│   ├── services/                       # AuthService, UserService, TaskService
│   ├── middleware/                     # Auth/session extraction and request context
│   ├── utils/                          # Password hashing, token/cookie helpers, error mapping
│   └── database.py                     # Session factory + DB connectivity
├── alembic/
│   └── versions/                       # Schema and data migration scripts
└── tests/
    ├── test_routes/                    # Auth and task authorization tests
    ├── test_services/                  # Auth/domain service tests
    └── test_integration/               # Session, ownership, migration behavior

frontend/
├── src/
│   ├── app/                            # Login/register/protected route flow
│   ├── components/                     # Auth forms + protected task UX
│   └── lib/                            # API client using credentials: 'include'
└── tests/                              # Frontend auth/session behavior tests
```

### Architectural Style

- Keep layered architecture: route handlers -> services -> ORM/data layer.
- Keep stateless backend APIs: authentication state is represented by signed tokens and httpOnly cookie, not in-memory sessions.
- Keep authentication compatible with Phase II requirement of Better Auth + JWT contracts while preserving existing API endpoint contracts.
- Preserve response envelope contract (`success`, `data`, `error`) across auth and task endpoints.
- Keep backward-compatible task endpoint paths while enforcing stricter authorization semantics.

## Major Components and Phases

### Major Components

1. **Identity and Authentication Component**
- Registration, login, logout, and `/api/auth/me`.
- Email normalization, password policy validation, password hashing.
- Token issuance and verification (cookie + optional bearer token response for non-browser clients).

2. **Authorization and Isolation Component**
- Request authentication guard for protected endpoints.
- Two-layer authorization model:
  - `403` when `{user_id}` path does not match authenticated user.
  - `404` when user matches but requested task is not owned by that user.

3. **Persistence and Migration Component**
- Durable PostgreSQL persistence for users and tasks.
- Schema migration flow for new auth requirements.
- Cleanup migration for orphaned pre-auth tasks.

4. **Rate Limiting and Security Hardening Component**
- Per-user limits for authenticated requests.
- IP-based limits for unauthenticated auth/public endpoints.
- Centralized sanitization, validation, and safe error output.

5. **Frontend Auth Integration Component**
- Login/register UI and protected route behavior.
- Cookie-based session usage (`credentials: 'include'`).
- Session expiry handling and redirect behavior.

### Implementation Phases

1. **Phase A - Foundation Alignment**
- Confirm existing backend/frontend structure and shared response contract.
- Add/align config for auth secrets, cookie settings, and DB connectivity.
- Freeze API/auth contracts (cookie + optional bearer token response behavior) before coding.

2. **Phase B - Auth Core**
- Implement register/login/logout/me endpoints.
- Add password hashing, email normalization, and token/cookie lifecycle.
- Create and validate baseline schema migration (users/tasks tables, foreign keys, required indexes).
- Install `better-auth` npm package in the Next.js frontend; backend uses `PyJWT` (HS256). Shared `SECRET_KEY` env var is the compatibility contract.

3. **Phase C - Authorization Enforcement on Tasks**
- Apply authentication to task routes.
- Enforce 403/404 two-layer ownership behavior.

4. **Phase D - Persistence and Migration**
- Execute data migration logic to drop orphaned legacy tasks.
- Validate rollback procedure and migration safety checks.

5. **Phase E - Rate Limits, Errors, and Test Coverage**
- Implement authenticated and unauthenticated rate-limit policies.
- Enforce exact error catalog mappings.
- Complete unit/integration tests for auth/session/isolation flows.
- Write Locust load test script targeting `/api/auth/login`, `/api/auth/register`, and `/api/auth/me`; run against docker-compose stack (backend + postgres); capture p95 latency and validate ≤300ms at 100 concurrent users (SC-008, PERF-001, PERF-003).

### Phase Exit Criteria

1. **Phase A exit**: Contract notes approved for `/api/auth/*`, task-route auth behavior, and response envelope shape.
2. **Phase B exit**: Registration/login/logout/me endpoints implemented with cookie behavior and password/email policy tests passing; baseline schema migration (users/tasks/fkeys/indexes) created and validated.
3. **Phase C exit**: Protected task endpoints enforce two-layer authorization (403 path mismatch, 404 ownership miss) with integration tests.
4. **Phase D exit**: Orphaned-task cleanup migration applied successfully; no orphaned tasks remain; rollback procedure documented and tested.
5. **Phase E exit**: Rate-limit policies active; exact error catalog mappings verified; Phase II quality targets validated (>=60% coverage, <=300ms p95 auth latency target, 100 concurrent users).

### Phase Deliverables

1. **Phase A deliverables**
- `specs/2-plan/phase-2/api-specs/auth-and-task-contracts.md` draft with route/error/auth contract freeze notes.
- External dependency gate checklist (Feature-01/Feature-02 completion, DB availability, auth secret readiness).
- Feature-03 task-traceability preparation notes confirming planned updates under `specs/3-tasks/phase-2/` before implementation.
- Contract-freeze acceptance checklist completed (required fields: endpoint matrix, auth precedence rules, error catalog mapping table, CORS/credentials settings, explicit FE+BE approvers and approval timestamp).

2. **Phase B deliverables**
- Auth endpoint implementation notes and test evidence.
- Baseline schema migration scripts (table creation, constraints, indexes) and apply/rollback validation notes.
- `.env.example` updates for database/auth configuration.
- Password-hashing benchmark note proving chosen configuration is within auth endpoint performance budget.

3. **Phase C deliverables**
- Authorization guard and ownership enforcement notes with SEC-003/SEC-004 verification evidence.
- Protected task route conformance checklist.

4. **Phase D deliverables**
- Data-cleanup migration for pre-auth orphaned tasks plus rollback playbook.
- `specs/2-plan/phase-2/db-schema/auth-migration-plan.md` and `specs/2-plan/phase-2/db-schema/auth-storage-schema.md` synchronized to executed migration behavior.

5. **Phase E deliverables**
- Rate-limit policy implementation and verification report (per-user/per-IP).
- Error catalog conformance results (exact message checks).
- Coverage report and acceptance/integration test summary.
- Locust load test script (`tests/load/locustfile.py`) and results report confirming p95 ≤300ms under 100 concurrent users against the docker-compose stack. Tool: Locust; environment: `docker compose up` (backend + postgres).
- `backend/CLAUDE.md` and `frontend/CLAUDE.md` updates with auth/storage patterns and traceability expectations.

## Dependencies Between Components

### Dependency Graph

Legend: `A -> B` means `A depends on B`.

- Frontend Auth Integration -> Identity and Authentication Component
- Identity and Authentication Component -> Persistence and Migration Component
- Authorization and Isolation Component -> Identity and Authentication Component
- Authorization and Isolation Component -> Persistence and Migration Component
- Rate Limiting and Security Hardening Component -> Identity and Authentication Component
- Rate Limiting and Security Hardening Component -> Authorization and Isolation Component

### Sequencing Dependencies

1. Auth token/cookie primitives must be implemented before protected route enforcement.
2. Baseline schema migrations (users/tasks/fkeys/indexes) must exist before registration/login is production-ready.
3. Ownership checks require both authenticated identity extraction and task-owner persistence.
4. Error catalog standardization must be centralized before full API parity testing.
5. Rate-limiting policy should be finalized after endpoint classification (public vs protected).
6. Orphaned-task data cleanup migration must run after baseline schema migration and before migration signoff.

### Parallel Work Opportunities

1. **Track P1 (parallel after Phase A contract freeze)**: Frontend auth pages/route guards can proceed in parallel with backend auth service internals.
2. **Track P2 (parallel in Phase B/C)**: Backend endpoint handlers and backend authorization middleware can be implemented in parallel once token/cookie helper interfaces are fixed.
3. **Track P3 (parallel in Phase D)**: Migration script authoring and migration test fixture setup can run in parallel.
4. **Track P4 (parallel in Phase E)**: Error mapping tests, rate-limit tests, and frontend session-expiry UX tests can run in parallel.

Guardrails:
- Do not start P1/P2 before contract freeze in Phase A.
- Do not start P4 before final error catalog and endpoint classification are locked.

### External Dependency Gates

1. **Gate G1 - Feature Baseline Ready**: Feature-01 and Feature-02 contracts are complete and unchanged for task endpoint paths/response envelope.
2. **Gate G2 - Runtime Prereqs Ready**: PostgreSQL instance reachable and environment auth secret provisioned.
3. **Gate G3 - Cross-Origin Auth Ready**: Frontend origin allowlist and `credentials: true` CORS configuration agreed before auth E2E testing.
4. **Gate G4 - Task Traceability Ready**: Feature-03 task IDs are defined in `specs/3-tasks/phase-2/` before implementation code lands.
5. **Gate G5 - Constitutional Engineering Guardrails Ready**: Implementation approach confirms ORM-based DB access (no direct SQL), stateless auth/session handling, and secret management via environment variables (no committed credentials).

### Critical Path

Contract freeze -> baseline schema migration -> auth endpoints -> task authorization enforcement -> orphaned-task cleanup migration -> rate limits/error exactness -> final coverage and acceptance signoff.

## Resolved Architecture Decisions

1. **Session Transport Strategy**
- Decision: dual transport (httpOnly cookie for browser + bearer token for non-browser), with bearer-header precedence when both are present.
- Constraint: backend remains stateless; no in-memory server sessions.
- ADR: @history/adr/0011-auth-session-transport-and-contract.md

2. **Token Lifetime Model**
- Decision: absolute 24-hour expiration from login time.
- Constraint: no refresh-token flow in this feature iteration.
- ADR: @history/adr/0011-auth-session-transport-and-contract.md

3. **Authorization Error Semantics**
- Decision: 401 unauthenticated, 403 for `{user_id}` path mismatch (checked first, before DB lookup), 404 for task ownership miss after user match.
- ADR: @history/adr/0013-two-layer-authorization-semantics.md

4. **Password Hashing Algorithm and Parameters**
- Decision: Argon2id with fixed initial configuration (`time_cost=3`, `memory_cost=65536`, `parallelism=2`), stored as encoded hash string.
- Constraint: parameters may be tuned upward later, but never downward below this baseline without a new ADR.
- Verification: Phase B benchmark must show hashing config fits Phase II latency target envelope.
- ADR: @history/adr/0011-auth-session-transport-and-contract.md

5. **Rate Limiting Backend and Keys**
- Decision: Redis-backed counters for runtime environments; deterministic in-memory adapter only for local tests/dev where Redis is unavailable.
- Keys: authenticated `rate:user:{user_id}:{hour_window}`, unauthenticated `rate:ip:{ip}:{hour_window}`.
- Policies: 1000 requests/hour per authenticated user and 100 requests/hour per unauthenticated IP.
- ADR: @history/adr/0012-rate-limiting-and-error-contract-enforcement.md

6. **Migration Handling for Legacy Orphaned Tasks**
- Decision: hard delete ownerless legacy tasks in cleanup migration; do not remap to synthetic/system user.
- Rollback policy: schema rollback supported; orphaned-task deletion is intentionally irreversible and must be documented in migration runbook before execution.
- ADR: @history/adr/0014-schema-first-migration-with-orphan-cleanup.md

7. **Error Catalog Enforcement Strategy**
- Decision: centralized error mapper (single module + shared exception types), with per-route handlers forbidden from ad hoc user-facing message text.
- Constraint: all error outputs must use wrapped envelope and exact catalog messages.
- ADR: @history/adr/0012-rate-limiting-and-error-contract-enforcement.md

8. **Better Auth Integration Boundary**
- Decision: `better-auth` npm package is installed in the Next.js frontend as the client-side auth utility. The FastAPI backend uses PyJWT (HS256) for JWT token generation and verification — Better Auth has no Python equivalent. The shared `SECRET_KEY` environment variable (HS256) is the compatibility contract between the two layers.
- Constraint: `/api/auth/*` and task endpoint contracts from feature specs remain authoritative. Custom route/service layer owns cookie transport behavior, response envelope shape, and authorization semantics.
- Implementation note: Phase B installs `better-auth` in the frontend; backend uses `PyJWT` directly. No Better Auth package exists for Python.
- ADR: @history/adr/0011-auth-session-transport-and-contract.md

## Constitution Check

- SDD loop respected: this plan is derived from @specs/1-specify/phase-2/feature-03-auth-db-monorepo.md.
- Mandatory monorepo structure respected: outputs are under `specs/2-plan/phase-2/` and implementation remains in `backend/` and `frontend/`.
- Security constraints reflected: authentication, user isolation, validation, and no plain-text credential storage.
- Persistence constraints reflected: PostgreSQL-backed storage with migration-first rollout.
- Constitutional forbidden-practice guardrails included: no direct SQL (ORM path), no stateful in-memory sessions, and no secrets committed to Git.

## Traceability

- Spec: @specs/1-specify/phase-2/feature-03-auth-db-monorepo.md
- Specification checklist: @specs/1-specify/phase-2/checklists/requirements-auth-db.md
- Related baseline spec: @specs/1-specify/phase-2/feature-01-fastapi-todo-backend.md
- Existing plan baseline: @specs/2-plan/phase-2/phase-2-fastapi-todo-backend.md
- Tasks to follow: @specs/3-tasks/phase-2/ (create auth/storage-specific task file in next step)

## Requirement-to-Phase Mapping

| Requirement Group | Planned Phase |
|-------------------|---------------|
| FR-001, FR-002, FR-003, FR-004, FR-009, FR-010, FR-012, FR-013, FR-016, FR-020 | Phase B |
| FR-005, FR-006, FR-007, FR-011 | Phase C |
| FR-008, FR-014, FR-018 | Phase B |
| FR-019 | Phase D |
| FR-015, FR-017 | Phase E |
| SEC-003/SEC-004 ordering and two-layer checks | Phase C |
| Error Message Catalog exactness | Phase E |

## Non-FR Requirement Trace Matrix

| Requirement Group | Planned Phase | Verification Signal |
|-------------------|---------------|---------------------|
| SEC-001, SEC-002, SEC-005, SEC-006, SESS-001, SESS-002 | Phase B | Auth integration tests for cookie/session/token validation and input/password policies |
| SEC-003, SEC-004 | Phase C | Authorization integration tests proving 403 path mismatch then 404 ownership miss behavior |
| SEC-007 | Phase E | Rate-limit tests for 1000/hr authenticated user and 100/hr unauthenticated IP |
| SEC-008 | Phase A | CORS + credentials contract checklist approved before end-to-end auth tests |
| ACC-001, ACC-002, ACC-003, ACC-004, ACC-005 | Phase E | Auth page accessibility audit results (keyboard, labels, contrast, screen-reader errors) |
| PERF-001, PERF-002 | Phase E | Auth/session latency benchmark report under expected load |
| PERF-003 | Phase E | Concurrency/load test evidence for 100 authenticated users |
| PERF-004 | Phase B + D | Indexes created in baseline schema migration and validated post-cleanup migration |
| PERF-005 | Phase E | Data volume test evidence for 10,000 tasks/user target |
| TEST-001, TEST-002, TEST-003 | Phase E | Coverage report and acceptance test mapping across all 6 user stories |
| SC-001, SC-002, SC-003, SC-004, SC-005, SC-006, SC-007, SC-008, SC-009, SC-010, SC-011 | Phase E | Final success-criteria checklist with pass/fail evidence references |
