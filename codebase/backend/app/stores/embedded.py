"""Embedded store family (ADR-P01) — SQLite-backed, durable across processes.

Implements IGraphStore + IVectorStore + IRelationalStore over a single SQLite file so `seed` and
`uvicorn` share state with zero external services. This is the Bible's air-gap substrate
(§8.6), not a mock: it enforces the same bitemporal (CP-7) and append-only-audit (§8.1)
semantics the production adapters do.

Concurrency: SQLite in WAL mode; the FastAPI app is single-process for the hackathon box. A
process-wide lock guards writes.
"""
from __future__ import annotations

import json
import sqlite3
import threading
from datetime import date, datetime
from pathlib import Path
from typing import Any

from ..domain.graph_types import EdgeType
from ..domain.models import AuditEntry, Edge, Node, Span
from ..embeddings import local_embedder

_LOCK = threading.RLock()


def _ser(obj: Any) -> str:
    def default(o: Any) -> Any:
        if isinstance(o, (datetime, date)):
            return o.isoformat()
        if isinstance(o, tuple):
            return list(o)
        return str(o)

    return json.dumps(obj, default=default)


def _as_date(v: Any) -> date | None:
    if v in (None, ""):
        return None
    if isinstance(v, date):
        return v
    return date.fromisoformat(str(v)[:10])


