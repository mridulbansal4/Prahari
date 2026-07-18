"""M7 Execution Center — draft + gated submit (Bible §7.3, CP-3)."""
from __future__ import annotations

from fastapi import APIRouter, Depends

from ..auth.abac import Principal
from ..auth.rbac import Access
from ..container import Container
from .deps import container, require_module
from .schemas import WorkOrderDraftRequest, WorkOrderRejectRequest, WorkOrderSubmitRequest

router = APIRouter(tags=["actions"])


@router.post("/v1/actions/work-order/draft")
async def draft(
    body: WorkOrderDraftRequest,
    principal: Principal = Depends(require_module("M7", Access.CONTRIBUTE)),
    c: Container = Depends(container),
) -> dict:
    asset = c.stores.graph.get_node(body.asset_id)
    tag = str(asset.props.get("tag")) if asset else body.asset_id
    d = c.actions.draft(body.asset_id, tag, body.symptom, principal,
                        hypothesis_id=body.hypothesis_id, investigation_id=body.investigation_id)
    return {"draft_id": d.draft_id, "preview": d.preview, "status": d.status}


@router.post("/v1/actions/work-order/submit", status_code=201)
async def submit(
    body: WorkOrderSubmitRequest,
    principal: Principal = Depends(require_module("M7", Access.ACT)),
    c: Container = Depends(container),
) -> dict:
    # The approver identity in the body must resolve to a real principal (CP-3, distinct authority).
    d = c.actions.submit(body.draft_id, principal, cmms_ok=body.cmms_ok)
    return {"cmms_work_order_id": d.cmms_work_order_id, "status": d.status,
            "approver": d.approver, "drafter": d.drafter}


@router.post("/v1/actions/work-order/reject")
async def reject(
    body: WorkOrderRejectRequest,
    principal: Principal = Depends(require_module("M7", Access.ACT)),
    c: Container = Depends(container),
) -> dict:
    d = c.actions.reject(body.draft_id, principal, reason=body.reason)
    return {"status": d.status}


@router.get("/v1/actions")
async def list_actions(
    principal: Principal = Depends(require_module("M7")),
    c: Container = Depends(container),
) -> dict:
    return {"drafts": [d.model_dump(mode="json") for d in c.actions.list_all(principal.tenant)]}
