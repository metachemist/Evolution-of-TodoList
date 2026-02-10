---
id: 0001
title: Correct-Phase-3-Specs
stage: spec
date: 2026-02-09
surface: CLI
model: Qwen
feature: 1-specify
branch: main
user: metachemist
command: manual-correction
labels: [correction, specification, ai, chatbot, monorepo]
links:
  spec: specs/1-specify/features/feature-03-chatbot.md
  ticket: 
  adr: 
  pr: 
files:
  - path: specs/1-specify/features/feature-03-chatbot.md
    action: created
    summary: Phase 3 AI Chatbot feature specification in correct location
  - path: specs/2-plan/phase-3-ai-chatbot.md
    action: created
    summary: Phase 3 AI Chatbot implementation plan
  - path: specs/3-tasks/phase-3/T-201-mcp-server.md
    action: created
    summary: Task specification for MCP server setup
  - path: specs/3-tasks/phase-3/T-202-agents-sdk.md
    action: created
    summary: Task specification for OpenAI Agents SDK integration
  - path: specs/3-tasks/phase-3/T-203-chatkit-ui.md
    action: created
    summary: Task specification for ChatKit UI integration
tests:
  - path: specs/1-specify/features/feature-03-chatbot.md
    action: verify
    summary: Verify spec follows constitutional requirements
---

## Prompt

Correct the Phase 3 AI Chatbot specification to follow the mandatory monorepo structure as defined in the constitution.

## Response snapshot

Corrected the Phase 3 AI Chatbot specification by placing it in the proper location according to the constitution: specs/1-specify/features/feature-03-chatbot.md. Also created the corresponding plan file at specs/2-plan/phase-3-ai-chatbot.md and task files at specs/3-tasks/phase-3/. Removed incorrectly created feature directory and branch that didn't follow the constitutional monorepo structure.

## Outcome

- ✅ Impact: Fixed specification location to comply with constitutional requirements
- 🧪 Tests: Verification needed to ensure all specs follow constitutional structure
- 📁 Files: Moved spec to correct location per constitution
- 🔁 Next prompts: Ready to continue with Phase 3 implementation
- 🧠 Reflection: Critical to always follow constitutional requirements for monorepo structure

## Evaluation notes (flywheel)

- Failure modes observed: Initially created specs in wrong location violating constitutional requirements
- Graders run and results (PASS/FAIL): Need to verify all specs follow constitutional structure
- Prompt variant (if applicable): Correction workflow for constitutional violations
- Next experiment (smallest change to try): Verify all existing specs follow constitutional structure
