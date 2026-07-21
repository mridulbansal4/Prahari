# Architecture Decisions (build-time)

Decisions made *during* implementation, in addition to the Engineering Bible's ADR-000…015.
Prefixed `ADR-P` ("P" = product build) to avoid collision with the Bible's numbering.
Format: Problem · Alternatives · Chosen · Trade-off · Consequence. Governance: PRB §8.2.

---

## ADR-P05 — Role-based landing dashboards (not one shared dashboard)
- **Problem:** every persona landed on the same Investigation Console. This contradicts
  `design.md` (Dashboard Philosophy: "role-based and opinionated… Operator / Engineer /
  Executive / Investigator views, each with a defined information hierarchy") and the PRB, which
  assigns each persona distinct **Primary modules** (§1.2) and a role→module access matrix (§1.4).
- **Chosen:** a `/home` route that renders a role-specific dashboard — **Operator** (technician
  Ravi: investigate CTA, recent investigations, own drafts), **Reliability** (Meera: resolution
  queue, approvals, corpus, analytics, knowledge risk), **Compliance** (coverage + overdue
  obligations), **Guardian/Admin** (Deepak: system/CP-9 state, audit trail, ingestion, controls),
  and **Auditor** (read-only audit). Each composes only from endpoints the role may call; the
  sidebar was already role-filtered (nav items hidden when access is `none`).
- **Governance:** this is a faithful implementation of an existing `design.md` + PRB requirement,
  not a new feature (PRB §8.1 authority: design.md governs *how* within PRB-specified behavior).
- **Consequence:** each login sees a surface suited to its decisions; no generic dashboard.

## ADR-P07 — Pilot-tier hardening (production stack, OIDC, rate-limit, concurrency, tests)
- **Production profile verified live:** the Neo4j/Qdrant/Postgres adapters were exercised
  end-to-end (`PRAHARI_PROFILE=production`) — seeded + a 6-hop grounded cited investigation.
  Fixes found while doing so: Neo4j 5 requires `RETURN count(n) AS c` (aliasing); the qdrant
  client is pinned `>=1.9,<1.12` to match the server image; **Postgres is published on host 5433**
  in compose to avoid colliding with a locally-installed Postgres on 5432.
- **Real OIDC (Bible §7.2/§8.2):** `OidcIdentityProvider` validates RS256 IdP tokens via JWKS
  (signature + audience + issuer + expiry), config-driven (`PRAHARI_OIDC_*`); selected
  automatically when a JWKS URI is set, else the dev stub. Deny-by-default ABAC unchanged.
- **Rate limiting (Bible §2.7/§7.7):** token-bucket per (tenant,user) at the gateway middleware,
  separate read vs ingestion buckets; `429 rate_limited` + `Retry-After`/`X-RateLimit-Remaining`.
- **Optimistic concurrency + idempotency (Bible §7.6):** proposals carry a `version` → stale
  adjudication returns `409`; work-order submit honours an `Idempotency-Key` (no duplicate CMMS
  write on retry).
- **Tests added:** OIDC (valid/forged), token-bucket, optimistic concurrency, idempotency,
  cross-tenant vector isolation, rule-engine effective-date boundaries, injection abstention.
- **CI re-enabled:** `.github/` is tracked again (reversing the earlier ignore) so the
  lint+tests+eval-gate workflow runs on push/PR.

## ADR-P08 — MVP polish
- Live document ingestion in the Admin console (upload → pipeline → investigable facts).
- Richer provenance-clean corpus (second instrument PESO + asset V-201) — scripted demo paths
  kept deterministic; eval re-verified green after catching a real over-answer regression (the
  entity gate now requires evidence to mention the asked tag, not just a generic word).
- PWA service worker for genuine offline Field Mode (M12/NFR-12).
- `MetricValue` renders numeric readings as the 36px numeral but long strings (e.g. "immediate
  (same session)") in a contained title style — fixes the metric-tile overflow.
- Fixed a React "setState during render" warning (banner update moved out of the stream reducer).

## ADR-P06 — No hardcoded asset ids / signing secret in surfaces
- **Problem:** the Compliance screen pinned `asset-p101b`; the stub auth signing key was a code
  literal.
- **Chosen:** add `GET /v1/assets` (tenant asset lookup) and drive the Compliance asset picker
  from it (default = first asset). Move the dev signing key to `PRAHARI_AUTH_DEV_SECRET`
  (config, default retained for dev; production uses the IdP's JWKS, §8.3).
- **Note (legitimately data-as-code, not violations):** the provenance-clean seed corpus
  (`seed.py`, ADR-012), the demo personas in the stub identity provider (ADR-P04, replaced by
  OIDC in production), and the design-token values in `tokens.css` (the token *source*) are
  intentionally in code and are not "hardcoding" in the CP-5/CP-6 sense.

---

## ADR-P01 — Embedded adapter family as the default runnable profile
- **Problem:** The Bible names Neo4j/Qdrant/Postgres/Redis + a cloud LLM. Requiring all five
  services + an API key + GPU OCR models just to *run* the demo contradicts the hackathon MVP
  goal ("Docker Compose, one box", PRB §5.3) and the air-gap requirement (Bible §8.6).
- **Alternatives:** (a) hard-require the full store topology; (b) mock the stores.
- **Chosen:** Implement every store **port** (Bible §2.4) with two adapters — an *embedded*
  family (NetworkX / local cosine index / SQLite / in-process cache / offline template
  synthesizer) selected by `PRAHARI_PROFILE=embedded` (default), and a *production* family
  (Neo4j/Qdrant/Postgres/Redis/LLM) selected by `PRAHARI_PROFILE=production`.
- **Why this is not a mock (governance-critical):** The embedded family *is* the Bible's
  mandated local fallback that "doubles as the air-gap mode" (ADR-007, §8.6) and the lower
  rungs of the CP-9 degradation ladder (§2.8). It is a first-class product state, styled and
  labelled, not a placeholder. The production adapters implement the identical port contract.
- **Trade-off:** two adapters per store to maintain; embedded recall/latency are lower.
- **Consequence:** `git clone && seed && run` works with no external dependency; the CP-9
  ladder and air-gap story are demonstrable by construction, not asserted.

## ADR-P02 — Offline template synthesizer is the model's degradation rung, not the default answer engine
- **Problem:** Investigations must be deterministic on the seeded corpus for the demo (Bible
  §11.7) and must work with no API key, yet CP-5 requires a real provider abstraction.
- **Chosen:** `IModelProvider` has three concrete providers: `GeminiProvider` (the primary
  reasoning model, used when `PRAHARI_GEMINI_API_KEY` is set), `LocalOpenWeightsProvider`
  (air-gap), and `TemplateSynthProvider` (the CP-9 `-model` rung — structured, grounded, no
  prose). A single hosted provider keeps the abstraction honest without carrying vendors the
  product does not ship against; a second one is a class plus a router branch. Selection
  and fallback are driven by the circuit breaker (Bible §2.7). The template synthesizer only
  ever emits claims that map to a provided context span, so grounding/citation invariants hold
  even at the lowest rung.
- **Consequence:** Faithfulness/citation gates (NFR-5/6) are enforceable even offline; the
  Verifier's abstention path is exercised identically regardless of provider.

## ADR-P03 — Graphics extraction (YOLO/Relationformer P&ID) is capability-flagged, not on the critical path
- **Problem:** The Bible lists YOLO + Relationformer for P&ID symbol/line extraction. These
  require model weights and GPU and are **not** on the PRB critical path (ingestion →
  resolution → investigation → correction; §5.4). The PRB's ingestion Must-scope is
  PDF/scan/CSV/DCS-export entity+relation extraction (FR-1).
- **Chosen:** Ingestion pipeline stages are pluggable `IExtractor`s. The P&ID graphics stage is
  present as an interface + a deterministic DEXPI-shaped stub extractor that reads pre-provided
  structured P&ID topology from the demo corpus, behind the `pid_graphics` capability flag
  (default off). No fabricated detections.
- **Governance:** This does not remove or reorder a PRB requirement — FR-1 is satisfied for the
  Must document classes; P&ID graphics detection is a `[V]`-tool Could-enhancement (Bible §3.1)
  logged here rather than silently dropped or silently faked (BR-1: never promote a fabricated
  extraction to a fact).

## ADR-P04 — Auth is a role-stub in embedded profile, full OIDC/ABAC in production
- **Problem:** PRB §5.3 hackathon MVP = "single-tenant, role stub"; enterprise = full
  RBAC/ABAC/OIDC/multi-tenant. Both must be true of one codebase.
- **Chosen:** The gateway's `IIdentityProvider` has a `StubIdentityProvider` (signed dev JWT,
  role chosen at login, single tenant `demo`) and an `OidcIdentityProvider` (validates IdP
  token signature/audience/expiry). ABAC policy evaluation (Bible §8.2) runs in-service in
  **both** profiles — deny-by-default is never stubbed, because the write-gating invariant
  (CP-3) and cross-tenant isolation (§8.1) must hold even in the demo.
- **Consequence:** The security posture (gated writes, ABAC, audit) is demonstrable in the
  hackathon build; only the *identity source* is stubbed, per PRB scope.
