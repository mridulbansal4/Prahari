# Prahari — UI Redesign Brief

> A self-contained prompt. Hand this whole document to any AI design agent.
> Nothing else needs to be supplied for it to produce a complete redesign.

---

## 0. Your role

You are a senior product designer specialising in **industrial / operational software** —
control-room consoles, SCADA and historian front-ends, reliability engineering tools, and
safety-critical decision support. You are being asked to produce a **new UI design** for an
existing, fully-working product called **Prahari**.

This is a redesign of a real system with real constraints, not a greenfield concept exercise.
The product's behaviour is fixed. What you are changing is the interface: layout, hierarchy,
visual language, interaction patterns, and the way evidence and uncertainty are expressed.

Read the whole brief before designing. The **Product laws (§4)** are non-negotiable — they
are the reason the product exists, and a design that breaks them is a failed design regardless
of how good it looks.

---

## 1. What Prahari is

**Prahari is an Industrial Decision Intelligence Operating System.**

Industrial organisations (refineries, power plants, petrochemical sites, EPC contractors)
generate enormous volumes of engineering drawings, maintenance records, operating procedures,
inspection reports, asset registers, and incident investigations. This information is
fragmented across systems, departments, and decades. Engineers spend their time *searching*
instead of *solving*, and institutional knowledge disappears when veterans retire.

Prahari unifies that fragmented knowledge into one continuously-learning decision-intelligence
layer that reasons **across** documents — and **shows its work**. Every answer carries its
evidence, its confidence, and the path it traversed to reach the conclusion.

### What Prahari is NOT — and must never look like

- **Not a chatbot.** No message bubbles, no avatars, no assistant persona, no "typing…"
  metaphor on the core investigation surface. Output is rendered as a **documented analysis**
  a colleague would hand you, in the same card language as human-authored content.
- **Not a document search engine.** It does not return a ranked list of PDFs.
- **Not a generic BI dashboard.** No drag-and-drop widget canvas. Views are opinionated and
  role-specific.
- **Not a consumer AI product.** No sparkle icons, no gradient-purple "AI magic" styling, no
  anthropomorphism. The AI is deliberately *invisible*; what is visible is the evidence.

### The founding story (use this to calibrate tone)

At **02:40**, a pump trips. The night technician has three systems that each know part of the
story and none that connect them. The one person who could connect them retired in 2023. The
real incumbent Prahari competes against is **a phone call to someone who might be dead or
retired.** Design for that person, at that hour, under that pressure.

---

## 2. The users

Six real personas, each with a different job and a different screen:

| Persona | Role | Context |
|---|---|---|
| **Ravi** | Technician / Operator | Night shift, on the plant floor, possibly gloved, possibly on a tablet in sunlight. Needs a grounded hypothesis in 90 seconds. |
| **Meera** | Reliability Engineer | The economic buyer and the approver. Adjudicates the asset map, approves work orders, watches the KPIs. |
| **Deepak** | Admin / OT Security | The veto holder. Cares that every write is attributed and nothing leaves the plant boundary. |
| **Anil** | Reliability veteran, 34 years | The corpus source. Spends his time *depositing* knowledge, not retrieving it. |
| **Compliance Officer** | EHS / Compliance | Needs evidence and gaps against statutory clauses, walk-in audit ready. |
| **Auditor** | External auditor | Strictly read-only. Needs the append-only trail to be legible and reproducible. |

Home is **five completely different dashboards** switched on role — not one dashboard with
things hidden. Navigation items the user cannot access are **hidden entirely**, never
greyed-out teases.

---

## 3. The three moments the design must make unforgettable

These are the product's reason to exist. If a redesign makes anything else prettier but
weakens these three, it has failed.

1. **Resolution (the moat).** Four different identifiers — `P-101B`, "Boiler Feed Pump B", an
   OEM part number, and "the noisy one" — collapse into **one** canonical asset. A human
   confirms the merge. The graph learns. The merge is **reversible and versioned**. This
   human-validated corpus is the thing competitors cannot copy, so the adjudication UI is the
   single most important screen in the product.