class EmbeddedStore:
    """One object implementing three ports over SQLite + an in-memory vector index."""

    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path
        self._conn = sqlite3.connect(str(db_path), check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.execute("PRAGMA foreign_keys=ON")
        self._init_schema()
        # In-memory vector index loaded from SQLite on start (rebuildable/derived store).
        self._vectors: dict[str, tuple[str, list[float], dict[str, Any], str]] = {}
        self._load_vectors()

    # ------------------------------------------------------------------ schema / lifecycle
    def _init_schema(self) -> None:
        with _LOCK, self._conn:
            self._conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS nodes (
                    id TEXT PRIMARY KEY, tenant TEXT, label TEXT, props TEXT,
                    effective_from TEXT, effective_to TEXT, recorded_at TEXT,
                    provisional INTEGER, superseded_by TEXT
                );
                CREATE TABLE IF NOT EXISTS edges (
                    id TEXT PRIMARY KEY, tenant TEXT, type TEXT, src TEXT, dst TEXT, props TEXT,
                    effective_from TEXT, effective_to TEXT, recorded_at TEXT, confidence REAL
                );
                CREATE TABLE IF NOT EXISTS spans (
                    span_id TEXT PRIMARY KEY, tenant TEXT, doc_id TEXT, page INTEGER,
                    text TEXT, char_range TEXT
                );
                CREATE TABLE IF NOT EXISTS vectors (
                    span_id TEXT PRIMARY KEY, tenant TEXT, text TEXT, vec TEXT, payload TEXT
                );
                CREATE TABLE IF NOT EXISTS kv (
                    kind TEXT, tenant TEXT, key TEXT, value TEXT, PRIMARY KEY (kind, tenant, key)
                );
                CREATE TABLE IF NOT EXISTS audit (
                    entry_id TEXT PRIMARY KEY, tenant TEXT, actor TEXT, action TEXT,
                    target TEXT, detail TEXT, ts TEXT
                );
                CREATE INDEX IF NOT EXISTS idx_nodes_label ON nodes(tenant, label);
                CREATE INDEX IF NOT EXISTS idx_edges_src ON edges(tenant, src);
                CREATE INDEX IF NOT EXISTS idx_edges_dst ON edges(tenant, dst);
                CREATE INDEX IF NOT EXISTS idx_edges_type ON edges(tenant, type);
                CREATE INDEX IF NOT EXISTS idx_audit_actor ON audit(tenant, actor);
                """
            )

    def _load_vectors(self) -> None:
        for row in self._conn.execute("SELECT span_id, tenant, text, vec, payload FROM vectors"):
            self._vectors[row["span_id"]] = (
                row["tenant"],
                json.loads(row["vec"]),
                json.loads(row["payload"]),
                row["text"],
            )

    # ----------------------------------------------------------------------- IGraphStore
    def _row_to_node(self, r: sqlite3.Row) -> Node:
        return Node(
            id=r["id"],
            label=r["label"],
            props=json.loads(r["props"]),
            tenant=r["tenant"],
            effective_from=_as_date(r["effective_from"]),
            effective_to=_as_date(r["effective_to"]),
            recorded_at=datetime.fromisoformat(r["recorded_at"]),
            provisional=bool(r["provisional"]),
            superseded_by=r["superseded_by"],
        )

    def _row_to_edge(self, r: sqlite3.Row) -> Edge:
        return Edge(
            id=r["id"],
            type=EdgeType(r["type"]),
            src=r["src"],
            dst=r["dst"],
            props=json.loads(r["props"]),
            tenant=r["tenant"],
            effective_from=_as_date(r["effective_from"]),
            effective_to=_as_date(r["effective_to"]),
            recorded_at=datetime.fromisoformat(r["recorded_at"]),
            confidence=r["confidence"],
        )

    def upsert_node(self, node: Node) -> None:
        with _LOCK, self._conn:
            self._conn.execute(
                """INSERT INTO nodes VALUES (?,?,?,?,?,?,?,?,?)
                   ON CONFLICT(id) DO UPDATE SET label=excluded.label, props=excluded.props,
                   effective_from=excluded.effective_from, effective_to=excluded.effective_to,
                   recorded_at=excluded.recorded_at, provisional=excluded.provisional,
                   superseded_by=excluded.superseded_by""",
                (
                    node.id, node.tenant, node.label.value, _ser(node.props),
                    node.effective_from.isoformat() if node.effective_from else None,
                    node.effective_to.isoformat() if node.effective_to else None,
                    node.recorded_at.isoformat(), int(node.provisional), node.superseded_by,
                ),
            )

    def upsert_edge(self, edge: Edge) -> None:
        with _LOCK, self._conn:
            self._conn.execute(
                """INSERT INTO edges VALUES (?,?,?,?,?,?,?,?,?,?)
                   ON CONFLICT(id) DO UPDATE SET type=excluded.type, src=excluded.src,
                   dst=excluded.dst, props=excluded.props, effective_from=excluded.effective_from,
                   effective_to=excluded.effective_to, recorded_at=excluded.recorded_at,
                   confidence=excluded.confidence""",
                (
                    edge.id, edge.tenant, edge.type.value, edge.src, edge.dst, _ser(edge.props),
                    edge.effective_from.isoformat() if edge.effective_from else None,
                    edge.effective_to.isoformat() if edge.effective_to else None,
                    edge.recorded_at.isoformat(), edge.confidence,
                ),
            )

    def delete_edge(self, edge_id: str) -> None:
        with _LOCK, self._conn:
            self._conn.execute("DELETE FROM edges WHERE id=?", (edge_id,))

    def get_node(self, node_id: str) -> Node | None:
        r = self._conn.execute("SELECT * FROM nodes WHERE id=?", (node_id,)).fetchone()
        return self._row_to_node(r) if r else None

    def upsert_span(self, span: Span) -> None:
        with _LOCK, self._conn:
            self._conn.execute(
                """INSERT INTO spans VALUES (?,?,?,?,?,?)
                   ON CONFLICT(span_id) DO UPDATE SET text=excluded.text""",
                (
                    span.span_id, span.tenant, span.doc_id, span.page, span.text,
                    _ser(list(span.char_range)) if span.char_range else None,
                ),
            )

    @staticmethod
    def _row_to_span(r: Any) -> Span:
        cr = json.loads(r["char_range"]) if r["char_range"] else None
        return Span(
            span_id=r["span_id"], tenant=r["tenant"], doc_id=r["doc_id"], page=r["page"],
            text=r["text"], char_range=tuple(cr) if cr else None,
        )

    def get_span(self, span_id: str) -> Span | None:
        r = self._conn.execute("SELECT * FROM spans WHERE span_id=?", (span_id,)).fetchone()
        return self._row_to_span(r) if r else None

    def nodes_by_label(self, label: str, tenant: str) -> list[Node]:
        rows = self._conn.execute(
            "SELECT * FROM nodes WHERE tenant=? AND label=?", (tenant, label)
        ).fetchall()
        return [self._row_to_node(r) for r in rows]

    def find_identifier(self, value: str, tenant: str) -> Node | None:
        for n in self.nodes_by_label("Identifier", tenant):
            if str(n.props.get("value", "")).strip().lower() == value.strip().lower():
                return n
        return None

    def edges_from(self, node_id: str, edge_type: str, tenant: str) -> list[Edge]:
        rows = self._conn.execute(
            "SELECT * FROM edges WHERE tenant=? AND src=? AND type=?", (tenant, node_id, edge_type)
        ).fetchall()
        return [self._row_to_edge(r) for r in rows]

    def all_edges(self, tenant: str) -> list[Edge]:
        rows = self._conn.execute("SELECT * FROM edges WHERE tenant=?", (tenant,)).fetchall()
        return [self._row_to_edge(r) for r in rows]

    def all_spans(self, tenant: str) -> list[Span]:
        rows = self._conn.execute("SELECT * FROM spans WHERE tenant=?", (tenant,)).fetchall()
        return [self._row_to_span(r) for r in rows]

    def spans_for_document(self, doc_id: str, tenant: str) -> list[Span]:
        rows = self._conn.execute(
            "SELECT * FROM spans WHERE doc_id=? AND tenant=?", (doc_id, tenant)
        ).fetchall()
        return [self._row_to_span(r) for r in rows]

    @staticmethod
    def _edge_valid_as_of(edge: Edge, as_of: date | None) -> bool:
        if as_of is None:
            return edge.effective_to is None  # current view: only unbounded (live) edges
        if edge.effective_from and edge.effective_from > as_of:
            return False
        if edge.effective_to and edge.effective_to <= as_of:
            return False
        return True

    def neighbours(
        self, node_id: str, edge_types: list[str] | None, tenant: str, as_of: date | None = None
    ) -> list[tuple[Edge, Node]]:
        rows = self._conn.execute(
            "SELECT * FROM edges WHERE tenant=? AND (src=? OR dst=?)", (tenant, node_id, node_id)
        ).fetchall()
        out: list[tuple[Edge, Node]] = []
        for r in rows:
            e = self._row_to_edge(r)
            if edge_types and e.type.value not in edge_types:
                continue
            if not self._edge_valid_as_of(e, as_of):
                continue
            other_id = e.dst if e.src == node_id else e.src
            other = self.get_node(other_id)
            if other:
                out.append((e, other))
        return out

    def traverse(
        self,
        anchor_ids: list[str],
        edge_types: list[str] | None,
        max_hops: int,
        tenant: str,
        as_of: date | None = None,
    ) -> tuple[list[Node], list[Edge]]:
        seen_nodes: dict[str, Node] = {}
        seen_edges: dict[str, Edge] = {}
        frontier = list(anchor_ids)
        for nid in anchor_ids:
            n = self.get_node(nid)
            if n:
                seen_nodes[nid] = n
        for _ in range(max_hops):
            nxt: list[str] = []
            for nid in frontier:
                for e, other in self.neighbours(nid, edge_types, tenant, as_of):
                    seen_edges[e.id] = e
                    if other.id not in seen_nodes:
                        seen_nodes[other.id] = other
                        nxt.append(other.id)
            frontier = nxt
            if not frontier:
                break
        return list(seen_nodes.values()), list(seen_edges.values())

    def evidence_spans(self, node_id: str, tenant: str) -> list[Span]:
        spans: list[Span] = []
        for e in self.edges_from(node_id, EdgeType.EVIDENCED_BY.value, tenant):
            s = self.get_span(e.dst)
            if s:
                spans.append(s)
        return spans

    def snapshot(self) -> dict[str, Any]:
        counts = {}
        for tbl in ("nodes", "edges", "spans", "vectors", "audit"):
            counts[tbl] = self._conn.execute(f"SELECT COUNT(*) c FROM {tbl}").fetchone()["c"]
        return counts

    # ----------------------------------------------------------------------- IVectorStore
    def upsert(self, span_id: str, text: str, payload: dict[str, Any], tenant: str) -> None:
        vec = local_embedder.embed(text)
        with _LOCK, self._conn:
            self._conn.execute(
                """INSERT INTO vectors VALUES (?,?,?,?,?)
                   ON CONFLICT(span_id) DO UPDATE SET text=excluded.text, vec=excluded.vec,
                   payload=excluded.payload""",
                (span_id, tenant, text, _ser(vec), _ser(payload)),
            )
        self._vectors[span_id] = (tenant, vec, payload, text)

    def search(
        self, query: str, k: int, tenant: str, filters: dict[str, Any] | None = None
    ) -> list[tuple[str, float, dict[str, Any]]]:
        qv = local_embedder.embed(query)
        scored: list[tuple[str, float, dict[str, Any]]] = []
        for span_id, (t, vec, payload, _text) in self._vectors.items():
            if t != tenant:  # tenant isolation (Bible §8.1 cross-tenant control)
                continue
            if filters and any(payload.get(fk) != fv for fk, fv in filters.items()):
                continue
            scored.append((span_id, local_embedder.cosine(qv, vec), payload))
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:k]

    # --------------------------------------------------------------------- IRelationalStore
    def put(self, kind: str, key: str, value: dict[str, Any], tenant: str) -> None:
        with _LOCK, self._conn:
            self._conn.execute(
                """INSERT INTO kv VALUES (?,?,?,?)
                   ON CONFLICT(kind, tenant, key) DO UPDATE SET value=excluded.value""",
                (kind, tenant, key, _ser(value)),
            )

    def get(self, kind: str, key: str, tenant: str) -> dict[str, Any] | None:
        r = self._conn.execute(
            "SELECT value FROM kv WHERE kind=? AND tenant=? AND key=?", (kind, tenant, key)
        ).fetchone()
        return json.loads(r["value"]) if r else None

    def list(self, kind: str, tenant: str) -> list[dict[str, Any]]:
        rows = self._conn.execute(
            "SELECT value FROM kv WHERE kind=? AND tenant=?", (kind, tenant)
        ).fetchall()
        return [json.loads(r["value"]) for r in rows]

    def delete(self, kind: str, key: str, tenant: str) -> None:
        with _LOCK, self._conn:
            self._conn.execute(
                "DELETE FROM kv WHERE kind=? AND tenant=? AND key=?", (kind, tenant, key)
            )

    def append_audit(self, entry: AuditEntry) -> None:
        # Append-only: INSERT with no UPDATE/DELETE path anywhere (Bible §8.1).
        with _LOCK, self._conn:
            self._conn.execute(
                "INSERT INTO audit VALUES (?,?,?,?,?,?,?)",
                (
                    entry.entry_id, entry.tenant, entry.actor, entry.action, entry.target,
                    _ser(entry.detail), entry.ts.isoformat(),
                ),
            )

    def query_audit(
        self,
        tenant: str,
        actor: str | None = None,
        action: str | None = None,
        frm: str | None = None,
        to: str | None = None,
        limit: int = 200,
    ) -> list[AuditEntry]:
        q = "SELECT * FROM audit WHERE tenant=?"
        args: list[Any] = [tenant]
        if actor:
            q += " AND actor=?"
            args.append(actor)
        if action:
            q += " AND action LIKE ?"
            args.append(f"{action}%")
        if frm:
            q += " AND ts>=?"
            args.append(frm)
        if to:
            q += " AND ts<=?"
            args.append(to)
        q += " ORDER BY ts DESC LIMIT ?"
        args.append(limit)
        rows = self._conn.execute(q, args).fetchall()
        return [
            AuditEntry(
                entry_id=r["entry_id"], tenant=r["tenant"], actor=r["actor"], action=r["action"],
                target=r["target"], detail=json.loads(r["detail"]),
                ts=datetime.fromisoformat(r["ts"]),
            )
            for r in rows
        ]
