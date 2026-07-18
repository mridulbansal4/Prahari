"""Agent Orchestrator (M1, Bible §4.1) — the bounded, role-specialised state machine.

    plan → retrieve → draft → critic → verify → (answer | abstain | correct)

Only Planner→Retriever→Executor→Critic→Verifier are on the live answer path (Bible §4.1.1);
supervisor logic lives here, not as a separate hallucinating agent. The Verifier gate (CP-2)
strips uncited claims and abstains (CP-4) below the grounding threshold — abstention is a
first-class success, not an error. Streams events for the live traversal (Bible §7.4).
"""
from __future__ import annotations

from collections.abc import AsyncIterator
from dataclasses import dataclass
from datetime import date
from typing import Any, Callable

from ..config import Settings
from ..domain.models import (
    Citation,
    Claim,
    ConfidenceState,
    InvestigationResult,
    Span,
    WhoToAsk,
)
from ..retrieval.context import AssembledContext
from ..retrieval.service import RetrievalRouter
from ..resilience.degradation import BANNER_COPY, Rung, worst
from .model_router import ModelRouter
from .prompts import load, manifest_hash


@dataclass
class Event:
    type: str  # stage | token | claim | graph_hop | verdict | abstain | done | banner
    data: dict[str, Any]


# Callables injected to avoid circular deps.
WhoToAskFn = Callable[[list[str], str], list[WhoToAsk]]
PriorCorrectionsFn = Callable[[str, str], list[str]]


