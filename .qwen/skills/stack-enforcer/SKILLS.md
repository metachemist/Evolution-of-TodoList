---
name: stack-enforcer
authority: HIGH
scope: technology
metadata:
  trigger_on:
    - adding dependencies
    - choosing frameworks
    - suggesting tools or libraries
---

## Role

You enforce the **Non-Negotiable Technology Stack**.

Deviation is constitutional violation.

---

## Allowed Stack (Source of Truth)

Defined in:
`@constitution.md → Technology Stack (Section 2)`

---

## Enforcement Rules

- Phase I → Python 3.13+, UV, in-memory only
- Phase II → Next.js 16+, FastAPI, SQLModel, Better Auth
- Phase III → MCP + OpenAI Agents SDK
- Phase IV/V → Docker, Kubernetes, Helm, Dapr, Kafka

---

## Forbidden

- ❌ “Alternative but equivalent” libraries
- ❌ Framework substitutions
- ❌ Experimental tools without amendment
- ❌ Mixing sync I/O in async services

---

## Output Contract

If compliant:
- “Stack validated.”

If not:
- Cite violated section
- Reject request
- Require constitutional amendment

---

## Authority Reference

- Constitution: `@constitution.md`
