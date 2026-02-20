# Task: T010 — Centralized error mapper with AppException hierarchy and exact catalog messages
# Spec: @specs/1-specify/phase-2/feature-03-auth-db-monorepo.md (Error Message Catalog)
# Plan: @specs/2-plan/phase-2/phase-2-auth-db-monorepo.md (Error Catalog Enforcement Strategy)
from fastapi.responses import JSONResponse


class AppException(Exception):
    """
    Base exception for all application-level errors.
    All subclasses carry a stable error code, the exact catalog message, and HTTP status.
    Route handlers MUST raise these instead of constructing ad-hoc error strings.
    """
    code: str = "INTERNAL_ERROR"
    message: str = "Something went wrong on our end. Please try again later."
    status_code: int = 500

    def __init__(
        self,
        code: str | None = None,
        message: str | None = None,
        status_code: int | None = None,
    ) -> None:
        self.code = code or self.__class__.code
        self.message = message or self.__class__.message
        self.status_code = status_code or self.__class__.status_code
        super().__init__(self.message)


# ---------------------------------------------------------------------------
# 4xx client errors
# ---------------------------------------------------------------------------

class EmailAlreadyExistsError(AppException):
    code = "EMAIL_ALREADY_EXISTS"
    message = "An account with this email already exists. Please log in instead."
    status_code = 409


class InvalidCredentialsError(AppException):
    code = "INVALID_CREDENTIALS"
    message = "Invalid email or password. Please try again."
    status_code = 401


class ValidationError(AppException):
    """
    Raised for invalid email format or weak password.
    The default message covers email format; callers may override with the password message.
    """
    code = "VALIDATION_ERROR"
    message = "Please enter a valid email address."
    status_code = 400


class PasswordValidationError(ValidationError):
    """Raised specifically for weak-password conditions."""
    message = (
        "Password must be at least 8 characters and contain at least one uppercase "
        "letter, one lowercase letter, and one number."
    )


class SessionExpiredError(AppException):
    code = "SESSION_EXPIRED"
    message = "Your session has expired. Please log in again."
    status_code = 401


class InvalidTokenError(AppException):
    code = "INVALID_TOKEN"
    message = "Your session has expired. Please log in again."
    status_code = 401


class UnauthorizedError(AppException):
    code = "UNAUTHORIZED"
    message = "Please log in to continue."
    status_code = 401


class ForbiddenError(AppException):
    code = "FORBIDDEN"
    message = "You do not have permission to perform this action."
    status_code = 403


class TaskNotFoundError(AppException):
    code = "TASK_NOT_FOUND"
    message = "This task could not be found."
    status_code = 404


class RateLimitedError(AppException):
    code = "RATE_LIMITED"
    message = "Too many requests. Please wait a moment and try again."
    status_code = 429


# ---------------------------------------------------------------------------
# 5xx server errors
# ---------------------------------------------------------------------------

class InternalError(AppException):
    code = "INTERNAL_ERROR"
    message = "Something went wrong on our end. Please try again later."
    status_code = 500


class ServiceUnavailableError(AppException):
    code = "SERVICE_UNAVAILABLE"
    message = "Something went wrong on our end. Please try again later."
    status_code = 503


# ---------------------------------------------------------------------------
# Response builder
# ---------------------------------------------------------------------------

def map_exception_to_response(exc: AppException) -> JSONResponse:
    """
    Convert an AppException into the standard error envelope.
    Registered as the global exception handler for AppException in main.py.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "data": None,
            "error": {
                "code": exc.code,
                "message": exc.message,
            },
        },
    )
