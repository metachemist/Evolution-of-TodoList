# ADR-0002: Command-Line Interface Design

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2026-02-05
- **Feature:** Phase 1 Console App
- **Context:** Need to design CLI commands that are intuitive and follow common patterns while supporting both basic and advanced usage patterns. Users should be able to use both long form options (verbose but clear) and short form options (concise for frequent use).

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security?
     2) Alternatives: Multiple viable options considered with tradeoffs?
     3) Scope: Cross-cutting concern (not an isolated detail)?
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

- **Command Structure**: Standard Unix-style CLI with subcommands (`todo add`, `todo list`, `todo update`, `todo complete`, `todo delete`)
- **Option Forms**: Support for both long form (`--status`, `--title`, `--description`, `--help`) and short form (`-s`, `-t`, `-d`, `-h`) options for all configurable parameters
- **Output Format**: Human-readable table-like structure when listing tasks with support for status filtering
- **User Experience**: Automatic help generation with Typer, consistent error messages, and clear feedback for all operations

## Consequences

### Positive

- Both long and short form options satisfy different user needs (verbose clarity vs concise efficiency)
- Standard Unix-style command patterns improve discoverability and reduce learning curve
- Typer's automatic help generation ensures consistent and accurate documentation
- Consistent feedback improves user experience and reduces confusion

### Negative

- Supporting both long and short forms increases implementation complexity slightly
- Need to maintain consistent option mappings across all commands
- Potential for user confusion if conventions aren't followed consistently
- Additional testing needed to verify both option forms work correctly

## Alternatives Considered

Alternative A: Long form options only
- Clearer but more verbose for frequent operations
- Rejected because it would be less convenient for power users

Alternative B: Short form options only
- More concise but less discoverable for new users
- Rejected because it would sacrifice clarity and accessibility

Alternative C: Different command structure (e.g., `todo-add`, `todo-list`)
- Alternative structure but would be inconsistent with common CLI patterns
- Rejected because it would be unfamiliar to most users

## References

- Feature Spec: @specs/1-specify/features/feature-01-task-crud.md
- Implementation Plan: @specs/2-plan/phase-1-console.md
- Related ADRs:
- Evaluator Evidence:
