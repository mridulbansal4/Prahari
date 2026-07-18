# Implementation Status

Per PRB §8.3, each Part-2 module tracks UI / Backend / API / Testing independently.
Legend: ✅ done · 🟡 partial · ⬜ not started · ➖ n/a for hackathon scope.
Build order = PRB §5.4 critical path: **ingestion → resolution → investigation → correction**,
then Should modules.

| Module | Backend | API | UI | Tests | Notes |
|---|:-:|:-:|:-:|:-:|---|
| Global Shell | ✅ | ✅ | ✅ | 🟡 | Nav, DegradedBanner, confidence legend, auth stub |
| M11 Ingestion (Must half) | ✅ | ✅ | ✅ | ✅ | Pipeline DAG, provenance, confidence gating, quarantine |
| M2 Living Asset Map | ✅ | ✅ | ✅ | ✅ | Resolution queue, adjudicate, unmerge (reversible) |
| M1 Decision Investigation | ✅ | ✅ | ✅ | ✅ | Agent path, streaming, citations, abstention, as-of |
| M8 Correction & Learning | ✅ | ✅ | ✅ | ✅ | Attributed graph edit, immediate re-answer, eval label |
| M12 Field Mode | ✅ | ✅ | ✅ | 🟡 | Same M1 pathway, offline/glare/traversal-trace layout |
| M6 Compliance Intelligence | ✅ | ✅ | ✅ | ✅ | Rule engine (rules-as-data), coverage footer, evidence |
| M7 Execution Center | ✅ | ✅ | ✅ | ✅ | Draft→approve gated write (CP-3), distinct approver |
| M9 Audit & Provenance | ✅ | ✅ | ✅ | 🟡 | Append-only log, filters, reproducible answer context |
| M10 Decision Analytics | ✅ | ✅ | ✅ | 🟡 | KPI cards, actual-vs-target, corpus-size flywheel |
| M5 Organizational Memory | ✅ | ✅ | ✅ | 🟡 | KNOWS edges, who-to-ask, retirement risk, PII-min |
| M4 Knowledge Evolution | ✅ | ✅ | ✅ | 🟡 | Decay job, KnowledgeRisk flags, supersede-not-delete |
| M3 Decision Memory & Replay (Could) | ✅ | ✅ | ✅ | 🟡 | Decision graph replay, "would this still hold today" |

## Cross-cutting

| Concern | State | Notes |
|---|:-:|---|
| Ports/adapters (embedded + production) | ✅ | ADR-P01 |
| Model provider abstraction (CP-5) + local fallback (CP-9) | ✅ | ADR-P02 |
| Bitemporal graph (CP-7) | ✅ | valid-time + transaction-time, as-of reconstruction |
| Provenance sink (CP-1) | ✅ | rejects unsourced writes |
| Verifier / grounding / abstention (CP-2/CP-4) | ✅ | claim→span check, strip, abstain |
| Gated writes / ABAC (CP-3) | ✅ | distinct approver, deny-by-default |
| Audit (append-only) | ✅ | every read/answer/proposed+committed write |
| Circuit breaker / degradation ladder (CP-9) | ✅ | 5 rungs, surfaced to UI |
| Eval harness (RAGAS/DeepEval-style) | ✅ | faithfulness, citation, abstention, resolution |
| Design tokens from design.md | ✅ | tokens.ts + global.css |
| docker-compose (production topology) | ✅ | infra/ |

## Known gaps (honest, per PRB §8.4.2 — see `known_bugs.md`)
- P&ID graphics extraction (YOLO/Relationformer) is stubbed behind a capability flag (ADR-P03).
- Production adapters (Neo4j/Qdrant/Postgres/Redis) are implemented against the port contract
  but exercised primarily in the embedded profile in this build; wiring is present.
- Voice-to-question (M12) uses the browser SpeechRecognition API where available; no offline
  ASR model is bundled.
