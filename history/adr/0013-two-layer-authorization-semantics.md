# ADR-0013: Two-Layer Authorization Semantics

> **Scope**: Authorization decision order and status-code semantics for user-scoped task routes.

- **Status:** Accepted
- **Date:** 2026-02-15
- **Feature:** phase-2-auth-db-monorepo
- **Context:** Task endpoints include `{user_id}` in path and must prevent cross-user leakage while preserving predictable API behavior.

## Decision

Apply a strict two-layer authorization model in fixed order:
1. Validate authenticated identity exists; reject unauthenticated with 401.
2. Compare authenticated user ID with `{user_id}` path parameter first; return 403 immediately on mismatch with no task lookup.
3. If path user matches, verify task ownership; return 404 when `{task_id}` is not owned by that user.

This order is mandatory and tested as a contract requirement.

### Decision Drivers (Why this choice)

- Information minimization: do not reveal task existence to unauthorized users.
- Explicit path semantics: `{user_id}` mismatch must fail early and predictably.
- Performance: early 403 check avoids unnecessary DB lookups.
- Testability: ordered checks are easy to validate with deterministic integration tests.

## Consequences

### Positive

- Minimizes information leakage while retaining explicit path-scoping behavior.
- Produces deterministic outcomes that can be verified in integration tests.
- Improves security posture by avoiding unnecessary DB lookups on obvious mismatches.

### Negative

- Semantics are nuanced and can be misunderstood by contributors.
- Requires exact middleware/service sequencing to avoid regressions.
- API consumers may question 403 vs 404 behavior without clear documentation.
- Developers may accidentally reverse checks during refactors without strong tests.

## Alternatives Considered

- **Always return 404 for any authorization miss**
  - Pros: maximum resource obfuscation.
  - Rejected: loses required path mismatch semantics and explicit cross-user denial behavior.
- **Always return 403 for any authorization miss**
  - Pros: simpler code path.
  - Rejected: leaks resource existence patterns for task IDs and violates spec rules.
- **Single combined DB authorization query without staged checks**
  - Pros: concise implementation.
  - Rejected: makes SEC-003 ordering requirement harder to prove.

## Likely Questions Later

- Why not always return 404 for stronger obfuscation?
- Why keep explicit 403 on path-user mismatch?
- Is the two-step model worth the added complexity?

## References

- Feature Spec: @specs/1-specify/phase-2/feature-03-auth-db-monorepo.md
- Implementation Plan: @specs/2-plan/phase-2/phase-2-auth-db-monorepo.md
- Related ADRs: @history/adr/0005-stateless-jwt-authentication-with-user-isolation.md
- Evaluator Evidence: Pending (to be linked after Phase C/E authorization test evidence)
