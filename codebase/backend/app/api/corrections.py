"""M8 Correction & Learning Loop (Bible §7.3, CP-10)."""
from __future__ import annotations

from fastapi import APIRouter, Depends

from ..auth.abac import Principal
from ..container import Container
from .deps import container, current_principal
from .schemas import CorrectionRequest

router = APIRouter(tags=["corrections"])


@router.post("/v1/corrections", status_code=201)
async def submit_correction(
    body: CorrectionRequest,
    principal: Principal = Depends(current_principal),  # any signed-in role may submit (BR-7)
    c: Container = Depends(container),
) -> dict:
    corr = c.corrections.submit(
        target_kind=body.target_kind, target_ref=body.target_ref, new_value=body.new_value,
        rationale=body.rationale, author=principal.subject, tenant=principal.tenant,
        prior_value=body.prior_value,
    )
    return {"correction_id": corr.correction_id}


@router.get("/v1/corrections")
async def list_corrections(
    target_ref: str | None = None,
    principal: Principal = Depends(current_principal),
    c: Container = Depends(container),
) -> dict:
    items = (c.corrections.history_for(target_ref, principal.tenant) if target_ref
             else c.corrections.all(principal.tenant))
    return {"corrections": [x.model_dump(mode="json") for x in items]}
