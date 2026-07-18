# 15 — Evaluation

> The harness that turns CP-2/CP-4 from claims into measurements. RAGAS + DeepEval + a golden set + citation/abstention/graph accuracy. This is the volume that discharges the Vol 1 promise "prove the abstention claim with an eval harness, not an assertion."

## 15.1 What we measure (and why each matters)

| Metric | Definition | Target `[D]` | Why it matters |
|---|---|---|---|
| **Faithfulness** (RAGAS) | fraction of answer claims entailed by retrieved context | ≥ 0.90 | no ungrounded prose (CP-2) |
| **Answer relevance** (RAGAS) | answer addresses the question | ≥ 0.85 | not evasive |
| **Context precision/recall** (RAGAS) | retrieved context is on-point / complete | ≥ 0.80 | router quality (`03`) |
| **Citation accuracy** | fraction of cited spans that actually support their claim | ≥ 0.95 | the credibility moat (NFR-6) |
| **Abstention correctness** | on unanswerable/ungrounded queries, system abstains | false-answer rate ≤ 2% | the safety claim (CP-4, Principle 5) |
| **Graph/resolution accuracy** | correct `RESOLVED_AS` decisions vs adjudicated truth | precision-first | FM-1 defence |
| **Retrieval latency** | P50/P95 of retrieve stage | see NFR-1 | UX |

**Design point:** abstention is scored **separately** from accuracy. A system that abstains correctly on a hard query is *succeeding*, and a benchmark that lumps the two hides that.

## 15.2 Golden dataset

- **Composition:** curated Q→(expected answer, expected cited spans, expected abstain?) triples over the provenance-clean corpus (`11`, ADR-012).
- **Buckets:** (a) single-fact, (b) multi-hop causal, (c) compliance/obligation, (d) *deliberately unanswerable* (must abstain), (e) *injection* (must ignore instruction).
- **Growth:** every human correction (CP-10) adds a labelled example → the regression suite grows with use. The eval set is a living asset, like the resolution corpus.

## 15.3 Harness

```
eval/
├─ golden.jsonl                 # Q, expected_answer, expected_spans, must_abstain, tenant
├─ run_ragas.py                 # faithfulness, relevance, ctx precision/recall
├─ run_deepeval.py              # assertion-style checks + custom metrics
├─ citation_accuracy.py         # cited span → claim entailment check
├─ abstention.py                # unanswerable/injection buckets
├─ graph_accuracy.py            # RESOLVED_AS decisions vs truth
└─ report.py                    # writes dashboard + CI gate verdict
```

- Runs against **≥2 model families** (CP-5) to prove no prompt binds to one vendor.
- `eval-smoke` (subset) runs on every PR; `eval-full` nightly and pre-deploy.

## 15.4 CI gates (from `12`/`09`)

A change cannot merge/deploy if any of: faithfulness < 0.90, citation accuracy < 0.95, abstention false-answer rate > 2%, or graph precision regresses beyond tolerance. **Quality is a gate, not a report** (ADR-014).

## 15.5 Regression testing

- Every fixed bug and every human correction becomes a golden-set case.
- Nightly full run diffed against the last green baseline; regressions alert (`09`).
- Demo-path determinism asserted (the scripted questions must stay green).

## 15.6 Benchmarks to report to judges

- Faithfulness/citation on the golden set (a real number, labelled `[V]`-of-our-measurement on our corpus, not a claim about the world).
- Abstention correctness on the unanswerable bucket — *the* differentiating number.
- Latency P50/P95 on the investigation path.
- Resolution precision on the adjudicated set.

**Honesty rule:** these numbers are measured on our curated corpus and are reported as such — never generalised to "Prahari is X% accurate on all industrial data." Overclaiming here is exactly the credibility landmine the evidence tiers exist to avoid.

## 15.7 What we explicitly do *not* claim

- We do not claim completeness of compliance coverage (FM-6).
- We do not claim the resolution corpus is complete or that the graph is exhaustive.
- We do not report a single-point ROI without sensitivity (that lives in `16`, and is `[D]`).

---

**Red Devil:** *Chollet:* "Separating abstention from accuracy is the correct evaluation design; most RAG demos conflate them. Running across two model families proves CP-5. **APPROVED.**"
**Hackathon Winning:** *Behavioural Psychologist:* "The abstention-correctness number, honestly scoped, is the single most credibility-generating figure you can show. **Strong Winner.**"
**Black Swan:** two-model eval → a model deprecation doesn't invalidate the product. **Survivable.**
**Green:** cache + compression measured; wasted inference visible and reducible. **Positive.**
