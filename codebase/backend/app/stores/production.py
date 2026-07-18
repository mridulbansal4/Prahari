"""Production store family (ADR-P01) — Neo4j / Qdrant / Postgres.

These implement the identical port contract as the embedded family (Bible §2.4 extraction
seam). They are imported lazily only when ``SENTINEL_PROFILE=production`` so the embedded profile
never needs the drivers installed. Exercised under docker-compose; see KB-2.
"""
from __future__ import annotations

import json
from datetime import date, datetime
from typing import Any

from ..config import Settings
from ..domain.graph_types import EdgeType
from ..domain.models import AuditEntry, Edge, Node, Span


def _as_date(v: Any) -> date | None:
    if not v:
        return None
    return date.fromisoformat(str(v)[:10])


class Neo4jGraphStore:
    def __init__(self, settings: Settings) -> None:
        from neo4j import GraphDatabase

        self._driver = GraphDatabase.driver(
            settings.graph_uri, auth=(settings.graph_user, settings.graph_password)
        )
        self._ensure_constraints()

    def _ensure_constraints(self) -> None:
        stmts = [
            "CREATE CONSTRAINT node_id IF NOT EXISTS FOR (n:Node) REQUIRE n.id IS UNIQUE",
            "CREATE INDEX ident_value IF NOT EXISTS FOR (n:Identifier) ON (n.value)",
            "CREATE INDEX asset_id IF NOT EXISTS FOR (n:Asset) ON (n.id)",
        ]
        with self._driver.session() as s:
            for st in stmts:
                try:
                    s.run(st)
                except Exception:  # pragma: no cover - idempotent best-effort
                    pass

    def upsert_node(self, node: Node) -> None:
        with self._driver.session() as s:
            s.run(
                f"MERGE (n:Node:{node.label.value} {{id:$id}}) SET n += $p, n.tenant=$t, "
                "n.effective_from=$ef, n.effective_to=$et, n.recorded_at=$ra, "
                "n.provisional=$pr, n.superseded_by=$sb",
                id=node.id, p=node.props, t=node.tenant,
                ef=node.effective_from.isoformat() if node.effective_from else None,
                et=node.effective_to.isoformat() if node.effective_to else None,
                ra=node.recorded_at.isoformat(), pr=node.provisional, sb=node.superseded_by,
            )

    def upsert_edge(self, edge: Edge) -> None:
        with self._driver.session() as s:
            s.run(
                f"MATCH (a:Node {{id:$src}}),(b:Node {{id:$dst}}) "
                f"MERGE (a)-[r:{edge.type.value} {{id:$id}}]->(b) SET r += $p, r.tenant=$t, "
                "r.effective_from=$ef, r.effective_to=$et, r.recorded_at=$ra, r.confidence=$c",
                src=edge.src, dst=edge.dst, id=edge.id, p=edge.props, t=edge.tenant,
                ef=edge.effective_from.isoformat() if edge.effective_from else None,
                et=edge.effective_to.isoformat() if edge.effective_to else None,
                ra=edge.recorded_at.isoformat(), c=edge.confidence,
            )

    def _node_from(self, rec: dict[str, Any]) -> Node:
        labels = [l for l in rec.get("labels", []) if l != "Node"]
        props = {k: v for k, v in rec.items() if k not in ("labels",)}
        return Node(
            id=props.pop("id"), label=labels[0] if labels else "Asset",
            tenant=props.pop("tenant", "demo"),
            effective_from=_as_date(props.pop("effective_from", None)),
            effective_to=_as_date(props.pop("effective_to", None)),
            recorded_at=datetime.fromisoformat(props.pop("recorded_at", datetime.utcnow().isoformat())),
            provisional=bool(props.pop("provisional", False)),
            superseded_by=props.pop("superseded_by", None), props=props,
        )

    def get_node(self, node_id: str) -> Node | None:
        with self._driver.session() as s:
            r = s.run(
                "MATCH (n:Node {id:$id}) RETURN n, labels(n) as labels", id=node_id
            ).single()
            if not r:
                return None
            d = dict(r["n"]); d["labels"] = r["labels"]
            return self._node_from(d)

    def upsert_span(self, span: Span) -> None:
        with self._driver.session() as s:
            s.run(
                "MERGE (sp:Node:Span {id:$id}) SET sp.span_id=$id, sp.doc_id=$d, sp.page=$pg, "
                "sp.text=$tx, sp.tenant=$t",
                id=span.span_id, d=span.doc_id, pg=span.page, tx=span.text, t=span.tenant,
            )

    def get_span(self, span_id: str) -> Span | None:
        with self._driver.session() as s:
            r = s.run("MATCH (sp:Span {id:$id}) RETURN sp", id=span_id).single()
            if not r:
                return None
            d = dict(r["sp"])
            return Span(span_id=span_id, doc_id=d.get("doc_id", ""), page=d.get("page"),
                       text=d.get("text", ""), tenant=d.get("tenant", "demo"))

    def nodes_by_label(self, label: str, tenant: str) -> list[Node]:
        with self._driver.session() as s:
            rows = s.run(
                f"MATCH (n:{label} {{tenant:$t}}) RETURN n, labels(n) as labels", t=tenant
            )
            out = []
            for r in rows:
                d = dict(r["n"]); d["labels"] = r["labels"]
                out.append(self._node_from(d))
            return out

    def find_identifier(self, value: str, tenant: str) -> Node | None:
        with self._driver.session() as s:
            r = s.run(
                "MATCH (n:Identifier {tenant:$t}) WHERE toLower(n.value)=toLower($v) "
                "RETURN n, labels(n) as labels", t=tenant, v=value,
            ).single()
            if not r:
                return None
            d = dict(r["n"]); d["labels"] = r["labels"]
            return self._node_from(d)

    def _edge_from(self, r: dict[str, Any], typ: str, src: str, dst: str) -> Edge:
        return Edge(
            id=r.get("id", f"{src}-{typ}-{dst}"), type=EdgeType(typ), src=src, dst=dst,
            props={k: v for k, v in r.items() if k not in ("id", "tenant", "effective_from",
                   "effective_to", "recorded_at", "confidence")},
            tenant=r.get("tenant", "demo"), effective_from=_as_date(r.get("effective_from")),
            effective_to=_as_date(r.get("effective_to")),
            recorded_at=datetime.fromisoformat(r.get("recorded_at", datetime.utcnow().isoformat())),
            confidence=r.get("confidence", 1.0),
        )

    def neighbours(self, node_id, edge_types, tenant, as_of=None):
        with self._driver.session() as s:
            rows = s.run(
                "MATCH (a:Node {id:$id})-[r]-(b:Node) RETURN r, type(r) as t, "
                "startNode(r).id as src, endNode(r).id as dst, b, labels(b) as labels",
                id=node_id,
            )
            out = []
            for row in rows:
                typ = row["t"]
                if edge_types and typ not in edge_types:
                    continue
                e = self._edge_from(dict(row["r"]), typ, row["src"], row["dst"])
                if as_of is None and e.effective_to is not None:
                    continue
                d = dict(row["b"]); d["labels"] = row["labels"]
                out.append((e, self._node_from(d)))
            return out

    def traverse(self, anchor_ids, edge_types, max_hops, tenant, as_of=None):
        seen_n: dict[str, Node] = {}
        seen_e: dict[str, Edge] = {}
        frontier = list(anchor_ids)
        for nid in anchor_ids:
            n = self.get_node(nid)
            if n:
                seen_n[nid] = n
        for _ in range(max_hops):
            nxt = []
            for nid in frontier:
                for e, other in self.neighbours(nid, edge_types, tenant, as_of):
                    seen_e[e.id] = e
                    if other.id not in seen_n:
                        seen_n[other.id] = other
                        nxt.append(other.id)
            frontier = nxt
            if not frontier:
                break
        return list(seen_n.values()), list(seen_e.values())

    def evidence_spans(self, node_id, tenant):
        out = []
        for e, other in self.neighbours(node_id, [EdgeType.EVIDENCED_BY.value], tenant, as_of="9999-01-01"):
            sp = self.get_span(other.id)
            if sp:
                out.append(sp)
        return out

    def edges_from(self, node_id, edge_type, tenant):
        with self._driver.session() as s:
            rows = s.run(
                f"MATCH (a:Node {{id:$id}})-[r:{edge_type}]->(b) RETURN r, endNode(r).id as dst",
                id=node_id,
            )
            return [self._edge_from(dict(row["r"]), edge_type, node_id, row["dst"]) for row in rows]

    def all_edges(self, tenant):
        with self._driver.session() as s:
            rows = s.run(
                "MATCH (a:Node {tenant:$t})-[r]->(b:Node) RETURN r, type(r) as t2, "
                "startNode(r).id as src, endNode(r).id as dst", t=tenant,
            )
            return [self._edge_from(dict(r["r"]), r["t2"], r["src"], r["dst"]) for r in rows]

    def delete_edge(self, edge_id):
        with self._driver.session() as s:
            s.run("MATCH ()-[r {id:$id}]-() DELETE r", id=edge_id)

    def snapshot(self):
        with self._driver.session() as s:
            n = s.run("MATCH (n) RETURN count(n) c").single()["c"]
            e = s.run("MATCH ()-[r]->() RETURN count(r) c").single()["c"]
        return {"nodes": n, "edges": e}


