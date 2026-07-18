# SENTINEL core

The modular monolith (Bible ADR-006). Ports/adapters seams; two adapter families behind one set
of ports (ADR-P01): **embedded** (default — SQLite/local-vector/template-synth, no external
services) and **production** (Neo4j/Qdrant/Postgres/Redis + provider-abstracted LLM).

## Layout (Bible §12.1)

```
app/
  config.py            profile selection (embedded | production)
  container.py         composition root — wires ports → adapters → services
  domain/              pure models, graph ontology (ISO 14224/DEXPI), provenance, errors
  ports/               IGraphStore, IVectorStore, IRelationalStore, IModelProvider
  stores/              embedded.py (SQLite) · production.py (Neo4j/Qdrant/Postgres) · registry
  graph/               provenance_sink.py — the CP-1 write gate
  embeddings/          local, offline, deterministic embedder (air-gap)
  ingestion/           the DAG: parse → extract → provenance → confidence gate → quarantine
  resolution/          entity resolution (the moat): scoring, adjudication, reversible unmerge
  retrieval/           dual graph+vector router, context assembly, fusion
  agents/              providers (CP-5 + CP-9 rungs), model_router, orchestrator (M1)
  rules/               compliance rule engine (rules-as-data, CP-6)
  actions/             gated writes (CP-3)
  corrections/         correction & learning loop (CP-10)
  orgmemory/ knowledge/ decisions/ analytics/   M5 · M4 · M3 · M10
  audit/               append-only sink (§8.5)
  auth/                identity (stub/OIDC), RBAC matrix (PRB §1.4), ABAC policy
  resilience/          circuit breaker + CP-9 degradation ladder
  api/                 FastAPI routers (Bible §7) + the thin gateway concerns
  seed.py              the provenance-clean demo corpus (ADR-012)
prompts/               versioned prompt files + manifest (CP-5/CP-7)
tests/                 critical-path release gates (Bible §14)
```

## Run (embedded, no external services)

```bash
py -3.12 -m venv .venv && .venv\Scripts\activate     # Windows
pip install -e ".[dev]"
python -m app.seed
pytest -q                    # 11 critical-path tests
uvicorn app.main:app         # http://localhost:8000/docs
```

## Invariant → mechanism map (Bible §14.10)

| Invariant | Enforced by |
|---|---|
| CP-1 provenance | `graph/provenance_sink.py` rejects unsourced fact writes |
| CP-2 citation | Orchestrator Verifier strips uncited claims; providers cite only given spans |
| CP-3 gated write | `actions/service.py` + `auth/abac.py` require a distinct approver |
| CP-4 abstention | `Verdict.ABSTAINED` with `{known, unresolved, who_to_ask}` |
| CP-5 model abstraction | `agents/providers.py` + versioned `prompts/` |
| CP-7 bitemporal | `effective_from/to` on edges; `as_of` traversal; supersede-not-delete |
| CP-9 degradation | `resilience/` ladder, surfaced to the UI banner |
| CP-10 correction | `corrections/service.py` — attributed graph edit + eval label |
