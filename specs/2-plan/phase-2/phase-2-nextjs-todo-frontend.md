# Implementation Plan: Next.js Todo Frontend

**Branch**: `006-nextjs-todo-frontend` | **Date**: 2026-02-13 | **Spec**: @specs/1-specify/phase-2/feature-02-nextjs-todo-frontend.md
**Input**: Feature specification for a responsive, authenticated Todo frontend using Next.js App Router and httpOnly cookie-based authentication

## Summary

Build a responsive Next.js 16+ frontend (App Router) that provides authenticated task management by integrating with the existing FastAPI backend. Authentication uses httpOnly cookies set by the backend — the frontend never handles raw JWT tokens. All task mutations use optimistic updates with rollback on failure. The UI supports dark/light mode with persistent preference and meets WCAG 2.1 Level AA accessibility requirements.

## Technical Context

**Language/Version**: TypeScript 5.x (strict mode), Node.js 22+
**Primary Dependencies**: Next.js 16+ (App Router), TanStack Query v5, Radix UI Dialog, react-hook-form v7, Zod v4, Sonner, next-themes
**Storage**: N/A (frontend — all persistence via backend API)
**Testing**: Vitest + React Testing Library (unit/component), Playwright (E2E)
**Target Platform**: Modern browsers (Chrome, Firefox, Safari, Edge — latest 2 major versions)
**Project Type**: Web frontend (part of monorepo)
**Performance Goals**: FCP < 1.5s, JS bundle < 250KB gzipped, UI updates < 2s, toggle response < 500ms
**Constraints**: 50 concurrent users, WCAG 2.1 AA, 15-minute JWT expiration (no refresh), Tailwind CSS only
**Scale/Scope**: 4 routes, 6 user stories, ~15 components, 60% test coverage target

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Constitutional Requirement | Status | Evidence |
|---|---|---|
| SDD Loop (Specify → Plan → Tasks → Implement) | PASS | Spec complete at @specs/1-specify/phase-2/feature-02-nextjs-todo-frontend.md, this plan is Phase 2 |
| Mandatory monorepo structure | PASS | Frontend code goes in `frontend/` directory per constitution |
| `frontend/CLAUDE.md` required for Phase II+ | PASS | Listed as deliverable in spec |
| Technology stack: Next.js 16+ (App Router only) | PASS | Using Next.js 16 App Router |
| TypeScript strict mode | PASS | `strict: true` in tsconfig.json |
| Tailwind CSS only for styling | PASS | Tailwind v4, no other CSS framework |
| Server components by default, client for interactivity | PASS | Architecture uses RSC for layouts/pages, client for interactive widgets |
| API calls centralized in `/lib/api.ts` | PASS | Centralized `apiClient` in `src/lib/api-client.ts` |
| Error boundaries for async components | PASS | error.tsx at route group level |
| Task traceability (every code file references task ID) | PASS | Will be enforced during implementation |
| 60% test coverage for Phase II | PASS | Vitest + RTL targeting 60% business logic coverage |
| No secrets committed to Git | PASS | `.env.example` only, `.env` in .gitignore |
| Stateless services | PASS | Frontend is stateless; session state from cookie + backend |
| User isolation | PASS | All task API calls scoped to authenticated user's ID |
| WCAG 2.1 AA accessibility | PASS | Radix UI primitives, focus management, color contrast enforcement |
| Authentication library: Better Auth | ⚠️ WAIVED | Constitution §2 mandates "Better Auth with JWT." Backend (branch `006-nextjs-todo-frontend`) was implemented with direct FastAPI custom JWT before this frontend feature was planned. Using httpOnly cookie + `GET /api/auth/me` instead. Formal amendment pending in `constitution.md`. |
| Test framework: Jest | ⚠️ WAIVED | Constitution §Testing mandates Jest for JavaScript. Vitest used instead per ADR-005 (4× faster, native ESM, Next.js 16 official testing guide). Formal amendment pending. |

**Gate Result: PASS with 2 documented waivers (see rows above). Waivers reflect pre-existing backend decisions, not new violations.**

## Project Structure

### Documentation (this feature)

