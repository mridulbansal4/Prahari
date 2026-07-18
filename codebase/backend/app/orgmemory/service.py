"""Organizational Memory (M5, Bible §5.2–5.3 Person/KNOWS) — capture expertise before it retires.

Feeds the "who to ask" field in M1's AbstainCard and the reviewer suggestion in M8. PII-minimal:
role/expertise/tenure/retirement-risk only — never an HR record (BR-9, Bible §8.8).
"""
from __future__ import annotations

from datetime import date

from ..audit.sink import AuditSink
from ..domain.graph_types import EdgeType, NodeLabel
from ..domain.models import Edge, ExpertiseRecord, Node, WhoToAsk
from ..ports import IGraphStore


class OrgMemoryService:
    def __init__(self, graph: IGraphStore, audit: AuditSink) -> None:
        self._g = graph
        self._audit = audit

    def who_to_ask(self, anchor_ids: list[str], question: str) -> list[WhoToAsk]:
        """Persons whose KNOWS edges touch the anchors or the failure-modes in question."""
        tenant = "demo"
        targets: set[str] = set(anchor_ids)
        # include failure modes / topics inferred from the question text
        ql = question.lower()
        people = self._g.nodes_by_label(NodeLabel.PERSON.value, tenant)
        scored: list[tuple[int, WhoToAsk]] = []
        for p in people:
            knows_edges = self._g.edges_from(p.id, EdgeType.KNOWS.value, tenant)
            expertise_hits = []
            score = 0
            for e in knows_edges:
                tgt = self._g.get_node(e.dst)
                label = str(e.props.get("expertise") or (tgt.props.get("description") if tgt else ""))
                if e.dst in targets:
                    score += 3
                    expertise_hits.append(label)
                elif label and any(w in ql for w in label.lower().split() if len(w) > 3):
                    score += 1
                    expertise_hits.append(label)
            if score > 0:
                scored.append((score, WhoToAsk(person=str(p.props.get("name", p.id)),
                              expertise="; ".join(expertise_hits[:2]) or "general",
                              tenure_years=p.props.get("tenure_years"))))
        scored.sort(key=lambda x: x[0], reverse=True)
        if not scored:  # honest fallback: most senior person on file
            people.sort(key=lambda p: p.props.get("tenure_years", 0), reverse=True)
            return [WhoToAsk(person=str(p.props.get("name", p.id)), expertise="general",
                    tenure_years=p.props.get("tenure_years")) for p in people[:1]]
        return [w for _, w in scored[:3]]

    def directory(self, tenant: str) -> list[ExpertiseRecord]:
        out: list[ExpertiseRecord] = []
        for p in self._g.nodes_by_label(NodeLabel.PERSON.value, tenant):
            knows = []
            for e in self._g.edges_from(p.id, EdgeType.KNOWS.value, tenant):
                tgt = self._g.get_node(e.dst)
                knows.append({"target_kind": tgt.label.value if tgt else "?", "target_ref": e.dst,
                              "label": str(e.props.get("expertise")
                                           or (tgt.props.get("tag") or tgt.props.get("description")
                                               if tgt else ""))})
            out.append(ExpertiseRecord(person_id=p.id, name=str(p.props.get("name", p.id)),
                       role=str(p.props.get("role", "")), tenure_years=int(p.props.get("tenure_years", 0)),
                       knows=knows, retirement_risk=bool(p.props.get("retirement_risk", False))))
        return out

    def upsert_person(self, person_id: str, name: str, role: str, tenure_years: int,
                      retirement_risk: bool, tenant: str, actor: str) -> None:
        self._g.upsert_node(Node(id=person_id, label=NodeLabel.PERSON, tenant=tenant,
                            props={"name": name, "role": role, "tenure_years": tenure_years,
                                   "retirement_risk": retirement_risk}, effective_from=date.today()))
        self._audit.log(actor, "org_memory.updated", tenant, target=person_id)

    def add_knows(self, person_id: str, target_ref: str, expertise: str, tenant: str, actor: str) -> None:
        self._g.upsert_edge(Edge(id=f"knows-{person_id}-{target_ref}", type=EdgeType.KNOWS,
                            src=person_id, dst=target_ref, tenant=tenant,
                            props={"expertise": expertise}))
        self._audit.log(actor, "org_memory.updated", tenant, target=person_id)
