# Tasks: Next.js Todo Frontend

**Feature**: Responsive, Authenticated Todo Frontend with Next.js App Router
**Branch**: `006-nextjs-todo-frontend`
**Created**: 2026-02-14
**Spec**: @specs/1-specify/phase-2/feature-02-nextjs-todo-frontend.md
**Plan**: @specs/2-plan/phase-2/phase-2-nextjs-todo-frontend.md

## Implementation Strategy

Build a responsive Next.js 16+ frontend (App Router) that provides authenticated task management by integrating with the existing FastAPI backend. Authentication uses httpOnly cookies set by the backend. All task mutations use optimistic updates with rollback. The UI supports dark/light mode and meets WCAG 2.1 Level AA.

**MVP Scope**: User Story 1 (Registration & Login) + User Story 2 (Viewing Tasks) — delivers a working authenticated app that displays tasks.

## Dependencies

- User Story 1 (Auth) requires Foundational phase (API client, types, validation schemas, UI primitives)
- User Story 2 (View Tasks) requires User Story 1 (authentication flow, UserProvider)
- User Story 3 (Create Tasks) requires User Story 2 (TaskList component, dashboard page)
- User Story 4 (Edit Tasks) requires User Story 3 (TaskCreateModal pattern, use-tasks hook patterns)
- User Story 5 (Complete & Delete) requires User Story 2 (TaskItem component, use-tasks hook)
- User Story 6 (Theme & Responsive) can start after Foundational phase (independent of task stories)
- Testing phase requires all User Stories complete

## Parallel Execution Examples

- Types, validation schemas, Tailwind theme, and UI primitives can be written in parallel (Phase 2: T004-T006, T009-T011); T007→T008 must remain sequential
- API client fetch wrapper and error catalog can be written sequentially (Phase 2: T007 → T008)
- LoginForm and RegisterForm can be written in parallel (Phase 3: T018, T019)
- User Story 6 (Theme) can run in parallel with User Stories 3-5
- All unit test files can be written in parallel (Phase 9)
- All component test files can be written in parallel (Phase 9)

---

## Phase 1: Setup

**Purpose**: Project initialization and scaffolding

