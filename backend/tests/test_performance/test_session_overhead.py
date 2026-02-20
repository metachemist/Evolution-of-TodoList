# Task: T040 — Session validation overhead benchmark (PERF-002)
# Spec: @specs/1-specify/phase-2/feature-03-auth-db-monorepo.md (PERF-002)
# Requirement: Session validation MUST add no more than 50ms overhead per request.
#
# This test measures the combined cost of decode_token() + get_user_by_email()
# which represents the overhead added by require_authenticated_user on every
# protected request.
import time
import statistics
from uuid import uuid4

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from src.utils.token import create_token, decode_token
from src.services.auth_service import get_user_by_email, create_user, hash_password

_ITERATIONS = 100
_MAX_MEAN_MS = 50.0  # PERF-002: ≤ 50ms mean overhead


@pytest.mark.asyncio
async def test_session_validation_overhead(db_session: AsyncSession):
    """
    PERF-002: Session validation overhead ≤ 50ms mean over 100 iterations.

    Measures: decode_token() + get_user_by_email() — the two operations
    performed by require_authenticated_user on every protected request.
    """
    # Set up a real user and token
    user_email = f"perf_{uuid4().hex[:8]}@example.com"
    hashed = hash_password("PerfTest1")
    user = await create_user(db_session, user_email, hashed)
    token = create_token(user.id, user.email)

    durations_ms: list[float] = []

    for _ in range(_ITERATIONS):
        t0 = time.perf_counter()

        # Simulate what require_authenticated_user does on each request
        payload = decode_token(token)
        email = payload.get("email", "")
        await get_user_by_email(db_session, email)

        t1 = time.perf_counter()
        durations_ms.append((t1 - t0) * 1000)

    mean_ms = statistics.mean(durations_ms)
    p95_ms = sorted(durations_ms)[int(_ITERATIONS * 0.95)]

    print(f"\nSession validation overhead (n={_ITERATIONS}):")
    print(f"  Mean:  {mean_ms:.2f}ms")
    print(f"  P95:   {p95_ms:.2f}ms")
    print(f"  Min:   {min(durations_ms):.2f}ms")
    print(f"  Max:   {max(durations_ms):.2f}ms")

    assert mean_ms <= _MAX_MEAN_MS, (
        f"PERF-002 VIOLATION: Session validation mean={mean_ms:.2f}ms exceeds {_MAX_MEAN_MS}ms limit"
    )
