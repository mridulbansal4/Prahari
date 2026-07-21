# Prahari frontend — current state & revamp brief

> Self-contained. Hand this whole document to an AI coding agent to revamp the UI.
> It describes exactly what exists today, how it works, and what must not break.

---

## 0. How to use this document

You are revamping the front end of a **working** application. The backend, the AI/retrieval
logic, and every API contract are **fixed and must not change**. Sections 1–7 describe what
exists. Section 8 lists the hard rules. Section 9 lists the known weaknesses — that is where
the actual work is. Section 10 tells you how to run and verify it.

If a change you want to make would require touching the backend, **stop and flag it** instead
of doing it.

---

## 1. What the product is

**Prahari — an Industrial Knowledge Intelligence platform.**

It ingests heterogeneous plant documents (engineering drawings and P&IDs, maintenance records,
safety procedures, inspection reports, operating instructions, spreadsheets) and lets anyone
ask questions across all of them in plain English. Answers come back **with citations**, plus
proactive alerts the system surfaced on its own (compliance gaps, contradictions between
documents, overdue inspections), plus a knowledge graph showing how everything connects.

The founding scenario: at **02:40** a pump trips. The night technician has three systems that
each know part of the story and none that connect them. The person who could connect them
retired in 2023. The real incumbent is *a phone call to someone who may no longer work there*.

### What it must never become
- **Not a chatbot.** No message bubbles, no avatars, no assistant persona, no "typing…"
  metaphor. Output is a documented analysis, in the same card language as human-authored work.
- **Not a document search engine.** It does not return a ranked list of PDFs.
- **Not a generic BI dashboard.** No drag-and-drop widget canvas.
- **Not a consumer AI product.** No sparkle icons, no purple "AI magic" gradients.

---

## 2. Architecture

```
codebase/
  backend/     FastAPI modular monolith — DO NOT TOUCH
  frontend/    React 18 + TypeScript + Vite  ← the revamp target
  eval/        golden-set harness
```

- **Frontend stack:** React 18.3, TypeScript 5.5, Vite 5. **No UI framework, no CSS framework,
  no component library.** Styling is hand-written CSS with custom properties, plus inline
  styles that reference those properties. No Tailwind, no styled-components, no MUI.
- **No router.** `react-router-dom` is still in `package.json` but is **unused** — the entire
  app is one page with anchor-scroll navigation. Safe to remove.
- **State:** local React state only. No Redux, Zustand, or React Query.
- **Backend:** runs at `localhost:8000`. Vite proxies `/v1` to it (including WebSocket
  upgrade), configured in `vite.config.ts`.

### Current file tree (~2,700 lines of active source)

```
src/
  main.tsx                    26   entry: bootstraps session, mounts App, registers SW
  App.tsx                     47   the single page — composes all sections in order
  design/
    tokens.css               129   THE ONLY PLACE RAW VALUES LIVE
    global.css               420   reset, base, type utilities, .btn/.card/.input/.chip, grids
  lib/
    api.ts                   156   REST client — every endpoint, bearer token (UNCHANGED)
    types.ts                  92   DTOs mirroring backend responses (UNCHANGED)
    stream.ts                 27   WebSocket client for live investigations (UNCHANGED)
    session.ts                41   silent dev-token bootstrap — replaces the deleted auth
    useInvestigation.ts      104   the ask controller: run state, streaming, plain-language stages
    alerts.ts                 90   merges compliance + knowledge-health into one Alert[] list
  components/
    ui.tsx                   232   Section, Orb, Chip, Badge, Confidence, EmptyState, Notice, …
    AnswerCard.tsx           195   AnswerCard + AbstainCard + citation peek
    GraphCanvas.tsx          233   knowledge map, node glyphs, legend, linear trace
  sections/
    TopNav.tsx               128   sticky nav, scroll-spy, mobile drawer
    Hero.tsx                  80   headline + embedded primary ask box + orbs
    HowItWorks.tsx            56   1-2-3 onboarding strip
    AskSection.tsx           203   the core Q&A surface
    DocumentsSection.tsx     235   drag-drop upload + grouped document library
    AlertsSection.tsx        131   proactive insight cards + coverage disclaimer
    KnowledgeMapSection.tsx   59   graph + legend + text equivalent
    Footer.tsx                39   minimal
  legacy/                          EXCLUDED FROM BUILD — the old multi-page UI, kept for reference
```

