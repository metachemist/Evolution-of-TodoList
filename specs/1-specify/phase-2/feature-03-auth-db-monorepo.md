# Feature Specification: Authentication & Persistent Storage

**Feature Branch**: `007-auth-db-monorepo`
**Created**: 2026-02-15
**Revised**: 2026-02-15 (v2 — post-review improvements)
**Status**: Draft
**Input**: User description: "Phase 2 Part 3 — Provide secure multi-user isolation and persistent storage for the todo application."

## Constitutional Compliance

This specification adheres to the Todo Evolution Constitution by:
- Following the SDD Loop (Specify → Plan → Tasks → Implement)
- Supporting the mandatory monorepo structure (specs under `specs/1-specify/phase-2/`)
- Ensuring traceability to task IDs in `specs/3-tasks/`
- Aligning with Phase II technology stack requirements
- Maintaining security and privacy standards (user isolation, token validation, password hashing)
- Respecting Phase II performance and scalability targets

Canonical interpretation notes for this feature (to resolve constitutional/sibling ambiguity before implementation):
- Session lifetime for this feature is **absolute 24 hours** from login time.
- Authorization status behavior is **two-layer**: 403 for `{user_id}` mismatch, 404 for task-level ownership miss after `{user_id}` check passes.
- This feature uses the phase quality target of **100 concurrent users** and **60% coverage**.
- This feature's error message catalog is canonical for auth/database behavior in Phase II Part 3.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - User Registration and Login (Priority: P1)

A new visitor arrives at the application and needs to create an account before they can use it. They provide their email and password, receive confirmation that their account was created, and are logged in. Returning users can log in with their existing credentials to access their previously saved data.

**Why this priority**: Without authentication, there is no way to identify users or isolate their data. This is the foundational capability that every other feature depends on.

**Independent Test**: Can be fully tested by registering a new account, logging out, and logging back in. Delivers the ability to establish user identity.

**Acceptance Scenarios**:

1. **Given** a visitor is on the application, **When** they provide a valid email and password to register, **Then** their account is created and they are logged in automatically
2. **Given** a registered user is logged out, **When** they enter their correct email and password, **Then** they are authenticated and can access their data
3. **Given** a visitor attempts to register, **When** they provide an email that is already in use, **Then** they see the message: "An account with this email already exists. Please log in instead."
4. **Given** a user attempts to log in, **When** they provide incorrect credentials, **Then** they see the message: "Invalid email or password. Please try again."
5. **Given** a logged-in user, **When** they choose to log out, **Then** their session is ended and they can no longer access protected resources

---

### User Story 2 - Task Ownership and Data Isolation (Priority: P1)

An authenticated user creates, views, updates, and deletes tasks. Each task belongs exclusively to the user who created it. No user can see, modify, or delete another user's tasks under any circumstances.

**Why this priority**: Data isolation is equally critical to authentication — together they form the security foundation. A multi-user system without data isolation is a data breach waiting to happen.

**Independent Test**: Can be tested by creating two user accounts, adding tasks to each, and verifying that neither user can see or modify the other's tasks.

**Acceptance Scenarios**:

1. **Given** a user is authenticated, **When** they create a task, **Then** the task is permanently associated with their account
2. **Given** two users exist with their own tasks, **When** User A requests their task list, **Then** they see only their own tasks and none of User B's
3. **Given** User A owns a task, **When** User B attempts to view, update, or delete that task, **Then** the system denies access as if the task does not exist
4. **Given** a user is authenticated, **When** they request their tasks, **Then** the system filters results to show only tasks owned by that user

---

### User Story 3 - Persistent Data Storage (Priority: P1)

All user accounts and tasks are stored persistently so that data survives application restarts, deployments, and server maintenance. Users expect their data to be available whenever they return to the application.

**Why this priority**: Without persistent storage, all user data would be lost on every restart. This is a non-negotiable infrastructure requirement.

**Independent Test**: Can be tested by creating a user and tasks, restarting the application, and verifying all data is intact.

