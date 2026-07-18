"""Seed the provenance-clean demo corpus (ADR-012, Bible §11.4).

Deterministic by construction so the scripted demo lands every time (Bible §11.7):
  - 4 identifiers → 1 asset (P-101B) resolution proposal (primary wow, M2).
  - a multi-hop causal chain for "why is P-101B running hot?" (secondary wow, M1).
  - an overdue OISD obligation with an evidence chain (M6).
  - Anil in organizational memory for the "who to ask" refusal (M1 abstain / M5).
  - a 2019 decision-replay chain incl. a rejected alternative (M3).

Every fact-bearing node/edge is written through the ProvenanceSink with a source span (CP-1).
Run:  python -m app.seed
"""
from __future__ import annotations

from datetime import date

from .container import get_container
from .domain.graph_types import EdgeType, NodeLabel
from .domain.models import Edge, Node, ResolutionProposal, Span

TENANT = "demo"


def _span(g, vector, sink, span_id: str, doc_id: str, page: int, text: str) -> Span:
    sp = Span(span_id=span_id, doc_id=doc_id, page=page, text=text, tenant=TENANT)
    sink.write_span(sp)
    vector.upsert(span_id, text, {"doc_id": doc_id, "page": page}, TENANT)
    return sp


def _doc(g, doc_id: str, filename: str, dtype: str) -> None:
    g.upsert_node(Node(id=doc_id, label=NodeLabel.DOCUMENT, tenant=TENANT,
                       props={"filename": filename, "type": dtype, "version": 1}))


