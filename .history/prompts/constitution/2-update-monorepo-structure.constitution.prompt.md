---
id: 2
title: Update Monorepo Structure Constitution
stage: constitution
date: '2026-02-04'
surface: agent
model: claude-sonnet-4-5-20250929
feature: todo-evolution
branch: main
user: metachemist
command: /sp.constitution
labels:
  - constitution
  - todo-evolution
  - hackathon
  - monorepo
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
  - history/prompts/constitution/2-update-monorepo-structure.constitution.prompt.md
tests: []
outcome: Successfully updated the constitution with mandatory monorepo structure
  section and enhanced documentation requirements.
evaluation: The constitution now properly reflects all requirements including the
  critical monorepo structure mandate and updated documentation standards.
---

# Update Monorepo Structure Constitution

## Original Prompt

```text
# Constitution.md
## Hackathon II: Todo Spec-Driven Development Project

**Version:** 1.0
**Last Updated:** February 4, 2026
**Project:** Evolution of Todo - From CLI to Cloud-Native AI Systems

---

## Purpose

This constitution establishes the immutable principles, constraints, and standards that govern all development decisions in the Todo Evolution project. Every agent, developer, and implementation must honor these rules. This document serves as the **WHY** - the foundational reasoning behind our architectural and technical choices.

---

## Core Philosophy

### Spec-Driven Development (SDD) First

**Principle:** No code exists without a specification.

- **Every feature must have a written specification before implementation**
- Specifications must be refined until Claude Code generates correct output
- Manual coding is prohibited - all implementation must flow through Claude Code + Spec-Kit Plus
- The specification is the contract; the code is the fulfillment

**Rationale:** Spec-Driven Development transforms developers from syntax writers to system architects, aligning perfectly with AI-native software engineering.

### Progressive Evolution Over Big Bang

**Principle:** Build iteratively, from simple to complex.

- Start with working fundamentals (console app)
- Add layers of sophistication incrementally (web → AI → cloud)
- Each phase must be fully functional before advancing
- Never skip phases; each builds essential foundations

**Rationale:** Real-world software evolves. Understanding this evolution builds better architects.

### AI-Native Architecture

**Principle:** Design for AI agents as first-class citizens.

- Natural language interfaces are not add-ons; they're core features
- MCP (Model Context Protocol) tools are primary interaction patterns
- Stateless, event-driven designs enable AI scalability
- Human interfaces and AI interfaces must have feature parity

**Rationale:** The future of software is conversational and agent-driven.

---

## Technical Constraints

### 1. Project Structure (Mandatory Monorepo)

**Principle:** All phases must follow this exact directory structure.

This project **MUST** use the following monorepo structure. Deviations are not permitted without constitutional amendment.

```
evolution-of-todo-list-01/
├── constitution.md                 # The Supreme Law (Principles & Constraints)
├── AGENTS.md                      # AI Agent Instructions (The "How-To")
├── CLAUDE.md                      # Claude Code entry point (Shim to AGENTS.md)
├── README.md                      # Project onboarding
│
├── .specify/                      # SpecifyPlus Tool Configuration
│   ├── config.yaml               # Tool settings
│   └── templates/                # Templates for Spec/Plan/Task generation
│       ├── spec-template.md
│       ├── plan-template.md
│       └── tasks-template.md
│
├── specs/                         # The Source of Truth (Lifecycle Stages)
│   │
│   ├── 1-specify/                # STEP 1: WHAT (Requirements & Context)
│   │   ├── system-overview.md    # High-level goals
│   │   ├── features/             # Feature Requirements
│   │   │   ├── feature-01-task-crud.md
│   │   │   ├── feature-02-auth.md
│   │   │   ├── feature-03-chatbot.md
│   │   │   ├── feature-04-recurring-tasks.md
│   │   │   └── feature-05-reminders.md
│   │   ├── domain/               # Domain Rules & Entities
│   │   │   ├── task-entity.md
│   │   │   ├── user-entity.md
│   │   │   └── conversation-entity.md
│   │   └── user-journeys/        # User Stories
│   │       ├── journey-01-basic-todo.md
│   │       ├── journey-02-ai-chat.md
│   │       └── journey-03-advanced-features.md
│   │
│   ├── 2-plan/                   # STEP 2: HOW (Architecture & Design)
│   │   ├── phase-1-console.md
│   │   ├── phase-2-fullstack.md
│   │   ├── phase-3-ai-chatbot.md
│   │   ├── phase-4-kubernetes.md
│   │   ├── phase-5-cloud.md
│   │   ├── api-specs/            # API Contracts (OpenAPI/MCP)
│   │   │   ├── rest-endpoints.md
│   │   │   ├── mcp-tools.md
│   │   │   └── websocket-events.md
│   │   ├── db-schema/            # Data Models (SQLModel)
│   │   │   ├── schema-v1.md
│   │   │   ├── schema-v2.md
│   │   │   └── migrations.md
│   │   └── ui-design/            # Component Architecture
│   │       ├── components.md
│   │       ├── pages.md
│   │       └── chatkit-integration.md
│   │
│   └── 3-tasks/                  # STEP 3: EXECUTE (Atomic Units)
│       ├── phase-1/
│       │   ├── T-001-setup-project.md
│       │   ├── T-002-core-logic.md
│       │   ├── T-003-cli-interface.md
│       │   └── T-004-testing.md
│       ├── phase-2/
│       │   ├── T-101-nextjs-setup.md
│       │   ├── T-102-fastapi-setup.md
│       │   ├── T-103-database-models.md
│       │   ├── T-104-auth-setup.md
│       │   └── ...
│       ├── phase-3/
│       │   ├── T-201-mcp-server.md
│       │   ├── T-202-agents-sdk.md
│       │   ├── T-203-chatkit-ui.md
│       │   └── ...
│       ├── phase-4/
│       │   ├── T-301-dockerfiles.md
│       │   ├── T-302-helm-charts.md
│       │   └── ...
│       └── phase-5/
│           ├── T-401-kafka-setup.md
│           ├── T-402-dapr-integration.md
│           └── ...
│
├── src/                           # STEP 4: IMPLEMENTATION (Phase I)
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── task_manager.py
│   │   └── models.py
│   ├── cli/
│   │   ├── __init__.py
│   │   └── main.py
│   └── tests/
│       ├── __init__.py
│       ├── test_task_manager.py
│       └── test_cli.py
│
├── frontend/                      # STEP 4: IMPLEMENTATION (Phase II+)
│   ├── CLAUDE.md                 # Frontend-specific Claude instructions
│   ├── package.json
│   ├── next.config.js
│   ├── tsconfig.json
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx
│   │   │   └── api/
│   │   ├── components/
│   │   │   ├── TaskList.tsx
│   │   │   ├── TaskForm.tsx
│   │   │   └── ChatInterface.tsx
│   │   └── lib/
│   │       ├── api.ts
│   │       └── auth.ts
│   └── public/
│
├── backend/                       # STEP 4: IMPLEMENTATION (Phase II+)
│   ├── CLAUDE.md                 # Backend-specific Claude instructions
│   ├── pyproject.toml
│   ├── src/
│   │   ├── __init__.py
│   │   ├── main.py               # FastAPI app entry
│   │   ├── models.py             # SQLModel models
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── tasks.py
│   │   │   ├── chat.py
│   │   │   └── auth.py
│   │   ├── mcp/
│   │   │   ├── __init__.py
│   │   │   ├── server.py
│   │   │   └── tools.py
│   │   ├── agents/
│   │   │   ├── __init__.py
│   │   │   └── todo_agent.py
│   │   └── db/
│   │       ├── __init__.py
│   │       └── connection.py
│   └── tests/
│       ├── __init__.py
│       ├── test_api.py
│       └── test_mcp.py
│
├── infra/                         # STEP 4: INFRASTRUCTURE (Phase IV+)
│   ├── docker/
│   │   ├── frontend.Dockerfile
│   │   ├── backend.Dockerfile
│   │   └── docker-compose.yml
│   ├── k8s/
│   │   ├── namespace.yaml
│   │   ├── frontend/
│   │   │   ├── deployment.yaml
│   │   │   ├── service.yaml
│   │   │   └── ingress.yaml
│   │   ├── backend/
│   │   │   ├── deployment.yaml
│   │   │   ├── service.yaml
│   │   │   └── configmap.yaml
│   │   └── kafka/
│   │       └── strimzi-kafka.yaml
│   ├── helm/
│   │   └── todo-app/
│   │       ├── Chart.yaml
│   │       ├── values.yaml
│   │       ├── values-dev.yaml
│   │       ├── values-prod.yaml
│   │       └── templates/
│   │           ├── deployment.yaml
│   │           ├── service.yaml
│   │           └── ingress.yaml
│   └── dapr/
│       ├── components/
│       │   ├── kafka-pubsub.yaml
│       │   ├── state-store.yaml
│       │   └── secrets.yaml
│       └── configurations/
│           └── tracing.yaml
│
├── .gitignore
├── .env.example
└── pyproject.toml                 # Root Python project config
```

#### Directory Structure Rules

**Root Level Files (Mandatory):**
- `constitution.md` - This document (supreme authority)
- `AGENTS.md` - Complete agent behavior specification
- `CLAUDE.md` - Entry point for Claude Code (must reference @AGENTS.md)
- `README.md` - Project setup and deployment guide

**Spec Organization (Mandatory):**
- `specs/1-specify/` - Contains WHAT we're building (requirements)
- `specs/2-plan/` - Contains HOW we're building it (architecture)
- `specs/3-tasks/` - Contains atomic work units with Task IDs

**Implementation Organization (Mandatory):**
- `src/` - Phase I console app only
- `frontend/` - Phase II+ Next.js application
- `backend/` - Phase II+ FastAPI application
- `infra/` - Phase IV+ Kubernetes/Docker/Helm configurations

**Per-Service CLAUDE.md (Required for Phase II+):**
- `frontend/CLAUDE.md` - Frontend-specific patterns and conventions
- `backend/CLAUDE.md` - Backend-specific patterns and conventions

#### Why This Structure is Mandatory

**Reason 1: Spec-Driven Development**
- Clear separation between WHAT (specify), HOW (plan), and EXECUTE (tasks)
- Claude Code can navigate specifications hierarchically
- Every implementation file traces back to a task in `specs/3-tasks/`

**Reason 2: Monorepo Benefits**
- Single context for Claude Code (sees entire project)
- Cross-cutting changes (frontend + backend) in one session
- Shared specifications across all services
- Unified version control and deployment

**Reason 3: Progressive Evolution**
- `src/` contains Phase I (simple start)
- `frontend/` and `backend/` added in Phase II (complexity grows)
- `infra/` added in Phase IV (cloud-native layers)
- Each phase builds on previous structure without restructuring

**Reason 4: Agent Navigation**
- Claude Code reads root `CLAUDE.md` → references `AGENTS.md`
- Knows to check `specs/` before implementing
- Finds service-specific guidance in `frontend/CLAUDE.md` or `backend/CLAUDE.md`
- Can reference any spec with `@specs/1-specify/features/feature-01.md`

#### Violation Policy

**Forbidden Actions:**
- ❌ Creating flat `/specs` folder without 1-specify/2-plan/3-tasks structure
- ❌ Mixing Phase I code with Phase II code in same directory
- ❌ Creating separate repos for frontend/backend
- ❌ Putting infrastructure code in application folders
- ❌ Skipping `CLAUDE.md` files in service directories

**Required Actions:**
- ✅ Use exact directory names as specified above
- ✅ Create service-specific `CLAUDE.md` when adding new services
- ✅ Organize all specs under `specs/1-specify/`, `specs/2-plan/`, `specs/3-tasks/`
- ✅ Keep infrastructure separate in `infra/`
- ✅ Maintain clear phase separation (src/ → frontend/backend/ → infra/)

#### Initialization Checklist

Before starting Phase I, verify this structure exists:
```bash
# Required root files
[ ] constitution.md
[ ] AGENTS.md
[ ] CLAUDE.md
[ ] README.md

