"""ABAC fine-grained policy (Bible §8.2). Deny-by-default, evaluated in-service in BOTH profiles.

The write-gating invariant (CP-3) and cross-tenant isolation (§8.1) must hold even in the
hackathon demo — only the *identity source* is stubbed (ADR-P04), never the policy.
"""
from __future__ import annotations

from dataclasses import dataclass

from ..domain.errors import ApprovalRequired, Forbidden
from .rbac import Role


@dataclass
class Principal:
    subject: str
    name: str
    role: Role
    tenant: str
    site: str = "site-a"


def require_tenant_match(principal: Principal, resource_tenant: str) -> None:
    if principal.tenant != resource_tenant:
        raise Forbidden(
            "You don't have access to this site's data.",
            {"reason": "cross_tenant"},
        )


# allow submit WorkOrder if user.role in {technician, reliability}
#                        and approver.role in {reliability, admin}   (Bible §8.2 example policy)
_DRAFTER_ROLES = {Role.TECHNICIAN, Role.RELIABILITY}
_APPROVER_ROLES = {Role.RELIABILITY, Role.ADMIN}


def authorize_work_order_submit(drafter_role: Role, approver: Principal) -> None:
    """CP-3: a system-of-record write needs a distinct-authority approver."""
    if approver.role not in _APPROVER_ROLES:
        raise ApprovalRequired(
            f"Role '{approver.role.value}' may not approve a work-order submission (CP-3).",
            {"required_roles": [r.value for r in _APPROVER_ROLES]},
        )


def can_adjudicate(role: Role) -> bool:
    return role in {Role.RELIABILITY, Role.ADMIN}


def can_unmerge(role: Role) -> bool:
    # Higher bar than confirming — undoing is rarer and higher-blast-radius (PRB §2.3).
    return role == Role.ADMIN