**Acceptance Scenarios**:

1. **Given** a user has created tasks, **When** the application is restarted, **Then** all previously created tasks are still available
2. **Given** a user has registered an account, **When** the application is restarted, **Then** the user can still log in with their credentials
3. **Given** multiple users have data in the system, **When** the database is queried, **Then** all user data maintains its ownership relationships

---

### User Story 4 - Secure Session Management (Priority: P2)

A logged-in user's session remains valid for 24 hours from the time of login. After 24 hours, the session expires automatically regardless of activity, requiring the user to log in again. Users can also explicitly end their session by logging out at any time.

**Why this priority**: Good session management balances security with convenience. It is important but depends on the authentication foundation being in place first.

**Independent Test**: Can be tested by logging in, simulating clock advancement past 24 hours from login time, and verifying the session has expired regardless of intervening activity.

**Acceptance Scenarios**:

1. **Given** a user has logged in, **When** they make requests within the session validity period, **Then** they remain authenticated without re-entering credentials
2. **Given** a user's session has expired, **When** they attempt to access a protected resource, **Then** they are redirected to the login page with the message: "Your session has expired. Please log in again."
3. **Given** a user explicitly logs out, **When** they attempt to access a protected resource, **Then** they are denied access immediately

---

### User Story 5 - Unauthenticated Access Protection (Priority: P2)

Any visitor who has not logged in is prevented from accessing task management features. They are directed to log in or register before they can interact with the application's core functionality.

**Why this priority**: Protects the system from unauthorized access and ensures all task operations are attributable to a specific user.

**Independent Test**: Can be tested by attempting to access task endpoints without authentication and verifying that access is denied.

**Acceptance Scenarios**:

1. **Given** a visitor is not authenticated, **When** they attempt to view tasks, **Then** they are denied access and redirected to the login page
2. **Given** a visitor is not authenticated, **When** they attempt to create, update, or delete a task, **Then** the operation is rejected with a 401 status
3. **Given** a visitor is not authenticated, **When** they navigate to a protected page, **Then** they are redirected to the login page

---

### User Story 6 - Data Migration from Pre-Auth System (Priority: P1)

The existing application has tasks stored without user ownership. When authentication and persistent storage are introduced, any pre-existing tasks that cannot be attributed to a user are discarded. After migration, all tasks in the system have a valid owner.

**Why this priority**: Without a clear migration strategy, the transition from the unauthenticated system to the authenticated system would leave orphaned data or cause errors.

**Independent Test**: Can be tested by verifying that after the migration, no tasks exist without a valid `user_id` foreign key, and all database constraints are satisfied.

**Acceptance Scenarios**:

1. **Given** the system is being upgraded from an unauthenticated version, **When** the migration runs, **Then** all pre-existing tasks without an owner are removed
2. **Given** the migration has completed, **When** querying the database, **Then** every task has a valid user owner reference
3. **Given** a new deployment with an empty database, **When** the application starts, **Then** the database schema is created with all required tables, foreign keys, and indexes

---

### Edge Cases