# Required directories
[ ] .specify/
[ ] specs/1-specify/
[ ] specs/2-plan/
[ ] specs/3-tasks/
[ ] src/

# Before Phase II, add:
[ ] frontend/
[ ] frontend/CLAUDE.md
[ ] backend/
[ ] backend/CLAUDE.md

# Before Phase IV, add:
[ ] infra/docker/
[ ] infra/k8s/
[ ] infra/helm/
```

**Rationale:** This structure is not arbitrary. It embodies spec-driven development principles and enables Claude Code to effectively navigate, understand, and implement your project across all five phases.

### 2. Technology Stack (Non-Negotiable)

#### Phase I: Console App
- **Language:** Python 3.13+
- **Package Manager:** UV
- **Development:** Claude Code + Spec-Kit Plus
- **Storage:** In-memory only

#### Phase II: Web Application
- **Frontend:** Next.js 16+ (App Router only)
- **Backend:** Python FastAPI
- **ORM:** SQLModel
- **Database:** Neon Serverless PostgreSQL
- **Authentication:** Better Auth with JWT

#### Phase III: AI Chatbot
- **Chat UI:** OpenAI ChatKit
- **AI Framework:** OpenAI Agents SDK
- **MCP:** Official MCP SDK (Python)
- **Architecture:** Stateless server, database-persisted state

#### Phase IV: Local Kubernetes
- **Containerization:** Docker (via Docker Desktop)
- **Orchestration:** Kubernetes (Minikube)
- **Package Manager:** Helm Charts
- **AIOps:** kubectl-ai, kagent, Gordon (Docker AI Agent)

#### Phase V: Cloud Deployment
- **Cloud Platform:** Azure (AKS) / Google Cloud (GKE) / Oracle (OKE)
- **Event Streaming:** Kafka (Confluent/Redpanda Cloud or Strimzi)
- **Runtime:** Dapr (Distributed Application Runtime)
- **CI/CD:** GitHub Actions

**Violation Policy:** Using alternative technologies requires constitutional amendment via spec update.

### 2. Development Workflow (Strict)

**The SDD Loop:**
```
Specify (WHAT) → Plan (HOW) → Tasks (BREAKDOWN) → Implement (CODE)
```

#### Rules:
1. **No Task ID = No Code:** Every code file must reference a task from `speckit.tasks`
2. **No Manual Coding:** All implementation through Claude Code
3. **Spec Refinement Over Code Fixes:** If output is wrong, refine the spec, don't patch code
4. **Documentation First:** README.md, CLAUDE.md, and specs must exist before implementation
5. **Version Control:** Every phase completion requires a git tag (e.g., `phase-1-complete`)

### 3. Security & Privacy Standards

#### Authentication & Authorization
- **User Isolation:** Every user sees only their own data
- **JWT Tokens:** Better Auth tokens required for all API calls
- **Token Validation:** Backend must verify JWT on every request
- **User ID Matching:** URL `user_id` must match JWT claims

#### Data Protection
- **Secrets Management:** Never commit secrets to Git
- **Environment Variables:** Use `.env` files (git-ignored)
- **Database Security:** Connection strings via environment only
- **API Keys:** Stored in Kubernetes Secrets or Dapr Secret Store (Phase IV+)

#### API Security
- **401 Unauthorized:** For missing/invalid tokens
- **403 Forbidden:** For authorization failures
- **Input Validation:** All user inputs must be validated
- **SQL Injection Prevention:** SQLModel ORM only, no raw SQL

### 4. Code Quality Standards

#### Python (Backend)
- **Type Hints:** Required for all function signatures
- **Async/Await:** Use async functions for I/O operations
- **Error Handling:** Try/except blocks for external calls (DB, API, Kafka)
- **Logging:** Use structured logging (JSON format preferred)
- **Testing:** Unit tests for business logic (target 70%+ coverage)

#### TypeScript/JavaScript (Frontend)
- **TypeScript:** Strict mode enabled
- **React Patterns:** Server components by default, client components for interactivity only
- **API Calls:** Centralized in `/lib/api.ts`
- **Styling:** Tailwind CSS only, no inline styles
- **Error Boundaries:** Wrap async components in error boundaries

#### General
- **DRY Principle:** Don't Repeat Yourself - extract reusable functions
- **Single Responsibility:** Each function/component does one thing well
- **Naming Conventions:**
  - Python: `snake_case` for functions/variables
  - JavaScript: `camelCase` for functions/variables
  - Components: `PascalCase`
- **File Organization:** Feature-based folders over type-based

### 5. Architecture Patterns

#### Stateless Services
**Principle:** Services must not hold session state in memory.

- **Conversation State:** Persisted to database, not server memory
- **User Sessions:** JWT tokens, not server-side sessions
- **Horizontal Scaling:** Any instance can handle any request
- **Crash Recovery:** Service restarts lose no data

**Rationale:** Cloud-native applications must scale horizontally and survive failures.

#### Event-Driven Architecture (Phase V)
**Principle:** Services communicate via events, not direct calls.

- **Kafka Topics:** task-events, reminders, task-updates
- **Producer Pattern:** Publish events after state changes
- **Consumer Pattern:** Subscribe to events, act asynchronously
- **Idempotency:** Event handlers must handle duplicate events safely

**Rationale:** Decoupling enables independent scaling and evolution of services.

#### MCP Tool Design
**Principle:** Every AI capability maps to an MCP tool.

- **Stateless Tools:** Tools read/write to database, not memory
- **Clear Contracts:** Input/output schemas in specifications
- **Error Responses:** Structured error objects, not exceptions
- **Composability:** Tools can be chained by agents

**Example Tools:**
- `add_task(user_id, title, description)` → `{task_id, status, title}`
- `list_tasks(user_id, status)` → `Array<Task>`
- `complete_task(user_id, task_id)` → `{task_id, status, title}`

### 6. Database Design Standards

#### Schema Principles
- **User Isolation:** All tables with user data include `user_id` foreign key
- **Timestamps:** Every table has `created_at` and `updated_at`
- **Soft Deletes:** Consider `deleted_at` instead of hard deletes for audit trail
- **Indexing:** Index all foreign keys and frequently queried fields

#### Migration Strategy
- **Version Control:** All schema changes via migration scripts
- **Backwards Compatible:** Migrations must not break existing deployments
- **Rollback Plan:** Every migration has a down script

#### Models
```python
# Standard pattern for all models
class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=200)
    description: str | None = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### 7. API Design Standards

