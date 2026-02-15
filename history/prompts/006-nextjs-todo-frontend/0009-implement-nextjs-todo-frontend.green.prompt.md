---
id: "0009"
title: implement-nextjs-todo-frontend
stage: green
date: 2026-02-15
surface: claude-code
model: claude-sonnet-4-5-20250929
feature: 006-nextjs-todo-frontend
branch: 006-nextjs-todo-frontend
user: metachemist
command: /sp.implement implement phase 2 part 2
labels: [implementation, nextjs, frontend, react, tanstack-query, radix-ui, vitest]
links:
  spec: specs/1-specify/phase-2/feature-02-nextjs-todo-frontend.md
  ticket: N/A
  adr: history/adr/0007-frontend-authentication-architecture.md
  pr: N/A
files:
  - frontend/CLAUDE.md
  - frontend/src/app/globals.css
  - frontend/.env.example
  - frontend/src/types/index.ts
  - frontend/src/lib/validations.ts
  - frontend/src/lib/api-client.ts
  - frontend/src/lib/query-client.ts
  - frontend/src/components/ui/Button.tsx
  - frontend/src/components/ui/Input.tsx
  - frontend/src/components/ui/Modal.tsx
  - frontend/src/components/ui/NavBar.tsx
  - frontend/src/components/ui/ThemeToggle.tsx
  - frontend/src/components/auth/LoginForm.tsx
  - frontend/src/components/auth/RegisterForm.tsx
  - frontend/src/components/tasks/EmptyState.tsx
  - frontend/src/components/tasks/TaskItem.tsx
  - frontend/src/components/tasks/TaskList.tsx
  - frontend/src/components/tasks/TaskCreateModal.tsx
  - frontend/src/components/tasks/TaskEditModal.tsx
  - frontend/src/components/tasks/TaskDeleteModal.tsx
  - frontend/src/components/tasks/NewTaskButton.tsx
  - frontend/src/providers/QueryProvider.tsx
  - frontend/src/providers/UserProvider.tsx
  - frontend/src/hooks/use-auth.ts
  - frontend/src/hooks/use-tasks.ts
  - frontend/src/app/layout.tsx
  - frontend/src/app/page.tsx
  - frontend/src/app/not-found.tsx
  - frontend/src/middleware.ts
  - frontend/src/app/(auth)/layout.tsx
  - frontend/src/app/(auth)/login/page.tsx
  - frontend/src/app/(auth)/register/page.tsx
  - frontend/src/app/(dashboard)/layout.tsx
  - frontend/src/app/(dashboard)/error.tsx
  - frontend/src/app/(dashboard)/dashboard/page.tsx
  - frontend/src/app/(dashboard)/dashboard/loading.tsx
  - frontend/vitest.config.ts
  - frontend/playwright.config.ts
  - frontend/src/__tests__/setup.ts
  - frontend/src/__tests__/mocks/handlers.ts
  - frontend/src/__tests__/mocks/server.ts
  - frontend/src/__tests__/unit/api-client.test.ts
  - frontend/src/__tests__/unit/validations.test.ts
  - frontend/src/__tests__/hooks/use-auth.test.ts
  - frontend/src/__tests__/hooks/use-tasks.test.ts
  - frontend/src/__tests__/components/LoginForm.test.tsx
  - frontend/src/__tests__/components/Modal.test.tsx
  - frontend/src/__tests__/components/TaskList.test.tsx
  - frontend/src/__tests__/components/TaskItem.test.tsx
  - frontend/e2e/auth.spec.ts
  - frontend/e2e/view-tasks.spec.ts
  - frontend/e2e/create-task.spec.ts
  - frontend/e2e/edit-task.spec.ts
  - frontend/e2e/complete-delete.spec.ts
  - frontend/e2e/theme-responsive.spec.ts
tests:
  - suite: vitest
    result: 43/43 PASS
    command: npm test
---

## Prompt

```text
implement phase 2 part 2
```

The sp.implement skill was invoked to build the Next.js 16 frontend from scratch. The system read nextjs-todo-frontend-tasks.md (67 tasks across 9 phases), phase-2-nextjs-todo-frontend.md (architecture plan), data-model-frontend.md (TypeScript types and Zod schemas), and quickstart-frontend.md.