---

## 3. What was recently done (the state you are inheriting)

The app used to be a **13-screen, role-gated, dark "control room" console** with a login
screen and six personas. It was collapsed into the current single light page. Specifically:

1. **Auth was removed entirely.** `lib/auth.tsx` and `pages/Login.tsx` deleted. No login,
   no signup, no route guards, no profile/avatar UI, no sign-out. The page loads straight
   into the product.
2. **All routing was removed.** Thirteen routes became one scrollable page with four anchored
   sections. URL stays at `/`.
3. **The design system was swapped** from a dark industrial palette to a light editorial one
   (see §5).
4. **The copy was rewritten for non-technical readers.** Every section has a plain-language
   title plus a one-line helper. "RAG Copilot" → "Ask about your documents". Internal agent
   stage names → "Reading your documents…".
5. **Nine superseded page components moved to `src/legacy/`**, excluded from the build.

### Important: auth is only gone from the *client*

The backend **still requires a bearer token on every `/v1` call.** `lib/session.ts` silently
logs in as the `deepak` admin persona on boot and caches the token in `localStorage` under
`prahari.token`. The user never sees this.

Admin is used because it is the **only** role whose RBAC row covers every module the page
touches — ingestion (`M11`) is admin-only. Do not change this principal without checking
`backend/app/auth/rbac.py`.

`ensureSession()` also **verifies the cached token belongs to the expected principal**, not
merely that it is valid. This matters: a leftover token from the old login screen
authenticates fine but lacks module access, which silently 403s parts of the page with no way
for a user to recover now that the sign-in UI is gone. Keep that check.

---

## 4. Data flow and API contracts — DO NOT CHANGE

Every endpoint below already exists and works. Preserve the call signatures and shapes.

| What | Call |
|---|---|
| Silent login | `POST /v1/auth/login` `{username}` → `{token, name, role, tenant}` |
| Whoami | `GET /v1/auth/me` → `{subject, name, role, tenant, site, modules[]}` |
| Ask a question | `POST /v1/investigations` `{question, as_of?, context?}` → `{investigation_id}` |
| Fetch a result | `GET /v1/investigations/{id}` → `InvestigationResult` |
| Recent questions | `GET /v1/investigations` → `{items[{investigation_id, question, abstained}]}` |
| **Live stream** | `WS /v1/stream/investigations/{id}?token=…` |
| Asset register | `GET /v1/assets` → `{assets[{id, tag, name, iso_class}]}` |
| Compliance (per asset) | `GET /v1/compliance/assets/{assetId}` → `{rows[], coverage}` |
| Knowledge risk | `GET /v1/knowledge/health` → `{flags[], last_run}` |
| Document library | `GET /v1/ingestion` → `{jobs[], quarantined[]}` |
| Upload | `POST /v1/documents` (multipart `file`) → `{doc_id, job_id, status}` |

### The streaming contract (the most important interaction)

`POST /v1/investigations` returns an id; open the WebSocket and reduce these event types:

| Event | Meaning |
|---|---|
| `stage` | `{stage, detail}` — pipeline moved on. Stages: `planner`, `retriever`, `executor`, `critic`, `verifier` |
| `graph_hop` | `{hop: GraphHop}` — one more node in the traversal; append and draw it |
| `token` | `{text}` — a fragment of the answer; concatenate |
| `abstain` | `{result}` — terminal, the system refused |
| `done` | `{result}` — terminal, answer complete |
| `error` | terminal failure |
| `banner` | degradation-rung change (currently **ignored** by the page) |