```text
specs/2-plan/phase-2/
├── phase-2-nextjs-todo-frontend.md     # This file
├── research-frontend.md                # Phase 0: Technology research
├── data-model-frontend.md              # Phase 1: Frontend data model
├── quickstart-frontend.md              # Phase 1: Developer quickstart
├── api-specs/
│   └── frontend-integration.md         # Phase 1: API integration contract
└── ui-design/
    ├── components.md                    # Component architecture
    └── pages.md                         # Page/route architecture
```

### Source Code (repository root)

```text
frontend/
├── CLAUDE.md                     # Frontend-specific Claude instructions
├── package.json
├── next.config.ts
├── tsconfig.json
├── vitest.config.ts
├── playwright.config.ts
├── .env.example
├── tailwind.css                  # Tailwind v4 CSS-first config
├── public/
│   └── (static assets)
├── src/
│   ├── app/
│   │   ├── layout.tsx            # Root layout: ThemeProvider, QueryProvider, Toaster
│   │   ├── not-found.tsx         # 404 page
│   │   ├── proxy.ts              # Route-level auth guard (cookie-presence check)
│   │   ├── (auth)/               # Route group: unauthenticated pages
│   │   │   ├── layout.tsx        # Minimal layout (no nav)
│   │   │   ├── login/
│   │   │   │   └── page.tsx      # Login page
│   │   │   └── register/
│   │   │       └── page.tsx      # Registration page
│   │   └── (dashboard)/          # Route group: authenticated pages
│   │       ├── layout.tsx        # Dashboard layout RSC: fetches /api/auth/me, renders <NavBar />
│   │       ├── error.tsx         # Error boundary
│   │       └── dashboard/
│   │           ├── page.tsx      # Task list page (Server Component shell)
│   │           └── loading.tsx   # Loading skeleton
│   ├── components/
│   │   ├── ui/                   # Primitive UI components
│   │   │   ├── Button.tsx
│   │   │   ├── Input.tsx
│   │   │   ├── Modal.tsx         # Radix Dialog wrapper
│   │   │   ├── Toast.tsx         # Sonner Toaster config
│   │   │   ├── ThemeToggle.tsx
│   │   │   └── NavBar.tsx        # Client component: user email + logout + ThemeToggle
│   │   ├── auth/
│   │   │   ├── LoginForm.tsx     # Client component
│   │   │   └── RegisterForm.tsx  # Client component
│   │   └── tasks/
│   │       ├── TaskList.tsx      # Client component: TanStack Query
│   │       ├── TaskItem.tsx      # Client component: toggle, edit, delete
│   │       ├── NewTaskButton.tsx     # 'use client': owns modal open state, renders Create Task button
│   │       ├── TaskCreateModal.tsx
│   │       ├── TaskEditModal.tsx
│   │       ├── TaskDeleteModal.tsx
│   │       └── EmptyState.tsx
│   ├── lib/
│   │   ├── api-client.ts        # Centralized fetch wrapper (FR-018)
│   │   ├── query-client.ts      # TanStack Query client config
│   │   └── validations.ts       # Zod schemas for forms
│   ├── hooks/
│   │   ├── use-tasks.ts          # TanStack Query hooks for task CRUD
│   │   └── use-auth.ts           # Auth actions (login, register, logout)
│   ├── providers/
│   │   ├── QueryProvider.tsx     # TanStack QueryClientProvider
│   │   └── UserProvider.tsx      # User context from /api/auth/me
│   └── types/
│       └── index.ts              # Shared TypeScript types
├── e2e/
│   ├── auth.spec.ts              # User Story 1 acceptance tests
│   ├── view-tasks.spec.ts        # User Story 2 acceptance tests
│   ├── create-task.spec.ts       # User Story 3 acceptance tests
│   ├── edit-task.spec.ts         # User Story 4 acceptance tests
│   ├── complete-delete.spec.ts   # User Story 5 acceptance tests
│   └── theme-responsive.spec.ts  # User Story 6 acceptance tests
└── src/__tests__/
    ├── unit/
    │   ├── api-client.test.ts
    │   └── validations.test.ts
    ├── components/
    │   ├── TaskList.test.tsx
    │   ├── TaskItem.test.tsx
    │   ├── LoginForm.test.tsx
    │   └── Modal.test.tsx
    └── hooks/
        ├── use-tasks.test.ts
        └── use-auth.test.ts
```

