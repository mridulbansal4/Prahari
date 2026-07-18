"""M2 Living Asset Map — resolution queue, adjudicate, unmerge (Bible §7.3)."""
from __future__ import annotations

from fastapi import APIRouter, Depends

from ..auth.abac import Principal, can_adjudicate, can_unmerge
from ..auth.rbac import Access
from ..container import Container
from ..domain.errors import Forbidden
from ..domain.models import Adjudication
from .deps import container, require_module
from .schemas import AdjudicateRequest

router = APIRouter(tags=["resolution"])


@router.get("/v1/resolution/queue")
async def queue(
    principal: Principal = Depends(require_module("M2")),
    c: Container = Depends(container),
) -> dict:
    # Regenerate proposals on read so a freshly-seeded corpus surfaces its queue.
    c.resolution.generate_proposals(principal.tenant)
    return {"proposals": [p.model_dump(mode="json") for p in c.resolution.queue(principal.tenant)],
            "corpus_size": c.resolution.corpus_size(principal.tenant)}


@router.post("/v1/resolution/{proposal_id}/adjudicate")
async def adjudicate(
    proposal_id: str,
    body: AdjudicateRequest,
    principal: Principal = Depends(require_module("M2", Access.CONTRIBUTE)),
    c: Container = Depends(container),
) -> dict:
    if not can_adjudicate(principal.role):
        raise Forbidden("Adjudication requires reliability or admin.", {"role": principal.role.value})
    adj = Adjudication(decision=body.decision, approver=principal.subject, note=body.note,
                       corrected=body.corrected, corrected_target_asset_id=body.corrected_target_asset_id,
                       version=body.version)
    return c.resolution.adjudicate(proposal_id, adj, principal.tenant)


@router.post("/v1/resolution/unmerge/{merge_id}")
async def unmerge(
    merge_id: str,
    principal: Principal = Depends(require_module("M2", Access.ACT)),
    c: Container = Depends(container),
) -> dict:
    if not can_unmerge(principal.role):
        raise Forbidden("Unmerge requires admin (higher bar than confirming).",
                        {"role": principal.role.value})
    return c.resolution.unmerge(merge_id, principal.tenant, principal.subject)


@router.get("/v1/resolution/assets/{asset_id}/history")
async def asset_history(
    asset_id: str,
    principal: Principal = Depends(require_module("M2")),
    c: Container = Depends(container),
) -> dict:
    return {"history": c.resolution.asset_history(asset_id, principal.tenant)}
