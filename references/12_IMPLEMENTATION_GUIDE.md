# 12 — Implementation Guide

> Repo layout, naming, standards, branching, CI/CD, feature flags, migration strategy. The thing a new engineer reads to start committing in an hour.

## 12.1 Repository structure (monorepo)

```
sentinel/
├─ README.md
├─ docker-compose.yml
├─ .github/workflows/            # ci.yml, deploy.yml, eval.yml
├─ gateway/                      # thin edge: authn/z, rate-limit, routing
├─ core/                         # the modular monolith
│  ├─ app/
│  │  ├─ api/                    # FastAPI routers (REST + WS)  → 07
│  │  ├─ orchestrator/           # LangGraph state machine       → 04
│  │  ├─ agents/                 # planner, executor, critic, verifier, compliance…
│  │  ├─ retrieval/              # router, graph_retriever, vector_retriever → 03
│  │  ├─ ingestion/              # parse, ocr, graphics, extract, provenance  → 03
│  │  ├─ resolution/             # entity resolution service     → 05
│  │  ├─ rules/                  # compliance rule engine (rules-as-data)     → 06
│  │  ├─ graph/                  # Neo4j gateway + Cypher templates → 05
│  │  ├─ stores/                 # postgres, qdrant, redis, blob adapters      → 06
│  │  ├─ audit/                  # append-only provenance/audit    → 08
│  │  └─ ports/                  # interfaces (extraction seams)   → 02
│  ├─ prompts/                   # versioned prompt templates      → 04
│  ├─ worker/                    # queue consumers
│  ├─ migrations/                # alembic (pg) + cypher (neo4j)
│  └─ tests/                     # unit, integration, eval         → 14,15
├─ web/                          # React + TS PWA                  → 10
│  ├─ src/components/            # AnswerCard, GraphCanvas, ResolutionQueue…
│  ├─ src/features/             # investigation, compliance, resolution, mobile
│  └─ src/lib/                   # api client, ws client, tokens
├─ eval/                         # golden set, RAGAS/DeepEval harness → 15
├─ infra/                        # k8s manifests, helm, terraform   → 09
└─ docs/                         # this bible + generated OpenAPI
```

## 12.2 Naming conventions

- Python: `snake_case` funcs/modules, `PascalCase` classes, `UPPER_SNAKE` consts. Ports prefixed `I` (`IRetriever`).
- TS: `camelCase` vars, `PascalCase` components/types, files `PascalCase.tsx` for components.
- Graph: node labels `PascalCase`, edge types `UPPER_SNAKE`, properties `snake_case`.
- API: paths `/kebab-case`, JSON fields `snake_case`.
- Env vars: `SENTINEL_<AREA>_<NAME>`.

## 12.3 Coding standards

- **Python:** ruff (lint) + black (format) + mypy (strict on `core/app`). No I/O in domain logic; adapters at the edges (hexagonal).
- **TS:** eslint + prettier + tsc strict. No `any` on public boundaries.
- **Every fact write** goes through the provenance sink — no direct graph writes bypassing CP-1.
- **No secrets in code**; config via env + vault (`08`).
- Functions do one thing; ports are deep, adapters thin (Ousterhout).

## 12.4 Branching & workflow

- Trunk-based with short-lived feature branches; `main` always deployable.
- Branch names `feat/…`, `fix/…`, `chore/…`.
- Conventional Commits (`feat:`, `fix:`, `docs:`…) → drives changelog.
- PRs require: green CI, one review, the PR checklist (`14`), and no eval regression.

## 12.5 CI/CD

```
ci.yml   (on PR):    ruff+black+mypy → eslint+tsc → unit tests → eval-smoke → build image
deploy.yml (on main):build → push → deploy staging → integration + eval-full → gate → prod
eval.yml (nightly):  full golden-set run → dashboard → alert on regression
```
**Eval is a gate (`15`):** a PR that drops faithfulness/citation/abstention below threshold cannot merge. Quality is enforced by the pipeline, not by hope.

## 12.6 Feature flags

- Flags for: `compliance_engine`, `gated_actions`, `decision_graph`, `local_model`, `counterfactual`.
- Hackathon build ships with only the **Must** flags on (PRD §1.10); **Could** features flagged off but present.
- Flags are config, not code branches littered through the codebase.

## 12.7 Migration strategy

- **Postgres:** Alembic, forward-only, tested down-revisions, run in CI against a seeded DB.
- **Neo4j:** versioned Cypher migrations with dry-run + rollback; every ontology change has an ADR (`13`).
- **Data backfills** run as idempotent workers, never as ad-hoc scripts against prod.

## 12.8 Local dev setup (a new engineer, in order)

```
1. cp .env.example .env            # fill vault refs
2. docker compose up -d            # brings up all stores + core + web
3. make seed                       # loads the provenance-clean demo corpus
4. make eval-smoke                 # confirms grounding/citation baselines
5. open https://localhost          # PWA console
```

## 12.9 Definition of Done

A change is done when: code + tests + docs updated, CI green, eval not regressed, provenance preserved (CP-1), any new write is gated (CP-3), and the ADR is written if a decision was made.

---

**Red Devil:** *Beck:* "Trunk-based + eval-as-gate + hexagonal core = changeable software. **APPROVED.**" *Martin:* "Ports/adapters keep the domain clean of I/O — the extraction seams are honest."
**Hackathon Winning:** "Feature-flagged Could-features let you demo depth without shipping risk. Average→Strong."
**Black Swan:** monorepo + flags → can cut scope in minutes if the clock demands. **Survivable.**
**Green:** eval-gate prevents shipping regressions that waste rework. **Positive.**