**Structure Decision**: Web application option — frontend code in the constitutional `frontend/` directory. Uses Next.js 16 App Router with route groups to separate auth and dashboard layouts. Feature-based component organization under `components/` (auth, tasks, ui).

## Architecture Overview

### Component Dependency Graph

```
                        ┌────────────────────┐
                        │   Root Layout      │
                        │  (ThemeProvider,   │
                        │   QueryProvider,   │
                        │   Toaster)         │
                        └────────┬───────────┘
                                 │
                    ┌────────────┼────────────┐
                    │                         │
           ┌────────▼──────┐        ┌────────▼──────┐
           │  (auth) Group │        │(dashboard) Grp│
           │  layout.tsx   │        │  layout.tsx   │
           └───┬───────┬───┘        │ (fetches /me) │
               │       │           └───────┬───────┘
        ┌──────▼┐  ┌───▼────┐             │
        │ Login │  │Register│      ┌──────▼──────┐
        │ Page  │  │ Page   │      │  Dashboard  │
        └───┬───┘  └───┬────┘      │    Page     │
            │          │           └──────┬──────┘
     ┌──────▼┐  ┌──────▼────┐            │
     │Login  │  │Register   │     ┌──────▼──────┐
     │Form   │  │Form       │     │  TaskList   │ ◄── useTasks() hook
     └───────┘  └───────────┘     └──┬──┬──┬────┘     (TanStack Query)
                                     │  │  │
                          ┌──────────┘  │  └─────────┐
                          │             │             │
                   ┌──────▼───┐  ┌──────▼───┐  ┌─────▼──────┐
                   │ TaskItem │  │EmptyState│  │CreateModal │
                   │(toggle,  │  └──────────┘  └────────────┘
                   │edit,del) │
                   └──┬───┬──┘
                      │   │
              ┌───────▼┐ ┌▼──────────┐
              │EditModal│ │DeleteModal│
              └────────┘ └───────────┘
```

### Data Flow Architecture

```
  Browser                    Next.js Server              FastAPI Backend
  ───────                    ──────────────              ──────────────
    │                              │                            │
    │  1. Navigate to /dashboard   │                            │
    │─────────────────────────────►│                            │
    │                              │  2. proxy.ts: cookie exists? │
    │                              │  3. Layout RSC: GET /api/auth/me
    │                              │───────────────────────────►│
    │                              │  4. { id, email }          │
    │                              │◄───────────────────────────│
    │  5. Hydrated page + user ctx │                            │
    │◄─────────────────────────────│                            │
    │                              │                            │
    │  6. Client: TanStack Query                                │
    │     GET /api/{userId}/tasks  │                            │
    │──────────────────────────────┼───────────────────────────►│
    │  7. [TaskResponse[]]         │                            │
    │◄─────────────────────────────┼────────────────────────────│
    │                              │                            │
    │  8. User toggles task        │                            │
    │  9. Optimistic UI update     │                            │
    │  10. PATCH /api/{id}/tasks/{tid}/complete                 │
    │──────────────────────────────┼───────────────────────────►│
    │  11a. 200 OK → cache sync    │                            │
    │  11b. Error → rollback + toast                            │
    │◄─────────────────────────────┼────────────────────────────│
```

### Authentication Flow

```
  Login/Register Flow:
  ┌──────────┐    POST /api/auth/login     ┌──────────┐
  │  Login   │ ──────────────────────────► │  FastAPI  │
  │  Form    │   credentials: 'include'    │  Backend  │
  │ (Client) │ ◄────────────────────────── │           │
  └──────────┘   Set-Cookie: access_token  └──────────┘
       │           (httpOnly, Secure, Lax)
       │
       │  router.push('/dashboard')
       ▼
  ┌──────────┐   cookies().get('access_token')  ┌──────────┐
  │Dashboard │ ──────────────────────────────── │  FastAPI  │
  │ Layout   │   GET /api/auth/me               │  Backend  │
  │  (RSC)   │ ◄──────────────────────────────  │           │
  └──────────┘   { id, email } → UserProvider   └──────────┘

  Session Expiry Flow:
  ┌──────────┐   Any API call → 401         ┌──────────┐
  │  Client  │ ◄─────────────────────────── │  FastAPI  │
  │Component │   QueryCache.onError:        │  Backend  │
  └──────────┘   redirect to /login?        └──────────┘
       │         reason=session_expired
       ▼
  ┌──────────┐
  │  Login   │  "Your session has expired.
  │  Page    │   Please log in again."
  └──────────┘
```

