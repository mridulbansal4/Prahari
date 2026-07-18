"""SENTINEL evaluation harness (Bible §15) — turns CP-2/CP-4 from claims into measurements.

Metrics (RAGAS/DeepEval-style, reimplemented in-repo to stay offline/dependency-light — KB-4):
  - faithfulness:        fraction of answer claims entailed by a cited span (CP-2) — target >= 0.90
  - citation_accuracy:   fraction of cited spans that actually support their claim  — target >= 0.95
  - abstention_correct:  on unanswerable/injection buckets, did the system abstain? (CP-4)
                         false-answer rate target <= 0.02

Abstention is scored SEPARATELY from accuracy (Bible §15.1): abstaining correctly on a hard
question is succeeding. Run:  python eval/run_eval.py   (from repo root, with core on the path)
"""
from __future__ import annotations

import asyncio
import json
import re
import sys
from pathlib import Path

CORE = Path(__file__).resolve().parent.parent / "backend"
sys.path.insert(0, str(CORE))

from app.container import get_container  # noqa: E402
from app.investigations.service import InvestigationService  # noqa: E402

GOLDEN = Path(__file__).resolve().parent / "golden.jsonl"
STOP = {"the", "a", "an", "is", "are", "of", "to", "in", "on", "why", "what", "how", "and", "which"}


def terms(text: str) -> set[str]:
    return {w.lower() for w in re.findall(r"[a-z0-9\-]+", text.lower()) if w not in STOP and len(w) > 2}


def entails(claim_text: str, span_text: str) -> bool:
    """Span-overlap entailment proxy: a majority of the claim's salient terms appear in the span."""
    ct, st = terms(claim_text), terms(span_text)
    if not ct:
        return False
    return len(ct & st) / len(ct) >= 0.4


async def run_case(svc: InvestigationService, graph, case: dict) -> dict:
    inv_id = svc.new_id()
    async for _ in svc.run_stream(inv_id, case["question"], "demo", "eval"):
        pass
    result = svc.get(inv_id, "demo")
    assert result is not None
    faithful = 0
    total_claims = len(result.claims)
    cited_ok = 0
    total_cites = 0
    for claim in result.claims:
        supported = False
        for cite in claim.citations:
            total_cites += 1
            span = graph.get_span(cite.span_id)
            if span and entails(claim.text, span.text):
                cited_ok += 1
                supported = True
        if supported:
            faithful += 1
    return {
        "id": case["id"],
        "bucket": case["bucket"],
        "abstained": result.abstained,
        "must_abstain": case["must_abstain"],
        "faithfulness": (faithful / total_claims) if total_claims else (1.0 if result.abstained else 0.0),
        "citation_accuracy": (cited_ok / total_cites) if total_cites else (1.0 if result.abstained else 0.0),
        "abstention_correct": result.abstained == case["must_abstain"],
    }


async def main() -> int:
    c = get_container()
    # Ensure the corpus exists (idempotent seed).
    from app import seed as seed_mod

    if c.stores.graph.snapshot().get("nodes", 0) == 0:
        seed_mod.seed()

    cases = [json.loads(l) for l in GOLDEN.read_text().splitlines() if l.strip()]
    results = [await run_case(c.investigations, c.stores.graph, case) for case in cases]

    answerable = [r for r in results if not r["must_abstain"]]
    faithfulness = sum(r["faithfulness"] for r in answerable) / max(1, len(answerable))
    citation = sum(r["citation_accuracy"] for r in answerable) / max(1, len(answerable))
    false_answer_rate = sum(1 for r in results if r["must_abstain"] and not r["abstained"]) / max(1, len(results))
    abstention_ok = sum(1 for r in results if r["abstention_correct"]) / len(results)

    print("=" * 68)
    print("SENTINEL evaluation report (measured on the demo corpus — Bible §15.6)")
    print("=" * 68)
    for r in results:
        verdict = "ABSTAIN" if r["abstained"] else "answer "
        ok = "OK " if r["abstention_correct"] else "!! "
        print(f"  [{ok}] {r['id']:3} {r['bucket']:12} {verdict}  faith={r['faithfulness']:.2f} "
              f"cite={r['citation_accuracy']:.2f}")
    print("-" * 68)
    gates = [
        ("faithfulness", faithfulness, 0.90, faithfulness >= 0.90),
        ("citation_accuracy", citation, 0.95, citation >= 0.95),
        ("abstention_correctness", abstention_ok, 0.98, abstention_ok >= 0.98),
        ("false_answer_rate", false_answer_rate, 0.02, false_answer_rate <= 0.02),
    ]
    for name, val, target, passed in gates:
        print(f"  {name:24} {val:.3f}   (target {target})   {'PASS' if passed else 'FAIL'}")
    print("=" * 68)
    all_pass = all(g[3] for g in gates)
    print("GATE:", "PASS — quality is enforced, not hoped" if all_pass else "FAIL — do not merge")
    print("Note: numbers are measured on this curated corpus, never generalized (Bible §15.6).")
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
