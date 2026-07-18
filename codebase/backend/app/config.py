"""Runtime configuration and profile selection.

Profiles (ADR-P01):
  - ``embedded``   — default; NetworkX/SQLite/local-vector/in-process cache/template-synth
                     model. Runs on one box with no external services and no API key. This IS
                     the Bible's air-gap / CP-9 fallback (§8.6), not a mock.
  - ``production`` — Neo4j/Qdrant/Postgres/Redis + provider-abstracted LLM (CP-5). Wired via
                     docker-compose.

No secret, statute, or tenant value is hardcoded (CP-5/CP-6): everything comes from env with a
``PRAHARI_`` prefix (Bible §12.2 naming law).
"""
from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

Profile = Literal["embedded", "production"]

_CORE_DIR = Path(__file__).resolve().parent.parent  # .../core


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="PRAHARI_", env_file=".env", extra="ignore")

    profile: Profile = "embedded"
    tenant_default: str = "demo"

    # Embedded profile state (durable across `seed` and `uvicorn` processes).
    state_dir: Path = _CORE_DIR / ".prahari_state"

    # --- Production store coordinates (unused in embedded profile) -----------------
    graph_uri: str = "bolt://localhost:7687"
    graph_user: str = "neo4j"
    graph_password: str = "sentinel-dev"
    vector_url: str = "http://localhost:6333"
    pg_dsn: str = "postgresql://sentinel:sentinel-dev@localhost:5432/sentinel"
    redis_url: str = "redis://localhost:6379/0"

    # --- Auth (stub dev provider, ADR-P04) -----------------------------------------
    # Configurable so no signing secret is a code literal (CP-5 / §8.3). Production uses the
    # customer IdP's JWKS instead of this symmetric dev key.
    auth_dev_secret: str = "prahari-dev-signing-key"

    # --- OIDC (production identity, Bible §7.2/§8.2) --------------------------------
    # When ``oidc_jwks_uri`` is set, the gateway validates real IdP tokens (RS256, signature +
    # audience + issuer + expiry) instead of the dev stub. Deny-by-default ABAC still runs.
    oidc_jwks_uri: str | None = None
    oidc_issuer: str | None = None
    oidc_audience: str | None = None
    oidc_role_claim: str = "role"

    # --- Model provider (CP-5) -----------------------------------------------------
    # If a key is present we may use the cloud reasoning provider; otherwise the local /
    # template-synth rungs of the CP-9 ladder serve grounded, structured answers offline.
    model_api_key: str | None = None
    model_id: str = "claude-fable-5"
    model_base_url: str = "https://api.anthropic.com"

    # Gemini provider (CP-5) — a low-cost Flash model keeps token usage down. When a key is set
    # this is the preferred Full-rung reasoning model. Model id is configurable.
    gemini_api_key: str | None = None
    gemini_model: str = "gemini-flash-lite-latest"  # lowest-cost tier (fewest tokens)
    gemini_base_url: str = "https://generativelanguage.googleapis.com"
    # Token budget for the model response — deliberately small (cheap, fast).
    model_max_output_tokens: int = 768

    # Force the degradation rung for demos of the CP-9 ladder / air-gap mode.
    # One of: full | -model | -vector | -graph | -everything
    force_rung: str | None = None

    # --- Confidence gating thresholds (Bible §3.1.3) -------------------------------
    confidence_auto_write: float = 0.85
    confidence_provisional: float = 0.60

    # --- Grounding / abstention (Bible §15.1, NFR-5..7) ---------------------------
    grounding_threshold: float = 0.60  # below this the Verifier abstains (CP-4)

    # --- Retrieval bounds (Bible §5.9) --------------------------------------------
    max_hops: int = 3
    retrieval_k: int = 8
    context_span_budget: int = 24

    @property
    def state_path(self) -> Path:
        self.state_dir.mkdir(parents=True, exist_ok=True)
        return self.state_dir


_settings: Settings | None = None


def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
