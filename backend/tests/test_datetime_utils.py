# Task: T006 — Timestamp utility normalization for DB writes
# Spec: @specs/1-specify/phase-2/feature-03-auth-db-monorepo.md (FR-018)
from datetime import datetime, timezone, timedelta

from src.utils.datetime_utils import to_naive_utc, utcnow_naive


def test_utcnow_naive_returns_naive_datetime() -> None:
    value = utcnow_naive()
    assert value.tzinfo is None


def test_to_naive_utc_keeps_naive_input() -> None:
    value = datetime(2026, 2, 19, 12, 0, 0)
    normalized = to_naive_utc(value)
    assert normalized == value
    assert normalized.tzinfo is None


def test_to_naive_utc_converts_aware_input_to_utc_naive() -> None:
    value = datetime(2026, 2, 19, 12, 0, 0, tzinfo=timezone(timedelta(hours=5, minutes=30)))
    normalized = to_naive_utc(value)

    # 12:00 at UTC+05:30 -> 06:30 UTC, then tzinfo removed.
    assert normalized == datetime(2026, 2, 19, 6, 30, 0)
    assert normalized.tzinfo is None