class QdrantVectorStore:
    COLLECTION = "sentinel_spans"

    def __init__(self, settings: Settings) -> None:
        from qdrant_client import QdrantClient
        from qdrant_client.models import Distance, VectorParams

        from ..embeddings.local_embedder import DIM

        self._client = QdrantClient(url=settings.vector_url)
        try:
            self._client.get_collection(self.COLLECTION)
        except Exception:
            self._client.create_collection(
                self.COLLECTION, vectors_config=VectorParams(size=DIM, distance=Distance.COSINE)
            )

    def upsert(self, span_id, text, payload, tenant):
        from qdrant_client.models import PointStruct

        from ..embeddings.local_embedder import embed

        pid = abs(hash(span_id)) % (2**63)
        self._client.upsert(
            self.COLLECTION,
            [PointStruct(id=pid, vector=embed(text),
                         payload={**payload, "span_id": span_id, "tenant": tenant, "text": text})],
        )

    def search(self, query, k, tenant, filters=None):
        from qdrant_client.models import FieldCondition, Filter, MatchValue

        from ..embeddings.local_embedder import embed

        must = [FieldCondition(key="tenant", match=MatchValue(value=tenant))]
        for fk, fv in (filters or {}).items():
            must.append(FieldCondition(key=fk, match=MatchValue(value=fv)))
        res = self._client.search(
            self.COLLECTION, query_vector=embed(query), limit=k, query_filter=Filter(must=must)
        )
        return [(r.payload["span_id"], r.score, r.payload) for r in res]


