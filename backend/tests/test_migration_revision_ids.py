# Task: T026 — Migration hardening and sequencing validation
# Spec: @specs/1-specify/phase-2/feature-03-auth-db-monorepo.md (FR-018, FR-019)
from __future__ import annotations

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


def _load_revision(module_path: Path) -> str:
    spec = spec_from_file_location(module_path.stem, module_path)
    assert spec and spec.loader
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    revision = getattr(module, "revision", "")
    assert isinstance(revision, str)
    return revision


def test_all_revision_ids_fit_alembic_version_column_limit() -> None:
    # Alembic default version table uses VARCHAR(32) for version_num.
    versions_dir = Path(__file__).resolve().parents[1] / "alembic" / "versions"
    migration_files = sorted(versions_dir.glob("*.py"))
    for migration_file in migration_files:
        revision = _load_revision(migration_file)
        assert len(revision) <= 32, (
            f"{migration_file.name} revision '{revision}' exceeds 32 chars; "
            "alembic_version.version_num update will fail on PostgreSQL."
        )
