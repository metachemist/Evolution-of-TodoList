---
id: 1
title: Update Hackathon II Todo Evolution Constitution
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
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
  - history/prompts/constitution/1-update-hackathon-ii-todo-evolution.constitution.prompt.md
tests: []
outcome: Successfully updated the project constitution with comprehensive principles
  for the Todo Evolution project, replacing all template placeholders with concrete
  content.
evaluation: The constitution now properly reflects the Hackathon II Todo Evolution
  project requirements with all principles, constraints, and guidelines clearly defined.
---

# Update Hackathon II Todo Evolution Constitution

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

### 1. Technology Stack (Non-Negotiable)

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

#### Root Level
- **README.md:** Setup instructions, architecture overview, deployment guide
- **CLAUDE.md:** Instructions for Claude Code (@AGENTS.md)
- **AGENTS.md:** Complete agent behavior specification
- **constitution.md:** This file

#### Specs Folder Structure
```
/specs
  /overview.md          # Project overview
  /architecture.md      # System architecture
  /features/            # Feature specifications
    /task-crud.md
    /authentication.md
    /chatbot.md
  /api/                 # API specifications
    /rest-endpoints.md
    /mcp-tools.md
  /database/            # Database specifications
    /schema.md
  /ui/                  # UI specifications
    /components.md
    /pages.md
```

#### Service-Specific
- **frontend/CLAUDE.md:** Frontend-specific patterns
- **backend/CLAUDE.md:** Backend-specific patterns

### Documentation Standards
- **Markdown Format:** All docs in Markdown
- **Code Examples:** Include working code snippets
- **Diagrams:** Use ASCII art or Mermaid for architecture
- **Updates:** Keep docs in sync with code changes

---

## Forbidden Practices

### What Agents Must NEVER Do

1. **Generate code without a Task ID reference**
2. **Modify architecture without updating `speckit.plan`**
3. **Add features without updating `speckit.specify`**
4. **Change tech stack without constitutional amendment**
5. **Commit secrets or credentials to Git**
6. **Use synchronous I/O for network/database calls**
7. **Write SQL directly instead of using ORM**
8. **Skip error handling for external calls**
9. **Create stateful services (holding session in memory)**
10. **Deploy without testing in Minikube first (Phase IV+)**

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

1. **Constitution.md** (This document) - Highest authority
2. **speckit.specify** - What we're building
3. **speckit.plan** - How we're building it
4. **speckit.tasks** - Breakdown of work
5. **Implementation** - The code itself

**Example:** If code contradicts the plan, the plan wins. If the plan contradicts the specification, the specification wins. If the specification contradicts the constitution, the constitution wins.

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

1. ✅ All features in phase specification are implemented
2. ✅ All tests pass (unit + integration)
3. ✅ Application deploys successfully
4. ✅ Demo video demonstrates all features (< 90 seconds)
5. ✅ Documentation is updated (README, specs)
6. ✅ Code is pushed to public GitHub repo
7. ✅ No secrets in repository
8. ✅ Claude Code can regenerate from specs

### Quality Gates

Before submission:

- **Security:** No exposed secrets, proper authentication
- **Performance:** Meets response time targets
- **Scalability:** Services are stateless
- **Maintainability:** Code follows standards
- **Documentation:** Complete and accurate

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

Successfully created the Todo Evolution Constitution file with comprehensive principles for the Hackathon II project. The constitution establishes:

- Core philosophy emphasizing Spec-Driven Development (SDD), progressive evolution, and AI-native architecture
- Detailed technical constraints across five development phases
- Development workflow following the SDD loop
- Security and privacy standards
- Code quality standards for Python and TypeScript
- Architecture patterns including stateless services and MCP tools
- Database design standards with SQLModel patterns
- API design standards with RESTful principles
- Cloud-native principles for Kubernetes and Dapr
- Performance and scalability targets
- Testing standards with unit, integration, and end-to-end testing
- Documentation requirements
- Forbidden practices for agents
- Conflict resolution hierarchy
- Success criteria and bonus points alignment

All template placeholders were replaced with concrete content specific to the Todo Evolution project, creating a comprehensive governance document for the development team.