- [X] T001 Initialize Next.js 16 project in `frontend/` using `npx create-next-app@latest . --typescript --tailwind --app --src-dir --no-import-alias`
- [X] T002 Install all dependencies (runtime: `@tanstack/react-query @radix-ui/react-dialog react-hook-form @hookform/resolvers zod sonner next-themes`; dev: `vitest @vitejs/plugin-react @testing-library/react @testing-library/jest-dom @testing-library/user-event jsdom playwright @playwright/test @axe-core/playwright msw`)
- [X] T003 Create `frontend/CLAUDE.md` with convention rules per plan Phase A item 9 (apiClient usage, RSC defaults, forms, mutations, modals, toasts, task ID traceability)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented. Includes UI primitives needed by all forms.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 [P] Create TypeScript types (`User`, `Task`, `TaskCreateRequest`, `TaskUpdateRequest`, `AuthRequest`, `TokenResponse`, `ApiErrorResponse`) in `frontend/src/types/index.ts` per data-model-frontend.md
- [X] T005 [P] Create Zod validation schemas (`authSchema`, `taskCreateSchema`, `taskUpdateSchema`) with exact error messages from spec in `frontend/src/lib/validations.ts` per data-model-frontend.md
- [X] T006 [P] Create Tailwind v4 theme in `frontend/tailwind.css` with 10 CSS custom properties for light/dark themes per plan Phase A item 8 color values, and create `frontend/.env.example` documenting `NEXT_PUBLIC_API_URL=http://localhost:8000`
- [X] T007 Implement centralized API fetch wrapper in `frontend/src/lib/api-client.ts` with `credentials: 'include'`, `AbortSignal.timeout(15000)`, base URL from `NEXT_PUBLIC_API_URL`, typed GET/POST/PUT/PATCH/DELETE methods, separate `AbortError` → `REQUEST_TIMEOUT` and `TypeError` → `NETWORK_ERROR` catch branches
- [X] T008 Add error code catalog to `frontend/src/lib/api-client.ts` mapping all 9 backend error codes (INVALID_CREDENTIALS, EMAIL_ALREADY_EXISTS, UNAUTHORIZED_ACCESS, USER_NOT_FOUND, TASK_NOT_FOUND, 500, REQUEST_TIMEOUT, NETWORK_ERROR, session expired 401) to user-facing messages from frontend-integration.md
- [X] T009 [P] Create `Button` primitive component in `frontend/src/components/ui/Button.tsx` with `variant` (primary | destructive | ghost), `size` (sm | md), `disabled`, `loading` (spinner), `aria-disabled` when loading
- [X] T010 [P] Create `Input` primitive component in `frontend/src/components/ui/Input.tsx` with `label`, `error`, `id`, `<label htmlFor>`, `aria-describedby` for error, `aria-invalid` when error present, react-hook-form `register()` compatible
- [X] T011 [P] Create `Modal` wrapper component in `frontend/src/components/ui/Modal.tsx` wrapping Radix UI Dialog (Root, Portal, Overlay bg-black/50, Content centered with max-width), props: `open`, `onOpenChange`, `title`, `description?`, `children`
- [X] T012 Configure TanStack Query client in `frontend/src/lib/query-client.ts` with `QueryCache.onError` global handler for 401 → redirect `/login?reason=session_expired` and 403 → toast + redirect `/dashboard`
- [X] T013 [P] Create QueryProvider client component in `frontend/src/providers/QueryProvider.tsx` wrapping children in `QueryClientProvider`
- [X] T014 Create root layout in `frontend/src/app/layout.tsx` with ThemeProvider (next-themes), QueryProvider, Sonner Toaster, and `<noscript>` fallback message "This application requires JavaScript to run."
- [X] T015 [P] Implement `frontend/src/app/proxy.ts` cookie-presence check: redirect unauthenticated requests from `/dashboard` to `/login`, redirect `/` to `/dashboard` (if cookie) or `/login` (if no cookie)
- [X] T016 [P] Create root page `frontend/src/app/page.tsx` as redirect-only Server Component: check for `access_token` cookie via `cookies()`, redirect to `/dashboard` if present, redirect to `/login` if absent

**Checkpoint**: Foundation ready — UI primitives, API client, auth guard, and providers all exist. User story implementation can now begin.

---

## Phase 3: User Story 1 — User Registration and Login (Priority: P1) 🎯 MVP

**Goal**: Users can register, log in, log out, and be redirected appropriately between auth and dashboard pages.

**Independent Test**: Register a new account, log out, log back in. Verify authentication flow works end-to-end with the backend.

### Implementation for User Story 1

- [X] T017 [US1] Implement `useAuth` hook in `frontend/src/hooks/use-auth.ts` with `login()` → POST `/api/auth/login` → `router.push('/dashboard')` or 401 error; `register()` → POST `/api/auth/register` → `router.push('/dashboard')` or 409 error; `logout()` → POST `/api/auth/logout` → `queryClient.clear()` → `router.push('/login')`
- [X] T018 [P] [US1] Create `LoginForm` client component in `frontend/src/components/auth/LoginForm.tsx` with react-hook-form + zodResolver(authSchema), `<Input>` for email + password, `<Button>` with loading state, error display, `?reason=session_expired` banner
- [X] T019 [P] [US1] Create `RegisterForm` client component in `frontend/src/components/auth/RegisterForm.tsx` with react-hook-form + zodResolver(authSchema), `<Input>` for email + password, `<Button>` with loading state, error display, "Already have an account?" link
- [X] T020 [US1] Create `(auth)` route group layout in `frontend/src/app/(auth)/layout.tsx` with minimal centered card (max-width 400px), no nav bar, cookie check via `cookies()` → `redirect('/dashboard')` if authenticated
- [X] T021 [P] [US1] Create login page in `frontend/src/app/(auth)/login/page.tsx` rendering `<LoginForm />` and reading `?reason` search param for session expiry message
- [X] T022 [P] [US1] Create register page in `frontend/src/app/(auth)/register/page.tsx` rendering `<RegisterForm />`
- [X] T023 [US1] Create UserProvider context in `frontend/src/providers/UserProvider.tsx` accepting `user: { id, email }` prop and exposing `useUser()` hook
- [X] T024 [US1] Create `(dashboard)` route group layout RSC in `frontend/src/app/(dashboard)/layout.tsx` that fetches `GET /api/auth/me` with forwarded cookies, redirects to `/login` on 401, wraps children in `<UserProvider user={user}>`
- [X] T025 [US1] Create `NavBar` client component in `frontend/src/components/ui/NavBar.tsx` (`'use client'`) accepting `email: string` prop, rendering user email display and a logout button that calls `useAuth().logout()`; then import `<NavBar email={user.email} />` into the RSC `(dashboard)/layout.tsx` (hooks cannot be called in Server Components — NavBar must be a separate client component)