#### RESTful Principles
- **Resource-Based URLs:** `/api/{user_id}/tasks` not `/api/get-tasks`
- **HTTP Methods:** GET (read), POST (create), PUT (update), DELETE (delete), PATCH (partial)
- **Status Codes:**
  - 200 OK - Success
  - 201 Created - Resource created
  - 400 Bad Request - Invalid input
  - 401 Unauthorized - Missing/invalid token
  - 403 Forbidden - Insufficient permissions
  - 404 Not Found - Resource doesn't exist
  - 500 Internal Server Error - Server error

#### Response Format
```json
{
  "success": true,
  "data": { ... },
  "error": null
}
```

Or for errors:
```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "TASK_NOT_FOUND",
    "message": "Task with ID 123 not found"
  }
}
```

### 8. Cloud-Native Principles (Phase IV & V)

#### Containerization
- **Single Responsibility:** One service per container
- **Minimal Base Images:** Use alpine or distroless when possible
- **Health Checks:** Every container exposes `/health` endpoint
- **Graceful Shutdown:** Handle SIGTERM properly

#### Kubernetes Resources
- **Resource Limits:** All pods have CPU/memory limits
- **Readiness Probes:** Don't route traffic until service is ready
- **Liveness Probes:** Restart unhealthy containers
- **ConfigMaps:** For configuration, not Secrets
- **Secrets:** For sensitive data only

