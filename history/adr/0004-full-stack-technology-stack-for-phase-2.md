# ADR-0004: Full-Stack Technology Stack for Phase 2 Todo Application

## Status
Proposed

## Date
2026-02-07

## Context
For Phase 2 of the Todo Evolution project, we need to select a technology stack that supports rapid development of a full-stack web application with authentication, task management, and future AI integration. The stack must align with constitutional requirements and support the progressive evolution approach.

## Decision
- Frontend: Next.js 16+ with App Router, TypeScript, Tailwind CSS
- Backend: FastAPI with Python 3.11+
- ORM: SQLModel for unified data modeling
- Database: PostgreSQL with Neon Serverless
- Package Managers: npm/yarn for frontend, uv/pip for backend

## Alternatives
- Alternative 1: React + Vite + Express + Sequelize + MySQL
- Alternative 2: Vue.js + Pinia + NestJS + TypeORM + MongoDB
- Alternative 3: SvelteKit + Supabase + Prisma + PostgreSQL

## Consequences
- Positive: Excellent developer experience, strong ecosystem, good performance, TypeScript support
- Negative: Learning curve for team unfamiliar with Next.js/FastAPI, vendor lock-in with specific hosting platforms
- Risk: Dependency on specific framework versions and potential breaking changes

## References
- @specs/2-plan/phase-2-fullstack.md
- @constitution.md (technology stack requirements)