- What happens when a user's session token is tampered with or malformed? The system rejects the request with 401 and requires re-authentication.
- What happens when a user tries to register with an invalid email format? The system rejects the registration with the message: "Please enter a valid email address."
- What happens when the database is temporarily unavailable? The system returns the message: "Something went wrong on our end. Please try again later." without exposing internal details.
- What happens when a user account is deleted? Their tasks are also removed (cascade deletion) to prevent orphaned data.
- What happens when two users attempt to register with the same email simultaneously? Only one registration succeeds; the other receives: "An account with this email already exists. Please log in instead."
- What happens when a session token expires mid-operation (e.g., while editing a task)? The user sees: "Your session has expired. Please log in again." and is redirected to the login page. The in-progress operation is not saved.
- What happens when a user submits a password that meets the length requirement but not the complexity requirement? The system rejects with: "Password must contain at least one uppercase letter, one lowercase letter, and one number."

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow new users to register with an email address and password
- **FR-002**: System MUST authenticate returning users with their email and password
- **FR-003**: System MUST issue a session credential as an httpOnly cookie upon successful authentication. The frontend MUST NOT handle or store the raw credential. The frontend MUST use `credentials: 'include'` on all API requests so the browser attaches the cookie to cross-origin requests.
- **FR-004**: System MUST verify the session credential on every request to a protected resource
- **FR-005**: System MUST associate every newly created task with the authenticated user who created it
- **FR-006**: System MUST filter all task queries to return only tasks belonging to the authenticated user
- **FR-007**: System MUST enforce a two-layer authorization model for task endpoints: (a) return 403 when `{user_id}` in path does not match the authenticated user's ID, and (b) return 404 when `{user_id}` matches but `{task_id}` is not owned by that user, to avoid revealing resource existence
- **FR-008**: System MUST store all user accounts and tasks in persistent storage that survives application restarts
- **FR-009**: System MUST automatically expire sessions 24 hours after authentication, regardless of activity
- **FR-010**: System MUST allow users to explicitly end their session (log out) by clearing the session credential
- **FR-011**: System MUST reject all task operations from unauthenticated visitors with 401 status
- **FR-012**: System MUST validate email format during registration, normalize emails to lowercase before storage and comparison, and require passwords of at least 8 characters containing at least one uppercase letter, one lowercase letter, and one number
- **FR-013**: System MUST never store passwords in plain text; passwords MUST be hashed using a one-way cryptographic hash
- **FR-014**: System MUST maintain referential integrity between users and their tasks (deleting a user removes their tasks via cascade)
- **FR-015**: System MUST return the exact error messages defined in the Error Message Catalog for all authentication and authorization failures
- **FR-016**: System MUST provide a session identity endpoint that returns the current authenticated user's identifier and email, so the frontend can determine the logged-in user without reading the cookie
- **FR-017**: System MUST enforce rate limiting of 1000 requests per hour per authenticated user, as required by the constitution. Unauthenticated requests (login, register, and other public endpoints) MUST be rate-limited by IP address at 100 requests per hour
- **FR-018**: System MUST run database schema migrations on deployment, creating all required tables, foreign keys, and indexes
- **FR-019**: System MUST discard any pre-existing tasks that have no valid user owner during the migration to the authenticated system
- **FR-020**: Authentication implementation in this feature MUST remain compatible with the constitution's Phase II authentication stack requirement (Better Auth with JWT), while preserving the endpoint contracts defined in feature-01 and feature-02

### Key Entities

- **User**: Represents a registered person in the system. Key attributes: unique identifier, email address (unique), account creation timestamp. Email serves as the sole user identifier. Each user owns zero or more tasks.
- **Task**: Represents a to-do item belonging to a user. Key attributes: unique identifier, owner (user, required foreign key), title (required, max 255 characters), description (optional, max 5000 characters), completion status, creation timestamp, last-modified timestamp. Each task belongs to exactly one user.
- **Session**: Represents an active authentication session. Key attributes: session credential (httpOnly cookie), associated user, creation timestamp, expiry timestamp (24 hours from creation). Each session belongs to exactly one user.

## Error Message Catalog

All error responses MUST use the following exact messages. No raw error codes, JSON structures, or stack traces may be visible to users.

| Condition | HTTP Status | Error Code | User-Facing Message |
|-----------|-------------|------------|---------------------|
| Duplicate email on registration | 409 | EMAIL_ALREADY_EXISTS | "An account with this email already exists. Please log in instead." |
| Invalid credentials on login | 401 | INVALID_CREDENTIALS | "Invalid email or password. Please try again." |
| Invalid email format | 400 | VALIDATION_ERROR | "Please enter a valid email address." |
| Password too weak | 400 | VALIDATION_ERROR | "Password must be at least 8 characters and contain at least one uppercase letter, one lowercase letter, and one number." |
| Missing/expired session | 401 | SESSION_EXPIRED | "Your session has expired. Please log in again." |
| Tampered/malformed token | 401 | INVALID_TOKEN | "Your session has expired. Please log in again." |
| Access to another user's task | 404 | TASK_NOT_FOUND | "This task could not be found." |
| Unauthenticated request | 401 | UNAUTHORIZED | "Please log in to continue." |
| Rate limit exceeded | 429 | RATE_LIMITED | "Too many requests. Please wait a moment and try again." |
| Server error | 500 | INTERNAL_ERROR | "Something went wrong on our end. Please try again later." |
| Database unavailable | 503 | SERVICE_UNAVAILABLE | "Something went wrong on our end. Please try again later." |