The socket can close without a terminal frame. `useInvestigation.ts` recovers by re-fetching
over REST rather than leaving the user on a spinner. **Keep that fallback.**

### Key types (`lib/types.ts`)

```ts
InvestigationResult {
  investigation_id, question, as_of, abstained,
  answer: string,
  claims: Claim[],           // each: { text, confidence, citations[] }
  graph_path: GraphHop[],    // each: { node, node_label, edge, detail }
  unresolved: string[],      // what it could not ground
  who_to_ask: WhoToAsk[],    // { person, expertise, tenure_years }
  degradation_level, prompt_manifest_hash, model_id, context_span_ids
}
Citation { doc_id, page, span_id, excerpt }
ConfidenceState = "grounded" | "inferred" | "unsupported" | "abstained"
```

Graph node labels seen in real data: `Asset`, `FailureMode`, `Inspection`, `Incident`,
`Sensor`, `Identifier`, `WorkOrder`.

### Seeded demo data (what you will actually see)

Three assets: `P-101B` (Boiler Feed Pump B), `S-14` (Suction Strainer 14), `V-201` (Knockout
Drum). The canonical demo question **"why is P-101B running hot?"** returns a grounded answer
with four cited claims and an 11-node traversal. `"why is P-101B running COLD ??"` abstains.
Alerts currently include one overdue OISD inspection on P-101B and two knowledge-risk flags.

---

## 5. The design system currently applied

Editorial, calm, print-magazine — adapted from an ElevenLabs-style spec. Full token set lives
in `src/design/tokens.css`. **Never inline a raw hex or px where a token exists.**

### Colour
| Role | Value |
|---|---|
| Page canvas | `#f5f5f5` · alt band `#fafafa` · card `#ffffff` |
| Ink / display text | `#0c0a09` · body `#4e4e4e` · muted `#777169` · muted-soft `#a8a29e` |
| Primary CTA | `#292524`, active `#0c0a09`, white text — **the only CTA colour** |
| Hairlines | `#e7e5e4` · strong `#d6d3d1` · surface-strong `#f0efed` |
| Semantic | success `#16a34a`, error `#dc2626` — used sparingly |
| Gradient orbs | mint `#a7e5d3`, peach `#f4c5a8`, lavender `#c8b8e0`, sky `#a8c8e8`, rose `#e8b8c4` |

**Orbs are atmosphere only** — soft radial blooms (`blur(56px)`, ~55% opacity) behind copy.
Never button fills, text colours, or card backgrounds. Two currently sit behind the hero.

### Typography
- **Display:** EB Garamond at **weight 300** — never bold. Hero 64px/-1.92px tracking
  (32px on mobile), section heads 36px, sub-heads 32px, card group titles 24px.
- **Body/UI:** Inter 400/500 with slightly loose tracking (+0.15–0.18px).
- Card titles 20px/500, body 16px/400, captions 14px, section labels 12px/600 uppercase
  +0.96px tracking.
- Google Fonts is loaded from `index.html`. **Note:** EB Garamond's lightest hosted weight is
  400, so display declares 300 and renders at 400. Cormorant Garamond is the true-300 swap.

### Shape, spacing, elevation
- Radii: CTAs and badges **pill** (`9999px`); cards 16px; orb cards 24px; inputs 8px.
- Spacing on a 4px base: 4/8/12/16/20/24/32/48, **96px section rhythm** (64px mobile).
- Elevation: 1px hairline borders, **flat by default**, one soft tier `0 4px 16px rgba(0,0,0,.04)`
  on hover only. **No heavy shadows anywhere.**
- Container max-width 1200px, centred.

### Components (in `global.css` as classes)
`.btn--primary` (ink pill, 40px min-height) · `.btn--outline` (transparent, 1px border) ·
`.btn--text` (inline link) · `.input` (white, 8px radius, 44px, border thickens to 2px ink on
focus) · `.card` / `.card--hover` · `.badge` (pill) · `.chip` (clickable pill, 40px) ·
`.orb` · `.skeleton` · `.progress` (sliding bar — **never a spinner**).

