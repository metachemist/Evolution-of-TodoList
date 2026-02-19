# Task: T035 — AuthService unit tests
# Spec: @specs/1-specify/phase-2/feature-03-auth-db-monorepo.md (FR-012, FR-013)
import pytest

from src.services.auth_service import (
    normalize_email,
    validate_email_format,
    validate_password,
    hash_password,
    verify_password,
)
from src.utils.error_mapper import ValidationError, PasswordValidationError


# ── normalize_email ───────────────────────────────────────────────────────────

def test_normalize_email_lowercases():
    assert normalize_email("User@Example.COM") == "user@example.com"


def test_normalize_email_strips_whitespace():
    assert normalize_email("  user@example.com  ") == "user@example.com"


def test_normalize_email_both():
    assert normalize_email("  UPPER@DOMAIN.IO  ") == "upper@domain.io"


# ── validate_email_format ─────────────────────────────────────────────────────

def test_valid_email_passes():
    validate_email_format("user@example.com")  # should not raise


def test_email_without_at_raises():
    with pytest.raises(ValidationError):
        validate_email_format("notanemail")


def test_email_without_domain_raises():
    with pytest.raises(ValidationError):
        validate_email_format("user@")


def test_email_without_tld_raises():
    with pytest.raises(ValidationError):
        validate_email_format("user@example")


# ── validate_password ─────────────────────────────────────────────────────────

def test_valid_password_passes():
    validate_password("SecurePass1")  # should not raise


def test_password_too_short_raises():
    with pytest.raises(PasswordValidationError):
        validate_password("Ab1")


def test_password_no_uppercase_raises():
    with pytest.raises(PasswordValidationError):
        validate_password("alllower1")


def test_password_no_lowercase_raises():
    with pytest.raises(PasswordValidationError):
        validate_password("ALLUPPER1")


def test_password_no_digit_raises():
    with pytest.raises(PasswordValidationError):
        validate_password("NoDigitsHere")


def test_password_validation_error_message():
    """The exact catalog message must be present in PasswordValidationError."""
    err = PasswordValidationError()
    assert "uppercase" in err.message
    assert "lowercase" in err.message
    assert "number" in err.message


# ── hash_password + verify_password ──────────────────────────────────────────

def test_hash_password_is_not_plaintext():
    hashed = hash_password("SecurePass1")
    assert hashed != "SecurePass1"
    assert hashed.startswith("$argon2")  # Argon2 hash prefix


def test_verify_password_correct():
    hashed = hash_password("SecurePass1")
    assert verify_password(hashed, "SecurePass1") is True


def test_verify_password_wrong():
    hashed = hash_password("SecurePass1")
    assert verify_password(hashed, "WrongPass1") is False


def test_verify_password_never_raises():
    """verify_password must return False (not raise) for invalid hash strings."""
    result = verify_password("not-a-valid-hash", "password")
    assert result is False
