# UI Rules — "never redesign, always defer to design.md"

`design.md` is the *only* authority for how Prahari looks. This file is the enforcement doc.

## Absolute rules
1. **No raw values in components.** Every colour, type ramp, radius, spacing, and motion value
   comes from `frontend/src/design/tokens.css` (a faithful transcription of `design.md`'s token
   blocks). A hex code or px literal in a `.tsx` file is a defect.
2. **One chromatic accent for action.** `--signal` (steel cyan #3FAAB8) carries navigation,
   focus, selection only. Consequential approve/reject uses `--decision` (#5C8FC7) via
   `button-decision` — never `--signal`. A user's eye must never confuse "navigate" with
   "approve a shutdown".
3. **Semantic colours mean one thing.** `evidence` gold, `investigation` indigo, `decision`
   blue, `knowledge` teal, `prediction` violet+dashed, `simulation` magenta+labelled, risk =
   green→amber→red gradient only. Never reuse a token because it "looks right".
4. **No shadows, ever.** Depth = the five-step surface ladder (`canvas`→`surface-1..4`) plus,
   on focus/live, a cyan instrument glow.
5. **Radius is use-coded.** 2–8px on chrome; **0px on every full-bleed data canvas**
   (GraphCanvas, timelines, charts); `full` reserved for status dots, toggles, avatars.
6. **Type: one family, weight 400–650 only.** Never lighter, never heavier. `Datum Sans`
   (Inter substitute), `Datum Mono` (JetBrains Mono) for code/logs/IDs/hashes only.
7. **AI output uses the same card language as human analysis.** No chat bubbles, no avatar, no
   assistant name, no sparkle icon. Every AI claim carries a `ConfidenceIndicator` and a
   `SourceCitationChip` as a structural requirement.
8. **Confidence is never colour-only** (NFR-10). Every state (`Grounded`/`Inferred`/
   `Unsupported`/`Abstained`) carries a label or icon in addition to any colour.
9. **Simulated/predicted data** is triple-marked: distinct hue + dashed stroke + persistent
   label. It can never resemble live operational data.
10. **No spinners.** Determinate progress bar where % is known; opacity-pulse skeleton
    otherwise. Investigation loading is *named per agent stage* (Planner→…→Verifier), not a
    generic spinner.

## Abstention styling (BR-6, hard rule)
The `AbstainCard` is a designed, positive success state. It must be visually distinct from both
"answer" and "error", and must **never** use `critical`/error-red styling. It shows: what could
not be grounded, what *is* known, and who to ask.

## Motion
Short, linear, mechanical (`ease-engineered` cubic-bezier(0.2,0,0,1)). Nothing bounces or
overshoots. The only looping motion is the traveling-dash on an active pipeline edge (real
flow) and the status-dot breathing pulse (live reading). Respect `prefers-reduced-motion`: the
traversal animation must have a static `TraversalTrace` equivalent carrying the same info.
