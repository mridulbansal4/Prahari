"""Runtime configuration and profile selection.

Profiles (ADR-P01):
  - ``embedded``   — default; SQLite/local-vector/in-process/template-synth model. Runs on one
                     box with **no external services, no containers and no API key**. This IS
                     the Bible's air-gap / CP-9 fallback (§8.6), not a mock.
  - ``production`` — Neo4j/Qdrant/Postgres + provider-abstracted LLM (CP-5). Run those three as
                     local installs; nothing here requires Docker.

Document-understanding providers (OCR for scanned text, VLM for drawings) both default to
``none`` so the app boots with zero cost and zero GPU. When a provider is absent the affected
document is quarantined with a stated reason — never silently dropped, never faked.

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
    # Gemini is the primary reasoning provider — a low-cost Flash model keeps token usage
    # down. With a key set it serves the Full CP-9 rung. Without one, the ladder falls to a
    # local open-weights server if reachable, then to template synthesis, which still answers
    # grounded and cited — just structured rather than narrated.
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

    # --- OCR: text out of scanned pages (NOT drawings) -----------------------------
    # "auto" picks Unlimited-OCR when an endpoint is configured, else Paddle when installed,
    # else nothing. Default "none" keeps a fresh checkout free and GPU-less: scanned documents
    # are quarantined with a reason rather than guessed at.
    ocr_provider: Literal["none", "auto", "unlimited", "paddle"] = "none"
    unlimited_ocr_base_url: str | None = None  # OpenAI-compatible vision endpoint (local or hosted)
    unlimited_ocr_model: str = "Unlimited-OCR"
    unlimited_ocr_mode: Literal["gundam", "base"] = "gundam"  # gundam=single page, base=multi
    unlimited_ocr_local: bool = False  # True = in-process transformers (requires CUDA)
    unlimited_ocr_api_key: str | None = None  # Bearer token for a hosted endpoint (e.g. NVIDIA)
    paddle_ocr_lang: str = "en"
    ocr_dpi: int = 300  # PDF page raster resolution handed to the OCR model

    # --- VLM: structured reasoning over engineering DRAWINGS ------------------------
    # This is not OCR. It is asked what the diagram *means* — components, connectivity,
    # ratings — and returns JSON that becomes graph nodes and edges. Default "none":
    # drawings are quarantined rather than have their topology invented.
    vlm_provider: Literal["none", "cosmos", "openai_vision", "local"] = "none"
    nvidia_api_key: str | None = None
    cosmos_base_url: str = "https://integrate.api.nvidia.com/v1"
    # A vision model on NVIDIA's hosted catalog that actually reads a P&ID's tags and
    # connectivity. (The earlier cosmos3-nano-reasoner id returns 404 — it is not published.)
    cosmos_model: str = "nvidia/nemotron-nano-12b-v2-vl"
    vlm_base_url: str | None = None  # any OpenAI-compatible vision endpoint
    vlm_model: str | None = None
    vlm_api_key: str | None = None
    vlm_timeout_s: float = 90.0
    drawing_dpi: int = 200  # raster resolution handed to the VLM

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