2. **Investigation (reasoning, not retrieval).** "Why is P-101B running hot?" produces a
   multi-hop causal chain traversed across five documents nobody had ever linked — vibration
   alarm → upstream strainer → a 2019 inspection note → a 21:00 feedstock change — with
   **every hop citing a specific page**. It streams in live, hop by hop, so the user watches
   the reasoning assemble rather than waiting on a spinner.

3. **The Refusal (abstention as a success state).** Asked something it cannot ground, Prahari
   **does not guess.** It states what it could not ground and **names who to ask**. In a
   plant, a wrong answer is worse than no answer. Abstention must be designed as a
   **confident, positive, first-class outcome** — never styled as an error, never red, never
   apologetic.

---

## 4. Product laws (non-negotiable design constraints)

These are enforced in the backend and must be honoured in the UI.

1. **Every claim is cited.** An AI-authored statement without a source citation is a defect.
   Citations resolve to `document · page · text span` and must be inspectable inline without
   losing your place.
2. **Confidence is always visible.** Four levels: **Grounded / Inferred / Unsupported /
   Abstained**. This is a structural part of every answer component, not an optional
   annotation. It must **never be conveyed by colour alone**.
3. **No write without a distinct approver.** The person who drafts a work order cannot be the
   person who approves it. "Drafted" and "Committed" must be **visually non-confusable** —
   a user must never mistake a proposal for an executed action.
4. **Reversibility is a feature, and must be visible.** Merges can be unmerged; the prior
   state is restored exactly. Say so in the UI, at the point of decision.
5. **Graceful degradation is surfaced, not hidden.** The system runs on a ladder of rungs
   (full → no-model → no-vector → no-graph → no-everything). When degraded, a persistent,
   **non-dismissible** banner explains *in plain language* what the user is and isn't getting
   (e.g. "Semantic search is unavailable — showing graph-linked results only"). Offline and
   air-gapped operation is a first-class mode, not an error condition.
6. **The audit trail is append-only.** The audit screen must present **no edit or delete
   affordance anywhere** — the absence is the design.
7. **Never imply completeness.** Compliance surfaces carry a permanent, **non-collapsible**
   coverage footer stating how many clauses are actually encoded. KPI targets are labelled as
   estimates, never displayed as achieved.
8. **Product names, never engineering names.** The UI says "Living Asset Map", never "the
   entity resolution service"; "Decision Investigation", never "GraphRAG query". Never expose
   the underlying tech in a user-facing label.
9. **Never a generic spinner.** Loading is either a determinate progress bar, a named
   stage indicator (the agent pipeline is `Planner › Retriever › Executor › Critic › Verifier`),
   or a skeleton. The user should always know *what* the system is doing.

---

## 5. Screen inventory — design all of these

Thirteen screens. Descriptions state what exists today; you are free to restructure, merge,
or re-sequence as long as the product laws hold.

### 5.1 Global shell
240px left sidebar (wordmark + nav) and a 56px top bar. Nav is grouped into four sections:
**Investigations** (Decision Investigation, Living Asset Map, Decision Memory & Replay),
**Operations** (Compliance Intelligence, Execution Center, Decision Analytics),
**Knowledge** (Organizational Memory, Knowledge Evolution),
**Administration** (Audit & Provenance, Admin & Ingestion), plus Home and a standalone
**Field Mode** entry. Top bar holds a **persistent confidence legend** (Grounded / Inferred /
Unsupported / Abstained) on the left, and identity + sign-out on the right. The degradation
banner sits directly beneath the top bar when active.

### 5.2 Login
No password. Six persona buttons for demo sign-in, each showing name, role, and a one-line
characterisation. Framed as organisation SSO.

### 5.3 Home — five role dashboards
- **Operator (Ravi):** "Good shift, {name}". A hero card that launches an investigation, plus
  two panels — recent investigations (each tagged Answered / Abstained) and drafted work
  orders.
- **Reliability (Meera):** four stat tiles — resolutions to adjudicate, actions awaiting
  approval, resolution-corpus size ("the moat, compounding"), knowledge risks — plus a KPI
  panel and quick jumps.
