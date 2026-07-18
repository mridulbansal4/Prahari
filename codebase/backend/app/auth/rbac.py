"""RBAC roles and the product-module access matrix (PRB §1.4).

RBAC roles are defined technically in Bible §8.2; this module is the single place mapping roles
to product modules and access levels, exactly as PRB §1.4 mandates.
"""
from __future__ import annotations

from enum import Enum


class Role(str, Enum):
    TECHNICIAN = "technician"
    RELIABILITY = "reliability"
    COMPLIANCE = "compliance"
    ADMIN = "admin"
    AUDITOR = "auditor"


class Access(str, Enum):
    NONE = "none"
    VIEW = "view"
    CONTRIBUTE = "contribute"  # propose / draft / submit
    ACT = "act"                # adjudicate / approve
    FULL = "full"
    ADMINISTER = "administer"


# Module → {role: access}. Mirrors the PRB §1.4 table verbatim.
MATRIX: dict[str, dict[Role, Access]] = {
    "M1": {Role.TECHNICIAN: Access.FULL, Role.RELIABILITY: Access.FULL, Role.COMPLIANCE: Access.VIEW, Role.ADMIN: Access.FULL, Role.AUDITOR: Access.VIEW},
    "M2": {Role.TECHNICIAN: Access.CONTRIBUTE, Role.RELIABILITY: Access.ACT, Role.COMPLIANCE: Access.VIEW, Role.ADMIN: Access.ACT, Role.AUDITOR: Access.VIEW},
    "M3": {Role.TECHNICIAN: Access.VIEW, Role.RELIABILITY: Access.FULL, Role.COMPLIANCE: Access.VIEW, Role.ADMIN: Access.FULL, Role.AUDITOR: Access.VIEW},
    "M4": {Role.TECHNICIAN: Access.VIEW, Role.RELIABILITY: Access.FULL, Role.COMPLIANCE: Access.VIEW, Role.ADMIN: Access.FULL, Role.AUDITOR: Access.VIEW},
    "M5": {Role.TECHNICIAN: Access.CONTRIBUTE, Role.RELIABILITY: Access.FULL, Role.COMPLIANCE: Access.VIEW, Role.ADMIN: Access.FULL, Role.AUDITOR: Access.VIEW},
    "M6": {Role.TECHNICIAN: Access.VIEW, Role.RELIABILITY: Access.FULL, Role.COMPLIANCE: Access.FULL, Role.ADMIN: Access.FULL, Role.AUDITOR: Access.VIEW},
    "M7": {Role.TECHNICIAN: Access.CONTRIBUTE, Role.RELIABILITY: Access.ACT, Role.COMPLIANCE: Access.VIEW, Role.ADMIN: Access.ACT, Role.AUDITOR: Access.VIEW},
    "M8": {Role.TECHNICIAN: Access.CONTRIBUTE, Role.RELIABILITY: Access.FULL, Role.COMPLIANCE: Access.CONTRIBUTE, Role.ADMIN: Access.FULL, Role.AUDITOR: Access.VIEW},
    "M9": {Role.TECHNICIAN: Access.VIEW, Role.RELIABILITY: Access.VIEW, Role.COMPLIANCE: Access.VIEW, Role.ADMIN: Access.FULL, Role.AUDITOR: Access.FULL},
    "M10": {Role.TECHNICIAN: Access.VIEW, Role.RELIABILITY: Access.FULL, Role.COMPLIANCE: Access.FULL, Role.ADMIN: Access.FULL, Role.AUDITOR: Access.VIEW},
    "M11": {Role.TECHNICIAN: Access.NONE, Role.RELIABILITY: Access.CONTRIBUTE, Role.COMPLIANCE: Access.CONTRIBUTE, Role.ADMIN: Access.ADMINISTER, Role.AUDITOR: Access.VIEW},
}


def access_for(module: str, role: Role) -> Access:
    return MATRIX.get(module, {}).get(role, Access.NONE)


def can_view(module: str, role: Role) -> bool:
    return access_for(module, role) != Access.NONE


def visible_modules(role: Role) -> list[str]:
    return [m for m in MATRIX if can_view(m, role)]
