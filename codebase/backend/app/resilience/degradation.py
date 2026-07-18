"""The CP-9 degradation ladder (Bible §2.8) — the reason the demo cannot fail.

Each rung is a *product state*, styled and labelled in the UI (PRB §2.1 DegradedBanner), never a
blank screen or a spinner-of-death. The ladder is surfaced, not swallowed.
"""
from __future__ import annotations

from enum import Enum


class Rung(str, Enum):
    FULL = "full"              # graph + vector + model → grounded cited answer
    NO_MODEL = "-model"        # graph + vector, template synthesis → structured, no prose
    NO_VECTOR = "-vector"      # graph traversal only → path + linked docs
    NO_GRAPH = "-graph"        # cached answers + document search only
    NO_EVERYTHING = "-everything"  # "who to ask" from org-memory graph


RUNG_ORDER = [Rung.FULL, Rung.NO_MODEL, Rung.NO_VECTOR, Rung.NO_GRAPH, Rung.NO_EVERYTHING]

BANNER_COPY = {
    Rung.FULL: "",
    Rung.NO_MODEL: "Answers are structured, not narrated — the reasoning model is unavailable.",
    Rung.NO_VECTOR: "Semantic search is unavailable — showing graph-linked results only.",
    Rung.NO_GRAPH: "Showing cached answers and document search only.",
    Rung.NO_EVERYTHING: "Live reasoning is unavailable — showing who to ask.",
}


def worst(a: Rung, b: Rung) -> Rung:
    return a if RUNG_ORDER.index(a) >= RUNG_ORDER.index(b) else b