### Responsive
| Width | Behaviour |
|---|---|
| ≥1024px | 3-up card grids; answer + map side by side (`1fr 560px`); full 64px hero |
| 640–1023px | 2-up grids; hero 48px |
| <768px | Nav collapses to hamburger drawer with the same anchor links |
| <640px | 1-up stacks; hero 32px; 64px section rhythm |
| <480px | Nav CTA hides |

Verified: no horizontal scroll at 375px. Touch targets ≥40px.

### Accessibility already in place
Visible ink focus ring on everything. Full keyboard reach. `prefers-reduced-motion` kills orb
drift, shimmer, and smooth scroll. **Confidence is never colour-only** — always a text label
beside the segments. **Graph node kind is carried by SHAPE, not colour**, so the map reads in
greyscale and under any colour blindness. Icon-only buttons carry `aria-label`; the graph SVG
carries `role="img"` + label; the nav uses `aria-expanded`.

---

## 6. The page, section by section

Order is deliberate — it mirrors the mental model: **understand → ask → feed it documents →
see what it caught → see how it connects.**

### Top nav (`TopNav.tsx`) — sticky, 64px
Wordmark left. Anchor links right: `Ask` · `Documents` · `Alerts` · `Knowledge map`. One ink
pill CTA "Ask a question" scrolling to `#ask`. **No sign-in, no profile, no avatar.** An
IntersectionObserver scroll-spy underlines the active section. Below 768px the links become a
hamburger drawer. Background is translucent with `backdrop-filter: blur(12px)`.

### Hero (`Hero.tsx`)
Headline **"Every plant document, finally connected."** One-line subhead. **The primary ask
box is embedded here** — a 52px input plus an Ask button — so the main action is the first
thing a visitor sees. Submitting runs the query *and* smooth-scrolls to `#ask`. Two gradient
orbs (mint, peach) behind the headline. Footnote: "No sign-in. Nothing leaves your plant."

### How it works (`HowItWorks.tsx`) — soft band
Three numbered cards, one line each: (1) Add your documents, (2) Ask a question in plain
English, (3) See the answer, and what it caught.

### Ask (`AskSection.tsx`) — `#ask` — **the core surface**
- Large input + Ask button. **Example chips** below it, always visible, that auto-fill and run:
  *"Pump P-101B is vibrating — what should I check before servicing it?"* etc. Recent real
  questions are mixed in; probe/eval strings (`ignore previous`, `password`, `fatigue life`)
  are filtered out of suggestions.
- **Empty state:** "Your answer will appear here" + explanation. Never a blank box.
- **Running:** a sliding progress bar with a **plain-language stage** — `planner` renders as
  "Working out where to look…", `retriever` as "Reading your documents…", `verifier` as
  "Verifying every statement has a source…". Streamed answer text appears as it arrives.
- **Answer:** `AnswerCard` — a badge, the plain answer at 17px, then "What this is based on"
  with one row per claim. Each row: claim text, inline numbered **citation chips**, and a
  confidence readout. Clicking a chip opens an inline peek showing `doc_id · page` and the
  excerpt. Confidence renders in plain language: *"Backed by your documents"* / *"Reasoned,
  partly inferred"* / *"Not supported by a source"* / *"Not answered"*.
- **Refusal:** `AbstainCard` — deliberately calm and confident, **never red, never an error**.
  "I won't guess on this one." Lists what it couldn't find, then **who to ask** (person,
  expertise, tenure) as avatar rows.
- **Inline flags:** if the answer's traversal touched an asset with an open alert, an
  "Also flagged on this equipment" card appears beneath the answer, linking to `#alerts`.
- Right column (≥1024px) is the live `GraphCanvas`, filling in hop by hop.

### Documents (`DocumentsSection.tsx`) — `#documents` — soft band
- **Drag-and-drop zone** (border and background change while dragging) plus a "Choose files"
  button. Accepts `.csv,.txt,.md,.pdf,.json,.xlsx,.tsv`. Multi-file upload is sequential.
