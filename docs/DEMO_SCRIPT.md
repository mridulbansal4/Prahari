# Prahari — Demo Video Script (3:30)

**Problem Statement 8 — AI for Industrial Knowledge Intelligence: Unified Asset & Operations Brain**
Format modelled on the Gaatha sample: one continuous screen-capture, mouse-led, spoken in one breath per beat.

---

## Part A — Reading the room: what an ET judge wants (my analysis before writing a word)

ET is a *business* publication. Their judges score five things — Innovation 25, Business Impact 25, Technical Excellence 20, Scalability 15, UX 15 — but PS8 also names a very specific **Evaluation Focus**, and that focus is what separates a winner from a chatbot demo. Read literally, PS8 asks the judge to check seven things:

1. **Entity extraction accuracy *across document types*** → so the demo must visibly handle a drawing, a datasheet, a spreadsheet and a procedure — not one clean corpus.
2. **Query answer quality on domain-expert benchmark questions** → the answer must sound like a reliability engineer wrote it, with real tag numbers.
3. **Knowledge-graph linkage completeness** → show the graph, and show an edge that came from a *drawing*, not typed by a human.
4. **Time-to-answer vs traditional search** → name the alternative out loud: a phone call, or Ctrl-F across 12 systems.
5. **Compliance gap detection accuracy** → surface an *overdue* statutory clause with the evidence trail.
6. **Cross-functional knowledge discovery** → the money shot: one answer that stitches a datasheet + a work order + an incident + a shift note that no single person had open.
7. **"ideally validated with real industrial document samples"** → the judge is quietly skeptical this runs on real data. **Prove it.**

That last line is why this cut opens differently from Gaatha. Before I ask the system anything, I **open a real document and let the judge read it** — the actual OEM pump datasheet, and the extracted passages behind it — using the document reader. It says, in ten seconds: *this is not toy data, and you can see exactly what the machine read.* Everything after that is trusted more.

The through-line I want the judge feeling: **35% of an engineer's week is spent searching; a quarter of these engineers retire this decade and the knowledge leaves with them. Prahari turns the plant's documents into one brain that answers in seconds, cites every word, refuses when it isn't sure, and remembers why decisions were made.** Trust is the product. So the demo spends its most expensive seconds on citations, the refusal, and the audit trail — the things a *safety-critical* buyer needs before Innovation even matters.

**Coverage map — every beat below is doing a job:** ① frames Business Impact. ② proves *real, multi-format* data + the new document reader (Evaluation Focus 1 & 7, UX). ③–④ query quality + time-to-answer + compliance + citations (Focus 2, 4, 5). ⑤ the refusal (Innovation, safety). ⑥ KG + P&ID→graph via vision (Focus 3, Technical Excellence). ⑦ entity-resolution moat (Innovation). ⑧ contradiction + overdue alerts (Focus 5, Innovation). ⑨ the retirement cliff — captured expertise used in a live answer (Business Impact). ⑩ decision memory + replay (Focus 6, RCA). ⑪ scale, air-gap, close (Scalability). Nothing is on screen that a judge isn't scoring.

*(One asset carries the whole story so the judge never re-orients: **P-101B**, a boiler-feed-water pump. Every document, alert and decision is about it.)*

---

## Part B — The script

> Timings are cumulative to **3:30**. 🎙 = narration. Stage cues in **bold**. Keep the cursor moving; never click faster than the UI settles.

### 1. (0:00–0:24) · 24s — Open on **Ask** (the workspace home). Mouse drifts across the sidebar, then the answer canvas. 🎙

"We're Team Prahari — the word means *sentinel*, the one who keeps watch. In an industrial plant, the answer to almost any question already exists — in a datasheet, a P&ID, a decade of work orders, a retiring engineer's head. It just lives in a dozen systems that don't talk. An engineer burns a third of the week hunting for it, and a quarter of them retire this decade. Prahari turns every one of those documents into a single brain you can ask."

### 2. (0:24–0:46) · 22s — **CLICK Documents** in the sidebar. ⏳ let the list settle. **CLICK "View content"** on `datasheet_P-101B_boiler_feed_pump.md`. The reader modal opens over the page. 👉 point at the rendered tables, then **CLICK the "Extracted passages" tab.** 🎙

"But first — is this real? These are actual plant documents: engineering datasheets, P&IDs, maintenance logs, safety procedures. Open one — the OEM pump datasheet, rendered clean, ratings and tables intact, right here in a box over the page, no waiting for a new tab. And this tab shows the exact passages the system pulled out — the citable units it reasons over. Nothing is hidden, nothing is invented." **CLOSE with the ✕.**

### 3. (0:46–1:12) · 26s — Back on **Ask**. **CLICK the question** "Why is P-101B tripping on high bearing temperature?" ⏳ ~1s as the answer streams, the graph draws on the right. 🎙

"Now ask it the way an engineer actually would. *Why is P-101B tripping on high bearing temperature?* Watch the right — it isn't searching text, it's walking the plant's knowledge graph: pump, to bearing, to the work orders, to the seal incident. The alternative to this is a phone call to someone who might be on leave, or Ctrl-F across twelve systems. This took four seconds — and every sentence it's about to show carries a source."

