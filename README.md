# SENTINEL

**Industrial Decision Intelligence Operating System** — ET Hackathon Problem Statement 8.

> SENTINEL unifies fragmented industrial knowledge into one continuously-learning
> decision-intelligence layer that reasons across documents **and shows its work** —
> every answer carries its evidence, its confidence, and the path it traversed to get there.

SENTINEL is **not** a chatbot, a GraphRAG demo, or a document search engine. It is an
operating system for industrial decision-making: it preserves the *reasoning* behind
decisions so that no failure repeats because the plant forgot why a decision was made.

---

## What this repository is

A faithful implementation of the **SENTINEL Product Requirements Bible (PRB)**, styled by
**`design.md`**, and engineered per the supporting reference volumes.

```
PRAHARI/
├─ 00_CLAUDE_IMPLEMENTATION_RULES.md          # governance (authority order)
├─ 01_PROJECT_CONTEXT.md                      # problem statement & vision
├─ 02_SENTINEL_Product_Requirements_Bible.md  # master implementation — the source of truth
├─ 03_design.md                               # design system (UI authority)
├─ 04_demo.md                                 # demo & presentation flow
├─ references/                                # supporting engineering volumes
│  ├─ 02_SYSTEM_ARCHITECTURE.md … 15_EVALUATION.md
├─ docs/                                       # build-time docs & status
│  ├─ ADR/        # architecture_decisions.md (build ADRs)
│  ├─ API/        # API reference (+ live OpenAPI at /v1/openapi.json)
│  ├─ diagrams/   # C4 / sequence / degradation-ladder (Mermaid)
│  ├─ assets/
│  ├─ coding_rules.md · ui_rules.md · implementation_status.md
│  └─ known_bugs.md · todo.md · verification_checklist.md
├─ codebase/
│  ├─ backend/    # FastAPI modular monolith — see codebase/backend/README.md
│  ├─ frontend/   # React + TS PWA console, built from 03_design.md tokens
│  ├─ eval/       # RAGAS/DeepEval-style golden-set harness
│  └─ docker-compose.yml   # production store topology (Neo4j/Qdrant/Postgres/Redis)
├─ .github/workflows/   # CI: lint · test · eval-gate · web build
├─ README.md · LICENSE · .gitignore
```

The build follows the PRB's single critical path (§5.4):

```
ingestion  →  entity resolution  →  investigation  →  correction
```

end-to-end, before any Should/Could module.

## The three things that make it SENTINEL (not "another RAG demo")

1. **The Living Asset Map (M2)** — four identifiers (`P-101B`, "Boiler Feed Pump B", an OEM
   part number, "the noisy one") collapse into one canonical asset, human-adjudicated and
   **reversible**. This human-validated resolution corpus is the moat.
2. **Decision Investigation (M1)** — a causal chain traversed across documents nobody linked,
   **each hop citing a page**, streamed as it is retrieved.
3. **The Refusal (M1 abstention)** — asked a question it cannot ground, SENTINEL **does not
   guess**. It says what it can't ground and *who to ask*. Abstention is a first-class success.

## Architecture at a glance

Modular monolith (Bible ADR-006) with ports/adapters seams:

- **`gateway/`** — thin edge: OIDC/RBAC pre-check, rate-limit, routing, correlation IDs.
- **`codebase/backend/`** — the monolith: API (REST+WS), LangGraph-style agent orchestrator,
  dual retrieval router (graph + vector), ingestion pipeline, entity resolution, compliance rule
  engine, audit + provenance sink.
- **`codebase/frontend/`** — React + TypeScript PWA console, built from `03_design.md` tokens.
- **`eval/`** — RAGAS/DeepEval-style golden-set harness (faithfulness, citation, abstention).
- **`infra/`** — docker-compose for the full production store topology.

### Two adapter families behind one set of ports

| Ports (Bible §2.4) | Embedded adapter (default, air-gap / CP-9) | Production adapter (docker-compose) |
|---|---|---|
| Graph | NetworkX-backed temporal graph | Neo4j |
| Vector | Local hashing-embedder + cosine index | Qdrant |
| Relational/Audit | SQLite | Postgres |
| Cache/Queue | In-process | Redis (+ Streams) |
| Model | Offline template synthesizer (CP-9 `-model` rung) | Provider-abstracted LLM (CP-5) |

The **embedded** family is the default so the demo runs on one box with **zero external
services and no API key** — which *is* the Bible's air-gap / degradation-ladder design
(ADR-007, §8.6), not a mock. Set `SENTINEL_PROFILE=production` to use the store topology in
`codebase/docker-compose.yml`. See `codebase/backend/README.md` and
`docs/ADR/architecture_decisions.md` (ADR-P01).

## Quickstart (embedded profile — no external services)

```bash
# 1. Backend
cd codebase/backend
py -3.12 -m venv .venv && .venv\Scripts\activate    # Windows (use py -3.12, not msys python)
pip install -e .
python -m app.seed            # loads the provenance-clean demo corpus
uvicorn app.main:app --reload # API on http://localhost:8000  (docs at /docs)

# 2. Frontend  (new terminal)
cd codebase/frontend
npm install
npm run dev                   # console on http://localhost:5173
```

Then open the console, ask **"why is P-101B running hot?"**, watch the traversal stream hop by
hop, and — the closing move — disable the graph (`Field Mode → degrade`) and ask again to see
the system refuse honestly.

## Governance

This codebase obeys `CLAUDE_IMPLEMENTATION_RULES.md`. Authority order:

1. Engineering invariants **CP-1…CP-10**
2. **SENTINEL Product Requirements Bible** — *what* to build
3. **`design.md`** — *how* it looks
4. Supporting engineering volumes — *how* it is engineered

See `docs/implementation_status.md` for per-module build state and
`docs/ADR/architecture_decisions.md` for every decision made during the build. All governance
and status docs live in `docs/`; the spec/source-of-truth docs are the numbered files at root
and in `references/`.

## License

See `LICENSE`.
