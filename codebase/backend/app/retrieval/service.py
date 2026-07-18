"""Retrieval router service — dual graph + vector retrieval with fusion (Bible §3.3).

Produces an AssembledContext: anchor resolution → bounded graph traversal (with source spans on
each node) → vector enrichment → fusion/dedup → context budget. Emits GraphHops for the live
streaming traversal (Bible §7.4).
"""
from __future__ import annotations

import re
from datetime import date

from ..config import Settings
from ..domain.graph_types import EdgeType, NodeLabel
from ..domain.models import GraphHop, Node, Span
from ..ports import IGraphStore, IVectorStore
from .context import AssembledContext, EntityCard
from .router import Route, classify

# Edge types that carry causal / investigative meaning for multi-hop traversal.
_INVESTIGATION_EDGES = [
    EdgeType.RESOLVED_AS.value,
    EdgeType.CONNECTED_TO.value,
    EdgeType.PART_OF.value,
    EdgeType.HAS_WORKORDER.value,
    EdgeType.HAS_INSPECTION.value,
    EdgeType.HAS_INCIDENT.value,
    EdgeType.EXHIBITS.value,
    EdgeType.MONITORS.value,
]

_TAG = re.compile(r"\b([A-Z]{1,4}-?\d{2,4}[A-Z]?)\b")


class RetrievalRouter:
    def __init__(self, graph: IGraphStore, vector: IVectorStore, settings: Settings) -> None:
        self._g = graph
        self._v = vector
        self._s = settings

    # -------------------------------------------------------------- anchor resolution
    def _resolve_anchors(self, question: str, tenant: str, context_asset_id: str | None) -> list[Node]:
        anchors: list[Node] = []
        if context_asset_id:
            n = self._g.get_node(context_asset_id)
            if n:
                anchors.append(n)
        # Tag-like tokens → Identifier → RESOLVED_AS → Asset (the moat edge, §5.6).
        for tok in _TAG.findall(question):
            ident = self._g.find_identifier(tok, tenant)
            if ident:
                for e in self._g.edges_from(ident.id, EdgeType.RESOLVED_AS.value, tenant):
                    asset = self._g.get_node(e.dst)
                    if asset and asset.id not in {a.id for a in anchors}:
                        anchors.append(asset)
        # Fallback: fuzzy match asset tags / aliases mentioned by name.
        if not anchors:
            ql = question.lower()
            for asset in self._g.nodes_by_label(NodeLabel.ASSET.value, tenant):
                tag = str(asset.props.get("tag", "")).lower()
                name = str(asset.props.get("name", "")).lower()
                if (tag and tag in ql) or (name and name in ql):
                    anchors.append(asset)
        return anchors

    # -------------------------------------------------------------------- retrieval
    def retrieve(
        self,
        question: str,
        tenant: str,
        as_of: date | None = None,
        context_asset_id: str | None = None,
        vector_enabled: bool = True,
        graph_enabled: bool = True,
    ) -> tuple[AssembledContext, Route]:
        route = classify(question)
        ctx = AssembledContext(question=question, as_of=as_of)

        anchors: list[Node] = []
        if graph_enabled:
            anchors = self._resolve_anchors(question, tenant, context_asset_id)
            ctx.anchors = anchors

        # --- graph traversal ---
        if graph_enabled and anchors:
            nodes, edges = self._g.traverse(
                [a.id for a in anchors], _INVESTIGATION_EDGES, self._s.max_hops, tenant, as_of
            )
            node_by_id = {n.id: n for n in nodes}
            # Build entity cards + collect provenance spans on every touched node.
            for n in nodes:
                if n.label in (NodeLabel.SPAN, NodeLabel.IDENTIFIER):
                    continue
                card = EntityCard(
                    node_id=n.id,
                    label=n.label.value,
                    title=str(n.props.get("tag") or n.props.get("name") or n.id),
                    facts=[f"{k}: {v}" for k, v in n.props.items() if k not in ("tag", "name")][:6],
                )
                ctx.entity_cards.append(card)
                for sp in self._g.evidence_spans(n.id, tenant):
                    ctx.spans.append(sp)
            # Ordered hops for the live traversal animation.
            for a in anchors:
                ctx.graph_path.append(GraphHop(node=a.id, node_label=a.label.value,
                                               detail=str(a.props.get("tag") or a.id)))
            for e in edges:
                if e.type == EdgeType.EVIDENCED_BY:
                    continue
                dst = node_by_id.get(e.dst)
                ctx.graph_path.append(
                    GraphHop(
                        edge=e.type.value,
                        node=e.dst,
                        node_label=dst.label.value if dst else None,
                        detail=(str(dst.props.get("tag") or dst.props.get("name") or e.dst)
                                if dst else None),
                    )
                )

        # --- vector enrichment (grounding evidence, not answers) ---
        if vector_enabled:
            for span_id, _score, payload in self._v.search(question, self._s.retrieval_k, tenant):
                sp = self._g.get_span(span_id)
                if sp:
                    ctx.spans.append(sp)
                elif payload.get("text"):
                    ctx.spans.append(
                        Span(span_id=span_id, doc_id=payload.get("doc_id", ""),
                             page=payload.get("page"), text=payload["text"], tenant=tenant)
                    )

        # --- fusion: dedup + budget (silence over noise, prefer high-provenance) ---
        ctx.spans = self._dedup_budget(ctx.spans)
        return ctx, route

    def _dedup_budget(self, spans: list[Span]) -> list[Span]:
        seen: set[str] = set()
        out: list[Span] = []
        for s in spans:
            if s.span_id in seen:
                continue
            seen.add(s.span_id)
            out.append(s)
            if len(out) >= self._s.context_span_budget:
                break
        return out