#### Helm Charts
- **Values:** All environment-specific config in `values.yaml`
- **Templates:** Parameterize all variable elements
- **Dependencies:** Declare chart dependencies explicitly
- **Versioning:** Semantic versioning for chart releases

#### Dapr Integration (Phase V)
- **Pub/Sub:** Use Dapr for Kafka abstraction
- **State Management:** Optional - prefer direct DB for simplicity
- **Service Invocation:** Use for cross-service calls
- **Secrets:** Use Dapr Secret Store or Kubernetes Secrets
- **Jobs API:** Use for scheduled reminders (preferred over cron)

---

## Performance & Scalability

### Response Time Targets
- **API Endpoints:** < 200ms (p95)
- **AI Chat Response:** < 3s (p95)
- **Database Queries:** < 50ms (p95)

### Scalability Targets
- **Concurrent Users:** Support 1,000+ (Phase V)
- **Tasks per User:** Support 10,000+ tasks
- **Horizontal Scaling:** All services must scale to N replicas

### Optimization Strategies
- **Database Indexing:** Index all foreign keys and query filters
- **Caching:** Consider Redis for hot data (optional advanced feature)
- **Connection Pooling:** Reuse database connections
- **Async I/O:** Never block the event loop

---

## Testing Standards

### Required Testing Levels