## Technology Decisions

| Decision Area | Choice | Rationale |
|---|---|---|
| **Framework** | Next.js 16+ App Router | Constitution mandate. Server Components by default, `proxy.ts` for route guards |
| **State Management** | TanStack Query v5 | Built-in optimistic updates + rollback. All app state is server state |
| **User Identity** | React Context (UserProvider) | Thin bridge from RSC `/api/auth/me` call to client components |
| **Forms** | react-hook-form v7 + Zod v4 | Uncontrolled inputs (fast), schema validation, <200ms error display |
| **Modals** | Radix UI Dialog | Accessible focus trap, escape-close, screen reader announcement — WCAG 2.1 AA |
| **Toasts** | Sonner | ~2KB, callable outside React, configurable duration + dismiss |
| **Theming** | Tailwind CSS v4 + next-themes | CSS-first config, `localStorage` persistence, hydration-safe |
| **Testing** | Vitest + RTL + Playwright | Vitest 4x faster than Jest. Playwright for cross-browser E2E |
| **API Client** | Custom fetch wrapper | `credentials: 'include'`, error catalog mapping, 15s timeout |
| **Auth Transport** | httpOnly cookie (backend-set) | XSS-safe. Frontend never handles JWT. Browser sends cookie automatically |

## Implementation Phases

### Phase A: Project Scaffolding & Core Infrastructure (Foundation)

**Goal**: Working Next.js 16 project with routing, theming, and API client layer.

**Components**:
1. **Next.js 16 project initialization** — `create-next-app` with TypeScript strict, Tailwind v4, App Router
2. **Root layout** — HTML shell, ThemeProvider (next-themes), QueryClientProvider, Sonner Toaster. MUST include a `<noscript>` element inside `<body>` with the message "This application requires JavaScript to run." to satisfy the spec edge case for no-JS browsers (no additional component needed — inline in `app/layout.tsx`).
3. **proxy.ts** — Cookie-presence check for `/dashboard` and redirect logic
4. **API client** (`lib/api-client.ts`) — Centralized fetch wrapper with `credentials: 'include'`, error normalization, error message catalog, and two distinct network failure cases:
   - **Timeout (>15s)**: `AbortSignal.timeout(15000)` triggers `AbortError` → display: *"The request is taking longer than expected. Please check your connection."* (spec edge case)
   - **No connection**: `fetch()` throws `TypeError` (network unreachable) → display: *"Unable to connect to the server. Please check your connection and try again."*
   These are separate error codes (`REQUEST_TIMEOUT` vs `NETWORK_ERROR`) so callers can distinguish them.
5. **TanStack Query client** (`lib/query-client.ts`) — Global error handler in `QueryCache.onError` for two cases:
   - **401**: Redirect to `/login?reason=session_expired` (session expired)
   - **403**: Redirect to `/dashboard` with toast *"You don't have permission to perform this action."* (spec edge case: 403 → redirect to dashboard, not just display message)
6. **Zod validation schemas** (`lib/validations.ts`) — Login, register, task create, task update
7. **TypeScript types** (`types/index.ts`) — User, Task, ApiError, TaskResponse
8. **Tailwind v4 theme** (`tailwind.css`) — Define CSS custom properties in `:root` and `.dark` selectors. All values must achieve ≥4.5:1 contrast ratio between foreground/background pairs (WCAG AA):
   ```css
   /* Light theme (:root) */
   --background: #ffffff;       /* page background */
   --foreground: #0f172a;       /* primary text */
   --muted: #f8fafc;            /* card/row background */
   --muted-foreground: #64748b; /* secondary/placeholder text */
   --primary: #3b82f6;          /* buttons, links */
   --primary-foreground: #ffffff;
   --destructive: #dc2626;      /* delete actions */
   --destructive-foreground: #ffffff;
   --border: #e2e8f0;           /* dividers, input borders */
   --ring: #3b82f6;             /* focus ring (3px offset) */

   /* Dark theme (.dark) */
   --background: #0f172a;
   --foreground: #f8fafc;
   --muted: #1e293b;
   --muted-foreground: #94a3b8;
   --primary: #60a5fa;
   --primary-foreground: #0f172a;
   --destructive: #f87171;
   --destructive-foreground: #0f172a;
   --border: #334155;
   --ring: #60a5fa;
   ```
   Contrast pairs to verify: foreground/background (≥7:1 target), muted-foreground/background (≥4.5:1), primary/primary-foreground (≥4.5:1), destructive/destructive-foreground (≥4.5:1).