- **Compliance:** overdue-obligation count and clauses-encoded ratio, an overdue list framed
  as a "walk-in evidence pack", and the coverage disclaimer.
- **Admin (Deepak):** system rung, recent write events, documents ingested + quarantined,
  knowledge risks, a recent audit trail, and guardian controls.
- **Auditor:** deliberately minimal — recorded event count and recent activity, read-only.

### 5.4 Decision Investigation ★ *hero screen*
A question bar (free-text question + an **"as of" date** for time-travel queries) and an
Investigate action. Empty state offers real questions others at the site are asking.

When running: a two-column layout — the left column streams the named pipeline stage, then the
answer text token by token, then the **answer card**; the right column is a **traversal canvas**
that draws the causal chain node by node as each hop arrives. When an asset was traversed, a
follow-on card offers "Draft a work order from this hypothesis."

The answer card shows: a **Hypothesis** label, the model + prompt-manifest hash (for
reproducibility), the answer, then one row per claim — claim text, inline numbered citation
chips, and a confidence indicator. Clicking a chip reveals the source excerpt inline. Every
claim carries a quiet **"This is wrong"** correction affordance that opens a *Teach Prahari*
composer (correct value + rationale, recorded and attributed permanently).

When abstaining: an **Abstained — I won't guess** card, styled as a confident outcome, listing
what could not be grounded and **who to ask** (person, expertise, years of tenure).

### 5.5 Living Asset Map ★ *the moat*
A stack of proposed-merge cards. Each shows a **visual merge diagram**: a column of candidate
identifiers (value + source system) resolving via an arrow into one canonical asset, with a
confidence percentage, the matching method, and a per-feature score breakdown. Actions:
**Confirm merge** / **Keep separate**, with an explicit note that merges are reversible and
versioned. After confirming, an inline **Unmerge** path remains available to admins. Only
reliability and admin roles may adjudicate; everyone else sees a view-only state. A header
tile counts the accumulated resolution corpus.

### 5.6 Compliance Intelligence
A per-asset table: Clause, Instrument, Asset, Periodicity, Last evidence, Status
(Overdue / Due / Satisfied). Beneath it, the permanent non-collapsible coverage footer
reporting encoded-vs-total clauses per statutory instrument.

### 5.7 Execution Center
Draft work-order cards: asset + symptom, who drafted it, which investigation it came from, and
a status of Draft-awaiting-approval / Committed (with CMMS work-order ID) / Rejected. Approvers
(reliability, admin) get Approve & submit, Reject, and a "simulate CMMS unreachable" control
that exercises the failure path. Non-approvers see an explicit message that a distinct approver
must commit it.

### 5.8 Field Mode ★ *mobile / rugged*
A single stacked column for one-handed use, oversized touch targets, a large question input, a
big Investigate action, a **glare mode** toggle for direct sunlight, and a linear text
traversal trace instead of the SVG canvas. Admins get a demo control to disable the graph and
force the refusal.

### 5.9 Organizational Memory — the largest screen
Anil's knowledge-deposit workspace. Currently 15 tabs, which is the clearest structural problem
in the product and a priority for your redesign. Contains: an expert-recognition panel
(knowledge score, contributions, assets covered, years preserved), AI-generated linking
suggestions, a knowledge-completeness readout across nine categories, a contribution timeline,
a **quick capture** composer (free text + category + tags + voice note + attachment), an **AI
interview mode** where the system interviews the veteran to extract what only he knows, eleven
structured capture modules (FAQs, Tips, Asset Knowledge, Decision Memory, Lessons Learned,
Incidents, Myth vs Reality, Manual Gaps, Common Mistakes, Tribal Knowledge, Best Practices),
and a search tab.

Note: the AI interview is the one place a conversational pattern is legitimate — but even here
it should read as a structured *intake interview*, not a chat with a bot.

### 5.10 Decision Memory & Replay
Pick a past decision and replay the **reasoning chain**, not just a timeline — step cards with
kind, title, detail, and the spans cited. Alternatives that were considered and rejected are
shown but visually de-emphasised.

