"""Domain models and DTOs.

These Pydantic models are the single in-code representation of graph nodes, provenance, and the
investigation/answer contract. API DTOs (app/api/schemas.py) mirror Bible §7 exactly and are
built from these.
"""
from __future__ import annotations

from datetime import date, datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field

from .graph_types import EdgeType, NodeLabel


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


# --------------------------------------------------------------------------- provenance (CP-1)
class Provenance(BaseModel):
    """Every fact traces to a source span + method + confidence (CP-1). If human-touched, also
    to a named person + timestamp."""

    doc_id: str
    page: int | None = None
    span_id: str
    method: str  # e.g. "parser", "ocr", "llm+rules", "human"
    confidence: float
    extractor_version: str = "v1"
    author: str | None = None  # set when human-touched
    recorded_at: datetime = Field(default_factory=now_utc)


class Span(BaseModel):
    span_id: str
    doc_id: str
    page: int | None = None
    text: str
    char_range: tuple[int, int] | None = None
    tenant: str = "demo"


# ------------------------------------------------------------------------------- graph records
class Node(BaseModel):
    id: str
    label: NodeLabel
    props: dict[str, Any] = Field(default_factory=dict)
    tenant: str = "demo"
    # Bitemporal axes (CP-7)
    effective_from: date | None = None
    effective_to: date | None = None
    recorded_at: datetime = Field(default_factory=now_utc)
    provisional: bool = False  # confidence 0.6–0.85 (Bible §3.1.3)
    superseded_by: str | None = None


class Edge(BaseModel):
    id: str
    type: EdgeType
    src: str
    dst: str
    props: dict[str, Any] = Field(default_factory=dict)
    tenant: str = "demo"
    effective_from: date | None = None
    effective_to: date | None = None
    recorded_at: datetime = Field(default_factory=now_utc)
    confidence: float = 1.0


# ------------------------------------------------------------------------ investigation / answer
class ConfidenceState(str, Enum):
    """The four-state confidence contract (PRB §3.4). Never colour-only in the UI (NFR-10)."""

    GROUNDED = "grounded"      # every claim resolves to >=1 cited span
    INFERRED = "inferred"      # reasoned from grounded facts, not itself directly cited
    UNSUPPORTED = "unsupported"  # stripped/flagged by the Verifier
    ABSTAINED = "abstained"    # declined; below grounding threshold (CP-4)


class Citation(BaseModel):
    doc_id: str
    page: int | None = None
    span_id: str
    excerpt: str | None = None


class Claim(BaseModel):
    text: str
    confidence: ConfidenceState
    citations: list[Citation] = Field(default_factory=list)


class GraphHop(BaseModel):
    """One step of the traversal, streamed to the UI as it is retrieved (Bible §7.4)."""

    node: str | None = None
    node_label: str | None = None
    edge: str | None = None
    detail: str | None = None


class WhoToAsk(BaseModel):
    person: str
    expertise: str
    tenure_years: int | None = None


class Verdict(str, Enum):
    GROUNDED = "grounded"
    ABSTAINED = "abstained"


class InvestigationResult(BaseModel):
    """Mirrors Bible §7.3 InvestigationResult DTO."""

    investigation_id: str
    question: str
    as_of: date | None = None
    abstained: bool = False
    answer: str = ""
    claims: list[Claim] = Field(default_factory=list)
    graph_path: list[GraphHop] = Field(default_factory=list)
    unresolved: list[str] = Field(default_factory=list)
    who_to_ask: list[WhoToAsk] = Field(default_factory=list)
    degradation_level: str = "full"
    # Reproducibility (CP-7 / Bible §8.5)
    prompt_manifest_hash: str | None = None
    model_id: str | None = None
    context_span_ids: list[str] = Field(default_factory=list)
    parent_investigation_id: str | None = None
    created_at: datetime = Field(default_factory=now_utc)


# --------------------------------------------------------------------------- resolution (M2)
class ResolutionProposal(BaseModel):
    proposal_id: str
    canonical_asset_id: str
    canonical_tag: str
    identifier_ids: list[str]
    identifiers: list[dict[str, Any]]  # {id, value, source_system, vocabulary}
    score: float
    method: str
    features: dict[str, float] = Field(default_factory=dict)
    tenant: str = "demo"
    version: int = 0  # optimistic concurrency (Bible §7.6): stale adjudication → 409
    created_at: datetime = Field(default_factory=now_utc)


