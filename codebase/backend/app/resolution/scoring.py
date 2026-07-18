"""Entity-resolution scoring (Bible §3.2).

A weighted feature vector → calibrated probability. Features: tag-pattern match, fuzzy string
(Jaro-Winkler), shared work-order history, functional-role match (ISO 14224 class), embedding
similarity of surrounding context. Deterministic and explainable (the score is auditable).
"""
from __future__ import annotations

import re

from ..embeddings.local_embedder import cosine, embed

_NORM = re.compile(r"[^a-z0-9]")


def normalize_tag(value: str) -> str:
    return _NORM.sub("", value.lower())


def jaro_winkler(s1: str, s2: str) -> float:
    if s1 == s2:
        return 1.0
    if not s1 or not s2:
        return 0.0
    match_dist = max(len(s1), len(s2)) // 2 - 1
    s1_matches = [False] * len(s1)
    s2_matches = [False] * len(s2)
    matches = 0
    for i, c1 in enumerate(s1):
        lo = max(0, i - match_dist)
        hi = min(i + match_dist + 1, len(s2))
        for j in range(lo, hi):
            if not s2_matches[j] and s1[i] == s2[j]:
                s1_matches[i] = s2_matches[j] = True
                matches += 1
                break
    if matches == 0:
        return 0.0
    trans = 0
    k = 0
    for i in range(len(s1)):
        if s1_matches[i]:
            while not s2_matches[k]:
                k += 1
            if s1[i] != s2[k]:
                trans += 1
            k += 1
    trans //= 2
    jaro = (matches / len(s1) + matches / len(s2) + (matches - trans) / matches) / 3
    prefix = 0
    for c1, c2 in zip(s1, s2):
        if c1 == c2:
            prefix += 1
        else:
            break
        if prefix == 4:
            break
    return jaro + prefix * 0.1 * (1 - jaro)


_WEIGHTS = {
    "tag_pattern": 0.30,
    "fuzzy": 0.20,
    "iso_class": 0.20,
    "wo_history": 0.15,
    "embedding": 0.15,
}


def score_pair(
    a_value: str,
    b_value: str,
    a_iso: str | None,
    b_iso: str | None,
    a_context: str,
    b_context: str,
    shared_wo: bool,
) -> tuple[float, dict[str, float]]:
    na, nb = normalize_tag(a_value), normalize_tag(b_value)
    features = {
        "tag_pattern": 1.0 if na == nb else (0.6 if (na in nb or nb in na) else 0.0),
        "fuzzy": jaro_winkler(na, nb),
        "iso_class": 1.0 if (a_iso and a_iso == b_iso) else 0.0,
        "wo_history": 1.0 if shared_wo else 0.0,
        "embedding": max(0.0, cosine(embed(a_context), embed(b_context))),
    }
    score = sum(_WEIGHTS[k] * v for k, v in features.items())
    return round(min(1.0, score), 4), {k: round(v, 3) for k, v in features.items()}
