# Todo Evolution - Claude Code Instructions

Welcome to the Todo Evolution project! This file provides entry-point instructions for Claude Code to work effectively on this project.

## Project Overview

This is a 5-phase evolution project that progresses from a simple CLI todo application to a cloud-native AI system:
1. **Phase I**: Console application (Python)
2. **Phase II**: Full-stack web application (Next.js + FastAPI)
3. **Phase III**: AI chatbot integration (MCP tools)
4. **Phase IV**: Kubernetes deployment (Docker + Helm)
5. **Phase V**: Cloud production (Kafka + Dapr)

## Critical References

### Authoritative Documents
- **[@AGENTS.md](./AGENTS.md)**: Complete agent behavior specification (READ FIRST)
- **[constitution.md](./constitution.md)**: Supreme law with all principles and constraints
- **[specs/](./specs/)**: Source of truth for requirements, architecture, and tasks

### Monorepo Structure
```
evolution-of-todo-list-01/
├── constitution.md                 # Supreme law
├── AGENTS.md                     # Agent behavior specification
├── CLAUDE.md                     # This file
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

## Working Protocol

### Before Starting Any Work
1. **READ [@AGENTS.md](./AGENTS.md)** - Understand complete agent behavior
2. **Review [constitution.md](./constitution.md)** - Know constitutional constraints
3. **Locate relevant specs** in `specs/` directory
4. **Find specific tasks** in `specs/3-tasks/` before implementing
5. **Verify monorepo structure** compliance

### Implementation Guidelines
- **Task Reference Required**: Every code file must reference a task ID from `specs/3-tasks/`
- **Follow Phase Progression**: Don't implement Phase II features during Phase I
- **Constitution Compliance**: Always prioritize constitutional principles
- **Spec-Driven**: Implement only what's specified in `specs/1-specify/`
- **Architecture Compliant**: Follow patterns defined in `specs/2-plan/`

### File Referencing
Use the `@` notation to reference project files:
- `@specs/1-specify/features/feature-01-task-crud.md` - Specifications
- `@specs/3-tasks/phase-2/T-102-fastapi-setup.md` - Tasks
- `@backend/src/routes/tasks.py` - Implementation files
- `@infra/k8s/backend/deployment.yaml` - Infrastructure

## Quality Gates

Before completing any work, ensure:
1. **Constitutional compliance** - All principles followed
2. **Spec traceability** - Links back to specifications
3. **Task reference** - Every file links to a task
4. **Monorepo structure** - Proper directory placement
5. **Quality standards** - As defined in constitution

## Quick Navigation

- **Specifications**: `@specs/1-specify/`
- **Architecture Plans**: `@specs/2-plan/`
- **Implementation Tasks**: `@specs/3-tasks/`
- **Frontend Code**: `@frontend/`
- **Backend Code**: `@backend/`
- **Infrastructure**: `@infra/`

---

*This file serves as a shim to [@AGENTS.md](./AGENTS.md) - for complete agent behavior, please read that file first.*