9. **frontend/CLAUDE.md** — Frontend-specific patterns and conventions. Must cover:
   - **API calls**: Always use `apiClient` from `lib/api-client.ts`, never raw `fetch()` directly
   - **Server vs Client**: Default to RSC; add `'use client'` only when component uses hooks, event handlers, or browser APIs
   - **Forms**: All forms use `react-hook-form` + `zodResolver` — no `useState` for field values
   - **Mutations**: All data-modifying operations go through `use-tasks.ts` or `use-auth.ts` hooks — no direct API calls from components
   - **Modals**: All dialogs use the `Modal` wrapper (`components/ui/Modal.tsx`) — no custom dialog implementations
   - **Toasts**: Call `toast.success()` / `toast.error()` from Sonner — no custom notification state
   - **Task ID traceability**: Every file header must include `// Task: T-XXX` referencing the spec task that created it

**Dependencies**: None (first phase)

### Phase B: Authentication UI (Login, Register, Logout)

**Goal**: Users can register, log in, log out, and be redirected appropriately.

**Components**:
1. **(auth) route group layout** — Minimal layout without navigation
2. **LoginForm** — Client component, react-hook-form + Zod, calls `POST /api/auth/login`
3. **RegisterForm** — Client component, react-hook-form + Zod, calls `POST /api/auth/register`
4. **Login page** (`/login`) — Renders LoginForm, displays `?reason=session_expired` message
5. **Register page** (`/register`) — Renders RegisterForm
6. **(dashboard) route group layout** — Fetches `/api/auth/me` via RSC, wraps children in UserProvider, renders `<NavBar email={user.email} />`
7. **NavBar** (`components/ui/NavBar.tsx`) — `'use client'` component; accepts `email: string` prop; renders user email, logout button (calls `useAuth().logout()`), and ThemeToggle. Must be a client component because it calls the `useAuth` hook — cannot live directly in the RSC layout.
8. **UserProvider** — React Context providing `{ id, email }` to client components
9. **use-auth hook** — Login, register, and logout actions with error handling:
   - `login(email, password)`: POST `/api/auth/login` → on success, `router.push('/dashboard')`; on 401 show field error "Invalid email or password"
   - `register(email, password)`: POST `/api/auth/register` → on success, `router.push('/dashboard')`; on 409 show field error "An account with this email already exists"
   - `logout()`: POST `/api/auth/logout` → on success, call `queryClient.clear()` to wipe all cached task data, then `router.push('/login')`
10. **Redirect logic** — In `(auth)/layout.tsx`, check for the `access_token` cookie using `cookies()`. If the cookie is present, `redirect('/dashboard')` immediately (before rendering login/register). This prevents authenticated users from seeing the auth pages on browser back-navigation.

**Dependencies**: Phase A (API client, validation schemas, types, proxy.ts)

### Phase C: Task Management (CRUD + Optimistic Updates)

**Goal**: Full task lifecycle — view, create, edit, toggle completion, delete — all with optimistic updates.