def seed() -> dict:
    c = get_container()
    g = c.stores.graph
    v = c.stores.vector
    rel = c.stores.relational
    sink = c.sink

    # ---- documents ----
    _doc(g, "DOC-DCS-ALARMS", "dcs_alarm_export.csv", "csv")
    _doc(g, "DOC-INSP-2019", "inspection_note_2019.pdf", "pdf")
    _doc(g, "DOC-PID-04", "pid_sheet_04.pdf", "pdf")
    _doc(g, "DOC-OEM-BFP", "oem_manual_bfp.pdf", "pdf")
    _doc(g, "DOC-INCIDENT-LOG", "shift_incident_log.csv", "csv")
    _doc(g, "DOC-OISD-129", "oisd_std_129_excerpt.pdf", "pdf")
    _doc(g, "DOC-DECISION-2019", "rca_shutdown_review_2019.pdf", "pdf")

    # ---- spans (the evidence) ----
    s_vib = _span(g, v, sink, "DOC-DCS-ALARMS:s1", "DOC-DCS-ALARMS", 1,
                  "Vibration sensor VIB-101B on pump P-101B recorded a HIGH-VIBRATION alarm; the "
                  "pump P-101B is running hot at the drive-end bearing.")
    s_strainer = _span(g, v, sink, "DOC-INSP-2019:s1", "DOC-INSP-2019", 14,
                       "2019 inspection note: strainer S-14 immediately upstream of P-101B was "
                       "found fouled, restricting suction flow to the pump.")
    s_pid = _span(g, v, sink, "DOC-PID-04:s1", "DOC-PID-04", 4,
                  "P&ID sheet 04: strainer S-14 is CONNECTED_TO the suction of Boiler Feed Pump "
                  "P-101B.")
    s_oem = _span(g, v, sink, "DOC-OEM-BFP:s1", "DOC-OEM-BFP", 22,
                  "OEM manual (model BFP-2205-B): the Boiler Feed Pump exhibits bearing overheating "
                  "and runs hot when suction is restricted.")
    s_feed = _span(g, v, sink, "DOC-INCIDENT-LOG:s1", "DOC-INCIDENT-LOG", 1,
                   "At 21:00 a feedstock change increased the thermal load on P-101B ahead of the "
                   "high-vibration alarm.")
    s_oisd = _span(g, v, sink, "DOC-OISD-129:s1", "DOC-OISD-129", 7,
                   "OISD-STD-129 clause 7.3 requires rotating-equipment vibration inspection of "
                   "boiler feed pumps at 12-month periodicity.")

    # ---- asset + topology ----
    asset = Node(id="asset-p101b", label=NodeLabel.ASSET, tenant=TENANT,
                 props={"tag": "P-101B", "name": "Boiler Feed Pump B", "iso14224_class": "PU",
                        "functional_location": "BOILER-FEED-TRAIN-1"}, effective_from=date(2015, 1, 1))
    sink.write_node(asset, spans=[s_pid])

    strainer = Node(id="asset-s14", label=NodeLabel.ASSET, tenant=TENANT,
                    props={"tag": "S-14", "name": "Suction Strainer 14", "iso14224_class": "FS"},
                    effective_from=date(2015, 1, 1))
    sink.write_node(strainer, spans=[s_pid])

    sink.write_edge(Edge(id="conn-s14-p101b", type=EdgeType.CONNECTED_TO, src="asset-s14",
                         dst="asset-p101b", tenant=TENANT, effective_from=date(2015, 1, 1)),
                    spans=[s_pid])

    sensor = Node(id="sensor-vib-101b", label=NodeLabel.SENSOR, tenant=TENANT,
                  props={"tag": "VIB-101B", "uom": "mm/s", "alarm_limits": "7.1 mm/s"},
                  effective_from=date(2015, 1, 1))
    sink.write_node(sensor, spans=[s_vib])
    sink.write_edge(Edge(id="mon-vib-p101b", type=EdgeType.MONITORS, src="sensor-vib-101b",
                         dst="asset-p101b", tenant=TENANT), spans=[s_vib])

    fm = Node(id="fm-bearing-overheat", label=NodeLabel.FAILURE_MODE, tenant=TENANT,
              props={"iso14224_code": "BRG-OVH", "description": "bearing overheating / running hot"})
    sink.write_node(fm, spans=[s_oem])
    sink.write_edge(Edge(id="exh-p101b-brg", type=EdgeType.EXHIBITS, src="asset-p101b",
                         dst="fm-bearing-overheat", tenant=TENANT), spans=[s_oem])

    insp = Node(id="insp-2019-strainer", label=NodeLabel.INSPECTION, tenant=TENANT,
                props={"date": "2019-03-11", "result": "strainer fouled", "method": "visual"})
    sink.write_node(insp, spans=[s_strainer])
    sink.write_edge(Edge(id="hasinsp-p101b-2019", type=EdgeType.HAS_INSPECTION, src="asset-p101b",
                         dst="insp-2019-strainer", tenant=TENANT), spans=[s_strainer])

    incident = Node(id="inc-feedstock", label=NodeLabel.INCIDENT, tenant=TENANT,
                    props={"date": "2026-07-17", "severity": "medium", "category": "process-upset"})
    sink.write_node(incident, spans=[s_feed])
    sink.write_edge(Edge(id="hasinc-p101b", type=EdgeType.HAS_INCIDENT, src="asset-p101b",
                         dst="inc-feedstock", tenant=TENANT), spans=[s_feed])

    # ---- the 4 identifiers (the moat: 4 → 1) ----
    idents = [
        ("ident-p101b", "P-101B", "cmms", "cmms"),
        ("ident-bfpb", "Boiler Feed Pump B", "dms", "operator"),
        ("ident-oem", "BFP-2205-B", "oem", "oem"),
        ("ident-noisy", "the noisy one", "operator", "operator"),
    ]
    for nid, value, src, vocab in idents:
        g.upsert_node(Node(id=nid, label=NodeLabel.IDENTIFIER, tenant=TENANT,
                           props={"value": value, "source_system": src, "vocabulary": vocab,
                                  "context": "boiler feed pump P-101B drive-end bearing"}))

    # Seed the medium-confidence proposal directly so the queue is deterministic (Bible §11.4).
    proposal = ResolutionProposal(
        proposal_id="prop-p101b-4to1",
        canonical_asset_id="asset-p101b",
        canonical_tag="P-101B",
        identifier_ids=[i[0] for i in idents],
        identifiers=[{"id": i[0], "value": i[1], "source_system": i[2], "vocabulary": i[3]}
                     for i in idents],
        score=0.78,
        method="rules+embedding",
        features={"tag_pattern": 0.42, "fuzzy": 0.35, "iso_class": 1.0, "wo_history": 1.0,
                  "embedding": 0.81},
        tenant=TENANT,
    )
    rel.put("resolution_proposal", proposal.proposal_id, proposal.model_dump(mode="json"), TENANT)

    # ---- compliance: overdue OISD obligation ----
    instrument = Node(id="inst-oisd", label=NodeLabel.INSTRUMENT, tenant=TENANT,
                      props={"name": "OISD", "authority": "OISD (Oil Industry Safety Directorate)"})
    g.upsert_node(instrument)
    ob = Node(id="ob-oisd-129-73", label=NodeLabel.OBLIGATION, tenant=TENANT,
              props={"clause": "OISD-STD-129 cl.7.3", "periodicity_months": 12,
                     "effective_from": "2018-01-01"})
    sink.write_node(ob, spans=[s_oisd])
    sink.write_edge(Edge(id="gov-ob-p101b", type=EdgeType.GOVERNS, src="ob-oisd-129-73",
                         dst="asset-p101b", tenant=TENANT), spans=[s_oisd])
    g.upsert_edge(Edge(id="def-ob-oisd", type=EdgeType.DEFINED_IN, src="ob-oisd-129-73",
                       dst="inst-oisd", tenant=TENANT))
    rel.put("compliance_rule", "ob-oisd-129-73",
            {"clause": "OISD-STD-129 cl.7.3", "instrument": "OISD",
             "total_clauses_in_instrument": 42, "periodicity_months": 12}, TENANT)

    # ---- organizational memory: Anil (the retiring expert) ----
    anil = Node(id="person-anil", label=NodeLabel.PERSON, tenant=TENANT,
                props={"name": "Anil", "role": "reliability", "tenure_years": 34,
                       "retirement_risk": True})
    g.upsert_node(anil)
    g.upsert_edge(Edge(id="knows-anil-p101b", type=EdgeType.KNOWS, src="person-anil",
                       dst="asset-p101b", tenant=TENANT,
                       props={"expertise": "strainer fouling and BFP bearing failures"}))
    g.upsert_edge(Edge(id="knows-anil-fm", type=EdgeType.KNOWS, src="person-anil",
                       dst="fm-bearing-overheat", tenant=TENANT,
                       props={"expertise": "boiler feed pump bearing overheating"}))

    # ---- decision-replay chain (M3, additive) ----
    _seed_decision_graph(g, sink, s_strainer, s_oem)

    # ---- run the decay job once so M4 has flags ----
    c.decay.run(TENANT)

    snap = g.snapshot()
    return {"tenant": TENANT, "graph": snap,
            "resolution_proposals": len(rel.list("resolution_proposal", TENANT))}


