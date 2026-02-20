# Load Test: Auth Endpoints

**Task**: T036
**Spec**: PERF-001, PERF-003, SC-008

## Acceptance Criterion

p95 response time ≤ 300ms for all auth endpoints under 100 concurrent users.

## Target Environment

`docker compose up` stack (backend + PostgreSQL + Redis).
**Never run against production.**

## Run Command

```bash
locust -f tests/load/locustfile.py \
       --users 100 \
       --spawn-rate 10 \
       --run-time 60s \
       --host http://localhost:8000
```

## Start the Stack First

```bash
cd backend/docker
docker compose up -d
# Wait for health checks to pass
docker compose ps
```

## Interpreting Results

- Open the Locust web UI at http://localhost:8089 during the test
- Accept the run if p95 ≤ 300ms for `/api/auth/register`, `/api/auth/login`, and `/api/auth/me`
- Failure rates > 1% indicate a backend problem, not a load issue

## What the Test Does

Each virtual user:
1. Registers with a unique email on startup
2. Loops: login (2× weight) and `/me` check (3× weight) with 1–3s think time
