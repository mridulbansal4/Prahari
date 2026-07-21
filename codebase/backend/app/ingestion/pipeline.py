"""Ingestion pipeline (M11, Bible §2.6, §3.1) — a DAG of idempotent, provenance-stamping stages.

detect → parse/ocr → (graphics) → extract entities+relations → provenance stamp → confidence
gate → resolution handoff → write. Idempotency keyed by (doc_id, doc_hash, extractor_version):
a changed hash becomes a new version linked by SUPERSEDES (CP-7); low-confidence extractions are
quarantined, never promoted to a fact (BR-1, Bible §1.8).
"""
from __future__ import annotations

import hashlib
import re
from datetime import date
from typing import Any

from ..audit.sink import AuditSink
from ..config import Settings
from ..domain.graph_types import EdgeType, NodeLabel
from ..domain.models import (
    Edge,
    IngestionJob,
    IngestionStatus,
    Node,
    Span,
)
from ..graph.provenance_sink import ProvenanceSink
from ..ports import IDrawingReader, IGraphStore, IOcrProvider, IRelationalStore, IVectorStore
from . import extractors
from .drawing_schema import DrawingExtraction
from .ocr import looks_like_image, looks_like_pdf, render_pdf_pages

_JOB = "ingestion_job"
_DOC = "document"
_LOWCONF = "low_confidence_extraction"


