"""Circuit breaker for model/provider calls (Bible §2.7). Open circuit → local fallback (CP-9)."""
from __future__ import annotations

import time
from typing import Callable, TypeVar

T = TypeVar("T")


class CircuitBreaker:
    def __init__(self, failure_threshold: int = 3, reset_after_s: float = 30.0) -> None:
        self._failures = 0
        self._threshold = failure_threshold
        self._reset_after = reset_after_s
        self._opened_at: float | None = None

    @property
    def is_open(self) -> bool:
        if self._opened_at is None:
            return False
        if time.monotonic() - self._opened_at > self._reset_after:
            # half-open: allow a trial
            self._opened_at = None
            self._failures = 0
            return False
        return True

    def record_success(self) -> None:
        self._failures = 0
        self._opened_at = None

    def record_failure(self) -> None:
        self._failures += 1
        if self._failures >= self._threshold:
            self._opened_at = time.monotonic()
