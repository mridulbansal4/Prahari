"""ProvenanceSink — the one write gateway for fact-bearing graph writes (CP-1 / BR-1).

No module writes a fact-bearing node or edge directly to the graph store. Everything routes
through here, which *rejects* any fact-bearing write that lacks at least one EVIDENCED_BY span.
This is what makes CP-1 an enforced mechanism, not a hope (Bible §12.3, §14.10).
"""
from __future__ import annotations

import uuid

from ..domain.errors import ProvenanceViolation
from ..domain.graph_types import FACT_BEARING, FACT_BEARING_EDGES, EdgeType
from ..domain.models import Edge, Node, Span
from ..ports import IGraphStore


class ProvenanceSink:
    def __init__(self, graph: IGraphStore) -> None:
        self._graph = graph

    def write_span(self, span: Span) -> None:
        self._graph.upsert_span(span)

    def write_node(self, node: Node, spans: list[Span] | None = None) -> Node:
        """Write a node and its provenance edges. Fact-bearing nodes require >=1 span."""
        spans = spans or []
        if node.label in FACT_BEARING and not spans:
            # Allow an already-evidenced node (re-upsert) only if provenance already exists.
            existing = self._graph.evidence_spans(node.id, node.tenant)
            if not existing:
                raise ProvenanceViolation(
                    f"Fact-bearing node {node.label.value}:{node.id} admitted with no source span "
                    "(CP-1/BR-1).",
                    {"node_id": node.id, "label": node.label.value},
                )
        self._graph.upsert_node(node)
        for sp in spans:
            self._graph.upsert_span(sp)
            self._graph.upsert_edge(
                Edge(
                    id=f"ev-{node.id}-{sp.span_id}",
                    type=EdgeType.EVIDENCED_BY,
                    src=node.id,
                    dst=sp.span_id,
                    tenant=node.tenant,
                    confidence=1.0,
                )
            )
        return node

    def write_edge(self, edge: Edge, spans: list[Span] | None = None) -> Edge:
        spans = spans or []
        if edge.type in FACT_BEARING_EDGES and not spans:
            raise ProvenanceViolation(
                f"Fact-bearing edge {edge.type.value} ({edge.src}->{edge.dst}) admitted with no "
                "source span (CP-1/BR-1).",
                {"edge": edge.type.value, "src": edge.src, "dst": edge.dst},
            )
        self._graph.upsert_edge(edge)
        for sp in spans:
            self._graph.upsert_span(sp)
            # Evidence the edge by attaching provenance to its endpoints' shared span reference.
            self._graph.upsert_edge(
                Edge(
                    id=f"ev-edge-{edge.id}-{sp.span_id}",
                    type=EdgeType.EVIDENCED_BY,
                    src=edge.src,
                    dst=sp.span_id,
                    tenant=edge.tenant,
                )
            )
        return edge

    @staticmethod
    def new_id(prefix: str) -> str:
        return f"{prefix}-{uuid.uuid4().hex[:12]}"
