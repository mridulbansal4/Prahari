"""Context assembly (Bible §3.4).

Assembled context = {resolved question, entity cards (from graph), evidence spans (cited),
prior corrections (org memory), as-of timestamp}. Every span carries its citation id so the
generator can only cite what it was given (enables CP-2 verification post-hoc).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date

from ..domain.models import GraphHop, Node, Span


@dataclass
class EntityCard:
    node_id: str
    label: str
    title: str
    facts: list[str] = field(default_factory=list)


@dataclass
class AssembledContext:
    question: str
    as_of: date | None
    entity_cards: list[EntityCard] = field(default_factory=list)
    spans: list[Span] = field(default_factory=list)
    graph_path: list[GraphHop] = field(default_factory=list)
    prior_corrections: list[str] = field(default_factory=list)
    anchors: list[Node] = field(default_factory=list)

    def as_provider_spans(self) -> list[dict]:
        # Dedup by span_id, preserve order.
        seen: set[str] = set()
        out = []
        for s in self.spans:
            if s.span_id in seen:
                continue
            seen.add(s.span_id)
            out.append({"span_id": s.span_id, "text": s.text, "doc_id": s.doc_id, "page": s.page})
        return out
