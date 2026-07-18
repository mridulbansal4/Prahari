"""Extractors (IExtractor adapters, Bible §3.1).

Each returns typed entities + relations with per-item confidence and the span each was drawn
from (provenance, CP-1). Confidence gating happens in the pipeline, never here.

For the provenance-clean demo corpus (ADR-012), documents may arrive as structured JSON whose
facts are already annotated with their source span and confidence — deterministic and audit-
clean. Free-text/CSV documents run the lightweight rule+pattern extractor. The P&ID graphics
extractor (YOLO/Relationformer) is a DEXPI-shaped stub behind the `pid_graphics` flag (ADR-P03):
it reads structured topology already present in the corpus and never fabricates a detection.
"""
from __future__ import annotations

import csv
import io
import re
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ExtractedSpan:
    span_id: str
    page: int | None
    text: str
    method: str
    confidence: float


@dataclass
class ExtractedEntity:
    kind: str  # NodeLabel value
    key: str
    props: dict[str, Any]
    span_id: str
    confidence: float


@dataclass
class ExtractedRelation:
    type: str  # EdgeType value
    src_key: str
    dst_key: str
    span_id: str
    confidence: float
    props: dict[str, Any] = field(default_factory=dict)


@dataclass
class Extraction:
    spans: list[ExtractedSpan] = field(default_factory=list)
    entities: list[ExtractedEntity] = field(default_factory=list)
    relations: list[ExtractedRelation] = field(default_factory=list)


_SENT = re.compile(r"(?<=[.!?])\s+")
_TAG = re.compile(r"\b([A-Z]{1,4}-?\d{2,4}[A-Z]?)\b")


def extract_structured(doc_id: str, payload: dict[str, Any]) -> Extraction:
    """Corpus documents with pre-annotated facts (provenance-clean, ADR-012)."""
    ex = Extraction()
    for s in payload.get("spans", []):
        ex.spans.append(
            ExtractedSpan(span_id=s["span_id"], page=s.get("page"), text=s["text"],
                          method=s.get("method", "parser"), confidence=s.get("confidence", 0.99))
        )
    for e in payload.get("entities", []):
        ex.entities.append(
            ExtractedEntity(kind=e["kind"], key=e["key"], props=e.get("props", {}),
                            span_id=e["span_id"], confidence=e.get("confidence", 0.95))
        )
    for r in payload.get("relations", []):
        ex.relations.append(
            ExtractedRelation(type=r["type"], src_key=r["src_key"], dst_key=r["dst_key"],
                              span_id=r["span_id"], confidence=r.get("confidence", 0.95),
                              props=r.get("props", {}))
        )
    return ex


def extract_text(doc_id: str, text: str) -> Extraction:
    """Lightweight rule+pattern extractor for free text (Bible §3.1 entity/relation extract)."""
    ex = Extraction()
    for i, sent in enumerate(_SENT.split(text.strip())):
        if not sent.strip():
            continue
        span_id = f"{doc_id}:s{i}"
        ex.spans.append(ExtractedSpan(span_id=span_id, page=1, text=sent.strip(),
                                      method="parser", confidence=0.9))
        for tag in set(_TAG.findall(sent)):
            ex.entities.append(
                ExtractedEntity(kind="Identifier", key=f"ident:{tag}",
                                props={"value": tag, "source_system": "dms", "vocabulary": "operator",
                                       "context": sent.strip()},
                                span_id=span_id, confidence=0.75)
            )
    return ex


def extract_csv(doc_id: str, text: str) -> Extraction:
    """CMMS-export style CSV → WorkOrder / Inspection rows (Bible FR-1)."""
    ex = Extraction()
    reader = csv.DictReader(io.StringIO(text))
    for i, row in enumerate(reader):
        span_id = f"{doc_id}:row{i}"
        ex.spans.append(ExtractedSpan(span_id=span_id, page=1,
                                      text=", ".join(f"{k}={v}" for k, v in row.items()),
                                      method="parser", confidence=0.97))
        tag = row.get("asset_tag") or row.get("tag")
        if tag:
            ex.entities.append(ExtractedEntity(kind="Identifier", key=f"ident:{tag}",
                               props={"value": tag, "source_system": "cmms", "vocabulary": "cmms",
                                      "context": span_id}, span_id=span_id, confidence=0.9))
        if row.get("wo_id"):
            ex.entities.append(ExtractedEntity(kind="WorkOrder", key=f"wo:{row['wo_id']}",
                               props={"wo_id": row["wo_id"], "status": row.get("status"),
                                      "opened": row.get("opened")}, span_id=span_id, confidence=0.9))
            if tag:
                ex.relations.append(ExtractedRelation(type="HAS_WORKORDER", src_key=f"asset:{tag}",
                                    dst_key=f"wo:{row['wo_id']}", span_id=span_id, confidence=0.9))
    return ex
