# Prahari backend — pipeline & infrastructure audit

> Phase 1 deliverable. What actually runs today, what only looks like it runs, and what the
> no-Docker / OCR / VLM work has to build on. Every claim below was read out of the code.

---

## 1. Ingestion pipeline — as executed

`POST /v1/documents` → `IngestionPipeline.ingest()` → response. **Fully synchronous inside the
HTTP request.** No queue, no worker, no background task.

| # | Stage | Real? | Note |
|---|---|---|---|
| 1 | hash + duplicate check | ✅ | SHA-256 of content; duplicate short-circuits |
| 2 | `detect` | ⚠️ | **File extension only.** `.csv`→csv, `.pdf`→pdf, everything else→text. No MIME, no magic bytes, no content sniff |
| 3 | Document node + `SUPERSEDES` | ⚠️ | Node yes. The `SUPERSEDES` write is **dead code** — guarded by `_prior_version()`, which is `return None` |
| 4 | `parse` | ❌ | `content.decode("utf-8", errors="replace")` and nothing else |
| 5 | quarantine-if-empty | ⚠️ | Only fires on a genuinely empty doc |
| 6 | `extract` | ⚠️ | Three extractors: `structured` / `csv` / `text` |
| 7 | span + vector write | ✅ | Real, provenance-stamped |
| 8–9 | confidence gate | ✅ | ≥0.85 auto, 0.60–0.85 provisional, <0.60 quarantine |
| 10 | `resolution_handoff` | ❌ | **A log line.** `ResolutionService` is never called |
| 11 | complete + audit | ✅ | |

The docstring advertises `detect → parse/ocr → (graphics) → extract → provenance → gate →
resolution handoff → write`. **Three of those eight stages do not exist:** `ocr`, `graphics`,
and a real `resolution handoff`. `IngestionStatus.OCR` and `IngestionStatus.GRAPHICS` are
defined in `domain/models.py` and never assigned anywhere.

### 1.1 The binary-document bug (blocks the OCR/VLM work)

```python
# ingestion/pipeline.py:93-96
try:
    text = content.decode("utf-8", errors="replace")
except Exception:
    text = ""
```

`errors="replace"` never raises, so the `except` is unreachable. A PDF or PNG uploaded today
does **not** get quarantined — it decodes to mojibake, the sentence splitter still yields
non-empty fragments, and **binary garbage is written to the graph and the vector index as
citable spans.** The quarantine branch only catches a genuinely empty document.

This must be fixed before OCR/VLM, not after: the "no provider available → quarantine" path
the plan depends on does not currently exist.

### 1.2 Extraction is thin on the text path

`extract_text` applies one regex (`[A-Z]{1,4}-?\d{2,4}[A-Z]?`) producing `Identifier` entities
at a hardcoded 0.75 confidence, and **zero relations**. Every narrative document therefore
contributes tags and nothing else — which is exactly why the 16-document corpus produced
1,565 spans but almost no new edges.

---

## 2. Investigation pipeline — as executed

`POST /v1/investigations` stores a request row; `WS /v1/stream/investigations/{id}` runs it.

**Stages emitted:** `Planner` → `Retriever` → `Executor` → `Critic` → `Verifier`.
**Two of the five do no work.** `Planner` emits its event and proceeds straight to retrieval;
`Critic` emits its event and builds two lookup dicts for the Verifier. There is no
decomposition and no adversarial pass. The Verifier gate is real and does enforce grounding.

**Event types emitted by the orchestrator (8):** `banner`, `stage`, `graph_hop`, `token`,
`claim`, `abstain`, `verdict`, `done`. A 9th, `error`, is emitted only at the API layer.
Wire shape is `{"type": ev.type, **ev.data}`; note `graph_hop` and `claim` nest their payload
under a key while the others are flat.

### 2.1 Retrieval has no ranking policy

`retrieve()` = anchor resolution → graph traversal (`max_hops=3`) → vector enrichment
(`retrieval_k=8`) → dedup → truncate at `context_span_budget=24`.

- **No reranker. No BM25. No keyword search anywhere in the app.**
- `classify()` returns a `Route` (`vector`/`graph_first`/`compliance`/`hybrid`) that is
  **never branched on** — every question gets identical treatment.
- Vector similarity scores are **discarded** (`for span_id, _score, payload in …`).
- Because graph spans are appended before vector spans and the budget truncates in insertion
  order, **graph provenance starves vector hits by accident**, not by policy.

Embedding is `embeddings/local_embedder.py`: MD5-hashed bag-of-words + character trigrams into
256 dims. Lexical, not semantic — "impeller oscillation" will not retrieve "pump vibration".
It is imported concretely by `stores/embedded.py`; there is **no `IEmbedder` port**.

---

## 3. Cross-module gap list

Ordered by how much it blocks the requested work.

