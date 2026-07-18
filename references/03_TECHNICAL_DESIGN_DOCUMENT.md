# 03 — Technical Design Document (TDD)

> The cross-cutting "how it actually works" doc: ingestion internals, retrieval router, context assembly, agent runtime wiring. Where `02` gives the shape, `03` gives the mechanism.

## 3.1 Ingestion pipeline (the place the engineering effort goes)

Rationale (Vol 1 §1.4): the data mess is steady-state, so ingestion — not the chat layer — is the hard part. The pipeline is a DAG of idempotent stages, each stamping provenance.

### 3.1.1 Stages

| Stage | Tool `[V]` existence | Output | Confidence source |
|---|---|---|---|
| Detect | libmagic / mime | doc type | deterministic |
| Parse | **Docling** | layout tree, text blocks, tables | parser score |
| OCR (scans) | **PaddleOCR** | text + bbox | OCR conf per token |
| Graphics (P&ID) | **YOLO** (symbols) + **Relationformer** (connections) | equipment/instrument nodes + line topology → DEXPI-shaped | detector conf |
| Entity extract | LLM + rules | typed entities w/ spans | model + rule agreement |
| Relation extract | LLM + graph patterns | typed edges w/ spans | model + pattern conf |
| Provenance | internal | `{doc,page,bbox/span,method,confidence,extractor_version}` | — |
| Resolution | Entity Resolution svc | merge proposals | resolver score |

### 3.1.2 Idempotency & versioning
Each stage keyed by `(doc_id, doc_hash, extractor_version)`. Re-running with a new extractor version produces a **new** provenance record and a supersession edge — never an overwrite (CP-1, CP-7). A re-uploaded document with a changed hash becomes a new version linked by `SUPERSEDES`.

### 3.1.3 Confidence gating
- ≥ 0.85 → auto-write to graph.
- 0.6–0.85 → written but flagged `provisional`; surfaced in adjudication queue.
- < 0.6 → not admitted (BR-1); retained in a "low-confidence extraction" table for review.

## 3.2 Entity resolution (the moat, mechanically)

**Problem restated:** P-101B, "Boiler Feed Pump B", OEM model no., "the noisy one", and a smudged tag on sheet 14 are one physical object across four vocabularies (Vol 1 Principle 2).

**Pipeline:**
1. **Blocking** — candidate generation via normalized tag patterns, fuzzy string (Jaro-Winkler), and embedding proximity of surrounding context.
2. **Scoring** — a weighted feature vector: tag-pattern match, spatial co-location on a drawing, shared work-order history, functional-role match (ISO 14224 class), embedding similarity. Score → calibrated probability.
3. **Decision** — high (auto-merge) / medium (queue for human) / low (keep separate).
4. **Adjudication** — human confirms/corrects; the decision writes an attributed `RESOLVED_AS` edge and a labelled training example (CP-10).
5. **Reversibility** — every merge is a recorded event; `unmerge(merge_id)` restores prior state (BR-4). This is why FM-1 (wrong-asset merge) is *survivable*: the error is in the substrate but it is versioned and reversible.

**Why humans in the loop, not full-auto:** a wrongly-merged node yields a perfectly-cited answer about the *wrong pump* — undetectable by any model-side QC (Vol 3 FM-1). Human adjudication + reversibility is the only defence.

## 3.3 Retrieval router (dual GraphRAG + vector)

### 3.3.1 Query classification
A lightweight classifier (rules + small model) routes each query:

| Query shape | Route | Example |
|---|---|---|
| Single-fact / definitional | **vector** | "what is the design pressure of V-201?" |
| Multi-hop / causal / relational | **graph-first**, vector to enrich spans | "why is P-101B running hot?" |
| Compliance / obligation | **graph + rule engine** | "which OISD inspections are overdue?" |
| Ambiguous | **hybrid** (both, reranked) | default |

### 3.3.2 Graph retrieval
Parameterised Cypher templates (see `05`) expand from anchor entities across bounded hops with typed edges, returning subgraphs plus the source spans attached to each node/edge.

### 3.3.3 Vector retrieval
Qdrant semantic search over document spans; results are **grounding evidence**, not answers. Each hit carries `{doc,page,span}` for citation.

### 3.3.4 Fusion & rerank
Graph subgraph + vector spans → deduped, reranked by (relevance × provenance-confidence × recency-as-of). Context budget enforced by a compression pass (§3.5).

## 3.4 Context assembly

Assembled context block = `{resolved question, entity cards (from graph), evidence spans (cited), prior corrections (org memory), as-of timestamp}`. Every span carries its citation id so the generator can only cite what it was given (enables CP-2 verification post-hoc).

## 3.5 Long-context & compression strategy

- **Semantic cache** (Redis): `hash(normalized_question + as_of + tenant)` → answer+citations; TTL + invalidation on relevant graph writes.
- **Compression:** map-reduce summarisation of low-salience spans; high-salience spans (those matching entity anchors) passed verbatim to preserve citation fidelity.
- **Budgeting:** hard token ceiling; router prefers *fewer, higher-provenance* spans over many weak ones (silence over noise, Vol 1 §1.8).

## 3.6 Agent runtime wiring (detail lives in `04`)

Orchestrator = a **LangGraph** state machine: `plan → retrieve → draft → critic → verify → (answer | abstain | correct)`. Tools are MCP-exposed functions with typed schemas. State is checkpointed to Redis so a run is resumable and auditable.

## 3.7 Prompt & template management

- Prompts are versioned files (`prompts/<agent>/<name>@vN.md`) with a manifest; the manifest hash is logged with every answer for reproducibility (CP-7).
- No statute, rule, or tenant value is hardcoded in a prompt (CP-5, CP-6).

## 3.8 Error taxonomy (internal)

| Class | Example | Handling |
|---|---|---|
| Transient | model timeout, DB blip | retry+backoff → circuit breaker → fallback |
| Data | unparseable doc, OCR failure | quarantine, flag, never fabricate |
| Grounding | draft claim without support | strip claim or abstain (CP-2/CP-4) |
| Resolution | ambiguous merge | queue for human, do not guess |
| Authorization | write without approver | reject, audit (CP-3) |

## 3.9 Technology choices (summary; full ADRs in `13`)

| Concern | Choice | Alt rejected | Why |
|---|---|---|---|
| Graph DB | Neo4j | Postgres+ltree, Neptune | mature Cypher, temporal patterns, local deploy |
| Vector DB | Qdrant | pgvector, Milvus | filtered search, local, fast, payloads |
| Relational | Postgres | MySQL | JSONB, extensions, audit tables |
| Cache/queue | Redis (+Streams) | Kafka, RabbitMQ | one dependency does cache+queue at MVP scale |
| Orchestration | LangGraph | bespoke, CrewAI | explicit state machine, checkpointing, auditability |
| Extraction | Docling+PaddleOCR+YOLO/Relationformer | cloud OCR | local/air-gap-capable, OSS, in-window originality |
| Backend | Python (FastAPI) | Node, Go | AI ecosystem, speed of build |
| Frontend | React + TS | — | `10` |

---

**Red Devil:** *Ousterhout:* "Ports are deep modules; ingestion complexity is contained behind `IExtractor`. **APPROVED.**" *Karpathy:* "Verifier-before-answer is the right default; prove it in `15`."
**Hackathon Winning:** "Confidence gating (auto/provisional/reject) is a great whiteboard answer to 'how do you avoid garbage in the graph?' **Strong Winner.**"
**Black Swan:** local-capable extraction removes cloud-OCR dependency risk. **Survivable.**
**Green:** compression reduces tokens → energy; verifier reduces rework. **Positive.**
