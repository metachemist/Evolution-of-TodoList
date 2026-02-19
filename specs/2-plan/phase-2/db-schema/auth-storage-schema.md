# Auth Storage Schema

**Feature**: 007-auth-db-monorepo
**Created**: 2026-02-15
**Task**: T028
**Status**: Final (matches migration 004 head state)

---

## `user` Table

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| `id` | UUID | PRIMARY KEY, NOT NULL | Generated via `uuid4()` |
| `email` | VARCHAR(255) | NOT NULL, UNIQUE | Stored normalized (lowercase, stripped) |
| `hashed_password` | TEXT | NOT NULL | Argon2id encoded hash (never plain text) |
| `created_at` | DATETIME | NOT NULL | UTC, set at insert via `datetime.utcnow()` |
| `updated_at` | DATETIME | NOT NULL | UTC, updated by application on each write |

### Indexes on `user`

| Index Name | Columns | Unique | Purpose |
|------------|---------|--------|---------|
| `ix_user_email` | `email` | YES | Fast lookup by email on login/register |
| `idx_user_email` | `email` | YES | SQLModel __table_args__ alias |
| `idx_user_created_at` | `created_at` | NO | Admin/ordering queries |

---

## `task` Table

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| `id` | UUID | PRIMARY KEY, NOT NULL | Generated via `uuid4()` |
| `title` | VARCHAR(255) | NOT NULL | Max 255 chars |
| `description` | VARCHAR(5000) | NULL | Optional, max 5000 chars |
| `is_completed` | BOOLEAN | NOT NULL, DEFAULT false | Completion toggle |
| `created_at` | DATETIME | NOT NULL | UTC |
| `updated_at` | DATETIME | NOT NULL | UTC |
| `owner_id` | UUID | NOT NULL, FK → `user.id` CASCADE | User ownership (FR-005, FR-014) |

### Indexes on `task`

| Index Name | Columns | Unique | Purpose |
|------------|---------|--------|---------|
| `ix_task_owner_id` | `owner_id` | NO | Per-user task list queries (PERF-004) |
| `ix_task_is_completed` | `is_completed` | NO | Filtered list queries |
| `ix_task_created_at` | `created_at` | NO | Newest-first ordering |
| `idx_task_owner_id` | `owner_id` | NO | SQLModel __table_args__ alias |
| `idx_task_created_at` | `created_at` | NO | SQLModel __table_args__ alias |
| `idx_task_is_completed` | `is_completed` | NO | SQLModel __table_args__ alias |

### Foreign Key Behavior

- `task.owner_id → user.id` with `ON DELETE CASCADE`
- Deleting a user removes all their tasks automatically (FR-014)
- No orphaned tasks are possible once migration 004 is applied

---

## Table Relationship

```
user (1) ──< task (many)
       └── owner_id FK
```

---

## Notes

- Table names are singular (`user`, `task`) — SQLModel default
- All timestamps are stored as UTC without timezone; application is responsible for timezone handling
- Argon2id hash strings are stored in the `hashed_password` column; format: `$argon2id$v=19$m=65536,t=3,p=2$<salt>$<hash>`
