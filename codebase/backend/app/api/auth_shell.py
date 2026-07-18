"""Auth + Global Shell endpoints (PRB §2.1)."""
from __future__ import annotations

from fastapi import APIRouter, Depends

from ..auth.abac import Principal
from ..auth.identity import get_identity_provider
from ..auth.rbac import visible_modules
from .deps import current_principal
from .schemas import LoginRequest, LoginResponse, MeResponse

router = APIRouter(tags=["auth"])


@router.post("/v1/auth/login", response_model=LoginResponse)
def login(body: LoginRequest) -> LoginResponse:
    """Stub SSO for the hackathon profile (ADR-P04): pick a demo persona, get a signed dev JWT."""
    idp = get_identity_provider()
    token = idp.issue(body.username)
    principal = idp.verify(token)
    return LoginResponse(token=token, name=principal.name, role=principal.role.value,
                         tenant=principal.tenant)


@router.get("/v1/auth/me", response_model=MeResponse)
def me(principal: Principal = Depends(current_principal)) -> MeResponse:
    return MeResponse(
        subject=principal.subject, name=principal.name, role=principal.role.value,
        tenant=principal.tenant, site=principal.site,
        # Nav items with no access are hidden entirely, not greyed out (PRB §2.1).
        modules=visible_modules(principal.role),
    )
