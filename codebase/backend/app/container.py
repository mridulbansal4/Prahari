"""Composition root — wires ports → adapters → services once per process.

This is the single place concrete adapters are chosen and injected. Everything downstream
depends on the service objects here, never on a concrete store (Bible §12.3 hexagonal).
"""
from __future__ import annotations

from functools import lru_cache

from .actions.service import ActionService
from .agents.model_router import ModelRouter
from .agents.orchestrator import Orchestrator
from .analytics.service import AnalyticsService
from .audit.sink import AuditSink
from .config import Settings, get_settings
from .corrections.service import CorrectionService
from .decisions.replay import DecisionReplayService
from .graph.provenance_sink import ProvenanceSink
from .ingestion.drawings import build_drawing_reader
from .ingestion.ocr import build_ocr
from .ingestion.pipeline import IngestionPipeline
from .investigations.service import InvestigationService
from .knowledge.contradictions import ContradictionDetector
from .knowledge.decay import DecayJob
from .orgmemory.service import OrgMemoryService
from .resolution.service import ResolutionService
from .retrieval.service import RetrievalRouter
from .rules.engine import RuleEngine
from .stores.registry import Stores, build_stores


class Container:
    def __init__(self, settings: Settings | None = None, stores: Stores | None = None) -> None:
        self.settings = settings or get_settings()
        self.stores = stores or build_stores(self.settings)
        s = self.stores

        self.sink = ProvenanceSink(s.graph)
        self.audit = AuditSink(s.relational)
        # vector + sink so captured knowledge becomes a citable, retrievable span;
        # relational so "used in N answers" is counted from real investigations.
        self.org_memory = OrgMemoryService(s.graph, self.audit, vector=s.vector,
                                           relational=s.relational, sink=self.sink)
        self.corrections = CorrectionService(s.graph, s.relational, self.sink, self.audit)
        self.resolution = ResolutionService(s.graph, s.relational, self.sink, self.audit, self.settings)
        # Document-understanding providers. Both default to a null adapter, so a fresh
        # checkout boots with no key, no GPU and no cost; documents they cannot read are
        # quarantined with a reason rather than admitted as garbage.
        self.ocr = build_ocr(self.settings)
        self.drawings = build_drawing_reader(self.settings)

        self.contradictions = ContradictionDetector(s.graph, self.sink, self.audit)
        self.ingestion = IngestionPipeline(s.graph, s.vector, s.relational, self.sink, self.audit,
                                           self.settings, ocr=self.ocr, drawings=self.drawings,
                                           contradictions=self.contradictions)
        self.rules = RuleEngine(s.graph, s.relational)
        self.actions = ActionService(s.relational, self.sink, self.audit)
        self.decay = DecayJob(s.graph, s.relational, self.audit, self.contradictions)
        self.replay = DecisionReplayService(s.graph)
        self.analytics = AnalyticsService(s.relational, self.resolution)

        self.retrieval = RetrievalRouter(s.graph, s.vector, self.settings)
        self.model_router = ModelRouter(self.settings)
        self.orchestrator = Orchestrator(
            retrieval=self.retrieval,
            model_router=self.model_router,
            settings=self.settings,
            who_to_ask=self.org_memory.who_to_ask,
            prior_corrections=self.corrections.prior_corrections_for,
        )
        self.investigations = InvestigationService(
            orchestrator=self.orchestrator, relational=s.relational, audit=self.audit
        )


@lru_cache(maxsize=1)
def get_container() -> Container:
    return Container()


def reset_container() -> None:  # test hook
    get_container.cache_clear()
