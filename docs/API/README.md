# API Documentation

The contract-first API surface (Bible §7). The **human contract** is
[`references/07_API_SPECIFICATION.md`](../../references/07_API_SPECIFICATION.md); the
**machine-readable OpenAPI** document is generated from the FastAPI models and served live at:

```
GET http://localhost:8000/v1/openapi.json      # OpenAPI schema
GET http://localhost:8000/docs                  # interactive Swagger UI
```

The two must agree in CI (Bible §7.8, §14.3 drift test).

## Resource map (Bible §7.3)

| Area | Endpoints | Module |
|---|---|---|
| Auth / shell | `POST /v1/auth/login`, `GET /v1/auth/me` | Global Shell |
| Investigations | `POST /v1/investigations`, `GET /v1/investigations/{id}`, `WS /v1/stream/investigations/{id}` | M1 |
| Resolution | `GET /v1/resolution/queue`, `POST /v1/resolution/{id}/adjudicate`, `POST /v1/resolution/unmerge/{id}` | M2 |
| Ingestion | `POST /v1/documents`, `GET /v1/ingestion/{job_id}` | M11 |
| Compliance | `GET /v1/compliance/assets/{id}`, `GET /v1/compliance/coverage` | M6 |
| Actions (gated) | `POST /v1/actions/work-order/draft`, `POST /v1/actions/work-order/submit` | M7 |
| Corrections | `POST /v1/corrections`, `GET /v1/corrections` | M8 |
| Audit | `GET /v1/audit` | M9 |
| Analytics · Org memory · Knowledge · Decisions | `GET /v1/analytics`, `/v1/org-memory`, `/v1/knowledge/health`, `/v1/decisions` | M10/M5/M4/M3 |

## Conventions
- Base path `/v1`; JSON only; OIDC bearer auth; `X-Request-Id` on every response.
- Write endpoints require an `approver` identity (CP-3). Streaming via WebSocket (Bible §7.4).
- Error model: `{ "error": { "code", "message", "request_id", "details" } }` (Bible §7.5).
- `503 degraded` returns a partial-but-useful answer with `degradation_level` (CP-9), never an
  empty failure.