class Adjudication(BaseModel):
    decision: str  # "merge" | "separate"
    approver: str
    note: str | None = None
    corrected: bool = False
    corrected_target_asset_id: str | None = None
    version: int | None = None  # if provided and stale vs the proposal → 409 (optimistic lock)


# ---------------------------------------------------------------------------- compliance (M6)
class ObligationStatus(str, Enum):
    SATISFIED = "satisfied"
    DUE = "due"
    OVERDUE = "overdue"
    UNKNOWN = "unknown"


class ComplianceRow(BaseModel):
    clause: str
    instrument: str
    authority: str
    asset_id: str
    asset_tag: str
    periodicity_months: int
    last_evidence_date: date | None = None
    last_evidence_doc: str | None = None
    last_evidence_span: str | None = None
    status: ObligationStatus


class CoverageReport(BaseModel):
    encoded_clauses: int
    total_applicable_clauses: int
    by_instrument: dict[str, dict[str, int]]  # instrument -> {encoded, total}
    disclaimer: str = (
        "Encoded clauses: {n} of {m}. This is not a completeness guarantee."
    )


# ------------------------------------------------------------------------------- actions (M7)
class ActionDraft(BaseModel):
    draft_id: str
    asset_id: str
    asset_tag: str
    symptom: str
    hypothesis_id: str | None = None
    investigation_id: str | None = None
    preview: dict[str, Any]
    drafter: str
    status: str = "pending"  # pending | approved | rejected | committed
    cmms_work_order_id: str | None = None
    approver: str | None = None
    rationale: str | None = None
    created_at: datetime = Field(default_factory=now_utc)


# --------------------------------------------------------------------------- corrections (M8)
class Correction(BaseModel):
    correction_id: str
    target_kind: str  # "claim" | "edge" | "resolution" | "fact"
    target_ref: str
    prior_value: str | None = None
    new_value: str
    rationale: str
    author: str
    tenant: str = "demo"
    created_at: datetime = Field(default_factory=now_utc)


# ------------------------------------------------------------------------ organizational memory
class KnowledgeItem(BaseModel):
    """One piece of captured expertise.

    `label` is the short title; `text` is the knowledge itself — the rule, the war story, the
    thing that walks out of the door at retirement. Capturing only the label was the original
    shape, and it lost precisely the part worth keeping.

    When `text` is present it is also written as a provenance-stamped Span, so a captured
    nugget is citable in an answer exactly like a sentence from a document. `span_id` is that
    citation handle.
    """

    target_kind: str
    target_ref: str
    label: str
    text: str = ""
    kind: str = "tip"  # tip | rule | faq | lesson | incident
    tags: list[str] = Field(default_factory=list)
    captured_on: str | None = None
    span_id: str | None = None
    used_in_answers: int = 0


class ExpertiseRecord(BaseModel):
    person_id: str
    name: str
    role: str
    tenure_years: int
    knows: list[KnowledgeItem]
    retirement_risk: bool = False


# --------------------------------------------------------------------------- knowledge risk (M4)
class KnowledgeRiskFlag(BaseModel):
    flag_id: str
    trigger: str  # equipment_change | vendor_change | sop_change | expert_departure | contradiction
    affected_fact_ref: str
    description: str
    raised_at: datetime = Field(default_factory=now_utc)
    resolved: bool = False


# --------------------------------------------------------------------------------- audit (M9)
class AuditEntry(BaseModel):
    entry_id: str
    actor: str
    action: str
    target: str | None = None
    detail: dict[str, Any] = Field(default_factory=dict)
    tenant: str = "demo"
    ts: datetime = Field(default_factory=now_utc)


# --------------------------------------------------------------------------- ingestion (M11)
class IngestionStatus(str, Enum):
    QUEUED = "queued"
    PARSING = "parsing"
    OCR = "ocr"
    GRAPHICS = "graphics"
    EXTRACTING = "extracting"
    RESOLVING = "resolving"
    COMPLETE = "complete"
    QUARANTINED = "quarantined"
    DUPLICATE = "duplicate"


class IngestionJob(BaseModel):
    job_id: str
    doc_id: str
    filename: str
    status: IngestionStatus = IngestionStatus.QUEUED
    stage_log: list[dict[str, Any]] = Field(default_factory=list)
    attempts: int = 0
    quarantine_reason: str | None = None
    node_count: int = 0
    edge_count: int = 0
    span_count: int = 0
    tenant: str = "demo"
    created_at: datetime = Field(default_factory=now_utc)
