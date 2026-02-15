# ADR-0010: Frontend Testing Strategy

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together.

- **Status:** Accepted
- **Date:** 2026-02-13
- **Feature:** Phase 2 — Next.js Todo Frontend
- **Context:** The spec requires 60% automated test coverage of frontend business logic (validation, state management, API integration) and acceptance tests for all 6 user stories (SC-012, SC-010). The constitution mandates the same: 60% coverage for Phase II (Verification section). Next.js 16 and TypeScript 5 with native ESM modules create specific constraints on test runner compatibility. The choice here shapes every test file structure, CI configuration, and coverage reporting in the project.

<!-- Significance checklist: PASS — affects all test files, CI pipeline, coverage target, multiple alternatives -->

## Decision

- **Unit & Component tests**: Vitest (test runner) + React Testing Library (RTL) for component rendering
- **E2E / Acceptance tests**: Playwright
- **Coverage**: Vitest's built-in V8 provider, 60% threshold enforced on `src/lib/**`, `src/hooks/**`, `src/components/**`
- **Test organisation**:
  - `src/__tests__/unit/` — pure functions (API client helpers, Zod validators)
  - `src/__tests__/components/` — React Testing Library component tests
  - `src/__tests__/hooks/` — TanStack Query hook tests with MSW mock server
  - `e2e/` — one Playwright spec file per user story (6 files)

## Consequences

### Positive

- Vitest runs ~4x faster than Jest for the same suite (native ESM, no Babel transform, no module mapper config)
- Next.js 16 has an official Vitest integration example — no custom config needed
- Playwright tests run against real browsers (Chromium, Firefox, WebKit), matching the spec's browser support matrix exactly
- V8 coverage is fast and accurate for TypeScript without instrumentation overhead

### Negative

- Vitest cannot render async React Server Components (RSCs) — RSC data-fetching logic must be tested indirectly via unit tests of the underlying API client functions
- Two separate test runners in the project (Vitest for unit/component, Playwright for E2E) — different commands, different config files
- MSW (Mock Service Worker) needed to test TanStack Query hooks in isolation — adds setup complexity

## Alternatives Considered

**Alternative A — Jest + React Testing Library + Playwright**: Rejected — Jest requires Babel transforms or custom module name mappers to handle Next.js 16's native ESM imports and path aliases. For a new project, there is no reason to choose Jest over Vitest. Jest setup takes ~1 hour; Vitest works out-of-the-box with the official Next.js template.

**Alternative B — Jest + Cypress (E2E)**: Rejected — Cypress runs tests in a single browser (Electron/Chromium by default). Multi-browser support (Chrome, Firefox, WebKit/Safari) requires additional configuration and a paid Cypress Cloud subscription. Playwright runs against all three engines locally for free. Next.js official docs recommend Playwright.

**Alternative C — Vitest only (no Playwright)**: Rejected — Vitest with jsdom cannot test real navigation, real cookie behaviour, or cross-browser rendering. The spec's 6 user stories require end-to-end verification including cookie-based auth flows that cannot be exercised in a jsdom environment.

**Alternative D — Playwright only (no unit tests)**: Rejected — E2E tests are slow (seconds per test) and brittle on CI. The 60% coverage target requires fast-running unit and component tests for the business logic layer. E2E alone would make the suite too slow and fragile to run on every PR.

## References

- Feature Spec: @specs/1-specify/phase-2/feature-02-nextjs-todo-frontend.md (SC-010, SC-012, SC-013, Constraints: Testing)
- Implementation Plan: @specs/2-plan/phase-2/phase-2-nextjs-todo-frontend.md (ADR-005, Phase D testing items, Technical Context)
- Quickstart: @specs/2-plan/phase-2/quickstart-frontend.md (vitest.config.ts configuration)
- Research: @specs/2-plan/phase-2/research-frontend.md (§4 Testing Framework)
- Related ADRs: ADR-0008 (TanStack Query hooks are the primary unit-test target), ADR-0009 (react-hook-form validators tested via Zod unit tests)
- Evaluator Evidence: @history/prompts/006-nextjs-todo-frontend/0004-frontend-implementation-plan.plan.prompt.md