**Components**:
1. **Dashboard page** (`/dashboard`) — Server Component shell rendering two client children: `<TaskList>` and `<NewTaskButton>`. The page itself uses no hooks and stays a pure RSC.
2. **NewTaskButton** (`components/tasks/NewTaskButton.tsx`) — `'use client'` component that owns `open`/`onOpenChange` state for `TaskCreateModal` and renders the "Create Task" `<Button>` trigger (top-right on desktop, full-width on mobile). Isolating state here prevents the page from becoming a client component.
3. **TaskList** — Client component using `useTasks()` hook (TanStack Query), handles loading/error/empty states
4. **TaskItem** — Displays a single task row:
   - **Completion checkbox**: leading element; clicking calls `toggleTask(task.id)` with optimistic update
   - **Title**: struck-through when `completed === true` (`line-through` class)
   - **Description**: clamped to 2 lines via `line-clamp-2`; full text shown in `title` attribute as tooltip for screen readers and hover overflow
   - **Edit button**: icon button (pencil icon), `aria-label="Edit task"`, opens `TaskEditModal` with this task pre-filled
   - **Delete button**: icon button (trash icon), `aria-label="Delete task"`, opens `TaskDeleteModal` for this task
   - Layout: checkbox + title/description block (flex-grow) + edit/delete buttons (flex-shrink)
5. **EmptyState** — Icon + "No tasks yet" message with prompt to create
6. **TaskCreateModal** — Radix Dialog, react-hook-form, optimistic insert at top of list
7. **TaskEditModal** — Radix Dialog, pre-filled form, optimistic update
8. **TaskDeleteModal** — Radix Dialog confirmation, optimistic removal with rollback
9. **use-tasks hook** — `useQuery` for fetch, `useMutation` for create/update/delete/toggle, all with the three-phase optimistic pattern:
   - **Fetch**: `useQuery({ queryKey: ['tasks', userId], queryFn: () => apiClient.get('/api/{userId}/tasks'), staleTime: 0 })`
   - **Create** (`useCreateTask`): `onMutate` prepends the new task object (with temporary `id: 'optimistic-${Date.now()}'`) to the front of the cached array — list is newest-first so prepend matches server order; `onSettled` invalidates `['tasks', userId]` which replaces the temp ID with the real server ID
   - **Update** (`useUpdateTask`): `onMutate` replaces the matching task in the cached array by ID
   - **Delete** (`useDeleteTask`): `onMutate` filters the task out of the cached array by ID
   - **Toggle** (`useToggleTask`): `onMutate` flips `completed` boolean on the matching task in cache
   - All four: `onError` restores the snapshot captured in `onMutate` and shows an error toast (5s, dismissible); `onSettled` invalidates the query
10. **Focus management** — Return focus to trigger element on modal close

**Dependencies**: Phase B (auth flow, UserProvider for userId)

### Phase D1: Polish & Accessibility

**Goal**: Theme toggle, responsive layout, error states, and accessibility compliance. All visual/structural work complete before testing begins.

**Components**:
1. **ThemeToggle** (`components/ui/ThemeToggle.tsx`) — Client component using `useTheme()` from next-themes; renders a button with sun icon (light mode) / moon icon (dark mode); dynamic `aria-label` reflects the mode the button will switch *to* ("Switch to dark mode" / "Switch to light mode"); rendered inside `NavBar.tsx` (the dashboard `'use client'` nav component created in Phase B)
2. **Responsive layout adjustments** — Dashboard page content max-width `768px` centered on desktop; full-width on mobile (< 640px). Task list rows stack vertically at all widths. Edit/delete buttons always visible (no hover-only reveal) to ensure touch accessibility
3. **404 page** (`not-found.tsx`) — Heading "Page not found", sub-text "The page you requested doesn't exist.", link "← Back to dashboard" (`href="/dashboard"`)
4. **Error boundary** (`error.tsx`) — Heading "Something went wrong", sub-text "An unexpected error occurred. Please try refreshing the page.", button "Refresh page" (`onClick={() => reset()}`)
5. **Loading skeleton** (`loading.tsx`) — 3 placeholder task rows rendered while `useTasks` is in loading state. Each row mirrors `TaskItem` layout: a 16px circle (checkbox placeholder) + two gray bars (title: 60% width, description: 40% width, both with `animate-pulse`). No text content — purely visual shimmer
6. **`.env.example`** — Document `NEXT_PUBLIC_API_URL=http://localhost:8000`

**Dependencies**: Phase C (all components exist to audit)

---

### Phase D2: Testing

**Goal**: 60% coverage of `src/lib/**`, `src/hooks/**`, `src/components/**`; all 6 user stories verified end-to-end across browsers.

