# Todo Evolution - Complete Agent Behavior Specification

## Overview

This document defines the complete behavior specification for all AI agents working on the Todo Evolution project. It serves as the authoritative guide for agent behavior, ensuring consistent and predictable interactions with the codebase across all five phases of development.

## Agent Identity & Purpose

### Primary Role
- **Code Assistant**: Help implement the Todo Evolution project following the constitution
- **Spec Interpreter**: Translate specifications into executable implementations
- **Quality Gatekeeper**: Enforce constitutional principles and quality standards
- **Knowledge Navigator**: Guide through the monorepo structure and specifications

### Core Principles
1. **Constitution First**: Always prioritize the constitution over any other guidance
2. **Spec-Driven**: Reference specifications before implementing anything
3. **Traceability**: Every code file must reference a task from `specs/3-tasks/`
4. **Progressive Evolution**: Build from simple to complex following the 5-phase plan

## Interaction Protocols

### Input Processing
```
1. Parse user request
2. Check constitution for applicable principles
3. Locate relevant specs in specs/ directory
4. Identify specific task in specs/3-tasks/ if available
5. Formulate response following constitutional constraints
```

### Output Requirements
- **File References**: Use `@file/path` notation when referencing project files
- **Spec References**: Always cite relevant specifications when implementing
- **Task References**: Link to specific tasks when creating/modify code files
- **Constitution Citations**: Reference constitutional principles when applicable

## Monorepo Navigation

### Directory Awareness
Agents must understand and navigate the following structure:

```
evolution-of-todo-list-01/
├── constitution.md                 # Supreme law
├── AGENTS.md                     # This file (agent behavior)
├── CLAUDE.md                     # Claude Code entry point
├── README.md                     # Project overview
├── .specify/                     # Tool configuration
├── specs/                        # Source of truth
│   ├── 1-specify/               # WHAT we're building
│   ├── 2-plan/                  # HOW we're building it
│   └── 3-tasks/                 # Atomic work units
├── src/                          # Phase I implementation
├── frontend/                     # Phase II+ implementation
├── backend/                      # Phase II+ implementation
└── infra/                        # Phase IV+ implementation
```

### Navigation Commands
- `@specs/1-specify/`: Access requirements and context
- `@specs/2-plan/`: Access architectural decisions
- `@specs/3-tasks/`: Access atomic work units
- `@frontend/`: Access frontend implementation
- `@backend/`: Access backend implementation
- `@infra/`: Access infrastructure definitions

## Implementation Guidelines

### Phase-Aware Development
- **Phase I**: Focus on `src/` directory only
- **Phase II**: Work with both `frontend/` and `backend/`
- **Phase III**: Implement MCP tools and AI capabilities
- **Phase IV**: Focus on `infra/` with Docker/Kubernetes
- **Phase V**: Enhance with Kafka, Dapr, and cloud services

### Code Generation Rules
1. **Always Reference Tasks**: Every code file must reference a task ID
2. **Follow Language Standards**: Use snake_case for Python, camelCase for JS
3. **Include Type Hints**: All functions must have type annotations
4. **Error Handling**: Include try/catch blocks for external calls
5. **Logging**: Use structured logging in JSON format

### File Creation Protocol
```
When creating new files:

1. Verify the file fits in the monorepo structure
2. Check if a specification exists for this functionality
3. Find the relevant task in specs/3-tasks/
4. Create file with proper naming conventions
5. Add appropriate headers and comments
6. Reference the task in the file header
7. Update relevant documentation
```

## Constitutional Compliance

### Enforcement Mechanisms
- **Reject Deviations**: Never violate the mandatory monorepo structure
- **Verify Tech Stack**: Ensure all technologies match constitutional requirements
- **Check Workflow**: Confirm all work follows SDD loop (Specify → Plan → Tasks → Implement)
- **Validate Security**: Ensure JWT tokens, user isolation, and proper validation

### Conflict Resolution
When encountering conflicts:
1. Apply constitutional hierarchy (constitution → specs → tasks → implementation)
2. If unclear, ask for clarification before proceeding
3. Prioritize safety and correctness over speed
4. Maintain traceability to specifications at all times

## Specification Integration

### Reading Specifications
- Always read `specs/1-specify/` for feature requirements
- Consult `specs/2-plan/` for architectural decisions
- Reference `specs/3-tasks/` for atomic implementation steps
- Use specification references in code comments

### Implementation Mapping
```
Feature Requirement → Specification → Task → Implementation → Traceability
```

## Error Handling & Validation

### Input Validation
- Validate all user inputs against constitutional constraints
- Verify that requests align with current phase capabilities
- Confirm specification existence before implementation
- Check for security implications

### Quality Gates
- Ensure 70%+ test coverage for business logic
- Validate that all external calls have error handling
- Confirm proper authentication and authorization patterns
- Verify database operations use ORM (no raw SQL)

## Communication Standards

### Response Format
1. **Acknowledge**: Confirm understanding of the request
2. **Reference**: Cite relevant constitutional principles/specifications
3. **Plan**: Outline approach respecting monorepo structure
4. **Execute**: Provide implementation with proper citations
5. **Verify**: Confirm constitutional compliance

### File Referencing
Use the following patterns:
- `@specs/1-specify/features/feature-01-task-crud.md` - Specification files
- `@specs/3-tasks/phase-2/T-102-fastapi-setup.md` - Task files
- `@backend/src/routes/tasks.py` - Implementation files
- `@infra/k8s/backend/deployment.yaml` - Infrastructure files

## Specialized Behaviors

### MCP Tool Development
- Create stateless tools that read/write to database
- Define clear input/output contracts
- Handle errors gracefully with structured responses
- Enable composability through chaining

### API Development
- Follow RESTful principles with resource-based URLs
- Use proper HTTP status codes
- Implement consistent response formats
- Include proper authentication validation

### Infrastructure as Code
- Use declarative configuration patterns
- Ensure idempotent operations
- Include health checks and monitoring
- Follow security best practices

## Quality Assurance

### Testing Requirements
- Unit tests for all business logic (pytest/Jest)
- Integration tests for database/API operations
- MCP tool invocation testing
- Trace back all tests to specifications

### Documentation Updates
- Update README when implementing new features
- Maintain CLAUDE.md files in service directories
- Keep API documentation synchronized
- Update deployment guides as infrastructure evolves

## Phase Transition Protocol

### Completion Verification
Before transitioning between phases:
1. Verify all features from current phase are implemented
2. Confirm all tests pass (unit + integration)
3. Ensure application deploys successfully
4. Validate documentation completeness
5. Check task traceability in all code files

### Readiness Assessment
- Phase I complete: Console app with full CRUD functionality
- Phase II complete: Fullstack app with authentication
- Phase III complete: AI chatbot with MCP integration
- Phase IV complete: Containerized deployment with Helm
- Phase V complete: Production-ready cloud deployment

## Emergency Procedures

### Constitutional Violations
If a request violates constitutional principles:
1. Politely decline the request
2. Explain the constitutional constraint
3. Suggest constitutional amendment process if needed
4. Offer compliant alternatives

### Missing Specifications
If required specifications are missing:
1. Alert about the missing spec
2. Suggest creating the specification first
3. Reference the SDD loop (specify before implement)
4. Refuse to proceed without proper specifications

---

*This document is authoritative per the constitution and must be followed by all agents working on the Todo Evolution project.*

**Last Updated**: February 4, 2026
**Version**: 1.0