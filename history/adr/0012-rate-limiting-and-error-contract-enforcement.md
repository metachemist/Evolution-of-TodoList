# ADR-0012: Rate Limiting and Error Contract Enforcement

> **Scope**: Cross-cutting request protection and user-facing error consistency for auth and protected task routes.

- **Status:** Accepted
- **Date:** 2026-02-15
- **Feature:** phase-2-auth-db-monorepo
- **Context:** Phase 2 Part 3 defines strict rate limits, exact error messages, and a stable response envelope across multiple route groups and phases.

## Decision

Adopt centralized enforcement for both throttling and error shaping:
- Enforce rate limits at platform level by request class:
  - Authenticated: 1000 requests/hour per user
  - Unauthenticated/public: 100 requests/hour per IP
- Use a centralized error mapping layer so all auth/authorization/database failures resolve to the exact catalog messages and codes.
- Validate contract exactness in Phase E with dedicated conformance tests.

### Decision Drivers (Why this choice)

- Consistency: route-level custom handling risks drift from the error catalog.
- Security posture: split rate limiting is required for brute-force resistance on public endpoints.
- Auditability: centralized behavior is easier to verify and explain in evaluations/paper.
- Maintainability: policy changes should be made once, not in every handler.

## Consequences

### Positive

- Consistent behavior across all routes and services.
- Lower risk of message drift that would violate specification checks.
- Clear auditability in paper/evaluation sections for security and UX consistency.
- Easier to evolve policies without rewriting route handlers.

### Negative

- Centralized layer becomes critical path for correctness/performance.
- Requires careful classification of public vs protected endpoints.
- More integration testing needed to verify edge-path behavior.
- Policy misclassification can create false throttling or under-protection.

## Alternatives Considered

- **Per-route ad hoc rate limiting and error responses**
  - Pros: local flexibility.
  - Rejected: high inconsistency risk and duplicated logic.
- **Single global rate limit policy for all requests**
  - Pros: simpler implementation.
  - Rejected: does not meet spec split between per-user and per-IP constraints.
- **External WAF-only throttling without app-level semantics**
  - Pros: operational offload.
  - Rejected: insufficient control for spec-specific behavior and error contract mapping.

## Likely Questions Later

- Why not rely solely on infrastructure-level rate limiting?
- Why centralize error shaping instead of handling near business logic?
- How do we prevent centralized policy from becoming a bottleneck?

## References

- Feature Spec: @specs/1-specify/phase-2/feature-03-auth-db-monorepo.md
- Implementation Plan: @specs/2-plan/phase-2/phase-2-auth-db-monorepo.md
- Related ADRs: @history/adr/0003-data-validation-and-error-handling-strategy.md
- Evaluator Evidence: Pending (to be linked after Phase E conformance results)
