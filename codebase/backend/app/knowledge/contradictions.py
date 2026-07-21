"""Cross-document contradiction detection — the writer for ``EdgeType.CONTRADICTS``.

Until now `CONTRADICTS` was declared in the ontology and read by ``decay.py`` trigger 2, but
nothing ever wrote one, so that trigger could never fire. This module closes the loop.

The detector is **deterministic and rule-based**, not model-based, for three reasons: it must
work at the default ``ocr_provider=none`` / ``vlm_provider=none`` posture with no key and no
GPU; a contradiction is a claim about the plant that has to be defensible; and an LLM asked
"do these disagree?" produces answers that cannot be re-derived at audit time.

It finds *quantitative disagreement*: two documents that state a different number for the same
measured property of the same asset. That is the failure mode the corpus actually contains —
a datasheet saying the bearing alarm is 90 °C while the operating manual says 85 °C, and a
datasheet saying seal bolts take 45 N·m while the maintenance SOP says 55 N·m.

Attribution of a value to an asset uses, in order:
  1. an asset tag printed in the same span; else
  2. the dominant asset tag of the document the span belongs to.
Rule 2 is recorded on the edge (``subject_source="document"``) so a reader can see the
attribution was inferred rather than read off the sentence.
"""
from __future__ import annotations

import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Iterable

from ..audit.sink import AuditSink
from ..domain.graph_types import EdgeType
from ..domain.models import Edge, Span
from ..graph.provenance_sink import ProvenanceSink
from ..ports import IGraphStore

_TAG = re.compile(r"\b([A-Z]{1,4}-\d{2,4}[A-Z]?)\b")


@dataclass(frozen=True)
class Measure:
    """A property whose value two documents can disagree about.

    Precision matters far more than recall here: a false contradiction is a false accusation
    against the plant's own paperwork. So a value only counts when it sits **next to** the word
    that names the property — a bare number elsewhere in the same paragraph is not an
    assertion about this measure. `value` therefore carries the keyword inside the pattern,
    rather than testing keywords and numbers independently.
    """

    kind: str
    label: str
    unit: str
    value: re.Pattern[str]
    # Context words that must appear somewhere in the span for the match to be considered at
    # all. This is a cheap pre-filter; `value` does the real work.
    context: frozenset[str]
    tolerance: float = 0.01  # relative difference below this is the same value


# Proximity templates. `\D{0,N}` keeps the keyword and the number in the same clause — long
# enough to cross a table cell separator, short enough not to reach the next sentence.
_TEMP = r"(\d{2,3}(?:\.\d+)?)\s*(?:°\s*)?C\b"
_TORQUE = r"(\d{2,3}(?:\.\d+)?)\s*N\s*[·\-.]?\s*m\b"
_FLOW = r"(\d{2,4}(?:\.\d+)?)\s*m\s*(?:³|3)\s*/\s*h"
_PRESS = r"(\d+(?:\.\d+)?)\s*bar\b"

MEASURES: tuple[Measure, ...] = (
    Measure(
        kind="bearing_temp_alarm",
        label="bearing temperature alarm setpoint",
        unit="°C",
        value=re.compile(rf"alarm\D{{0,30}}{_TEMP}|{_TEMP}\D{{0,20}}alarm", re.I),
        context=frozenset({"bearing"}),
    ),
    Measure(
        kind="bearing_temp_trip",
        label="bearing temperature trip setpoint",
        unit="°C",
        value=re.compile(rf"trip\D{{0,30}}{_TEMP}|{_TEMP}\D{{0,20}}trip", re.I),
        context=frozenset({"bearing"}),
    ),
    Measure(
        kind="seal_bolt_torque",
        label="mechanical seal bolt torque",
        unit="N·m",
        value=re.compile(
            rf"(?:torque|tighten\w*)\D{{0,40}}{_TORQUE}|{_TORQUE}\D{{0,30}}(?:torque|tighten\w*)",
            re.I,
        ),
        context=frozenset({"seal", "gland"}),
    ),
    Measure(
        kind="min_continuous_flow",
        label="minimum continuous flow",
        unit="m³/h",
        # Deliberately strict: the full phrase only. "flow fell to 61 m³/h" is an observation,
        # not a statement of the design minimum, and must not be compared against it.
        value=re.compile(rf"minimum\s+continuous(?:\s+stable)?\s+flow\D{{0,30}}{_FLOW}", re.I),
        context=frozenset({"minimum"}),
    ),
    Measure(
        kind="strainer_dp_alarm",
        label="strainer differential pressure alarm",
        unit="bar",
        value=re.compile(rf"alarm\D{{0,25}}{_PRESS}|{_PRESS}\D{{0,20}}alarm", re.I),
        context=frozenset({"strainer", "differential"}),
    ),
)


@dataclass
class Assertion:
    subject: str
    subject_source: str  # "span" | "document"
    measure: Measure
    value: float
    span_id: str
    doc_id: str
    quote: str


def _first_number(m: re.Match[str]) -> float | None:
    for g in m.groups():
        if g:
            try:
                return float(g)
            except ValueError:
                return None
    return None