**Components**:
1. **Unit tests** (`__tests__/unit/`) — Vitest:
   - `api-client.test.ts`: mock `fetch` to verify `REQUEST_TIMEOUT` on `AbortError`, `NETWORK_ERROR` on `TypeError`, correct error message strings, `credentials: 'include'` present on every call
   - `validations.test.ts`: valid/invalid inputs for all 4 Zod schemas (login, register, task create, task update); verify exact error messages match spec
2. **Hook tests** (`__tests__/hooks/`) — Vitest + MSW:
   - `use-auth.test.ts`: login success → redirect `/dashboard`; login 401 → field error; logout → `queryClient.clear()` + redirect `/login`
   - `use-tasks.test.ts`: fetch renders task list; create optimistically prepends + temp ID replaced on settle; toggle flips completed; delete removes item; `onError` triggers rollback
3. **Component tests** (`__tests__/components/`) — Vitest + RTL:
   - `LoginForm.test.tsx`: submits with valid data; shows field error on 401; disables submit button during loading
   - `Modal.test.tsx`: opens/closes on trigger; Escape key closes; focus returns to trigger on close
   - `TaskList.test.tsx`: renders skeleton during load; renders `EmptyState` when array is empty; renders TaskItem for each task
   - `TaskItem.test.tsx`: checkbox click calls `toggleTask`; Edit button opens edit modal; Delete button opens delete modal; `line-clamp-2` applied to description; title has `line-through` when `completed`
4. **Accessibility (axe-core)** — `@axe-core/playwright` injected in each E2E spec's `beforeEach` via `injectAxe()` + `checkA11y()`. Runs against the live rendered page in Chromium. Any axe violation fails the test. Covers both light and dark themes by toggling `ThemeToggle` within the spec.
5. **E2E tests** (`e2e/`) — Playwright (Chromium + Firefox + WebKit):
   - `auth.spec.ts` — register new user, login, logout, session expiry redirect, already-authenticated redirect
   - `view-tasks.spec.ts` — empty state, task list renders after login
   - `create-task.spec.ts` — open modal, fill form, submit, task appears at top of list optimistically
   - `edit-task.spec.ts` — open edit modal pre-filled, update, list reflects change
   - `complete-delete.spec.ts` — toggle checkbox (title struck-through), delete with confirmation
   - `theme-responsive.spec.ts` — toggle dark mode (class applied to `<html>`), responsive layout at 375px viewport

**Dependencies**: Phase D1 (all components finalized before tests are written)

## Component Dependency Matrix

| Component | Depends On | Blocks |
|---|---|---|
| API Client (`lib/api-client.ts`) | Types | All API-consuming components |
| Query Client (`lib/query-client.ts`) | API Client | All TanStack Query hooks |
| Validation Schemas (`lib/validations.ts`) | Zod | All forms |
| proxy.ts | — | Route protection |
| Root Layout | ThemeProvider, QueryProvider, Toaster | All pages |
| (auth) Layout | — | Login, Register pages |
| (dashboard) Layout | API Client, UserProvider | Dashboard page |
| UserProvider | — | TaskList, all task mutations |
| NavBar | use-auth hook | (dashboard) Layout |
| LoginForm | Validation schemas, use-auth hook | — |
| RegisterForm | Validation schemas, use-auth hook | — |
| use-auth hook | API Client | LoginForm, RegisterForm |
| use-tasks hook | API Client, Query Client, UserProvider | TaskList |
| TaskList | use-tasks hook, TaskItem, EmptyState | — |
| TaskItem | TaskEditModal, TaskDeleteModal | — |
| NewTaskButton | Button, TaskCreateModal | Dashboard page |
| TaskCreateModal | Modal (Radix), Validation schemas, use-tasks | — |
| TaskEditModal | Modal (Radix), Validation schemas, use-tasks | — |
| TaskDeleteModal | Modal (Radix), use-tasks | — |
| ThemeToggle | next-themes | — |

## Design Decisions Requiring Documentation

### ADR-001: httpOnly Cookie Authentication (No Bearer Header)

**Context**: The backend supports both Bearer token and httpOnly cookie authentication. The frontend must choose one transport mechanism.

