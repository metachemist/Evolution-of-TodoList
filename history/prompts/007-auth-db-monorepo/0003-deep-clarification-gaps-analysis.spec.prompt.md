---
id: "0003"
title: deep-clarification-gaps-analysis
stage: spec
date: 2026-02-15
surface: claude-code
model: claude-opus-4-6
feature: 007-auth-db-monorepo
branch: 007-auth-db-monorepo
user: metachemist
command: /sp.clarify
labels: [spec, clarify, auth, security, cors, rate-limiting, phase-2]
links:
  spec: specs/1-specify/phase-2/feature-03-auth-db-monorepo.md
  ticket: ""
  adr: ""
  pr: ""
files:
  - specs/1-specify/phase-2/feature-03-auth-db-monorepo.md
tests:
  - N/A (specification phase)
---

## Prompt

/sp.clarify Please analyze it for:
1. Ambiguous terms
2. Missing assumptions
3. Incomplete requirements
4. Scope conflicts

What gaps should I address before planning the structure?

## Response snapshot

Second clarification pass focused on the user's four specific areas. Asked 5 questions (max quota), all accepted:

1. **FR-003 "same-origin" vs SEC-008 "cross-origin" contradiction** (Scope Conflict) → Fixed FR-003 to say cross-origin with `credentials: 'include'`. Resolved internal contradiction introduced in v2.
2. **Email case sensitivity** (Missing Assumption) → Case-insensitive. Normalize to lowercase before storage and comparison. Updated FR-012.
3. **access_token in body vs "frontend MUST NOT handle"** (Scope Conflict) → Deliberate dual-auth pattern: cookie for browser, Bearer token for non-browser clients (API testing, future mobile). Updated endpoint contract with explicit notes. Updated task endpoints to mention dual-auth consistent with feature-01 FR-020.
4. **Rate limiting for unauthenticated requests** (Incomplete Requirement) → By IP at 100/hr (stricter than 1000/hr for authenticated). Updated FR-017 and SEC-007.
5. **SEC-003 (403) vs FR-007 (404) ambiguity** (Ambiguous Terms) → Two-layer defense: path check (403) fires first without DB query, task-level check (404) fires second. Updated SEC-003 and SEC-004 with explicit ordering.

## Outcome

- ✅ Impact: 5 gaps resolved across all 4 requested areas (2 scope conflicts, 1 missing assumption, 1 incomplete requirement, 1 ambiguous term)
- 🧪 Tests: N/A (specification phase)
- 📁 Files: 1 file updated (feature-03-auth-db-monorepo.md — FR-003, FR-012, FR-017, SEC-003, SEC-004, SEC-007, Auth Endpoint Contract, Task Endpoints, Clarifications)
- 🔁 Next prompts: /sp.plan
- 🧠 Reflection: The FR-003 "same-origin" issue was introduced in v2 and not caught in the first clarify session — shows that edits can introduce new inconsistencies. Email case sensitivity is a classic miss in auth specs. The dual-auth pattern question revealed that feature-01 FR-020 already supported both Bearer and cookie but feature-03 hadn't acknowledged this.

## Evaluation notes (flywheel)

- Failure modes observed: v2 spec edits introduced a new contradiction (FR-003 same-origin vs SEC-008 cross-origin) that wasn't caught in the first clarify pass. Multiple clarify passes catch issues introduced by previous edits.
- Graders run and results (PASS/FAIL): All 4 user-requested areas addressed. PASS.
- Prompt variant (if applicable): User-directed focus areas (ambiguous terms, missing assumptions, incomplete requirements, scope conflicts) — more productive than open-ended scan.
- Next experiment (smallest change to try): After any spec edit, re-scan for terminology consistency across all sections that reference the changed concept.