**Checkpoint**: User Story 1 fully functional — register, login, logout, and redirect flows work end-to-end

---

## Phase 4: User Story 2 — Viewing and Managing Tasks (Priority: P1) 🎯 MVP

**Goal**: Authenticated users see all their tasks displayed newest-first with loading, empty, and error states.

**Independent Test**: Log in, verify tasks from backend are displayed correctly, verify empty state when no tasks exist, verify loading skeleton appears.

### Implementation for User Story 2

- [X] T026 [US2] Implement `useTasks` hook in `frontend/src/hooks/use-tasks.ts` with `useQuery({ queryKey: ['tasks', userId], queryFn })` reading userId from UserContext, `staleTime: 0`
- [X] T027 [P] [US2] Create `EmptyState` component in `frontend/src/components/tasks/EmptyState.tsx` with clipboard icon and message "No tasks yet. Create your first task to get started."
- [X] T028 [US2] Create `TaskItem` client component in `frontend/src/components/tasks/TaskItem.tsx` with completion checkbox, title (line-through when completed, opacity-60), description (line-clamp-2, title attribute), edit button (pencil, aria-label), delete button (trash, aria-label), flex layout
- [X] T029 [US2] Create `TaskList` client component in `frontend/src/components/tasks/TaskList.tsx` using `useTasks()` hook, rendering loading skeleton (3 shimmer rows), error state with retry button, `<EmptyState />` when empty, list of `<TaskItem />` components in `<ul role="list">`
- [X] T030 [US2] Create dashboard page in `frontend/src/app/(dashboard)/dashboard/page.tsx` as Server Component shell rendering `<TaskList />`

**Checkpoint**: User Stories 1 & 2 complete — authenticated users can view their task list (MVP delivered)

---

## Phase 5: User Story 3 — Creating New Tasks (Priority: P2)

**Goal**: Users can create tasks via a modal dialog with optimistic UI insert.

**Independent Test**: Log in, click "Create Task", fill in title and description, submit. Verify task appears at top of list immediately.

### Implementation for User Story 3

- [X] T031 [US3] Implement `useCreateTask` mutation hook in `frontend/src/hooks/use-tasks.ts` with optimistic prepend (temp id `optimistic-${Date.now()}`), `onError` rollback + error toast 5s, `onSettled` invalidate, success toast "Task created" 3s
- [X] T032 [US3] Create `TaskCreateModal` in `frontend/src/components/tasks/TaskCreateModal.tsx` with react-hook-form + zodResolver(taskCreateSchema), title + description `<Input>` fields, "Cancel" and "Create Task" `<Button>` components, error display inside modal on backend failure, submit disabled during loading
- [X] T033 [US3] Create `NewTaskButton` client component in `frontend/src/components/tasks/NewTaskButton.tsx` (`'use client'`) that manages `open`/`onOpenChange` state and renders the "Create Task" `<Button>` (top-right desktop, full-width mobile) with `<TaskCreateModal open={open} onOpenChange={setOpen} />`; then import `<NewTaskButton />` into the Server Component dashboard page (`page.tsx`) alongside `<TaskList />` — state must live in a client component, not the RSC page

**Checkpoint**: User Story 3 complete — users can create tasks with optimistic insert

---

## Phase 6: User Story 4 — Editing Existing Tasks (Priority: P2)

**Goal**: Users can edit task title and description via a pre-filled modal with optimistic update.

**Independent Test**: Log in, click edit on a task, change title, save. Verify changes appear immediately.

### Implementation for User Story 4

