"""Token-bucket rate limiting per (tenant, user) at the gateway (Bible §2.7, §7.7).

Separate buckets for the read path vs the ingestion path (bulkhead). In-memory for the
single-process hackathon box; a Redis-backed bucket is the production swap (same interface).
Limits are deliberately generous so scripted demos never trip them accidentally.
"""
from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field

_LOCK = threading.Lock()


@dataclass
class _Bucket:
    capacity: float
    refill_per_sec: float
    tokens: float = field(default=0.0)
    last: float = field(default=0.0)

    def allow(self, now: float) -> tuple[bool, float]:
        if self.last == 0.0:
            self.tokens = self.capacity
            self.last = now
        # refill
        self.tokens = min(self.capacity, self.tokens + (now - self.last) * self.refill_per_sec)
        self.last = now
        if self.tokens >= 1.0:
            self.tokens -= 1.0
            return True, self.tokens
        return False, self.tokens


class RateLimiter:
    """One limiter instance holds the read and ingestion bucket families."""

    def __init__(self, read=(240.0, 8.0), ingest=(30.0, 1.0)) -> None:
        self._read_cfg = read
        self._ingest_cfg = ingest
        self._read: dict[str, _Bucket] = {}
        self._ingest: dict[str, _Bucket] = {}

    def check(self, key: str, *, ingestion: bool, monotonic: float) -> tuple[bool, int, int]:
        """Return (allowed, remaining, retry_after_seconds)."""
        with _LOCK:
            table = self._ingest if ingestion else self._read
            cap, rate = self._ingest_cfg if ingestion else self._read_cfg
            bucket = table.get(key)
            if bucket is None:
                bucket = _Bucket(capacity=cap, refill_per_sec=rate)
                table[key] = bucket
            allowed, remaining = bucket.allow(monotonic)
            retry_after = 0 if allowed else max(1, int(1.0 / rate))
            return allowed, int(remaining), retry_after


_limiter = RateLimiter()


def get_limiter() -> RateLimiter:
    return _limiter


def now_monotonic() -> float:
    return time.monotonic()
