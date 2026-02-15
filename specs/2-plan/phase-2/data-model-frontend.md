# Data Model: Next.js Todo Frontend

**Feature**: 006-nextjs-todo-frontend | **Date**: 2026-02-13

## Frontend TypeScript Types

These types represent the frontend's view of data. They mirror backend response shapes but are owned by the frontend.

### User (Session Identity)

```typescript
// Populated from GET /api/auth/me
interface User {
  id: string       // UUID
  email: string
}
```

**Source**: Backend `GET /api/auth/me` response
**Lifecycle**: Created on dashboard layout load, destroyed on logout
**Storage**: React Context (in-memory only). Never persisted client-side.

### Task

```typescript
interface Task {
  id: string              // UUID
  title: string           // Required, max 255 chars
  description: string | null  // Optional, max 5000 chars
  is_completed: boolean   // Default false
  created_at: string      // ISO 8601 datetime
  updated_at: string      // ISO 8601 datetime
  owner_id: string        // UUID, matches authenticated user
}
```

**Source**: Backend task endpoints
**Lifecycle**: Fetched on dashboard load, mutated via CRUD operations
**Storage**: TanStack Query cache, key `['tasks', userId]`
**Ordering**: Newest-first (by `created_at` DESC, backend-enforced)

### Task Mutations (Request Shapes)

```typescript
// POST /api/{userId}/tasks
interface TaskCreateRequest {
  title: string       // Required, 1-255 chars
  description?: string // Optional, 0-5000 chars
}

// PUT /api/{userId}/tasks/{taskId}
interface TaskUpdateRequest {
  title?: string       // Optional, 1-255 chars if provided
  description?: string // Optional, 0-5000 chars if provided
}

// PATCH /api/{userId}/tasks/{taskId}/complete — no body
// DELETE /api/{userId}/tasks/{taskId} — no body
```

### Auth Requests

```typescript
// POST /api/auth/register, POST /api/auth/login
interface AuthRequest {
  email: string    // Valid email format
  password: string // Min 8 characters
}

// Response from login/register (JSON body — frontend ignores token)
interface TokenResponse {
  access_token: string
  token_type: 'bearer'
}
```

### API Error

```typescript
interface ApiErrorResponse {
  success: false
  data: null
  error: {
    code: string    // e.g., INVALID_CREDENTIALS, TASK_NOT_FOUND
    message: string // Backend message (may differ from user-facing message)
  }
}
```

**Frontend maps error codes to user-friendly messages via the error catalog in `api-client.ts`.**

## Validation Rules (Zod Schemas)

```typescript
// Login/Register
const authSchema = z.object({
  email: z.string().email('Please enter a valid email address.'),
  password: z.string().min(8, 'Password must be at least 8 characters.'),
})

// Task Create
const taskCreateSchema = z.object({
  title: z.string()
    .min(1, 'Title is required.')
    .max(255, 'Title must be 255 characters or less.'),
  description: z.string()
    .max(5000, 'Description must be 5000 characters or less.')
    .optional()
    .or(z.literal('')),
})

// Task Update (same constraints, title can be provided or omitted)
const taskUpdateSchema = taskCreateSchema
```

## State Transitions

### Task State

```
                 ┌──────────────────┐
  create ───────►│  is_completed:   │
                 │     false        │
                 └────────┬─────────┘
                          │
                   toggle │
                          ▼
                 ┌──────────────────┐
                 │  is_completed:   │
                 │     true         │
                 └────────┬─────────┘
                          │
                   toggle │
                          ▼
                 ┌──────────────────┐
                 │  is_completed:   │
                 │     false        │
                 └──────────────────┘

  Any state ──── delete ────► removed
  Any state ──── edit ──────► title/description updated
```

### Session State

```
  Unauthenticated ──── register/login ────► Authenticated
                                                │
  Authenticated ────── logout ────────────► Unauthenticated
  Authenticated ────── 401 (expired) ─────► Unauthenticated
                                            (redirect to /login
                                             with expiry message)
```

## Entity Relationships

```
  User (1) ◄────────────── (*) Task
       │                        │
       │  id ◄── owner_id ─────┘
       │
       └── Session exists only in-memory (UserContext)
           Populated from GET /api/auth/me
           Destroyed on logout or 401

  TanStack Query Cache:
       ['tasks', userId] ────► Task[]
       Invalidated on: create, update, delete, toggle (onSettled)
       Optimistically updated on: all mutations (onMutate)
```
