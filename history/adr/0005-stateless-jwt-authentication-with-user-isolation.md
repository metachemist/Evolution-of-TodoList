# ADR-0005: Stateless JWT Authentication with User Isolation

## Status
Proposed

## Date
2026-02-07

## Context
The application requires secure user authentication with proper data isolation between users. The architecture must be stateless to support horizontal scaling and cloud-native deployment in later phases.

## Decision
- Authentication: JWT tokens with BETTER_AUTH_SECRET
- Password Security: bcrypt hashing with cost factor 12
- Session Management: Stateless JWT approach (no server-side sessions)
- User Isolation: Strict validation of user_id in JWT vs URL parameter
- Token Expiration: 1-hour expiration (3600 seconds)

## Alternatives
- Alternative 1: Session-based authentication with server-side storage
- Alternative 2: OAuth 2.0 with external providers
- Alternative 3: Custom token system instead of JWT

## Consequences
- Positive: Scalable, stateless, supports horizontal scaling, secure by design
- Negative: Token management complexity on frontend, no centralized logout capability
- Risk: JWT token security depends on proper secret management and validation

## References
- @specs/2-plan/phase-2-fullstack.md
- @specs/1-specify/features/feature-02-fullstack-todo.md
- @constitution.md (security requirements)