- [X] T034 [US4] Implement `useUpdateTask` mutation hook in `frontend/src/hooks/use-tasks.ts` with optimistic replacement by ID, `onError` rollback + error toast 5s, `onSettled` invalidate, success toast "Task updated" 3s, 404 handling ("This task no longer exists")
- [X] T035 [US4] Create `TaskEditModal` in `frontend/src/components/tasks/TaskEditModal.tsx` with react-hook-form pre-filled from `task` prop, same validation as create, 404 error message with close button, submit disabled during loading
- [X] T036 [US4] Wire edit button in `TaskItem.tsx` to open `<TaskEditModal />` with the selected task, manage `open` state per task, focus returns to edit button on close

**Checkpoint**: User Story 4 complete — users can edit tasks with optimistic update

---

## Phase 7: User Story 5 — Completing and Deleting Tasks (Priority: P2)

**Goal**: Users can toggle task completion and delete tasks with confirmation modal and optimistic UI.

**Independent Test**: Log in, toggle a task's checkbox (verify strikethrough), delete a task via confirmation modal (verify removal).

### Implementation for User Story 5

- [X] T037 [US5] Implement `useToggleTask` mutation hook in `frontend/src/hooks/use-tasks.ts` with optimistic `is_completed` flip, `onError` rollback + error toast 5s, `onSettled` invalidate, no success toast
- [X] T038 [US5] Implement `useDeleteTask` mutation hook in `frontend/src/hooks/use-tasks.ts` with optimistic filter-out by ID, `onError` rollback (reinsert at original index) + error toast 5s, `onSettled` invalidate, success toast "Task deleted" 3s
- [X] T039 [US5] Create `TaskDeleteModal` in `frontend/src/components/tasks/TaskDeleteModal.tsx` with confirmation message "Are you sure you want to delete this task? This action cannot be undone.", "Cancel" and "Delete" (destructive red) `<Button>` components, focus returns to nearest task's delete button (or "New Task" if none remain)
- [X] T040 [US5] Wire completion checkbox in `TaskItem.tsx` to call `useToggleTask` with optimistic UI update
- [X] T041 [US5] Wire delete button in `TaskItem.tsx` to open `<TaskDeleteModal />` with selected task, manage `open` state per task

**Checkpoint**: User Story 5 complete — full task lifecycle works (create, view, edit, toggle, delete)

---

## Phase 8: User Story 6 — Dark/Light Mode and Responsive Layout (Priority: P3)

**Goal**: Theme toggle with persistent preference, responsive layout across mobile/tablet/desktop.

**Independent Test**: Toggle theme switch, verify visual change persists after refresh. Resize browser to verify layout at 320px, 768px, and 1024px.

### Implementation for User Story 6

- [X] T042 [US6] Create `ThemeToggle` in `frontend/src/components/ui/ThemeToggle.tsx` using `useTheme()` from next-themes, sun/moon icon button, dynamic `aria-label` that reflects the mode the button will switch *to*: `"Switch to dark mode"` when currently light, `"Switch to light mode"` when currently dark (per plan Phase D1 and WCAG 2.4.6)
- [X] T043 [US6] Add `<ThemeToggle />` to `frontend/src/components/ui/NavBar.tsx` next to user email and logout button (NavBar is the client component created in T025; ThemeToggle must live in a client component since it uses `useTheme()`)
- [X] T044 [US6] Apply responsive layout adjustments: dashboard content max-width 768px centered on desktop, full-width on mobile (<640px), edit/delete buttons always visible (no hover-only), auth pages max-width 400px centered

**Checkpoint**: User Story 6 complete — theme toggle and responsive layout work

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Error pages, loading states, testing infrastructure, and full test suite

### Error & Loading States

- [X] T045 Create 404 page in `frontend/src/app/not-found.tsx` with "Page not found" heading, "The page you requested doesn't exist." sub-text, "← Back to dashboard" link
- [X] T046 [P] Create error boundary in `frontend/src/app/(dashboard)/error.tsx` as client component with "Something went wrong" heading, sub-text "An unexpected error occurred. Please try refreshing the page.", and "Refresh page" button calling `reset()` per plan Phase D1 item 4
- [X] T047 [P] Create loading skeleton in `frontend/src/app/(dashboard)/dashboard/loading.tsx` with 3 placeholder TaskItem rows (16px circle + two gray bars at 60%/40% width, `animate-pulse`). Note: this is complementary to the skeleton in T029 — `loading.tsx` covers the Next.js RSC hydration phase (~50-150ms); `TaskList`'s inline skeleton covers the TanStack Query fetch latency (~300ms+). Both render, sequentially, and together eliminate all visible flashes of unstyled content.

### Testing Setup

- [X] T048 Configure Vitest in `frontend/vitest.config.ts` with jsdom environment, V8 coverage provider, 60% threshold, path aliases, setup file at `src/__tests__/setup.ts`
- [X] T049 Create test setup file `frontend/src/__tests__/setup.ts` with `@testing-library/jest-dom` import and MSW server setup (`beforeAll` start, `afterEach` reset, `afterAll` close)
- [X] T050 [P] Configure Playwright in `frontend/playwright.config.ts` for Chromium + Firefox + WebKit, base URL `http://localhost:3000`, webServer for dev server

### Unit Tests

- [X] T051 [P] Write unit tests for API client in `frontend/src/__tests__/unit/api-client.test.ts`: `REQUEST_TIMEOUT` on AbortError, `NETWORK_ERROR` on TypeError, error message catalog, `credentials: 'include'` on every call
- [X] T052 [P] Write unit tests for Zod schemas in `frontend/src/__tests__/unit/validations.test.ts`: valid/invalid inputs for all 3 schema definitions (authSchema, taskCreateSchema, taskUpdateSchema — noting taskUpdateSchema re-uses taskCreateSchema), exact error messages match spec

### Hook Tests

- [X] T053 [P] Write hook tests for `useAuth` in `frontend/src/__tests__/hooks/use-auth.test.ts` with MSW: login success → redirect, login 401 → error, logout → queryClient.clear() + redirect
- [X] T054 [P] Write hook tests for `useTasks` in `frontend/src/__tests__/hooks/use-tasks.test.ts` with MSW: fetch renders list, create prepends with temp ID, toggle flips completed, delete removes, onError triggers rollback

### Component Tests

- [X] T055 [P] Write component test for LoginForm in `frontend/src/__tests__/components/LoginForm.test.tsx`: valid submit, 401 error display, submit button disabled during loading
- [X] T056 [P] Write component test for Modal in `frontend/src/__tests__/components/Modal.test.tsx`: opens/closes, Escape key closes, focus returns to trigger
- [X] T057 [P] Write component test for TaskList in `frontend/src/__tests__/components/TaskList.test.tsx`: skeleton during load, EmptyState when empty, renders TaskItem per task
- [X] T058 [P] Write component test for TaskItem in `frontend/src/__tests__/components/TaskItem.test.tsx`: checkbox calls toggleTask, Edit/Delete buttons open modals, line-clamp-2 on description, line-through when completed

### E2E Tests

- [X] T059 Write E2E test for auth flow in `frontend/e2e/auth.spec.ts` with axe-core: register, login, logout, session expiry redirect, already-authenticated redirect
- [X] T060 [P] Write E2E test for viewing tasks in `frontend/e2e/view-tasks.spec.ts` with axe-core: empty state, task list renders after login
- [X] T061 [P] Write E2E test for creating tasks in `frontend/e2e/create-task.spec.ts` with axe-core: open modal, fill form, submit, task at top
- [X] T062 [P] Write E2E test for editing tasks in `frontend/e2e/edit-task.spec.ts` with axe-core: pre-filled modal, update, list reflects change
- [X] T063 [P] Write E2E test for complete/delete in `frontend/e2e/complete-delete.spec.ts` with axe-core: toggle checkbox (strikethrough), delete with confirmation
- [X] T064 [P] Write E2E test for theme/responsive in `frontend/e2e/theme-responsive.spec.ts` with axe-core: toggle dark mode, check class on `<html>`, verify layout at 375px viewport

### Final Validation

