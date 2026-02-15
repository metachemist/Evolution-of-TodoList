---
id: "0006"
title: generate-and-review-frontend-tasks
stage: tasks
date: 2026-02-14
surface: claude-code
model: claude-opus-4-6
feature: 006-nextjs-todo-frontend
branch: 006-nextjs-todo-frontend
user: metachemist
command: /sp.tasks
labels: [tasks, frontend, nextjs, atomic-tasks, review, quality-audit]
links:
  spec: specs/1-specify/phase-2/feature-02-nextjs-todo-frontend.md
  plan: specs/2-plan/phase-2/phase-2-nextjs-todo-frontend.md
  tasks: specs/3-tasks/phase-2/nextjs-todo-frontend-tasks.md
  ticket: ""
---

## Prompt

User requested `/sp.tasks` to generate atomic tasks from the frontend implementation plan, then asked for a 5-point review:
1. Is each task atomic (ONE thing, ONE acceptance criterion)?
2. Are they sized right (15-30 minutes)?
3. Can each be reviewed independently?
4. Identify tasks to split or combine.
5. Which tasks to add or remove?

## Response

Generated `specs/3-tasks/phase-2/nextjs-todo-frontend-tasks.md` with 67 tasks across 9 phases:
- Phase 1: Setup (3 tasks)
- Phase 2: Foundational (13 tasks) — includes UI primitives (Button, Input, Modal) moved here from US3 to fix dependency inversion
- Phases 3-8: 6 User Stories (28 tasks total)
- Phase 9: Polish & Testing (23 tasks)

5-point review found and fixed:
- **3 splits**: API client (fetch wrapper + error catalog), dashboard layout (RSC auth + nav bar), TaskItem wiring (toggle + delete)
- **2 combines**: runtime + dev npm install, .env.example into Tailwind config task
- **2 additions**: test setup file (`__tests__/setup.ts` for MSW), root page redirect (`app/page.tsx`)
- **1 reorder**: Button/Input/Modal moved from Phase 5 (US3) to Phase 2 (Foundational) — LoginForm and RegisterForm depend on these primitives

Final metrics: 67 tasks, 32 parallel opportunities, MVP at 30 tasks (Phase 1-4).