#### Unit Tests
- **Coverage Target:** 70%+ for business logic
- **Focus:** Pure functions, business rules, data transformations
- **Framework:** pytest (Python), Jest (JavaScript)

#### Integration Tests
- **Database:** Test actual DB operations with test database
- **API:** Test REST endpoints with real HTTP calls
- **MCP Tools:** Test tool invocation and responses

#### End-to-End Tests (Optional but Recommended)
- **User Flows:** Test complete user journeys
- **Tools:** Playwright (web), pytest (API)

### Testing Principles
- **Test Isolation:** Each test is independent
- **Deterministic:** Same input = same output, always
- **Fast Feedback:** Tests run in < 30 seconds
- **CI Integration:** All tests run on every PR

---

## Documentation Requirements

### Required Files

All documentation must follow the mandatory monorepo structure defined in Section 1 (Project Structure).

#### Root Level (Mandatory)
- **constitution.md:** This file - the supreme law
- **AGENTS.md:** Complete agent behavior specification
- **CLAUDE.md:** Entry point for Claude Code (must contain `@AGENTS.md`)
- **README.md:** Setup instructions, architecture overview, deployment guide

#### Specs Folder Structure (Mandatory)
The `specs/` directory must follow the three-stage lifecycle:

```
/specs
  ├── 1-specify/              # WHAT we're building
  │   ├── system-overview.md
  │   ├── features/
  │   ├── domain/
  │   └── user-journeys/
  │
  ├── 2-plan/                 # HOW we're building it
  │   ├── phase-N-name.md     (one per phase)
  │   ├── api-specs/
  │   ├── db-schema/
  │   └── ui-design/
  │
  └── 3-tasks/                # Atomic work units
      ├── phase-1/
      ├── phase-2/
      ├── phase-3/
      ├── phase-4/
      └── phase-5/
```