- [X] T065 Run full Vitest suite with coverage, verify ≥60% of `src/lib/**`, `src/hooks/**`, `src/components/**`
- [X] T066 Run full Playwright suite across Chromium + Firefox + WebKit, verify all 6 E2E specs pass
- [X] T067 Run quickstart.md validation: fresh clone → install → dev server → register → create task → verify flow

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup — BLOCKS all user stories
- **US1 Auth (Phase 3)**: Depends on Phase 2 (API client, types, schemas, Button, Input, Modal)
- **US2 View Tasks (Phase 4)**: Depends on Phase 3 (needs auth flow + UserProvider)
- **US3 Create Tasks (Phase 5)**: Depends on Phase 4 (needs TaskList, dashboard page)
- **US4 Edit Tasks (Phase 6)**: Hard dependency on Phase 4 only (TaskItem for T036, use-tasks.ts for T034). Soft/pattern dependency on Phase 5 — sequenced after US3 to establish consistent modal/mutation patterns before replicating them, and to avoid write conflicts on `use-tasks.ts`.
- **US5 Complete & Delete (Phase 7)**: Depends on Phase 4 (needs TaskItem, use-tasks hook). Must remain sequential after US3/US4 — all three phases write to `use-tasks.ts` and cannot run in parallel without merge conflicts.
- **US6 Theme (Phase 8)**: Depends on Phase 2 only — CAN run in parallel with US3-US5
- **Polish & Testing (Phase 9)**: Depends on all User Stories

### Parallel Opportunities

Within each phase, tasks marked `[P]` can run in parallel:
- Phase 2: T004 + T005 + T006 + T009 + T010 + T011 + T015 + T016 in parallel (independent files, no dependency on API client); then T007 → T008 sequential
- Phase 3: T018 + T019 in parallel (forms); T021 + T022 in parallel (pages)
- Phase 7: T037 + T038 in parallel (hooks); T040 + T041 in parallel (wiring)
- Phase 8: Independent of Phases 5-7 — can run in parallel
- Phase 9: All unit tests in parallel (T051-T052); all hook tests in parallel (T053-T054); all component tests in parallel (T055-T058); all E2E tests except T059 in parallel (T060-T064)

### User Story Independence

| Story | Can Start After | Independent Test |
|-------|----------------|------------------|
| US1 (Auth) | Phase 2 | Register → logout → login |
| US2 (View) | US1 | Login → see tasks or empty state |
| US3 (Create) | US2 | Login → create task → appears at top |
| US4 (Edit) | US3 | Login → edit task → see change |
| US5 (Complete/Delete) | US2 | Login → toggle → delete |
| US6 (Theme) | Phase 2 | Toggle theme → persists after refresh |

---

## Implementation Strategy

### MVP First (User Stories 1 + 2)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL — blocks all stories)
3. Complete Phase 3: User Story 1 (Auth)
4. Complete Phase 4: User Story 2 (View Tasks)
5. **STOP and VALIDATE**: Login, see tasks, verify empty state
6. Deploy/demo if ready — this is the MVP

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. US1 (Auth) → Login/register works → First increment
3. US2 (View Tasks) → Tasks displayed → **MVP!**
4. US3 (Create) → Create via modal → Second increment
5. US4 (Edit) + US5 (Complete/Delete) → Full CRUD → Third increment
6. US6 (Theme) → Dark mode + responsive → Fourth increment
7. Phase 9 (Testing) → 60% coverage + E2E → Release candidate

---

## Summary

| Metric | Value |
|--------|-------|
| Total tasks | 67 |
| Setup tasks | 3 (T001-T003) |
| Foundational tasks | 13 (T004-T016) |
| US1 tasks | 9 (T017-T025) |
| US2 tasks | 5 (T026-T030) |
| US3 tasks | 3 (T031-T033) |
| US4 tasks | 3 (T034-T036) |
| US5 tasks | 5 (T037-T041) |
| US6 tasks | 3 (T042-T044) |
| Polish & Testing tasks | 23 (T045-T067) |
| Parallel opportunities | 32 tasks marked [P] |
| Suggested MVP | Phase 1-4 (US1 + US2): 30 tasks |

---

## Notes

- [P] tasks = different files, no dependencies on incomplete tasks in same phase
- [USn] label maps task to specific user story for traceability
- Every code file must include `// Task: T-XXX` header per constitution traceability
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Backend must be running at `http://localhost:8000` for all testing
