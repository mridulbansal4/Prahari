# 13 — Engineering Decisions (ADRs)

> One record per important decision: Problem, Alternatives, Evaluation, Rejected, Chosen, Trade-offs, Consequences, Future impact. Status: Accepted unless noted.

---

## ADR-000 — Evidence tiers `[V]/[R]/[D]`
- **Problem:** a single unlabelled invented statistic discredits the whole pitch.
- **Alternatives:** cite everything (impractical); cite nothing (not credible).
- **Chosen:** three-tier labelling inline, references in `18`.
- **Trade-off:** verbosity for credibility. **Consequence:** a probed number becomes a credibility *win*, not a loss.

## ADR-001 — Knowledge graph as the substrate (not vector-only)
- **Problem:** industrial questions need *connected* facts, not *similar* text.
- **Alternatives:** pure vector RAG; relational joins; graph.
- **Evaluation:** vector retrieves similarity, not connection (Vol 1 wrong-assumption table); relational can't cheaply do multi-hop over heterogeneous entities.
- **Chosen:** Neo4j knowledge graph + vector as enrichment (dual retrieval).
- **Trade-off:** graph ops complexity. **Future impact:** graph models a physical network that outlives retrieval fashions (Black Swan survivability).

## ADR-002 — Ontology by alignment (ISO 14224/DEXPI/ISA-95), not invention
- **Problem:** a bespoke taxonomy is slow, unauditable, and alien to reliability engineers.
- **Chosen:** align to existing standards `[V]`.
- **Trade-off:** must learn the standards. **Consequence:** speaks the buyer's language day one; RCA auditable against a standard.

## ADR-003 — Human-adjudicated, reversible entity resolution
- **Problem:** a wrongly-merged node yields a perfectly-cited answer about the wrong asset (FM-1) — undetectable by model-side QC.
- **Alternatives:** full-auto merge; no merge.
- **Chosen:** auto high-confidence, human-adjudicate medium, always reversible + versioned.
- **Trade-off:** human-in-loop latency. **Consequence:** the moat corpus forms as a by-product; FM-1 becomes survivable.

## ADR-004 — Grounding + abstention as first-class outputs (CP-2/CP-4)
- **Problem:** in a plant a wrong answer is worse than none (Principle 5).
- **Chosen:** verifier strips uncited claims; abstention is a scored success.
- **Trade-off:** lower answer-coverage. **Consequence:** deployable in safety contexts; the demo's closing move.

## ADR-005 — Rules as data, not code (CP-6)
- **Problem:** regulation churns (DGMS circulars, state rules); statutes in `.py` are unmaintainable and un-versionable.
- **Chosen:** declarative rule library with effective-date ranges; regulation-agnostic engine.
- **Consequence:** same engine serves OSHA/ATEX later without a rewrite; rule churn becomes a *reason to buy*.

## ADR-006 — Modular monolith now, extract to services later
- **Problem:** a 4-person team can't operate microservices in 4 days.
- **Chosen:** modular monolith with ports as extraction seams.
- **Trade-off:** shared deploy. **Future impact:** ingestion + inference workers extract first (recorded, not built).

## ADR-007 — Provider-abstracted model + local fallback (CP-5, CP-9)
- **Problem:** vendor lock-in risk; air-gap requirement; model-cost volatility.
- **Chosen:** provider abstraction; default cloud reasoning model; local open-weights fallback that *is* the air-gap mode.
- **Consequence:** model shocks are a tailwind; air-gap and degradation are one design.

## ADR-008 — Polyglot persistence with derived stores
- **Problem:** one store can't be good at graph, vectors, relational, and cache.
- **Chosen:** Postgres+Neo4j = sources of truth; Qdrant+Redis = derived/rebuildable.
- **Trade-off:** operational surface. **Consequence:** true backup surface shrinks to the two sources of truth.

## ADR-009 — Bitemporal graph (CP-7)
- **Problem:** stale-graph answers (FM-5); audits must be reproducible.
- **Chosen:** valid-time + transaction-time on edges; supersede, never delete.
- **Consequence:** any answer reconstructable as-of its date; FM-5 mitigated.

## ADR-010 — Gated writes only (CP-3)
- **Problem:** autonomous writes to a CMMS in a plant are unacceptable.
- **Chosen:** propose-then-approve tool layer; approver identity audited.
- **Consequence:** compliance/security veto (Deepak) is pre-answered.

## ADR-011 — Ingested content is data, never instruction
- **Problem:** prompt injection via ingested documents (FM-7) — the product's input *is* the attack surface.
- **Chosen:** strict data/instruction separation; tools gated; no answer-path egress.
- **Consequence:** the document-ingestion product's worst threat is designed against, not disclaimed.

## ADR-012 — Public-source demo corpus only
- **Problem:** hackathon originality rules + no real plant data available.
- **Chosen:** curated public-source corpus with provenance; never fabricate-and-present-as-real.
- **Consequence:** originality challenge and credibility challenge both pre-answered.

## ADR-013 — Mobile-first PWA (not native)
- **Problem:** primary user is in the field; native app = store dependency + build cost.
- **Chosen:** installable, offline-capable PWA.
- **Trade-off:** some native-API limits. **Consequence:** offline path doubles as the CP-9 field mode.

## ADR-014 — Eval as a deploy gate
- **Problem:** AI quality silently regresses.
- **Chosen:** RAGAS/DeepEval thresholds block merges/deploys.
- **Consequence:** quality is enforced by the pipeline (`12`, `15`).

## ADR-015 — Decision graph is additive, demo-optional
- **Problem:** the v2 "reasoning graph" is compelling but must not endanger the core.
- **Chosen:** reasoning primitives (Observation…LessonLearned) as *additive* nodes; core investigation works without them.
- **Consequence:** category-defining narrative available without core risk.

---

**Red Devil:** "Each ADR names the rejected option and the debt. This is the volume that separates engineers from demo-builders. **APPROVED.**"
**Hackathon Winning:** "ADR-003 and ADR-004 are the two that win Q&A. Rehearse them."
**Black Swan:** ADR-007/008/013 are the survivability spine. **Survivable.**
**Green:** ADR-014 prevents wasteful regressions. **Positive.**
