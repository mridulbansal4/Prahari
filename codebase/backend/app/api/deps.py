"""API dependencies — the in-service half of the gateway contract (Bible §2.9, §7.2).

The thin gateway (authn/z pre-check, rate-limit, correlation id) is expressed here as FastAPI
dependencies. Fine-grained ABAC runs in the services (deny-by-default), never only at the edge.
"""
from __future__ import annotations

from fastapi import Depends, Header

from ..auth.abac import Principal
from ..auth.identity import get_identity_provider
from ..auth.rbac import Access, access_for, can_view
from ..container import Container, get_container
from ..domain.errors import Forbidden, Unauthenticated


def container() -> Container:
    return get_container()


async def current_principal(authorization: str | None = Header(default=None)) -> Principal:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise Unauthenticated("Missing bearer token.")
    token = authorization.split(" ", 1)[1].strip()
    return get_identity_provider().verify(token)


def require_module(module: str, min_access: Access = Access.VIEW):
    """Coarse RBAC pre-check for a module (PRB §1.4 matrix)."""

    async def _dep(principal: Principal = Depends(current_principal)) -> Principal:
        if not can_view(module, principal.role):
            raise Forbidden(f"No access to {module}.", {"module": module, "role": principal.role.value})
        acc = access_for(module, principal.role)
        _order = [Access.NONE, Access.VIEW, Access.CONTRIBUTE, Access.ACT, Access.FULL, Access.ADMINISTER]
        if _order.index(acc) < _order.index(min_access):
            raise Forbidden(
                f"Requires {min_access.value} on {module}; you have {acc.value}.",
                {"module": module},
            )
        return principal

    return _dep
