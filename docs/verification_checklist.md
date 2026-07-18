# Verification Checklist

Maps to the PRB §8.4 "Definition of satisfied" and the Bible §14 checklists. Status as built.

## Critical path (PRB §5.4) — end-to-end, verified
- [x] Ingestion pipeline: parse → extract → provenance → confidence gate → quarantine (M11)
- [x] Entity resolution: 4→1 proposal, adjudicate, reversible unmerge (M2) — verified in UI + test
- [x] Investigation: multi-hop grounded answer with per-hop citations, streamed (M1) — verified in UI
- [x] Correction: attributed graph edit, immediate re-answer context, eval label (M8) — test

## Engineering invariants (Bible §14.10) — each maps to a mechanism + a test
- [x] CP-1 provenance sink rejects unsourced fact (`test_provenance_sink_rejects_unsourced_fact`)
- [x] CP-2 citation: grounded claims cite spans (`test_investigation_grounded_with_citations`)
- [x] CP-3 gated write: distinct approver required (`test_gated_write_requires_distinct_approver`)
- [x] CP-4 abstention with who-to-ask (`test_abstention_is_a_success_state`)
- [x] CP-7 bitemporal as-of traversal (embedded store `_edge_valid_as_of`)
- [x] CP-9 degradation ladder surfaced to UI (DegradedBanner + `-graph` refusal, verified in UI)
- [x] CP-10 correction is attributed + immediate (`test_correction_is_attributed_and_immediate`)

## Eval gates (Bible §15.4) — measured, not hoped (`eval/run_eval.py`)
- [x] faithfulness 1.00 (target ≥ 0.90)
- [x] citation_accuracy 1.00 (target ≥ 0.95)
- [x] abstention_correctness 1.00 (target ≥ 0.98) — incl. injection bucket (FM-7/ADR-011)
- [x] false_answer_rate 0.00 (target ≤ 0.02)

## Design conformance (design.md via ui_rules.md)
- [x] All visual values from tokens (no raw hex/px in components)
- [x] No shadows; depth = surface ladder + focus glow
- [x] Single signal accent for action; decision-blue for approve/reject
- [x] Confidence never colour-only (label + segments)
- [x] AI output in card language — no chat bubble/avatar; every claim has confidence + citation
- [x] Abstention styled as a designed success state, never error-red (BR-6)

## Demo checklist (Bible §14.9)
- [x] Seeded corpus loads; 4→1 resolution lands deterministically
- [x] Multi-hop investigation returns cited chain
- [x] Compliance matrix shows overdue OISD item + coverage footer
- [x] Gated work-order write path works + audited
- [x] Graph-disabled refusal path works (the closing move)
- [x] Runs with the network cable pulled (embedded profile, no external services, no API key)

## Known gaps (honest — `known_bugs.md`)
- P&ID graphics extraction stubbed behind a flag (KB-1); production DB adapters lightly exercised
  in this build (KB-2); browser SpeechRecognition for voice (KB-3); in-repo eval metrics (KB-4).
