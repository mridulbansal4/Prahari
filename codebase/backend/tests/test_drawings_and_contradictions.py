"""Drawing → graph topology, OCR/VLM quarantine, and cross-document contradiction detection.

The vision model itself is not exercised here — that needs a key and a GPU-backed endpoint.
What IS exercised is everything around it: that a drawing reader's output becomes real
`CONNECTED_TO` edges with provenance, that an unavailable provider quarantines instead of
inventing, and that the contradiction detector finds genuine disagreement and only that.
"""
from __future__ import annotations

import pytest

from app.container import get_container
from app.domain.graph_types import EdgeType
from app.domain.models import Span
from app.ingestion.drawing_schema import (
    DrawingExtraction,
    DrawnAnnotation,
    DrawnComponent,
    DrawnConnection,
)
from app.knowledge.contradictions import ContradictionDetector

TENANT = "demo"

# PNG magic bytes: a raster drawing goes straight to the reader without PDF rendering,
# which keeps these tests about the wiring rather than about PyMuPDF.
def png(unique: str) -> bytes:
    """A distinct raster per test — ingestion is idempotent by content hash, so two
    tests sharing bytes would make the second a duplicate rather than a fresh run."""
    return bytes.fromhex("89504e470d0a1a0a") + unique.encode() + bytes(32)


class StubDrawingReader:
    """Stands in for Cosmos: returns what a vision model would report for the BFW P&ID."""

    id = "stub"

    def __init__(self, extraction: DrawingExtraction | None = None) -> None:
        self._extraction = extraction

    def available(self) -> bool:
        return True

    def read_drawing(self, page, mime="image/png", hint=None):  # noqa: ANN001, ARG002
        if self._extraction is None:
            raise RuntimeError("reader failed")
        return self._extraction


def _bfw_drawing() -> DrawingExtraction:
    return DrawingExtraction(
        drawing_title="BOILER FEED WATER SYSTEM — P&ID",
        drawing_number="PID-BFW-04",
        components=[
            DrawnComponent(tag="S-14", kind="strainer", label="Suction Strainer 14",
                           source_note="S-14 SUCTION STRAINER shown on suction header"),
            DrawnComponent(tag="P-101B", kind="pump", label="Boiler Feed Pump B",
                           source_note="P-101B BOILER FEED PUMP B"),
            DrawnComponent(tag="V-201", kind="vessel", label="Knockout Drum",
                           source_note="V-201 KNOCKOUT DRUM"),
        ],
        connections=[
            DrawnConnection(from_tag="S-14", to_tag="P-101B", relation="CONNECTED_TO",
                            line_number='8"-BFW-1041',
                            source_note='S-14 discharges to P-101B suction via 8"-BFW-1041'),
        ],
        annotations=[
            DrawnAnnotation(subject_tag="P-101B", text="SEAL PLAN: API 682 PLAN 23",
                            kind="seal_plan", source_note="printed beside P-101B"),
        ],
        confidence=0.9,
    )


@pytest.fixture()
def container():
    return get_container()


# --------------------------------------------------------------------------- drawings

def test_drawing_without_vlm_is_quarantined_not_guessed(container):
    """No reader configured → the drawing is set aside with a reason. Topology is never faked."""
    original = container.ingestion._drawings
    container.ingestion._drawings = None
    try:
        job = container.ingestion.ingest(
            "PID-BFW-99_test.png", png("no-vlm"), TENANT, "tester")
    finally:
        container.ingestion._drawings = original

    assert job.status.value == "quarantined"
    assert "no VLM is configured" in (job.quarantine_reason or "")
    assert job.span_count == 0
    assert "graphics" in [s.get("stage") for s in job.stage_log]


def test_drawing_becomes_graph_topology(container):
    """The point of the VLM: a drawing yields S-14 CONNECTED_TO P-101B, with provenance."""
    original = container.ingestion._drawings
    container.ingestion._drawings = StubDrawingReader(_bfw_drawing())
    try:
        job = container.ingestion.ingest(
            "PID-BFW-04_topology.png", png("topology"), TENANT, "tester")
    finally:
        container.ingestion._drawings = original

    assert job.status.value == "complete", job.quarantine_reason
    assert job.span_count >= 4  # 3 components + 1 connection + 1 annotation

    graph = container.stores.graph
    s14 = graph.find_identifier("S-14", TENANT)
    assert s14 is not None, "the drawing's components must reach the graph"

    connected = [
        e for e in graph.all_edges(TENANT)
        if e.type == EdgeType.CONNECTED_TO and e.props.get("from_drawing") == "PID-BFW-04"
    ]
    assert connected, "the drawing must produce a CONNECTED_TO edge"
    assert connected[0].props.get("line_number") == '8"-BFW-1041'


