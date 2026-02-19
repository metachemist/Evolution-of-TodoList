# ADR-0014: Schema-First Migration with Orphan Cleanup

> **Scope**: Migration sequencing and data treatment during transition from pre-auth task storage to authenticated ownership model.

- **Status:** Accepted
- **Date:** 2026-02-15
- **Feature:** phase-2-auth-db-monorepo
- **Context:** Feature requires persistent ownership guarantees, deploy-time migrations, and removal of pre-existing tasks without valid owners.

## Decision

Use a two-stage migration strategy across phases:
- Stage 1 (Phase B): establish baseline schema (users/tasks tables, foreign keys, required indexes) and validate apply/rollback.
- Stage 2 (Phase D): execute targeted cleanup migration that removes orphaned legacy tasks and verifies no ownerless tasks remain.

The strategy is rollback-documented and treated as a gated dependency for production signoff.

### Decision Drivers (Why this choice)

- Risk containment: separate foundational schema change from destructive cleanup.
- Operational safety: preserve clear rollback boundaries and verification checkpoints.
- Spec conformance: FR-018 and FR-019 require both deploy-time schema readiness and orphan removal.
- Communication clarity: phased migration is easier to explain and defend in design/paper review.

## Consequences

### Positive

- Reduces risk by separating schema setup from destructive cleanup logic.
- Makes migration behavior auditable and easier to explain in the paper.
- Aligns directly with requirement traceability for FR-018 and FR-019.
- Improves confidence through explicit rollback and validation checkpoints.

### Negative

- Requires additional migration artifacts and coordination across phases.
- Legacy anonymous tasks are intentionally lost; this can be questioned by stakeholders.
- More test fixtures are needed to cover upgrade and rollback paths.
- Longer delivery path compared with a single migration pass.

## Alternatives Considered

- **Single big-bang migration (schema + cleanup together)**
  - Pros: fewer steps.
  - Rejected: harder rollback and higher blast radius on failure.
- **Backfill orphan tasks to a synthetic/system user**
  - Pros: avoids data deletion.
  - Rejected: violates spec intent that unattributable legacy tasks are discarded.
- **Keep anonymous tasks in parallel table**
  - Pros: preserves historical data.
  - Rejected: adds long-term complexity and weakens ownership guarantees.

## Likely Questions Later

- Why delete orphaned tasks instead of preserving them?
- Why not perform schema + cleanup in one migration?
- How do we prove rollback safety under real deployment pressure?

## References

- Feature Spec: @specs/1-specify/phase-2/feature-03-auth-db-monorepo.md
- Implementation Plan: @specs/2-plan/phase-2/phase-2-auth-db-monorepo.md
- Related ADRs: @history/adr/0005-stateless-jwt-authentication-with-user-isolation.md
- Evaluator Evidence: Pending (to be linked after migration execution reports)
