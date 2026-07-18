# Prahari — Product Requirements Bible (PRB)

**Version 1.0 — 18 July 2026**
**Status:** Locked draft, pending Red Devil + Hackathon Winning + Black Swan + Green council sign-off
**Document type:** Product Requirements Bible — the single source of truth for *what Prahari is and does*. Not an architecture document. Not a PRD in the generic sense — the definitive product contract from which the PRD, the design system, the engineering plan, the test plan, and the demo script are all derived.

---

## How to read this document (authority order)

Three documents govern Prahari. They do not compete — each is supreme in its own domain, and this section is the tie-breaker if anyone ever thinks they conflict.

| Document | Is the supreme authority for… | Is NOT the authority for… |
|---|---|---|
| **This PRB** | What exists: every screen, workflow, feature, state, permission, button, edge case, acceptance criterion. The *product*. | Visual design (colour, type, spacing, layout, motion). Technical mechanism (how retrieval, agents, or the graph work internally). |
| **`design.md`** (supplied separately, kept in the codebase) | The *only* UI authority: colour tokens, typography, spacing, component visuals, layout grids, motion/animation treatment. | Whether a feature exists, what it does, what data it shows, what happens when it fails. |
| **`SENTINEL_Master_Engineering_Bible_MERGED.md`** | Technical truth: architecture, agent internals, graph schema, API contracts, database design, security posture, evaluation methodology. | Product scope or UI decisions — it describes *how* the things in this PRB are built, never *whether* they should exist. |

**Working rule for engineering and design:** if this PRB says a screen or button exists, build it. If it says what the screen must show or do, that is a functional requirement, not a suggestion. **Never invent layouts, colours, typography, spacing, or motion — those come only from `design.md`.** Where this PRB names a UI component (`AnswerCard`, `GraphCanvas`, `ComplianceMatrix`, etc.) it is naming a *functional* unit inherited from the Engineering Bible's UI System volume; its final visual form is `design.md`'s decision, not this document's.

This PRB never contradicts the Engineering Bible's ten engineering invariants (CP-1…CP-10) or its canonical facts. Where the Bible already specifies a mechanism (e.g. the agent roster, the graph schema, the API DTOs), this PRB references it rather than re-deriving it, so the two documents cannot drift apart. Every requirement below is traceable to a Bible section — see **Appendix B**.

---

# PART 0 — PRODUCT PHILOSOPHY (READ THIS BEFORE ANYTHING ELSE)

This part is not an introduction. It is the lens every requirement in this document must be viewed through. If a feature, screen, or workflow described later in this PRB does not visibly reinforce Part 0, it has failed its own design review and must be redesigned before it is built.

## 0.1 Locked Product Identity

> **Prahari is an Industrial Decision Intelligence Operating System.**

This identity is **locked**. It is not a tagline to place at the top of a slide — it is the categorical description that must be true of every screen, every workflow, every module, and every sentence of copy in the product.

**Prahari is NOT:**

| ❌ Not this | Why it undersells the product |
|---|---|
| An AI chatbot | A chatbot answers questions and forgets. Prahari accumulates organizational reasoning across every question ever asked. |
| A GraphRAG platform | GraphRAG is a retrieval technique. It is *how* Prahari fetches evidence, not *what* Prahari is for. |
| A knowledge graph product | A graph is a data structure. Prahari is a decision-making capability built on top of one. |
| An enterprise search engine | Search returns documents. Prahari returns a defensible, cited, actionable decision. |
| A document intelligence tool | Documents are raw material. The product is the reasoning connecting them. |
| A compliance chatbot | Compliance is one pillar among several, never the whole story, and never a legal opinion (BR-3). |

GraphRAG, knowledge graphs, LLMs, OCR, vector databases, and multi-agent orchestration are **implementation details** described fully in the Engineering Bible. They are how Prahari is built. They are never how Prahari is described to a user, a buyer, or a judge. Every product surface must make a person feel like they are operating an **operating system for industrial decision-making** — not chatting with an assistant.

## 0.2 First Principles — why Prahari must exist

Industrial failures repeat not because the facts were unavailable, but because the **reasoning behind past decisions was never preserved**.

- Documents survive. The engineer who read them does not stay forever.
- People retire — Anil, Prahari's canonical retiring-expert persona, is 34 years into a career the organization is about to lose (Bible §1.3).
- Knowledge decays quietly: a procedure written for one vendor's valve is silently wrong after a vendor change, and nothing flags it (Bible §5.10).
- Context disappears faster than content: a P&ID survives; the reason a shutdown was *rejected* in 2019 does not.
- Relationships between systems — which tag means which pump, which inspection note explains which alarm — live only in retiring people's heads (Bible §0.6 "the moat").
- Reasoning gets lost the moment it isn't written down as reasoning, only as an outcome.

**Prahari exists to preserve, reconstruct, evolve, and operationalize industrial decision intelligence** — so that no failure repeats *because the plant forgot*.

## 0.3 Core Philosophy — the shift in every interaction

| Generic pattern (what Prahari must never feel like) | Prahari's pattern (what every surface must feel like) |
|---|---|
| Find information | Navigate organizational memory |
| Search documents | Reconstruct the reasoning behind a decision |
| Answer a question | Reconstruct industrial reasoning, with the option to act on it |
| Chat with an assistant | Operate a system of record for decisions |
| Retrieve similar text | Traverse connected facts no human ever linked |

Any screen that reduces to "type a question, get an answer" has regressed to the chatbot pattern this product is explicitly not. Every screen must additionally show **where the reasoning came from**, **what would have to change for the reasoning to be wrong**, and **what should happen next**.

## 0.4 Decision Intelligence Principles (non-negotiable, product-level)