class PostgresRelationalStore:
    def __init__(self, settings: Settings) -> None:
        import psycopg

        self._conn = psycopg.connect(settings.pg_dsn, autocommit=True)
        with self._conn.cursor() as c:
            c.execute(
                "CREATE TABLE IF NOT EXISTS kv (kind text, tenant text, key text, value jsonb, "
                "PRIMARY KEY (kind, tenant, key))"
            )
            c.execute(
                "CREATE TABLE IF NOT EXISTS audit (entry_id text primary key, tenant text, "
                "actor text, action text, target text, detail jsonb, ts timestamptz)"
            )

    def put(self, kind, key, value, tenant):
        with self._conn.cursor() as c:
            c.execute(
                "INSERT INTO kv VALUES (%s,%s,%s,%s) ON CONFLICT (kind,tenant,key) "
                "DO UPDATE SET value=EXCLUDED.value",
                (kind, tenant, key, json.dumps(value, default=str)),
            )

    def get(self, kind, key, tenant):
        with self._conn.cursor() as c:
            c.execute("SELECT value FROM kv WHERE kind=%s AND key=%s AND tenant=%s",
                      (kind, key, tenant))
            r = c.fetchone()
            return r[0] if r else None

    def list(self, kind, tenant):
        with self._conn.cursor() as c:
            c.execute("SELECT value FROM kv WHERE kind=%s AND tenant=%s", (kind, tenant))
            return [r[0] for r in c.fetchall()]

    def delete(self, kind, key, tenant):
        with self._conn.cursor() as c:
            c.execute("DELETE FROM kv WHERE kind=%s AND key=%s AND tenant=%s", (kind, key, tenant))

    def append_audit(self, entry: AuditEntry):
        with self._conn.cursor() as c:
            c.execute(
                "INSERT INTO audit VALUES (%s,%s,%s,%s,%s,%s,%s)",
                (entry.entry_id, entry.tenant, entry.actor, entry.action, entry.target,
                 json.dumps(entry.detail, default=str), entry.ts),
            )

    def query_audit(self, tenant, actor=None, action=None, frm=None, to=None, limit=200):
        q = "SELECT entry_id,tenant,actor,action,target,detail,ts FROM audit WHERE tenant=%s"
        args: list[Any] = [tenant]
        if actor:
            q += " AND actor=%s"; args.append(actor)
        if action:
            q += " AND action LIKE %s"; args.append(f"{action}%")
        q += " ORDER BY ts DESC LIMIT %s"; args.append(limit)
        with self._conn.cursor() as c:
            c.execute(q, args)
            return [
                AuditEntry(entry_id=r[0], tenant=r[1], actor=r[2], action=r[3], target=r[4],
                           detail=r[5], ts=r[6]) for r in c.fetchall()
            ]
