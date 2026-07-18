# 14 — Testing & Engineering Checklists

> Test strategy across the pyramid + the specialised AI/graph tests, plus production/security/deployment/demo/PR checklists. Eval-specific harness is in `15`; this file is functional correctness and process gates.

## 14.1 Test strategy (the pyramid, plus two AI layers)

```
                 ┌────────────────────────┐
                 │  Eval harness (15)      │  faithfulness, citation, abstention
                 ├────────────────────────┤
                 │  E2E / demo-path tests  │  the exact scripted flow
                 ├────────────────────────┤
                 │  Integration tests      │  stores, retrieval, ingestion, API
                 ├────────────────────────┤
                 │  Unit tests             │  domain logic, rule engine, resolver
                 └────────────────────────┘
```

## 14.2 Unit tests

- **Rule engine:** given graph state + rule, assert satisfied/due/overdue correct across effective-date boundaries.
- **Resolver:** scoring monotonicity; merge/unmerge round-trips restore prior state (BR-4).
- **Provenance sink:** rejects unsourced writes (CP-1).
- **Verifier:** strips uncited claims; abstains when stripping leaves an incomplete answer (CP-2/CP-4).
- **Temporal queries:** as-of reconstruction returns the correct historical state (CP-7).

## 14.3 Integration tests

- Ingestion DAG: upload → parse → ocr → extract → provenance → graph write, with a known fixture document and asserted node/edge counts + spans.
- Retrieval router: each query class routes correctly; graph+vector fusion returns cited spans.
- API contracts: every endpoint validated against the OpenAPI schema; **OpenAPI ↔ markdown (`07`) must agree** (drift test).
- Gated write: submit without approver → 403 + audit entry (CP-3).

## 14.4 AI/graph-specific tests

- **Grounding:** every claim in a sampled answer maps to a provided span (property test).
- **Injection:** ingested document containing an instruction ("ignore previous…") must not change tool behaviour (FM-7 regression test).
- **Abstention:** graph-disabled query abstains and returns who-to-ask (CP-4 + CP-9).
- **Cross-tenant:** a user of tenant A can never retrieve tenant B spans (isolation test).
- **Determinism of demo path:** scripted questions return stable, cited answers against the seeded corpus.

## 14.5 Non-functional tests

- Load: P95 latency under target RPS (NFR-1); ingestion under burst adds workers not latency.
- Chaos-lite: kill the model provider → degradation ladder engages, response still useful (CP-9).
- Backup/restore drill: rebuild Qdrant+Redis from sources of truth (`06`).

---

## 14.6 Production Readiness Checklist

- [ ] Health/readiness probes on every service (`09`)
- [ ] Metrics + traces + structured logs with correlation ids
- [ ] AI SLIs dashboarded (grounding, citation, abstention, resolution-queue depth)
- [ ] Alerts wired (latency, queue lag, DLQ, abstention spike, degradation persistence)
- [ ] Backups scheduled + a restore drill passed
- [ ] Secrets in vault; none in repo/images
- [ ] Rate limits + backpressure verified under load
- [ ] Degradation ladder tested end-to-end
- [ ] Eval thresholds green (`15`)

## 14.7 Security Checklist

- [ ] OIDC validated at gateway; deny-by-default ABAC in-service
- [ ] Every write requires + audits an approver (CP-3)
- [ ] Append-only audit (UPDATE/DELETE revoked)
- [ ] TLS external, mTLS internal, encryption at rest
- [ ] Prompt-injection regression test passing (FM-7)
- [ ] Cross-tenant isolation test passing
- [ ] Air-gap build has zero answer-path egress
- [ ] SBOM generated; OSS-only; provenance log complete

## 14.8 Deployment Checklist

- [ ] Same images across compose/staging/prod
- [ ] `local-model` profile builds and serves
- [ ] Migrations dry-run + rollback tested (pg + neo4j)
- [ ] Feature flags set correctly per environment
- [ ] Air-gap bundle signed + verify-on-install tested

## 14.9 Demo Checklist (`11`)

- [ ] Seeded corpus loads; 4→1 resolution lands deterministically
- [ ] 5-hop investigation returns cited chain
- [ ] Compliance matrix shows the overdue OISD item + coverage footer
- [ ] Gated work-order write path works + audited
- [ ] Graph-disabled refusal path works (the closing move)
- [ ] Semantic cache pre-warmed for scripted questions
- [ ] Offline recording + backup device ready
- [ ] Network-cable-pulled dry run passed

## 14.10 Architecture Checklist

- [ ] Every port has exactly one adapter + a stated extraction seam
- [ ] No I/O in domain logic
- [ ] Every fact write passes the provenance sink
- [ ] CP-1…CP-10 each map to an enforcing mechanism

## 14.11 PR / Code Review Checklist

- [ ] CI green (lint, type, unit, eval-smoke)
- [ ] Tests added/updated; determinism preserved on demo path
- [ ] Provenance preserved; new writes gated
- [ ] ADR written if a decision was made
- [ ] Docs/OpenAPI updated; no drift
- [ ] No secrets; no `any`/untyped public boundary
- [ ] Feature-flagged if not in the Must scope

---

**Red Devil:** *Beck:* "The two AI layers on top of the pyramid (injection + abstention as tests, not hopes) is the mature move. **APPROVED.**"
**Hackathon Winning:** "The demo checklist including 'network-cable-pulled dry run' is why you won't panic on stage. Strong Winner."
**Black Swan:** chaos-lite + restore drill = survivability proven, not asserted. **Survivable.**
**Green:** regression gates prevent wasteful rework. **Positive.**
