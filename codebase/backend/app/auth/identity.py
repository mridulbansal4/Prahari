"""Identity providers (ADR-P04).

StubIdentityProvider — signed dev JWT, role chosen at login, single tenant. Used in the
embedded/hackathon profile. OidcIdentityProvider — validates a customer IdP token
(signature/audience/expiry). The ABAC policy (abac.py) runs identically for both.
"""
from __future__ import annotations

import time

import jwt

from ..config import get_settings
from ..domain.errors import Unauthenticated
from .abac import Principal
from .rbac import Role

_DEV_SECRET = "sentinel-dev-signing-key"  # dev only; production uses IdP JWKS (never a secret in code)

# Canonical demo personas (PRB §1.2) available in the stub login.
DEMO_USERS = {
    "ravi": {"name": "Ravi", "role": Role.TECHNICIAN},
    "meera": {"name": "Meera", "role": Role.RELIABILITY},
    "deepak": {"name": "Deepak", "role": Role.ADMIN},
    "anil": {"name": "Anil", "role": Role.RELIABILITY},
    "auditor": {"name": "Auditor", "role": Role.AUDITOR},
    "compliance": {"name": "Compliance Officer", "role": Role.COMPLIANCE},
}


class StubIdentityProvider:
    def issue(self, username: str) -> str:
        u = DEMO_USERS.get(username.lower())
        if not u:
            raise Unauthenticated(f"Unknown demo user '{username}'.")
        payload = {
            "sub": username.lower(),
            "name": u["name"],
            "role": u["role"].value,
            "tenant": get_settings().tenant_default,
            "site": "site-a",
            "iat": int(time.time()),
            "exp": int(time.time()) + 3600 * 8,
        }
        return jwt.encode(payload, _DEV_SECRET, algorithm="HS256")

    def verify(self, token: str) -> Principal:
        try:
            payload = jwt.decode(token, _DEV_SECRET, algorithms=["HS256"])
        except jwt.PyJWTError as e:
            raise Unauthenticated("Invalid or expired token.", {"reason": str(e)})
        return Principal(
            subject=payload["sub"],
            name=payload["name"],
            role=Role(payload["role"]),
            tenant=payload["tenant"],
            site=payload.get("site", "site-a"),
        )


class OidcIdentityProvider:  # pragma: no cover - exercised in production profile
    """Validates a customer IdP token. JWKS fetch omitted here; wired in production deploy."""

    def verify(self, token: str) -> Principal:
        raise Unauthenticated("OIDC provider not configured in this build (see ADR-P04).")


def get_identity_provider() -> StubIdentityProvider:
    return StubIdentityProvider()