#### Service-Specific (Required for Phase II+)
- **frontend/CLAUDE.md:** Frontend-specific patterns (Next.js, React, Tailwind)
- **backend/CLAUDE.md:** Backend-specific patterns (FastAPI, SQLModel, MCP)

#### Optional but Recommended
- **infra/README.md:** Infrastructure deployment guide
- **CHANGELOG.md:** Version history and phase completion dates

### Documentation Standards
- **Markdown Format:** All docs in Markdown
- **Code Examples:** Include working code snippets
- **Diagrams:** Use ASCII art or Mermaid for architecture
- **Updates:** Keep docs in sync with code changes
- **Spec References:** Use relative paths from project root
  - Example: `@specs/1-specify/features/feature-01-task-crud.md`
  - Example: `@specs/2-plan/api-specs/rest-endpoints.md`
  - Example: `@specs/3-tasks/phase-2/T-102-fastapi-setup.md`

### File Reference Patterns

When agents reference files in prompts or code comments:

**Specification References:**
```python
# Implements: @specs/3-tasks/phase-2/T-103-database-models.md
# Spec: @specs/1-specify/features/feature-01-task-crud.md
# Plan: @specs/2-plan/phase-2-fullstack.md
```

**Code References:**
```python
# Frontend API client: @frontend/src/lib/api.ts
# Backend route handler: @backend/src/routes/tasks.py
# Shared model: @backend/src/models.py
```