def test_reader_failure_quarantines(container):
    original = container.ingestion._drawings
    container.ingestion._drawings = StubDrawingReader(None)  # raises
    try:
        job = container.ingestion.ingest(
            "PID-BFW-98_broken.png", png("broken"), TENANT, "tester")
    finally:
        container.ingestion._drawings = original
    assert job.status.value == "quarantined"
    assert "Drawing reader failed" in (job.quarantine_reason or "")


def test_dangling_connections_are_dropped():
    """A model naming an edge whose endpoints it never reported has not read the diagram."""
    d = DrawingExtraction(
        components=[DrawnComponent(tag="P-101B")],
        connections=[
            DrawnConnection(from_tag="P-101B", to_tag="GHOST-99"),
            DrawnConnection(from_tag="P-101B", to_tag="P-101B"),
        ],
    )
    d.drop_dangling_connections()
    assert all(c.to_tag == "P-101B" for c in d.connections)
    assert not any(c.to_tag == "GHOST-99" for c in d.connections)


# ------------------------------------------------------------------------------- ocr

def test_scanned_page_without_ocr_is_quarantined(container):
    original = container.ingestion._ocr
    container.ingestion._ocr = None
    try:
        job = container.ingestion.ingest("inspection_scan.png", png("scan"), TENANT, "tester")
    finally:
        container.ingestion._ocr = original
    assert job.status.value == "quarantined"
    assert "no OCR provider" in (job.quarantine_reason or "")


def test_binary_upload_never_becomes_citable_garbage(container):
    """Regression: a PDF used to decode as mojibake and land in the graph as evidence."""
    original = container.ingestion._ocr
    container.ingestion._ocr = None
    try:
        job = container.ingestion.ingest(
            "scan_report.pdf", b"%PDF-1.7\n\x00\x01\x02binary noise", TENANT, "tester")
    finally:
        container.ingestion._ocr = original
    assert job.status.value == "quarantined"
    assert job.span_count == 0


# -------------------------------------------------------------------- contradictions

def _detector(container) -> ContradictionDetector:
    return ContradictionDetector(container.stores.graph, container.sink, container.audit)


def test_detects_disagreement_between_documents(container):
    det = _detector(container)
    known = frozenset({"P-101B"})
    spans = [
        Span(span_id="d1:s1", doc_id="doc-datasheet", page=1, tenant=TENANT,
             text="P-101B bearing temperature alarm 90 C and trip 100 C."),
        Span(span_id="d2:s1", doc_id="doc-manual", page=1, tenant=TENANT,
             text="P-101B bearing high temperature alarm is set at 85 C."),
    ]
    found = det.assertions(spans, known)
    alarms = {a.value for a in found if a.measure.kind == "bearing_temp_alarm"}
    assert alarms == {90.0, 85.0}

    edges = det.scan(TENANT, spans=spans)
    assert len(edges) == 1
    assert edges[0].type == EdgeType.CONTRADICTS
    assert edges[0].props["subject"] == "P-101B"
    assert {edges[0].props["left_value"], edges[0].props["right_value"]} == {85.0, 90.0}


def test_same_document_restating_a_value_is_not_a_contradiction(container):
    det = _detector(container)
    spans = [
        Span(span_id="same:s1", doc_id="doc-one", page=1, tenant=TENANT,
             text="P-101B bearing alarm 85 C."),
        Span(span_id="same:s2", doc_id="doc-one", page=2, tenant=TENANT,
             text="Reminder: P-101B bearing alarm 90 C."),
    ]
    assert det.scan(TENANT, spans=spans) == []


def test_observed_readings_do_not_contradict_the_design_minimum(container):
    """`flow fell to 61 m3/h` is an observation, not a claim about the design minimum."""
    det = _detector(container)
    known = frozenset({"P-101B"})
    spans = [
        Span(span_id="f1:s1", doc_id="doc-a", page=1, tenant=TENANT,
             text="P-101B minimum continuous flow 72 m3/h."),
        Span(span_id="f2:s1", doc_id="doc-b", page=1, tenant=TENANT,
             text="P-101B flow fell to a minimum of 61 m3/h on the afternoon shift."),
    ]
    kinds = {a.measure.kind for a in det.assertions(spans, known)}
    assert kinds == {"min_continuous_flow"}
    assert det.scan(TENANT, spans=spans) == []


def test_non_equipment_tags_are_not_subjects(container):
    """C-276 is a Hastelloy grade, OISD-STD-129 a standard. Neither can own a setpoint."""
    det = _detector(container)
    known = frozenset({"P-101B"})
    spans = [
        Span(span_id="m1:s1", doc_id="doc-x", page=1, tenant=TENANT,
             text="Seal faces C-276. Gland bolt tightening torque 45 N.m."),
    ]
    subjects = {a.subject for a in det.assertions(spans, known)}
    assert "C-276" not in subjects