### 5.11 Knowledge Evolution
"Knowledge decays — Prahari notices." Flag cards for at-risk facts with the trigger, the
affected fact reference, and a description. A control to re-run the decay job.

### 5.12 Decision Analytics
KPI cards for the learning flywheel — recurrence rate, work orders originating from Prahari,
correction-to-improvement rate — each with actual vs target and an explicit note that targets
are estimates pending validation.

### 5.13 Audit & Provenance / Admin & Ingestion
**Audit:** an append-only table (When / Actor / Action / Target) with a filter, and no
mutation affordances.
**Admin:** document upload with a provenance guarantee, an ingested-document table (Document,
Status, Nodes, Edges, Spans), and a **quarantine** section listing documents whose facts were
never promoted, with reasons.

---

## 6. Component vocabulary to design

- **Confidence indicator** — a 5-segment bar plus a text label; never colour-only.
- **Citation chip** — a compact `[n]` that reveals the source excerpt inline.
- **Answer / hypothesis card** — claims, citations, confidence, reproducibility metadata.
- **Abstain card** — the refusal, as a positive state.
- **Correction composer** — "This is wrong" → *Teach Prahari*.
- **Traversal canvas** — the causal chain; currently a single vertical spine with typed,
  colour-coded nodes (Asset, FailureMode, Inspection, Incident, Sensor, Identifier) and named
  edges. **This is the biggest visual opportunity in the product** — reimagine it.
- **Merge diagram** — many identifiers → one canonical asset.
- **Stage indicator** — the named pipeline, never a spinner.
- **Degradation banner** — persistent, non-dismissible, plain-language.
- **Status badge, metric tile, panel, skeleton, empty state.**

---

## 7. Current design language

The existing system is documented and coherent. **You may evolve or replace it — but you must
justify any departure**, and the accessibility and colour-redundancy rules must survive.

- **Canvas:** graphite-black `#0B0D0F` (deliberately not blue-black, not neutral grey).
- **Depth:** a five-step surface ladder (`#08090A` inset → `#131619` → `#1A1E22` → `#22262B`
  → `#2A2F35`) with hairline borders. **No drop shadows anywhere.** Focus and live-selection
  are marked by a soft cyan **instrument glow**, never a cast shadow.
- **Signal colour:** a single restrained steel-cyan `#3FAAB8` carries all primary action and
  focus. Consequential approve/reject actions instead use a distinct `decision` blue `#5C8FC7`
  — the accent colour and the commitment colour are deliberately different.
- **Semantic colours are meanings, not decoration:** evidence `#B9A46C`, investigation
  `#7B7FC4`, knowledge `#4E9B94`, decision `#5C8FC7`, prediction `#9A8FD6`, simulation
  `#A66B9E`, twin `#2FB6C4`; success `#3FA66B`, warning `#C98A3F`, critical `#C4453A`,
  offline `#565C64`.
- **Type:** Inter-class sans, weights held strictly between **400 and 650** — never lighter,
  never bolder. Tight line-heights on display, relaxed on data-dense body. Tabular numerals on
  every metric and table cell. Uppercase tracked **index labels** mark every section boundary —
  this is the system's one consistent structural signature.
- **Shape:** 2–8px radii on UI chrome; **0px on every full-bleed data canvas**, so instruments
  read as instruments rather than cards.
- **Two whitespace registers:** *dense-operational* (16–24px rhythm) for surfaces being
  **scanned**; *relaxed-editorial* (up to 96px, 840px max column) for surfaces being **read**.
  Choose per surface, deliberately.
- **No gradients, no atmospheric lighting, no background illustration** in the operational
  product. Illustration is permitted in empty states only.

---

## 8. Responsive and environmental requirements

This product is used in places most software isn't.

