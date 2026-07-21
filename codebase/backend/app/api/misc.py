"""M9 Audit, M10 Analytics, M5 Org Memory, M4 Knowledge, M3 Decision Replay, health."""
from __future__ import annotations

from fastapi import APIRouter, Depends

from ..auth.abac import Principal
from ..auth.rbac import Access
from ..container import Container, get_container
from .deps import container, current_principal, require_module
from .schemas import ExpertiseUpsert, KnowsUpsert

router = APIRouter()


# ------------------------------------------------------------------- assets (shared lookup)
@router.get("/v1/assets", tags=["assets"])
async def list_assets(
    principal: Principal = Depends(current_principal),
    c: Container = Depends(container),
) -> dict:
    """Assets in the tenant graph — used by asset pickers and role dashboards (no hardcoding)."""
    nodes = c.stores.graph.nodes_by_label("Asset", principal.tenant)
    return {
        "assets": [
            {"id": n.id, "tag": n.props.get("tag"), "name": n.props.get("name"),
             "iso_class": n.props.get("iso14224_class")}
            for n in nodes
        ]
    }


# ---------------------------------------------------------------- M9 Audit & Provenance
@router.get("/v1/audit", tags=["audit"])
async def audit_log(
    actor: str | None = None,
    action: str | None = None,
    frm: str | None = None,
    to: str | None = None,
    principal: Principal = Depends(require_module("M9")),
    c: Container = Depends(container),
) -> dict:
    entries = c.audit.query(principal.tenant, actor=actor, action=action, frm=frm, to=to)
    return {"entries": [e.model_dump(mode="json") for e in entries]}


# ---------------------------------------------------------------------- M10 Analytics
@router.get("/v1/analytics", tags=["analytics"])
async def analytics(
    principal: Principal = Depends(require_module("M10")),
    c: Container = Depends(container),
) -> dict:
    c.audit.log(principal.subject, "analytics.viewed", principal.tenant)
    return c.analytics.kpis(principal.tenant)


# --------------------------------------------------------------- M5 Organizational Memory
@router.get("/v1/org-memory", tags=["org-memory"])
async def org_directory(
    principal: Principal = Depends(require_module("M5")),
    c: Container = Depends(container),
) -> dict:
    return {"people": [p.model_dump(mode="json") for p in c.org_memory.directory(principal.tenant)]}


@router.post("/v1/org-memory/person", tags=["org-memory"])
async def upsert_person(
    body: ExpertiseUpsert,
    principal: Principal = Depends(require_module("M5", Access.FULL)),
    c: Container = Depends(container),
) -> dict:
    c.org_memory.upsert_person(body.person_id, body.name, body.role, body.tenure_years,
                               body.retirement_risk, principal.tenant, principal.subject)
    return {"ok": True}


@router.post("/v1/org-memory/knows", tags=["org-memory"])
async def add_knows(
    body: KnowsUpsert,
    principal: Principal = Depends(require_module("M5", Access.FULL)),
    c: Container = Depends(container),
) -> dict:
    item = c.org_memory.add_knows(body.person_id, body.target_ref, body.expertise,
                                  principal.tenant, principal.subject, text=body.text,
                                  kind=body.kind, tags=body.tags)
    # Return the stored item so the caller can confirm the knowledge text was kept, rather
    # than trusting a bare {"ok": true}.
    return {"ok": True, "item": item.model_dump(mode="json")}


# ------------------------------------------------------------------- M4 Knowledge Evolution
@router.get("/v1/knowledge/health", tags=["knowledge"])
async def knowledge_health(
    principal: Principal = Depends(require_module("M4")),
    c: Container = Depends(container),
) -> dict:
    return {"flags": [f.model_dump(mode="json") for f in c.decay.list_flags(principal.tenant)],
            "last_run": c.decay.last_run(principal.tenant)}


@router.post("/v1/knowledge/run-decay", tags=["knowledge"])
async def run_decay(
    principal: Principal = Depends(require_module("M4", Access.FULL)),
    c: Container = Depends(container),
) -> dict:
    flags = c.decay.run(principal.tenant)
    return {"flags": [f.model_dump(mode="json") for f in flags]}


@router.post("/v1/knowledge/flags/{flag_id}/reverify", tags=["knowledge"])
async def reverify(
    flag_id: str,
    principal: Principal = Depends(require_module("M4", Access.FULL)),
    c: Container = Depends(container),
) -> dict:
    c.decay.reverify(flag_id, principal.tenant, principal.subject)
    return {"ok": True}


@router.post("/v1/knowledge/flags/{flag_id}/supersede", tags=["knowledge"])
async def supersede(
    flag_id: str,
    principal: Principal = Depends(require_module("M4", Access.FULL)),
    c: Container = Depends(container),
) -> dict:
    c.decay.supersede(flag_id, principal.tenant, principal.subject)
    return {"ok": True}


# -------------------------------------------------------------- M3 Decision Memory & Replay
@router.get("/v1/decisions", tags=["decisions"])
async def list_decisions(
    principal: Principal = Depends(require_module("M3")),
    c: Container = Depends(container),
) -> dict:
    return {"decisions": c.replay.list_decisions(principal.tenant)}


@router.get("/v1/decisions/{decision_id}/replay", tags=["decisions"])
async def replay(
    decision_id: str,
    principal: Principal = Depends(require_module("M3")),
    c: Container = Depends(container),
) -> dict:
    chain = c.replay.replay(decision_id, principal.tenant)
    if not chain:
        return {"decision_id": decision_id, "steps": [],
                "note": "No decision chain recorded for this event."}
    return chain


# ---------------------------------------------- demo/ops control for the CP-9 ladder
@router.post("/v1/admin/degrade", tags=["health"])
async def set_degradation(
    rung: str = "full",
    principal: Principal = Depends(current_principal),
    c: Container = Depends(container),
) -> dict:
    """Force the CP-9 degradation rung at runtime (admin only). This exposes the *existing* rung
    mechanism (Bible §2.8) so the graph-disabled refusal is demonstrable live — it is not a new
    product feature. `full` clears the override."""
    from ..auth.rbac import Role

    if principal.role != Role.ADMIN:
        from ..domain.errors import Forbidden

        raise Forbidden("Degradation control is admin-only.")
    c.settings.force_rung = None if rung == "full" else rung
    c.audit.log(principal.subject, "admin.degrade_set", principal.tenant, detail={"rung": rung})
    return {"rung": rung}


# ------------------------------------------------------------------------------ health
@router.get("/v1/health", tags=["health"])
async def health() -> dict:
    c = get_container()
    return {"status": "ok", "profile": c.settings.profile,
            "graph": c.stores.graph.snapshot(),
            "forced_rung": c.settings.force_rung or "full"}
