# Known Bugs / Gaps

Honest register per PRB §8.4.2 (an edge case is either handled or logged here — never silently
skipped).

| # | Area | Description | Severity | Status |
|---|---|---|---|---|
| KB-1 | Ingestion | P&ID symbol/line graphics detection (YOLO/Relationformer) is a deterministic DEXPI stub behind the `pid_graphics` flag; real detection needs model weights + GPU (ADR-P03). | Low (Could-scope) | Documented |
| KB-2 | Stores | Production Neo4j/Qdrant/Postgres adapters **verified live** (seed + 6-hop cited investigation, ADR-P07). Note: qdrant client pinned `<1.12` to match the v1.9 server image; compose publishes Postgres on host **5433** to avoid a local-Postgres collision on 5432. | Low | Verified |
| KB-3 | M12 | Offline voice input relies on browser `SpeechRecognition`; unavailable browsers fall back to text (identical M1 pathway). | Low | By design |
| KB-4 | Eval | RAGAS/DeepEval metrics are computed by an in-repo faithful reimplementation (entailment via span-overlap + provider check), not the upstream pip packages, to keep the embedded profile dependency-light and offline-capable. | Info | By design |
