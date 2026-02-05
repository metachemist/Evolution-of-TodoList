# ADR-0001: Console Application Technology Stack

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2026-02-05
- **Feature:** Phase 1 Console App
- **Context:** Need to select technology stack for a command-line todo application with in-memory storage that meets performance requirements (<100ms response time) and follows Python best practices with type hints.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security?
     2) Alternatives: Multiple viable options considered with tradeoffs?
     3) Scope: Cross-cutting concern (not an isolated detail)?
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

- **Primary Language**: Python 3.13+ for modern features and performance optimizations
- **CLI Framework**: Typer for building beautiful command-line interfaces with minimal code
- **Data Storage**: In-Memory List using Python native list for Task objects during runtime
- **Additional Libraries**: Datetime module for timestamp management, Standard Library for file operations
- **Development Dependencies**: pytest for testing, black for code formatting, mypy for type checking

## Consequences

### Positive

- Typer provides excellent developer experience with automatic help generation and type inference
- Python 3.13+ offers modern syntax and performance improvements
- In-memory storage keeps the architecture simple for Phase 1 with no external dependencies
- Type hints improve code quality and maintainability
- Standard library components ensure portability and stability

### Negative

- Typer introduces an external dependency (though with argparse as alternative)
- In-memory storage means data loss on application exit (but acceptable for Phase 1)
- Python 3.13+ may have limited deployment environments initially
- Additional dev dependencies increase development environment complexity

## Alternatives Considered

Alternative Stack A: Python + Argparse + SQLite
- Simpler standard library approach but more verbose CLI code, with persistence
- Rejected because it would add database complexity for Phase 1 requirements

Alternative Stack B: Node.js + Commander.js + JavaScript
- Would use different language ecosystem but similar CLI framework
- Rejected to maintain consistency with constitution requirements favoring Python

Alternative Stack C: Go + Cobra + Native structs
- Different language with compiled performance benefits
- Rejected to maintain consistency with project technology stack decisions

## References

- Feature Spec: @specs/1-specify/features/feature-01-task-crud.md
- Implementation Plan: @specs/2-plan/phase-1-console.md
- Related ADRs:
- Evaluator Evidence:
