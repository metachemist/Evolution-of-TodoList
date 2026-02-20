# Auth Migration Plan

**Feature**: 007-auth-db-monorepo
**Created**: 2026-02-15
**Task**: T028
**ADR**: @history/adr/0014-schema-first-migration-with-orphan-cleanup.md

---

## Migration Sequence

| ID | File | Description | Reversible |
|----|------|-------------|-----------|
| 001 | `001_initial_models.py` | Create `user` and `task` tables with `owner_id` FK | YES |
| 002 | `002_add_performance_indexes.py` | Add named indexes for email, owner_id, created_at, is_completed | YES |
| 003 | `003_delete_orphan_tasks.py` | Delete tasks with NULL owner_id (pre-auth orphans) | **NO** |
| 004 | `004_enforce_tasks_owner_id_not_null.py` | Enforce owner_id NOT NULL constraint | YES (schema only) |

---

## Reversibility

- **001 downgrade**: Drops `task` then `user` tables (data lost)
- **002 downgrade**: Drops named indexes (re-creatable)
- **003 downgrade**: **NOT SUPPORTED** — orphaned task deletion is intentionally irreversible per ADR-0014. `downgrade()` raises `NotImplementedError`.
- **004 downgrade**: Makes `owner_id` nullable again; data deleted in 003 is NOT restored

---

## Rollback Playbook

### Rolling back migration 004 (owner_id NOT NULL)

```bash
docker compose run backend alembic downgrade -1
```

This makes `owner_id` nullable again. No data is restored.

### Rolling back migration 002 (indexes)

```bash
docker compose run backend alembic downgrade -1
```

Drops the named performance indexes. Application continues to work without them.

### Rolling back migration 001 (full schema)

```bash
docker compose run backend alembic downgrade base
```

**WARNING**: Drops all tables. All user and task data is permanently lost.

### Migration 003 CANNOT be rolled back

Orphaned task deletion is intentional and irreversible. If this is an error, restore from a database backup taken before the migration.

---

## Run Instructions

### Fresh database (new environment)

```bash
docker compose run backend alembic upgrade head
```

Creates all tables and applies all migrations from scratch. Safe and idempotent.

### Already-at-head database

```bash
docker compose run backend alembic upgrade head
```

No-op — detects that all migrations are applied and exits cleanly.

### Check current state

```bash
docker compose run backend alembic current
```

### Check pending migrations

```bash
docker compose run backend alembic history --verbose
```

---

## Deployment

The backend Dockerfile runs `alembic upgrade head` automatically before starting uvicorn:

```dockerfile
CMD ["sh", "-c", "poetry run alembic upgrade head && poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000"]
```

This satisfies FR-018 (schema migrations run on deployment).

---

## Notes

- In this codebase, `owner_id` has been NOT NULL since migration 001, so migration 003 is a safe no-op (no orphaned tasks exist). The migration is included for spec compliance and as a safety net for environments transitioning from a truly unauthenticated schema.
- Migration 004 (`op.alter_column("task", "owner_id", nullable=False)`) is also idempotent — the column is already NOT NULL.
