# ADR-0007: Frontend Authentication Architecture

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together.

- **Status:** Accepted
- **Date:** 2026-02-13
- **Feature:** Phase 2 — Next.js Todo Frontend
- **Context:** The frontend integrates with a FastAPI backend that issues JWTs as httpOnly cookies (see ADR-0005). The frontend cannot read the cookie. Next.js 16 scoped `proxy.ts` (formerly middleware) to routing only — auth enforcement must happen in Server Components. CVE-2025-29927 demonstrated that middleware-only auth can be bypassed. The spec requires user identity on every task API call and defines distinct responses for 401 (session expired) and 403 (forbidden) errors.

<!-- Significance checklist: PASS — security architecture, cross-cutting, multiple alternatives -->

## Decision

- **Token transport**: All API calls use `credentials: 'include'` — browser attaches httpOnly cookie automatically. Frontend never reads, stores, or transmits raw JWT.
- **Layer 1 — Coarse guard** (`proxy.ts`): Checks cookie *presence* only. Redirects unauthenticated requests away from `/dashboard`. Fast routing check, not a security gate.
- **Layer 2 — Real validation** (`(dashboard)/layout.tsx` Server Component): Calls `GET /api/auth/me` with cookie forwarded via `cookies()` API. On 401 → redirect to `/login`. Authoritative auth check, CVE-safe.
- **User identity**: `/api/auth/me` response (`{ id, email }`) passed into `UserProvider` React Context. Client components read `userId` from context — no token reading required anywhere.
- **Global 401 handling**: `QueryCache.onError` catches 401 from any API call → redirect to `/login?reason=session_expired`.
- **Global 403 handling**: `QueryCache.onError` catches 403 → show toast "You don't have permission to perform this action." + redirect to `/dashboard`.

## Consequences

### Positive

- XSS-safe: raw JWT never in JavaScript-accessible memory or storage
- Two-layer defence: expired cookies caught by layout RSC even if proxy.ts is bypassed
- Stateless: no server-side session table; horizontal scaling unaffected
- Clean separation: task components receive `userId` from context with no auth complexity

### Negative

- Server Components must explicitly forward cookies in server-to-server fetch calls (extra `cookies()` boilerplate)
- Every `/dashboard` page load makes an additional `GET /api/auth/me` network call
- Token expiry cannot be detected proactively — only reactively when backend returns 401

## Alternatives Considered

**Alternative A — Middleware-only auth** (`proxy.ts` validates JWT with `jose`): Rejected — Next.js 16 explicitly restricts proxy.ts to routing. Vulnerable to CVE-2025-29927 bypass. Cannot make DB or backend calls from middleware.

**Alternative B — Auth.js (NextAuth v5)**: Rejected — backend owns the full auth lifecycle. Auth.js introduces providers, adapters, and its own session DB schema for a problem the FastAPI backend already solves. Over-engineered.

**Alternative C — JWT in localStorage + Bearer header**: Rejected — XSS-vulnerable (any injected script can read the token). Spec explicitly mandates httpOnly cookies.

**Alternative D — JWT in sessionStorage**: Rejected — still XSS-vulnerable. Token lost on tab close forces re-login. Spec mandates httpOnly cookies.

## References

- Feature Spec: @specs/1-specify/phase-2/feature-02-nextjs-todo-frontend.md (FR-003, FR-004, FR-006, FR-020, edge cases)
- Implementation Plan: @specs/2-plan/phase-2/phase-2-nextjs-todo-frontend.md (ADR-001, ADR-003, Phase A items 4–5, Phase B)
- Research: @specs/2-plan/phase-2/research-frontend.md (§1 App Router Patterns, §2 Authentication)
- Related ADRs: ADR-0005 (backend JWT auth), ADR-0004 (full-stack technology stack)
- Evaluator Evidence: @history/prompts/006-nextjs-todo-frontend/0004-frontend-implementation-plan.plan.prompt.md
