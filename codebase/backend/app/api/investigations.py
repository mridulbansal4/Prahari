"""M1 Decision Investigation — REST + WebSocket streaming (Bible §7.3–7.4)."""
from __future__ import annotations

import asyncio
import json

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from ..auth.abac import Principal
from ..auth.identity import get_identity_provider
from ..container import Container
from ..domain.errors import InvalidRequest, SentinelError
from .deps import container, current_principal, require_module
from .schemas import InvestigationAccepted, InvestigationRequest

router = APIRouter(tags=["investigations"])


@router.post("/v1/investigations", response_model=InvestigationAccepted, status_code=202)
async def create_investigation(
    body: InvestigationRequest,
    principal: Principal = Depends(require_module("M1")),
    c: Container = Depends(container),
) -> InvestigationAccepted:
    """202 accepted; the answer streams over WS /v1/stream/investigations/{id} (Bible §7.3)."""
    if not body.question.strip():
        raise InvalidRequest("question is required.")
    inv_id = c.investigations.new_id()
    # Stash the request so the WS handler (which authenticates separately) can run it.
    c.stores.relational.put(
        "investigation_request", inv_id,
        {"question": body.question, "as_of": body.as_of.isoformat() if body.as_of else None,
         "context_asset_id": (body.context or {}).get("asset_id"),
         "parent_id": body.parent_investigation_id, "actor": principal.subject},
        principal.tenant,
    )
    return InvestigationAccepted(investigation_id=inv_id)


@router.get("/v1/investigations/{investigation_id}")
async def get_investigation(
    investigation_id: str,
    principal: Principal = Depends(require_module("M1")),
    c: Container = Depends(container),
) -> dict:
    result = c.investigations.get(investigation_id, principal.tenant)
    if result:
        return result.model_dump(mode="json")
    # Not yet run (client may GET before opening the stream) → run synchronously and return.
    req = c.stores.relational.get("investigation_request", investigation_id, principal.tenant)
    if not req:
        raise InvalidRequest("Unknown investigation id.")
    from datetime import date

    async for _ev in c.investigations.run_stream(
        investigation_id, req["question"], principal.tenant, principal.subject,
        as_of=date.fromisoformat(req["as_of"]) if req.get("as_of") else None,
        context_asset_id=req.get("context_asset_id"), parent_id=req.get("parent_id"),
    ):
        pass
    result = c.investigations.get(investigation_id, principal.tenant)
    return result.model_dump(mode="json") if result else {}


@router.get("/v1/investigations")
async def recent(
    principal: Principal = Depends(require_module("M1")),
    c: Container = Depends(container),
) -> dict:
    return {"items": c.investigations.recent(principal.tenant)}


@router.websocket("/v1/stream/investigations/{investigation_id}")
async def stream_investigation(websocket: WebSocket, investigation_id: str) -> None:
    """WS upgrade carries the bearer token as a query param or first message (Bible §2.9)."""
    await websocket.accept()
    c = container()
    token = websocket.query_params.get("token")
    try:
        if not token:
            first = await websocket.receive_text()
            token = json.loads(first).get("token")
        principal: Principal = get_identity_provider().verify(token or "")
    except Exception:
        await websocket.send_json({"type": "error", "error": {"code": "unauthenticated"}})
        await websocket.close()
        return

    req = c.stores.relational.get("investigation_request", investigation_id, principal.tenant)
    if not req:
        await websocket.send_json({"type": "error", "error": {"code": "invalid_request"}})
        await websocket.close()
        return

    from datetime import date

    try:
        async for ev in c.investigations.run_stream(
            investigation_id, req["question"], principal.tenant, principal.subject,
            as_of=date.fromisoformat(req["as_of"]) if req.get("as_of") else None,
            context_asset_id=req.get("context_asset_id"), parent_id=req.get("parent_id"),
        ):
            await websocket.send_json({"type": ev.type, **ev.data})
            await asyncio.sleep(0)  # cooperative yield so tokens render progressively
    except SentinelError as e:
        await websocket.send_json({"type": "error", "error": {"code": e.code, "message": e.message}})
    except WebSocketDisconnect:
        return
    finally:
        try:
            await websocket.close()
        except Exception:
            pass
