# Page Architecture: Next.js Todo Frontend

**Feature**: 006-nextjs-todo-frontend | **Date**: 2026-02-13
**Spec**: @specs/1-specify/phase-2/feature-02-nextjs-todo-frontend.md
**Plan**: @specs/2-plan/phase-2/phase-2-nextjs-todo-frontend.md

## Route Map

| Path | File | Auth | Layout Group | Component Type |
|---|---|---|---|---|
| `/` | `app/page.tsx` | No | Root | Server Component (public landing page) |
| `/login` | `app/(auth)/login/page.tsx` | No (redirects if auth) | (auth) | Server + Client |
| `/register` | `app/(auth)/register/page.tsx` | No (redirects if auth) | (auth) | Server + Client |
| `/dashboard` | `app/(dashboard)/dashboard/page.tsx` | Yes | (dashboard) | Server + Client |
| `*` (404) | `app/not-found.tsx` | No | Root | Server Component |

## Layout Hierarchy

```
app/layout.tsx (Root)
├── ThemeProvider (next-themes)
├── QueryProvider (TanStack Query)
├── Toaster (Sonner)
│
├── app/(auth)/layout.tsx
│   ├── Minimal centered layout
│   ├── No navigation bar
│   ├── Max-width container (sm: 400px)
│   └── Children: login/page.tsx, register/page.tsx
│
└── app/(dashboard)/layout.tsx
    ├── Fetches GET /api/auth/me (Server Component)
    ├── Redirects to / on 401
    ├── Wraps children in UserProvider
    ├── Navigation bar (logo, email display, theme toggle, logout button)
    └── Children: dashboard/page.tsx
```

## Page Specifications

### Root Page (`/`)

**File**: `app/page.tsx`
**Type**: Server Component
**Behavior**: Public landing page with visible marketing UI and entry CTAs.

```
Landing page content renders at `/`.
Primary CTA ("Get Started") navigates to `/login`.
Secondary CTA ("Create account") navigates to `/register`.
```

**Note**: `/` is intentionally public and never guarded.

---

### Login Page (`/login`)

**File**: `app/(auth)/login/page.tsx`
**Type**: Server Component shell + Client Component form

**Layout**: Centered card on minimal background

```
┌─────────────────────────────────────┐
│           (centered card)            │
│                                      │
│  ┌────────────────────────────────┐  │
│  │         Focentra Logo          │  │
│  │                                │  │
│  │  [Session expired message]     │  │ ← Only if ?reason=session_expired
│  │                                │  │
│  │  Email:    [________________]  │  │
│  │  Password: [________________]  │  │
│  │                                │  │
│  │  [     Log In Button      ]    │  │
│  │                                │  │
│  │  Don't have an account?        │  │
│  │  Register here →               │  │
│  └────────────────────────────────┘  │
│                                      │
└─────────────────────────────────────┘
```

**States**:
- Default: Empty form
- Session expired: Banner "Your session has expired. Please log in again." above form
- Validation errors: Inline below each field (on blur + submit)
- Backend error: Error message below form (e.g., "Invalid email or password")
- Submitting: Button shows loading state, disabled

---

### Register Page (`/register`)

**File**: `app/(auth)/register/page.tsx`
**Type**: Server Component shell + Client Component form

**Layout**: Same centered card as login

```
┌─────────────────────────────────────┐
│           (centered card)            │
│                                      │
│  ┌────────────────────────────────┐  │
│  │         Focentra Logo          │  │
│  │                                │  │
│  │  Email:    [________________]  │  │
│  │  Password: [________________]  │  │
│  │                                │  │
│  │  [    Create Account      ]    │  │
│  │                                │  │
│  │  Already have an account?      │  │
│  │  Log in here →                 │  │
│  └────────────────────────────────┘  │
│                                      │
└─────────────────────────────────────┘
```

**States**: Same as login (minus session expired message)

---

### Dashboard Page (`/dashboard`)

**File**: `app/(dashboard)/dashboard/page.tsx`
**Type**: Server Component shell → Client Component TaskList

**Layout**:

#### Desktop (>1024px)
```
┌─────────────────────────────────────────────────────┐
│ Nav: [Logo]              [user@email.com] [🌙] [Logout] │
├─────────────────────────────────────────────────────┤
│                                                       │
│  ┌─── Main Content (max-width: 768px, centered) ───┐ │
│  │                                                   │ │
│  │  My Tasks                    [+ Create Task]      │ │
│  │                                                   │ │
│  │  ┌─────────────────────────────────────────────┐  │ │
│  │  │ ☑ Buy groceries                    [✏️][🗑️] │  │ │
│  │  │   Get milk, eggs, and bread...              │  │ │
│  │  ├─────────────────────────────────────────────┤  │ │
│  │  │ ☐ Write report                     [✏️][🗑️] │  │ │
│  │  │   Quarterly performance review for...       │  │ │
│  │  ├─────────────────────────────────────────────┤  │ │
│  │  │ ☐ Call dentist                     [✏️][🗑️] │  │ │
│  │  │                                             │  │ │
│  │  └─────────────────────────────────────────────┘  │ │
│  │                                                   │ │
│  └───────────────────────────────────────────────────┘ │
│                                                       │
└─────────────────────────────────────────────────────┘
```

