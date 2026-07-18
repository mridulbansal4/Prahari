"""Query classification (Bible §3.3.1, §4.3).

Deliberately cheap and explainable — rules first, so the routing decision itself is auditable
and never a black box (Bible §4.3).
"""
from __future__ import annotations

import re
from enum import Enum


class Route(str, Enum):
    VECTOR = "vector"            # single-fact / definitional
    GRAPH_FIRST = "graph_first"  # multi-hop / causal / relational
    COMPLIANCE = "compliance"    # obligation / overdue
    HYBRID = "hybrid"            # ambiguous → both, reranked


_CAUSAL = re.compile(r"\b(why|cause|because|root|running hot|failing|trip|hot|vibrat)\b", re.I)
_COMPLIANCE = re.compile(r"\b(oisd|peso|dgms|cpcb|obligation|overdue|inspection due|complian)\b", re.I)
_DEFINITIONAL = re.compile(r"\b(what is|design pressure|rated|spec|definition of|value of)\b", re.I)


def classify(question: str) -> Route:
    if _COMPLIANCE.search(question):
        return Route.COMPLIANCE
    if _CAUSAL.search(question):
        return Route.GRAPH_FIRST
    if _DEFINITIONAL.search(question):
        return Route.VECTOR
    return Route.HYBRID