### 4. (1:12–1:28) · 16s — 👉 point down the **cited claims**; hover a citation chip; then 👉 the "also flagged" line. 🎙

"Here's the answer, and every claim is footnoted — the datasheet's temperature limit, the 2023 seal failure, last month's condition-monitoring trend. Hover any one and you see the exact document and page. And unprompted, it flags something adjacent: the OISD inspection on this pump is **overdue** — with the evidence trail to prove it."

### 5. (1:28–1:44) · 16s — **CLICK the question** "Can we run P-101B in cold standby over the weekend?" ⏳ ~1s. 👉 point at the abstention banner. 🎙

"This next part is what makes it safe to deploy. Ask something the documents don't actually answer — *can we run it cold over the weekend?* A chatbot would guess. Prahari **refuses** — it tells you it can't ground that, names what's missing, and points you to the two people who'd know. In a plant, a confident wrong answer is the dangerous one. It would rather say *I don't know.*"

### 6. (1:44–2:04) · 20s — **CLICK Knowledge map.** ⏳ let it draw. 👉 trace a couple of hops, then 👉 point at an edge labelled from the P&ID. 🎙

"Every answer stands on this — the knowledge graph. Assets, instruments, procedures, incidents, people, all linked. And this edge here wasn't typed by anyone: a vision model **read the P&ID drawing** and extracted that the feed line ties into this header. That's the hard part of this problem — turning a scanned engineering drawing into a connection you can query — and it's live."

### 7. (2:04–2:22) · 18s — **CLICK Asset map.** 👉 point at the four source tags collapsing into one canonical asset. 🎙

"And underneath, the quiet moat. The same pump is `P-101B` in the maintenance system, `PU-101-B` in the DCS, an equipment number in SAP, a tag on the drawing. Four names, one machine. Prahari resolves them into a single identity — with the match score and evidence shown, never a silent guess. Without this, every answer above would be stitching the wrong pump."

### 8. (2:22–2:42) · 20s — **CLICK Alerts.** 👉 point at the overdue-compliance card, then the **contradiction** card. 🎙

"This is the graph working for you while you sleep. Top card — that overdue OISD inspection, surfaced against the statutory clause and its interval. Below it, something only a connected brain can catch: two documents that **disagree** — the datasheet's bearing-temperature limit versus what a shift note recorded as normal. It doesn't pick a side; it raises the contradiction for a human. That's compliance-gap detection and knowledge-conflict detection, automatically."

### 9. (2:42–3:02) · 20s — **CLICK Expert knowledge.** 👉 point at an expert flagged as retirement-risk, then at "used in 3 answers." 🎙

"Remember the retirement cliff. Here's Prahari's answer to it. This is a 34-year reliability engineer, flagged because his knowledge is about to walk out the door. Capture what he knows once — *this seal always weeps before it fails* — and it becomes a citable span. See this? *Used in three answers.* His judgement is already grounding decisions he isn't in the room for. That's institutional memory that no longer retires."

### 10. (3:02–3:20) · 18s — **CLICK Decisions & replay.** **CLICK the top decision** to expand. 👉 point at the rejected options and the reasoning. 🎙

"And it remembers the *why*. Every significant call is written down as a decision — what was chosen, and just as important, what was considered and rejected, and on what evidence. So when this pump acts up again in two years, the next engineer doesn't re-run the whole investigation — they replay this one. Root-cause analysis that compounds instead of repeating."

### 11. (3:20–3:30) · 10s — **CLICK Coverage / trust**, hold on screen. 🎙 (slow, land it)

"Real documents, cited answers, honest refusals, an audit of every decision — and it runs air-gapped, inside the plant, because this data never leaves the fence. From twelve systems and a retiring workforce, to one brain that keeps watch. This is Prahari. Thank you." ⏹ **STOP at 3:30.**

---

## Part C — Cheat sheet for the record

**Numbers to have on screen (all traceable to the corpus / PS8):**
- "third of the week searching" → McKinsey 35% (PS8 context).
- "a quarter retire this decade" → PS8 knowledge-cliff stat.
- "twelve systems" → PS8's 7–12 disconnected systems.
- Asset: **P-101B** boiler-feed-water pump throughout.
- Overdue clause: **OISD** inspection on P-101B (`compliance_OISD_P-101B.md`).
- Contradiction: datasheet limit (`datasheet_P-101B_boiler_feed_pump.md`) vs `shift_handover_notes.md`.
- Incident cited: `incident_report_2023_P-101B_seal_failure.md`.
- P&ID→graph edge: `PID_BFW_system_P-101B.md` + `drawings/`.

**If you must trim to 3:00:** drop beat ⑩ (Decisions) and fold its one line into ⑪. Never cut ②, ④, ⑤, or ⑧ — those are the four Evaluation-Focus proofs a judge is explicitly told to look for.

**Recording notes:** hard-reload once before you start (Ctrl+Shift+R) so nothing is half-cached; run at 1280-wide so the sidebar and answer canvas both breathe; pause a full second after every click before speaking — dead air reads as confidence, rushing reads as a bug.
