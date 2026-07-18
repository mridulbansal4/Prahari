"""Decision Memory & Replay (M3, Bible §5.7 — additive, Could-scope, ADR-015).

Reconstructs a past reasoning chain: Observation → Hypothesis → Evidence → Decision →
Alternative(rejected) → RiskAccepted → Outcome → LessonLearned, connected by LED_TO edges, each
EVIDENCED_BY a span. The core investigation works without this (§5.7); absence is a clean empty
state, never an error.
"""
from __future__ import annotations

from typing import Any

from ..domain.graph_types import EdgeType, NodeLabel
from ..ports import IGraphStore

_DECISION_LABELS = [
    NodeLabel.OBSERVATION.value, NodeLabel.HYPOTHESIS.value, NodeLabel.EVIDENCE.value,
    NodeLabel.DECISION.value, NodeLabel.ALTERNATIVE.value, NodeLabel.RISK_ACCEPTED.value,
    NodeLabel.OUTCOME.value, NodeLabel.LESSON_LEARNED.value,
]


class DecisionReplayService:
    def __init__(self, graph: IGraphStore) -> None:
        self._g = graph

    def list_decisions(self, tenant: str) -> list[dict[str, Any]]:
        out = []
        for d in self._g.nodes_by_label(NodeLabel.DECISION.value, tenant):
            out.append({"decision_id": d.id, "title": d.props.get("title", d.id),
                        "date": d.props.get("date"), "asset_id": d.props.get("asset_id")})
        return out

    def replay(self, decision_id: str, tenant: str) -> dict[str, Any] | None:
        decision = self._g.get_node(decision_id)
        if not decision or decision.label != NodeLabel.DECISION:
            return None
        # Walk LED_TO in both directions to assemble the ordered chain.
        chain_nodes, _ = self._g.traverse([decision_id], [EdgeType.LED_TO.value], 6, tenant, as_of="9999-01-01")
        steps = []
        for n in chain_nodes:
            if n.label.value in _DECISION_LABELS:
                spans = self._g.evidence_spans(n.id, tenant)
                steps.append({
                    "id": n.id, "kind": n.label.value,
                    "title": n.props.get("title") or n.props.get("text") or n.id,
                    "detail": n.props.get("text") or n.props.get("rationale") or "",
                    "citations": [{"doc_id": s.doc_id, "page": s.page, "span_id": s.span_id}
                                  for s in spans],
                    "order": _order(n.label.value),
                })
        steps.sort(key=lambda s: s["order"])
        return {"decision_id": decision_id, "title": decision.props.get("title", decision_id),
                "steps": steps}


def _order(label: str) -> int:
    try:
        return _DECISION_LABELS.index(label)
    except ValueError:
        return 99
