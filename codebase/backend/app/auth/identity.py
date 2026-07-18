"""Identity providers (ADR-P04).

StubIdentityProvider — signed dev JWT, role chosen at login, single tenant. Used in the
embedded/hackathon profile. OidcIdentityProvider — validates a customer IdP token
(signature/audience/expiry). The ABAC policy (abac.py) runs identically for both.
"""
from __future__ import annotations

import json
import time
from typing import Any

import jwt

from ..config import Settings, get_settings
from ..domain.errors import Unauthenticated
from .abac import Principal
from .rbac import Role

def _dev_secret() -> str:
    # Read from config, not a code literal; production uses IdP JWKS (§8.3).
    return get_settings().auth_dev_secret


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
        return jwt.encode(payload, _dev_secret(), algorithm="HS256")

    def verify(self, token: str) -> Principal:
        try:
            payload = jwt.decode(token, _dev_secret(), algorithms=["HS256"])
        except jwt.PyJWTError as e:
            raise Unauthenticated("Invalid or expired token.", {"reason": str(e)})
        return Principal(
            subject=payload["sub"],
            name=payload["name"],
            role=Role(payload["role"]),
            tenant=payload["tenant"],
            site=payload.get("site", "site-a"),
        )


class OidcIdentityProvider:
    """Validates a real customer-IdP token (Bible §7.2/§8.2): RS256 signature via the IdP's JWKS,
    plus audience/issuer/expiry. Maps IdP claims → Principal; role comes from a configurable claim.
    ``jwks`` may be injected (offline/tests); otherwise keys are fetched from ``oidc_jwks_uri``."""

    def __init__(self, settings: Settings | None = None, jwks: list[dict[str, Any]] | None = None) -> None:
        self._s = settings or get_settings()
        self._jwks = jwks

    def _signing_key(self, token: str) -> Any:
        header = jwt.get_unverified_header(token)
        kid = header.get("kid")
        if self._jwks is not None:
            jwk = next((k for k in self._jwks if k.get("kid") == kid), self._jwks[0])
            return jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))
        if not self._s.oidc_jwks_uri:
            raise Unauthenticated("OIDC is not configured (set PRAHARI_OIDC_JWKS_URI).")
        client = jwt.PyJWKClient(self._s.oidc_jwks_uri)
        return client.get_signing_key_from_jwt(token).key

    def verify(self, token: str) -> Principal:
        try:
            key = self._signing_key(token)
            claims = jwt.decode(
                token, key, algorithms=["RS256"],
                audience=self._s.oidc_audience, issuer=self._s.oidc_issuer,
                options={"verify_aud": bool(self._s.oidc_audience),
                         "verify_iss": bool(self._s.oidc_issuer)},
            )
        except jwt.PyJWTError as e:
            raise Unauthenticated("Invalid IdP token.", {"reason": str(e)})
        role_raw = claims.get(self._s.oidc_role_claim, Role.TECHNICIAN.value)
        try:
            role = Role(role_raw)
        except ValueError:
            raise Unauthenticated(f"Unknown role claim '{role_raw}'.")
        return Principal(
            subject=claims["sub"],
            name=claims.get("name", claims["sub"]),
            role=role,
            tenant=claims.get("tenant", self._s.tenant_default),
            site=claims.get("site", "site-a"),
        )


def get_identity_provider() -> StubIdentityProvider | OidcIdentityProvider:
    """Pick the identity provider by config: real OIDC when a JWKS URI is set, else the dev stub."""
    settings = get_settings()
    if settings.oidc_jwks_uri:
        return OidcIdentityProvider(settings)
    return StubIdentityProvider()
