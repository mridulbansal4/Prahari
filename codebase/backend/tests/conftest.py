"""Test fixtures — an isolated store per test session, seeded with the demo corpus."""
from __future__ import annotations

import os
import tempfile
from pathlib import Path

import pytest

# Force a throwaway embedded state dir BEFORE importing the app.
_TMP = Path(tempfile.mkdtemp(prefix="prahari-test-"))
os.environ["PRAHARI_STATE_DIR"] = str(_TMP)
os.environ["PRAHARI_PROFILE"] = "embedded"
# Keep tests deterministic + offline: never use a live model, even if a .env sets one
# (env vars override the .env file in pydantic-settings). Tests exercise the template-synth rung.
os.environ["PRAHARI_GEMINI_API_KEY"] = ""
os.environ["PRAHARI_MODEL_API_KEY"] = ""
os.environ["PRAHARI_FORCE_RUNG"] = ""


@pytest.fixture(scope="session", autouse=True)
def seeded_app():
    from app import seed
    from app.container import get_container

    get_container()  # build container against the throwaway state
    seed.seed()
    yield


@pytest.fixture()
def client():
    from fastapi.testclient import TestClient

    from app.main import app

    return TestClient(app)


def token_for(client, username: str) -> str:
    r = client.post("/v1/auth/login", json={"username": username})
    assert r.status_code == 200, r.text
    return r.json()["token"]


def auth(client, username: str) -> dict:
    return {"Authorization": f"Bearer {token_for(client, username)}"}
