"""The knowledge-graph ontology — aligned to existing standards, not invented (Bible §5.1).

Node labels and edge types are the canonical vocabulary from Bible §5.2–5.3. Reasoning
primitives (§5.7 decision graph) are additive and demo-optional (ADR-015).
"""
from __future__ import annotations

from enum import Enum


class NodeLabel(str, Enum):
    # Core industrial substrate (ISO 14224 / DEXPI aligned)
    ASSET = "Asset"
    IDENTIFIER = "Identifier"
    DOCUMENT = "Document"
    SPAN = "Span"
    WORK_ORDER = "WorkOrder"
    INSPECTION = "Inspection"
    FAILURE_MODE = "FailureMode"
    INCIDENT = "Incident"
    OBLIGATION = "Obligation"
    INSTRUMENT = "Instrument"
    PERSON = "Person"
    SENSOR = "Sensor"
    CONTRADICTION = "Contradiction"
    CORRECTION = "Correction"
    KNOWLEDGE_RISK = "KnowledgeRisk"
    # Reasoning primitives — the decision graph (§5.7, additive)
    OBSERVATION = "Observation"
    HYPOTHESIS = "Hypothesis"
    EVIDENCE = "Evidence"
    DECISION = "Decision"
    ALTERNATIVE = "Alternative"
    RISK_ACCEPTED = "RiskAccepted"
    OUTCOME = "Outcome"
    LESSON_LEARNED = "LessonLearned"


class EdgeType(str, Enum):
    RESOLVED_AS = "RESOLVED_AS"          # Identifier -> Asset  (the moat edge, §5.6)
    PART_OF = "PART_OF"                  # Asset -> Asset
    CONNECTED_TO = "CONNECTED_TO"        # Asset -> Asset (P&ID connectivity)
    HAS_WORKORDER = "HAS_WORKORDER"      # Asset -> WorkOrder
    HAS_INSPECTION = "HAS_INSPECTION"    # Asset -> Inspection
    EXHIBITS = "EXHIBITS"                # Asset -> FailureMode
    EVIDENCED_BY = "EVIDENCED_BY"        # * -> Span  (provenance, CP-1)
    GOVERNS = "GOVERNS"                  # Obligation -> Asset
    DEFINED_IN = "DEFINED_IN"            # Obligation -> Instrument
    SUPERSEDES = "SUPERSEDES"            # Document -> Document / fact version chain (CP-7)
    CONTRADICTS = "CONTRADICTS"          # Span -> Span
    CORRECTED_BY = "CORRECTED_BY"        # * -> Correction (CP-10)
    KNOWS = "KNOWS"                      # Person -> Asset/FailureMode (org memory)
    MONITORS = "MONITORS"               # Sensor -> Asset
    HAS_INCIDENT = "HAS_INCIDENT"        # Asset -> Incident
    LED_TO = "LED_TO"                   # decision-graph ordering (§5.7)


# Nodes that assert a fact about the plant must carry >=1 EVIDENCED_BY span (CP-1, BR-1).
# Structural / provenance nodes are exempt (a Span is itself the evidence; a Correction/Person
# carries its own attribution).
FACT_BEARING: frozenset[NodeLabel] = frozenset(
    {
        NodeLabel.ASSET,
        NodeLabel.WORK_ORDER,
        NodeLabel.INSPECTION,
        NodeLabel.FAILURE_MODE,
        NodeLabel.INCIDENT,
        NodeLabel.OBLIGATION,
        NodeLabel.SENSOR,
        NodeLabel.HYPOTHESIS,
        NodeLabel.EVIDENCE,
    }
)

# Edges whose existence asserts a fact and therefore require provenance (CP-1).
FACT_BEARING_EDGES: frozenset[EdgeType] = frozenset(
    {
        EdgeType.PART_OF,
        EdgeType.CONNECTED_TO,
        EdgeType.HAS_WORKORDER,
        EdgeType.HAS_INSPECTION,
        EdgeType.EXHIBITS,
        EdgeType.GOVERNS,
        EdgeType.HAS_INCIDENT,
        EdgeType.MONITORS,
    }
)
