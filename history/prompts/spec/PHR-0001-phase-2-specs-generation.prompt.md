---
id: PHR-0001
title: Phase-2-Specs-Generation
stage: spec
date: 2026-02-05
surface: agent
model: claude-sonnet-4-5-20250929
feature: phase-2
branch: phase-ii
user: metachemist
command: /sp.specify
labels: ["phase-2", "specification", "todo-evolution", "fullstack", "authentication"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - specs/1-specify/phase-2-overview.md
 - specs/1-specify/features/feature-01-task-crud.md
 - specs/1-specify/features/feature-02-authentication.md
 - specs/2-plan/phase-2-fullstack.md
 - specs/2-plan/api-specs/rest-endpoints.md
 - specs/3-tasks/phase-2/task-breakdown.md
tests:
 - none
---

## Prompt

# Prompt for Claude Code CLI: Generate Phase 2 Specifications

Copy and paste this prompt to Claude Code CLI:

---

I need you to create comprehensive, production-grade specifications for Phase 2 of my Hackathon II project. I already have the file structure in place, so you MUST update existing files rather than creating new ones.

## Context

This is Phase II of a 5-phase "Evolution of Todo" project that transforms a console app into a full-stack web application with authentication and persistent storage.

**Technology Stack:**
- Frontend: Next.js 16+ (App Router), TypeScript, Tailwind CSS, Better Auth
- Backend: FastAPI, SQLModel, JWT authentication
- Database: Neon Serverless PostgreSQL
- Deployment: Vercel (frontend), Railway/Render (backend)

## Existing File Structure

My project follows this mandatory monorepo structure:

```
specs/
├── 1-specify/
│   ├── phase-2-overview.md           (EXISTS - needs content)
│   └── features/
│       ├── feature-01-task-crud.md   (EXISTS - needs content)
│       └── feature-02-authentication.md (EXISTS - needs content)
├── 2-plan/
│   ├── phase-2-fullstack.md          (EXISTS - needs content)
│   └── api-specs/
│       └── rest-endpoints.md         (EXISTS - needs content)
└── 3-tasks/
    └── phase-2/
        └── task-breakdown.md         (EXISTS - needs content)
```

## CRITICAL REQUIREMENTS

### 1. DO NOT CREATE NEW FILES
- All files listed above already exist (empty or with placeholder content)
- You MUST use `str_replace` or file editing tools to UPDATE these existing files
- DO NOT use `create_file` or suggest creating new files
- Work with the existing file structure only

### 2. File-by-File Content Requirements

#### File: `specs/1-specify/phase-2-overview.md`
Create comprehensive overview including:
- Executive summary with clear objectives
- Scope (in-scope: 5 basic CRUD features + authentication; out-of-scope: AI chatbot, advanced features)
- 3 detailed user journeys:
  - Journey 1: New user registration and first task creation
  - Journey 2: Existing user managing tasks (CRUD operations)
  - Journey 3: Multi-user data isolation verification
- Key requirements (functional and non-functional)
- Success criteria and deliverables
- Dependencies and constraints
- Risk assessment with mitigation strategies
- Acceptance criteria checklist

**Length:** 3,000-4,000 words minimum

---

#### File: `specs/1-specify/features/feature-01-task-crud.md`
Create detailed task CRUD specification including:
- 5 user stories (Create, View, Update, Delete, Mark Complete)
- Each user story with acceptance criteria
- Functional requirements (FR-2.1 through FR-2.6):
  - FR-2.1: Create Task (input, process, output, error cases)
  - FR-2.2: List Tasks (filtering by user_id, ordering)
  - FR-2.3: Get Single Task
  - FR-2.4: Update Task
  - FR-2.5: Delete Task
  - FR-2.6: Toggle Completion
- Data model (SQLModel schema)
- API endpoint specifications for each operation
- UI component specifications (TaskList, TaskItem, TaskForm, DeleteConfirmDialog)
- Business rules (title required, length limits, completion defaults)
- Edge cases and error handling
- Testing requirements

**Length:** 4,000-5,000 words minimum

---

#### File: `specs/1-specify/features/feature-02-authentication.md`
Create detailed authentication specification including:
- 5 user stories (Registration, Login, Logout, Protected Routes, Session Persistence)
- Each with detailed acceptance criteria
- Functional requirements (FR-1.1 through FR-1.5):
  - FR-1.1: User Registration (email validation, password hashing, JWT generation)
  - FR-1.2: User Login (password verification, token generation)
  - FR-1.3: JWT Token Management (creation, verification, expiration)
  - FR-1.4: User Authorization (user_id validation from URL vs JWT)
  - FR-1.5: Protected Routes
- Technical architecture (Better Auth + JWT flow)
- JWT token structure and payload
- Password requirements and bcrypt configuration
- Security requirements (SEC-201 through SEC-205)
- API endpoints (signup, signin, me, signout)
- UI components (SignUpForm, SignInForm, AuthGuard)
- Environment variables (BETTER_AUTH_SECRET shared between services)
- Error handling and user enumeration prevention

**Length:** 5,000-6,000 words minimum

---

#### File: `specs/2-plan/phase-2-fullstack.md`
Create comprehensive architectural plan including:
- High-level system architecture diagram (ASCII art showing Browser → Next.js → FastAPI → PostgreSQL)
- Component breakdown:
  - Frontend components (11+ components with responsibilities)
  - Backend components (routes, models, auth, db)
- Data flow diagrams for:
  - User registration flow (10+ steps)
  - User login flow (9+ steps)
  - Task creation flow (13+ steps)
  - Task list loading flow (10+ steps)
  - Task update flow (13+ steps)
  - Task deletion flow (10+ steps)
  - Task completion toggle flow (9+ steps)
- Database schema (SQL CREATE statements with indexes)
- Deployment architecture (dev and production environments)
- Implementation strategy (8-day timeline broken down by day)
- Technical decisions with rationale
- Security considerations
- Performance considerations
- Testing strategy

**Length:** 6,000-8,000 words minimum

---

#### File: `specs/2-plan/api-specs/rest-endpoints.md`
Create complete REST API documentation including:
- Base URLs (dev and production)
- Authentication header format
- Response format standards
- Status code reference table
- Authentication endpoints (3 endpoints):
  - POST /api/auth/signup (full request/response examples)
  - POST /api/auth/signin (full request/response examples)
  - GET /api/auth/me (full request/response examples)
- Task endpoints (6 endpoints):
  - GET /api/{user_id}/tasks
  - GET /api/{user_id}/tasks/{id}
  - POST /api/{user_id}/tasks
  - PUT /api/{user_id}/tasks/{id}
  - DELETE /api/{user_id}/tasks/{id}
  - PATCH /api/{user_id}/tasks/{id}/complete
- For EACH endpoint include:
  - Description
  - Authentication requirements
  - Path parameters
  - Request body schema (with JSON example)
  - Success response (with JSON example)
  - Error responses (all possible with examples)
  - cURL example
- CORS configuration details
- Error handling best practices
- Testing with cURL section (complete flow example)

**Length:** 4,000-5,000 words minimum

---

#### File: `specs/3-tasks/phase-2/task-breakdown.md`
Create detailed task breakdown including:
- Organization: 25 atomic tasks across 7 implementation phases
- Each task must include:
  - Task ID (T-101, T-102, etc.)
  - Title
  - Description (detailed steps)
  - Dependencies (which tasks must complete first)
  - Acceptance criteria (checklist)
  - Estimated time (in hours)
  - References to spec files

**Task Structure:**
- Phase 1: Project Setup (T-101 to T-105) - 5 tasks, ~6 hours
- Phase 2: Database & Models (T-201 to T-203) - 3 tasks, ~3 hours
- Phase 3: Authentication (T-301 to T-304) - 4 tasks, ~6 hours
- Phase 4: Task CRUD Backend (T-401 to T-405) - 5 tasks, ~3.5 hours
- Phase 5: Frontend Auth (T-501 to T-504) - 4 tasks, ~6 hours
- Phase 6: Frontend Task CRUD (T-505 to T-507) - 3 tasks, ~6 hours
- Phase 7: Polish & Testing (T-601 to T-604) - 4 tasks, ~6 hours
- Phase 8: Deployment (T-701 to T-706) - 6 tasks, ~4 hours

Include:
- 8-day implementation timeline with daily breakdown
- Dependencies graph (ASCII art or text-based)
- Progress tracking checklist
- Total estimated time: 35 hours

**Length:** 5,000-7,000 words minimum

---

## Quality Standards

### Writing Quality
- Professional, production-grade documentation
- Clear, concise, actionable language
- Use tables, code blocks, and examples extensively
- Include ASCII art diagrams where helpful
- NO vague descriptions - everything must be specific and implementable

### Technical Depth
- Every functional requirement must have:
  - Input specification
  - Process steps
  - Output specification
  - All error cases with exact error messages
- Every API endpoint must have:
  - Complete request/response examples
  - All possible HTTP status codes
  - cURL examples
- Every component must have:
  - TypeScript/Python interfaces
  - Clear responsibilities
  - Props/parameters

### Completeness
- Cover 100% of Phase II requirements:
  - User authentication (signup, signin, JWT)
  - Task CRUD (all 5 basic operations)
  - Multi-user data isolation
  - Database persistence
  - Responsive UI
  - RESTful API
  - Deployment to production

### Format
- Use Markdown with proper headers (##, ###, ####)
- Include table of contents where needed
- Use code blocks with language tags (```typescript, ```python, ```bash)
- Use tables for structured information
- Include ✅/❌ for requirements and checklists

## Reference Material

Base your specifications on these principles from my constitution.md:

**Technology Stack (Constitutional):**
- Frontend: Next.js 16+ App Router (mandatory)
- Backend: FastAPI with SQLModel (mandatory)
- Database: Neon Serverless PostgreSQL (mandatory)
- Auth: Better Auth + JWT (mandatory)

**Security Requirements:**
- Passwords hashed with bcrypt (cost factor 12)
- JWT tokens signed with BETTER_AUTH_SECRET
- All task endpoints require authentication
- user_id validation on every request
- CORS properly configured

**Code Quality Standards:**
- TypeScript strict mode (frontend)
- Python type hints (backend)
- Async/await for I/O operations
- No manual SQL - ORM only
- Input validation with Pydantic

**Architecture Principles:**
- Stateless services (no session in memory)
- JWT tokens (no server-side sessions)
- Database-persisted state
- Horizontal scaling ready

## Example Quality Level

Here's an example of the detail level I expect for ONE functional requirement:

```markdown
### FR-2.1: Create Task

**Input:**
- Title (string, required, 1-200 characters after trimming)
- Description (string, optional, 0-1000 characters)

**Process:**
1. Extract user_id from authenticated JWT token
2. Validate title is not empty after trimming whitespace
3. Validate title length ≤ 200 characters
4. Validate description length ≤ 1000 characters (if provided)
5. Create task record in database:
   - user_id = authenticated user from JWT
   - title = provided title (trimmed)
   - description = provided description (or null)
   - completed = false (default)
   - created_at = current UTC timestamp
   - updated_at = current UTC timestamp
6. Insert into tasks table
7. Return created task object with auto-generated ID

**Output:**
Task object with all fields including auto-generated ID

**Error Cases:**
- Empty title (after trim) → 400 "Title is required"
- Title > 200 chars → 400 "Title must be 200 characters or less"
- Description > 1000 chars → 400 "Description must be 1000 characters or less"
- Database connection failed → 500 "Failed to create task. Please try again."
- Invalid JWT token → 401 "Authentication required"
- user_id mismatch → 403 "Unauthorized to access this resource"

**Database Schema:**
```sql
INSERT INTO tasks (user_id, title, description, completed, created_at, updated_at)
VALUES ($1, $2, $3, false, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
RETURNING *;
```

**API Example:**
```bash
curl -X POST http://localhost:8000/api/user_abc123/tasks \
  -H "Authorization: Bearer eyJhbGc..." \
  -H "Content-Type: application/json" \
  -d '{"title":"Prepare Q4 presentation","description":"Slides for board meeting"}'
```
```

Apply this level of detail to EVERY functional requirement, API endpoint, and component specification.

## Output Format

For each file, provide:

1. **First:** Show me which file you're updating
   ```
   Updating: specs/1-specify/phase-2-overview.md
   ```

2. **Then:** Use str_replace or file editing to update the entire file content

3. **Do this for all 6 files** in order:
   - phase-2-overview.md
   - feature-01-task-crud.md
   - feature-02-authentication.md
   - phase-2-fullstack.md
   - rest-endpoints.md
   - task-breakdown.md

## Final Checklist

After generating all specifications, verify:

- [ ] All 6 existing files have been updated (not created)
- [ ] Total word count > 30,000 words across all files
- [ ] Every functional requirement has input/process/output/errors
- [ ] Every API endpoint has complete examples
- [ ] Every component has clear responsibilities
- [ ] 25 tasks with estimated times total to ~35 hours
- [ ] All specifications are implementable without ambiguity
- [ ] Security requirements are comprehensive
- [ ] Testing requirements are specified
- [ ] Deployment steps are detailed

## Success Criteria

These specifications should enable someone to:
1. Understand exactly what to build (no ambiguity)
2. Know exactly how to build it (clear technical approach)
3. Break work into atomic tasks (25 tasks ready to execute)
4. Implement using Claude Code with minimal questions
5. Deploy to production following step-by-step guide

Start with the first file: `specs/1-specify/phase-2-overview.md`

Remember: UPDATE existing files, do NOT create new ones. Use str_replace or file editing tools only.

## Response snapshot

Successfully generated comprehensive Phase 2 specifications by updating all 6 required files with detailed content covering full-stack application architecture, authentication system, task CRUD operations, API documentation, and implementation tasks.

## Outcome

- ✅ Impact: Complete Phase 2 specifications created for full-stack todo application with authentication
- 🧪 Tests: none
- 📁 Files: specs/1-specify/phase-2-overview.md, specs/1-specify/features/feature-01-task-crud.md, specs/1-specify/features/feature-02-authentication.md, specs/2-plan/phase-2-fullstack.md, specs/2-plan/api-specs/rest-endpoints.md, specs/3-tasks/phase-2/task-breakdown.md
- 🔁 Next prompts: /sp.plan to create implementation plan based on these specs
- 🧠 Reflection: Detailed specifications provide clear roadmap for Phase 2 implementation

## Evaluation notes (flywheel)

- Failure modes observed: None - all specifications created successfully as requested
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): None needed - comprehensive specifications completed