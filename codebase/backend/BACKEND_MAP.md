# Prahari backend — architecture map

> Phase 0 deliverable. Describes the conventions a new capability must conform to.
> Nothing here proposes changes; see `BACKEND_AUDIT.md` for gaps and the plan.

---

## 1. Shape of the codebase

A **hexagonal (ports/adapters) modular monolith** with a single composition root. 3,700-odd
lines of application code under `codebase/backend/app/`, plus `prompts/` and `tests/` beside it.

```
codebase/backend/
  app/
    config.py            pydantic-settings; the ONLY place env is read
    container.py         composition root — the ONLY place adapters are chosen
    main.py              FastAPI assembly, router mounting
    seed.py              the demo corpus, written in code
    ports/__init__.py    ALL port protocols live in this one file
    stores/              the adapter families + registry
    domain/              pure models, graph ontology, errors
    <capability>/        one package per business concern
    api/                 one router module per resource
  prompts/               versioned prompt files + manifest.json
  tests/                 pytest; 19 passing
```

---

## 2. The five conventions that matter

Any new capability must follow all five. There is no `services/` folder and no per-module DI.

### 2.1 A port is a `Protocol` in one shared file
`app/ports/__init__.py` holds **every** port as a `@runtime_checkable Protocol`. There are
exactly four today: `IGraphStore`, `IVectorStore`, `IRelationalStore`, `IModelProvider`. Ports
import only from `domain.models` — never from adapters.

### 2.2 Adapters come in families, selected by profile
`app/stores/registry.py` exposes `build_stores(settings) -> Stores`, a frozen dataclass of
`(graph, vector, relational)`. Two families:

| Profile | Adapter | Notes |
|---|---|---|
| `embedded` (default) | `stores/embedded.py` → `EmbeddedStore` | **One object implements all three ports**, backed by a single SQLite file at `state_dir/prahari.db`. No external services, no API key. |
| `production` | `stores/production.py` → `Neo4jGraphStore`, `QdrantVectorStore`, `PostgresRelationalStore` | Imported **lazily** so embedded never needs the drivers. |

`IModelProvider` is the exception: it is **not** in `Stores`. Providers are constructed by
`agents/model_router.py` from settings, because provider choice is a runtime degradation
decision (CP-9), not a deployment-profile decision.

### 2.3 `container.py` is the only wiring point
One `Container` class. Its `__init__` constructs every service in dependency order and assigns
it to a public attribute (`self.ingestion`, `self.retrieval`, `self.orchestrator`, …).
`get_container()` is `@lru_cache(maxsize=1)`; `reset_container()` is the test hook. API routes
reach services through `api/deps.py`, never by importing a service module directly.

**Consequence for new work:** a new capability is (a) a port in `ports/__init__.py`, (b) one or
more adapters in the module that owns the concern, (c) a selection function next to the
adapters, (d) one line in `Container.__init__`, (e) config keys in `config.py`.

### 2.4 Config is one flat `Settings` class, prefix `PRAHARI_`
`app/config.py` defines a single `Settings(BaseSettings)` with
`env_prefix="PRAHARI_"`, `env_file=".env"`, `extra="ignore"`. Every field is typed and
defaulted so the app boots with **zero** environment variables.

> **Naming note.** Existing keys are `graph_uri`, `graph_user`, `graph_password`, `vector_url`,
> `pg_dsn`, `redis_url` — i.e. `PRAHARI_GRAPH_URI`, `PRAHARI_VECTOR_URL`, … There is **no**
> `NEO4J_URI` or `QDRANT_URL`. New keys must adopt the same prefix and flat style.

### 2.5 Prompts are versioned files with a hashed manifest
`backend/prompts/<stage>/<name>@v<n>.md`, indexed by `prompts/manifest.json`
(`{"version": "1.0.0", "prompts": {"planner": "planner/plan@v1.md", …}}`). The manifest hash is
returned on every answer (`prompt_manifest_hash`) for reproducibility. A new model-facing
prompt belongs here, not inline in Python.

---

## 3. Module ledger

One line per module: what it owns, and its implementation state.