## Error Response Format

All error responses MUST follow this consistent structure, as established by feature-01:

```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable message from catalog above"
  }
}
```

Successful responses MUST follow:

```json
{
  "success": true,
  "data": { ... },
  "error": null
}
```

Auth endpoints defined below MUST also use this wrapped success response shape (no unwrapped success bodies).

## Auth Endpoint Contract

This feature introduces or modifies the following endpoints. All endpoints are consistent with the contracts defined in feature-01 (`specs/1-specify/phase-2/feature-01-fastapi-todo-backend.md`) and feature-02 (`specs/1-specify/phase-2/feature-02-nextjs-todo-frontend.md`).

### Registration

- Method: `POST`
- Path: `/api/auth/register`
- Request body: `{ "email": "<valid email>", "password": "<string meeting FR-012 rules>" }`
- Success (201): Backend sets httpOnly, Secure, SameSite=Lax cookie. Body:
  `{ "success": true, "data": { "access_token": "<token>", "token_type": "bearer" }, "error": null }`.
  The `access_token` in `data` is provided for non-browser clients (API testing tools, future mobile apps). The frontend MUST ignore it and rely solely on the cookie.
- Error (409): EMAIL_ALREADY_EXISTS
- Error (400): VALIDATION_ERROR (invalid email or weak password)

### Login

- Method: `POST`
- Path: `/api/auth/login`
- Request body: `{ "email": "<valid email>", "password": "<string>" }`
- Success (200): Backend sets httpOnly, Secure, SameSite=Lax cookie. Body:
  `{ "success": true, "data": { "access_token": "<token>", "token_type": "bearer" }, "error": null }`.
  The `access_token` in `data` is provided for non-browser clients. The frontend MUST ignore it and rely solely on the cookie.
- Error (401): INVALID_CREDENTIALS

### Session Check

- Method: `GET`
- Path: `/api/auth/me`
- Authentication: httpOnly cookie (attached automatically by browser)
- Success (200): `{ "success": true, "data": { "id": "<uuid>", "email": "<string>" }, "error": null }`
- Error (401): SESSION_EXPIRED or INVALID_TOKEN

### Logout

- Method: `POST`
- Path: `/api/auth/logout`
- Authentication: httpOnly cookie
- Success (200): Backend clears the httpOnly cookie. Always succeeds even with invalid/missing cookie.
  Response body: `{ "success": true, "data": { "logged_out": true }, "error": null }`

### Task Endpoints (Modified)

All existing task endpoints from feature-01 remain unchanged in their paths and request/response shapes. The modification is:

- All task endpoints now REQUIRE authentication via httpOnly cookie or Bearer token header (dual-auth: cookie for browser, Bearer for non-browser clients; header takes priority if both present, consistent with feature-01 FR-020)
- The `{user_id}` path parameter MUST match the authenticated user's ID (extracted from the session credential)
- Unauthenticated requests receive 401
- Requests where `{user_id}` does not match the authenticated user receive 403

## Routing Table

| Path | Behavior | Auth Required |
|------|----------|---------------|
| `/` | Redirect to `/dashboard` if authenticated, otherwise redirect to `/login` | No |
| `/login` | Render login form. Redirect to `/dashboard` if already authenticated. | No (redirects if auth) |
| `/register` | Render registration form. Redirect to `/dashboard` if already authenticated. | No (redirects if auth) |
| `/dashboard` | Render task management interface. Redirect to `/login` if not authenticated. | Yes |

