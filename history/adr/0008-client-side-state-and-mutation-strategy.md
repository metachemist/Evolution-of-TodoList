# ADR-0008: Client-Side State and Mutation Strategy

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together.

- **Status:** Accepted
- **Date:** 2026-02-13
- **Feature:** Phase 2 — Next.js Todo Frontend
- **Context:** The frontend must fetch tasks from the backend on dashboard load and support four mutation types (create, update, delete, toggle completion). The spec mandates optimistic UI updates for all mutations with rollback on backend rejection (FR-009–FR-012). The only non-server state is the authenticated user's identity. There is no complex client-side UI state (no filters, no selection state, no draft editing state).

<!-- Significance checklist: PASS — affects every task component, cross-cutting optimistic pattern, multiple alternatives -->

## Decision

- **Server state**: TanStack Query v5 manages all task data. Query key: `['tasks', userId]`.
- **Data fetching**: `useQuery` with `staleTime: 0` — always fresh on navigation.
- **Optimistic mutation pattern** (applied to all 4 mutations):
  1. `onMutate`: cancel in-flight queries → snapshot cache → apply optimistic change
  2. `onError`: restore snapshot → show error toast (5s, dismissible)
  3. `onSettled`: invalidate `['tasks', userId]` to sync with server truth
- **User identity**: `UserProvider` React Context (not TanStack Query). Populated once by the dashboard layout Server Component from `GET /api/auth/me`. Session state, not cache state.
- **No global client state library**: No Zustand, no Redux. No non-server state exists beyond user identity.

## Consequences

### Positive

- Consistent, testable three-phase optimistic pattern across all 4 mutation types
- TanStack Query DevTools provides cache visibility during development
- Automatic background refetch and request deduplication built in
- Zero custom caching or loading-state logic to maintain

### Negative

- ~16KB bundle addition vs ~5KB for SWR (acceptable within 250KB gzipped budget)
- `onSettled` triggers a refetch after every mutation — one extra GET per mutation at Phase II scale
- Developers unfamiliar with TanStack Query's query key model have a ramp-up curve

## Alternatives Considered

**Alternative A — SWR** (~5KB, Vercel-maintained): Rejected — optimistic rollback API is more manual (requires explicitly passing the rollback function to `mutate()`). TanStack Query's `onMutate`/`onError`/`onSettled` lifecycle is more ergonomic for 4 independent mutation types. SWR is better suited for simpler read-heavy apps.

**Alternative B — Zustand + manual fetch**: Rejected — would require reimplementing deduplication, loading state, error state, background refetch, and cache invalidation that TanStack Query provides. Appropriate for complex client-side UI state, not server cache.

**Alternative C — React Context + useReducer**: Rejected — same objections as Zustand, with worse ergonomics (no DevTools, manual cache management, no query key invalidation pattern).

**Alternative D — React 19 `useOptimistic` + Server Actions**: Rejected — Server Actions are co-located with the Next.js app. Backend calls go to a separate FastAPI service; using Server Actions adds an unnecessary network hop through the Next.js server layer.

## References

- Feature Spec: @specs/1-specify/phase-2/feature-02-nextjs-todo-frontend.md (FR-009–FR-012, edge case: optimistic rollback)
- Implementation Plan: @specs/2-plan/phase-2/phase-2-nextjs-todo-frontend.md (ADR-002, Component Dependency Matrix, Phase C)
- Data Model: @specs/2-plan/phase-2/data-model-frontend.md (Task entity, state transitions)
- Research: @specs/2-plan/phase-2/research-frontend.md (§3 State Management)
- Related ADRs: ADR-0007 (auth architecture — UserProvider depends on this pattern)
- Evaluator Evidence: @history/prompts/006-nextjs-todo-frontend/0004-frontend-implementation-plan.plan.prompt.md