**Decision**: Use httpOnly cookies exclusively. The frontend never handles raw JWT tokens. All API calls use `credentials: 'include'` to let the browser attach the cookie automatically.

**Consequences**:
- The frontend cannot read the JWT payload (user ID, expiration) — must call `GET /api/auth/me` instead
- Server Components must explicitly forward cookies when making server-to-server API calls via `cookies()` API
- CORS must be configured with `allow_credentials=True` and a specific origin (not `*`)
- Stronger XSS protection since tokens are never in JavaScript-accessible storage

### ADR-002: TanStack Query for All Server State

**Context**: The app needs state management with optimistic updates and rollback.

**Decision**: TanStack Query v5 manages all server state. No additional client state library (no Zustand, Redux). User identity is passed through React Context from a Server Component.

**Consequences**:
- All task data is cache-managed by TanStack Query with `['tasks', userId]` query key
- Optimistic updates use `onMutate` → snapshot → optimistic write → `onError` → rollback pattern
- Cache invalidation via `queryClient.invalidateQueries` on `onSettled`
- No global state store to debug — DevTools shows server cache state

### ADR-003: proxy.ts for Coarse Auth Guard Only

**Context**: Next.js 16 renamed middleware.ts to proxy.ts and explicitly documented it as a routing layer, not an auth enforcement layer (informed by CVE-2025-29927).

**Decision**: `proxy.ts` only checks for cookie **presence** (not validity). Real auth validation happens in the `(dashboard)/layout.tsx` Server Component by calling `GET /api/auth/me`.

**Consequences**:
- Two-layer auth: fast coarse check (proxy.ts) + real validation (layout RSC)
- Users with expired cookies get past proxy.ts but are redirected by the layout
- Secure against middleware bypass attacks since layout enforces auth independently

### ADR-004: Radix UI Primitives for Accessibility

**Context**: The spec requires WCAG 2.1 AA compliance with focus trapping, screen reader announcements, and keyboard operability for all modals.

**Decision**: Use Radix UI Dialog for all modal interactions (create, edit, delete confirmation). Unstyled primitives styled with Tailwind.

**Consequences**:
- Focus trap, escape-close, aria attributes, and portal rendering handled automatically
- Consistent behavior across all three modal types
- Additional Radix primitives available for future phases (tooltip, dropdown)

### ADR-005: Vitest Over Jest

**Context**: Need a test runner compatible with Next.js 16, TypeScript, and ES modules.

**Decision**: Vitest with React Testing Library for unit/component tests, Playwright for E2E.

**Consequences**:
- ~4x faster test execution than Jest (native ESM support, no Babel transforms)
- Compatible with Next.js 16 official testing guide
- Coverage via Vitest's V8 provider
- E2E tests exercise real browser behavior across Chrome, Firefox, Safari

## Complexity Tracking

No constitutional violations to justify. All decisions align with the technology stack and architectural patterns mandated by the constitution.

## Backend Integration Notes

The existing FastAPI backend (branch `006-nextjs-todo-frontend`) already provides all required endpoints:

| Endpoint | Status | Notes |
|---|---|---|
| `POST /api/auth/register` | Exists | Sets httpOnly cookie + JSON response |
| `POST /api/auth/login` | Exists | Sets httpOnly cookie + JSON response |
| `GET /api/auth/me` | Exists | Returns `{ id, email }` from cookie |
| `POST /api/auth/logout` | Exists | Clears httpOnly cookie |
| `GET /api/{user_id}/tasks` | Exists | Paginated, newest-first |
| `POST /api/{user_id}/tasks` | Exists | Creates task |
| `GET /api/{user_id}/tasks/{task_id}` | Exists | Get single task |
| `PUT /api/{user_id}/tasks/{task_id}` | Exists | Update task |
| `DELETE /api/{user_id}/tasks/{task_id}` | Exists | Delete task |
| `PATCH /api/{user_id}/tasks/{task_id}/complete` | Exists | Toggle completion |

The backend accepts auth from both `Authorization: Bearer` header and `access_token` httpOnly cookie (cookie-first priority per `get_current_user_id` in `utils/auth.py`). CORS is configured for `http://localhost:3000` with `allow_credentials=True`.

No backend modifications are required for the frontend feature.