All other paths return a 404 page with the message: "Page not found." and a link back to the dashboard.

## Constraints

### Security

- **SEC-001**: The session credential MUST be transmitted as an httpOnly, Secure, SameSite=Lax cookie. The frontend MUST NOT handle raw tokens.
- **SEC-002**: The system MUST return 401 for missing or invalid session credentials
- **SEC-003**: The system MUST check the `{user_id}` path parameter FIRST, before any database query. If the authenticated user's ID does not match `{user_id}`, return 403 immediately (no DB lookup needed).
- **SEC-004**: If the `{user_id}` path parameter matches but the specific `{task_id}` is not owned by the user (e.g., direct ID guessing), return 404 (not 403) to avoid revealing resource existence. This is the second layer of defense, checked only after SEC-003 passes.
- **SEC-005**: All user inputs MUST be validated against schema before processing
- **SEC-006**: Passwords MUST be hashed using a one-way cryptographic hash before storage
- **SEC-007**: Rate limiting MUST be enforced at 1000 requests per hour per authenticated user, and 100 requests per hour per IP for unauthenticated endpoints, per constitution Section 3
- **SEC-008**: Backend MUST configure CORS to allow the frontend origin with `credentials: true`, using an explicit origin allowlist (not wildcard `*`). Without this, cookie-based auth will silently fail on cross-origin requests. Consistent with feature-01 FR-021.

### Accessibility

- **ACC-001**: Login and registration pages MUST conform to WCAG 2.1 Level AA, per constitution
- **ACC-002**: All form inputs MUST have associated visible labels and aria-labels
- **ACC-003**: All interactive elements MUST be reachable and operable via keyboard alone (Tab, Enter, Escape)
- **ACC-004**: Color contrast MUST meet a minimum ratio of 4.5:1 for normal text and 3:1 for large text in both themes
- **ACC-005**: Form validation errors MUST be announced to screen readers

### Performance

- **PERF-001**: Auth endpoints (login, register, logout) MUST respond within 300ms for 95% of requests, per constitution Phase II targets
- **PERF-002**: Session validation (checking the cookie on each request) MUST add no more than 50ms overhead to existing endpoint response times
- **PERF-003**: The system MUST support 100 concurrent authenticated users without degradation, per constitution Phase II quality targets
- **PERF-004**: Database queries MUST use indexes on all foreign keys and frequently queried fields (user_id, email, completed status)
- **PERF-005**: Persistent storage MUST support at least 10,000 tasks per user without performance degradation, consistent with feature-01 TC-002

### Testing

- **TEST-001**: Automated test coverage MUST reach 60% of business logic, per constitution Phase II targets
- **TEST-002**: All 6 user stories MUST have corresponding acceptance tests that can be executed as part of a test suite
- **TEST-003**: Data isolation MUST be verified by automated tests that attempt cross-user access and confirm denial

### Session and Token Behavior

- **SESS-001**: Session credentials expire 24 hours after authentication, regardless of activity. When expired, the backend returns 401 and the frontend redirects to the login page.
- **SESS-002**: Token refresh is explicitly out of scope for this iteration. Expired sessions require full re-authentication.

## Non-Goals

The following are explicitly NOT part of this specification and MUST NOT be implemented:

- **No third-party OAuth/SSO**: Users authenticate only with email and password. Integration with Google, GitHub, or other identity providers is deferred to a future phase.
- **No two-factor authentication (2FA)**: Login requires only email and password. TOTP, SMS, or hardware key support is out of scope.
- **No email verification**: Registration accepts email and password without verifying that the email is real or owned by the user. Verification workflows are deferred.
- **No password reset or recovery**: Users who forget their password have no self-service recovery flow. This is deferred to a future iteration.
- **No password history or rotation**: Users can reuse previous passwords. There is no forced rotation policy.
- **No account lockout after failed attempts**: The system does not lock accounts after repeated failed login attempts. Rate limiting (FR-017) provides the only brute-force protection.
- **No session revocation**: There is no mechanism to invalidate all sessions for a user (e.g., "log out everywhere"). Only single-session logout (FR-010) is supported.
- **No multi-device session management**: The system does not track or display active sessions across devices. Users cannot see or manage sessions from other devices.
- **No "remember me" functionality**: All sessions expire 24 hours after login. There is no option for extended session duration.
- **No role-based access control**: All authenticated users have identical permissions. Admin roles, moderators, or tiered access are out of scope.
- **No audit logging of auth events**: Login attempts, registration events, and session expirations are not logged for audit purposes. Structured logging covers operational concerns only.
- **No account deletion self-service**: Users cannot delete their own accounts. Account removal is an admin-only operation for this phase.
- **No real-time session notifications**: Users are not notified in real-time when their session is about to expire. Expiration is detected on the next request.

## Migration Strategy

### Pre-Auth to Auth Transition

Baseline clarification: this migration targets the pre-Part-3 baseline where auth/session and persistent ownership guarantees are not yet enforced for all existing task data paths. This section defines the required behavior regardless of whether legacy data came from in-memory task storage or an early schema without enforced ownership.

The transition to authenticated, persistent storage requires:

1. **Database initialization**: On first deployment with the new schema, create all required tables (users, tasks with `user_id` foreign key) with proper indexes and constraints
2. **Orphaned data handling**: Any tasks existing in the previous in-memory store that lack a valid `user_id` are discarded. There is no attempt to migrate anonymous tasks.
3. **Clean start**: After migration, the system begins with an empty user base. All users must register fresh accounts.
4. **Schema versioning**: The migration is versioned and can be rolled back to the previous schema if needed

### Rollback Plan

If the migration fails or the new auth system has critical issues:
1. Revert to the previous deployment (pre-auth frontend and backend)
2. The previous in-memory task store continues functioning as before
3. No user data is lost because the auth system starts fresh (no existing user data to lose)

## Deliverables

The following artifacts MUST be produced as part of this feature:

- All authentication-related backend code (registration, login, logout, session check, token verification, password hashing)
- Database schema migration files creating users and tasks tables with constraints
- Frontend authentication pages (login, register) and route protection
- Frontend session management (cookie-based auth, session check on load)
- Updated `frontend/CLAUDE.md` and `backend/CLAUDE.md` with auth-specific patterns, as required by the constitution for Phase II+
- Automated tests meeting the 60% coverage target for auth business logic
- Every code file MUST include a comment referencing the task ID from `specs/3-tasks/` that it implements, per constitution traceability requirements
- A `.env.example` file documenting all required environment variables (database connection, auth secret)
- Existing Phase II task artifacts MUST be updated to include explicit Feature-03 task IDs and traceability mapping before implementation starts (no implementation without task linkage)

## Assumptions

- Users authenticate with email and password only (no third-party OAuth providers in this phase)
- The application is a web-based system where the frontend and backend communicate over a network
- The frontend from feature-02 already supports httpOnly cookie authentication (the backend sets the cookie; the frontend uses `credentials: 'include'` on all fetch calls)
- The backend from feature-01 already has auth endpoint stubs (register, login, me, logout) that will be connected to persistent storage
- The system operates in a single-region deployment for this phase
- The existing in-memory task store will be replaced entirely by persistent database storage
- Session credential uses the same HS256-signed token format already established in features 01 and 02

## Dependencies

