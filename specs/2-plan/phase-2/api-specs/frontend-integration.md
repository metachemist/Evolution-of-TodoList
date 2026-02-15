# Frontend API Integration Contract

**Feature**: 006-nextjs-todo-frontend | **Date**: 2026-02-13

## Overview

This document defines how the Next.js frontend integrates with the FastAPI backend. All communication flows through a centralized API client (`lib/api-client.ts`) per FR-018.

## Transport: httpOnly Cookie Authentication

- **Mechanism**: The backend sets `access_token` as an httpOnly, Secure, SameSite=Lax cookie on login/register
- **Client-side calls**: Use `credentials: 'include'` — browser attaches cookie automatically
- **Server-side calls (RSC)**: Forward cookie via `cookies().get('access_token')` in the `Cookie` header
- **No Authorization header**: The frontend never reads or sends the JWT as a Bearer token

## Base URL

- **Environment variable**: `NEXT_PUBLIC_API_URL` (default: `http://localhost:8000`)
- **Timeout**: 15 seconds per request (AbortSignal.timeout)

## Endpoint Contracts

### Authentication

#### POST /api/auth/register
```
Request:  { email: string, password: string }
Response: 201 { access_token: string, token_type: "bearer" }
          + Set-Cookie: access_token=<jwt>; HttpOnly; Secure; SameSite=Lax
Errors:   409 EMAIL_ALREADY_EXISTS
Frontend: Ignore response body token. Cookie is set automatically.
          Redirect to /dashboard on success.
```

#### POST /api/auth/login
```
Request:  { email: string, password: string }
Response: 200 { access_token: string, token_type: "bearer" }
          + Set-Cookie: access_token=<jwt>; HttpOnly; Secure; SameSite=Lax
Errors:   401 INVALID_CREDENTIALS
Frontend: Ignore response body token. Cookie is set automatically.
          Redirect to /dashboard on success.
```

#### GET /api/auth/me
```
Request:  No body. Cookie sent automatically.
Response: 200 { id: string (UUID), email: string }
Errors:   401 (expired/invalid token)
Frontend: Called from (dashboard) layout RSC.
          Cookie forwarded explicitly via cookies() API.
          On 401: redirect to /login.
```

#### POST /api/auth/logout
```
Request:  No body. Cookie sent automatically.
Response: 200 { message: "Logged out successfully" }
          + Set-Cookie: access_token=; expires=Thu, 01 Jan 1970... (clears cookie)
Errors:   None (always returns 200)
Frontend: Clear UserContext, redirect to /login.
```

### Tasks

All task endpoints require a valid `access_token` cookie. The `{user_id}` path parameter must match the JWT `sub` claim.

#### GET /api/{user_id}/tasks?skip=0&limit=20
```
Request:  Query params: skip (int, default 0), limit (int, default 20, max 100)
Response: 200 TaskResponse[]
Frontend: TanStack Query key: ['tasks', userId]
          Fetched on dashboard mount.
          Frontend does NOT paginate — uses backend defaults.
```

#### POST /api/{user_id}/tasks
```
Request:  { title: string, description?: string }
Response: 201 TaskResponse
Frontend: Optimistic insert at index 0 of task list.
          On error: remove optimistic task, show error toast 5s.
          On success: toast "Task created" 3s.
```

#### PUT /api/{user_id}/tasks/{task_id}
```
Request:  { title?: string, description?: string }
Response: 200 TaskResponse
Frontend: Optimistic update of matching task in cache.
          On error: revert to previous state, show error toast 5s.
          On success: toast "Task updated" 3s.
```

#### DELETE /api/{user_id}/tasks/{task_id}
```
Request:  No body.
Response: 204 No Content
Frontend: Optimistic removal from task list.
          On error: reinsert task at original position, show error toast 5s.
          On success: toast "Task deleted" 3s.
```

#### PATCH /api/{user_id}/tasks/{task_id}/complete
```
Request:  No body.
Response: 200 TaskResponse
Frontend: Optimistic toggle of is_completed.
          On error: revert toggle, show error toast 5s.
          On success: no toast (visual change is sufficient).
```

## Error Mapping

The API client maps backend error codes to user-facing messages:

| HTTP Status | Error Code | User Message |
|---|---|---|
| 401 | INVALID_CREDENTIALS | "Invalid email or password. Please try again." |
| 401 | (expired token) | "Your session has expired. Please log in again." |
| 403 | UNAUTHORIZED_ACCESS | "You don't have permission to perform this action." |
| 404 | USER_NOT_FOUND | "Account not found. Please register first." |
| 404 | TASK_NOT_FOUND | "This task no longer exists. It may have been deleted." |
| 409 | EMAIL_ALREADY_EXISTS | "An account with this email already exists. Please log in instead." |
| 500 | (any) | "Something went wrong on our end. Please try again later." |
| 0 | NETWORK_ERROR | "Unable to connect to the server. Please check your connection and try again." |
| 0 | REQUEST_TIMEOUT | "The request is taking longer than expected. Please check your connection." |

**Note**: `NETWORK_ERROR` and `REQUEST_TIMEOUT` are client-side only — they are never returned by the backend. `REQUEST_TIMEOUT` is thrown when `AbortSignal.timeout(15000)` fires (`AbortError`). `NETWORK_ERROR` is thrown when `fetch()` itself fails to connect (`TypeError`). They must be handled separately in the `catch` block.

## Global Error Handling

- **401 from any endpoint**: `QueryCache.onError` catches `ApiError` with `statusCode === 401` → redirects to `/login?reason=session_expired`
- **403 from any endpoint**: `QueryCache.onError` catches `ApiError` with `statusCode === 403` → shows error toast "You don't have permission to perform this action." then redirects to `/dashboard` (spec edge case)
- **Timeout (>15s)**: `AbortSignal.timeout(15000)` fires → `AbortError` caught → throws `ApiError(0, 'REQUEST_TIMEOUT', "The request is taking longer than expected...")`
- **Connection failure**: `fetch()` throws `TypeError` → caught → throws `ApiError(0, 'NETWORK_ERROR', "Unable to connect to the server...")`
- **No-JS browsers**: Root layout `app/layout.tsx` includes `<noscript>This application requires JavaScript to run.</noscript>` in the HTML body (no client-side handling needed)
- **Optimistic rollback**: Each mutation's `onError` callback reverts the cache to the pre-mutation snapshot

## CORS Requirements

The backend must be configured with:
```python
CORSMiddleware(
    allow_origins=["http://localhost:3000"],  # Frontend origin
    allow_credentials=True,                    # Required for cookies
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Status**: Already configured in `backend/src/main.py`.
