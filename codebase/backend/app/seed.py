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

    # ---- second instrument (PESO) — a SATISFIED obligation, for contrast ----
    s_peso = _span(g, v, sink, "DOC-OISD-129:s2", "DOC-OISD-129", 9,
                   "PESO SMPV rules require a pressure-vessel external inspection of knockout "
                   "drums at 24-month periodicity.")
    g.upsert_node(Node(id="inst-peso", label=NodeLabel.INSTRUMENT, tenant=TENANT,
                       props={"name": "PESO", "authority": "PESO (Petroleum & Explosives Safety Org.)"}))
    ob_peso = Node(id="ob-peso-smpv", label=NodeLabel.OBLIGATION, tenant=TENANT,
                   props={"clause": "PESO SMPV r.12", "periodicity_months": 24,
                          "effective_from": "2018-01-01"})
    sink.write_node(ob_peso, spans=[s_peso])

    # ---- second asset: V-201 knockout drum (single-fact target + PESO obligation) ----
    s_v201 = _span(g, v, sink, "DOC-PID-04:s2", "DOC-PID-04", 5,
                   "Knockout Drum V-201 has a design pressure of 24.5 barg per the vessel datasheet.")
    v201 = Node(id="asset-v201", label=NodeLabel.ASSET, tenant=TENANT,
                props={"tag": "V-201", "name": "Knockout Drum V-201", "iso14224_class": "VE",
                       "design_pressure_barg": 24.5}, effective_from=date(2015, 1, 1))
    sink.write_node(v201, spans=[s_v201])
    sink.write_edge(Edge(id="gov-peso-v201", type=EdgeType.GOVERNS, src="ob-peso-smpv",
                         dst="asset-v201", tenant=TENANT), spans=[s_peso])
    g.upsert_edge(Edge(id="def-peso", type=EdgeType.DEFINED_IN, src="ob-peso-smpv",
                       dst="inst-peso", tenant=TENANT))
    # a recent inspection satisfies the PESO obligation (contrast with the overdue OISD one)
    insp_v201 = Node(id="insp-2026-v201", label=NodeLabel.INSPECTION, tenant=TENANT,
                     props={"date": "2026-05-02", "result": "pass", "method": "external-visual"})
    sink.write_node(insp_v201, spans=[s_v201])
    sink.write_edge(Edge(id="hasinsp-v201", type=EdgeType.HAS_INSPECTION, src="asset-v201",
                         dst="insp-2026-v201", tenant=TENANT), spans=[s_v201])
    rel.put("compliance_rule", "ob-peso-smpv",
            {"clause": "PESO SMPV r.12", "instrument": "PESO",
             "total_clauses_in_instrument": 30, "periodicity_months": 24}, TENANT)

    # ---- organizational memory: the roster, and what each person actually knows ----
    # Every nugget below is traceable to the document corpus (shift logs, the 2023 incident
    # report, the strainer history) — none is invented for the demo. Captured through the
    # service so the text is written as a citable span and indexed for retrieval, exactly as a
    # nugget typed into the capture form would be.
    people = [
        ("person-anil", "Anil Kumar", "reliability", 34, True),
        ("person-suresh", "Suresh Nair", "rotating equipment", 21, False),
        ("person-priya", "Priya Menon", "instrumentation", 12, False),
        ("person-ravi-s", "Ravi Sharma", "shift supervisor", 17, False),
    ]
    for pid, name, role, tenure, risk in people:
        c.org_memory.upsert_person(pid, name, role, tenure, risk, TENANT, "system:seed")

    captured = [
        # Anil — the retiring expert; the knowledge most at risk.
        ("person-anil", "asset-p101b", "Restart sequence for the parallel BFPs", "rule",
         ["restart", "cavitation", "P-101A", "P-101B"],
         "Never restart P-101A before P-101B after a shutdown. The common suction header "
         "drains toward A, and starting A first pulls the header down and cavitates B. "
         "Start B, let the header repressurise, then bring A up."),
        ("person-anil", "asset-p101b", "Strainer DP predicts bearing trouble", "lesson",
         ["S-14", "strainer", "bearing", "PDI-S14"],
         "Watch PDI-S14, not just vibration. Every bearing event on P-101B I have seen was "
         "preceded by strainer differential creeping past 0.5 bar for a week or two. "
         "Vibration is the last symptom to appear, not the first."),
        ("person-anil", "fm-bearing-overheat", "Low-flow churn is the real cause", "rule",
         ["min flow", "MOV-118", "churn"],
         "Bearing overheating on this pump is almost never a bearing fault. It is the pump "
         "running under its 72 m3/h minimum continuous flow and churning the water. Check "
         "flow and MOV-118 before anyone opens a bearing housing."),
        # Suresh — rotating equipment.
        ("person-suresh", "asset-p101b", "Seal flush cooler fouls silently", "tip",
         ["API 682", "Plan 23", "seal"],
         "There is no gauge on the Plan 23 seal flush loop, so fouling is invisible on the "
         "DCS. Feel the cooler return line by hand — if it is not appreciably cooler than "
         "the supply, the loop is not circulating and the seal is running hot."),
        ("person-suresh", "fm-bearing-overheat", "Alignment reads differently hot", "tip",
         ["alignment", "thermal growth"],
         "Cold alignment on this set looks fine and still runs rough. Take cold readings, "
         "then apply the vendor thermal growth offsets before you sign it off."),
        # Priya — instrumentation.
        ("person-priya", "asset-p101b", "TE-101B reads about 5% high", "tip",
         ["TE-101B", "calibration", "pyrometer"],
         "TE-101B has read roughly 5% high since the 2024 loop check — verified against a "
         "portable pyrometer. An 85 C indication is nearer 81 C in reality. Worth knowing "
         "before anyone trips the unit on an indicated alarm."),
        ("person-priya", "asset-s14", "PDI-S14 needs a zero check after cleaning", "tip",
         ["PDI-S14", "strainer"],
         "After S-14 is cleaned, re-zero PDI-S14. The transmitter holds a small offset if "
         "it is isolated while the basket is out, which makes a clean strainer look fouled."),
        # Ravi — shift supervisor.
        ("person-ravi-s", "asset-p101b", "MOV-118 sticks in summer", "rule",
         ["MOV-118", "min flow", "summer"],
         "MOV-118 sticks on hot afternoons — it will show commanded-open on the DCS and "
         "barely move. There is no position-deviation alarm, so you have to look at the "
         "feedback. If P-101B is running hot in the afternoon, check the valve physically."),
        ("person-ravi-s", "asset-p101b", "P-101B runs hot on hot afternoons", "lesson",
         ["ambient", "afternoon"],
         "This is a daytime problem, not a night one. Overnight the pump sits normal; it is "
         "the afternoon ambient plus reduced flow that pushes the bearing up."),
    ]
    for pid, target, title, kind, tags, text in captured:
        c.org_memory.add_knows(pid, target, title, TENANT, "system:seed",
                               text=text, kind=kind, tags=tags)

    # ---- decision-replay chain (M3, additive) ----
    _seed_decision_graph(g, sink, s_strainer, s_oem)

    # ---- run the decay job once so M4 has flags ----
    c.decay.run(TENANT)

    snap = g.snapshot()
    return {"tenant": TENANT, "graph": snap,
            "resolution_proposals": len(rel.list("resolution_proposal", TENANT))}


