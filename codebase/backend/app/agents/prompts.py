"""Prompt manifest loader + hashing (Bible §3.7, §4.6; CP-5/CP-7).

Prompts are versioned files; the manifest hash is logged with every answer for reproducibility.
"""
from __future__ import annotations

import hashlib
import json
from functools import lru_cache
from pathlib import Path

_PROMPTS_DIR = Path(__file__).resolve().parent.parent.parent / "prompts"


@lru_cache(maxsize=1)
def manifest() -> dict:
    return json.loads((_PROMPTS_DIR / "manifest.json").read_text(encoding="utf-8"))


@lru_cache(maxsize=8)
def load(agent: str) -> str:
    rel = manifest()["prompts"][agent]
    return (_PROMPTS_DIR / rel).read_text(encoding="utf-8")


@lru_cache(maxsize=1)
def manifest_hash() -> str:
    parts = [json.dumps(manifest(), sort_keys=True)]
    for agent in manifest()["prompts"]:
        parts.append(load(agent))
    return hashlib.sha256("".join(parts).encode()).hexdigest()[:16]
