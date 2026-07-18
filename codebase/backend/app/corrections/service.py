"""Correction & Learning Loop (M8, Bible §4.5, CP-10) — reasoning that outlives the person.

Every correction is an attributed, append-only graph edit AND a labelled eval example (the
Learning agent's input). Never anonymous (BR-7). The same question re-answers correctly
immediately (UC-3 AC) because prior corrections are injected into the retrieval context (the
Memory agent's job) and, where the correction targets a fact, the graph edit is live at once.
"""
from __future__ import annotations

from datetime import date

from ..audit.sink import AuditSink
from ..domain.graph_types import EdgeType, NodeLabel
from ..domain.models import Correction, Edge, Node
from ..graph.provenance_sink import ProvenanceSink
from ..ports import IGraphStore, IRelationalStore

_CORRECTION = "correction"


class CorrectionService:
    def __init__(
        self,
        graph: IGraphStore,
        relational: IRelationalStore,
        sink: ProvenanceSink,
        audit: AuditSink,
    ) -> None:
        self._g = graph
        self._rel = relational
        self._sink = sink
        self._audit = audit

    def submit(
        self,
        target_kind: str,
        target_ref: str,
        new_value: str,
        rationale: str,
        author: str,
        tenant: str,
        prior_value: str | None = None,
    ) -> Correction:
        correction = Correction(
            correction_id=self._sink.new_id("corr"),
            target_kind=target_kind,
            target_ref=target_ref,
            prior_value=prior_value,
            new_value=new_value,
            rationale=rationale,
            author=author,
            tenant=tenant,
        )
        # 1) Durable, attributed graph edit: a Correction node + CORRECTED_BY edge (CP-10).
        self._g.upsert_node(
            Node(id=correction.correction_id, label=NodeLabel.CORRECTION, tenant=tenant,
                 props={"author": author, "rationale": rationale, "new_value": new_value,
                        "prior_value": prior_value, "target_kind": target_kind,
                        "target_ref": target_ref}, effective_from=date.today())
        )
        if self._g.get_node(target_ref):
            self._g.upsert_edge(
                Edge(id=f"corr-{target_ref}-{correction.correction_id}",
                     type=EdgeType.CORRECTED_BY, src=target_ref, dst=correction.correction_id,
                     tenant=tenant)
            )
        # 2) Store the correction (also surfaced as prior-correction context for future answers).
        self._rel.put(_CORRECTION, correction.correction_id, correction.model_dump(mode="json"),
                      tenant)
        # 3) Learning agent input: a labelled eval example (CP-10, grows the regression suite).
        self._rel.put("eval_label", correction.correction_id,
                      {"kind": "correction", "target_ref": target_ref, "new_value": new_value,
                       "rationale": rationale, "author": author}, tenant)
        self._audit.log(author, "correction.submitted", tenant, target=target_ref,
                        detail={"correction_id": correction.correction_id, "new_value": new_value})
        return correction

    def history_for(self, target_ref: str, tenant: str) -> list[Correction]:
        return [Correction(**c) for c in self._rel.list(_CORRECTION, tenant)
                if c.get("target_ref") == target_ref]

    def all(self, tenant: str) -> list[Correction]:
        return [Correction(**c) for c in self._rel.list(_CORRECTION, tenant)]

    # Injected into the orchestrator as the Memory agent (prior corrections → context).
    def prior_corrections_for(self, question: str, tenant: str) -> list[str]:
        ql = question.lower()
        out: list[str] = []
        for c in self._rel.list(_CORRECTION, tenant):
            ref = str(c.get("target_ref", "")).lower()
            nv = str(c.get("new_value", ""))
            if ref and (ref in ql or any(tok in ql for tok in ref.split("-"))):
                out.append(f"Correction by {c['author']}: {nv} — {c['rationale']}")
            elif any(w in nv.lower() for w in ql.split() if len(w) > 4):
                out.append(f"Correction by {c['author']}: {nv} — {c['rationale']}")
        return out[:5]
