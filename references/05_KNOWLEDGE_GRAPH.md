# 05 — Knowledge Graph

> The substrate. Ontology (aligned, not invented), schema, temporal model, entity resolution edges, traversal, and Cypher. Obeys CP-1 (provenance), CP-7 (versioned), CP-8 (own-nothing mirror).

## 5.1 Ontology philosophy — alignment, not invention

Vol 2 §2.2.1 finding: the industry already has an ontology; it is simply not assembled. SENTINEL **aligns** to existing standards rather than inventing a schema — faster to build, credible to a reliability engineer, auditable.

- Failure/asset taxonomy anchor: **ISO 14224** `[V]`.
- Drawing target schema: **DEXPI** `[V]`.
- Integration/level map: **ISA-95 / IEC 62264** `[V]`.
- OT information model alignment: **OPC-UA companion specs** `[V]`.
- Causal edge source: **HAZOP / IEC 61882** records (under-exploited by competitors) `[V]`.

## 5.2 Node (entity) types

| Label | Meaning | Key properties |
|---|---|---|
| `Asset` | Physical equipment (pump, vessel, valve…) | `id, iso14224_class, tag, functional_location` |
| `Identifier` | A name/tag from one source vocabulary | `value, source_system, vocabulary` |
| `Document` | Source artefact | `doc_id, type, version, hash, uri` |
| `Span` | A cited region of a document | `doc_id, page, bbox/char_range` |
| `WorkOrder` | CMMS work order | `wo_id, status, opened, closed` |
| `Inspection` | Inspection/test record | `date, result, method` |
| `FailureMode` | ISO 14224 failure mode | `iso14224_code, description` |
| `Incident` | Near-miss / incident | `date, severity, category` |
| `Obligation` | A regulatory requirement instance | `clause, periodicity, effective_from, effective_to` |
| `Instrument` | Regulatory instrument | `name (OISD/PESO/…), authority` |
| `Person` | Engineer/operator/expert (org memory) | `role, tenure, retirement_risk` |
| `Sensor` | DCS/historian tag | `tag, uom, alarm_limits` |
| `Contradiction` | Surfaced conflict between sources | `about, sources[]` |
| `Correction` | Human correction event (CP-10) | `author, ts, rationale` |

**Reasoning primitives (from the v2 brief, adopted as optional first-class nodes):** `Observation, Hypothesis, Evidence, Decision, Alternative, RiskAccepted, Outcome, LessonLearned`. These make the *decision graph* (§5.7) possible without changing the core. They are additive; the answer path works without them.

## 5.3 Edge (relationship) types

| Type | From → To | Meaning |
|---|---|---|
| `RESOLVED_AS` | Identifier → Asset | this name denotes this asset (the moat edge) |
| `PART_OF` | Asset → Asset | topology / functional location |
| `CONNECTED_TO` | Asset → Asset | process connectivity (from P&ID) |
| `HAS_WORKORDER` | Asset → WorkOrder | maintenance history |
| `EXHIBITS` | Asset → FailureMode | observed/typical failure |
| `EVIDENCED_BY` | * → Span | provenance link (CP-1) |
| `GOVERNS` | Obligation → Asset | which rule attaches where |
| `DEFINED_IN` | Obligation → Instrument | rule source |
| `SUPERSEDES` | Document → Document | version chain (CP-7) |
| `CONTRADICTS` | Span → Span | conflict evidence |
| `CORRECTED_BY` | * → Correction | human fix (CP-10) |
| `KNOWS` | Person → Asset/FailureMode | org-memory / expertise |
| `MONITORS` | Sensor → Asset | instrumentation |

**Every fact-bearing node/edge has ≥1 `EVIDENCED_BY` → Span, or it is not admitted (CP-1).**

## 5.4 Temporal / bitemporal model (CP-7)

Two time axes:
- **Valid time** — when the fact was true in the plant (`effective_from/to`).
- **Transaction time** — when SENTINEL recorded it (`recorded_at`).

Implementation: edges carry both; superseded facts are not deleted but bounded (`effective_to` set, or a new edge with a later `recorded_at`). Any answer can be reconstructed *as-of* a date by filtering both axes. This is what makes "stale graph" (FM-5) survivable and audits reproducible.

## 5.5 Namespaces, multi-tenancy, versioning

- **Multi-tenancy:** tenant id on every node/edge; enterprise scale uses database-per-tenant for hard isolation (see `06`, `08`).
- **Namespaces:** vocabulary namespaces on `Identifier` (`cmms:`, `dms:`, `oem:`, `operator:`).
- **Schema versioning:** ontology changes are migrations (§5.9) with an ADR.

