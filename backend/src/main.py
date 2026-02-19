# Task: T011 — CORS fix (no wildcard) and AppException global handler
# Task: T010 — Imports AppException from error_mapper
# Spec: @specs/1-specify/phase-2/feature-03-auth-db-monorepo.md (SEC-008, FR-015)
import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import DataError, IntegrityError
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.utils.error_mapper import AppException, InternalError, map_exception_to_response
from src.middleware.rate_limit import RateLimitMiddleware
from src.database import async_engine


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Lifespan context manager for startup and shutdown events."""
    print("Starting up the application...")
    yield
    await async_engine.dispose()
    print("Shutting down the application...")


# Create FastAPI app
app = FastAPI(
    title="Focentra API",
    description="Focentra API for task management focused on deep work.",
    version="0.2.0",
    lifespan=lifespan,
)

# ---------------------------------------------------------------------------
# Middleware registration — Starlette uses LIFO ordering: last added = outermost.
# CORSMiddleware MUST be outermost so CORS headers appear on ALL responses
# (including rate-limit 429s and error responses from inner middleware).
# ---------------------------------------------------------------------------
_cors_origin = os.getenv("CORS_ORIGIN", os.getenv("ALLOWED_ORIGINS", "http://localhost:3000"))

# Rate limiting — added FIRST so it is INNER (SEC-008, T031)
app.add_middleware(RateLimitMiddleware)

# CORS — added LAST so it is OUTERMOST; handles preflight OPTIONS before anything else
app.add_middleware(
    CORSMiddleware,
    allow_origins=[_cors_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Exception handlers
# ---------------------------------------------------------------------------

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """
    Handle all AppException subclasses using the centralized error mapper.
    No route handler may construct its own error strings — all errors flow here.
    """
    return map_exception_to_response(exc)


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    """
    Ensure FastAPI validation errors also follow the unified response envelope.
    Status code remains 422 to preserve existing behavior.
    """
    first_error = exc.errors()[0]["msg"] if exc.errors() else "Validation failed."
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "data": None,
            "error": {"code": "VALIDATION_ERROR", "message": first_error},
        },
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    """
    Normalize HTTPException responses into the same envelope contract.
    """
    if isinstance(exc.detail, dict) and {"success", "data", "error"}.issubset(exc.detail.keys()):
        return JSONResponse(status_code=exc.status_code, content=exc.detail, headers=exc.headers)

    code_map = {
        400: "VALIDATION_ERROR",
        401: "UNAUTHORIZED",
        403: "FORBIDDEN",
        404: "NOT_FOUND",
    }
    message_map = {
        400: "Validation failed.",
        401: "Please log in to continue.",
        403: "You do not have permission to perform this action.",
        404: "This resource could not be found.",
    }
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "data": None,
            "error": {
                "code": code_map.get(exc.status_code, "HTTP_ERROR"),
                "message": (
                    str(exc.detail)
                    if isinstance(exc.detail, str)
                    else message_map.get(exc.status_code, "Request failed.")
                ),
            },
        },
        headers=exc.headers,
    )


@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError) -> JSONResponse:
    """
    Normalize SQL integrity violations (constraint failures) into 422 envelope responses.
    """
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "data": None,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Validation failed.",
            },
        },
    )


@app.exception_handler(DataError)
async def data_error_handler(request: Request, exc: DataError) -> JSONResponse:
    """
    Normalize SQL data-format errors into 422 envelope responses.
    """
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "data": None,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Validation failed.",
            },
        },
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Catch-all for unexpected exceptions; never expose internal details.

    This handler is dispatched by Starlette's ServerErrorMiddleware, which sits
    OUTSIDE CORSMiddleware in the middleware stack.  That means the response it
    returns never passes through CORSMiddleware, so we must attach CORS headers
    ourselves — otherwise the browser blocks the 500 body and shows a misleading
    "CORS policy" error instead of the real failure.
    """
    response = map_exception_to_response(InternalError())
    origin = request.headers.get("origin")
    if origin and origin in [_cors_origin]:
        response.headers["access-control-allow-origin"] = origin
        response.headers["access-control-allow-credentials"] = "true"
    return response


# ---------------------------------------------------------------------------
# Health endpoints
# ---------------------------------------------------------------------------

@app.get("/")
async def root() -> dict:
    return {
        "success": True,
        "data": {"message": "Welcome to the Focentra API"},
        "error": None,
    }


@app.get("/health")
async def health_check() -> dict:
    return {
        "success": True,
        "data": {"status": "healthy", "message": "API is running"},
        "error": None,
    }


# ---------------------------------------------------------------------------
# Routers (deferred import to avoid circular imports)
# ---------------------------------------------------------------------------

def _include_routers() -> None:
    from src.routes.tasks import router as tasks_router
    from src.routes.tasks import task_tools_router
    from src.routes.auth import router as auth_router

    app.include_router(task_tools_router, prefix="/api/tasks", tags=["tasks"])
    app.include_router(tasks_router, prefix="/api/{user_id}", tags=["tasks"])
    app.include_router(auth_router, prefix="/api/auth", tags=["auth"])


_include_routers()
