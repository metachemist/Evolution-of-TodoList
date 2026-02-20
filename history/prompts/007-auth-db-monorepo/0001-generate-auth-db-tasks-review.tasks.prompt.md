---
id: "0001"
title: generate-auth-db-tasks-review
stage: tasks
date: 2026-02-15
surface: claude-code
model: claude-sonnet-4-5-20250929
feature: 007-auth-db-monorepo
branch: 007-auth-db-monorepo
user: metachemist
command: /sp.tasks
labels: [tasks, auth, database, review]
links:
  spec: specs/1-specify/phase-2/feature-03-auth-db-monorepo.md
  ticket: ""
  adr: history/adr/0011-auth-session-transport-and-contract.md
  pr: ""
files:
  - specs/3-tasks/phase-2/auth-db-tasks.md
  - specs/2-plan/phase-2/api-specs/auth-and-task-contracts.md (to be created T001)
tests:
  - backend/tests/test_routes/test_auth.py (T028a/T028b)
  - backend/tests/test_routes/test_tasks_auth.py (T029)
  - backend/tests/test_services/test_auth_service.py (T030)
  - backend/tests/load/locustfile.py (T031)
---

## Prompt

Generate task list for feature 007-auth-db-monorepo (Authentication & Persistent Storage). Review the output against 5 criteria: (1) atomicity — does ONE thing with ONE acceptance criterion; (2) sizing — 15–30 minutes, not hours or minutes; (3) independent reviewability; (4) tasks to split or combine; (5) tasks to add or remove.

## Response snapshot

Generated `specs/3-tasks/phase-2/auth-db-tasks.md` with 34 tasks across 7 phases mapped to 6 user stories. Reviewed against all 5 criteria and identified:

- **7 atomicity violations**: T001 (5-section doc), T005 (engine + Alembic init), T010 (7 AuthService functions), T014 (2 endpoints), T016 (6 routes + guard), T025 (protocol + 2 adapters), T028 (11 test scenarios)
- **7 oversized tasks** (>30 min): T010 most critical at 60–90 min; T028 similar; T025, T001, T016, T029, T030 borderline
- **3 undersized tasks** (<15 min): T022, T004, T002 — combinable
- **7 splits recommended**, **3 combines recommended** → net ~40 tasks after restructuring
- **2 tasks to add**: FR-018 deployment hook (alembic upgrade head in docker-compose), rate-limit endpoint classification task
- **1 task to remove**: T027 ("verify error catalog") — not a discrete implementable unit; fold into T008 + T028b

## Outcome

- ✅ Impact: First complete atomic task list for auth-db feature; identifies all pre-implementation ambiguities before coding begins
- 🧪 Tests: Test tasks T028a/b, T029, T030 created; Locust load test T031 created with exact CLI command
- 📁 Files: specs/3-tasks/phase-2/auth-db-tasks.md created (34 tasks)
- 🔁 Next prompts: Apply split/combine recommendations to refine tasks.md; then sp.implement
- 🧠 Reflection: AuthService (T010) is the single biggest risk — 7 functions in one task is a session-killer. Always split service implementations by concern (validation vs data access).

## Evaluation notes (flywheel)

- Failure modes observed: Oversized service implementation tasks; "verify" tasks that have no concrete artifact; doc tasks conflating multiple deliverables
- Graders run and results (PASS/FAIL): Manual review against 5 criteria — 7 atomicity violations found (FAIL on atomicity gate)
- Prompt variant (if applicable): User-driven review prompt with 5 explicit criteria
- Next experiment: Pre-generate a sizing estimate (min/max) alongside each task to catch >30 min tasks before review phase