class Orchestrator:
    def __init__(
        self,
        retrieval: RetrievalRouter,
        model_router: ModelRouter,
        settings: Settings,
        who_to_ask: WhoToAskFn,
        prior_corrections: PriorCorrectionsFn,
    ) -> None:
        self._r = retrieval
        self._models = model_router
        self._s = settings
        self._who_to_ask = who_to_ask
        self._prior_corrections = prior_corrections

    async def run(
        self,
        investigation_id: str,
        question: str,
        tenant: str,
        as_of: date | None = None,
        context_asset_id: str | None = None,
        parent_id: str | None = None,
    ) -> AsyncIterator[Event]:
        provider, rung = self._models.select()

        # Rung governs which retrieval modalities are available (CP-9 ladder).
        vector_enabled = rung not in (Rung.NO_VECTOR, Rung.NO_GRAPH, Rung.NO_EVERYTHING)
        graph_enabled = rung not in (Rung.NO_GRAPH, Rung.NO_EVERYTHING)

        yield Event("banner", {"rung": rung.value, "copy": BANNER_COPY.get(rung, "")})

        # --- PLAN ---
        yield Event("stage", {"stage": "Planner", "detail": "Decomposing the question"})

        # --- RETRIEVE ---
        yield Event("stage", {"stage": "Retriever", "detail": "Traversing the decision graph"})
        ctx, route = self._r.retrieve(
            question, tenant, as_of=as_of, context_asset_id=context_asset_id,
            vector_enabled=vector_enabled, graph_enabled=graph_enabled,
        )
        # Prior corrections become part of the context (org memory / CP-10 self-correction).
        ctx.prior_corrections = self._prior_corrections(question, tenant)
        for hop in ctx.graph_path:
            yield Event("graph_hop", {"hop": hop.model_dump()})

        # --- lowest rung: no live reasoning, only who-to-ask ---
        if rung == Rung.NO_EVERYTHING or (not ctx.spans and not graph_enabled):
            result = self._abstain(investigation_id, question, ctx, rung, provider,
                                   as_of, parent_id, reason="Live reasoning is unavailable.")
            yield Event("abstain", {"result": result.model_dump(mode="json")})
            yield Event("verdict", {"abstained": True})
            yield Event("done", {"result": result.model_dump(mode="json")})
            return

        # --- DRAFT (Executor) ---
        yield Event("stage", {"stage": "Executor", "detail": "Drafting the grounded hypothesis"})
        prompt = self._build_prompt(question, ctx)
        try:
            raw = provider.synthesize(prompt, ctx.as_provider_spans())
            self._models.record_success()
        except Exception:
            self._models.record_failure()
            provider = self._models._template  # explicit fallback to -model rung
            rung = worst(rung, Rung.NO_MODEL)
            yield Event("banner", {"rung": rung.value, "copy": BANNER_COPY.get(rung, "")})
            raw = provider.synthesize(prompt, ctx.as_provider_spans())

        draft_claims = raw.get("claims", [])

        # --- CRITIC: check each claim's citations exist in the assembled context ---
        yield Event("stage", {"stage": "Critic", "detail": "Challenging each claim"})
        valid_span_ids = {s.span_id for s in ctx.spans}
        span_by_id = {s.span_id: s for s in ctx.spans}

        # --- VERIFIER: enforce CP-2 (strip uncited) and decide answer vs abstain (CP-4) ---
        yield Event("stage", {"stage": "Verifier", "detail": "Enforcing the grounding contract"})
        verified: list[Claim] = []
        for c in draft_claims:
            cited = [sid for sid in c.get("citations", []) if sid in valid_span_ids]
            if not cited:
                continue  # strip uncited claim (CP-2)
            verified.append(
                Claim(
                    text=c["text"],
                    confidence=ConfidenceState(c.get("confidence", "grounded"))
                    if c.get("confidence") in {s.value for s in ConfidenceState}
                    else ConfidenceState.GROUNDED,
                    citations=[
                        Citation(doc_id=span_by_id[sid].doc_id, page=span_by_id[sid].page,
                                 span_id=sid, excerpt=_excerpt(span_by_id[sid]))
                        for sid in cited
                    ],
                )
            )

        grounding = len(verified) / max(1, len(draft_claims)) if draft_claims else 0.0
        must_abstain = raw.get("abstained", False) or not verified or grounding < self._s.grounding_threshold

        if must_abstain:
            result = self._abstain(investigation_id, question, ctx, rung, provider, as_of,
                                   parent_id, reason="Could not sufficiently ground the answer.",
                                   unresolved=raw.get("unresolved", []))
            for hop in ctx.graph_path:
                pass
            yield Event("abstain", {"result": result.model_dump(mode="json")})
            yield Event("verdict", {"abstained": True})
            yield Event("done", {"result": result.model_dump(mode="json")})
            return

        # --- ANSWER ---
        answer_text = raw.get("answer") or " ".join(c.text for c in verified)
        for tok in _tokenize_stream(answer_text):
            yield Event("token", {"text": tok})
        for c in verified:
            yield Event("claim", {"claim": c.model_dump()})

        result = InvestigationResult(
            investigation_id=investigation_id,
            question=question,
            as_of=as_of,
            abstained=False,
            answer=answer_text,
            claims=verified,
            graph_path=ctx.graph_path,
            unresolved=raw.get("unresolved", []),
            degradation_level=rung.value,
            prompt_manifest_hash=manifest_hash(),
            model_id=getattr(provider, "id", "unknown"),
            context_span_ids=[s.span_id for s in ctx.spans],
            parent_investigation_id=parent_id,
        )
        yield Event("verdict", {"abstained": False})
        yield Event("done", {"result": result.model_dump(mode="json")})

    # --------------------------------------------------------------------------- abstain
    def _abstain(
        self,
        investigation_id: str,
        question: str,
        ctx: AssembledContext,
        rung: Rung,
        provider: object,
        as_of: date | None,
        parent_id: str | None,
        reason: str,
        unresolved: list[str] | None = None,
    ) -> InvestigationResult:
        anchor_ids = [a.id for a in ctx.anchors]
        who = self._who_to_ask(anchor_ids, ctx.question) if anchor_ids else self._who_to_ask([], question)
        known = [f"{card.title} ({card.label})" for card in ctx.entity_cards[:5]]
        return InvestigationResult(
            investigation_id=investigation_id,
            question=question,
            as_of=as_of,
            abstained=True,
            # Carry "what I do know" as context (CP-4 contract: known / missing / who-to-ask).
            answer=("Known context: " + "; ".join(known)) if known else "",
            claims=[],
            graph_path=ctx.graph_path,
            unresolved=(unresolved or []) + [reason],
            who_to_ask=who,
            degradation_level=rung.value,
            prompt_manifest_hash=manifest_hash(),
            model_id=getattr(provider, "id", "unknown"),
            context_span_ids=[s.span_id for s in ctx.spans],
            parent_investigation_id=parent_id,
        )

    # --------------------------------------------------------------------------- prompt
    def _build_prompt(self, question: str, ctx: AssembledContext) -> str:
        contract = load("executor")
        cards = "\n".join(f"- {c.title} [{c.label}]: {'; '.join(c.facts)}" for c in ctx.entity_cards)
        corrections = "\n".join(f"- {c}" for c in ctx.prior_corrections)
        return (
            f"{contract}\n\n<question>{question}</question>\n"
            f"<entity_cards>\n{cards}\n</entity_cards>\n"
            f"<prior_corrections>\n{corrections}\n</prior_corrections>\n"
            f"<as_of>{ctx.as_of or 'now'}</as_of>"
        )


def _excerpt(span: Span) -> str:
    t = span.text.strip()
    return t if len(t) <= 160 else t[:157] + "…"


def _tokenize_stream(text: str) -> list[str]:
    # Word-level "streaming" chunks for the WS token events (Bible §7.4).
    words = text.split(" ")
    return [w + " " for w in words]
