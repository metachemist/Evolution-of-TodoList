# Task: T041 — Data volume integration test (PERF-005)
# Spec: @specs/1-specify/phase-2/feature-03-auth-db-monorepo.md (PERF-005)
# Requirement: Persistent storage MUST support at least 10,000 tasks per user
#              without performance degradation (list, get first, get last ≤ 300ms each).
import time
import uuid
from datetime import datetime, timezone

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import text

from src.models.task import Task
from src.services.auth_service import create_user, hash_password
from src.utils.token import create_token

_TASK_COUNT = 10_000
_MAX_RESPONSE_MS = 300.0  # PERF-005: ≤ 300ms per list/get operation


@pytest.mark.asyncio
async def test_task_volume_performance(client, db_session: AsyncSession):
    """
    PERF-005: List and individual task lookups complete within 300ms for a user with
    10,000 tasks.

    Seeds tasks via direct bulk insert (not through the API) to keep the test fast.
    """
    # Create a user and get their auth token
    email = f"vol_{uuid.uuid4().hex[:8]}@example.com"
    hashed = hash_password("VolumeTest1")
    user = await create_user(db_session, email, hashed)
    token = create_token(user.id, user.email)
    user_id = str(user.id)

    # Bulk insert 10,000 tasks directly via ORM
    print(f"\nInserting {_TASK_COUNT} tasks for user {user_id}...")
    t_insert_start = time.perf_counter()

    batch_size = 500
    all_task_ids: list[str] = []

    for batch_start in range(0, _TASK_COUNT, batch_size):
        tasks = []
        for i in range(batch_start, min(batch_start + batch_size, _TASK_COUNT)):
            task_id = uuid.uuid4()
            all_task_ids.append(str(task_id))
            tasks.append(
                Task(
                    id=task_id,
                    title=f"Volume task {i}",
                    description=f"Description for task {i}",
                    is_completed=(i % 2 == 0),
                    created_at=datetime.now(timezone.utc),
                    updated_at=datetime.now(timezone.utc),
                    owner_id=user.id,
                )
            )
        db_session.add_all(tasks)
        await db_session.commit()

    t_insert_end = time.perf_counter()
    print(f"  Insert time: {(t_insert_end - t_insert_start):.2f}s")

    auth_headers = {"Authorization": f"Bearer {token}"}

    # ── Test 1: List all tasks (paginated, first page) ─────────────────────
    t0 = time.perf_counter()
    resp = await client.get(f"/api/{user_id}/tasks?skip=0&limit=20", headers=auth_headers)
    list_ms = (time.perf_counter() - t0) * 1000

    assert resp.status_code == 200, f"List tasks failed: {resp.status_code}"
    body = resp.json()
    assert body["success"] is True
    assert body["error"] is None
    assert len(body["data"]) == 20  # Full page returned

    print(f"  GET /tasks (first page):  {list_ms:.1f}ms")
    assert list_ms <= _MAX_RESPONSE_MS, (
        f"PERF-005 VIOLATION: List tasks = {list_ms:.1f}ms > {_MAX_RESPONSE_MS}ms"
    )

    # ── Test 2: Get first task ──────────────────────────────────────────────
    first_id = all_task_ids[0]
    t0 = time.perf_counter()
    resp = await client.get(f"/api/{user_id}/tasks/{first_id}", headers=auth_headers)
    first_ms = (time.perf_counter() - t0) * 1000

    assert resp.status_code == 200, f"Get first task failed: {resp.status_code}"
    assert resp.json()["success"] is True
    print(f"  GET /tasks/{first_id[:8]}... (first): {first_ms:.1f}ms")
    assert first_ms <= _MAX_RESPONSE_MS, (
        f"PERF-005 VIOLATION: Get first task = {first_ms:.1f}ms > {_MAX_RESPONSE_MS}ms"
    )

    # ── Test 3: Get last task (worst case for sequential scan) ──────────────
    last_id = all_task_ids[-1]
    t0 = time.perf_counter()
    resp = await client.get(f"/api/{user_id}/tasks/{last_id}", headers=auth_headers)
    last_ms = (time.perf_counter() - t0) * 1000

    assert resp.status_code == 200, f"Get last task failed: {resp.status_code}"
    assert resp.json()["success"] is True
    print(f"  GET /tasks/{last_id[:8]}... (last):  {last_ms:.1f}ms")
    assert last_ms <= _MAX_RESPONSE_MS, (
        f"PERF-005 VIOLATION: Get last task = {last_ms:.1f}ms > {_MAX_RESPONSE_MS}ms"
    )