- **Library grouped by plain-language type**, inferred from filename regex: Drawings &
  diagrams · Maintenance records · Safety & procedures · Inspection reports · Spreadsheets &
  data · Other. Each card: filename, a "Read" badge, and "N things identified · N passages
  kept as evidence".
- **Empty state** explains what to drop and offers a CTA. A **failed load shows a real error**
  rather than falsely claiming the library is empty.
- **Quarantine block** (red border) lists documents that couldn't be read confidently, with
  reasons, and states that nothing from them is used.

### Alerts (`AlertsSection.tsx`) — `#alerts` — **the differentiator**
Cards for what the system found unprompted, merged in `lib/alerts.ts` from two existing
sources — compliance rows (overdue/due) and knowledge-health flags. Sorted overdue → knowledge
→ due. Each card: title, badge (Overdue / Coming due / At risk), plain-English detail, what it
involves, and an expandable **View details** revealing the equipment, the most recent
supporting document, and a link to ask about it.

**A permanent, non-collapsible coverage footer** states the disclaimer and per-instrument
encoded-rule counts (e.g. "OISD: 1 of 42 rules checked"). The product must never imply it has
checked more than it encodes. **Do not make this collapsible or remove it.**

### Knowledge map (`KnowledgeMapSection.tsx`) — `#graph` — soft band
Explainer: "How your equipment, drawings, procedures and records connect." A **legend**
mapping each node glyph to a plain-language name (Equipment, Failure mode, Inspection,
Incident, Sensor, Other name for it, Work order). Then the `GraphCanvas` — currently a
**single vertical spine**, 78px per row, with edge names in lowercase beside the connecting
line — alongside "The same path, in words", a linear text equivalent. Empty state prompts the
user to ask a question first, because the map is drawn from the last answer's traversal.

### Footer (`Footer.tsx`)
Minimal and calm. Wordmark, one line, the same four anchor links. No auth links.

---

## 7. How to run and verify

```bash
# Backend (embedded profile, no external services, DB already seeded)
cd codebase/backend
./.venv/Scripts/python.exe -m uvicorn app.main:app --port 8000
#   health:  http://localhost:8000/v1/health
#   docs:    http://localhost:8000/docs

# Frontend
cd codebase/frontend
npm run dev          # http://localhost:5173
npm run build        # tsc -b && vite build — currently passes clean
npx tsc --noEmit     # currently passes clean
```

**Service-worker gotcha:** `public/sw.js` caches the app shell **cache-first**. After changing
`index.html` or the shell you may be served the stale UI. Bump the `SHELL`/`API` cache constants
(currently `v3`), or in DevTools unregister the worker and clear caches, then hard-reload.

**Verification path that exercises everything:** load `/`, type *"why is P-101B running hot?"*
in the hero box, submit. You should get a grounded answer with four cited claims, an
"Also flagged on this equipment" card, and an 11-node knowledge map.

---

## 8. Hard rules — a revamp that breaks these has failed

**Product**
1. **Every claim carries a citation.** An uncited AI statement is a defect. Citations resolve
   to `document · page · span` and must be inspectable inline without losing your place.
2. **Confidence is always visible**, structurally, and **never colour-only**.
3. **Abstention is a success state.** Style the refusal as calm and confident — never red,
   never an error, never apologetic. It must name who to ask.
4. **Never imply completeness.** The coverage footer stays, permanently and non-collapsibly.
5. **No jargon in primary labels.** Say "Ask about your documents", not "RAG Copilot"; every
   section keeps its one-line helper.
6. **Every interactive area keeps a helpful empty state** with example prompts or a CTA.
7. **Never a generic spinner** — determinate bar, named stage, or skeleton.
8. **Quarantined documents stay visibly excluded** from answers.

**Structure**
9. **One page. No routing.** URL stays `/`. Navigation is smooth anchor-scroll.
10. **No auth, no gate, no "continue as guest".** Keep the silent session bootstrap *and* its
    principal check.

