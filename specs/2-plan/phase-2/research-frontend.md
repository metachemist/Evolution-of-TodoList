# Research: Next.js Todo Frontend

**Feature**: 006-nextjs-todo-frontend | **Date**: 2026-02-13

## 1. Next.js 16+ App Router Patterns

**Decision**: App Router with route groups, `proxy.ts` for coarse auth guard, Server Components by default.

**Rationale**: Next.js 16 renames middleware.ts to proxy.ts and explicitly scopes it to routing (redirects, rewrites) — not auth enforcement. This is informed by CVE-2025-29927 where middleware auth was bypassed via `x-middleware-subrequest` header. Auth validation must happen in Server Components (layout.tsx calling `/api/auth/me`). Route groups `(auth)` and `(dashboard)` separate layout concerns without URL segments.

**Alternatives considered**:
- Pages Router: Legacy, lacks RSC and streaming. Constitution mandates modern Next.js.
- Middleware-only auth: Insecure per CVE-2025-29927 and Next.js 16 guidance.

## 2. Authentication with httpOnly Cookies

**Decision**: Frontend uses `credentials: 'include'` on all fetch calls. Dashboard layout RSC calls `GET /api/auth/me` with forwarded cookie to validate session and get user identity.

**Rationale**: The backend already sets httpOnly, Secure, SameSite=Lax cookies. The frontend cannot (and should not) read the JWT. The `cookies()` API in Next.js Server Components allows forwarding the cookie in server-to-server calls. `proxy.ts` performs a fast cookie-presence check; real validation is in the layout.

**Alternatives considered**:
- Auth.js (NextAuth): Over-engineered — backend owns auth, no need for Auth.js providers/adapters.
- localStorage/sessionStorage JWT: Vulnerable to XSS. Spec mandates httpOnly cookies.
- iron-session: Not needed — backend owns JWT lifecycle.

## 3. State Management

**Decision**: TanStack Query v5 for all server state. React Context for user identity only.

**Rationale**: All application state is server state (tasks fetched/mutated via API). TanStack Query provides: `useQuery` for data fetching with background refetch, `useMutation` with `onMutate`/`onError`/`onSettled` for optimistic updates + rollback, query invalidation for cache consistency. DevTools for debugging. No global client state library needed — user identity is a simple context bridge from RSC to client.

**Alternatives considered**:
- SWR: Viable, smaller bundle (5KB vs 16KB). Rejected: less ergonomic optimistic update API for multi-mutation apps.
- Zustand: Appropriate for complex client state. Unnecessary here — no non-server state beyond user identity.
- React Context + useReducer: Would require reimplementing caching, deduplication, and background sync.

## 4. Testing Framework

**Decision**: Vitest + React Testing Library (unit/component), Playwright (E2E).

**Rationale**: Vitest runs ~4x faster than Jest (native ESM/TS, no Babel). Next.js 16 has official Vitest example. V8 coverage provider for the 60% target. Playwright covers cross-browser E2E (Chrome, Firefox, WebKit) matching spec browser support requirements.

**Alternatives considered**:
- Jest: More config needed for ESM/Next.js 16. No advantage over Vitest for new projects.
- Cypress: Less multi-browser support, slower. Playwright is the Next.js recommended E2E tool.

## 5. CSS/Styling & Theming

**Decision**: Tailwind CSS v4 (CSS-first config) + next-themes for dark/light mode persistence.

**Rationale**: Constitution mandates Tailwind CSS. v4 uses `@import "tailwindcss"` and `@theme` CSS directives — no JS config file. 100x faster incremental builds. next-themes provides `localStorage` persistence, hydration-safe class toggling, and `useTheme()` hook. `suppressHydrationWarning` on `<html>` prevents mismatch.

**Alternatives considered**:
- Tailwind v3: v4 is stable, should be used for new projects.
- Manual dark mode with CSS variables: next-themes handles edge cases (SSR hydration, storage).

## 6. Toast Notifications

**Decision**: Sonner.

**Rationale**: ~2KB gzipped. Callable outside React components (useful in API client layer). Supports duration, close button, stacking animations. Satisfies spec: success toast 3s auto-dismiss, error toast 5s dismissible.

**Alternatives considered**:
- react-hot-toast: Similar size/API. Sonner has better animations and shadcn/ui ecosystem alignment.
- react-toastify: ~20KB, features not needed.
- Custom: Would duplicate Sonner's accessible ARIA handling (`role="status"`, `aria-live="polite"`).

## 7. Modal/Dialog

**Decision**: Radix UI Dialog (`@radix-ui/react-dialog`).

**Rationale**: Spec requires WCAG 2.1 AA modal accessibility: focus trap, Escape close, focus restoration, screen reader announcement, scroll lock. Radix provides all automatically. Unstyled primitives styled with Tailwind for full visual control.

**Alternatives considered**:
- Headless UI: Strong alternative, Tailwind-team maintained. Radix has broader component ecosystem for future phases.
- Native HTML `<dialog>`: Inconsistent accessibility across browsers. Requires polyfill for focus trap.
- Custom div + ARIA: High implementation cost to reach WCAG compliance.

## 8. Form Validation

**Decision**: react-hook-form v7 + Zod v4 + @hookform/resolvers.

**Rationale**: Uncontrolled inputs minimize re-renders (spec: <200ms validation error display). Zod schemas provide TypeScript-first validation matching spec rules (email format, password 8+ chars, title 255 max, description 5000 max). Same schemas usable on client and server.

**Alternatives considered**:
- React 19 useActionState + Server Actions: Backend is FastAPI, not Next.js Server Actions — would add unnecessary network hop.
- Formik + Yup: Heavier (~45KB vs ~21KB), controlled inputs cause more re-renders.
- Native HTML5 validation: Cannot produce spec-specific error messages or custom length constraints.

## 9. API Client Layer

**Decision**: Custom fetch wrapper with `credentials: 'include'`, error message catalog, 15s timeout.

**Rationale**: Spec FR-018 mandates centralized API layer. Native fetch works in both browser and Node.js (Server Components). Custom wrapper handles: cookie auth (`credentials: 'include'`), error code → user-friendly message mapping, 15s timeout (spec edge case), 401 → session expiry redirect. No external dependency needed.

**Alternatives considered**:
- Axios: ~15KB for functionality available natively.
- openapi-fetch (auto-generated): Deferred to later phase when API surface grows.
- Next.js Route Handlers as proxy: Unnecessary — backend CORS is configured for frontend origin.

## 10. Backend Compatibility Verification

**Decision**: No backend modifications required.

**Rationale**: The existing FastAPI backend already supports:
- httpOnly cookie auth alongside Bearer token auth (`get_current_user_id` checks both)
- `GET /api/auth/me` — returns `{ id, email }` from cookie/token
- `POST /api/auth/logout` — clears httpOnly cookie
- CORS with `allow_credentials=True` for `http://localhost:3000`
- All task CRUD endpoints with user isolation
- Structured error responses matching spec error catalog

**Verification**: Backend routes, auth utilities, and test fixtures confirmed via codebase analysis.
