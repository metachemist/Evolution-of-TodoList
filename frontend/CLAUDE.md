# Frontend Agent Instructions

**Task**: T003 | **Feature**: 006-nextjs-todo-frontend

## Project Conventions

### API Calls
- **Always** use `apiClient` from `@/lib/api-client` — never raw `fetch()` directly
- All requests include `credentials: 'include'` (cookie auth)
- Error codes are mapped to user-facing messages in `api-client.ts`

### Server vs Client Components
- **Default**: All components are Server Components (RSC)
- **Add `'use client'`** only when component uses hooks, event handlers, or browser APIs
- Layouts that need auth (`(dashboard)/layout.tsx`) are RSC — they call `cookies()` and `redirect()`
- NavBar, forms, and interactive widgets are client components

### Forms
- All forms use `react-hook-form` + `zodResolver` from `@hookform/resolvers/zod`
- Never use `useState` for field values — use `register()` from `useForm()`
- Error messages come from Zod schemas in `@/lib/validations`

### Data Mutations
- All data-modifying operations go through hooks in `use-tasks.ts` or `use-auth.ts`
- Never call `apiClient` directly from components — use the hooks
- All mutations use optimistic updates with rollback on error

### Modals
- All dialogs use the `Modal` wrapper from `@/components/ui/Modal`
- Never implement custom dialog/overlay components
- Focus returns to trigger element when modal closes

### Toasts
- Call `toast.success()` or `toast.error()` from `sonner`
- Never manage notification state with `useState`
- Success: 3s; Error: 5s, dismissible

### Task ID Traceability
- Every file header must include `// Task: T-XXX` referencing the task that created it
- Example: `// Task: T007 | api-client.ts`

## File Locations
- Types: `src/types/index.ts`
- Zod schemas: `src/lib/validations.ts`
- API client: `src/lib/api-client.ts`
- Query client: `src/lib/query-client.ts`
- Task hooks: `src/hooks/use-tasks.ts`
- Auth hooks: `src/hooks/use-auth.ts`
- UI primitives: `src/components/ui/`
- Auth components: `src/components/auth/`
- Task components: `src/components/tasks/`
- Providers: `src/providers/`

## Feature 007: Auth & Session Patterns (Task: T039)

### better-auth Package Role
- Installed: `npm install better-auth`
- Used as the client-side auth configuration utility
- Shares `SECRET_KEY` (HS256) with the backend PyJWT/python-jose — same secret = compatible JWTs
- `BETTER_AUTH_SECRET` and `BETTER_AUTH_URL` in `.env.example` configure the client

### Session Transport
- All API calls use `credentials: 'include'` (set globally in `src/lib/api-client.ts`)
- The browser attaches the `access_token` httpOnly cookie automatically on same-origin and allowed-origin requests
- **Never** read, parse, or store the cookie from JS — it is httpOnly

### Session Expiry Handling
- `src/lib/query-client.ts` global `QueryCache.onError` handler:
  - 401 or code `SESSION_EXPIRED` → `window.location.href = '/login?reason=session_expired'`
  - 403 → `toast.error(...)` + redirect to dashboard
- Login page (`src/app/(auth)/login/page.tsx`) renders a `role="alert"` banner when `?reason=session_expired` is in the URL

### Proxy Session Check (F05 pattern)
- `src/proxy.ts` runs on `/dashboard/*` routes (Next.js 16: renamed from `middleware.ts`)
- Function export: `export default async function proxy(request: Request)` — uses standard `Request`, NOT `NextRequest` (edge runtime not supported in proxy)
- Parses cookies from `request.headers.get('cookie')` — no `request.cookies` on standard Request
- **Does** extract the `access_token` cookie value and passes it explicitly:
  ```ts
  fetch(`${API_URL}/api/auth/me`, { headers: { Cookie: `access_token=${cookieValue}` } })
  ```
- On 401 → redirect to `/login?reason=session_expired`
- On network error → fail open (let dashboard handle it)

### Task Traceability
- Every file must include `// Task: T-XXX` or `// Task: TXXX` at the top

## Testing
- Unit tests: `src/__tests__/unit/`
- Hook tests: `src/__tests__/hooks/`
- Component tests: `src/__tests__/components/`
- E2E tests: `e2e/`
- Run tests: `npm test` (Vitest)
- Run E2E: `npm run test:e2e` (self-contained: boots backend + frontend)
