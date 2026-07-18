"""Investigation service (M1) — runs the orchestrator, streams events, persists the result.

Persistence enables: GET /v1/investigations/{id}, audit reproducibility (CP-7), and the semantic
cache (a re-asked scripted question returns instantly — Bible §3.5, §11.7). Every answer logs
{question, context span ids, prompt manifest hash, model id, verdict} (Bible §8.5).
"""
from __future__ import annotations

import hashlib
import uuid
from collections.abc import AsyncIterator
from datetime import date
from typing import Any

from ..agents.orchestrator import Event, Orchestrator
from ..audit.sink import AuditSink
from ..domain.models import InvestigationResult
from ..ports import IRelationalStore

_INV = "investigation"
_CACHE = "semantic_cache"


class InvestigationService:
    def __init__(self, orchestrator: Orchestrator, relational: IRelationalStore, audit: AuditSink) -> None:
        self._orch = orchestrator
        self._rel = relational
        self._audit = audit

    @staticmethod
    def new_id() -> str:
        return f"inv-{uuid.uuid4().hex[:12]}"

    def _cache_key(self, question: str, as_of: date | None, tenant: str) -> str:
        raw = f"{question.strip().lower()}|{as_of or 'now'}|{tenant}"
        return hashlib.sha256(raw.encode()).hexdigest()[:20]

    async def run_stream(
        self,
        investigation_id: str,
        question: str,
        tenant: str,
        actor: str,
        as_of: date | None = None,
        context_asset_id: str | None = None,
        parent_id: str | None = None,
    ) -> AsyncIterator[Event]:
        self._audit.log(actor, "investigation.asked", tenant, target=investigation_id,
                        detail={"question": question, "as_of": str(as_of) if as_of else None,
                                "parent": parent_id})
        final: InvestigationResult | None = None
        async for ev in self._orch.run(investigation_id, question, tenant, as_of=as_of,
                                        context_asset_id=context_asset_id, parent_id=parent_id):
            if ev.type == "done":
                final = InvestigationResult(**ev.data["result"])
            yield ev
        if final:
            self._persist(final, tenant)
            self._audit.log(actor, "investigation.answered", tenant, target=investigation_id,
                            detail={"abstained": final.abstained,
                                    "context_span_ids": final.context_span_ids,
                                    "prompt_manifest_hash": final.prompt_manifest_hash,
                                    "model_id": final.model_id,
                                    "verdict": "abstained" if final.abstained else "grounded",
                                    "degradation_level": final.degradation_level})

    def _persist(self, result: InvestigationResult, tenant: str) -> None:
        self._rel.put(_INV, result.investigation_id, result.model_dump(mode="json"), tenant)
        key = self._cache_key(result.question, result.as_of, tenant)
        self._rel.put(_CACHE, key, {"investigation_id": result.investigation_id}, tenant)

    def get(self, investigation_id: str, tenant: str) -> InvestigationResult | None:
        raw = self._rel.get(_INV, investigation_id, tenant)
        return InvestigationResult(**raw) if raw else None

    def recent(self, tenant: str, limit: int = 8) -> list[dict[str, Any]]:
        items = self._rel.list(_INV, tenant)
        items.sort(key=lambda r: r.get("created_at", ""), reverse=True)
        return [{"investigation_id": r["investigation_id"], "question": r["question"],
                 "abstained": r.get("abstained", False)} for r in items[:limit]]
