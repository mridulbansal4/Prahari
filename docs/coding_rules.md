# Coding Rules (enforcement)

Derived from Bible §12.2–12.3 and the ten invariants CP-1…CP-10. These are hard rules; a
violation is a defect, not a style preference.

## Structure
- Hexagonal: **no I/O in domain logic.** Adapters live at the edges (`app/stores`,
  `app/graph`, `app/agents/providers`). Domain logic (`app/domain`, `app/resolution`,
  `app/rules`) depends only on ports (`app/ports`), never on a concrete store.
- Ports are prefixed `I` (`IRetriever`, `IGraphStore`). Exactly one production + one embedded
  adapter per port; each is a documented extraction seam (Bible §2.4).

## The invariants, mechanically
- **CP-1 provenance:** every fact-bearing node/edge write goes through `ProvenanceSink`, which
  rejects any write lacking ≥1 `EVIDENCED_BY` span. No module writes to the graph directly.
- **CP-2 citation:** the Executor may cite only span ids present in the assembled context; the
  Verifier re-checks every claim→span mapping and strips uncited claims.
- **CP-3 gated writes:** no code path reaches a system-of-record commit without a distinct,
  authorized `approver` identity. Enforced in `actions` service + ABAC policy + a test.
- **CP-4 abstention:** abstention is a returned `Verdict.ABSTAINED`, never an exception or an
  empty answer. Carries `{what_is_known, unresolved, who_to_ask}`.
- **CP-5 model abstraction:** no prompt, statute, or tenant value hardcoded in code. Prompts
  are versioned files under `backend/prompts/`; the manifest hash is logged per answer.
- **CP-7 bitemporal:** edges carry `effective_from/to` + `recorded_at`. Supersede, never
  delete. `as_of` queries filter both axes.
- **CP-9 degradation:** every external dependency call is wrapped by a circuit breaker that
  drops to the next rung; the rung is surfaced to the UI, never swallowed.
- **CP-10 correction:** every correction is an attributed, append-only graph edit + an eval
  label. Never anonymous (BR-7).

## Python
- `ruff` + `black` + `mypy` (strict on `backend/app`). Type-safe public boundaries; no bare `Any`.
- Pydantic models for every DTO; DTOs mirror the API spec (Bible §7) exactly.
- Functions do one thing; ports are deep, adapters thin.

## TypeScript
- `eslint` + `prettier` + `tsc` strict. No `any` on public boundaries.
- **UI never hardcodes a colour, size, radius, or motion value** — everything references a
  token from `frontend/src/design/tokens.css`, transcribed from `design.md`. See `ui_rules.md`.
- Every component rendering an AI-derived value must render a confidence reading and ≥1
  citation chip — enforced by the `Claim`/`AnswerCard` component contract (design.md AI rules).

## Naming (Bible §12.2)
- Python `snake_case`/`PascalCase`/`UPPER_SNAKE`. Graph labels `PascalCase`, edges
  `UPPER_SNAKE`, properties `snake_case`. API paths `/kebab-case`, JSON fields `snake_case`.
  Env vars `SENTINEL_<AREA>_<NAME>`.
