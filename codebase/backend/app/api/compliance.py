"""M6 Compliance Intelligence — obligations + coverage (Bible §7.3). Coverage footer mandatory."""
from __future__ import annotations

from fastapi import APIRouter, Depends

from ..auth.abac import Principal
from ..container import Container
from .deps import container, require_module

router = APIRouter(tags=["compliance"])


@router.get("/v1/compliance/assets/{asset_id}")
async def asset_obligations(
    asset_id: str,
    principal: Principal = Depends(require_module("M6")),
    c: Container = Depends(container),
) -> dict:
    rows = c.rules.evaluate_asset(asset_id, principal.tenant)
    c.audit.log(principal.subject, "compliance.viewed", principal.tenant, target=asset_id)
    # The honest coverage footer is part of every compliance response (BR-3/FM-6), never optional.
    return {"rows": [r.model_dump(mode="json") for r in rows],
            "coverage": c.rules.coverage(principal.tenant).model_dump(mode="json")}


@router.get("/v1/compliance/coverage")
async def coverage(
    principal: Principal = Depends(require_module("M6")),
    c: Container = Depends(container),
) -> dict:
    c.audit.log(principal.subject, "compliance.coverage_viewed", principal.tenant)
    return c.rules.coverage(principal.tenant).model_dump(mode="json")
