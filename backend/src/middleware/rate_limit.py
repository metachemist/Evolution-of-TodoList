# Task: T029 — RateLimitAdapter Protocol + InMemoryAdapter
# Task: T030 — RedisAdapter
# Task: T031 — RateLimitMiddleware with direct JWT extraction (F02 fix)
# Spec: @specs/1-specify/phase-2/feature-03-auth-db-monorepo.md (FR-017, SEC-007)
# ADR: @history/adr/0012-rate-limiting-and-error-contract-enforcement.md
#
# F02 fix: Middleware runs BEFORE FastAPI Depends(), so current_user is NEVER
# available in request.state at middleware time. The middleware extracts the JWT
# directly from the Authorization header or access_token cookie, then calls
# decode_token() to get the user_id for the rate-limit key. Falls back to IP on
# any decode failure (treats as unauthenticated).
import os
import time
import asyncio
from typing import Protocol, runtime_checkable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from src.utils.token import decode_token
from src.utils.error_mapper import RateLimitedError, ServiceUnavailableError, map_exception_to_response

# ---------------------------------------------------------------------------
# Rate limit policies (ADR-0012)
# ---------------------------------------------------------------------------
_AUTHENTICATED_LIMIT = 1000   # requests per hour per user
_UNAUTHENTICATED_LIMIT = 100  # requests per hour per IP
_WINDOW_SECONDS = 3600        # 1 hour
# Adapter outage policy:
# - true  -> fail-open (preserve availability)
# - false -> fail-closed with envelope 503 (secure alternative for production hardening)
_FAIL_OPEN = os.getenv("RATE_LIMIT_FAIL_OPEN", "true").lower() == "true"

# Public endpoints that are rate-limited by IP (not by user)
_UNAUTHENTICATED_PATHS = {"/api/auth/login", "/api/auth/register"}


# ---------------------------------------------------------------------------
# Adapter Protocol (T029)
# ---------------------------------------------------------------------------

@runtime_checkable
class RateLimitAdapter(Protocol):
    """
    Abstract rate-limit backend.
    Returns True if the request is within the limit; False if the limit is exceeded.
    """
    async def increment(self, key: str, limit: int, window_seconds: int) -> bool:
        ...


# ---------------------------------------------------------------------------
# InMemoryAdapter — single-process dev/test fallback (T029)
# ---------------------------------------------------------------------------

class InMemoryAdapter:
    """
    In-process rate-limit counter. Thread-safe for asyncio single-process use.
    Not suitable for multi-process production deployments — use RedisAdapter there.
    """
    def __init__(self) -> None:
        self._store: dict[str, tuple[int, float]] = {}
        self._lock = asyncio.Lock()

    async def increment(self, key: str, limit: int, window_seconds: int) -> bool:
        now = time.time()
        async with self._lock:
            count, reset_at = self._store.get(key, (0, now + window_seconds))
            if now > reset_at:
                # Window has expired — start fresh
                count = 0
                reset_at = now + window_seconds
            count += 1
            self._store[key] = (count, reset_at)
            return count <= limit


# ---------------------------------------------------------------------------
# RedisAdapter (T030)
# ---------------------------------------------------------------------------

class RedisAdapter:
    """
    Redis-backed rate-limit counter using INCR + EXPIRE.
    Falls back transparently to InMemoryAdapter when redis.asyncio is unavailable.
    """
    def __init__(self, redis_url: str) -> None:
        import redis.asyncio as aioredis
        connect_timeout = float(os.getenv("RATE_LIMIT_REDIS_CONNECT_TIMEOUT_SECONDS", "0.2"))
        socket_timeout = float(os.getenv("RATE_LIMIT_REDIS_SOCKET_TIMEOUT_SECONDS", "0.2"))
        self._client = aioredis.from_url(
            redis_url,
            decode_responses=True,
            socket_connect_timeout=connect_timeout,
            socket_timeout=socket_timeout,
        )

    async def increment(self, key: str, limit: int, window_seconds: int) -> bool:
        try:
            count = await self._client.incr(key)
            if count == 1:
                # First request in this window — set expiry
                await self._client.expire(key, window_seconds)
            return count <= limit
        except Exception:
            # Let middleware policy decide fail-open or fail-closed.
            raise


# ---------------------------------------------------------------------------
# Adapter factory
# ---------------------------------------------------------------------------

def _build_adapter() -> RateLimitAdapter:
    redis_url = os.getenv("REDIS_URL")
    if redis_url:
        try:
            return RedisAdapter(redis_url)
        except Exception:
            pass
    return InMemoryAdapter()


# ---------------------------------------------------------------------------
# RateLimitMiddleware (T031 — F02 fix)
# ---------------------------------------------------------------------------

class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    ASGI middleware for rate limiting.

    Key derivation:
      - Authenticated: extracts JWT from Authorization header or access_token cookie,
        calls decode_token() to get user_id → key = rate:user:{user_id}:{epoch_hour}
      - Unauthenticated (or decode failure): → key = rate:ip:{client_ip}:{epoch_hour}

    F02 fix: FastAPI Depends() runs INSIDE route handlers, AFTER all middleware.
    Therefore current_user is never in request.state at this point. We decode the
    JWT directly here rather than reading from request.state.
    """
    def __init__(self, app, adapter: RateLimitAdapter | None = None) -> None:
        super().__init__(app)
        self._adapter: RateLimitAdapter = adapter or _build_adapter()

    async def dispatch(self, request: Request, call_next) -> Response:
        epoch_hour = int(time.time() // _WINDOW_SECONDS)

        # Determine if this is an authenticated request by decoding the JWT
        user_id: str | None = None
        token: str | None = None

        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header[7:]
        if not token:
            token = request.cookies.get("access_token")

        if token:
            try:
                payload = decode_token(token)
                user_id = payload.get("sub")
            except Exception:
                # Expired or invalid token — treat as unauthenticated for rate limiting
                pass

        # Build the rate-limit key and choose the appropriate limit
        if user_id and request.url.path not in _UNAUTHENTICATED_PATHS:
            key = f"rate:user:{user_id}:{epoch_hour}"
            limit = _AUTHENTICATED_LIMIT
        else:
            client_ip = request.client.host if request.client else "unknown"
            key = f"rate:ip:{client_ip}:{epoch_hour}"
            limit = _UNAUTHENTICATED_LIMIT

        try:
            allowed = await self._adapter.increment(key, limit, _WINDOW_SECONDS)
        except Exception:
            if _FAIL_OPEN:
                # Availability-first mode: allow traffic when limiter backend is degraded.
                allowed = True
            else:
                # Security-first mode: deny traffic if limiter health is unknown.
                return map_exception_to_response(ServiceUnavailableError())

        if not allowed:
            return map_exception_to_response(RateLimitedError())

        return await call_next(request)