def _seed_decision_graph(g, sink, s_strainer, s_oem) -> None:
    # Four recorded decisions, each a full reasoning chain
    # (Observation → Hypothesis → Evidence → Decision → Alternative → RiskAccepted → Outcome →
    # LessonLearned) so the page reads like real institutional memory, not a single example.
    # Every chain is drawn from the document corpus — the 2019 strainer call, the 2023 seal
    # failure, the TE-101B calibration bias, and the MOV-118 sticking valve.
    chains = [
        {
            "eff": date(2019, 3, 11),
            "evidence_span": s_strainer,
            "nodes": [
                ("dec-obs-2019", NodeLabel.OBSERVATION,
                 {"title": "2019: recurring high vibration on P-101B", "date": "2019-03-11"}),
                ("dec-hyp-2019", NodeLabel.HYPOTHESIS,
                 {"title": "Hypothesis: suction strainer fouling"}),
                ("dec-evi-2019", NodeLabel.EVIDENCE,
                 {"title": "Strainer S-14 found fouled on inspection"}),
                ("dec-decision-2019", NodeLabel.DECISION,
                 {"title": "Clean the strainer online rather than shut the unit down",
                  "date": "2019-03-12", "asset_id": "asset-p101b"}),
                ("dec-alt-2019", NodeLabel.ALTERNATIVE,
                 {"title": "Rejected: full unit shutdown",
                  "text": "Rejected — the production impact of a shutdown outweighed the risk, "
                          "given the strainer was cleanable online."}),
                ("dec-risk-2019", NodeLabel.RISK_ACCEPTED,
                 {"title": "Accepted risk: continued run to the next turnaround"}),
                ("dec-out-2019", NodeLabel.OUTCOME,
                 {"title": "Vibration returned to normal after cleaning"}),
                ("dec-les-2019", NodeLabel.LESSON_LEARNED,
                 {"title": "Lesson: strainer DP trend predicts BFP vibration — monitor DP, "
                           "not just vibration."}),
            ],
        },
        {
            "eff": date(2023, 8, 20),
            "evidence_span": s_oem,
            "nodes": [
                ("dec-obs-2023", NodeLabel.OBSERVATION,
                 {"title": "2023: mechanical seal failure on P-101B", "date": "2023-08-18"}),
                ("dec-hyp-2023", NodeLabel.HYPOTHESIS,
                 {"title": "Hypothesis: prolonged run below minimum continuous flow"}),
                ("dec-evi-2023", NodeLabel.EVIDENCE,
                 {"title": "Teardown found MOV-118 stuck and S-14 fouled — pump ran below 72 m³/h"}),
                ("dec-decision-2023", NodeLabel.DECISION,
                 {"title": "Replace the seal and fit a low-flow protective trip",
                  "date": "2023-08-20", "asset_id": "asset-p101b"}),
                ("dec-alt-2023", NodeLabel.ALTERNATIVE,
                 {"title": "Rejected: replace the seal only",
                  "text": "Rejected — a like-for-like seal swap leaves the low-flow cause in "
                          "place, so the failure would recur."}),
                ("dec-risk-2023", NodeLabel.RISK_ACCEPTED,
                 {"title": "Accepted risk: trip setpoint tightening pending MOC approval"}),
                ("dec-out-2023", NodeLabel.OUTCOME,
                 {"title": "Pump returned to service; no repeat seal failure since"}),
                ("dec-les-2023", NodeLabel.LESSON_LEARNED,
                 {"title": "Lesson: the seal is the symptom — minimum-flow protection is the fix."}),
            ],
        },
        {
            "eff": date(2024, 6, 3),
            "evidence_span": s_oem,
            "nodes": [
                ("dec-obs-2024", NodeLabel.OBSERVATION,
                 {"title": "TE-101B alarms that don't match field readings", "date": "2024-06-01"}),
                ("dec-hyp-2024", NodeLabel.HYPOTHESIS,
                 {"title": "Hypothesis: TE-101B reads about 5% high"}),
                ("dec-evi-2024", NodeLabel.EVIDENCE,
                 {"title": "Bearing temperature verified against a portable pyrometer"}),
                ("dec-decision-2024", NodeLabel.DECISION,
                 {"title": "Keep the 85 °C alarm and recalibrate TE-101B",
                  "date": "2024-06-03", "asset_id": "asset-p101b"}),
                ("dec-alt-2024", NodeLabel.ALTERNATIVE,
                 {"title": "Rejected: raise the alarm setpoint",
                  "text": "Rejected — moving the setpoint to suppress the nuisance alarm would "
                          "mask a genuine overheat. Fix the instrument, not the limit."}),
                ("dec-risk-2024", NodeLabel.RISK_ACCEPTED,
                 {"title": "Accepted risk: operate with a known instrument bias until calibration"}),
                ("dec-out-2024", NodeLabel.OUTCOME,
                 {"title": "Recalibration scheduled; no spurious trips after operator briefing"}),
                ("dec-les-2024", NodeLabel.LESSON_LEARNED,
                 {"title": "Lesson: fix the instrument, don't move the setpoint."}),
            ],
        },
        {
            "eff": date(2023, 9, 12),
            "evidence_span": s_strainer,
            "nodes": [
                ("dec-obs-mov", NodeLabel.OBSERVATION,
                 {"title": "MOV-118 sticks on hot afternoons, running P-101B below min flow",
                  "date": "2023-09-10"}),
                ("dec-hyp-mov", NodeLabel.HYPOTHESIS,
                 {"title": "Hypothesis: actuator binding with no position-feedback alarm"}),
                ("dec-evi-mov", NodeLabel.EVIDENCE,
                 {"title": "Valve moved 6% and stopped despite a full-open command"}),
                ("dec-decision-mov", NodeLabel.DECISION,
                 {"title": "Overhaul the MOV-118 actuator and add a position-deviation alarm",
                  "date": "2023-09-12", "asset_id": "asset-p101b"}),
                ("dec-alt-mov", NodeLabel.ALTERNATIVE,
                 {"title": "Rejected: replace the whole valve",
                  "text": "Rejected — a full valve replacement carries a long lead time when the "
                          "fault is confined to the actuator."}),
                ("dec-risk-mov", NodeLabel.RISK_ACCEPTED,
                 {"title": "Accepted risk: manual afternoon checks until the alarm is commissioned"}),
                ("dec-out-mov", NodeLabel.OUTCOME,
                 {"title": "Actuator overhauled; the deviation alarm now catches sticking early"}),
                ("dec-les-mov", NodeLabel.LESSON_LEARNED,
                 {"title": "Lesson: a commanded-open signal is not proof of movement — "
                           "alarm on the feedback."}),
            ],
        },
    ]

    for chain in chains:
        spans = {
            NodeLabel.EVIDENCE: [chain["evidence_span"]],
            NodeLabel.HYPOTHESIS: [chain["evidence_span"]],
        }
        prev = None
        for nid, label, props in chain["nodes"]:
            node = Node(id=nid, label=label, tenant=TENANT, props=props, effective_from=chain["eff"])
            if label in (NodeLabel.HYPOTHESIS, NodeLabel.EVIDENCE):
                sink.write_node(node, spans=spans.get(label, []))
            else:
                g.upsert_node(node)
            if prev:
                g.upsert_edge(Edge(id=f"led-{prev}-{nid}", type=EdgeType.LED_TO, src=prev,
                                   dst=nid, tenant=TENANT))
            prev = nid


if __name__ == "__main__":
    result = seed()
    print("Prahari demo corpus seeded (provenance-clean, ADR-012).")
    print(f"  Profile:   {get_container().settings.profile}")
    print(f"  Graph:     {result['graph']}")
    print(f"  Proposals: {result['resolution_proposals']} (the 4->1 resolution awaits adjudication)")
    print("  Try:       ask 'why is P-101B running hot?' -- then set PRAHARI_FORCE_RUNG=-graph")
    print("             and ask again to see the honest refusal (CP-4).")