**Design**
11. Ink pill is the **only** CTA colour — no saturated brand/action colour.
12. Display type stays at weight 300 — never bold the serif.
13. Gradient orbs are atmosphere only — never fills, text, or card backgrounds.
14. No drop shadows beyond the single soft hover tier. No sharp 0px corners on CTAs.
15. Body Inter never drops below 400.
16. Reference tokens; never inline a raw hex or px where a token exists.

**Engineering**
17. **Do not touch the backend or any API shape.** Flag anything that would need a server change.
18. Keep the knowledge-graph component and its data source — restyle only.
19. Keep the WebSocket-close REST fallback in `useInvestigation.ts`.
20. `tsc --noEmit` and `npm run build` must stay clean.

---

## 9. Known weaknesses — this is where the real work is

Honest assessment of what is weak right now. A good revamp attacks these.

1. **The knowledge map is under-designed.** It is a plain vertical spine of glyphs — a list
   pretending to be a graph. It is also **not interactive**: no pan, zoom, hover, click-to-
   inspect, or filtering, despite the section being called an "interactive knowledge graph".
   The real relationships are a network, not a line. **This is the biggest single opportunity.**
2. **The map only ever shows the last answer's traversal.** There is no way to browse the
   whole knowledge graph. Users may reasonably expect a plant-wide map, and the empty state
   currently has to apologise for this.
3. **Document type grouping is filename-regex guesswork.** A file called `notes.pdf` lands in
   "Other documents" regardless of content. The backend does detect a `doc_type` in its
   ingestion `stage_log` — using that would be more honest, and needs no server change.
4. **Alerts are shallow.** Contradictions between documents are promised in the section copy
   but only compliance gaps and knowledge-risk flags are actually wired. "View details" reveals
   little. There is no dismiss, snooze, assign, or triage.
5. **No answer history.** Each new question destroys the previous answer. There is no way to
   compare, revisit, or share a result, and no permalink.
6. **Upload feedback is coarse.** Multi-file upload is sequential with a single "Adding…"
   state — no per-file progress, and no visibility into the ingestion pipeline that the
   backend actually exposes stage by stage.
7. **Real product capabilities are unreachable in the UI.** All endpoints are live and the old
   components sit in `src/legacy/`, but the page does not surface: **entity resolution / the
   Living Asset Map** (four identifiers collapsing into one asset — described in the project's
   own docs as the moat), the **work-order draft/approve flow**, **Organizational Memory**
   capture, **Decision Memory & Replay**, analytics, the audit log, **Field Mode**, and the
   **"This is wrong" correction composer**. Consider whether any of these deserve a place.
8. **Degradation is invisible.** The backend emits a `banner` event when it drops to a lower
   capability rung; the page ignores it. A user could be reading a degraded answer without
   knowing.
9. **Compliance fan-out is N+1.** `loadAlerts()` fetches every asset then one compliance call
   per asset. Fine for three assets, poor at plant scale.
10. **Sequencing is slightly off.** Alerts — explicitly the differentiator — sit fourth, below
    the fold, after Documents. Consider whether a user who hasn't uploaded anything should meet
    Documents before Alerts.
11. **Minor:** `react-router-dom` is an unused dependency; EB Garamond renders at 400 not 300;
    the hero and Ask sections contain two visually similar input boxes, which can read as
    duplication rather than as one continuing action.

---

## 10. Suggested deliverables from the revamp

1. A short written rationale — what you changed and why.
2. Any token changes, expressed in `tokens.css`, with semantic names tied to meaning.
3. The revamped page, with all states designed: default, hover, focus, loading, empty, error.
4. Specific attention to the knowledge map (§9.1–2) and the alerts surface (§9.4).
5. A summary of files added, changed, or removed, and anything you stubbed or flagged.
6. Confirmation that `npm run build` and `npx tsc --noEmit` still pass, and that the
   verification path in §7 still produces a grounded, cited answer.
