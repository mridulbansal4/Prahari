# 11 — Demo Guide

> Story, flow, dataset, script, judge Q&A, and failure recovery. The demo is a failure-tolerant runbook, not a scenario list. Twelve minutes, three wow moments, one refusal.

## 11.1 Demo thesis (say this, not "we built an AI chatbot")

> *"We unified disconnected industrial intelligence into one continuously-learning operating layer that reasons across documents — and shows its work."* (judges' note §3, §12.)

Open with the **02:40 phone call**, not architecture (Harvey Specter rule, Vol 1). The true incumbent is a phone call to someone who might have retired.

## 11.2 Demo flow (12 minutes)

| Min | Beat | On screen |
|---|---|---|
| 0–1.5 | **The 02:40 story** | narration only; one image of a pump + three disconnected systems |
| 1.5–3 | **Problem, shown** | the same workflow diagram twice — once broken, once with SENTINEL, one node changed |
| 3–5.5 | **Primary wow: resolution** | 4 identifiers → 1 asset; human corrects one; graph updates; answer recomputes |
| 5.5–8 | **Secondary wow: investigation** | "why is P-101B running hot?" → causal chain across 5 docs, each hop cited |
| 8–9.5 | **Compliance** | ComplianceMatrix; overdue OISD obligation with evidence; the honest coverage footer |
| 9.5–10.5 | **Execute** | draft work order → approval sheet → committed to CMMS (audited) |
| 10.5–11 | **The refusal** | same question with the graph disabled → system abstains, names who to ask (CP-4/CP-9) |
| 11–12 | **Close** | the moat line + the resolution corpus compounding with use |

## 11.3 The three wow moments (declared in Vol 1, staged here)

1. **Primary — Resolution.** Four identifiers collapse into one node; a human correction is learned live. *Demonstrates the secret.*
2. **Secondary — Investigation.** Multi-hop causal chain with page-level citations. *Demonstrates reasoning, not retrieval.*
3. **Final — The Refusal.** The system deliberately declines when ungrounded. *Nobody else will demo their system refusing to answer.*

## 11.4 Demo dataset (provenance-clean)

- **Public-source only:** published standards excerpts, public incident/investigation reports, sample/synthetic P&IDs, a synthetic-but-realistic CMMS export and inspection notes. Every item carries provenance.
- **Never** fabricate a document and present it as a real plant record (Vol 3 risk table).
- The dataset is seeded to *guarantee* the 4→1 resolution and the 5-hop investigation both land.

## 11.5 Narration script (condensed, speak-aloud)

> "At 2:40 a.m., a pump trips. The night technician has three systems that each know part of the story and none that connect them. The one person who could connect them retired in 2023. **This** is the real incumbent — a phone call. Watch what happens when the connections are a living graph instead of a memory…"
>
> *(resolution)* "P-101B, Boiler Feed Pump B, this OEM number, and 'the noisy one' — four names, one pump. SENTINEL proposes the merge, our engineer confirms it, and the graph learns. That confirmation is the thing a competitor can never copy."
>
> *(investigation)* "Now the question: why is it running hot? Watch the traversal — vibration alarm, upstream strainer, a 2019 inspection note nobody had read, a feedstock change at 21:00. Five documents, never linked by a human, each hop citing a page."
>
> *(refusal)* "And now, the most important slide in this pitch. I disable the graph and ask again. It doesn't guess. It tells me what it can't ground, and who to ask. In a plant, a wrong answer is worse than no answer."

## 11.6 Expected judge questions → answers

| Q | A |
|---|---|
| "How do you prevent hallucination?" | "Hallucination is the risk we solved with citations and a verifier. The risk that keeps us up is **entity resolution** — a wrongly-merged node gives a perfectly-cited answer about the *wrong* pump. We adjudicate merges with humans and make them reversible and versioned." |
| "Isn't this just RAG?" | "RAG retrieves similar text. We retrieve *connected facts* across documents no human linked, and we show the path. Vector-only can't do the multi-hop." |
| "What's the moat? GraphRAG is copyable." | "The moat isn't GraphRAG or the ontology — those are copyable. It's the plant-specific human-validated resolution corpus, which grows every time the tool is merely *used*." |
| "How do you handle our data leaving the plant?" | "Air-gap mode: local model, local embeddings, no answer-path egress. The fallback and the air-gap are the same design." |
| "How is compliance not a liability?" | "It's a rule engine producing evidence + gaps attributed to a clause, never a legal opinion, and it reports which clauses are encoded vs not. We never imply completeness." |
| "Can you build this for real?" | "The substrate is standards-aligned (ISO 14224, DEXPI), the stack is OSS, and the roadmap in Vol 17 sizes it for a 4-person team." |

## 11.7 Failure recovery (the runbook)

| Failure | Recovery |
|---|---|
| Network dies mid-demo | switch to `--profile local-model`; the degradation is *itself* the CP-9 story — narrate it |
| Model/API latency spike | pre-warmed semantic cache serves the scripted questions instantly |
| Live query returns weird result | the seeded dataset makes scripted queries deterministic; do not free-type |
| Projector/display fails | backup recording of the exact flow on a second device |
| Everything fails | offline recorded demo + slide deck; the story still lands |

## 11.8 Backup / offline demo

A pre-recorded, narrated run of the exact flow, plus the semantic cache pre-seeded so the live app answers scripted questions with zero external dependency. The demo must be runnable with the network cable pulled.

---

**Red Devil:** *Jobs:* "Open with the phone call, close with the refusal. The refusal is the bravest thing here — keep it. **APPROVED.**"
**Hackathon Winning:** *ET Judge:* "Twenty teams show what they built; you show what you refuse to answer. That is finalist behaviour. **Strong Winner.**"
**Black Swan:** the offline path means a network failure *becomes* a feature demo. **Survivable.**
**Green:** the narration teaches the judges the retention thesis. **Positive.**
