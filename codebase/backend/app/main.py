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


@app.middleware("http")
async def correlation_id(request: Request, call_next):  # type: ignore[no-untyped-def]
    rid = request.headers.get("X-Request-Id", f"req-{uuid.uuid4().hex[:12]}")
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
