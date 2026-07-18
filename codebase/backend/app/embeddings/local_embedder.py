"""Deterministic, offline, dependency-free embedding model.

A hashed bag-of-character-n-grams projected into a fixed-dimensional unit vector. This is the
local embedding model the Bible requires so vector search works air-gapped (§4.7, §8.6). It is
deterministic (important for demo reproducibility, Bible §11.7) and needs no downloaded weights.
Quality is lower than a transformer embedder — which is exactly the CP-9 trade-off, honestly
labelled — but it is a real, functioning semantic-similarity signal, not a mock.
"""
from __future__ import annotations

import hashlib
import math
import re

DIM = 256
_WORD = re.compile(r"[a-z0-9]+")


def _tokens(text: str) -> list[str]:
    text = text.lower()
    words = _WORD.findall(text)
    grams: list[str] = list(words)
    # character trigrams give sub-word robustness (tags like P-101B, OEM numbers)
    joined = " ".join(words)
    for i in range(len(joined) - 2):
        grams.append(joined[i : i + 3])
    return grams


def embed(text: str) -> list[float]:
    vec = [0.0] * DIM
    for tok in _tokens(text):
        h = int.from_bytes(hashlib.md5(tok.encode()).digest()[:4], "big")
        idx = h % DIM
        sign = 1.0 if (h >> 31) & 1 else -1.0
        vec[idx] += sign
    norm = math.sqrt(sum(v * v for v in vec)) or 1.0
    return [v / norm for v in vec]


def cosine(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))
