"""FastAPI application assembly + the thin gateway concerns (Bible §2.9, §7).

The gateway does no business logic: correlation IDs, the uniform error model (§7.5), CORS, and
router mounting only. Business logic and fine-grained ABAC live in the services.
"""
from __future__ import annotations

import uuid

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .api import (
    actions,
    auth_shell,
    compliance,
    corrections,
    documents,
    investigations,
    misc,
    resolution,
)
from .config import get_settings
from .domain.errors import SentinelError

app = FastAPI(
    title="Prahari — Industrial Decision Intelligence Operating System",
    version="1.0.0",
    description="Contract-first API (Bible §7). Every answer carries citations (CP-2); every "
    "write is gated (CP-3); abstention is a first-class state (CP-4); the degradation ladder is "
    "surfaced, never swallowed (CP-9).",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # dev; production pins the console origin at the gateway
    allow_methods=["*"],
    allow_headers=["*"],
)


_RL_EXEMPT = {"/", "/v1/health", "/docs", "/openapi.json", "/v1/openapi.json", "/redoc"}


def _rl_key(request: Request) -> str:
    """Key the bucket by token subject (per-user), falling back to client host."""
    auth = request.headers.get("authorization", "")
    if auth.lower().startswith("bearer "):
        try:
            import jwt

            claims = jwt.decode(auth.split(" ", 1)[1], options={"verify_signature": False})
            return f"{claims.get('tenant', '?')}:{claims.get('sub', '?')}"
        except Exception:
            pass
    return f"ip:{request.client.host if request.client else 'unknown'}"


@app.middleware("http")
async def correlation_id(request: Request, call_next):  # type: ignore[no-untyped-def]
    rid = request.headers.get("X-Request-Id", f"req-{uuid.uuid4().hex[:12]}")

    # Token-bucket rate limiting at the edge (Bible §7.7); ingestion has its own tighter bucket.
    if request.url.path not in _RL_EXEMPT and not request.url.path.startswith("/docs"):
        from .resilience.rate_limit import get_limiter, now_monotonic

        is_ingest = request.url.path == "/v1/documents" and request.method == "POST"
        allowed, remaining, retry = get_limiter().check(
            _rl_key(request), ingestion=is_ingest, monotonic=now_monotonic()
        )
        if not allowed:
            return JSONResponse(
                status_code=429,
                content={"error": {"code": "rate_limited", "message": "Rate limit exceeded.",
                                   "request_id": rid, "details": {}}},
                headers={"Retry-After": str(retry), "X-RateLimit-Remaining": "0",
                         "X-Request-Id": rid},
            )
        response = await call_next(request)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-Request-Id"] = rid
        return response

    response = await call_next(request)
    response.headers["X-Request-Id"] = rid
    return response


@app.exception_handler(SentinelError)
async def prahari_error_handler(request: Request, exc: SentinelError) -> JSONResponse:
    rid = request.headers.get("X-Request-Id", "")
    return JSONResponse(
        status_code=exc.http_status,
        content={"error": {"code": exc.code, "message": exc.message, "request_id": rid,
                           "details": exc.details}},
    )


for r in (auth_shell, investigations, documents, resolution, compliance, actions, corrections, misc):
    app.include_router(r.router)


@app.get("/", tags=["health"])
async def root() -> dict:
    s = get_settings()
    return {
        "product": "Prahari — Industrial Decision Intelligence Operating System",
        "profile": s.profile,
        "docs": "/docs",
        "note": "Ask an investigation, watch the traversal, then disable the graph and watch it "
        "refuse honestly. That refusal is the point.",
    }