| Module | Owns | Status |
|---|---|---|
| `config` | Settings, profile selection | implemented |
| `container` | Composition root | implemented |
| `ports` | The four port protocols | implemented |
| `stores` | Embedded (SQLite) + production (Neo4j/Qdrant/Postgres) adapters | implemented |
| `domain` | Pure models, graph ontology, errors | implemented |
| `graph` | `ProvenanceSink` — the CP-1 write gate | implemented |
| `embeddings` | Local deterministic embedder (air-gap) | implemented |
| `ingestion` | Upload → detect → parse → extract → provenance → confidence gate → write | **partial** — text-only; `ocr`, `graphics`, `resolution_handoff` stages advertised in the docstring do not exist; `SUPERSEDES` write is unreachable |
| `resolution` | Entity resolution, alias collapsing, reversible merges | **partial** — adjudication/unmerge real; candidate generation depends on a `candidate_asset` prop ingestion never sets |
| `retrieval` | Graph traversal + vector enrichment + fusion | **partial** — no rerank, no BM25; `classify()` computed but never branched on; vector scores discarded |
| `agents` | Orchestrator, providers, model router, prompt loading | **partial** — Planner and Critic emit a stage event and do no work; providers + template-synth are real |
| `investigations` | Investigation lifecycle + persistence | **partial** — semantic cache is write-only, never read |
| `rules` | Compliance rule engine + coverage | **partial** — engine is data-driven, but the only rule writer is `seed.py` (N=2); coverage denominator is a per-rule constant |
| `knowledge` | Decay/risk flags | **partial** — 3 of 4 triggers live; `contradiction` is unreachable; no scheduler |
| `resilience` | CP-9 degradation ladder, circuit breaker, rate limit | **partial** — `-vector`/`-graph` rungs reachable only by admin override, never by a failure path |
| `actions` | Gated writes (work orders, CP-3) | **partial** — CMMS commit simulated; two-person rule not actually enforced (`abac.py` ignores `drafter_role`) |
| `corrections` | Correction & learning loop (CP-10) | implemented — eval labels written but never consumed |
| `decisions` | Decision memory + replay | implemented (read-only; no runtime writer) |
| `orgmemory` | Who-knows-what, who-to-ask | implemented — `who_to_ask` hardcodes `tenant = "demo"` |
| `analytics` | Flywheel KPIs | **partial** — 4 of 6 KPIs return `None` or a literal string |
| `audit` | Append-only audit sink | implemented (no tamper-evidence) |
| `auth` | Dev/OIDC identity, RBAC matrix, ABAC policy | implemented |
| `api` | FastAPI routers, one per resource | implemented — `POST /v1/documents` leaks an `_http` field and always returns 202 |
| `seed` | The demo corpus, inline in code | implemented — reads no files; the 16 corpus files on disk are disconnected from it |

*(Status column is corroborated module-by-module in `BACKEND_AUDIT.md`.)*

---

## 4. The `/v1` contract surface (must not change)

33 REST endpoints plus one WebSocket. The frontend consumes all of the following; any change
here is a breaking change and must be flagged rather than made.

```
auth          POST /v1/auth/login · GET /v1/auth/me
investigate   POST /v1/investigations · GET /v1/investigations · GET /v1/investigations/{id}
              WS   /v1/stream/investigations/{id}?token=…      (not in OpenAPI)
documents     POST /v1/documents · GET /v1/documents/{doc_id}
              GET  /v1/ingestion · GET /v1/ingestion/{job_id}
assets        GET  /v1/assets
compliance    GET  /v1/compliance/assets/{asset_id} · GET /v1/compliance/coverage
knowledge     GET  /v1/knowledge/health · POST /v1/knowledge/run-decay
              POST /v1/knowledge/flags/{id}/reverify · …/supersede
resolution    GET  /v1/resolution/queue · GET /v1/resolution/assets/{id}/history
              POST /v1/resolution/{proposal_id}/adjudicate · POST /v1/resolution/unmerge/{id}
actions       GET  /v1/actions · POST /v1/actions/work-order/{draft|submit|reject}
corrections   POST /v1/corrections · GET /v1/corrections
memory        GET  /v1/org-memory · POST /v1/org-memory/{person|knows}
decisions     GET  /v1/decisions · GET /v1/decisions/{id}/replay
ops           GET  /v1/health · GET /v1/audit · GET /v1/analytics · POST /v1/admin/degrade
```

**Streaming events** (WebSocket frame `type` values) consumed by the frontend:
`banner`, `stage`, `token`, `claim`, `graph_hop`, `verdict`, `abstain`, `done`, `error`.

---

## 5. Dependencies as declared

`pyproject.toml`:

- **base** — fastapi, uvicorn, pydantic, pydantic-settings, python-multipart, httpx,
  websockets, PyJWT, cryptography.
- **`[production]`** — neo4j, qdrant-client, psycopg, redis.
- **`[dev]`** — pytest, pytest-asyncio, ruff, black, mypy.

**There is no PDF, image, OCR, or vision dependency of any kind.** No PyMuPDF/fitz, no Pillow,
no pytesseract, no paddle. This is the single most important fact for the OCR/VLM work.

Tests: `pytest -q` → **19 passed**.
