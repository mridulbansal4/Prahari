"""Knowledge Evolution & Decay (M4, Bible §5.10) — flag stale knowledge before it misleads.

Knowledge is flagged stale not by age alone but by triggers — equipment/vendor/SOP change,
expert departure, contradictory sensor evidence. A nightly job raises KnowledgeRisk flags.
Superseding a fact bounds it (effective_to), never deletes it (CP-7).
"""
from __future__ import annotations

from datetime import date
from typing import Any

from ..audit.sink import AuditSink
from ..domain.graph_types import EdgeType, NodeLabel
from ..domain.models import KnowledgeRiskFlag
from ..ports import IGraphStore, IRelationalStore
from .contradictions import ContradictionDetector

_FLAG = "knowledge_risk"
_META = "knowledge_meta"


class DecayJob:
    def __init__(
        self,
        graph: IGraphStore,
        relational: IRelationalStore,
        audit: AuditSink,
        contradictions: ContradictionDetector | None = None,
    ) -> None:
        self._g = graph
        self._rel = relational
        self._audit = audit
        self._contradictions = contradictions

    def run(self, tenant: str) -> list[KnowledgeRiskFlag]:
        """The nightly decay pass. Deterministic triggers over graph state."""
        # Detect disagreements first, so Trigger 2 below has something to read. Before this,
        # nothing in the system ever wrote a CONTRADICTS edge and that trigger was dead.
        if self._contradictions is not None:
            self._contradictions.scan(tenant)
        flags: list[KnowledgeRiskFlag] = []
        # Trigger 1: expert departure — a Person flagged retirement_risk who KNOWS a fact.
        for p in self._g.nodes_by_label(NodeLabel.PERSON.value, tenant):
            if p.props.get("retirement_risk"):
                for e in self._g.edges_from(p.id, EdgeType.KNOWS.value, tenant):
                    flags.append(self._flag("expert_departure", e.dst,
                                 f"Expertise held by {p.props.get('name')} (retirement risk) about "
                                 f"{e.dst} is at risk of being lost.", tenant))
        # Trigger 2: contradictions surfaced between spans. One flag per (subject, measure) —
        # the same disagreement usually shows up across several span pairs, and a reader wants
        # to be told once that two documents disagree, not once per sentence that proves it.
        seen_conflicts: set[str] = set()
        for e in self._g.all_edges(tenant):
            if e.type != EdgeType.CONTRADICTS:
                continue
            subject = str(e.props.get("subject") or e.src)
            measure = str(e.props.get("measure") or "value")
            key = f"{subject}:{measure}"
            if key in seen_conflicts:
                continue
            seen_conflicts.add(key)
            # The "between X and Y" phrasing is load-bearing — the console parses it to show
            # the two sides next to each other. The summary follows it, not replaces it.
            detail = str(e.props.get("summary") or "")
            flags.append(self._flag(
                "contradiction", key,
                f"Contradictory evidence between {e.props.get('left_doc', e.src)} and "
                f"{e.props.get('right_doc', e.dst)}. {detail}".strip(), tenant))
        # Trigger 3: vendor/SOP change markers on documents.
        for d in self._g.nodes_by_label(NodeLabel.DOCUMENT.value, tenant):
            if d.props.get("vendor_changed") or d.props.get("sop_changed"):
                flags.append(self._flag("vendor_change" if d.props.get("vendor_changed") else "sop_change",
                             d.id, f"Document {d.id} reflects a vendor/SOP change; dependent facts "
                             "may be stale.", tenant))
        self._rel.put(_META, "last_run", {"date": date.today().isoformat(), "count": len(flags)}, tenant)
        self._audit.log("system:decay", "knowledge_risk.job_ran", tenant,
                        detail={"flags": len(flags)})
        return flags

    def _flag(self, trigger: str, ref: str, desc: str, tenant: str) -> KnowledgeRiskFlag:
        flag = KnowledgeRiskFlag(flag_id=f"kr-{trigger}-{ref}", trigger=trigger,
                                 affected_fact_ref=ref, description=desc)
        self._rel.put(_FLAG, flag.flag_id, flag.model_dump(mode="json"), tenant)
        return flag

    def list_flags(self, tenant: str) -> list[KnowledgeRiskFlag]:
        return [KnowledgeRiskFlag(**f) for f in self._rel.list(_FLAG, tenant) if not f.get("resolved")]

    def last_run(self, tenant: str) -> dict[str, Any] | None:
        return self._rel.get(_META, "last_run", tenant)

    def reverify(self, flag_id: str, tenant: str, actor: str) -> None:
        f = self._rel.get(_FLAG, flag_id, tenant)
        if f:
            f["resolved"] = True
            self._rel.put(_FLAG, flag_id, f, tenant)
            self._audit.log(actor, "knowledge_risk.reverified", tenant, target=flag_id)

    def supersede(self, flag_id: str, tenant: str, actor: str) -> None:
        """Bound the flagged fact (effective_to), never delete it (CP-7)."""
        f = self._rel.get(_FLAG, flag_id, tenant)
        if not f:
            return
        ref = f["affected_fact_ref"]
        node = self._g.get_node(ref)
        if node:
            node.effective_to = date.today()
            self._g.upsert_node(node)
        f["resolved"] = True
        self._rel.put(_FLAG, flag_id, f, tenant)
        self._audit.log(actor, "knowledge_risk.superseded", tenant, target=ref)