**Infrastructure References:**
```yaml
# Helm values: @infra/helm/todo-app/values.yaml
# K8s deployment: @infra/k8s/backend/deployment.yaml
# Docker compose: @infra/docker/docker-compose.yml
```

---

## Forbidden Practices

### What Agents Must NEVER Do

1. **Violate the mandatory monorepo structure** (See Section 1)
   - Don't create flat specs/ folder without 1-specify/2-plan/3-tasks
   - Don't mix phases in wrong directories
   - Don't create separate repositories for services
2. **Generate code without a Task ID reference**
3. **Modify architecture without updating `specs/2-plan/`**
4. **Add features without updating `specs/1-specify/`**
5. **Change tech stack without constitutional amendment**
6. **Commit secrets or credentials to Git**
7. **Use synchronous I/O for network/database calls**
8. **Write SQL directly instead of using ORM**
9. **Skip error handling for external calls**
10. **Create stateful services (holding session in memory)**
11. **Deploy without testing in Minikube first (Phase IV+)**
12. **Create service directories without CLAUDE.md** (Phase II+)

### Code Smells to Avoid
- **God Functions:** Functions > 50 lines
- **Deep Nesting:** Indentation > 4 levels
- **Magic Numbers:** Use named constants
- **TODO Comments:** Create tasks instead
- **Console.log Debugging:** Use proper logging
- **Commented Code:** Delete it; Git remembers

---

## Conflict Resolution

### Hierarchy of Authority

When conflicts arise between requirements, this is the resolution order:

1. **constitution.md** (This document) - Highest authority
2. **specs/1-specify/** - What we're building (requirements, features, domain)
3. **specs/2-plan/** - How we're building it (architecture, APIs, schemas)
4. **specs/3-tasks/** - Breakdown of work (atomic tasks with IDs)
5. **Implementation** - The code itself (src/, frontend/, backend/, infra/)

**Example:** If code contradicts a task, the task wins. If a task contradicts the plan, the plan wins. If the plan contradicts the specification, the specification wins. If the specification contradicts the constitution, the constitution wins.

**Directory Structure:** The mandatory monorepo structure (Section 1) is constitutional law. Deviations require constitutional amendment.

### Amendment Process

To change this constitution:

1. Create a new spec: `constitution-amendment-v2.md`
2. Document the rationale for change
3. Update affected specifications
4. Get approval (in hackathon context: instructor/mentor review)
5. Update this file with version increment

---

## Success Criteria

### Definition of Done (Per Phase)

A phase is complete when:

1. ✅ **Monorepo structure** is correct (follows Section 1 mandatory structure)
2. ✅ **All features** in phase specification are implemented
3. ✅ **All tests** pass (unit + integration)
4. ✅ **Application deploys** successfully
5. ✅ **Demo video** demonstrates all features (< 90 seconds)
6. ✅ **Documentation** is updated (README, specs in correct directories)
7. ✅ **Code is pushed** to public GitHub repo
8. ✅ **No secrets** in repository
9. ✅ **Claude Code** can regenerate from specs
10. ✅ **Task traceability** - every code file references task IDs from `specs/3-tasks/`

### Quality Gates

Before submission:

- **Structure:** Follows mandatory monorepo layout (Section 1)
- **Traceability:** All code references task IDs from `specs/3-tasks/phase-N/`
- **Security:** No exposed secrets, proper authentication
- **Performance:** Meets response time targets
- **Scalability:** Services are stateless
- **Maintainability:** Code follows standards
- **Documentation:** Complete and in correct directories
  - Specs in `specs/1-specify/`, `specs/2-plan/`, `specs/3-tasks/`
  - Service docs in `frontend/CLAUDE.md`, `backend/CLAUDE.md`
  - Infrastructure docs in `infra/README.md`

---

## Bonus Points Alignment

### Reusable Intelligence (+200 points)

**Requirement:** Create Claude Code Subagents and Agent Skills

**Constitutional Alignment:**
- Skills must be documented in `/skills` folder
- Each skill has its own `SKILL.md` with usage examples
- Skills are composable and single-purpose
- Skills follow same SDD principles

### Cloud-Native Blueprints (+200 points)

**Requirement:** Create reusable deployment blueprints via Agent Skills

**Constitutional Alignment:**
- Blueprints are declarative YAML/JSON specifications
- Blueprints reference this constitution
- Blueprints are version-controlled
- Blueprints can deploy from spec alone

### Multi-Language Support (+100 points)

**Requirement:** Support Urdu in chatbot

**Constitutional Alignment:**
- i18n libraries only (next-intl for frontend)
- Language detection from user profile
- All UI strings externalized to translation files
- MCP tools remain English (internal protocol)

### Voice Commands (+200 points)

**Requirement:** Add voice input for todo commands

**Constitutional Alignment:**
- Web Speech API for browser-based voice
- Voice input converts to text before agent processing
- Same MCP tools handle voice and text equally
- Accessibility: voice is alternative input, not required

---

## Monitoring & Observability (Phase V)

### Logging Standards
- **Structured Logging:** JSON format
- **Log Levels:** DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Correlation IDs:** Track requests across services
- **PII Redaction:** Never log passwords, tokens, or sensitive data

### Metrics to Track
- **Request Rate:** Requests per second
- **Error Rate:** Errors per second
- **Latency:** p50, p95, p99 response times
- **Resource Usage:** CPU, memory, disk

### Alerting (Production)
- **Service Down:** Immediate alert
- **Error Rate Spike:** Alert if > 5% errors
- **Latency Degradation:** Alert if p95 > 500ms

---

## Final Notes

This constitution is a living document. As the project evolves through phases, we may discover necessary amendments. However, the **core principles** remain immutable:

1. **Spec-Driven Development is mandatory**
2. **AI-native architecture is foundational**
3. **Progressive evolution is the path**
4. **Quality over speed**
5. **Security by design**

Every line of code, every architectural decision, every deployment strategy must honor these principles.

**Remember:** We're not just building a todo app. We're mastering the art of AI-native, cloud-native, spec-driven software engineering.

---

**Version History:**
- v1.0 (2026-02-04): Initial constitution for Hackathon II

**Maintainers:**
- Panaversity Team
- PIAIC Team
- GIAIC Team

**Contact:** For constitutional amendments or clarifications, consult project mentors or submit via GitHub Issues.

---

*"The constitution is the compass. The specs are the map. The code is the journey."*
```

## Response Summary

Successfully updated the Todo Evolution Constitution with the critical mandatory monorepo structure section. The updated constitution now includes:

1. **Enhanced Project Structure Section**: Added detailed monorepo structure requirements with complete directory tree, rules, rationale, and violation policies
2. **Updated Documentation Requirements**: Enhanced to require adherence to the monorepo structure with specific file organization requirements
3. **Expanded Forbidden Practices**: Added violation of mandatory monorepo structure as the first prohibited practice
4. **Updated Success Criteria**: Now requires monorepo structure compliance as the first criterion
5. **Version Increment**: Updated from 1.0.0 to 1.0.1 to reflect the important structural changes

The constitution now properly emphasizes the mandatory monorepo structure as a constitutional requirement, making it clear that deviations require formal constitutional amendments. The structure supports progressive evolution from Phase I console app through Phase V cloud deployment while maintaining proper separation of concerns and enabling effective agent navigation.