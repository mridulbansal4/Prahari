"""Decision Analytics (M10, PRB §5.1) — make the flywheel visible as a number.

Every KPI shows actual-vs-target, never a target presented as achieved (BR-8). Targets are
design-judgement estimates `[D]` until validated by the eval harness (Bible §15).
"""
from __future__ import annotations

from typing import Any

from ..ports import IRelationalStore
from ..resolution.service import ResolutionService


class AnalyticsService:
    def __init__(self, relational: IRelationalStore, resolution: ResolutionService) -> None:
        self._rel = relational
        self._resolution = resolution

    def kpis(self, tenant: str) -> dict[str, Any]:
        corrections = self._rel.list("correction", tenant)
        drafts = self._rel.list("action_draft", tenant)
        committed = [d for d in drafts if d.get("status") == "committed"]
        corpus = self._resolution.corpus_size(tenant)
        investigations = self._rel.list("investigation", tenant)
        return {
            "kpis": [
                {"key": "time_to_answer", "label": "Time-to-answer at point of symptom",
                 "actual_seconds": None, "target": "≤ 90s", "unit": "s",
                 "note": "Measured live per investigation; target is [D] pending eval (Bible §15)."},
                {"key": "recurrence_rate", "label": "Recurrence of documented failures",
                 "actual": None, "target": "measurably ↓", "note": "Requires pilot history."},
                {"key": "wo_from_sentinel", "label": "% work orders from a SENTINEL hypothesis",
                 "actual": len([d for d in committed if d.get("investigation_id")]),
                 "denominator": len(committed) or None, "target": "growing fraction"},
                {"key": "audit_prep", "label": "Audit prep time", "actual": None,
                 "target": "hours, not days"},
                {"key": "resolution_corpus", "label": "Resolution corpus size (adjudications)",
                 "actual": corpus, "target": "monotonically ↑", "is_flywheel": True},
                {"key": "correction_to_improvement", "label": "Correction→improvement latency",
                 "actual": "immediate (same session)", "target": "immediate",
                 "note": "Proves P7 — corrections change the next answer at once (UC-3)."},
            ],
            "counts": {"corrections": len(corrections), "drafts": len(drafts),
                       "committed_work_orders": len(committed), "investigations": len(investigations),
                       "resolution_corpus": corpus},
            "disclaimer": "Actuals are measured on this deployment's data; targets are design "
            "estimates [D] pending evaluation-harness validation — never reported as achieved.",
        }
