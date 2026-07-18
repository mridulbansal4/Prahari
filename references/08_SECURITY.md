# 08 — Security

> Written for Deepak (OT security, veto power) before he asks. Threat model, RBAC/ABAC, secrets, encryption, audit, air-gap, zero-trust, residency. This volume is what turns a demo into a pilot.

## 8.1 Threat model (STRIDE, abridged)

| Threat | Vector | Control |
|---|---|---|
| **Spoofing** | forged identity | OIDC + short-lived tokens; mTLS between internal components |
| **Tampering** | altered graph/audit | append-only audit (revoked UPDATE/DELETE); provenance on every fact |
| **Repudiation** | "I didn't approve that write" | approver identity required + audited (CP-3) |
| **Information disclosure** | cross-tenant leak | tenant id on every record; DB-per-tenant at enterprise; filtered vector search |
| **Denial of service** | ingestion flood | rate limit + backpressure + bulkheads |
| **Elevation of privilege** | ABAC bypass | deny-by-default; policy evaluated in-service, not just at gateway |
| **Prompt injection** | malicious text in ingested doc | ingested content is data, never instruction; tools gated; no answer-path egress (FM-7) |
| **Data exfiltration** | agent sends data out | egress disallowed on answer path; write tools gated + audited |

**The two threats every other team ignores:** prompt injection *via ingested documents* (the product's own input is the attack surface) and *cross-tenant graph leakage*. Both are designed against here, not disclaimed.

## 8.2 AuthN / AuthZ

- **AuthN:** OIDC (customer IdP: Azure AD / Keycloak). Tokens validated at the gateway (signature, audience, expiry).
- **RBAC (coarse):** roles `technician | reliability | compliance | admin | auditor`. Checked at gateway.
- **ABAC (fine):** attribute predicates evaluated in-service — e.g. `user.site == asset.site`, `user.clearance >= document.classification`. Deny-by-default.
- **Write authorisation:** every mutation of a system of record requires an `approver` whose role permits it *and* who is distinct-or-same-with-authority per policy (CP-3).

Policy example (declarative):
```
allow read Document if user.tenant == doc.tenant
                    and user.site in doc.sites
                    and user.clearance >= doc.classification
allow submit WorkOrder if user.role in {technician, reliability}
                       and approver.role in {reliability, admin}
default deny
```

## 8.3 Secrets management

- Secrets in a vault (HashiCorp Vault / cloud KMS); never in env files committed to the repo.
- Short-lived DB/service credentials via dynamic secrets where available.
- Model provider keys held server-side only; never sent to the client (also the rule for any AI-in-artifact demos).

## 8.4 Encryption

- **In transit:** TLS 1.2+ external; mTLS internal.
- **At rest:** disk/volume encryption for all stores; blob encrypted; backups encrypted.
- **Field-level:** PII on `Person` nodes and audit details encrypted with tenant-scoped keys.

## 8.5 Audit & provenance

- Append-only `audit_log` (`06`): every read, answer, proposed write, committed write.
- Every answer logs `{question, context span_ids, prompt manifest hash, model id, verdict}` — reproducibility (CP-7) + forensic trail.
- Provenance (CP-1) means every fact is traceable to a source span and, if human-touched, to a named person + timestamp.

## 8.6 Air-gapped design

Named because the wedge is Indian regulated industry, where air-gap is common.
- All stores run locally; no external network dependency on the answer path.
- Model served by a **local open-weights model** (degradation-quality but functional) — the CP-9 fallback doubles as the air-gap mode.
- Embeddings local; OCR/extraction local (Docling/PaddleOCR/YOLO are OSS, run offline).
- Updates (rule library, model weights) delivered via signed offline packages, verified before install.

## 8.7 Zero-trust posture

- No implicit trust between components; every internal call authenticated (mTLS + service identity).
- Least privilege: each component gets only the DB/tool scopes it needs (bulkheads).
- Network segmentation: ingestion workers cannot reach the internet; only the (optional) model egress path is allowed, and it is disabled in air-gap.

## 8.8 Data residency

- Residency recorded per tenant (`06.tenant.data_residency`); enforced by deployment topology (region-pinned or air-gap).
- No cross-region replication unless the tenant's residency policy allows it.
- PII minimisation: SENTINEL stores expertise relationships, not HR records.

## 8.9 Supply-chain & originality (hackathon-specific)

- OSS-only dependencies; dependency manifest + provenance log (hackathon originality rule).
- All code authored in-window; no pre-built project imported (Vol 0.5 constraint).
- SBOM generated in CI (`14`).

## 8.10 Compliance posture (product, not legal)

SENTINEL evaluates encoded rules against graph state and produces **evidence + gaps**, attributed to a clause (BR-3). It **never** renders a legal opinion and **never implies completeness** — it reports which clauses are encoded vs not (FM-6). This is the only defensible position and it is what keeps the compliance pillar an asset rather than a liability.

---

**Red Devil:** *Principal Security Engineer:* "Prompt-injection-via-ingest and cross-tenant leakage are named as the top two — most teams name neither. Air-gap = fallback = one design is elegant. **APPROVED.**" *Schneier-lens:* "Append-only audit + provenance + approver identity closes repudiation."
**Hackathon Winning:** "Deepak's veto is pre-answered. 'How do you prevent data leaving the plant?' → local model + no answer-path egress. **Strong Winner.**"
**Black Swan:** local-capable stack → cloud/vendor outage or ban is survivable. **Survivable.**
**Green:** minimal PII, local compute option. **Positive.**