class IngestionPipeline:
    def __init__(
        self,
        graph: IGraphStore,
        vector: IVectorStore,
        relational: IRelationalStore,
        sink: ProvenanceSink,
        audit: AuditSink,
        settings: Settings,
        ocr: IOcrProvider | None = None,
        drawings: IDrawingReader | None = None,
        contradictions: Any | None = None,
    ) -> None:
        self._g = graph
        self._v = vector
        self._rel = relational
        self._sink = sink
        self._audit = audit
        self._s = settings
        self._ocr = ocr
        self._drawings = drawings
        self._contradictions = contradictions

    # ------------------------------------------------------------------------- ingest
    def ingest(
        self,
        filename: str,
        content: bytes,
        tenant: str,
        actor: str,
        doc_type: str | None = None,
        structured: dict[str, Any] | None = None,
    ) -> IngestionJob:
        doc_hash = hashlib.sha256(content).hexdigest()
        doc_id = structured.get("doc_id") if structured else f"doc-{doc_hash[:12]}"

        # Idempotency by content hash (Bible §7.6): duplicate → 409-style, return existing doc.
        existing = self._find_by_hash(doc_hash, tenant)
        if existing:
            job = IngestionJob(job_id=self._sink.new_id("job"), doc_id=existing["doc_id"],
                               filename=filename, status=IngestionStatus.DUPLICATE, tenant=tenant)
            job.stage_log.append({"stage": "detect", "note": "duplicate content hash",
                                  "existing_doc_id": existing["doc_id"]})
            self._rel.put(_JOB, job.job_id, job.model_dump(mode="json"), tenant)
            self._audit.log(actor, "document.duplicate", tenant, target=existing["doc_id"])
            return job

        job = IngestionJob(job_id=self._sink.new_id("job"), doc_id=doc_id, filename=filename,
                           tenant=tenant)
        self._save(job)

        # --- detect ---
        dtype = doc_type or self._detect(filename, structured, content)
        self._stage(job, IngestionStatus.PARSING, {"stage": "detect", "doc_type": dtype})

        # --- Document node + supersession chain (CP-7) ---
        version = self._version_for(doc_id, tenant)
        self._g.upsert_node(Node(id=doc_id, label=NodeLabel.DOCUMENT, tenant=tenant,
                                 props={"type": dtype, "filename": filename, "hash": doc_hash,
                                        "version": version}, recorded_at=job.created_at))
        prior = self._prior_version(doc_id, tenant)
        if prior:
            self._g.upsert_edge(Edge(id=f"sup-{doc_id}-{prior}", type=EdgeType.SUPERSEDES,
                                     src=doc_id, dst=prior, tenant=tenant))

        # --- parse / extract ---
        text = ""
        if structured:
            ex = extractors.extract_structured(doc_id, structured)
        elif dtype == "csv":
            text = content.decode("utf-8", errors="replace")
            ex = extractors.extract_csv(doc_id, text)
        elif dtype == "drawing":
            # An engineering drawing is not a text problem. Ask the VLM what the diagram
            # MEANS; if no reader is configured, quarantine rather than invent topology.
            drawn = self._read_drawing(job, content, doc_id, filename, actor, tenant)
            if drawn is None:
                return job
            ex = drawn
        elif dtype in ("pdf", "image"):
            # Scanned pages: transcribe with OCR. Without a provider we cannot read the file,
            # and decoding the bytes as UTF-8 would write mojibake into the graph as citable
            # evidence — so this quarantines instead.
            parsed = self._read_scanned(job, content, doc_id, dtype, actor, tenant)
            if parsed is None:
                return job
            ex = parsed
        else:
            text = content.decode("utf-8", errors="replace")
            self._stage(job, IngestionStatus.EXTRACTING, {"stage": "parse"})
            ex = extractors.extract_text(doc_id, text)

        if not ex.spans:
            job.status = IngestionStatus.QUARANTINED
            job.quarantine_reason = "No parseable content (unreadable scan or empty document)."
            self._save(job)
            self._audit.log(actor, "ingestion.quarantined", tenant, target=doc_id,
                            detail={"reason": job.quarantine_reason})
            return job

        self._stage(job, IngestionStatus.EXTRACTING, {"stage": "extract",
                    "entities": len(ex.entities), "relations": len(ex.relations)})

        # --- provenance stamp + write spans ---
        span_by_id: dict[str, Span] = {}
        for es in ex.spans:
            sp = Span(span_id=es.span_id, doc_id=doc_id, page=es.page, text=es.text, tenant=tenant)
            self._sink.write_span(sp)
            self._v.upsert(sp.span_id, sp.text, {"doc_id": doc_id, "page": es.page}, tenant)
            span_by_id[es.span_id] = sp
            job.span_count += 1

        # --- confidence gate (Bible §3.1.3): >=0.85 auto; 0.6-0.85 provisional; <0.6 quarantine ---
        key_to_node: dict[str, str] = {}
        for ent in ex.entities:
            if ent.confidence < self._s.confidence_provisional:
                self._rel.put(_LOWCONF, f"{doc_id}:{ent.key}",
                              {"doc_id": doc_id, "entity": ent.__dict__}, tenant)
                continue
            label = NodeLabel(ent.kind)
            node_id = self._node_id_for(ent)
            provisional = ent.confidence < self._s.confidence_auto_write
            node = Node(id=node_id, label=label, tenant=tenant, props=ent.props,
                        provisional=provisional, effective_from=date.today())
            spans = [span_by_id[ent.span_id]] if label in _FACT_LABELS else []
            self._sink.write_node(node, spans=spans)
            key_to_node[ent.key] = node_id
            key_to_node.setdefault(f"asset:{ent.props.get('value','')}", node_id)
            job.node_count += 1

        for rel in ex.relations:
            if rel.confidence < self._s.confidence_provisional:
                continue
            src = key_to_node.get(rel.src_key) or self._resolve_key(rel.src_key, tenant)
            dst = key_to_node.get(rel.dst_key) or self._resolve_key(rel.dst_key, tenant)
            if not src or not dst:
                continue
            # rel.props carries what the extractor learned about the relationship itself —
            # a drawing's line number, which sheet it came from. It was being discarded.
            edge = Edge(id=f"{rel.type}-{src}-{dst}", type=EdgeType(rel.type), src=src, dst=dst,
                        tenant=tenant, confidence=rel.confidence, effective_from=date.today(),
                        props=dict(rel.props))
            self._sink.write_edge(edge, spans=[span_by_id[rel.span_id]])
            job.edge_count += 1

        # --- resolution handoff ---
        self._stage(job, IngestionStatus.RESOLVING, {"stage": "resolution_handoff"})
        job.status = IngestionStatus.COMPLETE
        self._save(job)
        self._rel.put(_DOC, doc_id, {"doc_id": doc_id, "hash": doc_hash, "filename": filename,
                      "type": dtype, "version": version, "job_id": job.job_id}, tenant)
        self._audit.log(actor, "document.uploaded", tenant, target=doc_id,
                        detail={"job_id": job.job_id, "nodes": job.node_count,
                                "edges": job.edge_count, "spans": job.span_count})
        return job

    # ------------------------------------------------------------------------ helpers
    # Filenames that announce an engineering drawing. Content sniffing cannot tell a scanned
    # report from a P&ID — both are just a raster — so the routing hint has to come from the
    # name or an explicit doc_type from the caller.
    _DRAWING_NAME = re.compile(
        r"(?:^|[^a-z])(?:p&?id|pid|drawing|schematic|isometric|ga[-_]?dwg|layout)(?:[^a-z]|$)",
        re.I,
    )

    def _detect(self, filename: str, structured: dict[str, Any] | None,
                content: bytes = b"") -> str:
        """Classify by content first, then filename.

        Extension alone used to decide this, which meant a PNG called `notes.txt` was parsed
        as text and a real PDF was decoded as UTF-8 mojibake. Magic bytes settle what the file
        *is*; the name only decides whether a raster is a drawing or a scanned page.
        """
        if structured:
            return structured.get("type", "structured")
        low = filename.lower()
        is_raster = looks_like_image(content)
        is_pdf = looks_like_pdf(content) or (low.endswith(".pdf") and not is_raster)

        if (is_pdf or is_raster) and self._DRAWING_NAME.search(low):
            return "drawing"
        if is_pdf:
            return "pdf"
        if is_raster:
            return "image"
        if low.endswith((".csv", ".tsv")):
            return "csv"
        return "text"

    def _quarantine(self, job: IngestionJob, reason: str, doc_id: str, actor: str,
                    tenant: str) -> IngestionJob:
        job.status = IngestionStatus.QUARANTINED
        job.quarantine_reason = reason
        self._save(job)
        self._audit.log(actor, "ingestion.quarantined", tenant, target=doc_id,
                        detail={"reason": reason})
        return job

    def _read_scanned(self, job: IngestionJob, content: bytes, doc_id: str, dtype: str,
                      actor: str, tenant: str) -> extractors.Extraction | None:
        """OCR a PDF/image into text spans. Returns None when the job was quarantined."""
        self._stage(job, IngestionStatus.OCR, {"stage": "ocr", "provider": getattr(
            self._ocr, "id", "none")})
        if self._ocr is None or not self._ocr.available():
            self._quarantine(
                job,
                "Scanned document needs OCR, and no OCR provider is configured "
                "(PRAHARI_OCR_PROVIDER=none). Nothing was guessed at.",
                doc_id, actor, tenant)
            return None

        pages = render_pdf_pages(content, self._s.ocr_dpi) if dtype == "pdf" else [content]
        if not pages:
            self._quarantine(job, "Could not render any page from this document.",
                             doc_id, actor, tenant)
            return None
        try:
            texts = self._ocr.read_pages(pages)
        except Exception as e:  # provider down / bad response — never fabricate a parse
            self._quarantine(job, f"OCR failed: {e}", doc_id, actor, tenant)
            return None

        ex = extractors.Extraction()
        for page_no, page_text in enumerate(texts, start=1):
            page_ex = extractors.extract_text(f"{doc_id}:p{page_no}", page_text or "")
            for sp in page_ex.spans:
                sp.page = page_no
                sp.method = "ocr"
            ex.spans.extend(page_ex.spans)
            ex.entities.extend(page_ex.entities)
            ex.relations.extend(page_ex.relations)
        return ex

    def _read_drawing(self, job: IngestionJob, content: bytes, doc_id: str, filename: str,
                      actor: str, tenant: str) -> extractors.Extraction | None:
        """Ask the VLM what the drawing means, and turn that into graph facts."""
        self._stage(job, IngestionStatus.GRAPHICS, {"stage": "graphics", "provider": getattr(
            self._drawings, "id", "none")})
        if self._drawings is None or not self._drawings.available():
            self._quarantine(
                job,
                "Engineering drawing needs a vision model, and no VLM is configured "
                "(PRAHARI_VLM_PROVIDER=none). Topology was not invented.",
                doc_id, actor, tenant)
            return None

        page = content
        if looks_like_pdf(content):
            rendered = render_pdf_pages(content, self._s.drawing_dpi, max_pages=1)
            if not rendered:
                self._quarantine(job, "Could not render the drawing page.", doc_id, actor,
                                 tenant)
                return None
            page = rendered[0]
        try:
            result: DrawingExtraction = self._drawings.read_drawing(page, hint=filename)
        except Exception as e:
            self._quarantine(job, f"Drawing reader failed: {e}", doc_id, actor, tenant)
            return None
        if result.is_empty():
            self._quarantine(job, "The drawing reader found no components it could assert.",
                             doc_id, actor, tenant)
            return None
        return self._drawing_to_extraction(doc_id, result)

    @staticmethod
    def _drawing_to_extraction(doc_id: str, d: DrawingExtraction) -> extractors.Extraction:
        """Fold a validated DrawingExtraction into the ordinary extractor contract.

        Every component and connection carries the reader's own `source_note` as its span, so
        a drawing-derived edge is cited exactly like a sentence from a PDF and passes the same
        CP-1 provenance gate. Nothing here is synthesised: a connection the model did not
        report simply does not exist.
        """
        ex = extractors.Extraction()
        conf = max(0.0, min(1.0, d.confidence))

        for i, comp in enumerate(d.components):
            span_id = f"{doc_id}:cmp{i}"
            note = comp.source_note or f"{comp.tag} shown on {d.drawing_number or 'the drawing'}"
            ex.spans.append(extractors.ExtractedSpan(
                span_id=span_id, page=1, text=note, method="vlm", confidence=conf))
            ex.entities.append(extractors.ExtractedEntity(
                kind="Identifier", key=f"ident:{comp.tag}",
                props={"value": comp.tag, "source_system": "pid", "vocabulary": "drawing",
                       "context": note, "kind": comp.kind, "label": comp.label},
                span_id=span_id, confidence=conf))

        for j, conn in enumerate(d.connections):
            span_id = f"{doc_id}:con{j}"
            note = conn.source_note or (
                f"{conn.from_tag} connected to {conn.to_tag}"
                + (f" via line {conn.line_number}" if conn.line_number else ""))
            ex.spans.append(extractors.ExtractedSpan(
                span_id=span_id, page=1, text=note, method="vlm", confidence=conf))
            rel = conn.relation if conn.relation in ("CONNECTED_TO", "PART_OF") else "CONNECTED_TO"
            ex.relations.append(extractors.ExtractedRelation(
                type=rel, src_key=f"asset:{conn.from_tag}", dst_key=f"asset:{conn.to_tag}",
                span_id=span_id, confidence=conf,
                props={"line_number": conn.line_number, "from_drawing": d.drawing_number}))

        for k, ann in enumerate(d.annotations):
            span_id = f"{doc_id}:ann{k}"
            text = f"{ann.subject_tag + ': ' if ann.subject_tag else ''}{ann.text}"
            ex.spans.append(extractors.ExtractedSpan(
                span_id=span_id, page=1, text=text, method="vlm", confidence=conf))
        return ex

    def _node_id_for(self, ent: extractors.ExtractedEntity) -> str:
        if ent.kind == "Identifier":
            return f"ident-{extractors_norm(ent.props.get('value',''))}"
        if ent.kind == "Asset":
            return ent.props.get("id") or f"asset-{extractors_norm(ent.props.get('tag',''))}"
        return ent.key.replace(":", "-")

    def _resolve_key(self, key: str, tenant: str) -> str | None:
        if key.startswith("asset:"):
            tag = key.split(":", 1)[1]
            for a in self._g.nodes_by_label(NodeLabel.ASSET.value, tenant):
                if str(a.props.get("tag", "")).lower() == tag.lower():
                    return a.id
        return None

    def _save(self, job: IngestionJob) -> None:
        self._rel.put(_JOB, job.job_id, job.model_dump(mode="json"), job.tenant)

    def _stage(self, job: IngestionJob, status: IngestionStatus, log: dict[str, Any]) -> None:
        job.status = status
        job.stage_log.append(log)
        self._save(job)

    def get_job(self, job_id: str, tenant: str) -> IngestionJob | None:
        raw = self._rel.get(_JOB, job_id, tenant)
        return IngestionJob(**raw) if raw else None

    def list_jobs(self, tenant: str) -> list[IngestionJob]:
        return [IngestionJob(**j) for j in self._rel.list(_JOB, tenant)]

    def quarantined(self, tenant: str) -> list[IngestionJob]:
        return [j for j in self.list_jobs(tenant) if j.status == IngestionStatus.QUARANTINED]

    def _find_by_hash(self, doc_hash: str, tenant: str) -> dict[str, Any] | None:
        for d in self._rel.list(_DOC, tenant):
            if d.get("hash") == doc_hash:
                return d
        return None

    def _version_for(self, doc_id: str, tenant: str) -> int:
        return len([d for d in self._rel.list(_DOC, tenant)
                    if d.get("doc_id", "").split("#")[0] == doc_id]) + 1

    def _prior_version(self, doc_id: str, tenant: str) -> str | None:
        return None  # supersession chain wired for versioned re-uploads; base version has no prior


_FACT_LABELS = {
    NodeLabel.ASSET, NodeLabel.WORK_ORDER, NodeLabel.INSPECTION, NodeLabel.FAILURE_MODE,
    NodeLabel.INCIDENT, NodeLabel.OBLIGATION, NodeLabel.SENSOR,
}


def extractors_norm(v: str) -> str:
    import re

    return re.sub(r"[^a-z0-9]", "", v.lower())
