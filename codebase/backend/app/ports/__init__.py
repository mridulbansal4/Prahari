"""Ports — the interfaces that domain/services depend on (never a concrete store).

Each port has exactly one embedded adapter and one production adapter today, and is the
documented extraction seam for a future service (Bible §2.4, ADR-006).
"""
from __future__ import annotations

from datetime import date
from typing import Any, Protocol, runtime_checkable

from ..domain.models import (
    AuditEntry,
    Edge,
    Node,
    Span,
)


@runtime_checkable
class IGraphStore(Protocol):
    """Bitemporal knowledge graph (CP-7). Writes of fact-bearing nodes/edges must pass through
    the ProvenanceSink (CP-1) — this port is the raw substrate below that gate."""

    def upsert_node(self, node: Node) -> None: ...
    def upsert_edge(self, edge: Edge) -> None: ...
    def get_node(self, node_id: str) -> Node | None: ...
    def get_span(self, span_id: str) -> Span | None: ...
    def upsert_span(self, span: Span) -> None: ...
    def nodes_by_label(self, label: str, tenant: str) -> list[Node]: ...
    def find_identifier(self, value: str, tenant: str) -> Node | None: ...
    def neighbours(
        self, node_id: str, edge_types: list[str] | None, tenant: str, as_of: date | None = None
    ) -> list[tuple[Edge, Node]]: ...
    def traverse(
        self,
        anchor_ids: list[str],
        edge_types: list[str] | None,
        max_hops: int,
        tenant: str,
        as_of: date | None = None,
    ) -> tuple[list[Node], list[Edge]]: ...
    def evidence_spans(self, node_id: str, tenant: str) -> list[Span]: ...
    def edges_from(self, node_id: str, edge_type: str, tenant: str) -> list[Edge]: ...
    def all_edges(self, tenant: str) -> list[Edge]: ...
    def delete_edge(self, edge_id: str) -> None: ...
    def snapshot(self) -> dict[str, Any]: ...


@runtime_checkable
class IVectorStore(Protocol):
    """Semantic search over document spans (Bible §3.3.3). Hits are grounding evidence, not
    answers; each carries {doc, page, span} for citation."""

    def upsert(self, span_id: str, text: str, payload: dict[str, Any], tenant: str) -> None: ...
    def search(
        self, query: str, k: int, tenant: str, filters: dict[str, Any] | None = None
    ) -> list[tuple[str, float, dict[str, Any]]]: ...


@runtime_checkable
class IRelationalStore(Protocol):
    """Metadata + append-only audit (Bible §8.5). Audit is append-only by construction; there
    is no update/delete on audit entries (§8.1 tampering control)."""

    def put(self, kind: str, key: str, value: dict[str, Any], tenant: str) -> None: ...
    def get(self, kind: str, key: str, tenant: str) -> dict[str, Any] | None: ...
    def list(self, kind: str, tenant: str) -> list[dict[str, Any]]: ...
    def delete(self, kind: str, key: str, tenant: str) -> None: ...
    def append_audit(self, entry: AuditEntry) -> None: ...
    def query_audit(
        self,
        tenant: str,
        actor: str | None = None,
        action: str | None = None,
        frm: str | None = None,
        to: str | None = None,
        limit: int = 200,
    ) -> list[AuditEntry]: ...


@runtime_checkable
class IModelProvider(Protocol):
    """Provider-abstracted reasoning model (CP-5). Concrete providers form the CP-9 rungs."""

    id: str
    rung: str  # "full" (cloud/local prose) | "-model" (template synth)

    def synthesize(self, prompt: str, context_spans: list[dict[str, Any]]) -> dict[str, Any]:
        """Return {answer, claims:[{text, citations:[span_id], confidence}], abstained, unresolved}.
        The provider may cite ONLY span ids present in ``context_spans`` (CP-2)."""
        ...

    def available(self) -> bool: ...