- **Feature-01** (FastAPI Todo Backend) must be complete — provides the task CRUD endpoints and auth endpoint stubs
- **Feature-02** (Next.js Todo Frontend) must be complete — provides the user interface, auth pages, and cookie-based session handling
- A persistent relational database must be available in the deployment environment
- A shared secret must be available as an environment variable for signing session credentials
- Any conflicting auth/session/error details in sibling Phase II specs MUST be synchronized to this feature's canonical rules before code implementation

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: New users can complete registration and see the dashboard within 3 user actions (navigate to register, fill form, submit). Verified by manual walkthrough.
- **SC-002**: Returning users can log in and see their task list within 5 seconds of submitting credentials. Verified by measuring time from form submission to visible task list.
- **SC-003**: 100% of task queries return only tasks owned by the requesting user (zero cross-user data leakage). Verified by automated tests that create two users and confirm isolation.
- **SC-004**: All user and task data persists across application restarts with zero data loss. Verified by creating data, restarting the application, and confirming all data is intact.
- **SC-005**: 100% of unauthenticated requests to protected resources are rejected with 401 status. Verified by automated tests against every protected endpoint.
- **SC-006**: Sessions expire automatically 24 hours after login, regardless of activity, requiring re-authentication. Verified by simulating clock advancement past 24h from login time in tests.
- **SC-007**: Users can complete a full task management workflow (create, view, edit, complete, delete) without re-authenticating during an active session. Verified by end-to-end test.
- **SC-008**: Auth endpoints respond within 300ms for 95% of requests under load of 100 concurrent users. Verified by load testing.
- **SC-009**: Every error condition in the Error Message Catalog produces the exact specified message with no raw error codes or stack traces visible. Verified by triggering each error condition and comparing output.
- **SC-010**: Automated test coverage of auth business logic reaches 60% or higher. Verified by running the test suite with coverage reporting.
- **SC-011**: All login and registration pages pass an automated accessibility audit with zero critical or serious violations. Verified by running axe-core or equivalent against each auth route.

## Clarifications

### Session 2026-02-15

- Q: Should sessions use a sliding window (reset on activity) or absolute expiry (fixed from login)? → A: Absolute 24-hour expiry from login. Sessions expire 24 hours after authentication regardless of activity. Forces daily re-login.
- Q: Should the User entity have a display name field? → A: No. Drop display name entirely. Email is the only user identifier, consistent with features 01 and 02. Name can be added in a future iteration.
- Q: Do the frontend and backend run on the same origin, or is CORS required for cookie auth? → A: Cross-origin. Backend MUST allow the frontend origin with credentials enabled, using an explicit origin allowlist (not wildcard). Consistent with feature-01 FR-021.
- Q: Should feature-03 inherit feature-01's 10,000 tasks-per-user data volume limit? → A: Yes. Persistent storage must support at least 10,000 tasks per user, consistent with feature-01 TC-002.
- Q: FR-003 says "same-origin" but SEC-008 says cross-origin — which is it? → A: Cross-origin. FR-003 updated to reference `credentials: 'include'` for cross-origin cookie attachment, consistent with SEC-008 and feature-02.
- Q: Are email addresses case-sensitive for registration and login? → A: Case-insensitive. All emails normalized to lowercase before storage and comparison. `User@Test.com` and `user@test.com` are the same account.
- Q: Why does the response body include access_token if the frontend must not handle it? → A: Deliberate dual-auth pattern. Cookie for browser clients, access_token in body for non-browser clients (API testing, future mobile). Frontend MUST ignore the body token. Consistent with feature-01 FR-020 (supports both Bearer header and cookie).
- Q: How are unauthenticated requests rate-limited (no user ID available)? → A: By IP address at 100 requests per hour (stricter than the 1000/hr for authenticated users). Protects login/register endpoints from brute-force attacks.
- Q: When SEC-003 (403) and FR-007 (404) both apply, which fires first? → A: Two-layer defense. Path check first: if `{user_id}` doesn't match authenticated user, return 403 immediately (no DB query). Task-level check second: if `{user_id}` matches but `{task_id}` not owned, return 404. SEC-003 always runs before SEC-004/FR-007.
- Q: Feature-02 still mentions 15-minute token expiry in one section. Which value governs Part 3? → A: For this feature, 24-hour absolute expiry is canonical. Sibling specs must be synchronized before implementation.
- Q: Should auth endpoint success bodies be wrapped or unwrapped? → A: Wrapped format is canonical for this feature: `{ success, data, error }` for all success and error responses.