#### Mobile (<768px)
```
┌───────────────────────┐
│ [Logo]    [🌙] [Logout] │
├───────────────────────┤
│                         │
│ My Tasks                │
│ [+ Create Task]         │
│                         │
│ ┌─────────────────────┐ │
│ │ ☑ Buy groceries     │ │
│ │   Get milk, eggs... │ │
│ │          [✏️] [🗑️]  │ │
│ ├─────────────────────┤ │
│ │ ☐ Write report      │ │
│ │   Quarterly perf... │ │
│ │          [✏️] [🗑️]  │ │
│ └─────────────────────┘ │
│                         │
└───────────────────────┘
```

**States**:

1. **Loading**: Skeleton placeholder cards (pulsing animation)
   ```
   ┌─────────────────────────────┐
   │ ░░░░░░░░░░░░░░              │
   │ ░░░░░░░░░░░░░░░░░░░░        │
   ├─────────────────────────────┤
   │ ░░░░░░░░░░░                  │
   │ ░░░░░░░░░░░░░░░░░░           │
   └─────────────────────────────┘
   ```

2. **Empty**: Centered empty state
   ```
   ┌─────────────────────────────┐
   │                              │
   │      📋 (clipboard icon)     │
   │                              │
   │   No tasks yet. Create your  │
   │   first task to get started. │
   │                              │
   └─────────────────────────────┘
   ```

3. **Error**: Error message with retry
   ```
   ┌─────────────────────────────┐
   │                              │
   │   Unable to load tasks.      │
   │   Please check your          │
   │   connection and try again.  │
   │                              │
   │        [Retry Button]        │
   │                              │
   └─────────────────────────────┘
   ```

4. **Task list**: Normal rendering (shown in desktop/mobile layouts above)

---

### 404 Page

**File**: `app/not-found.tsx`
**Type**: Server Component

```
┌─────────────────────────────────────┐
│           (centered content)         │
│                                      │
│            404                        │
│                                      │
│         Page not found.              │
│                                      │
│     [Go to Dashboard →]             │
│                                      │
└─────────────────────────────────────┘
```

---

### Error Boundary

**File**: `app/(dashboard)/error.tsx`
**Type**: Client Component (`'use client'` — required by Next.js)

```
┌─────────────────────────────────────┐
│           (centered content)         │
│                                      │
│   Something went wrong.             │
│                                      │
│     [Try Again Button]              │
│                                      │
└─────────────────────────────────────┘
```

**Behavior**: Catches unhandled errors in dashboard route group. "Try Again" calls `reset()` to re-render the segment.

## Modal Overlays

All modals render via Radix Portal (outside the component tree, appended to `<body>`).

### Create Task Modal
```
┌──── Overlay (bg-black/50) ────────────────┐
│                                             │
│  ┌─────────────────────────────────┐       │
│  │  Create Task                [✕]  │       │
│  │                                  │       │
│  │  Title *                         │       │
│  │  [____________________________]  │       │
│  │                                  │       │
│  │  Description                     │       │
│  │  [____________________________]  │       │
│  │  [____________________________]  │       │
│  │  [____________________________]  │       │
│  │                                  │       │
│  │       [Cancel]  [Create Task]    │       │
│  └─────────────────────────────────┘       │
│                                             │
└─────────────────────────────────────────────┘
```

### Edit Task Modal
Same layout as Create, pre-filled with current values. Title: "Edit Task". Button: "Save Changes".

### Delete Confirmation Modal
```
┌──── Overlay (bg-black/50) ────────────────┐
│                                             │
│  ┌─────────────────────────────────┐       │
│  │  Delete Task                     │       │
│  │                                  │       │
│  │  Are you sure you want to        │       │
│  │  delete this task? This action   │       │
│  │  cannot be undone.               │       │
│  │                                  │       │
│  │       [Cancel]  [Delete]         │       │
│  └─────────────────────────────────┘       │
│                                             │
└─────────────────────────────────────────────┘
```

Delete button styled in destructive red.

## Responsive Breakpoints

| Breakpoint | Viewport | Layout Changes |
|---|---|---|
| Mobile | < 768px | Single column. Nav simplified. Task actions stack below content. Full-width cards. |
| Tablet | 768px - 1024px | Single column with wider margins. Nav full width. Cards with inline actions. |
| Desktop | > 1024px | Centered max-width container (768px). Full nav with email display. |

## Focus Management Summary

| Trigger Action | Focus On Open | Focus On Close |
|---|---|---|
| Click "Create Task" button | First input in create modal (title) | "Create Task" button |
| Click edit button on task | First input in edit modal (title) | Edit button of that task |
| Click delete button on task | Cancel button in delete modal | Nearest task's delete button (or "Create Task" if none remain) |
| 401 redirect to /login | Email input on login form | N/A |
