# Task: T036 — Locust load test for auth endpoints
# Spec: @specs/1-specify/phase-2/feature-03-auth-db-monorepo.md (SC-008, PERF-001, PERF-003)
# Plan: @specs/2-plan/phase-2/phase-2-auth-db-monorepo.md (Phase E)
#
# Run command (against docker-compose stack):
#   locust -f tests/load/locustfile.py \
#          --users 100 --spawn-rate 10 --run-time 60s \
#          --host http://localhost:8000
#
# Acceptance criterion: p95 response time ≤ 300ms for register, login, and /me
# Target environment: docker compose up (backend + postgres)
# WARNING: Never run this against production.
import json
import uuid

from locust import HttpUser, between, task


class AuthUser(HttpUser):
    """
    Simulates a user performing registration, login, and session checks.
    Each virtual user gets a unique email to avoid EMAIL_ALREADY_EXISTS conflicts.
    """
    # Think time between tasks: 1–3 seconds (realistic user pacing)
    wait_time = between(1, 3)

    def on_start(self) -> None:
        """Called once per virtual user before the task loop begins."""
        # Unique email per user instance to avoid collision across concurrent users
        self.user_email = f"loadtest_{uuid.uuid4().hex[:12]}@example.com"
        self.user_password = "LoadTest1"
        self.access_token: str | None = None
        self._register()

    def _register(self) -> None:
        """Register the virtual user and capture the access token."""
        with self.client.post(
            "/api/auth/register",
            json={"email": self.user_email, "password": self.user_password},
            name="/api/auth/register",
            catch_response=True,
        ) as resp:
            if resp.status_code == 201:
                data = resp.json().get("data", {})
                self.access_token = data.get("access_token")
            else:
                resp.failure(f"Register failed: {resp.status_code} {resp.text[:200]}")

    @task(2)
    def task_login(self) -> None:
        """POST /api/auth/login — weighted 2x (most common auth op)."""
        with self.client.post(
            "/api/auth/login",
            json={"email": self.user_email, "password": self.user_password},
            name="/api/auth/login",
            catch_response=True,
        ) as resp:
            if resp.status_code == 200:
                data = resp.json().get("data", {})
                self.access_token = data.get("access_token")
            else:
                resp.failure(f"Login failed: {resp.status_code}")

    @task(3)
    def task_me(self) -> None:
        """GET /api/auth/me — weighted 3x (most frequent: every dashboard load)."""
        if not self.access_token:
            return
        with self.client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {self.access_token}"},
            name="/api/auth/me",
            catch_response=True,
        ) as resp:
            if resp.status_code != 200:
                resp.failure(f"/me failed: {resp.status_code}")