## 5.6 Entity resolution in the graph

The `RESOLVED_AS` edge is the product (Vol 1 secret). Properties: `{confidence, method, adjudicated_by, adjudicated_at, reversible_of}`. A merge creates `RESOLVED_AS` edges from each `Identifier` to a canonical `Asset`; `unmerge` restores the prior `Identifier`↔`Asset` mapping using the recorded event. Human adjudication is the trust anchor (§3.2).

## 5.7 The decision graph (optional, differentiating)

Every significant event can be modelled as a chain:
```
Observation → Hypothesis → Evidence → Decision → {Alternative(rejected)} → RiskAccepted → Outcome → LessonLearned
```
This lets SENTINEL replay *reasoning*, not just a timeline (v2 brief): "why was shutdown rejected then, and would that reasoning still hold today?" Implemented as ordered nodes with `LED_TO` edges, each `EVIDENCED_BY` a span. It is additive and demo-optional; the core investigation works without it.

## 5.8 Traversal & Cypher examples

**Investigation — why is P-101B running hot:**
```cypher
MATCH (id:Identifier {value:'P-101B'})-[:RESOLVED_AS]->(a:Asset)
OPTIONAL MATCH (a)-[:HAS_WORKORDER]->(wo:WorkOrder)
OPTIONAL MATCH (a)-[:EXHIBITS]->(fm:FailureMode)
OPTIONAL MATCH (a)-[:CONNECTED_TO*1..2]->(up:Asset)-[:EXHIBITS]->(upfm:FailureMode)
OPTIONAL MATCH (a)-[:EVIDENCED_BY]->(s:Span)<-[:EVIDENCED_BY]-(note)
WHERE note:Inspection OR note:Incident
RETURN a, collect(distinct wo), collect(distinct fm),
       collect(distinct {upstream:up, mode:upfm}),
       collect(distinct s) LIMIT 50;
```

**Compliance — overdue OISD obligations on an asset:**
```cypher
MATCH (o:Obligation)-[:GOVERNS]->(a:Asset {id:$assetId})
MATCH (o)-[:DEFINED_IN]->(i:Instrument {name:'OISD'})
OPTIONAL MATCH (a)-[:HAS_WORKORDER|:HAS_INSPECTION]->(ev)-[:EVIDENCED_BY]->(:Span)
WITH o, a, max(ev.date) AS last_evidence
WHERE last_evidence IS NULL OR
      last_evidence < date() - duration({months: o.periodicity_months})
RETURN o.clause, a.tag, last_evidence, 'OVERDUE' AS status;
```

**As-of reconstruction:**
```cypher
MATCH (a:Asset {id:$assetId})-[r]->(x)
WHERE r.effective_from <= $asOf
  AND (r.effective_to IS NULL OR r.effective_to > $asOf)
RETURN a, type(r), x;
```

## 5.9 Indexes, performance, migration

- **Indexes:** `Asset.id`, `Identifier.value`, `Document.doc_id`, composite on `(tenant, label)`; full-text index on `Span` text for hybrid retrieval.
- **Performance:** bound traversal hops (`*1..2/3`); precompute hot subgraphs into Redis; read replicas for traversal load.
- **Migration:** ontology changes run as versioned Cypher migrations with dry-run + rollback; every migration has an ADR and a data-fix report. Graph updates are event-driven (from ingestion), never a full rebuild.

## 5.10 Knowledge evolution & decay (v2 concepts, made concrete)

- **Evolution:** a new observation can `STRENGTHEN`/`WEAKEN`/`INVALIDATE` a prior fact via edge-weight updates + `SUPERSEDES`.
- **Decay:** knowledge is flagged stale not by age alone but by triggers — equipment/vendor/SOP change, expert departure, contradictory sensor evidence. A nightly job raises `KnowledgeRisk` flags. This is the mechanism behind the "dangerous/obsolete knowledge" flagging in the v2 brief — implemented as data, not magic.

---

**Red Devil:** *Evans:* "Aligning to ISO 14224/DEXPI is correct DDD — the ubiquitous language already exists. **APPROVED.**" *Kleppmann:* "Bitemporal + supersede-not-delete is right; prove the as-of query in the demo."
**Hackathon Winning:** "The `RESOLVED_AS` edge *is* the pitch. Put the Cypher for the merge on screen. **Strong Winner.**"
**Black Swan:** "The graph models a physical network that outlives retrieval fashions — GraphRAG obsolescence is survivable."
**Green:** knowledge-decay flagging directly serves retention/safety. **Positive.**
