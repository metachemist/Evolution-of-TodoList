# ADR-0011: Auth Session Transport and Contract

> **Scope**: Authentication transport, token precedence rules, and response contract consistency across backend and frontend integration.

- **Status:** Accepted
- **Date:** 2026-02-15
- **Feature:** phase-2-auth-db-monorepo
- **Context:** Phase 2 Part 3 requires cookie-based browser auth, compatibility with Better Auth + JWT, and contract continuity with existing task APIs across frontend and backend.

## Decision

Use a dual transport model for authenticated requests:
- Browser flow: httpOnly, Secure, SameSite=Lax cookie with `credentials: 'include'`
- Non-browser flow: Bearer token support in `Authorization` header
- Precedence: Bearer header takes priority when both cookie and header are present
- Keep wrapped API response envelope for all auth and task responses: `success`, `data`, `error`

This model is stateless (no in-memory session store) and preserves existing endpoint contract expectations.

### Decision Drivers (Why this choice)

- Security: browser clients must not handle raw session tokens.
- Compatibility: non-browser/API-tool clients still need authenticated access.
- Contract stability: preserve existing wrapped response envelope and endpoint compatibility.
- Constitutional alignment: keep services stateless and avoid in-memory session state.

## Consequences

### Positive

- Supports both browser and non-browser clients without separate auth stacks.
- Preserves API contract stability while introducing auth hardening.
- Aligns with constitutional stateless-service constraints and Phase II stack direction.
- Reduces frontend token handling risk by keeping browser auth in httpOnly cookies.

### Negative

- Dual-mode auth increases test matrix and implementation complexity.
- Header-vs-cookie precedence must be documented and enforced consistently.
- Misconfigured CORS/credentials setup can break browser auth flows.
- Debugging ambiguity can occur when both cookie and header are sent unintentionally.

## Alternatives Considered

- **Cookie-only auth**
  - Pros: simpler browser security model.
  - Rejected: limits non-browser clients and API tooling compatibility.
- **Bearer-only auth**
  - Pros: single mechanism.
  - Rejected: pushes token handling/storage risk to frontend; conflicts with spec intent for cookie-first browser behavior.
- **Server-side stateful sessions**
  - Pros: easy revocation semantics.
  - Rejected: conflicts with constitutional stateless-service requirement.

## Likely Questions Later

- Why not simplify to cookie-only now and add bearer later?
- Why should bearer header override cookie when both are present?
- Does dual-mode transport create avoidable security or maintenance burden?

## References

- Feature Spec: @specs/1-specify/phase-2/feature-03-auth-db-monorepo.md
- Implementation Plan: @specs/2-plan/phase-2/phase-2-auth-db-monorepo.md
- Related ADRs: @history/adr/0005-stateless-jwt-authentication-with-user-isolation.md, @history/adr/0007-frontend-authentication-architecture.md
- Evaluator Evidence: Pending (to be linked after Phase E evaluation artifacts)
