"""Organizational Memory (M5, Bible §5.2–5.3 Person/KNOWS) — capture expertise before it retires.

Feeds the "who to ask" field in M1's AbstainCard and the reviewer suggestion in M8. PII-minimal:
role/expertise/tenure/retirement-risk only — never an HR record (BR-9, Bible §8.8).

Capture stores the knowledge ITSELF, not just a label for it. When an item carries text, that
text is written as a provenance-stamped Span and indexed for retrieval, so a captured nugget —
"never restart P-101A before P-101B, you cavitate the header" — becomes citable evidence in an
answer exactly like a sentence from a PDF. That is the whole point of capturing it.
"""
from __future__ import annotations

from datetime import date
from typing import Any

from ..audit.sink import AuditSink
from ..domain.graph_types import EdgeType, NodeLabel
from ..domain.models import Edge, ExpertiseRecord, KnowledgeItem, Node, Span, WhoToAsk
from ..graph.provenance_sink import ProvenanceSink
from ..ports import IGraphStore, IRelationalStore, IVectorStore

_INVESTIGATION = "investigation"


def _doc_id_for(person_id: str) -> str:
    """Captured knowledge is filed under a per-person pseudo-document, so a citation points
    somewhere real instead of dangling."""
    return f"ORGMEM-{person_id}"


def _slug(v: str) -> str:
    keep = [c.lower() if c.isalnum() else "-" for c in v]
    return "".join(keep).strip("-")[:48] or "item"


class OrgMemoryService:
    def __init__(
        self,
        graph: IGraphStore,
        audit: AuditSink,
        vector: IVectorStore | None = None,
        relational: IRelationalStore | None = None,
        sink: ProvenanceSink | None = None,
    ) -> None:
        self._g = graph
        self._audit = audit
        self._v = vector
        self._rel = relational
        self._sink = sink

    def who_to_ask(
        self, anchor_ids: list[str], question: str, tenant: str = "demo"
    ) -> list[WhoToAsk]:
        """Persons whose KNOWS edges touch the anchors or the failure-modes in question."""
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
                label = str(
                    e.props.get("expertise") or (tgt.props.get("description") if tgt else "")
                )
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

    # ------------------------------------------------------------------- read

    def _answer_usage(self, tenant: str) -> dict[str, int]:
        """How many recorded answers cited each span. Real counts only — never an estimate."""
        if self._rel is None:
            return {}
        usage: dict[str, int] = {}
        for row in self._rel.list(_INVESTIGATION, tenant):
            for span_id in row.get("context_span_ids") or []:
                usage[str(span_id)] = usage.get(str(span_id), 0) + 1
        return usage

    def directory(self, tenant: str) -> list[ExpertiseRecord]:
        usage = self._answer_usage(tenant)
        out: list[ExpertiseRecord] = []
        for p in self._g.nodes_by_label(NodeLabel.PERSON.value, tenant):
            knows: list[KnowledgeItem] = []
            for e in self._g.edges_from(p.id, EdgeType.KNOWS.value, tenant):
                tgt = self._g.get_node(e.dst)
                label = str(e.props.get("expertise")
                            or (tgt.props.get("tag") or tgt.props.get("description")
                                if tgt else ""))
                span_id = e.props.get("span_id")
                tags = e.props.get("tags") or []
                knows.append(KnowledgeItem(
                    target_kind=tgt.label.value if tgt else "?",
                    target_ref=e.dst,
                    label=label,
                    text=str(e.props.get("text") or ""),
                    kind=str(e.props.get("kind") or "tip"),
                    tags=[str(t) for t in tags] if isinstance(tags, list) else [],
                    captured_on=e.props.get("captured_on"),
                    span_id=str(span_id) if span_id else None,
                    used_in_answers=usage.get(str(span_id), 0) if span_id else 0,
                ))
            out.append(ExpertiseRecord(
                person_id=p.id, name=str(p.props.get("name", p.id)),
                role=str(p.props.get("role", "")),
                tenure_years=int(p.props.get("tenure_years", 0)),
                knows=knows, retirement_risk=bool(p.props.get("retirement_risk", False))))
        return out

    # ------------------------------------------------------------------ write

    def upsert_person(self, person_id: str, name: str, role: str, tenure_years: int,
                      retirement_risk: bool, tenant: str, actor: str) -> None:
        self._g.upsert_node(Node(id=person_id, label=NodeLabel.PERSON, tenant=tenant,
                            props={"name": name, "role": role, "tenure_years": tenure_years,
                                   "retirement_risk": retirement_risk},
                            effective_from=date.today()))
        self._audit.log(actor, "org_memory.updated", tenant, target=person_id)

    def add_knows(
        self,
        person_id: str,
        target_ref: str,
        expertise: str,
        tenant: str,
        actor: str,
        text: str = "",
        kind: str = "tip",
        tags: list[str] | None = None,
        captured_on: str | None = None,
    ) -> KnowledgeItem:
        """Record what someone knows.

        `expertise` is the short title. `text` is the knowledge itself and is preserved
        verbatim — the previous signature accepted only a label, so a capture form would have
        appeared to work while silently discarding the thing worth keeping.
        """
        clean_tags = [t.strip() for t in (tags or []) if t and t.strip()]
        on = captured_on or date.today().isoformat()
        span_id: str | None = None

        if text.strip() and self._sink is not None:
            doc_id = _doc_id_for(person_id)
            span_id = f"{doc_id}:{_slug(expertise or target_ref)}"
            body = f"{expertise}: {text}" if expertise else text
            self._sink.write_span(Span(span_id=span_id, doc_id=doc_id, page=None,
                                       text=body, tenant=tenant))
            if self._v is not None:
                # Indexed so retrieval can surface it: this is what makes a captured nugget
                # citable in an answer rather than trapped on a profile page.
                self._v.upsert(span_id, body,
                               {"doc_id": doc_id, "page": None, "source": "org_memory",
                                "person_id": person_id}, tenant)

        props: dict[str, Any] = {"expertise": expertise, "text": text, "kind": kind,
                                 "tags": clean_tags, "captured_on": on}
        if span_id:
            props["span_id"] = span_id
        # Edge id keys on the item, not just the target, so one person can hold several
        # distinct pieces of knowledge about the same asset.
        edge_id = f"knows-{person_id}-{target_ref}-{_slug(expertise)}" if expertise \
            else f"knows-{person_id}-{target_ref}"
        self._g.upsert_edge(Edge(id=edge_id, type=EdgeType.KNOWS, src=person_id,
                                 dst=target_ref, tenant=tenant, props=props))
        self._audit.log(actor, "org_memory.captured", tenant, target=person_id,
                        detail={"target_ref": target_ref, "kind": kind, "has_text": bool(text)})
        tgt = self._g.get_node(target_ref)
        return KnowledgeItem(
            target_kind=tgt.label.value if tgt else "?", target_ref=target_ref,
            label=expertise, text=text, kind=kind, tags=clean_tags, captured_on=on,
            span_id=span_id,
        )