| Class | Behaviour |
|---|---|
| Desktop ≥1440px | Full three-region shell, canvases at full capability, 4-up metric grid |
| Laptop 1280–1439 | Sidebar collapses to a 64px icon rail; 3-up grid |
| Tablet 1024–1279 | Sidebar becomes an overlay drawer; canvas toolbars condense |
| Field tablet 768–1023 | Single-pane task-first; 48px touch targets; persistent offline/sync indicator; canvases read-only |
| Wall display 32–55" | Glanceable; typography scales **up** (metrics 48–64px); the status strip becomes the whole screen |
| Mobile <768px | Deliberately scoped to alerts, approvals, and status checks. The analysis canvases are **not available** — do not ship a degraded version of them |

Plus three genuine environmental modes, not cosmetic themes:
- **Gloves Mode** — 56px targets, wider spacing, no hover-dependent affordances.
- **Outdoor Sunlight Mode** — higher luminance and contrast; solid fills replace low-opacity
  washes, which vanish in direct sun.
- **Night Shift Mode** — capped luminance, warmer accent, to protect night vision in a
  control room at 03:00.

Accessibility is an operational requirement, not a compliance checkbox: full keyboard reach,
ARIA live regions for critical alerts, a "view as table" fallback for every visualisation,
colour-blind-safe redundancy on every semantic pairing, and a documented high-contrast token
set that preserves hue identity.

---

## 9. What I want from the redesign

Keep the rigour. Raise the craft. Specifically:

1. **Make the Decision Investigation screen feel like an instrument**, not a form with results
   under it. The streaming traversal is the product's best moment and is currently
   under-designed — a plain vertical spine of circles. Reimagine how a multi-hop causal chain
   across documents is drawn, and how a citation opens without losing the reader's place.
2. **Elevate the Living Asset Map.** It is the moat and it currently looks like a settings
   list. The four-names-become-one-pump moment should be immediately legible and satisfying.
3. **Restructure Organizational Memory.** Fifteen top-level tabs is a navigation failure.
   Find the information architecture that lets a 34-year veteran deposit knowledge without
   feeling like he's filling in forms — and make the *recognition* of his contribution feel
   genuinely earned rather than gamified.
4. **Design the refusal properly.** The abstention card should be the most quietly confident
   thing in the interface.
5. **Give the five role dashboards genuinely distinct characters** while keeping them
   recognisably one system.
6. **Sharpen the trust surfaces** — confidence, citation, provenance, degradation, coverage
   disclaimers. These are the product's differentiators and should feel designed, not bolted
   on for compliance.
7. **Resist decoration.** Every added element must answer an operational question. No vanity
   visualisations, no widgets filling slots.

---

## 10. Deliverables

1. **Design direction** — a short written rationale: the concept, and what you changed from
   the current system and why.
2. **Full token set** — colour, typography, spacing, radius, elevation, motion, in a
   structured format, with semantic names tied to meaning rather than appearance.
3. **Component specifications** for §6, including all states (default, hover, active,
   focus, disabled, loading, empty, error) and the accessibility notes for each.
4. **High-fidelity screen designs** for all thirteen surfaces in §5, at desktop, plus
   field-tablet and mobile treatments for Field Mode, Execution Center, and Home.
5. **The three hero moments** designed in detail, including their motion and streaming
   behaviour: resolution, investigation traversal, and the refusal.
6. **A responsive and environmental-modes specification** covering §8.

Reference tokens rather than raw values throughout. If you propose a new colour, define the
**operational meaning** it represents before you assign it a hex value.

---

## 11. Hard don'ts

- No chat bubbles, avatars, or assistant persona on the investigation surface.
- No "AI magic" visual language — sparkles, purple gradients, glowing orbs, animated
  constellations.
- No drop shadows.
- No type below 400 or above 650 weight.
- No rounded corners on a data canvas; no squared-off status dots, toggles, or avatars.
- No multi-hue "jet" colormap on any heatmap or risk visualisation.
- No colour-only status encoding, anywhere.
- No drag-and-drop customisable dashboard canvas.
- No generic spinners.
- No auto-dismissing critical alerts — they persist until acknowledged.
- No visual treatment that lets a *drafted* action be mistaken for a *committed* one.
- No UI that implies completeness the system cannot guarantee.
