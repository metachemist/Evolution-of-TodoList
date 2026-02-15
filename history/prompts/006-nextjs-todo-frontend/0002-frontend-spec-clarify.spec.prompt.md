---
id: "0002"
title: frontend-spec-clarify
stage: spec
date: 2026-02-13
surface: claude-code
model: claude-opus-4-6
feature: 006-nextjs-todo-frontend
branch: 006-nextjs-todo-frontend
user: metachemist
command: /sp.clarify
labels: [frontend, clarification, spec, phase-2]
links:
  spec: specs/1-specify/phase-2/feature-02-nextjs-todo-frontend.md
  ticket: ""
  adr: ""
  pr: ""
files:
  - path: specs/1-specify/phase-2/feature-02-nextjs-todo-frontend.md
    action: modified
tests:
  - none (specification clarification phase)
---

## Prompt

/sp.clarify — Run structured ambiguity scan and interactive clarification on the Next.js Todo Frontend specification.

## Response snapshot

Asked 5 clarification questions, all answered. Updated spec with:
1. Token storage: httpOnly cookie set by backend. Added `/api/auth/me` and `/api/auth/logout` endpoints to API contract. Updated FR-003, FR-006, FR-020, User Session entity, and assumptions.
2. Form UX: Modal dialog for both create and edit. Updated FR-008, FR-009, FR-010 and all acceptance scenarios in User Stories 3 and 4.
3. Optimistic updates: All mutations update UI immediately with rollback on failure via error toast (5s, dismissible). Updated FR-009, FR-010, FR-011, FR-012. Added optimistic rollback edge case.
4. Description truncation: 2-line truncation with ellipsis in list view. Added FR-024. Updated User Story 2.
5. Post-action feedback: Success toasts (3s, auto-dismiss) for create/edit/delete. Focus returns to trigger element. No toast for toggle. Added FR-025. Updated acceptance scenarios.

Total FRs: 20 → 25. Clarifications section added to spec.

## Outcome

- Impact: Resolved all 5 critical ambiguities identified in scan
- Tests: N/A (specification phase)
- Files: 1 file modified (spec), 1 file created (this PHR)
- Next prompts: `/sp.plan` to design frontend architecture
- Reflection: All questions were in the Interaction & UX Flow and Constraints & Tradeoffs categories as predicted. Token storage question had the highest downstream impact (requires backend changes).

## Evaluation notes (flywheel)

- Failure modes observed: None — all questions answered cleanly with single option selection
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