| # | Gap | Impact |
|---|---|---|
| G1 | No PDF/image/OCR/VLM capability of any kind; no such dependency declared | Blocks all of 3b/3c |
| G2 | Binary uploads produce garbage spans instead of quarantine | Corrupts the graph; blocks the "no provider → quarantine" contract |
| G3 | `CONTRADICTS` is **never written** anywhere; not seeded either | `knowledge/decay.py` trigger 2 is unreachable → **Phase 4 acceptance #6 cannot pass today** |
| G4 | Ingestion never calls `ResolutionService`; proposals need a `candidate_asset` prop the pipeline never sets | Aliases from uploaded docs never resolve → Phase 4 #6 (alias collapse) only works on seeded data |
| G5 | `SUPERSEDES` write unreachable (`_prior_version` → `None`) | No document version chain; CP-7 unimplemented |
| G6 | No rerank / BM25 / hybrid fusion; `classify()` inert; vector scores dropped | Retrieval quality ceiling; "hybrid retrieval + rerank" in 3d is greenfield |
| G7 | Planner and Critic stages are event-only | "Streamed agentic stages" in 3d are partly theatre |
| G8 | Compliance rule corpus is 2 rows, both from `seed.py`; coverage denominator is a per-rule constant (42, 30) | Coverage is honest in *form* but the numbers come from literals |
| G9 | Two-person rule not enforced — `authorize_work_order_submit` ignores `drafter_role` | CP-3 claim is false today |
| G10 | `orgmemory.who_to_ask` hardcodes `tenant = "demo"` | Abstain cards break in any other tenant |
| G11 | Semantic cache is write-only; never read | Every ask re-runs the full pipeline |
| G12 | `POST /v1/documents` returns HTTP 202 always, leaking `_http: 409` in the body for duplicates | Contract wart the frontend currently ignores |
| G13 | Blocking `httpx.post` inside the async streaming path | One slow provider stalls every concurrent WS client |
| G14 | `LocalOpenWeightsProvider` reports `Rung.FULL` but delegates to template-synth | Breaks the banner-honesty invariant CP-9 is built on |
| G15 | `stores/embedded.py` vector index has no delete method | Removed documents leave orphan vectors |

---

## 4. Infrastructure audit — what the code actually assumes

This is the decisive section for "no Docker".

### 4.1 There are two profiles, and the default already needs nothing

| Profile | Graph | Vector | Relational | External services |
|---|---|---|---|---|
| **`embedded`** (default) | `EmbeddedStore` | `EmbeddedStore` | `EmbeddedStore` | **none** |
| `production` | Neo4j | Qdrant | Postgres | 3 servers |

`stores/registry.py::_build_embedded` returns **one object bound to all three ports**, backed by
a single SQLite file at `state_dir/prahari.db` (WAL mode, indices, tenant scoping, bitemporal
filtering). Production adapters are imported **lazily**, so the embedded profile never needs
`neo4j`/`qdrant-client`/`psycopg` installed.

> **The no-Docker floor already exists and is the default.** The app boots, seeds, serves, and
> streams with zero external servers and zero environment variables. Everything verified in this
> session — 17 documents ingested, investigations streaming, 1,819 spans — ran on it.

### 4.2 Redis is declared but dead

- `pyproject.toml` declares `redis>=5.0` under `[production]`.
- `config.py` defines `redis_url`.
- **Nothing imports redis. Nothing reads `redis_url`.**
- No Celery, RQ, Dramatiq, APScheduler, Kafka. No `BackgroundTasks`, no `asyncio.create_task`.
- The WS stream is fed by an **in-process async generator** (`run_stream` yields; the route
  sends). Rate limiting is an in-process `threading.Lock` token bucket.

**Consequence:** a `QUEUE_BACKEND=inprocess|redis` setting would be a knob that switches
nothing, because there is no queue consumer to switch. Recommendation in the plan.

### 4.3 Environment naming — the prompt's names do not match the code

Config is a single flat `Settings` with `env_prefix="PRAHARI_"`. Existing keys:

| Concern | Actual setting | Actual env var |
|---|---|---|
| Graph | `graph_uri`, `graph_user`, `graph_password` | `PRAHARI_GRAPH_URI`, … |
| Vector | `vector_url` | `PRAHARI_VECTOR_URL` |
| Relational | `pg_dsn` | `PRAHARI_PG_DSN` |
| Cache | `redis_url` | `PRAHARI_REDIS_URL` (unread) |

There is **no** `NEO4J_URI`, `QDRANT_URL`, or `REDIS_URL`. New keys must adopt the `PRAHARI_`
prefix and flat style, or they will be silently ignored (`extra="ignore"`).

### 4.4 Docker today

`codebase/docker-compose.yml` brings up neo4j / qdrant / postgres / redis, and
`backend/Dockerfile` runs `python -m app.seed` at build time. Neither is required for the
default profile. Per the brief, no new compose/Dockerfile will be added; the existing ones can
stay as an unused artifact or be deleted — **your call, flagged rather than decided.**

---

## 5. The VLM blocker you should know about before approving

**There is no drawing anywhere in this repository.**

- No `.png`, `.jpg`, `.pdf`, `.tif`, or `.dwg` file exists in the repo (the only image is the
  frontend's `icon.svg`).
- The corpus is 11 `.md`, 4 `.csv`, 1 `.json`.
- `PID_BFW_system_P-101B.md` — the file Phase 4 test #3 names — is **markdown text**: an ASCII
  schematic plus a component/connection list. A vision model adds nothing to it; it is already
  machine-readable prose.
- `seed.py` labels five documents `type: "pdf"`, but those are node props with hand-written
  span text. No PDF is ever parsed.

So Phase 4 test #3 ("ingesting the P&ID makes the VLM populate connectivity edges") **cannot be
satisfied as written** — there is nothing for the VLM to look at. Options are set out in the
plan; this needs a decision from you before 3c is worth building.
