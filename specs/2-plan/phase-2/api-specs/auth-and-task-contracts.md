# Auth & Task API Contracts — Feature 007 (Auth-DB-Monorepo)

**Status**: FROZEN
**Created**: 2026-02-15
**Branch**: `007-auth-db-monorepo`
**Spec**: @specs/1-specify/phase-2/feature-03-auth-db-monorepo.md
**Plan**: @specs/2-plan/phase-2/phase-2-auth-db-monorepo.md

---

## Contract-Freeze Checklist

- [x] Endpoint matrix documented below
- [x] Auth precedence rule defined
- [x] Error catalog mapping table complete (11 entries)
- [x] CORS/credentials settings agreed

---

## Endpoint Matrix

### Auth Endpoints (public — no session required)

| Method | Path | Auth | Success | Description |
|--------|------|------|---------|-------------|
| POST | `/api/auth/register` | None | 201 | Register new user; issues httpOnly cookie |
| POST | `/api/auth/login` | None | 200 | Authenticate user; issues httpOnly cookie |
| POST | `/api/auth/logout` | Optional | 200 | Clear httpOnly cookie; always succeeds |
| GET | `/api/auth/me` | Required | 200 | Return current user id + email |

### Task Endpoints (protected — session required)

| Method | Path | Auth | Success | Description |
|--------|------|------|---------|-------------|
| GET | `/api/{user_id}/tasks` | Required | 200 | List user's tasks (paginated) |
| POST | `/api/{user_id}/tasks` | Required | 201 | Create task for user |
| GET | `/api/{user_id}/tasks/{task_id}` | Required | 200 | Get specific task |
| PUT | `/api/{user_id}/tasks/{task_id}` | Required | 200 | Update task title/description |
| DELETE | `/api/{user_id}/tasks/{task_id}` | Required | 204 | Delete task |
| PATCH | `/api/{user_id}/tasks/{task_id}/complete` | Required | 200 | Toggle completion |

---

## Auth Precedence Rule

When a request arrives at a protected endpoint, the backend resolves the session credential in this order:

1. **Check `Authorization: Bearer <token>` header** — if present and valid, use it
2. **Else check `access_token` httpOnly cookie** — if present and valid, use it
3. **Else raise 401 UNAUTHORIZED**

**Rationale**: Bearer header takes priority to support non-browser clients (API testing tools, future mobile clients) while the browser uses the cookie automatically.

---

## Response Envelope

### Success envelope
```json
{
  "success": true,
  "data": { "...": "..." },
  "error": null
}
```

### Error envelope
```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable message"
  }
}
```

---

## Auth Endpoint Request/Response Shapes

### POST /api/auth/register → 201

Request:
```json
{ "email": "user@example.com", "password": "SecurePass1" }
```
Response body:
```json
{ "success": true, "data": { "access_token": "<jwt>", "token_type": "bearer" }, "error": null }
```
Response headers: `Set-Cookie: access_token=<jwt>; HttpOnly; Secure; SameSite=Lax; Max-Age=86400; Path=/`

Note: `access_token` in the body is for non-browser clients only. Frontend ignores it and uses the cookie.

### POST /api/auth/login → 200

Request:
```json
{ "email": "user@example.com", "password": "SecurePass1" }
```
Response body:
```json
{ "success": true, "data": { "access_token": "<jwt>", "token_type": "bearer" }, "error": null }
```
Response headers: `Set-Cookie: access_token=<jwt>; HttpOnly; Secure; SameSite=Lax; Max-Age=86400; Path=/`

### POST /api/auth/logout → 200

No request body required (even with no valid cookie, returns 200).
Response body:
```json
{ "success": true, "data": { "logged_out": true }, "error": null }
```
Response headers: `Set-Cookie: access_token=; HttpOnly; Secure; SameSite=Lax; Max-Age=0; Path=/`

### GET /api/auth/me → 200

No request body. Cookie or Bearer header required.
Response body:
```json
{ "success": true, "data": { "id": "<uuid>", "email": "user@example.com" }, "error": null }
```

---

## JWT Token Format

| Field | Value |
|-------|-------|
| Algorithm | HS256 |
| Header | `{"alg": "HS256", "typ": "JWT"}` |
| Payload `sub` | `str(user.id)` — UUID as string |
| Payload `email` | user's email string |
| Payload `exp` | `now() + 86400 seconds` (24h absolute, no refresh) |
| Secret | `SECRET_KEY` env var (shared between backend PyJWT/python-jose and frontend better-auth) |

---

## Error Catalog Mapping Table

| Condition | HTTP Status | Code | Exact Message |
|-----------|-------------|------|---------------|
| Duplicate email on registration | 409 | `EMAIL_ALREADY_EXISTS` | "An account with this email already exists. Please log in instead." |
| Invalid credentials on login | 401 | `INVALID_CREDENTIALS` | "Invalid email or password. Please try again." |
| Invalid email format | 400 | `VALIDATION_ERROR` | "Please enter a valid email address." |
| Password too weak | 400 | `VALIDATION_ERROR` | "Password must be at least 8 characters and contain at least one uppercase letter, one lowercase letter, and one number." |
| Missing or expired session | 401 | `SESSION_EXPIRED` | "Your session has expired. Please log in again." |
| Tampered or malformed token | 401 | `INVALID_TOKEN` | "Your session has expired. Please log in again." |
| Unauthenticated request (no token) | 401 | `UNAUTHORIZED` | "Please log in to continue." |
| `{user_id}` path mismatch | 403 | `FORBIDDEN` | "You do not have permission to perform this action." |
| Task not owned by user | 404 | `TASK_NOT_FOUND` | "This task could not be found." |
| Rate limit exceeded | 429 | `RATE_LIMITED` | "Too many requests. Please wait a moment and try again." |
| Server error | 500 | `INTERNAL_ERROR` | "Something went wrong on our end. Please try again later." |
| Database unavailable | 503 | `SERVICE_UNAVAILABLE` | "Something went wrong on our end. Please try again later." |

---

## CORS Configuration

| Setting | Value |
|---------|-------|
| `allow_origins` | `[os.getenv("CORS_ORIGIN", "http://localhost:3000")]` — explicit allowlist, **no wildcard** |
| `allow_credentials` | `True` — required for httpOnly cookie transport |
| `allow_methods` | `["*"]` |
| `allow_headers` | `["*"]` |

**CORS_ORIGIN env var** must be set to the frontend origin in all environments. Without this, cookie-based auth silently fails on cross-origin requests (SEC-008).

---

## Rate Limit Policy

| Client Type | Key | Limit | Window |
|-------------|-----|-------|--------|
| Authenticated user | `rate:user:{user_id}:{epoch_hour}` | 1000 req | 1 hour |
| Unauthenticated IP | `rate:ip:{ip_address}:{epoch_hour}` | 100 req | 1 hour |

Public endpoints (login, register) are rate-limited by IP. Protected endpoints are rate-limited by user_id (extracted from JWT, not from Depends()).

---

## Two-Layer Authorization Semantics (ADR-0013)

```
Request arrives at task endpoint
  └─► Is user authenticated? (check Bearer header, then cookie)
        NO  → 401 UNAUTHORIZED
        YES → Does {user_id} in path == current_user.id?
                NO  → 403 FORBIDDEN (no DB query performed)
                YES → Does {task_id} exist AND owner_id == current_user.id?
                        NO  → 404 TASK_NOT_FOUND
                        YES → Process request
```

The 403 check MUST fire before any database query. The 404 check uses the existing ownership filter in the ORM query (no explicit "does this task exist?" check needed — the query simply returns nothing).