These are product principles, not engineering principles — though each is backed by an engineering invariant (CP-#) that makes it enforceable, not aspirational.

| # | Principle | Enforced by (Engineering Bible) |
|---|---|---|
| P1 | **Knowledge must evolve — it never remains static.** A fact recorded once is a snapshot, not a truth; Prahari continuously re-tests what it believes. | CP-7 (bitemporal graph), Bible §5.10 |
| P2 | **Every decision has context, and context is worth more than the document it came from.** A citation without the reasoning chain around it is trivia, not intelligence. | CP-1 (provenance), CP-2 (citation) |
| P3 | **Reasoning is a company asset, not an employee's private property.** When Anil corrects an answer, the correction belongs to the organization forever. | CP-10 (correction as a feature) |
| P4 | **Knowledge decays, and the platform is responsible for noticing.** Silence about decay is itself a failure mode. | Bible §5.10 KnowledgeRisk flags |
| P5 | **Every investigation should make the next investigation better.** Nothing Prahari does is disposable. | CP-10, Bible §4.5 self-correction loop |
| P6 | **Humans remain in control. AI recommends; humans decide and execute.** Prahari never writes to a system of record unattended. | CP-3 (gated writes) |
| P7 | **Industrial memory compounds. Every correction increases platform intelligence — for everyone, not just the person who made it.** | CP-10, Bible §16.3 moat |
| P8 | **Abstention is a legitimate, first-class answer.** Telling the truth about the limits of what is known is a success condition, not a failure state. | CP-4 (abstention) |
| P9 | **Everything is explainable, traceable, and auditable — nothing is a black box, including to the person who asked the question.** | CP-1, CP-2, CP-7, Bible §8.5 |
| P10 | **The model is a commodity; the corpus is not.** Prahari's value must not depend on which LLM happens to be inside it today. | CP-5 (swappable model) |

## 0.5 The Decision Intelligence Lifecycle

Every meaningful event inside Prahari — an investigation, a compliance check, a correction, an approved action — is an instance of one lifecycle. This lifecycle is the organizing structure of the entire product; almost every screen in Part 2 is a view onto one stage of it.

```
Observation  →  Evidence  →  Hypothesis  →  Decision  →  Execution
                                                              ↓
Future Decision  ←  Knowledge Evolution  ←  Correction  ←  Outcome
```

This is not a marketing diagram — it is implemented, additively, as the Engineering Bible's **reasoning primitives** and **decision graph** (Bible §5.2, §5.7): `Observation → Hypothesis → Evidence → Decision → Alternative(rejected) → RiskAccepted → Outcome → LessonLearned`, connected by `LED_TO` edges, each `EVIDENCED_BY` a source span. The PRB's lifecycle language and the Bible's node/edge model are the same object described at two altitudes: product language here, graph mechanics there.

| Lifecycle stage | What the user experiences | Bible primitive | Primary module (Part 2) |
|---|---|---|---|
| Observation | A symptom, alarm, or audit trigger appears | `Observation` node | M1 Decision Investigation |
| Evidence | Prahari assembles cited, provenance-tagged facts | `Span`, `EVIDENCED_BY` | M1, M9 |
| Hypothesis | A ranked, causal explanation is proposed | `Hypothesis` node | M1 |
| Decision | A human reviews, and either accepts, rejects, or requests more evidence | `Decision`, `Alternative`, `RiskAccepted` | M1, M3, M7 |
| Execution | An approved action is written to a system of record | `WorkOrder` | M7 Execution Center |
| Outcome | What actually happened is recorded | `Outcome` node | M3, M10 |
| Correction | A human marks something wrong and why | `Correction` node (CP-10) | M8 Correction & Learning Loop |
| Knowledge Evolution | The correction changes what the graph believes, for every future user | edge-weight `STRENGTHEN`/`WEAKEN`/`INVALIDATE`, `SUPERSEDES` | M4 Knowledge Evolution & Decay |
| Future Decision | The next investigation starts smarter than the last | Retrieval router reads the updated graph | Every module |

## 0.6 The Industrial Decision Intelligence Operating System model

Prahari should be described — to users, buyers, and judges — as an **operating system**, with layers, not as a single application with menu items. Each layer below is a genuine architectural component from the Engineering Bible, renamed to its decision-intelligence role.

```
┌─────────────────────────────────────────────────────────┐
│                         UI Layer                          │  ← Part 2 screens; visuals = design.md
├─────────────────────────────────────────────────────────┤
│  Learning Layer        (Learning agent, eval harness)     │  ← M8, M10   | Bible §4.1.1, §15
│  Execution Layer       (Actions/CMMS, gated writes)       │  ← M7        | Bible §4.2, §7.3 Actions
│  Compliance Engine     (Rule engine, evidence + gaps)     │  ← M6        | Bible §3.x, §8.10
│  Knowledge Evolution   (Decay flags, edge re-weighting)   │  ← M4        | Bible §5.10
│  Decision Engine       (Planner→Retriever→Executor→       │  ← M1, M3    | Bible §4.1
│                         Critic→Verifier)                  │
│  Memory                (Entity resolution corpus,         │  ← M2, M5    | Bible §5.6, §5.2 Person/KNOWS
│                         Decision graph, Org memory)        │
├─────────────────────────────────────────────────────────┤
│                        Kernel                              │
│   Temporal knowledge graph (Neo4j) · Vector index (Qdrant) │  ← Bible §0.6, §5, §6
│   Relational + audit (Postgres) · Cache (Redis) · Blob     │
└─────────────────────────────────────────────────────────┘
```

Naming this stack an "operating system" is only honest because each layer is a real, separately reasoned-about component (see Bible §2.3–2.4 container/component model) — this is a re-labelling for product clarity, not an invented abstraction.

## 0.7 The Four Compounding Moats

Every feature in Part 2 must be traceable to at least one of these four moats. A feature that doesn't strengthen any of them is a "nice to have," not a "must," and should be reconsidered before it consumes build time (see MoSCoW, §5.3).

| Moat | What compounds | Mechanism (Bible reference) |
|---|---|---|
| **1 — Decision Memory** | Every investigation's causal chain, every rejected alternative, every accepted risk becomes replayable reasoning, not just a historical record. | Decision graph, §5.7 |
| **2 — Organizational Intelligence** | Expert judgement (Anil's 34 years) is captured as `KNOWS` edges and corrections *before* it leaves with the person who holds it. | `Person`/`KNOWS` nodes, §5.2–5.3 |
| **3 — Knowledge Evolution** | The graph does not just grow — it re-tests itself. Stale, superseded, or contradicted knowledge is flagged, not silently trusted. | `KnowledgeRisk`, §5.10 |
| **4 — Entity Resolution Corpus** | The plant-specific, human-adjudicated map of "which identifier means which physical thing" — the one asset competitors cannot copy because it is produced by *this* customer's own labour inside *this* system. | `RESOLVED_AS`, §5.6, §16.3 |

**The flywheel:** every correction → improves future investigations → improves future compliance evidence → improves future execution confidence → improves future organizational memory → improves future decisions → attracts more use → produces more corrections. This is why Prahari gets *harder to displace*, not easier to commoditize, as it is used (Bible §16.3, §16.7) — the opposite of a thin LLM wrapper.

## 0.8 Non-negotiables for anyone building from this PRB

- Never call a feature by its underlying technology in user-facing copy, screen titles, or navigation labels ("Knowledge Graph" the menu item is wrong; "Decision Memory" is right — see Part 2 naming table).
- Never let a screen present an answer without also presenting where it came from and what would change it.
- Never write to a system of record (CMMS, DMS, or any external system) without an explicit, attributed human approval (CP-3).
- Never let an "I don't know" be indistinguishable from an error — abstention is a designed, first-class state (CP-4), not the absence of a state.
- Never imply compliance completeness. Every compliance surface must disclose what fraction of applicable clauses are actually encoded (Bible FM-6, BR-3).
- Never treat a UI decision as this document's to make. If a screen's behavior is specified here but its look is not, that is intentional — go to `design.md`.


---

# PART 1 — PRODUCT FOUNDATIONS

## 1.1 Mission / Vision / Problem

- **Mission:** Transform fragmented industrial knowledge into a continuously evolving decision intelligence layer that lets humans and agents investigate, decide, execute, protect, and preserve — together.
- **Vision:** A world in which no industrial failure repeats because the plant forgot why a decision was made.
- **Problem:** The plant is a physical graph documented as disconnected trees. The edges between systems — which alarm means which failure, which inspection note explains which vibration reading — live only in retiring people's heads. The knowledge exists. The *relationships*, and the *reasoning that produced them*, do not survive.

## 1.2 Personas — dual frame

Prahari's four canonical personas (Bible §1.3, inherited from Vol 3, **do not re-decide without an ADR**) are preserved exactly. Alongside each, this PRB assigns a **decision-mindset name** — not a replacement, a second lens that must show up in how the product frames their experience. Screen copy should read naturally to the operational persona; internal feature naming and product strategy should reason in the decision-mindset frame.

### Ravi — the primary user
- **Operational description:** night-shift maintenance technician. One hand, gloves, glare, weak signal, 02:40.
- **Decision-mindset name:** **Decision Creator / Decision Executor.** Ravi is the person standing in front of the failure who must turn a symptom into a hypothesis and, on approval, into an action.
- **Success condition:** a grounded, cited hypothesis in ≤ 90 seconds (Bible NFR-1, KPI table).
- **RBAC role:** `technician`.
- **Primary modules:** M1 Decision Investigation, M7 Execution Center (drafting only), M8 Correction (flagging only), Field Mode.

### Meera — the economic buyer
- **Operational description:** reliability engineer / plant-head-adjacent buyer. Cares about recurrence rate, audit readiness, ROI.
- **Decision-mindset name:** **Decision Approver & Knowledge Curator.** Meera reviews hypotheses before they become actions, and curates whether the organization's evidence is audit-ready.
- **Success condition:** walks into an audit with an evidence pack, not a scramble (JTBD-2); recurrence rate measurably falls over the pilot.
- **RBAC role:** `reliability` (and frequently also holds `compliance`).
- **Primary modules:** M6 Compliance Intelligence, M7 Execution Center (approval), M10 Decision Analytics, M3 Decision Memory & Replay.

### Deepak — the veto holder
- **Operational description:** OT security lead. Cares about data residency, air-gap, write-consent, the audit trail.
- **Decision-mindset name:** **Knowledge Guardian.** Deepak's job is to ensure the organization's decision intelligence never leaves the boundary and is never mutated without consent.
- **Success condition:** can sign off deployment because no data leaves the plant and every write is approved (JTBD-5).
- **RBAC role:** `admin` / `auditor`.
- **Primary modules:** M9 Audit & Provenance Center, M11 Admin & Ingestion Console (security settings), and veto visibility across every module.

### Anil — the corpus source (not a product user)
- **Operational description:** 34-year veteran, retiring. Not a user of the product's UI in the ordinary sense — a **source of corpus**.
- **Decision-mindset name:** **Knowledge Contributor.** Every correction Anil makes is captured as an attributed, durable graph edit (CP-10) — this is the mechanism by which his reasoning outlives his tenure.
- **Success condition:** his judgement is captured, not just his files (JTBD-3).
- **RBAC role:** typically `technician` or `reliability` for the purpose of submitting corrections; his product role is conceptual, not a distinct screen set.

### A fifth role occupant: the Compliance/EHS officer
The Bible's RBAC model (§8.2) includes a `compliance` role distinct from `reliability`. In smaller sites this role is held by Meera; in larger sites it is a dedicated EHS/compliance officer. This PRB does not invent a fifth canonical persona (that would contradict Bible §1.3) — it specifies that **any screen gated to the `compliance` RBAC role must work correctly for whichever human occupies it**, and that M6 Compliance Intelligence's copy must not assume the viewer is also the reliability buyer.

## 1.3 Jobs To Be Done (JTBD)

| ID | When… | I want to… | So I can… | Persona |
|---|---|---|---|---|
| JTBD-1 | a symptom appears at 02:40 | traverse sensor → asset → work order → drawing → manual → incident as one connected reasoning chain | act on a grounded, cited hypothesis in 90 seconds | Ravi |
| JTBD-2 | an audit approaches | see plant state evaluated against statutory instruments, with evidence attached | walk in with an evidence pack, not a scramble | Meera |
| JTBD-3 | an expert is about to retire | capture their judgement, not just their files | keep the reasoning after they leave | Anil → org |
| JTBD-4 | a failure recurs | see whether this exact mode was documented, decided on, and reasoned about before | break the recurrence loop | Meera |
| JTBD-5 | evaluating a pilot | prove no decision intelligence leaves the boundary and every write is human-approved | sign off deployment | Deepak |
| JTBD-6 *(new, product-level)* | a correction is made anywhere in the system | see that it visibly changes what the system believes, immediately | trust that using the system makes it smarter, not just bigger | All |
| JTBD-7 *(new, product-level)* | reviewing a past decision | replay the reasoning chain that led to it, including rejected alternatives | judge whether that reasoning still holds today | Meera, Deepak |

## 1.4 Roles → RBAC → module access

RBAC roles are defined once, technically, in Bible §8.2 (`technician | reliability | compliance | admin | auditor`), enforced coarse-grained at the gateway and fine-grained (ABAC) in-service. This PRB is the single place that says which **product modules** each role can reach and at what level (view / act / approve / administer).

| Module | technician | reliability | compliance | admin | auditor |
|---|:-:|:-:|:-:|:-:|:-:|
| M1 Decision Investigation | Full | Full | View | Full | View |
| M2 Entity Resolution | Propose | Adjudicate | View | Adjudicate | View |
| M3 Decision Memory & Replay | View | Full | View | Full | View |
| M4 Knowledge Evolution & Decay | View (flags) | Full | View | Full | View |
| M5 Organizational Memory | Contribute | Full | View | Full | View |
| M6 Compliance Intelligence | View | Full | Full | Full | View |
| M7 Execution Center | Draft | Approve | View | Approve | View |
| M8 Correction & Learning Loop | Submit | Submit + Review | Submit | Submit + Review | View |
| M9 Audit & Provenance Center | Own-actions only | Site-scoped | Site-scoped | Full | Full |
| M10 Decision Analytics | View (own) | Full | Full (compliance KPIs) | Full | View |
| M11 Admin & Ingestion Console | — | Upload only | Upload only | Full | View (read-only) |

"Draft," "Propose," and "Adjudicate" are meaningfully different levels of the same module and are specified in each module's action table in Part 2. No role ever reaches "Full" on a write path alone — every gated write (CP-3) requires a second, approving identity distinct in authority from the drafting identity, enforced by the ABAC policy in Bible §8.2.


---

# PART 2 — DECISION INTELLIGENCE MODULES (the feature set)

## 2.0 Naming law

Every module below has a **decision-intelligence name** (used in navigation, screen titles, and all user-facing copy) and an **engineering-bible mapping** (used only in this document and in engineering tickets, never in the product). This mapping is what keeps this PRB from drifting away from what is actually buildable.

| # | Product name (user-facing) | Engineering Bible mapping | MoSCoW (Bible §1.10) | Primary persona |
|---|---|---|---|---|
| M1 | **Decision Investigation** | Investigation / multi-hop causal retrieval (UC-1, FR-3, FR-4, FR-9) | Must | Ravi |
| M2 | **Living Asset Map** (entity resolution surface) | Entity resolution (FR-2, §5.6, §16.3 moat) | Must | Ravi, Meera |
| M3 | **Decision Memory & Replay** | Decision graph (§5.7) | Could | Meera, Deepak |
| M4 | **Knowledge Evolution** | Knowledge decay/evolution (§5.10) | Could (Should for KnowledgeRisk flags) | Meera |
| M5 | **Organizational Memory** | `Person`/`KNOWS` nodes, corpus capture (JTBD-3) | Should | Anil → org, Meera |
| M6 | **Compliance Intelligence** | Compliance rule engine (UC-2, FR-5) | Should | Meera, compliance officer |
| M7 | **Execution Center** | Approved actions / gated writes (UC-4, FR-6) | Should | Ravi (draft), Meera (approve) |
| M8 | **Correction & Learning Loop** | Correction loop (UC-3, FR-7, CP-10) | Must | All |
| M9 | **Audit & Provenance Center** | Audit log (FR-10, §8.5) | Should | Deepak |
| M10 | **Decision Analytics** | KPI dashboards (§1.9) | Should | Meera |
| M11 | **Admin & Ingestion Console** | Ingestion pipeline UI, RBAC/tenant admin (§2.6, §8.2) | Must (ingestion), Should (admin) | Deepak, Meera |
| M12 | **Field Mode** | Mobile-first PWA signature surface (§10.7) | Must | Ravi |
| — | **Global Shell** (nav, auth, notifications, degraded banner) | Cross-cutting (§10.2–10.3) | Must | All |

A module marked **Won't** in the Bible's MoSCoW (autonomous writes, native mobile app, multi-plant network features — §1.10) is explicitly **out of scope for this PRB** and must not be built even if it would be easy to add; scope discipline is itself part of the hackathon-winning posture (Bible §1.12 risk register).

## 2.1 Global Shell (applies to every module)

### Purpose
The shell is the first thing anyone sees and the last thing that ever fails silently. It carries authentication, navigation, the current degradation rung (CP-9), notifications, and the confidence-legend — every module lives inside it.

### Screens

**Login**
- Fields: organization SSO entry point (OIDC redirect — Bible §7.2, §8.2), no local password field (identity is federated from the customer IdP).
- Buttons: `Sign in with [Organization SSO]` → redirects to IdP → on return, token validated at gateway → routes to last-visited module or, on first login, to M1 Decision Investigation.
- Failure state: IdP unreachable → "Can't reach your organization's sign-in. Try again, or contact your admin." (never a raw auth stack trace).
- Session states: token near expiry → silent refresh; refresh fails → soft logout with "Your session ended — sign in again to continue," preserving in-flight draft text where technically possible.

**Global navigation (persistent shell chrome)**
- Primary nav items, in order: Decision Investigation, Living Asset Map, Compliance Intelligence, Execution Center, Decision Memory & Replay, Organizational Memory, Decision Analytics, Audit & Provenance *(role-gated)*, Admin *(role-gated)*.
- Each nav item hidden entirely (not merely disabled) if the signed-in role has no access to any screen inside it — an empty-permission state is invisibility, not a greyed-out tease.
- **Notification bell:** shows resolution-queue items awaiting adjudication, actions awaiting approval, and compliance items newly overdue — each a deep link to the exact record.
- **DegradedBanner** *(functional component; visual form = design.md)*: persistent, non-dismissible whenever the system is operating below the "Full" rung of the degradation ladder (Bible §2.8). States: `Full` (banner hidden), `-model` ("Answers are structured, not narrated — the reasoning model is unavailable"), `-vector` ("Semantic search is unavailable — showing graph-linked results only"), `-graph` ("Showing cached answers and document search only"), `-everything` ("Live reasoning is unavailable — showing who to ask"). This banner is a product requirement, not a DevOps nicety: **CP-9 must be visible to the user, not just survivable in the backend.**
- **Confidence legend** (persistent, small, always visible near any AnswerCard): `Grounded` / `Inferred` / `Unsupported` / `Abstained` — labelled, never colour-only (accessibility, Bible NFR-10).
- **Profile/settings menu:** organization, role, site scope, glare-mode toggle (Field Mode), sign out.

### Edge cases (global)
- Network loss mid-session → shell keeps the DegradedBanner accurate in real time via the WebSocket heartbeat; cached last-known state is shown, never a blank screen (CP-9).
- Role change mid-session (admin revokes access) → next request returns `403 forbidden` (Bible §7.5) → shell removes the nav item live and shows a one-time toast: "Your access to [module] has changed."
- Multi-tab session → last-write-wins is acceptable for navigation state; write actions (approvals, corrections) are protected by optimistic concurrency (`version` field, 409 on stale write — Bible §7.6), surfaced as "This was already actioned by [name] — refresh to see the current state."


## 2.2 M1 — Decision Investigation

**Engineering mapping:** UC-1, FR-3, FR-4, FR-9; Agent path Planner→Retriever→Executor→Critic→Verifier (Bible §4.1); API `POST /v1/investigations`, `GET /v1/investigations/{id}`, `WS /v1/stream/investigations/{id}` (Bible §7.3–7.4).
**Priority:** Must. **Pillar:** Design + Operate. **Primary persona:** Ravi. **Secondary:** Meera, Deepak (view).
**JTBD:** JTBD-1.

### Why this exists
This is the module where an "Observation" becomes a "Hypothesis" (§0.5 lifecycle stages 1–3). It is the **secondary wow moment** of the product (Bible §11.3) — a causal chain assembled across documents nobody had linked, each hop citing a page. It must never present as a chat transcript; it must present as an argument the user can inspect hop by hop.

### Screen: Investigation Console

**Layout (functional, not visual — see design.md):** question bar at the top; a streamed `AnswerCard` on one side; a `GraphCanvas` on the other showing the traversal animating hop by hop as it is retrieved; `CitationChip`s inline inside every claim; a `CorrectionAffordance` on every claim and every edge. On Field Mode (§2.13) the canvas collapses to a linear `TraversalTrace` and the `AnswerCard` stacks above it.

**Entry points:** Global nav "Decision Investigation"; deep link from a notification; deep link from M6 Compliance (an overdue obligation can launch "investigate why"); deep link from M10 Analytics (a recurrence spike can launch "investigate this failure mode").

### Actions & buttons

| Action | Trigger | API call | Permission | Loading state | Success state | Error / failure state | Confirmation | Audit event |
|---|---|---|---|---|---|---|---|---|
| **Ask a question** | User types a free-text question and presses `Investigate` (or Enter) | `POST /v1/investigations {question, as_of?, context?}` → `202 {investigation_id}`, then subscribe `WS /v1/stream/investigations/{id}` | `technician`+ (any signed-in role) | Question bar disables re-submit; a "Planning…" indicator appears (names the Planner agent stage, not a generic spinner) | Streamed tokens populate `AnswerCard`; `graph_hop` events animate `GraphCanvas` live; final `verdict` event marks the card complete | Gateway/model unreachable → degrade per CP-9 ladder, banner updates, and a structured (non-narrated) answer is still attempted at the next rung | None (read-only) | `investigation.asked {question, investigation_id}` |
| **As-of date picker** | User sets a historical date before asking | Passed as `as_of` in the request body | Same as above | N/A | Answer is reconstructed exactly as it would have appeared on that date (bitemporal query, Bible §5.8 "as-of reconstruction") | If no graph state existed before that date → AbstainCard: "No recorded knowledge as of that date" | None | `investigation.asked {as_of}` |
| **Open a citation** | Tap/click a `CitationChip` (e.g. `[doc p.14]`) | `GET` source span (peek panel; no dedicated network call if context already streamed) | Any viewer | Peek panel loading skeleton | Source span opens inline with document/page/highlighted span | Span unavailable (blob store issue) → "Source temporarily unavailable — citation ID: [span_id]" (never silently drop the citation) | None | `citation.viewed {span_id}` |
| **Expand a graph hop** | Click a node/edge in `GraphCanvas` | Local state (already-fetched subgraph); may lazy-fetch neighbours via `graph.traverse` tool | Any viewer | Node expands with a brief highlight | Neighbouring nodes/edges render, each still carrying its own confidence badge | Traversal depth limit reached (bound hops, Bible §5.9) → "Traversal limited to N hops — ask a follow-up to go further" | None | `graph.hop_expanded` |
| **Flag a claim as wrong** | `CorrectionAffordance` ("this is wrong") on any claim or edge | Opens Correction composer → `POST /v1/corrections` (see M8) | Any viewer with a role above pure read | Composer inline expand | Claim visually marked "correction submitted," graph will reflect the fix on next fetch | Submission fails → claim keeps its "correction pending — retry" state, never silently discarded | Confirm dialog: "This will be recorded as a correction attributed to you. Continue?" | `correction.submitted` (see M8) |
| **Draft a work order from this hypothesis** | `Draft action` button on a ranked hypothesis | Deep-links into M7 `POST /v1/actions/work-order/draft {asset_id, symptom, hypothesis_id}` | `technician`, `reliability` | Button shows "Drafting…" | Navigates to M7 Execution Center with the draft pre-filled and this investigation linked as its evidence | Draft API fails → error toast, hypothesis remains selectable, retry offered | None (drafting is not a system-of-record write; see M7 for the write itself) | `action.draft_created {investigation_id}` |
| **Ask "why" on an upstream node** (follow-up) | Click "investigate this" on any node surfaced in the graph | New `POST /v1/investigations` scoped with `context.asset_id` | Any viewer | Same as "Ask a question" | New AnswerCard opens threaded under the current investigation | Same as "Ask a question" | None | `investigation.asked {parent_investigation_id}` |
| **Copy / share investigation link** | Share icon on a completed AnswerCard | None (client-side URL) | Any viewer | N/A | Link copied; opens to the same investigation for anyone with permission on that site | Recipient lacks permission → `403` with "You don't have access to this site's investigations" | None | `investigation.shared` |

### States

- **Empty state (no question asked yet):** a short list of "things people are asking right now" (recent non-sensitive investigations at this site) and a one-line prompt — never a blank input box with nothing else on the page.
- **Loading:** staged, named loading copy tied to the actual agent stage (Planner → Retriever → Executor → Critic → Verifier), not a generic spinner — this is both honest and, per the Bible's demo guide, a legitimate trust-building device.
- **Grounded / Inferred / Unsupported:** every claim chip carries exactly one of these three labelled states (never an unlabelled percentage — Bible §10.1, §10.9).
- **Abstained (`AbstainCard`):** shown whenever the Verifier cannot ground a necessary claim (CP-4). Must show: what could not be grounded, what *is* known, and **who to ask** (pulled from Organizational Memory, M5). This is a designed success state, not an error — it must never use error-red styling that implies system failure (defer exact treatment to design.md, but the functional requirement is: visually distinct from both "answer" and "error").
- **Degraded (per CP-9 rung):** see Global Shell DegradedBanner; the Investigation Console must additionally suppress prose synthesis at the `-model` rung and show a structured, templated answer instead (Bible §2.8).
- **Offline (Field Mode):** shows the last cached answer for a previously-asked or pre-seeded question, clearly labelled "cached — [timestamp]," never presented as live.

### Edge cases & failure handling (answers to the mandatory pre-build checklist)

- **Why does this exist?** To collapse a 30–60 minute phone-call chain into a 90-second, cited hypothesis (JTBD-1).
- **Which persona?** Ravi (primary), Meera/Deepak (view/audit).
- **Which JTBD?** JTBD-1.
- **Which API?** `POST/GET /v1/investigations`, `WS /v1/stream/investigations/{id}`.
- **Which agent(s)?** Planner, Retriever, Executor, Critic, Verifier (live path); Memory (prior corrections context).
- **Which graph nodes?** `Asset, Identifier, WorkOrder, FailureMode, Inspection, Incident, Span, Sensor` and the reasoning primitives `Observation, Hypothesis, Evidence`.
- **Which permissions?** Any signed-in role may ask; drafting an action requires `technician`/`reliability`.
- **What happens offline?** Cached/pre-seeded answers only, honestly labelled (CP-9 `-everything` rung: "who to ask").
- **What if the model fails?** Structured, un-narrated answer (CP-9 `-model` rung) — never blank.
- **What if retrieval fails?** Graph-only or cache-only fallback per the ladder; never a raw error to Ravi mid-shift.
- **What if the graph is unavailable?** Document search fallback ("here is what I can see" — Bible §2.8).
- **What if the API returns nothing?** Treated as insufficient grounding → abstain, not an empty screen.
- **What if the user has no permission?** The console itself is visible to all signed-in roles; only the action-drafting button is gated, and it is hidden (not disabled) for roles without it.
- **Loading state?** Named per agent stage (above).
- **Error state?** Non-technical, human copy; retry always offered; request ID shown for support escalation.
- **Empty state?** Suggested/recent investigations, never a bare box.
- **How is it logged?** Every question, context id set, prompt manifest hash, model id, and verdict is written to the append-only audit log (Bible §8.5, CP-7 reproducibility).
- **How is it tested?** Golden-set questions with known-correct traversal paths (Bible §15.2); grounding faithfulness ≥ 0.90, citation accuracy ≥ 0.95 (NFR-5, NFR-6) are release gates, not aspirations.
- **How is it verified?** Every PR touching this module must re-run the golden set before merge (Bible §14, Definition of Done).

### Acceptance criteria

```gherkin
Feature: Decision Investigation

  Scenario: Grounded multi-hop hypothesis with citations
    Given P-101B has a vibration alarm and a 2019 inspection note about strainer fouling
    When Ravi asks "why is P-101B running hot"
    Then the system returns at least one hypothesis ranked by confidence
    And each hop in the hypothesis cites a document, page, and span
    And the traversal path renders progressively on the graph as it is retrieved
    And if grounding falls below threshold, the system abstains and names who to ask

  Scenario: Historical reconstruction
    Given a graph state that has since been superseded
    When a user sets an as-of date before the supersession and asks the same question
    Then the answer reflects only facts valid as of that date

  Scenario: Degraded but honest
    Given the reasoning model is unavailable
    When Ravi asks a question
    Then the system returns a structured, un-narrated answer instead of failing
    And the DegradedBanner names the current rung

  Scenario: Abstention is a success state
    Given the assembled context does not sufficiently ground a necessary claim
    When the Verifier evaluates the draft
    Then the system returns an AbstainCard with what is known, what is missing, and who to ask
    And this is logged and scored as an abstention, not an error
```


## 2.3 M2 — Living Asset Map (Entity Resolution)

**Engineering mapping:** FR-2, §3.2 (entity resolution mechanics), §5.6 (`RESOLVED_AS` edge), §16.3 (the moat). API: `GET /v1/resolution/queue`, `POST /v1/resolution/{proposal_id}/adjudicate`, `POST /v1/resolution/unmerge/{merge_id}` (Bible §7.3).
**Priority:** Must. **Pillar:** Design + Build + Operate. **Primary persona:** Ravi (confirms), Meera (adjudicates at scale).
**JTBD:** underlies JTBD-1 and JTBD-4 (nothing else works if the plant's identifiers aren't resolved to real assets).

### Why this exists
This is **the primary wow moment** (Bible §11.3, §10.5): four different names for one physical pump — `P-101B`, "Boiler Feed Pump B", an OEM part number, and "the noisy one" — collapse into a single canonical `Asset` node. This is also **the moat itself** — the plant-specific, human-validated corpus that compounds with use and cannot be copied by a competitor shipping the same GraphRAG stack (Bible §16.3, §16.7). Every screen here must make the user feel like they are building something durable, not just cleaning data.

### Screen: Resolution Queue

**Layout (functional):** a queue of medium-confidence merge proposals, each showing the candidate `Identifier` chips animating toward a single proposed `Asset` node; a one-tap confirm/correct action per proposal (`ResolutionQueue` component, Bible §10.3).

### Actions & buttons

| Action | Trigger | API call | Permission | Loading | Success | Error | Confirmation | Audit event |
|---|---|---|---|---|---|---|---|---|
| **Confirm merge** | Tap `Confirm` on a proposal | `POST /v1/resolution/{proposal_id}/adjudicate {decision:"merge", approver}` | `reliability`, `admin` (Ravi may confirm low-stakes proposals per site policy) | Chips animate collapsing into the canonical node | Proposal removed from queue; `RESOLVED_AS` edges written with `{confidence, method:"human", adjudicated_by, adjudicated_at}`; any prior answer referencing this asset silently becomes correct on next fetch | Write conflict (already adjudicated by someone else) → `409`, "Already resolved by [name] at [time]" | None (confirm is itself the action; explicit "this cannot be silently undone but IS reversible" microcopy shown once) | `resolution.adjudicated {decision:"merge"}` |
| **Reject / keep separate** | Tap `Separate` on a proposal | `POST /v1/resolution/{proposal_id}/adjudicate {decision:"separate", approver}` | Same as above | Chips visibly separate, stay as distinct identifiers | Proposal removed; no merge edge created; identifiers remain individually resolvable | Same conflict handling as above | Optional note field: "why are these different?" (captured as adjudication rationale) | `resolution.adjudicated {decision:"separate"}` |
| **Correct a proposed merge** (wrong grouping, right idea) | Tap `Correct`, re-assign one identifier chip to a different/new asset | Same adjudicate endpoint with a modified target | `reliability`, `admin` | Chip re-animates to the corrected target | Corrected `RESOLVED_AS` edges written; this correction feeds the Learning agent (CP-10) exactly like an M8 correction | Same conflict handling | Confirm dialog naming the new target explicitly | `resolution.adjudicated {decision:"merge", corrected:true}` |
| **Unmerge** | From an asset's detail view, `Unmerge` on a prior merge event | `POST /v1/resolution/unmerge/{merge_id}` | `admin` (higher bar than confirming — undoing is rarer and higher-blast-radius) | Confirmation modal | Prior `Identifier`↔`Asset` mapping restored exactly as recorded (BR-4: all merges are reversible) | Merge already superseded by further activity → warns of downstream effects before allowing | Explicit: "This asset has N linked work orders/investigations that will be affected. Continue?" | `resolution.unmerged {merge_id}` |
| **View adjudication history** | `History` tab on an asset | `GET` asset detail (adjudication history embedded) | Any viewer | Skeleton list | Chronological list: who adjudicated what, when, and why | N/A (read-only) | None | `resolution.history_viewed` |
| **Manually propose a merge** (bottom-up, not from the queue) | `Propose merge` from search results showing two identifiers | Creates a new proposal in the queue via the same adjudicate flow | `technician`+ | Adds to queue | Confirmation toast: "Sent for adjudication" | N/A | None (creating a proposal is not itself a write to the canon) | `resolution.proposed` |

### States

- **Empty queue:** "No pending resolutions — the asset map is fully adjudicated" (a genuinely good state, framed as one, not a dead end).
- **Loading:** proposal cards show skeleton chips, never a spinner covering the whole screen (the animation of chips-into-node *is* the loading state once data arrives).
- **High-confidence auto-merge (no queue entry):** disclosed transparently in the asset's history as "auto-resolved, high confidence" with the option to challenge it later — auto-merge is never invisible.
- **Low-confidence, ambiguous identifier:** never force a decision — abstains into the queue rather than guessing (Bible §1.8 edge case: "ambiguous identifier that could be two assets → resolution abstains, asks a human").

### Edge cases & failure handling

- **Why does this exist?** It is the mechanism that makes every other module trustworthy — if the wrong pump is cited, a perfectly-grounded answer is still wrong (Bible §11.6, judge Q&A on hallucination risk).
- **Which persona?** Ravi (confirm), Meera/admin (adjudicate at scale, unmerge).
- **Which JTBD?** Underlies JTBD-1, JTBD-4.
- **Which API?** `/v1/resolution/queue`, `/v1/resolution/{id}/adjudicate`, `/v1/resolution/unmerge/{id}`.
- **Which agent(s)?** Entity Resolution Service (not an LLM agent — a scoring/candidate-generation service, Bible §2.4).
- **Which graph nodes?** `Identifier`, `Asset`, edge `RESOLVED_AS`.
- **Which permissions?** Confirm/separate: `reliability`/`admin` (site policy may extend to `technician` for low-stakes proposals); unmerge: `admin` only.
- **What happens offline?** Queue is read-only cached; adjudication actions queue locally and sync on reconnect, never silently lost (must be clearly labelled "pending sync").
- **What if the model/service fails?** Candidate generation degrades to rules-based matching only (no learned scoring); still human-adjudicated, so correctness is preserved even if recall drops.
- **What if retrieval/graph fails?** Queue cannot load; DegradedBanner shown; no adjudication actions possible until the graph is reachable (an explicit UI-level fail-safe: never let adjudication happen against a store that can't durably record it).
- **What if the API returns nothing?** Empty-queue state (above), distinguished from a load failure.
- **What if the user has no permission?** Queue is view-only; action buttons hidden, not disabled-and-confusing.
- **Loading/error/empty states?** Specified above.
- **How is it logged?** Every adjudication is append-only audited with actor, timestamp, decision, and rationale (Bible §8.5); this log **is** the moat's provenance.
- **How is it tested?** A seeded 4-identifier → 1-asset scenario is a release-gating golden-set case (this is literally the demo's primary wow moment — Bible §11.4).
- **How is it verified?** Reversibility is tested explicitly: merge → unmerge must restore bit-for-bit the prior mapping (BR-4 acceptance test).

### Acceptance criteria

```gherkin
Feature: Living Asset Map (entity resolution)

  Scenario: Four identifiers resolve to one asset
    Given the identifiers "P-101B", "Boiler Feed Pump B", an OEM part number, and "the noisy one" exist unlinked
    When the resolution engine proposes a merge and a human confirms it
    Then all four identifiers resolve to one canonical Asset node
    And any prior investigation referencing any of the four now returns the unified answer

  Scenario: Reversible merge
    Given a confirmed merge exists
    When an admin unmerges it
    Then the prior Identifier-to-Asset mapping is restored exactly
    And the system warns of any investigations or work orders affected before completing the unmerge

  Scenario: Ambiguous identifier never auto-resolves
    Given an identifier could plausibly refer to two different assets
    When the resolution engine evaluates it
    Then it is queued for human adjudication, never auto-merged
```


## 2.4 M6 — Compliance Intelligence

**Engineering mapping:** UC-2, FR-5, BR-3, FM-6; API `GET /v1/compliance/assets/{asset_id}`, `GET /v1/compliance/coverage` (Bible §7.3).
**Priority:** Should. **Pillar:** Protect. **Primary persona:** Meera / compliance officer.
**JTBD:** JTBD-2, JTBD-4.

### Why this exists
Regulatory obligations (OISD, PESO, DGMS, CPCB/SPCB — Bible §18.3) attach to assets with a periodicity and must be evidenced. This module turns "an audit is coming" from a scramble into a walk-in-ready evidence pack (JTBD-2) — while never crossing into legal opinion (BR-3) or implying completeness (FM-6).

### Screen: Compliance Matrix

**Layout (functional):** rows = obligations, columns = status (satisfied / due / overdue), each cell links to its evidencing document (`ComplianceMatrix` component, Bible §10.3, §10.6). A **persistent, honest footer is mandatory on every view of this screen**: "Encoded clauses: N of M. This is not a completeness guarantee." This footer is a product requirement, not a legal disclaimer bolted on after the fact — remove it and the module becomes a liability (Bible §8.10, BR-3).

### Actions & buttons

| Action | Trigger | API call | Permission | Loading | Success | Error | Confirmation | Audit event |
|---|---|---|---|---|---|---|---|---|
| **View asset obligations** | Select an asset (or land here from a nav filter) | `GET /v1/compliance/assets/{asset_id}` | `compliance`, `reliability`, `admin` (view: any) | Skeleton matrix | Rows populate with `{clause, asset, periodicity, last-evidence-doc, status}` | Asset has no data → distinguished empty state (below), never confused with "fully compliant" | None | `compliance.viewed {asset_id}` |
| **Open evidencing document** | Click a status cell with evidence | Opens the linked `Document`/`Span` (reuses citation peek panel from M1) | Any viewer | Peek panel loading | Document opens at the evidencing page | Evidence document missing/moved → "Evidence link broken — flagged for review," auto-creates a `Contradiction`-style flag for follow-up | None | `compliance.evidence_viewed` |
| **View coverage report** | `Coverage` tab | `GET /v1/compliance/coverage` | Any viewer | Skeleton | Shows which clauses are ENCODED vs NOT, by instrument (OISD/PESO/DGMS/CPCB) | N/A | None | `compliance.coverage_viewed` |
| **Investigate an overdue obligation** | `Investigate` button on an overdue row | Deep-links to M1 with the asset/obligation as context | `technician`+ | N/A | Opens Decision Investigation pre-scoped to "why is this overdue / what changed" | N/A | None | `investigation.asked {source:"compliance"}` |
| **Export evidence pack** | `Export` on the matrix | Generates a document bundle of the current view + citations (server-side job) | `compliance`, `reliability`, `admin` | "Preparing evidence pack…" progress | Downloadable file, itself carrying provenance stamps per item | Export fails → retry, never a partial silent file | None | `compliance.exported {asset_id or scope}` |
| **Filter by instrument/authority/status** | Filter chips (OISD / PESO / DGMS / CPCB / status) | Client-side + query param on the GET | Any viewer | Instant | Matrix re-renders filtered | N/A | None | `compliance.filtered` |

### States

- **Empty (no obligations configured for this asset/site yet):** explicit "No obligations encoded for this asset yet" — never rendered identically to "fully satisfied," since those are opposite meanings for an auditor.
- **Overdue (highlighted per silence-over-noise principle):** only genuine gaps are visually emphasized; a satisfied obligation is calm, not celebratory-noisy (Bible §10.1 "silence over noise" — an alert firing when nothing is wrong destroys this pillar's credibility permanently).
- **Coverage disclaimer:** always visible, never collapsible into a tooltip that could be missed.
- **Degraded:** if the rule engine cannot reach the graph, the module shows the last precomputed nightly evaluation with an explicit "as of [timestamp], not live" label — never a stale value presented as current (Bible NFR-2: precomputed nightly + on-demand).

### Edge cases & failure handling

- **Why does this exist?** JTBD-2 — an evidence pack, not a scramble.
- **Which persona?** Meera / compliance officer (full); Ravi (view, investigate).
- **Which API?** `/v1/compliance/assets/{asset_id}`, `/v1/compliance/coverage`.
- **Which agent?** Compliance agent (Bible §4.1.1), reading the versioned rule library (CP-6: rules are data, not code) against graph state.
- **Which graph nodes?** `Obligation`, `Instrument`, edges `GOVERNS`, `DEFINED_IN`.
- **Which permissions?** View: broad; export/full management: `compliance`/`reliability`/`admin`.
- **What happens offline?** Last precomputed nightly evaluation shown, clearly dated; no live evaluation possible offline.
- **What if the model fails?** Rule evaluation does not depend on the LLM (Bible §3.x: rule engine vs graph state) — this module is largely resilient to model outage by design; note this explicitly to Deepak/Meera in the UI as a reliability property.
- **What if the graph is unavailable?** Falls back to last cached evaluation, timestamped.
- **What if the API returns nothing?** Empty state, not "all satisfied."
- **What loading/error/empty states?** Specified above.
- **How is it logged?** Every view and export is audited (who saw what evidence, when — itself sometimes an audit requirement).
- **How is it tested?** Golden-set includes at least one deliberately-overdue OISD obligation whose evidence chain is known (Bible §11.4 demo dataset design).
- **How is it verified?** BR-3/FM-6 compliance is a release gate: no build may ship a version of this screen without the coverage footer.

### Acceptance criteria

```gherkin
Feature: Compliance Intelligence

  Scenario: Overdue obligation with evidence chain
    Given an OISD obligation attached to an asset has no evidence within its periodicity window
    When Meera opens the Compliance Matrix for that asset
    Then the obligation shows status OVERDUE
    And the last known evidence document (if any) is linked
    And the coverage footer states how many of the applicable clauses are encoded

  Scenario: Never implies completeness
    Given any state of the Compliance Matrix
    When it is rendered
    Then the "Encoded clauses: N of M — not a completeness guarantee" footer is always visible
```

## 2.5 M7 — Execution Center

**Engineering mapping:** UC-4, FR-6, CP-3; API `POST /v1/actions/work-order/draft`, `POST /v1/actions/work-order/submit` (Bible §7.3).
**Priority:** Should. **Pillar:** Build + Operate. **Primary persona:** Ravi (draft), Meera (approve).
**JTBD:** completes JTBD-1 (a hypothesis is only valuable if it can become an action).

### Why this exists
This is the "Execution" stage of the Decision Intelligence Lifecycle (§0.5) and the hard boundary of CP-3: **no write to a system of record without an explicit, attributed human approval.** This module exists specifically to make that boundary visible and unavoidable, not just enforced invisibly on the backend.

### Screen: Action Draft & Approval

**Layout (functional):** a draft card (asset, symptom, linked hypothesis/investigation) → an `ApprovalSheet` (review-before-write, Bible §10.3) → on approval, a confirmation showing the resulting system-of-record ID.

### Actions & buttons

| Action | Trigger | API call | Permission | Loading | Success | Error | Confirmation | Audit event |
|---|---|---|---|---|---|---|---|---|
| **Draft a work order** | From M1 ("Draft action from this hypothesis") or directly here | `POST /v1/actions/work-order/draft {asset_id, symptom, hypothesis_id}` | `technician`, `reliability` | "Drafting…" | Draft appears with a full preview (asset, symptom, linked evidence, hypothesis confidence) | Draft API fails → retry, hypothesis remains available, nothing partially written | None (drafting writes nothing to CMMS) | `action.draft_created` |
| **Review draft** | Open the `ApprovalSheet` | N/A (loads the draft) | `reliability`, `admin` (approvers); `technician` may view own drafts | Sheet loading skeleton | Full evidence trail shown: linked investigation, citations, confidence | Draft not found/expired → "This draft is no longer available" | None | `action.reviewed` |
| **Approve & submit** | `Approve` button on the ApprovalSheet | `POST /v1/actions/work-order/submit {draft_id, approver}` → `201 {cmms_work_order_id}` | `reliability`, `admin` — **and the approver must be distinct-or-authorized per ABAC policy from the drafter, per site policy (Bible §8.2 example policy)** | "Submitting to CMMS…" | Work order committed to the system of record; resulting ID shown and linked back to the originating investigation | CMMS write fails → draft remains pending, explicit "not yet committed" state, retry offered, **never silently marked done** | Explicit approval dialog naming the exact action, asset, and approver identity — this is the CP-3 gate made visible | `action.submitted {cmms_work_order_id}` |
| **Reject draft** | `Reject` on the ApprovalSheet | Marks draft rejected (no CMMS call) | `reliability`, `admin` | Instant | Draft closed, rationale optionally captured | N/A | Optional rationale field | `action.rejected {reason}` |
| **View action history** | `History` tab | `GET` action history for an asset | Any viewer | Skeleton list | Chronological list of drafted/approved/rejected actions with links to their evidence | N/A | None | `action.history_viewed` |

### States

- **Draft pending approval:** clearly distinct from "approved" — a draft is never mistakable for a committed action anywhere in the UI (this is the single most safety-critical visual distinction in the product; exact treatment = design.md, but the functional requirement is non-negotiable).
- **Committed:** shows the system-of-record ID and a permanent link back to the evidence chain that produced it (traceability, CP-1/CP-7).
- **Failed submission:** never shown as ambiguous — either "committed with ID X" or "not committed, here's why," never a state a user must guess about.

### Edge cases & failure handling

- **Why does this exist?** To make CP-3 (no unattended writes) a felt product experience, not just a backend guarantee.
- **Which persona?** Ravi (draft), Meera/admin (approve).
- **Which API?** `/v1/actions/work-order/draft`, `/v1/actions/work-order/submit`.
- **Which agent?** None generates the write itself — the Executor agent may propose the draft's content, but submission is a pure human action gated by ABAC, never agent-initiated.
- **Which permissions?** Draft: `technician`/`reliability`; approve: `reliability`/`admin`, distinct-authority rule enforced.
- **What happens offline?** Drafts can be composed offline and queued; **approval and submission require connectivity** — this is an intentional, disclosed limitation, not a bug, since a system-of-record write must not happen against a store that cannot durably confirm it.
- **What if the model fails?** Drafting can fall back to a template (structured fields only, no narrated summary) at the `-model` CP-9 rung; approval/submission logic is unaffected since it does not depend on the model.
- **What if the CMMS is unreachable?** Submission fails cleanly with retry; draft stays pending, never falsely marked committed.
- **What if the user has no permission?** Approve button is hidden for non-approvers; they see a read-only view with "awaiting approval from [role]."
- **How is it logged?** Every draft, approval, rejection, and submission is audited with actor identity (Bible §8.5, CP-3).
- **How is it tested?** A test asserts no code path can reach a `201` CMMS commit without a distinct approver identity present in the request (Bible §14.7 Security Checklist).
- **How is it verified?** This module's Definition of Done explicitly includes "cannot be bypassed" as a security test, not just a functional one.

### Acceptance criteria

```gherkin
Feature: Execution Center

  Scenario: Draft requires approval before any system-of-record write
    Given a hypothesis exists from a Decision Investigation
    When Ravi drafts a work order from it
    Then the draft is shown for human approval
    And no write occurs against the CMMS until an approver explicitly approves it
    And the approval and the resulting CMMS work order ID are both fully audited

  Scenario: Rejected draft never reaches the system of record
    Given a drafted action
    When an approver rejects it
    Then no CMMS write occurs
    And the rejection and its rationale are recorded
```


## 2.6 M8 — Correction & Learning Loop

**Engineering mapping:** UC-3, FR-7, CP-10; API `POST /v1/corrections` (Bible §7.3); Learning agent (Bible §4.1.1).
**Priority:** Must. **Pillar:** Operate. **Primary persona:** all (this is where Anil's expertise actually enters the system).
**JTBD:** JTBD-3.

### Why this exists
This is Moat #1 and #2 made concrete (§0.7): every correction is how organizational reasoning outlives the person who holds it. This module must feel less like "reporting a bug" and more like "teaching the system something it will remember forever" — because that is literally what it does (CP-10).

### Screen: Correction Composer (a modal/inline affordance, not a standalone page)

The `CorrectionAffordance` appears on every claim, every citation, every graph edge, and every resolution proposal across the product — this is a cross-cutting component, not one screen.

### Actions & buttons

| Action | Trigger | API call | Permission | Loading | Success | Error | Confirmation | Audit event |
|---|---|---|---|---|---|---|---|---|
| **Flag as wrong** | "This is wrong" affordance on any claim/edge | Opens composer (target pre-filled) | Any signed-in role | N/A | Composer expands inline | N/A | N/A | `correction.opened` |
| **Submit correction** | `Submit` in composer, with `new_value` and `rationale` | `POST /v1/corrections {target_kind, target_ref, new_value, rationale, author}` → `201 {correction_id}` | Any signed-in role (attribution is mandatory, never anonymous — CP-10 requires an author) | "Recording correction…" | Correction persists as a durable graph edit; the same question re-answers correctly **immediately** (Bible UC-3 AC); a "Thank you — this is now part of the organization's memory" confirmation | Submission fails → correction remains in a locally-queued "retry" state, never silently dropped | None beyond the initial "this will be attributed to you" notice | `correction.submitted {correction_id}` |
| **View correction history on a fact** | `History` on any claim/edge | `GET` associated correction chain | Any viewer | Skeleton | Chronological list: prior value, corrected value, author, timestamp, rationale | N/A | None | `correction.history_viewed` |
| **Review pending corrections (curator queue)** | Correction review queue (Meera/curator role) | `GET` corrections pending review (site policy may require review before graph write, or may write immediately with review-after) | `reliability`, `admin` | Skeleton list | List of recent corrections with accept/escalate options | N/A | Escalation dialog if a correction looks systemic (e.g. contradicts many facts) | `correction.reviewed` |

### States

- **Immediate effect (default policy):** a correction writes to the graph immediately and is retroactively visible; this is the Bible's explicit acceptance criterion ("the same question re-answers correctly immediately" — UC-3). Sites requiring pre-publication review may configure a review gate, but the default and demo-critical behavior is immediate.
- **Attribution always visible:** no correction is ever anonymous; "corrected by [name] on [date]" is permanent and visible wherever the corrected fact is shown.
- **Correction becomes a training signal:** silently, on the backend, the Learning agent adds a labelled example to the eval set (Bible §4.5, §15) — this is not user-facing, but the module's copy should say "this improves future answers" so the mental model is accurate.

### Edge cases & failure handling

- **Why does this exist?** JTBD-3 — Anil's judgement must outlive Anil.
- **Which persona?** All; especially high-tenure experts.
- **Which API?** `POST /v1/corrections`.
- **Which agent?** Learning agent (turns corrections into labelled examples, CP-10); Memory agent (surfaces prior corrections as context in future investigations).
- **Which graph nodes/edges?** `Correction` node, `CORRECTED_BY` edge.
- **Which permissions?** Any signed-in role may submit; review/escalation gated to `reliability`/`admin`.
- **What happens offline?** Corrections composed offline queue locally and sync on reconnect, clearly labelled "pending sync," never lost.
- **What if the model fails?** Unaffected — correction submission does not depend on the reasoning model.
- **What if the graph is unavailable?** Correction cannot be durably written; composer shows "can't save right now — try again shortly," retains the user's typed rationale so it isn't lost.
- **What if the API returns nothing / times out?** Client retries with backoff; user is told the correction is "pending," never silently assumed successful.
- **How is it logged?** Every correction is itself an audit-logged, append-only event (Bible §8.5).
- **How is it tested?** UC-3's Gherkin (below) is a release-gating regression test — corrections must visibly change the very next answer to the same question.
- **How is it verified?** The regression suite (Bible §15.5) grows by exactly one case per meaningfully-different correction type, monotonically.

### Acceptance criteria

```gherkin
Feature: Correction & Learning Loop

  Scenario: A correction is durable and immediately effective
    Given Anil corrects an answer with a reason
    When the correction is submitted
    Then it is written as an attributed graph edit with {prior_value, new_value, author, timestamp, rationale}
    And the same question, asked again, now answers correctly
    And the correction is visible in the fact's history to any future viewer
```

## 2.7 M3 — Decision Memory & Replay

**Engineering mapping:** §5.7 decision graph (additive, demo-optional). **Priority:** Could. **Pillar:** Operate. **Persona:** Meera, Deepak.
**JTBD:** JTBD-7 (replay past reasoning and judge whether it still holds).

### Why this exists
Turns "what happened" into "why we decided that, and whether that reasoning still holds" — the Decision Intelligence Lifecycle (§0.5) made explorable after the fact.

### Screen: Decision Replay

**Layout (functional):** a timeline of `Observation → Hypothesis → Evidence → Decision → Alternative(rejected) → RiskAccepted → Outcome → LessonLearned` nodes connected by `LED_TO` edges, each node expandable to its evidencing spans.

### Actions & buttons

| Action | Trigger | API/mechanism | Permission | Loading | Success | Error | Confirmation | Audit event |
|---|---|---|---|---|---|---|---|---|
| **Open a past decision** | From an asset's history, or a link from M1/M7 | Graph query over decision-graph nodes | `reliability`, `admin`; view for others | Skeleton timeline | Full replay renders, including rejected alternatives | Decision graph not populated for this event (additive/optional per Bible §5.7) → "No decision chain recorded for this event" (distinct from "nothing happened") | None | `decision_replay.viewed` |
| **"Would this still hold today?"** | Button on a past Decision node | Re-runs the original hypothesis question through current retrieval (M1 pathway), diffed against the historical answer | `reliability`, `admin` | "Re-evaluating against current knowledge…" | Side-by-side: original reasoning vs. current reasoning, flagging what changed | N/A | None | `decision_replay.reevaluated` |
| **View rejected alternatives** | Expand `Alternative(rejected)` node | Local graph expansion | Any viewer | Instant | Shows what was considered and why it was not chosen | N/A | None | `decision_replay.alternative_viewed` |

### Edge cases
This module is explicitly additive (Bible §5.7: "the core investigation works without it") — its absence for older events, or at sites that have not yet populated decision-graph nodes, must be a clean, honest empty state, never an error. Offline: view-only from cache. Model failure: unaffected (this is a graph read, not a generation task) except for the "would this still hold today" re-evaluation, which depends on M1's pathway and inherits its degradation behavior.

## 2.8 M4 — Knowledge Evolution

**Engineering mapping:** §5.10 (evolution & decay). **Priority:** Could (Should for the `KnowledgeRisk` flag surface). **Pillar:** Operate. **Persona:** Meera.
**JTBD:** underlies JTBD-4 (don't trust knowledge that has quietly gone stale).

### Screen: Knowledge Health

**Layout (functional):** a list of `KnowledgeRisk` flags raised by the nightly decay job — each shows what triggered the flag (equipment/vendor/SOP change, expert departure, contradictory sensor evidence), the affected facts, and a path to resolve (correct, re-verify, or supersede).

### Actions & buttons

| Action | Trigger | API/mechanism | Permission | Loading | Success | Error | Confirmation | Audit event |
|---|---|---|---|---|---|---|---|---|
| **View flagged knowledge** | Nav entry / notification | Nightly-job output query | `reliability`, `admin` | Skeleton list | List of flags with trigger reason and affected facts | No flags → "No knowledge currently flagged as at-risk" (a good state) | None | `knowledge_risk.viewed` |
| **Re-verify a flagged fact** | `Re-verify` on a flag | Opens the fact in context (deep link to M1 or the source document) | `reliability`, `admin` | N/A | Fact confirmed still valid → flag cleared, logged | N/A | None | `knowledge_risk.reverified` |
| **Supersede a flagged fact** | `Mark superseded` | Writes a `SUPERSEDES` edge, effectively a correction | `reliability`, `admin` | N/A | Old fact bounded (`effective_to` set), never deleted (CP-7) | N/A | Confirm dialog naming what will be superseded | `knowledge_risk.superseded` |

### Edge cases
Never delete a superseded fact — bound it (CP-7 bitemporal model); this makes "why did we used to believe X" always answerable. Model/graph failure: this screen reads precomputed nightly output, so it is resilient to live model outage; if the nightly job itself failed to run, the screen must say so explicitly ("Knowledge health last computed [date] — nightly job did not complete since"), never silently show stale data as current.

## 2.9 M5 — Organizational Memory

**Engineering mapping:** `Person`/`KNOWS` nodes (§5.2–5.3); JTBD-3 capture mechanism; feeds the "who to ask" field in M1's AbstainCard. **Priority:** Should. **Pillar:** Operate. **Persona:** Meera (curates), Anil (source).

### Screen: Expertise Map

**Layout (functional):** a directory of people, assets/failure-modes they are linked to via `KNOWS` edges, and a retirement-risk indicator; primarily a *read* surface that feeds other modules (the "who to ask" in an abstention, the reviewer suggestion in M8).

### Actions & buttons

| Action | Trigger | API/mechanism | Permission | Loading | Success | Error | Confirmation | Audit event |
|---|---|---|---|---|---|---|---|---|
| **View expertise for an asset/failure mode** | From M1's AbstainCard "who to ask," or direct nav | Graph query on `KNOWS` edges | Any viewer | Skeleton | List of people with relevant expertise and tenure | No one recorded → "No expertise on file for this — consider capturing it" (actionable empty state) | None | `org_memory.viewed` |
| **Add/edit an expertise record** | `Add expertise` (typically Meera, on behalf of capturing Anil's knowledge) | Writes/edits a `Person`–`KNOWS`→asset/failure-mode edge | `reliability`, `admin` | N/A | Record saved, immediately available to future "who to ask" lookups | N/A | None | `org_memory.updated` |
| **Flag retirement risk** | Toggle on a person's record | Updates `retirement_risk` property | `reliability`, `admin` | N/A | Person surfaced with priority in capture-outreach lists | N/A | None | `org_memory.risk_flagged` |

### Edge cases
This module holds `Person` data — PII minimization applies (Bible §8.8: "Prahari stores expertise relationships, not HR records"). No screen in this module may display data beyond role/expertise/tenure/retirement-risk; it is not an HR system and must never become one. Offline: read-only from cache. No permission: view-only, edit buttons hidden.

## 2.10 M9 — Audit & Provenance Center

**Engineering mapping:** FR-10, §8.5; API `GET /v1/audit?actor=&action=&from=&to=` (Bible §7.3). **Priority:** Should. **Pillar:** Protect. **Persona:** Deepak.

### Screen: Audit Log

**Layout (functional):** a filterable, append-only log of every read, answer, proposed write, and committed write, each entry showing actor, action, timestamp, and a link to the full context (prompt manifest hash, model id, span ids — Bible §8.5).

### Actions & buttons

| Action | Trigger | API call | Permission | Loading | Success | Error | Confirmation | Audit event |
|---|---|---|---|---|---|---|---|---|
| **View audit log** | Nav entry (role-gated) | `GET /v1/audit?actor=&action=&from=&to=` | `admin`, `auditor` (site-scoped for `reliability`/`compliance`) | Skeleton table | Paginated, cursor-based log (Bible §7.1) | N/A | None | `audit.viewed` (meta-audited) |
| **Filter by actor/action/date** | Filter controls | Same endpoint with query params | Same | Instant | Table re-filters | N/A | None | `audit.filtered` |
| **Open full context of an answer** | Click a logged investigation entry | Deep link to the reconstructed investigation (question, context ids, prompt manifest hash, model id, verdict — CP-7 reproducibility) | Same | Skeleton | Full reproducible record shown | Underlying context expired/archived per retention policy → "Full context archived per retention policy — summary shown" | None | `audit.context_viewed` |
| **Export audit range** | `Export` | Server-side job producing a signed export | `admin`, `auditor` | Progress indicator | Downloadable signed file | Export fails → retry, never a silent partial file | None | `audit.exported {range}` |

### Edge cases
This log is append-only by design (Bible §8.1: tampering control — "revoked UPDATE/DELETE"); the UI must never offer an edit or delete action on any entry, full stop. No permission: module invisible in nav (per Global Shell rule). Offline: unavailable (an audit log that could be falsified offline is worse than one that is simply unreachable) — shows a clear "requires connection" state, not a stale cached log presented as current.

## 2.11 M10 — Decision Analytics

**Engineering mapping:** Bible §1.9 KPIs & success metrics. **Priority:** Should. **Pillar:** Operate. **Persona:** Meera.

### Screen: Decision Analytics Dashboard

**Layout (functional):** KPI cards and trend charts for: time-to-answer at point of symptom (target ≤ 90s), recurrence rate of previously-documented failures (target: measurably falling), % of work orders originating from a Prahari hypothesis, audit prep time (target: hours, not days), and resolution-corpus size (target: monotonically increasing — the flywheel, §0.7, made visible as a number).

### Actions & buttons

| Action | Trigger | Mechanism | Permission | Loading | Success | Error | Confirmation | Audit event |
|---|---|---|---|---|---|---|---|---|
| **View dashboard** | Nav entry | Aggregation query over audit/investigation/correction data | `reliability`, `compliance`, `admin` | Skeleton cards | KPI values + trend lines render | Insufficient history to trend (new deployment) → "Not enough data yet — trends appear after [N] days of use" (honest, not a broken chart) | None | `analytics.viewed` |
| **Drill into a KPI** | Click a KPI card | Deep-links to the underlying records (e.g. recurrence rate → the specific recurring failure-mode instances) | Same | Skeleton | Detail list renders | N/A | None | `analytics.drilldown` |
| **Change time range** | Date range selector | Re-queries with new range | Same | Instant | Chart re-renders | N/A | None | `analytics.range_changed` |

### Edge cases
Every KPI target in this dashboard is explicitly a design-judgement estimate (`[D]` per Bible §0.2) until validated by the evaluation harness (Bible §15) — the dashboard must never present a target as an already-achieved fact; it shows *actuals* against *targets*, clearly distinguished. Offline: unavailable (requires aggregation across live data); shows last-refreshed timestamp when reachable.

## 2.12 M11 — Admin & Ingestion Console

**Engineering mapping:** §2.6 ingestion data flow, §8.2 RBAC/tenant admin. **Priority:** Must (ingestion), Should (admin). **Pillar:** Build + Protect. **Persona:** Deepak, Meera.

### Screen: Document Ingestion

**Layout (functional):** upload area, per-document ingestion status (queued → parsing → OCR if needed → extraction → entity resolution → complete), and a failure/quarantine list for documents that could not be confidently processed.

### Actions & buttons

| Action | Trigger | API call | Permission | Loading | Success | Error | Confirmation | Audit event |
|---|---|---|---|---|---|---|---|---|
| **Upload document(s)** | `Upload` / drag-and-drop | `POST /v1/documents` (multipart) → `202 {doc_id, job_id}` | `reliability`, `admin` (upload); `compliance` may upload evidence docs | Per-file progress bar | Document enqueued; status card appears | Duplicate content hash → `409`, "Already ingested as [doc_id]" (Bible §7.6 idempotency) | None | `document.uploaded` |
| **View ingestion status** | Click a document's status card | `GET /v1/ingestion/{job_id}` | Same + view for others | Live-updating stage indicator | Shows current stage; on completion, links to the resulting graph nodes | Failed stage (e.g. unreadable scan) → quarantined with reason, **never silently promoted to a fact** (Bible §1.8: "OCR garbage / rotated scans → low-confidence extraction flagged, never promoted to a fact") | None | `ingestion.status_viewed` |
| **Review quarantined document** | From the failure list | Opens extraction preview with confidence flags | `reliability`, `admin` | N/A | Human can manually confirm/correct low-confidence extractions (feeds M2/M8) | N/A | Confirm before promoting a low-confidence extraction to a fact | `ingestion.quarantine_reviewed` |
| **Manage RBAC / tenant settings** | Admin settings | Tenant/role management APIs | `admin` only | N/A | Role/site assignments updated | N/A | Confirm on any privilege escalation | `admin.rbac_updated` |

### Edge cases
A duplicate/near-duplicate document (e.g. a versioned P&ID) creates a `SUPERSEDES` edge, never an overwrite (Bible §1.8). A document containing text that resembles instructions to the system is treated strictly as data, never as instruction (FM-7/ADR-011) — this is a security-critical UI note: ingestion previews must not "render" untrusted document text in any way that could be mistaken for system output. No permission: upload/admin controls hidden; ingestion status remains viewable to relevant roles.

## 2.13 M12 — Field Mode (mobile-first surface)

**Engineering mapping:** §10.7 signature surface 4. **Priority:** Must. **Pillar:** Design. **Persona:** Ravi.

### Why this exists
Ravi's 90-second success path is the product's north star (Bible §10.7). Field Mode is not a "responsive breakpoint" afterthought — it is the primary design target that the console is built up from, not down to.

### Functional requirements (behavioral; visual treatment = design.md)
- One-handed reach zone; tap targets ≥ 44px (accessibility floor, refined visually in design.md).
- Works fully offline against cached answers and a locally-cached graph slice (CP-9); the DegradedBanner (§2.1) is present and honest here above all other surfaces.
- A high-contrast "glare mode" toggle for outdoor/bright conditions.
- Voice-to-question input as a fallback for gloved hands (transcribed text goes through the identical M1 pathway — no separate "voice answer" logic).
- AnswerCard + `TraversalTrace` (linear breadcrumb) stacked; the full `GraphCanvas` is available on demand, never forced.
- Installable PWA, not a native app (Bible ADR-013) — this is explicitly a scope boundary, not an oversight.

### Edge cases
Everything specified for M1 applies here identically — Field Mode is the same Decision Investigation module under a different layout constraint, not a different feature set. Loss of connectivity mid-question: falls to the CP-9 `-everything` rung ("who to ask," pulled from a locally cached Organizational Memory slice) rather than a spinner that never resolves.


---

# PART 3 — CROSS-CUTTING REQUIREMENTS

## 3.1 Functional Requirements (master table)

Extends Bible §1.5 FR-1…FR-10 with the module-level sub-requirements implied by Part 2. Every sub-requirement traces to exactly one parent FR so nothing here is an orphan requirement.

| ID | Requirement | Module | Parent (Bible) |
|---|---|---|---|
| FR-1 | Ingest PDF/scan/CAD/CSV/DCS-export and extract entities+relations with provenance | M11 | FR-1 |
| FR-1.1 | Quarantine, never auto-promote, low-confidence extractions | M11 | FR-1, BR-1 |
| FR-1.2 | Duplicate/versioned documents create supersession edges, never overwrite | M11 | FR-1, CP-7 |
| FR-2 | Resolve multiple identifiers to one asset node with human adjudication + reversibility | M2 | FR-2 |
| FR-2.1 | Ambiguous identifiers abstain into the adjudication queue, never auto-merge | M2 | FR-2 |
| FR-2.2 | Every merge is unmergeable, restoring the prior mapping exactly | M2 | BR-4 |
| FR-3 | Dual retrieval (graph traversal + vector) with a query-classifying router | M1 | FR-3 |
| FR-4 | Grounded generation with per-claim citations and abstention | M1 | FR-4 |
| FR-4.1 | Abstention always includes what is known and who to ask | M1, M5 | CP-4 |
| FR-5 | Compliance rule engine evaluating encoded rules vs graph state | M6 | FR-5 |
| FR-5.1 | Every compliance view discloses encoded-vs-total clause coverage | M6 | BR-3, FM-6 |
| FR-6 | Approved-action tool layer writing to CMMS/DMS | M7 | FR-6 |
| FR-6.1 | Drafting and approving require distinct-authority identities | M7 | CP-3 |
| FR-7 | Correction loop that persists as graph edits + eval labels | M8 | FR-7 |
| FR-7.1 | A correction changes the very next answer to the same question | M8 | CP-10 |
| FR-8 | Temporal/bitemporal versioning; answer reconstructable as-of a date | M1, M3, M4 | FR-8 |
| FR-9 | Graph-centric UI: traversal visible, correctable, mobile-first | M1, M12 | FR-9 |
| FR-10 | Full audit log of every read/write/answer | M9 | FR-10 |
| FR-11 *(new)* | Decision graph replay: reconstruct and re-evaluate past reasoning chains | M3 | §5.7 |
| FR-12 *(new)* | Knowledge decay detection and flagging, triggered by defined events, not age alone | M4 | §5.10 |
| FR-13 *(new)* | Organizational memory capture: expertise linked to assets/failure modes, with retirement-risk flagging | M5 | JTBD-3 |
| FR-14 *(new)* | Decision analytics: KPI dashboard against the Bible's target metrics, actual-vs-target always distinguished | M10 | §1.9 |

## 3.2 Non-Functional Requirements

Reused verbatim from Bible §1.6 (do not re-derive numeric targets here — the Bible's evaluation harness, §15, is the authority for validating them):

| ID | Category | Target `[D]` | Owning module(s) |
|---|---|---|---|
| NFR-1 | Investigation latency | P50 ≤ 4s, P95 ≤ 9s end-to-end | M1 |
| NFR-2 | Compliance evaluation latency | ≤ 2s per asset obligation set | M6 |
| NFR-3 | Availability | 99.5% pilot; degrade, never fail | All (Global Shell CP-9) |
| NFR-4 | Data residency | In-boundary; air-gap-capable | M11, M9 |
| NFR-5 | Grounding faithfulness | ≥ 0.90 RAGAS faithfulness on golden set | M1 |
| NFR-6 | Citation accuracy | ≥ 0.95 of cited spans support their claim | M1, M6 |
| NFR-7 | Abstention correctness | False-answer rate ≤ 2% | M1 |
| NFR-8 | Scalability | 10⁵ assets, 10⁶ documents, 10⁷ edges (enterprise) | M2, M11 |
| NFR-9 | Onboarding | New document class ingestible without code change | M11 |
| NFR-10 | Accessibility | WCAG 2.1 AA | Global Shell, all modules |

**Product-level additions:**

| ID | Category | Requirement | Owning module(s) |
|---|---|---|---|
| NFR-11 | Explainability | Every AI-originated statement in the product must be one click from its evidence — no screen may show a conclusion with no path to its source | M1, M6 |
| NFR-12 | Offline-first | Field Mode must degrade to a usable (if reduced) state with zero network, never a blank screen | M12 |
| NFR-13 | Non-ambiguity of write state | A drafted action and a committed action must never be visually or textually confusable | M7 |

## 3.3 Business Rules

Reused and extended from Bible §1.7:

- **BR-1:** An unsourced fact is not admitted to the graph (CP-1).
- **BR-2:** A write to any system of record requires an approving human identity (CP-3).
- **BR-3:** Compliance output is evidence + gaps, never a legal opinion.
- **BR-4:** Entity merges are proposals until adjudicated; all merges are reversible.
- **BR-5:** Every regulatory rule carries an effective-date range; superseded rules are retained, not deleted.
- **BR-6 *(new)*:** Abstention is never styled or copy-written as an error; it is a distinct, positive-framed state (P8, §0.4).
- **BR-7 *(new)*:** No correction is ever anonymous; attribution is permanent and visible on the corrected fact (CP-10, JTBD-3).
- **BR-8 *(new)*:** No screen may imply a metric target has been achieved when it is a design-judgement estimate pending evaluation-harness validation (Bible §0.2 evidence tiers, applied to Decision Analytics).
- **BR-9 *(new)*:** Person-linked data (Organizational Memory) is limited to role/expertise/tenure/retirement-risk; it is never an HR record (Bible §8.8 PII minimization).

## 3.4 Global states & confidence contract (functional, not visual)

Every AI-originated statement in the product carries exactly one of four states. **This is a functional/product contract; the colours, icons, and typography that express it are `design.md`'s decision, already tokenised there as `--grounded` / `--inferred` / `--unsupported` / `--abstain` per the Engineering Bible's UI System volume (§10.2) — but this PRB is what mandates that the states exist and what they mean.**

| State | Meaning | Never confused with |
|---|---|---|
| **Grounded** | Every claim in this statement resolves to ≥ 1 cited source span | "Inferred" (partial grounding) |
| **Inferred** | Reasoned from grounded facts but not itself directly cited | "Grounded" (fully cited) |
| **Unsupported** | Present in a draft but stripped/flagged by the Verifier — shown only where surfacing the gap itself is useful (e.g. "the model considered X but could not support it") | An error |
| **Abstained** | The system declined to answer because grounding fell below threshold — includes what is known and who to ask | An error, a bug, or "no results" |

**Rule that binds design.md too:** confidence must never be encoded by colour alone (NFR-10); every state carries a label or icon in addition to any colour treatment design.md assigns it.

## 3.5 Notification & event framework

Every write-adjacent event that a role would reasonably want to know about generates a notification, deep-linked to the exact record:

| Event | Notified role(s) | Deep link target |
|---|---|---|
| New resolution proposal in queue | `reliability`, `admin` | M2 Resolution Queue |
| Action drafted, awaiting approval | Approvers per site policy | M7 Execution Center |
| Action approved and committed | Original drafter | M7 action detail |
| Obligation newly overdue | `compliance`, `reliability` | M6 Compliance Matrix |
| Knowledge risk flag raised | `reliability`, `admin` | M4 Knowledge Health |
| Correction submitted on a fact you authored/investigated | Original investigator | M8 correction detail |
| Ingestion quarantine requires review | `reliability`, `admin` | M11 quarantine list |
| Role/permission changed for you | Affected user | N/A (shell toast only) |

## 3.6 Global edge & failure case framework

Reused and generalized from Bible §1.8, applied as a checklist every module in Part 2 has already answered individually. Restated once here as the canonical framework so future features (not yet in this PRB) are held to the same bar:

1. Duplicate/near-duplicate input → supersession, never overwrite.
2. Conflicting facts across sources → a `Contradiction` surfaced to a human, never silently resolved.
3. Low-confidence extraction → flagged, never promoted to a fact.
4. Ambiguous identifier → resolution abstains, asks a human.
5. Model unavailable → degradation ladder (CP-9), never a blank screen.
6. Content inside an ingested document that resembles an instruction → treated as data, never as instruction (FM-7).
7. No permission → the feature is invisible or view-only, never a confusing disabled state without explanation.
8. Empty data → an honest, specific empty state, never indistinguishable from "everything is fine" or "something broke."
9. Partial/failed write → never silently marked successful; always distinguishable from a committed state.
10. Offline → cached/last-known state, honestly labelled with its age, never presented as live.

## 3.7 Accessibility

WCAG 2.1 AA (NFR-10) applies to every module. Product-level (non-visual) requirements this PRB owns, distinct from design.md's contrast/typography ownership:
- Confidence state is never colour-only (§3.4).
- Every interactive element is keyboard-reachable and screen-reader labelled, including graph nodes/edges in `GraphCanvas`.
- Reduced-motion is respected; the traversal animation must have a static equivalent (e.g. the `TraversalTrace` breadcrumb) that carries the same information.
- Tap targets ≥ 44px in Field Mode (M12).


---

# PART 4 — THE DECISION INTELLIGENCE NARRATIVE

This part reframes the Engineering Bible's demo guide (§11) in product language. It is a product requirement, not a presentation nicety: **if the modules in Part 2 cannot support this narrative end to end, Part 2 is incomplete**, not the narrative wrong.

## 4.1 The narrative shape

Never demo, pitch, or onboard a new user with: *"ask the AI, get an answer."* Always: 

```
Incident  →  Decision Investigation  →  Historical Decisions  →  Expert Knowledge
    →  Compliance  →  Recommended Action  →  Human Approval
    →  Knowledge Updated  →  Future Intelligence Improved
```

| Narrative beat | Product module | Bible demo-guide beat (§11.2) |
|---|---|---|
| An incident/symptom appears | Observation (§0.5) | "The 02:40 story" |
| Decision Investigation runs | M1, backed by M2's resolved asset map | "Primary wow: resolution" + "Secondary wow: investigation" |
| Historical decisions are checked | M3 Decision Memory & Replay | (extends the Bible's flow — replay is additive) |
| Expert knowledge is consulted | M5 Organizational Memory ("who to ask," or a KNOWS-linked expert confirms) | Implicit in JTBD-3 |
| Compliance is checked | M6 Compliance Intelligence | "Compliance" beat |
| A recommended action is drafted | M7 Execution Center (draft) | "Execute" beat |
| A human approves | M7 Execution Center (approval, CP-3) | "Execute" beat |
| Knowledge is updated | M8 Correction & Learning Loop | Implicit throughout; explicit at "The refusal" |
| Future intelligence improves | The flywheel (§0.7) — visible in M10 Decision Analytics as corpus-size trending up | "Close: the moat line" |

## 4.2 The three wow moments (product framing)

1. **The Living Asset Map assembling itself** (M2) — four names becoming one pump, live, with a human's single tap. This demonstrates the moat, not a feature.
2. **A Decision Investigation tracing five never-linked documents** (M1) — a causal chain, not a document dump.
3. **A deliberate refusal** (M1's AbstainCard) — the system, asked the same question with its graph disabled, does not guess. It says what it can't ground and who to ask. This is the single most important state in the entire product and must never be quietly removed to make a demo "look more capable."

## 4.3 What every onboarding, sales, and judge-facing surface must never say

- "We built an AI chatbot for industrial data." (§0.1)
- Any framing that leads with GraphRAG, Neo4j, or the model vendor before leading with the decision-intelligence problem.
- Any implied claim of compliance completeness (BR-3/FM-6, non-negotiable in every context, not only inside M6).

---

# PART 5 — SUCCESS METRICS, SCOPE, AND ROADMAP

## 5.1 KPIs & success metrics

Reused from Bible §1.9, mapped to their owning module for dashboard construction (M10):

| KPI | Baseline (phone call) | Target | Module |
|---|---|---|---|
| Time-to-answer at 02:40 | ~30–60 min (call + guess) | ≤ 90s | M1, M10 |
| Recurrence rate of previously-documented failures | Unmeasured | Measurably ↓ over pilot | M3, M10 |
| % work orders originating from a Prahari hypothesis | 0 | Measurable, growing fraction | M7, M10 |
| Audit prep time | Days | Hours | M6, M10 |
| Resolution corpus size (adjudications) | 0 | Monotonically ↑ with use | M2, M10 |

**Flywheel metric (new, product-level):** correction-to-improvement latency — the time between a correction being submitted (M8) and it being reflected in the next relevant answer (M1). Target: immediate (same session), per UC-3's acceptance criterion. This is the single number that proves P7 (§0.4) is real and not a slogan.

## 5.2 MoSCoW, restated under product module names

| Priority | Modules |
|---|---|
| **Must** | M1 Decision Investigation, M2 Living Asset Map, M8 Correction & Learning Loop, M11 (ingestion half), M12 Field Mode, Global Shell |
| **Should** | M6 Compliance Intelligence, M7 Execution Center, M4 (KnowledgeRisk flags), M5 Organizational Memory, M9 Audit & Provenance Center, M10 Decision Analytics, M11 (admin half) |
| **Could** | M3 Decision Memory & Replay, geospatial asset map *(not specified further in this PRB — out of current scope)*, blind-spot report *(likewise)* |
| **Won't (this cycle)** | Autonomous writes of any kind, a native mobile app (PWA only, ADR-013), multi-plant network features |

## 5.3 MVP scope — Hackathon vs Enterprise

Reused from Bible §1.11, restated so product and engineering scope decisions cannot silently diverge:

| | Hackathon MVP | Enterprise MVP |
|---|---|---|
| Corpus | Curated public-source demo corpus with provenance | Customer estate connectors |
| M2 Living Asset Map | Live demo of 4→1 merge + human correction | At-scale adjudication queue |
| M6 Compliance | One encoded rule family (OISD interval) as proof | Full rule library + state parameterisation |
| Auth | Single-tenant, role stub | Full RBAC/ABAC, OIDC, multi-tenant |
| Deploy | Docker Compose, one box | K8s + GPU + observability |

## 5.4 Roadmap posture

Sprint-level planning is out of scope for this PRB (that is Bible §17's job). This PRB's only roadmap obligation is to confirm that the **critical path is a single line**: ingestion → resolution → investigation → correction, end to end, before any Should/Could module is built — matching the Bible's own risk register entry ("4-day build vs scope → freeze to MVP ring; demo path end-to-end first," §1.12).

---

# PART 6 — RISK REGISTER

Reused and reframed from Bible §1.12 in decision-intelligence terms:

| Risk | Likelihood | Impact | Response |
|---|---|---|---|
| Scope exceeds build capacity | Certain (any hackathon timeline) | Fatal | Freeze to Must-only ring; demo path end-to-end first |
| Perceived as "another RAG demo" | Medium | Fatal | Lead with M2 (resolution), never with retrieval mechanics |
| Wrong-asset merge corrupts Decision Memory | Medium | Fatal | Human adjudication + reversibility + versioning (M2, non-negotiable) |
| Live demo failure | Medium | High | CP-9 ladder + precomputed fallback (Bible §11.7) |
| Compliance module perceived as a liability, not an asset | Low-Medium | High | BR-3/FM-6 footer is never optional, in any build |
| Originality challenge (hackathon) | Low | Fatal | All work in-window; provenance log; OSS only (Bible §8.9) |


---

# PART 7 — FEATURE TRACEABILITY MATRIX

This matrix is the bridge from this PRB into implementation. Before any architecture or code is written, every row must resolve — a feature with a blank cell anywhere in this table is not ready to build.

| Feature (Module) | Business objective | Persona | User story | Screen(s) | Agent(s) | API(s) | Permission | Acceptance criteria | Demo scenario | Success metric |
|---|---|---|---|---|---|---|---|---|---|---|
| M1 Decision Investigation | Collapse 30–60 min phone-call chains into 90s cited answers | Ravi | UC-1 / JTBD-1 | Investigation Console | Planner, Retriever, Executor, Critic, Verifier | `POST/GET /v1/investigations`, `WS /v1/stream/investigations/{id}` | Any signed-in role (view); technician+ (draft action) | §2.2 Gherkin | Secondary wow (Bible §11.3) | Time-to-answer ≤ 90s |
| M2 Living Asset Map | Build the non-copyable resolution corpus | Ravi, Meera | UC-3-adjacent / underlies JTBD-1, JTBD-4 | Resolution Queue, Asset History | Entity Resolution Service | `GET /v1/resolution/queue`, `POST /v1/resolution/{id}/adjudicate`, `POST /v1/resolution/unmerge/{id}` | reliability/admin (adjudicate), admin (unmerge) | §2.3 Gherkin | Primary wow (Bible §11.3) | Resolution corpus size ↑ |
| M3 Decision Memory & Replay | Make past reasoning replayable and re-testable | Meera, Deepak | JTBD-7 | Decision Replay | (graph read; M1 pathway for re-evaluation) | Graph query; reuses `/v1/investigations` for re-evaluation | reliability/admin (full), view for others | §2.7 (narrative) | Not in core 12-min demo (additive) | Recurrence rate ↓ |
| M4 Knowledge Evolution | Flag stale/decayed knowledge before it misleads someone | Meera | Underlies JTBD-4 | Knowledge Health | Nightly decay job (non-agent) | Internal query over `KnowledgeRisk` | reliability/admin | §2.8 (narrative) | Not in core demo | Fraction of flags resolved |
| M5 Organizational Memory | Capture expert judgement before it retires | Anil → org, Meera | JTBD-3 | Expertise Map | (feeds M1 AbstainCard) | Graph query/update on `Person`/`KNOWS` | reliability/admin (edit), any (view) | §2.9 (narrative) | Referenced in "who to ask" beat | Expertise records captured pre-retirement |
| M6 Compliance Intelligence | Audit-ready evidence, never a legal claim | Meera, compliance officer | UC-2 / JTBD-2 | Compliance Matrix | Compliance agent | `GET /v1/compliance/assets/{id}`, `GET /v1/compliance/coverage` | compliance/reliability/admin (full), any (view) | §2.4 Gherkin | "Compliance" beat | Audit prep time ↓ |
| M7 Execution Center | No unattended writes to a system of record | Ravi (draft), Meera (approve) | UC-4 / completes JTBD-1 | Action Draft & Approval | Executor (drafting content only) | `POST /v1/actions/work-order/draft`, `POST /v1/actions/work-order/submit` | technician/reliability (draft), reliability/admin (approve) | §2.5 Gherkin | "Execute" beat | % work orders from Prahari hypotheses |
| M8 Correction & Learning Loop | Reasoning outlives the person who produced it | All | UC-3 / JTBD-3 | Correction Composer (cross-cutting) | Learning, Memory | `POST /v1/corrections` | Any signed-in role | §2.6 Gherkin | Implicit throughout; explicit at "the refusal" | Correction-to-improvement latency |
| M9 Audit & Provenance Center | Deepak can sign off on the pilot | Deepak | JTBD-5 | Audit Log | Audit sink (non-agent) | `GET /v1/audit` | admin/auditor (full), site-scoped for reliability/compliance | (security checklist, Bible §14.7) | Answers "how do you handle our data" | 100% of writes traceable to an approver |
| M10 Decision Analytics | Make the flywheel visible as a number | Meera | Cross-cutting | Analytics Dashboard | (aggregation, non-agent) | Internal aggregation queries | reliability/compliance/admin | (KPI table, §5.1) | "Close: the moat line" | All five Bible §1.9 KPIs |
| M11 Admin & Ingestion Console | Onboard new document classes without code change | Deepak, Meera | NFR-9 | Document Ingestion | Ingestion Pipeline (non-agent) | `POST /v1/documents`, `GET /v1/documents/{id}`, `GET /v1/ingestion/{job_id}` | reliability/admin (upload), admin (RBAC mgmt) | (edge cases, §2.12) | "Problem, shown" setup beat | New doc class ingestible without code change |
| M12 Field Mode | 90-second success path in the field | Ravi | JTBD-1 (field conditions) | Field Investigation Console | Same as M1 | Same as M1 | Same as M1 | Same as M1, plus offline cases | Entire demo could run on this surface | Time-to-answer ≤ 90s, glove/glare usable |

---

# PART 8 — GOVERNANCE OF THIS DOCUMENT

## 8.1 Authority order (restated for engineering onboarding)

1. **Engineering invariants CP-1…CP-10** (Bible §0.4) — never violated by any requirement in this PRB, ever. If a future addition to this PRB appears to require violating one, the addition is wrong, not the invariant.
2. **This PRB** — supreme for product scope, behavior, and requirements.
3. **`design.md`** — supreme for visual and interaction design within the behavior this PRB specifies.
4. **The Engineering Bible's other volumes** — supreme for technical mechanism (how, not what/whether).

## 8.2 Change control

Any change to a **Must** feature's behavior, or to Part 0's locked identity, requires a logged decision (in the companion `architecture_decisions.md` — see §8.3) with reason, alternatives considered, and trade-offs — the same discipline the Engineering Bible applies to its own ADRs (Bible §13). This PRB is versioned; §-level diffs should be summarized at the top of the file on every substantive revision.

## 8.3 Companion files this PRB assumes exist in the repository

This PRB is written assuming the development workflow already agreed for this project, and does not repeat that specification here. For reference, the companion files expected alongside this PRB, `design.md`, and the Engineering Bible are: `memory.md` (persistent development memory), `implementation_status.md` (per-feature build status), `architecture_decisions.md` (ADRs for product/engineering decisions made during build), `known_bugs.md`, `todo.md`, `prompts.md` (production agent prompts), `agent_memory.md` (investigation patterns, correction history, reusable reasoning), `ui_rules.md` (the enforcement doc for "never redesign, always defer to design.md"), `coding_rules.md`, and `verification_checklist.md`. Each module in Part 2 should have a corresponding entry in `implementation_status.md` tracking its UI/Backend/API/Testing completion independently.

## 8.4 Definition of "this PRB is satisfied" for a given feature

A feature is not complete against this PRB until:
1. Every row of its action table (Part 2) is implemented and its stated permission is enforced.
2. Every edge case listed for it is either handled as specified or explicitly logged as a known gap in `known_bugs.md`.
3. Its Gherkin acceptance criteria pass in the test harness (Bible §14).
4. Its entry in the Feature Traceability Matrix (Part 7) has no blank cell.
5. Its UI has been reviewed against `design.md` for visual conformance and against this PRB for behavioral conformance — two separate reviews, because they are two separate authorities.


---

# APPENDIX A — Glossary

Reused from Bible §18.1, extended with this PRB's product-level vocabulary.

| Term | Meaning |
|---|---|
| **Decision Intelligence Lifecycle** | Observation → Evidence → Hypothesis → Decision → Execution → Outcome → Correction → Knowledge Evolution → Future Decision (§0.5). |
| **Decision Memory** | The replayable record of past reasoning chains — decision graph made product-visible (M3). |
| **Decision Replay** | The act of reconstructing and re-testing a past decision's reasoning against current knowledge (M3). |
| **Knowledge Evolution** | The continuous re-testing and decay-flagging of what the graph believes (M4, §5.10). |
| **Organizational Memory** | Captured expertise/relationships between people and assets/failure modes, used for "who to ask" and corpus continuity (M5). |
| **The Four Compounding Moats** | Decision Memory, Organizational Intelligence, Knowledge Evolution, Entity Resolution Corpus (§0.7). |
| **Living Asset Map** | The product name for the entity-resolution surface (M2); "the moat, on screen" (Bible §10.5). |
| **Resolution corpus** | The plant-specific, human-validated set of identifier→asset adjudications. (Bible §18.1) |
| **`RESOLVED_AS`** | Graph edge asserting an identifier denotes an asset. (Bible §18.1) |
| **Dual retrieval** | Combined graph traversal + vector search, routed by query class. (Bible §18.1) |
| **Grounding** | The property that every generated claim maps to a source span. (Bible §18.1) |
| **Abstention** | A first-class output stating the system cannot ground an answer (CP-4). (Bible §18.1) |
| **Provenance** | Source span + method + confidence + (if human-touched) person + timestamp on every fact (CP-1). (Bible §18.1) |
| **Bitemporal** | Facts carry both valid-time and transaction-time (CP-7). (Bible §18.1) |
| **Degradation ladder** | Ordered fallback states so the system downgrades, never blanks (CP-9). (Bible §18.1) |
| **Decision graph** | Observation→Hypothesis→Evidence→Decision→Alternative→RiskAccepted→Outcome→Lesson chain. (Bible §18.1) |
| **CP-1…CP-10** | The engineering invariants (Bible §0.4). |
| **`[V]/[R]/[D]`** | Verified / Reported / Design-judgement evidence tiers (Bible §0.2) — this PRB inherits the same convention; any numeric target repeated in this document is `[D]` unless the Bible marks it otherwise. |

---

# APPENDIX B — Cross-reference map (PRB module → Engineering Bible section)

So that no requirement in this PRB can silently drift from what is actually specified as buildable:

| PRB module | Primary Bible section(s) |
|---|---|
| Part 0 Product Philosophy | Bible §0.6 canonical facts, §1.1 mission/vision/problem |
| Part 1 Personas/RBAC | Bible §1.3 personas, §8.2 RBAC/ABAC |
| M1 Decision Investigation | Bible §1.4 UC-1, §4.1 agent roster, §7.3–7.4 API, §10.4 |
| M2 Living Asset Map | Bible §3.2, §5.6, §7.3 resolution endpoints, §10.5, §16.3 |
| M3 Decision Memory & Replay | Bible §5.7, §5.2 reasoning primitives |
| M4 Knowledge Evolution | Bible §5.10 |
| M5 Organizational Memory | Bible §5.2–5.3 Person/KNOWS |
| M6 Compliance Intelligence | Bible §1.4 UC-2, §7.3 compliance endpoints, §8.10, §10.6 |
| M7 Execution Center | Bible §1.4 UC-4, §4.2 tool calling, §7.3 actions endpoints |
| M8 Correction & Learning Loop | Bible §1.4 UC-3, §4.5 self-correction, §7.3 corrections endpoint, §13 ADR |
| M9 Audit & Provenance Center | Bible §7.3 audit endpoint, §8.5 |
| M10 Decision Analytics | Bible §1.9 KPIs |
| M11 Admin & Ingestion Console | Bible §2.6 ingestion flow, §8.2 |
| M12 Field Mode | Bible §10.7 |
| Global Shell | Bible §2.8 degradation ladder, §10.2–10.3 |
| Part 5 Scope | Bible §1.10–1.11 |
| Part 6 Risk Register | Bible §1.12 |

---

# APPENDIX C — Open questions & assumptions log

Per the Engineering Bible's own evidence-tier discipline (§0.2), every judgement call this PRB made where the Bible was silent is logged here as `[D]`, not silently presented as settled fact. These should be resolved (or explicitly ratified) during the first architecture review and recorded thereafter in `architecture_decisions.md`.

- **`[D]`** Whether corrections (M8) default to immediate-effect or require a pre-publication review gate is left as a site-configurable policy; the demo-critical and default behavior is immediate effect, per UC-3's literal acceptance criterion.
- **`[D]`** Which RBAC roles may confirm low-stakes M2 resolution proposals (this PRB extends `technician` confirmation rights beyond the Bible's literal §8.2 policy example) is a site-policy decision, not a hard requirement — the hard requirement is that `unmerge` stays `admin`-only.
- **`[D]`** The exact set of KPI cards on M10's dashboard beyond the Bible's five (§1.9) plus this PRB's one addition (correction-to-improvement latency) is open to product discovery during pilot.
- **`[D]`** Whether M3 Decision Memory & Replay ships in the hackathon build at all is explicitly optional per the Bible's own "Could" prioritisation (§1.10) and this PRB's §5.2 restatement — it must not be allowed to consume Must-tier build time.
- **`[D]`** Screen names in Part 2 ("Investigation Console," "Resolution Queue," "Compliance Matrix," etc.) are this PRB's naming, not yet ratified against `design.md`'s eventual navigation labels — if `design.md` names something differently, `design.md`'s label wins for display copy, and this PRB's name should be updated to match in the next revision so the two documents don't quietly diverge.

---

*End of Prahari Product Requirements Bible v1.0. This document, `design.md`, and `SENTINEL_Master_Engineering_Bible_MERGED.md` together are the complete, sufficient specification for building Prahari. Nothing outside these three documents should be needed to build any feature described here — if it is, the gap belongs in `architecture_decisions.md`, not in an assumption made silently during implementation.*