def _seed_decision_graph(g, sink, s_strainer, s_oem) -> None:
    chain = [
        ("dec-obs-2019", NodeLabel.OBSERVATION, {"title": "2019: recurring high vibration on P-101B",
                                                 "date": "2019-03-11"}),
        ("dec-hyp-2019", NodeLabel.HYPOTHESIS, {"title": "Hypothesis: suction strainer fouling"}),
        ("dec-evi-2019", NodeLabel.EVIDENCE, {"title": "Strainer S-14 found fouled on inspection"}),
        ("dec-decision-2019", NodeLabel.DECISION, {"title": "Clean strainer; do NOT shut the unit down",
                                                   "date": "2019-03-12", "asset_id": "asset-p101b"}),
        ("dec-alt-2019", NodeLabel.ALTERNATIVE, {"title": "Rejected alternative: full unit shutdown",
                                                 "text": "Rejected — production impact judged to "
                                                 "outweigh risk given strainer was cleanable online."}),
        ("dec-risk-2019", NodeLabel.RISK_ACCEPTED, {"title": "Accepted risk: continued run to next TA"}),
        ("dec-out-2019", NodeLabel.OUTCOME, {"title": "Vibration returned to normal after cleaning"}),
        ("dec-les-2019", NodeLabel.LESSON_LEARNED, {"title": "Lesson: strainer DP trend predicts BFP "
                                                    "vibration; monitor DP, not just vibration."}),
    ]
    spans = {NodeLabel.EVIDENCE: [s_strainer], NodeLabel.HYPOTHESIS: [s_strainer],
             NodeLabel.OBSERVATION: [s_oem]}
    prev = None
    for nid, label, props in chain:
        node = Node(id=nid, label=label, tenant=TENANT, props=props, effective_from=date(2019, 3, 11))
        if label in (NodeLabel.HYPOTHESIS, NodeLabel.EVIDENCE):
            sink.write_node(node, spans=spans.get(label, []))
        else:
            g.upsert_node(node)
        if prev:
            g.upsert_edge(Edge(id=f"led-{prev}-{nid}", type=EdgeType.LED_TO, src=prev, dst=nid,
                               tenant=TENANT))
        prev = nid


if __name__ == "__main__":
    result = seed()
    print("SENTINEL demo corpus seeded (provenance-clean, ADR-012).")
    print(f"  Profile:   {get_container().settings.profile}")
    print(f"  Graph:     {result['graph']}")
    print(f"  Proposals: {result['resolution_proposals']} (the 4->1 resolution awaits adjudication)")
    print("  Try:       ask 'why is P-101B running hot?' -- then set SENTINEL_FORCE_RUNG=-graph")
    print("             and ask again to see the honest refusal (CP-4).")
