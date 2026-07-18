"""Error taxonomy (Bible §3.8) and API error codes (Bible §7.5)."""
from __future__ import annotations


class SentinelError(Exception):
    code: str = "internal_error"
    http_status: int = 500

    def __init__(self, message: str, details: dict | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details or {}


class InvalidRequest(SentinelError):
    code = "invalid_request"
    http_status = 400


class Unauthenticated(SentinelError):
    code = "unauthenticated"
    http_status = 401


class Forbidden(SentinelError):
    code = "forbidden"
    http_status = 403


class Conflict(SentinelError):
    code = "conflict"
    http_status = 409


class Ungrounded(SentinelError):
    """Answer stripped to abstain — signalled, not an error to the user (Bible §7.5)."""

    code = "ungrounded"
    http_status = 422


class RateLimited(SentinelError):
    code = "rate_limited"
    http_status = 429


class Degraded(SentinelError):
    """Operating on a lower rung of the CP-9 ladder — response still useful (Bible §7.5)."""

    code = "degraded"
    http_status = 503


class ProvenanceViolation(SentinelError):
    """A fact-bearing write lacked provenance (CP-1 / BR-1)."""

    code = "provenance_violation"
    http_status = 422


class ApprovalRequired(SentinelError):
    """A system-of-record write was attempted without a distinct approver (CP-3)."""

    code = "approval_required"
    http_status = 403