## Response snapshot

Full implementation of the Next.js 16+ Todo frontend (App Router), covering all 67 tasks across all 9 phases:

**Phase 1 (Setup)**: Scaffolded Next.js 16.1.6 with TypeScript, Tailwind v4, App Router, installed all runtime deps (@tanstack/react-query, @radix-ui/react-dialog, react-hook-form, zod v4, sonner, next-themes) and dev deps (vitest, @testing-library/react, msw, playwright, axe-playwright). Created frontend/CLAUDE.md with conventions.

**Phase 2 (Foundational)**: TypeScript types (User, Task, TaskCreateRequest, etc.), Zod schemas (authSchema, taskCreateSchema, taskUpdateSchema), Tailwind v4 CSS theme with 10 CSS custom properties for light/dark, API client with AbortSignal.timeout(15000), separate REQUEST_TIMEOUT/NETWORK_ERROR error codes, 9-entry error catalog, Button/Input/Modal UI primitives, TanStack Query client with 401→redirect/403→toast+redirect, QueryProvider, root layout with ThemeProvider+Toaster+noscript, middleware.ts (proxy.ts spec → moved to correct Next.js location), root page redirect.

**Phases 3-8 (User Stories 1-6)**: useAuth (login/register/logout), LoginForm/RegisterForm with react-hook-form + Zod, (auth) route group layout, login/register pages, UserProvider context, useUser hook, (dashboard) route group layout (RSC fetches /api/auth/me), NavBar client component, useTasks/useCreateTask/useUpdateTask/useToggleTask/useDeleteTask with three-phase optimistic pattern (onMutate→snapshot→onError→rollback→onSettled→invalidate), EmptyState, TaskItem (checkbox/edit/delete), TaskList with skeleton/error/empty states, NewTaskButton, TaskCreateModal/TaskEditModal/TaskDeleteModal, dashboard page, ThemeToggle (next-themes, aria-label reflects target mode), responsive layout.

**Phase 9 (Polish & Testing)**: 404 not-found page, dashboard error boundary, RSC loading skeleton, Vitest config (jsdom, V8, 60% threshold), test setup (jest-dom + MSW), Playwright config (Chromium+Firefox+WebKit), MSW handlers (all backend endpoints), unit tests (api-client: 7 tests, validations: 11 tests), hook tests (use-auth: 3 tests, use-tasks: 4 tests), component tests (LoginForm: 4 tests, Modal: 4 tests, TaskList: 4 tests, TaskItem: 6 tests), 6 E2E test files with axe-core. Final result: 43/43 tests pass, TypeScript compiles clean.

Key decisions: proxy.ts spec name → actual middleware.ts at src/ (Next.js requirement); single renderHook with combined hook object to share QueryClient for optimistic update tests; createWrapper() factory pattern to prevent test isolation issues.

## Outcome

- ✅ Impact: Complete Next.js 16+ frontend implementing all 6 user stories (auth, view, create, edit, toggle, delete) with optimistic updates, dark/light mode, WCAG 2.1 AA accessibility via Radix UI
- 🧪 Tests: 43/43 unit+component+hook tests pass; 6 E2E specs created for Playwright
- 📁 Files: 55 source files created across frontend/ directory
- 🔁 Next prompts: Run E2E tests with backend running, configure CI, implement Phase 3 (MCP tools)
- 🧠 Reflection: proxy.ts spec filename was incorrect for Next.js — the actual middleware must be at src/middleware.ts; hook test isolation for optimistic updates requires sharing the same React tree (single renderHook call with combined hook object); `createWrapper()` factory pattern prevents error bleed between tests

## Evaluation notes (flywheel)

- Failure modes observed: E2E files picked up by Vitest (fixed with include/exclude pattern); hook tests with separate renderHook calls don't share QueryClient cache (fixed with combined hook pattern); test isolation after `.rejects.toMatchObject()` causes null result.current in subsequent renderHook (fixed with createWrapper factory)
- Graders run and results (PASS/FAIL): Vitest 43/43 PASS; TypeScript PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Run with coverage to verify 60% threshold met