def _asset_tags(text: str, known: frozenset[str]) -> list[str]:
    """Tags in `text` that are real registered equipment.

    Membership of the asset register is the only test. A pattern-based guess reads material
    grades (C-276), standard numbers (OISD-STD-129) and tool ids as equipment, and once a
    value is attributed to a phantom asset it can never contradict the real one.
    """
    return [t for t in _TAG.findall(text) if t in known]


class ContradictionDetector:
    """Scans spans for quantitative disagreement and writes ``CONTRADICTS`` edges."""

    def __init__(self, graph: IGraphStore, sink: ProvenanceSink, audit: AuditSink) -> None:
        self._g = graph
        self._sink = sink
        self._audit = audit

    # -- extraction -------------------------------------------------------------

    def known_assets(self, tenant: str) -> frozenset[str]:
        """Tags from the Asset register — the only valid contradiction subjects."""
        tags: set[str] = set()
        for node in self._g.nodes_by_label("Asset", tenant):
            tag = str(node.props.get("tag") or "").strip()
            if tag:
                tags.add(tag.upper())
        return frozenset(tags)

    def _dominant_subject(self, spans: Iterable[Span], known: frozenset[str]) -> dict[str, str]:
        """doc_id -> the asset tag mentioned most often across that document's spans."""
        counts: dict[str, Counter[str]] = defaultdict(Counter)
        for sp in spans:
            for tag in _asset_tags(sp.text or "", known):
                counts[sp.doc_id][tag] += 1
        return {doc: c.most_common(1)[0][0] for doc, c in counts.items() if c}

    def assertions(self, spans: list[Span], known: frozenset[str]) -> list[Assertion]:
        dominant = self._dominant_subject(spans, known)
        out: list[Assertion] = []
        for sp in spans:
            text = sp.text or ""
            if not text:
                continue
            low = text.lower()
            in_span = _asset_tags(text, known)
            for measure in MEASURES:
                if not any(w in low for w in measure.context):
                    continue
                match = measure.value.search(text)
                if not match:
                    continue
                value = _first_number(match)
                if value is None:
                    continue
                if in_span:
                    subject, source = in_span[0], "span"
                elif sp.doc_id in dominant:
                    subject, source = dominant[sp.doc_id], "document"
                else:
                    continue  # no defensible subject — assert nothing
                out.append(
                    Assertion(
                        subject=subject,
                        subject_source=source,
                        measure=measure,
                        value=value,
                        span_id=sp.span_id,
                        doc_id=sp.doc_id,
                        quote=" ".join(text.split())[:240],
                    )
                )
        return out

    # -- detection --------------------------------------------------------------

    def scan(self, tenant: str, spans: list[Span] | None = None) -> list[Edge]:
        """Find disagreements and write one ``CONTRADICTS`` edge per conflicting pair.

        Edge ids are deterministic (``contra-{kind}-{spanA}-{spanB}`` with the span ids
        sorted), so re-running is idempotent rather than duplicating.
        """
        all_spans = spans if spans is not None else self._g.all_spans(tenant)
        found = self.assertions(all_spans, self.known_assets(tenant))

        grouped: dict[tuple[str, str], list[Assertion]] = defaultdict(list)
        for a in found:
            grouped[(a.subject, a.measure.kind)].append(a)

        written: list[Edge] = []
        for (subject, kind), group in grouped.items():
            for i, a in enumerate(group):
                for b in group[i + 1 :]:
                    # Same document restating its own number is not a contradiction.
                    if a.doc_id == b.doc_id:
                        continue
                    scale = max(abs(a.value), abs(b.value), 1e-9)
                    if abs(a.value - b.value) / scale <= a.measure.tolerance:
                        continue
                    written.append(self._write(a, b, subject, kind, tenant))
        if written:
            self._audit.log(
                "system:contradiction-scan",
                "knowledge.contradictions_detected",
                tenant,
                detail={"count": len(written)},
            )
        return written

    def _write(self, a: Assertion, b: Assertion, subject: str, kind: str, tenant: str) -> Edge:
        left, right = sorted([a, b], key=lambda x: x.span_id)
        edge = Edge(
            id=f"contra-{kind}-{left.span_id}-{right.span_id}",
            type=EdgeType.CONTRADICTS,
            src=left.span_id,
            dst=right.span_id,
            tenant=tenant,
            confidence=0.9 if a.subject_source == b.subject_source == "span" else 0.75,
            props={
                "subject": subject,
                "measure": kind,
                "measure_label": a.measure.label,
                "unit": a.measure.unit,
                "left_value": left.value,
                "right_value": right.value,
                "left_doc": left.doc_id,
                "right_doc": right.doc_id,
                "left_quote": left.quote,
                "right_quote": right.quote,
                "subject_source": (
                    "span" if a.subject_source == b.subject_source == "span" else "document"
                ),
                "summary": (
                    f"{subject} {a.measure.label}: {left.doc_id} states "
                    f"{left.value:g} {a.measure.unit}, {right.doc_id} states "
                    f"{right.value:g} {a.measure.unit}."
                ),
            },
        )
        # CONTRADICTS is not in FACT_BEARING_EDGES, but it is an assertion about the plant, so
        # it goes through the sink with both spans attached — the disagreement is itself cited.
        span_a = self._g.get_span(left.span_id)
        span_b = self._g.get_span(right.span_id)
        evidence = [s for s in (span_a, span_b) if s is not None]
        self._sink.write_edge(edge, spans=evidence or None)
        return edge

