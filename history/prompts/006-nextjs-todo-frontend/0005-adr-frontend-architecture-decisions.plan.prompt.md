---
id: "0005"
title: adr-frontend-architecture-decisions
stage: plan
date: 2026-02-13
surface: claude-code
model: claude-sonnet-4-5-20250929
feature: 006-nextjs-todo-frontend
branch: 006-nextjs-todo-frontend
user: metachemist
command: /sp.adr
labels: [adr, architecture, frontend, authentication, state-management, testing, accessibility]
links:
  spec: specs/1-specify/phase-2/feature-02-nextjs-todo-frontend.md
  ticket: ""
  adr: history/adr/0007-frontend-authentication-architecture.md
  pr: ""
files:
  - path: history/adr/0007-frontend-authentication-architecture.md
    action: created
  - path: history/adr/0008-client-side-state-and-mutation-strategy.md
    action: created
  - path: history/adr/0009-accessible-ui-component-primitives.md
    action: created
  - path: history/adr/0010-frontend-testing-strategy.md
    action: created
tests:
  - none (planning phase)
---

## Prompt

Review the generated plan and record key Architectural Decisions. Focus on decisions that: (1) affect multiple sections or phases, (2) had alternatives we considered, (3) will shape how we write the paper, (4) someone might question later.

## Response snapshot

Identified 4 decision clusters from the frontend plan and research artifacts, all passing the significance test (cross-cutting impact, multiple alternatives, will be questioned). Checked 6 existing ADRs (0001–0006) — no conflicts found; ADR-0004 (full-stack stack) and ADR-0005 (backend JWT) are referenced from new ADRs. Created ADR-0007 (Frontend Authentication Architecture — two-layer guard, httpOnly cookies, CVE-2025-29927), ADR-0008 (Client-Side State — TanStack Query optimistic pattern), ADR-0009 (Accessible UI Primitives — Radix + react-hook-form + Sonner cluster), ADR-0010 (Frontend Testing Strategy — Vitest + RTL + Playwright). Each ADR has 4 alternatives with rejection rationale and explicit positive/negative consequences.

## Outcome

- ✅ Impact: 4 permanent architecture records with full traceability to spec FRs and plan ADRs
- 🧪 Tests: N/A (planning phase)
- 📁 Files: 4 created
- 🔁 Next prompts: /sp.tasks to generate atomic task breakdown
- 🧠 Reflection: The prerequisite script fails when the feature dir (specs/006-...) doesn't exist at the constitutional path. ADR decisions were extracted directly from plan/research artifacts. Clustering rules prevented over-granular ADRs — all 9 tech decisions from research.md collapsed into 4 meaningful clusters.

## Evaluation notes (flywheel)

- Failure modes observed: prerequisites script requires feature dir at non-constitutional path
- Graders run and results (PASS/FAIL): Significance test applied to all 4 clusters — PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Update check-prerequisites.sh to also accept constitutional plan path as fallback
