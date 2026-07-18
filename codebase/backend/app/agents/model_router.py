"""Model selection + CP-9 rung resolution (ADR-P02).

Picks the reasoning provider by availability + circuit-breaker state + any forced rung, and
reports the resulting degradation rung so the UI banner stays honest (never swallowed).
"""
from __future__ import annotations

from ..config import Settings
from ..resilience.circuit_breaker import CircuitBreaker
from ..resilience.degradation import Rung
from .providers import (
    AnthropicProvider,
    GeminiProvider,
    LocalOpenWeightsProvider,
    TemplateSynthProvider,
)


class ModelRouter:
    def __init__(self, settings: Settings) -> None:
        self._s = settings
        self._breaker = CircuitBreaker()
        self._template = TemplateSynthProvider()
        self._gemini = GeminiProvider(settings) if settings.gemini_api_key else None
        self._cloud = AnthropicProvider(settings) if settings.model_api_key else None
        self._local = LocalOpenWeightsProvider()

    def select(self) -> tuple[object, Rung]:
        forced = self._s.force_rung
        if forced in ("-model", "-vector", "-graph", "-everything"):
            return self._template, Rung(forced)
        if self._breaker.is_open:
            return self._template, Rung.NO_MODEL
        if self._gemini and self._gemini.available():
            return self._gemini, Rung.FULL
        if self._cloud and self._cloud.available():
            return self._cloud, Rung.FULL
        if self._local.available():
            return self._local, Rung.FULL
        # No prose model reachable → CP-9 -model rung with structured synthesis.
        return self._template, Rung.NO_MODEL

    def record_success(self) -> None:
        self._breaker.record_success()

    def record_failure(self) -> None:
        self._breaker.record_failure()
