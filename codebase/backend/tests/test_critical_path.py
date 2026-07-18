"""Critical-path tests: ingestion → resolution → investigation → correction (PRB §5.4).

Each maps to a PRB acceptance criterion or an engineering invariant (CP-#). These are the
release-gating cases (Bible §14, §15).
"""
from __future__ import annotations

from conftest import auth


# --------------------------------------------------------------------------- shell / auth
def test_health_and_login(client):
    assert client.get("/v1/health").json()["status"] == "ok"
    me = client.get("/v1/auth/me", headers=auth(client, "ravi")).json()
    assert me["role"] == "technician"
    assert "M1" in me["modules"] and "M11" not in me["modules"]  # nav hidden by role (PRB §2.1, §1.4)


# ------------------------------------------------------------------ M1 grounded investigation
def test_investigation_grounded_with_citations(client):
    h = auth(client, "ravi")
    inv_id = client.post("/v1/investigations",
                         json={"question": "why is P-101B running hot?"}, headers=h).json()["investigation_id"]
    result = client.get(f"/v1/investigations/{inv_id}", headers=h).json()
    assert result["abstained"] is False
    assert len(result["claims"]) >= 1
    # Every claim carries >=1 citation with a doc + span (CP-2, §2.2 Gherkin).
    for claim in result["claims"]:
        assert claim["citations"], "a grounded claim must cite a span (CP-2)"
        assert claim["citations"][0]["doc_id"]
    # The traversal path rendered progressively (graph_path present).
    assert any(h.get("edge") for h in result["graph_path"])
    # Reproducibility fields logged (CP-7 / §8.5).
    assert result["prompt_manifest_hash"] and result["model_id"]


# --------------------------------------------------------------------- M1 abstention (CP-4)
def test_abstention_is_a_success_state(client):
    from app.container import get_container

    c = get_container()
    c.settings.force_rung = "-graph"  # graph disabled → the demo's closing move
    try:
        h = auth(client, "ravi")
        inv_id = client.post("/v1/investigations",
                             json={"question": "why is P-101B running hot?"},
                             headers=h).json()["investigation_id"]
        result = client.get(f"/v1/investigations/{inv_id}", headers=h).json()
        assert result["abstained"] is True
        assert result["who_to_ask"], "abstention must name who to ask (CP-4)"
        assert result["degradation_level"] == "-graph"
    finally:
        c.settings.force_rung = None


# ------------------------------------------------------------- M2 resolution 4->1 + reverse
def test_resolution_four_to_one_and_reversible(client):
    admin = auth(client, "deepak")
    q = client.get("/v1/resolution/queue", headers=admin).json()
    prop = next(p for p in q["proposals"] if p["proposal_id"] == "prop-p101b-4to1")
    assert len(prop["identifier_ids"]) == 4  # four names, one pump (§2.3 Gherkin)

    res = client.post(f"/v1/resolution/{prop['proposal_id']}/adjudicate",
                      json={"decision": "merge", "approver": "deepak"}, headers=admin).json()
    merge_id = res["reversible_id"]
    assert res["resulting_asset_id"] == "asset-p101b"

    # Now the identifier resolves to the asset (RESOLVED_AS written).
    from app.container import get_container

    g = get_container().stores.graph
    edges = g.edges_from("ident-noisy", "RESOLVED_AS", "demo")
    assert any(e.dst == "asset-p101b" for e in edges)

    # Reversible (BR-4): unmerge restores prior state.
    un = client.post(f"/v1/resolution/unmerge/{merge_id}", headers=admin).json()
    assert un["restored"] is True
    assert not get_container().stores.graph.edges_from("ident-noisy", "RESOLVED_AS", "demo")


def test_unmerge_requires_admin(client):
    # reliability may adjudicate but not unmerge (higher bar, PRB §2.3).
    r = client.post("/v1/resolution/unmerge/nonexistent", headers=auth(client, "meera"))
    assert r.status_code == 403


# ------------------------------------------------------------------- M8 correction (CP-10)
def test_correction_is_attributed_and_immediate(client):
    h = auth(client, "anil")
    r = client.post("/v1/corrections", json={
        "target_kind": "fact", "target_ref": "asset-p101b",
        "new_value": "P-101B suction restriction is caused by strainer S-14 fouling",
        "rationale": "Confirmed on the 2019 walkdown.", "author": "anil"}, headers=h)
    assert r.status_code == 201
    hist = client.get("/v1/corrections?target_ref=asset-p101b", headers=h).json()["corrections"]
    assert hist and hist[0]["author"] == "anil"  # never anonymous (BR-7)
    # The correction now appears as prior-correction context in the next answer (Memory agent).
    from app.container import get_container

    priors = get_container().corrections.prior_corrections_for("why is P-101B running hot?", "demo")
    assert any("Anil" in p or "anil" in p for p in priors)


# ------------------------------------------------------------------- M6 compliance (BR-3/FM-6)
def test_compliance_overdue_with_coverage_footer(client):
    h = auth(client, "meera")
    data = client.get("/v1/compliance/assets/asset-p101b", headers=h).json()
    assert any(row["status"] == "overdue" for row in data["rows"])  # overdue OISD obligation
    # The coverage footer is always present and never implies completeness (§2.4 Gherkin).
    assert "not a completeness guarantee" in data["coverage"]["disclaimer"]


# --------------------------------------------------------------------- M7 gated write (CP-3)
def test_gated_write_requires_distinct_approver(client):
    # Ravi (technician) drafts.
    draft = client.post("/v1/actions/work-order/draft",
                        json={"asset_id": "asset-p101b", "symptom": "running hot"},
                        headers=auth(client, "ravi")).json()
    # Ravi cannot approve his own draft (technician not an approver role, CP-3).
    r = client.post("/v1/actions/work-order/submit",
                    json={"draft_id": draft["draft_id"], "approver": "ravi"},
                    headers=auth(client, "ravi"))
    assert r.status_code == 403
    # Meera (reliability) approves → committed with a CMMS id.
    ok = client.post("/v1/actions/work-order/submit",
                     json={"draft_id": draft["draft_id"], "approver": "meera"},
                     headers=auth(client, "meera"))
    assert ok.status_code == 201
    assert ok.json()["cmms_work_order_id"].startswith("CMMS-WO")


def test_cmms_unreachable_never_marks_committed(client):
    draft = client.post("/v1/actions/work-order/draft",
                        json={"asset_id": "asset-p101b", "symptom": "test"},
                        headers=auth(client, "ravi")).json()
    r = client.post("/v1/actions/work-order/submit",
                    json={"draft_id": draft["draft_id"], "approver": "meera", "cmms_ok": False},
                    headers=auth(client, "meera"))
    assert r.status_code == 409  # explicit "not committed", never silently done (NFR-13)


# ------------------------------------------------------------------------ CP-1 provenance
def test_provenance_sink_rejects_unsourced_fact(client):
    import pytest

    from app.domain.errors import ProvenanceViolation
    from app.domain.graph_types import NodeLabel
    from app.domain.models import Node
    from app.container import get_container

    sink = get_container().sink
    with pytest.raises(ProvenanceViolation):
        sink.write_node(Node(id="asset-orphan", label=NodeLabel.ASSET, tenant="demo"), spans=[])


# ------------------------------------------------------------------------ M9 audit (§8.5)
def test_audit_records_writes(client):
    entries = client.get("/v1/audit?action=action.submitted",
                         headers=auth(client, "deepak")).json()["entries"]
    assert any(e["action"] == "action.submitted" for e in entries)
