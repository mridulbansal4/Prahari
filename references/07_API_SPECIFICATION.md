# 07 — API Specification

> REST + WebSocket contracts, DTOs, errors, auth, versioning. Contract-first: this file is the source for the OpenAPI document. Obeys CP-2 (citations in responses), CP-3 (gated writes), CP-4 (abstain shape).

## 7.1 Conventions

- Base path `/v1`. Versioned by URL; breaking changes → `/v2`.
- JSON only; `Content-Type: application/json`. Streaming via WebSocket / SSE.
- All requests authenticated (OIDC bearer). All responses carry `X-Request-Id`.
- Timestamps ISO-8601 UTC. IDs are UUIDv4 unless noted.
- Pagination: cursor-based (`?limit=&cursor=`), `next_cursor` in response.

## 7.2 Auth

- **OIDC** bearer token from the customer IdP; gateway validates signature + audience.
- **RBAC** coarse check at gateway; **ABAC** fine check in-service (`08`).
- Write endpoints require an `approver` identity in the body (CP-3); the token subject alone is insufficient.

## 7.3 Core resources & endpoints

### Investigations
```
POST /v1/investigations
  body: { question: string, as_of?: date, context?: {asset_id?} }
  → 202 { investigation_id }           # async; stream via WS
GET  /v1/investigations/{id}
  → 200 InvestigationResult
```

`InvestigationResult` (DTO):
```json
{
  "investigation_id": "uuid",
  "question": "why is P-101B running hot?",
  "as_of": "2026-07-18",
  "abstained": false,
  "answer": "…",
  "claims": [
    { "text": "…", "confidence": "grounded|inferred|unsupported",
      "citations": [ { "doc_id":"…","page":14,"span_id":"…" } ] }
  ],
  "graph_path": [ { "node":"Asset:P-101B" }, { "edge":"CONNECTED_TO" }, { "node":"Strainer:S-14" } ],
  "unresolved": [],
  "who_to_ask": [ { "person":"Anil", "expertise":"strainer fouling" } ]  // present when abstained
}
```

### Ingestion
```
POST /v1/documents            # multipart upload → blob + enqueue
  → 202 { doc_id, job_id }
GET  /v1/documents/{doc_id}   # metadata + ingestion status
GET  /v1/ingestion/{job_id}   # stage/status/attempts
```

### Entity resolution
```
GET  /v1/resolution/queue                 # pending merge proposals (medium-confidence)
POST /v1/resolution/{proposal_id}/adjudicate
  body: { decision: "merge"|"separate", note?: string, approver: uuid }
  → 200 { resulting_asset_id, reversible_id }
POST /v1/resolution/unmerge/{merge_id}     # reversibility (BR-4)
```

### Compliance
```
GET /v1/compliance/assets/{asset_id}       # obligations: satisfied/due/overdue + evidence
GET /v1/compliance/coverage                # which clauses are ENCODED vs NOT (FM-6)
```

### Actions (gated writes, CP-3)
```
POST /v1/actions/work-order/draft
  body: { asset_id, symptom, hypothesis_id }
  → 200 { draft_id, preview }
POST /v1/actions/work-order/submit
  body: { draft_id, approver: uuid }
  → 201 { cmms_work_order_id }             # writes to CMMS system of record
```

### Corrections (CP-10)
```
POST /v1/corrections
  body: { target_kind, target_ref, new_value, rationale, author: uuid }
  → 201 { correction_id }                  # persists edit + labels eval example
```

### Audit
```
GET /v1/audit?actor=&action=&from=&to=     # append-only log (admin/Deepak)
```

## 7.4 WebSocket streaming

```
WS /v1/stream/investigations/{id}
  server → client events:
    { "type":"token", "text":"…" }
    { "type":"claim", "claim":{…} }
    { "type":"graph_hop", "hop":{…} }
    { "type":"verdict", "abstained":bool }
    { "type":"done" }
```
Streaming lets the UI render the traversal *as it happens* (Vol 1 §1.8: show the traversal, not just the answer).

## 7.5 Error model

```json
{ "error": { "code":"string", "message":"human readable", "request_id":"…", "details":{} } }
```

| HTTP | code | Meaning |
|---|---|---|
| 400 | `invalid_request` | DTO validation failed |
| 401 | `unauthenticated` | missing/invalid token |
| 403 | `forbidden` | RBAC/ABAC denied |
| 409 | `conflict` | e.g. duplicate document hash |
| 422 | `ungrounded` | answer stripped to abstain (not an error to the user, but signalled) |
| 429 | `rate_limited` | token bucket exceeded |
| 503 | `degraded` | operating on a lower rung of CP-9 ladder (response still useful) |

`503 degraded` returns a *partial useful answer* with a `degradation_level` field — never an empty failure (CP-9).

## 7.6 Idempotency & concurrency

- Uploads idempotent by content hash (409 on duplicate; returns existing `doc_id`).
- Write actions carry an `Idempotency-Key` header.
- Optimistic concurrency on corrections/merges via `version` field; 409 on stale write.

## 7.7 Rate limiting & quotas

Token-bucket per `(tenant, user)` at the gateway; separate buckets for read vs ingestion; headers `X-RateLimit-Remaining`, `Retry-After`.

## 7.8 OpenAPI

The machine-readable contract is generated from FastAPI models and published at `/v1/openapi.json`. This markdown is the human contract; the two must agree in CI (`14`).

## 7.9 gRPC (enterprise, deferred)

Internal service-to-service calls become gRPC when the monolith is split (ADR-007). Not on the hackathon path — recorded in `17`.

---

**Red Devil:** *Newman:* "Contract-first with a `503 degraded` that still returns value is the right resilience contract. **APPROVED.**" *Fowler:* "Idempotency keys + optimistic concurrency on merges — correct."
**Hackathon Winning:** "The streaming `graph_hop` event is what makes the traversal visible live. **Strong Winner.**"
**Black Swan:** versioned URL + provider-abstract writes → contract stable across model/vendor change. **Survivable.**
**Green:** cursor pagination + streaming reduce over-fetch. **Positive.**
