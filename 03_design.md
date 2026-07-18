# SENTINEL Design System

*Industrial Decision Intelligence Operating System — v1.0*

---
version: 1.0
name: SENTINEL-design-system
description: "An Industrial Decision Intelligence Operating System interface built on a graphite-black instrument canvas rather than a neutral or blue-black one. A single restrained steel-cyan signal color carries all primary action and focus; every other color in the system is a semantic token tied to a specific operational meaning — evidence, investigation, decision, risk, prediction, simulation, digital twin — never decoration. Display type is set in a compressed weight range (400-650, never lighter, never bolder) with tight line-heights on headlines and relaxed line-heights on data-dense body copy. Corners run small and precise (2-8px) everywhere UI chrome appears, and drop to 0px on every full-bleed data canvas, so the instrument surfaces read as instruments, not cards. Depth is carried entirely by a five-step surface ladder and an occasional cyan instrument-glow — never a shadow. The result reads as a single, quiet, engineered command surface: evidence visible, reasoning visible, AI invisible."

colors:
  canvas: "#0B0D0F"
  surface-inset: "#08090A"
  surface-1: "#131619"
  surface-2: "#1A1E22"
  surface-3: "#22262B"
  surface-4: "#2A2F35"
  hairline: "#2B3036"
  hairline-soft: "#1D2024"
  hairline-strong: "#3A4048"
  ink: "#F2F4F6"
  ink-muted: "#ADB5BD"
  ink-subtle: "#767E87"
  ink-faint: "#4A5058"
  inverse-canvas: "#F2F4F6"
  inverse-ink: "#0B0D0F"
  on-signal: "#06181B"
  on-critical: "#FFFFFF"
  on-decision: "#FFFFFF"
  signal: "#3FAAB8"
  signal-bright: "#5CC4D1"
  signal-dim: "#2C7885"
  signal-wash: "rgba(63,170,184,0.12)"
  success: "#3FA66B"
  success-dim: "#2C7A4C"
  warning: "#C98A3F"
  warning-dim: "#9C6B2E"
  critical: "#C4453A"
  critical-dim: "#96332A"
  critical-bright: "#E85A4D"
  offline: "#565C64"
  investigation: "#7B7FC4"
  evidence: "#B9A46C"
  knowledge: "#4E9B94"
  decision: "#5C8FC7"
  decision-dim: "#43699B"
  prediction: "#9A8FD6"
  simulation: "#A66B9E"
  twin: "#2FB6C4"
  risk-low: "#3FA66B"
  risk-mid: "#C98A3F"
  risk-high: "#C4453A"
  overlay-scrim: "rgba(8,9,10,0.72)"

typography:
  display-xl:
    fontFamily: "'Datum Sans', Inter, -apple-system, 'Segoe UI', sans-serif"
    fontSize: 56px
    fontWeight: 650
    lineHeight: 1.10
    letterSpacing: -0.01em
  display-lg:
    fontFamily: "'Datum Sans', Inter, sans-serif"
    fontSize: 40px
    fontWeight: 650
    lineHeight: 1.12
    letterSpacing: -0.01em
  display-md:
    fontFamily: "'Datum Sans', Inter, sans-serif"
    fontSize: 32px
    fontWeight: 600
    lineHeight: 1.15
    letterSpacing: 0
  headline:
    fontFamily: "'Datum Sans', Inter, sans-serif"
    fontSize: 24px
    fontWeight: 600
    lineHeight: 1.20
    letterSpacing: 0
  title:
    fontFamily: "'Datum Sans', Inter, sans-serif"
    fontSize: 20px
    fontWeight: 600
    lineHeight: 1.25
    letterSpacing: 0
  subtitle:
    fontFamily: "'Datum Sans', Inter, sans-serif"
    fontSize: 17px
    fontWeight: 500
    lineHeight: 1.35
    letterSpacing: 0
  body:
    fontFamily: "'Datum Sans', Inter, sans-serif"
    fontSize: 15px
    fontWeight: 400
    lineHeight: 1.60
    letterSpacing: 0
  body-sm:
    fontFamily: "'Datum Sans', Inter, sans-serif"
    fontSize: 13px
    fontWeight: 400
    lineHeight: 1.55
    letterSpacing: 0
  caption:
    fontFamily: "'Datum Sans', Inter, sans-serif"
    fontSize: 12px
    fontWeight: 400
    lineHeight: 1.45
    letterSpacing: 0
  metadata:
    fontFamily: "'Datum Sans', Inter, sans-serif"
    fontSize: 11px
    fontWeight: 500
    lineHeight: 1.40
    letterSpacing: 0.02em
  label:
    fontFamily: "'Datum Sans', Inter, sans-serif"
    fontSize: 11px
    fontWeight: 600
    lineHeight: 1.30
    letterSpacing: 0.08em
    textTransform: uppercase
  button:
    fontFamily: "'Datum Sans', Inter, sans-serif"
    fontSize: 13px
    fontWeight: 600
    lineHeight: 1.20
    letterSpacing: 0.02em
  table-header:
    fontFamily: "'Datum Sans', Inter, sans-serif"
    fontSize: 11px
    fontWeight: 600
    lineHeight: 1.30
    letterSpacing: 0.06em
    textTransform: uppercase
  table-cell:
    fontFamily: "'Datum Sans', Inter, sans-serif"
    fontSize: 13px
    fontWeight: 400
    lineHeight: 1.50
    letterSpacing: 0
    fontFeature: tabular-nums
  code:
    fontFamily: "'Datum Mono', 'JetBrains Mono', ui-monospace, monospace"
    fontSize: 13px
    fontWeight: 400
    lineHeight: 1.60
    letterSpacing: 0
  log-line:
    fontFamily: "'Datum Mono', 'JetBrains Mono', ui-monospace, monospace"
    fontSize: 12px
    fontWeight: 400
    lineHeight: 1.70
    letterSpacing: 0
  chart-label:
    fontFamily: "'Datum Sans', Inter, sans-serif"
    fontSize: 11px
    fontWeight: 500
    lineHeight: 1.30
    letterSpacing: 0.01em
  chart-value:
    fontFamily: "'Datum Sans', Inter, sans-serif"
    fontSize: 14px
    fontWeight: 600
    lineHeight: 1.20
    letterSpacing: 0
    fontFeature: tabular-nums
  metric-value:
    fontFamily: "'Datum Sans', Inter, sans-serif"
    fontSize: 36px
    fontWeight: 650
    lineHeight: 1.05
    letterSpacing: -0.01em
    fontFeature: tabular-nums
  graph-node-label:
    fontFamily: "'Datum Sans', Inter, sans-serif"
    fontSize: 11px
    fontWeight: 500
    lineHeight: 1.20
    letterSpacing: 0
  timeline-label:
    fontFamily: "'Datum Sans', Inter, sans-serif"
    fontSize: 11px
    fontWeight: 500
    lineHeight: 1.30
    letterSpacing: 0.02em
  decision-title:
    fontFamily: "'Datum Sans', Inter, sans-serif"
    fontSize: 17px
    fontWeight: 600
    lineHeight: 1.30
    letterSpacing: 0
  evidence-citation:
    fontFamily: "'Datum Sans', Inter, sans-serif"
    fontSize: 12px
    fontWeight: 400
    lineHeight: 1.50
    letterSpacing: 0
  alert-title:
    fontFamily: "'Datum Sans', Inter, sans-serif"
    fontSize: 15px
    fontWeight: 600
    lineHeight: 1.30
    letterSpacing: 0
  mobile-display:
    fontFamily: "'Datum Sans', Inter, sans-serif"
    fontSize: 28px
    fontWeight: 650
    lineHeight: 1.15
    letterSpacing: 0

rounded:
  none: 0px
  xs: 2px
  sm: 4px
  md: 6px
  lg: 8px
  xl: 12px
  full: 9999px

spacing:
  hair: 1px
  2xs: 2px
  xs: 4px
  sm: 8px
  md: 12px
  lg: 16px
  xl: 24px
  2xl: 32px
  3xl: 48px
  4xl: 64px
  section: 96px

components:
  button-primary:
    backgroundColor: "{colors.signal}"
    textColor: "{colors.on-signal}"
    typography: "{typography.button}"
    rounded: "{rounded.sm}"
    padding: 10px 16px
  button-primary-hover:
    backgroundColor: "{colors.signal-bright}"
    textColor: "{colors.on-signal}"
    rounded: "{rounded.sm}"
  button-primary-pressed:
    backgroundColor: "{colors.signal-dim}"
    textColor: "{colors.on-signal}"
    rounded: "{rounded.sm}"
  button-primary-disabled:
    backgroundColor: "{colors.surface-3}"
    textColor: "{colors.ink-faint}"
    rounded: "{rounded.sm}"
  button-secondary:
    backgroundColor: "{colors.surface-2}"
    textColor: "{colors.ink}"
    typography: "{typography.button}"
    rounded: "{rounded.sm}"
    padding: 10px 16px
    border: "1px solid {colors.hairline-strong}"
  button-tertiary:
    backgroundColor: transparent
    textColor: "{colors.ink-muted}"
    typography: "{typography.button}"
    rounded: "{rounded.sm}"
    padding: 10px 16px
  button-destructive:
    backgroundColor: "{colors.critical}"
    textColor: "{colors.on-critical}"
    typography: "{typography.button}"
    rounded: "{rounded.sm}"
    padding: 10px 16px
  button-decision:
    backgroundColor: "{colors.decision}"
    textColor: "{colors.on-decision}"
    typography: "{typography.button}"
    rounded: "{rounded.sm}"
    padding: 10px 16px
  button-icon:
    backgroundColor: transparent
    textColor: "{colors.ink-muted}"
    rounded: "{rounded.sm}"
    padding: 8px
  text-input:
    backgroundColor: "{colors.surface-1}"
    textColor: "{colors.ink}"
    typography: "{typography.body}"
    rounded: "{rounded.sm}"
    padding: 8px 12px
    border: "1px solid {colors.hairline}"
  text-input-focus:
    backgroundColor: "{colors.surface-1}"
    textColor: "{colors.ink}"
    rounded: "{rounded.sm}"
    border: "1.5px solid {colors.signal}"
  text-input-error:
    backgroundColor: "{colors.surface-1}"
    textColor: "{colors.ink}"
    rounded: "{rounded.sm}"
    border: "1.5px solid {colors.critical}"
  dropdown-panel:
    backgroundColor: "{colors.surface-3}"
    textColor: "{colors.ink}"
    typography: "{typography.body-sm}"
    rounded: "{rounded.md}"
    border: "1px solid {colors.hairline-strong}"
    padding: 4px
  checkbox:
    backgroundColor: transparent
    rounded: "{rounded.xs}"
    border: "1px solid {colors.hairline-strong}"
  checkbox-checked:
    backgroundColor: "{colors.signal}"
    textColor: "{colors.on-signal}"
    rounded: "{rounded.xs}"
  toggle-off:
    backgroundColor: "{colors.surface-3}"
    rounded: "{rounded.full}"
  toggle-on:
    backgroundColor: "{colors.signal}"
    rounded: "{rounded.full}"
  segmented-control:
    backgroundColor: "{colors.surface-1}"
    rounded: "{rounded.sm}"
    border: "1px solid {colors.hairline}"
    padding: 2px
  segmented-item-active:
    backgroundColor: "{colors.surface-3}"
    textColor: "{colors.ink}"
    typography: "{typography.body-sm}"
    rounded: "{rounded.xs}"
  tab-item-active:
    backgroundColor: transparent
    textColor: "{colors.ink}"
    typography: "{typography.body-sm}"
    border: "2px solid {colors.signal}"
  sidebar:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink-muted}"
    typography: "{typography.body-sm}"
    width: 240px
  sidebar-nav-item-active:
    backgroundColor: "{colors.signal-wash}"
    textColor: "{colors.ink}"
    typography: "{typography.body-sm}"
    rounded: "{rounded.sm}"
  top-command-bar:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.body-sm}"
    height: 56px
    border: "0 0 1px 0 solid {colors.hairline}"
  metric-card:
    backgroundColor: "{colors.surface-1}"
    textColor: "{colors.ink}"
    typography: "{typography.metric-value}"
    rounded: "{rounded.md}"
    border: "1px solid {colors.hairline}"
    padding: 20px
  decision-card:
    backgroundColor: "{colors.surface-1}"
    textColor: "{colors.ink}"
    typography: "{typography.decision-title}"
    rounded: "{rounded.md}"
    border: "1px solid {colors.hairline}"
    borderLeft: "3px solid {colors.decision}"
    padding: 20px
  evidence-card:
    backgroundColor: "{colors.surface-1}"
    textColor: "{colors.ink}"
    typography: "{typography.body-sm}"
    rounded: "{rounded.sm}"
    border: "1px solid {colors.hairline}"
    padding: 16px
  knowledge-card:
    backgroundColor: "{colors.surface-1}"
    textColor: "{colors.ink}"
    typography: "{typography.body-sm}"
    rounded: "{rounded.sm}"
    border: "1px solid {colors.hairline}"
    padding: 16px
  alert-card-critical:
    backgroundColor: "{colors.surface-1}"
    textColor: "{colors.ink}"
    typography: "{typography.alert-title}"
    rounded: "{rounded.sm}"
    border: "1px solid {colors.hairline}"
    borderLeft: "3px solid {colors.critical}"
    padding: 16px
  risk-card:
    backgroundColor: "{colors.surface-1}"
    textColor: "{colors.ink}"
    typography: "{typography.body-sm}"
    rounded: "{rounded.sm}"
    border: "1px solid {colors.hairline}"
    padding: 16px
  status-badge:
    backgroundColor: "{colors.surface-2}"
    textColor: "{colors.ink-muted}"
    typography: "{typography.label}"
    rounded: "{rounded.full}"
    padding: 2px 10px
  tree-row:
    backgroundColor: transparent
    textColor: "{colors.ink}"
    typography: "{typography.body-sm}"
    height: 32px
  data-grid-header:
    backgroundColor: "{colors.surface-1}"
    textColor: "{colors.ink-muted}"
    typography: "{typography.table-header}"
    height: 36px
    border: "0 0 1px 0 solid {colors.hairline-strong}"
  data-grid-row:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.table-cell}"
    height: 40px
    border: "0 0 1px 0 solid {colors.hairline-soft}"
  data-grid-row-selected:
    backgroundColor: "{colors.signal-wash}"
    textColor: "{colors.ink}"
    typography: "{typography.table-cell}"
    height: 40px
  terminal-panel:
    backgroundColor: "{colors.surface-inset}"
    textColor: "{colors.ink-muted}"
    typography: "{typography.log-line}"
    rounded: "{rounded.md}"
    padding: 16px
  command-bar:
    backgroundColor: "{colors.surface-3}"
    textColor: "{colors.ink}"
    typography: "{typography.body}"
    rounded: "{rounded.lg}"
    border: "1px solid {colors.hairline-strong}"
    padding: 8px
  copilot-panel:
    backgroundColor: "{colors.surface-1}"
    textColor: "{colors.ink}"
    typography: "{typography.body-sm}"
    width: 360px
    border: "1px 0 0 0 solid {colors.hairline}"
  confidence-indicator:
    backgroundColor: "{colors.surface-2}"
    fillColor: "{colors.signal}"
    rounded: "{rounded.xs}"
  source-citation-chip:
    backgroundColor: transparent
    textColor: "{colors.evidence}"
    typography: "{typography.metadata}"
    rounded: "{rounded.xs}"
    border: "1px solid {colors.evidence}"
    padding: 0px 6px
  investigation-canvas:
    backgroundColor: "{colors.surface-inset}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
  digital-twin-canvas:
    backgroundColor: "{colors.surface-inset}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
  simulation-panel:
    backgroundColor: "{colors.surface-inset}"
    textColor: "{colors.simulation}"
    rounded: "{rounded.none}"
    border: "1px dashed {colors.simulation}"
  status-dot-live:
    backgroundColor: "{colors.success}"
    rounded: "{rounded.full}"
  status-dot-stale:
    backgroundColor: "{colors.warning}"
    rounded: "{rounded.full}"
  status-dot-fault:
    backgroundColor: "{colors.critical}"
    rounded: "{rounded.full}"
  dialog:
    backgroundColor: "{colors.surface-3}"
    textColor: "{colors.ink}"
    typography: "{typography.title}"
    rounded: "{rounded.lg}"
    border: "1px solid {colors.hairline-strong}"
    padding: 24px
  drawer:
    backgroundColor: "{colors.surface-2}"
    textColor: "{colors.ink}"
    typography: "{typography.body}"
    rounded: "{rounded.lg}"
    padding: 24px
  toast-critical:
    backgroundColor: "{colors.surface-3}"
    textColor: "{colors.ink}"
    typography: "{typography.body-sm}"
    rounded: "{rounded.sm}"
    border: "1px solid {colors.hairline-strong}"
    borderLeft: "3px solid {colors.critical}"
    padding: 12px 16px
  tooltip:
    backgroundColor: "{colors.surface-4}"
    textColor: "{colors.ink}"
    typography: "{typography.caption}"
    rounded: "{rounded.xs}"
    padding: 4px 8px
  skeleton-loader:
    backgroundColor: "{colors.surface-2}"
    rounded: "{rounded.sm}"
---

## Overview

SENTINEL runs on a single instrument-grade canvas: `{colors.canvas}` (#0B0D0F), a graphite black with a cool, neutral undertone — dark enough to disappear in a control room, warm enough that it never reads as a "theme." A five-step surface ladder (`{colors.canvas}` → `{colors.surface-1}` → `{colors.surface-2}` → `{colors.surface-3}` → `{colors.surface-4}`) carries every unit of hierarchy in the system. There is no drop shadow anywhere in SENTINEL. Depth is either a surface stepping up, or — on focus, on a live signal, on an active state — a quiet cyan glow. Nothing floats; everything sits at a known level.

One chromatic color, `{colors.signal}`, carries general-purpose action: navigation, links, focus, selection. Every other color in the palette is a semantic instrument reading, not a decoration — evidence is gold, investigation is indigo, decision is blue, knowledge is teal, prediction is violet and dashed, simulation is magenta-violet and always labeled, risk moves along a green-amber-red gradient that never leaves that gradient. A designer or engineer extending SENTINEL should be able to look at any colored element and state, without guessing, what class of information it represents.

Type runs on a single family, `Datum Sans`, across the entire hierarchy — display, body, tables, labels, buttons — the way a single instrument typeface would run across every gauge on a console. The weight range is deliberately compressed: nothing lighter than 400, nothing heavier than 650. There is no delicate thin-weight editorial voice and no oversized black display weight; the range itself is the brand's restraint. A companion mono, `Datum Mono`, is reserved for code, logs, IDs, and evidentiary hashes — anywhere the exact character matters more than the voice.

Corners run small and are use-coded, not decorative: 2–8px on every piece of UI chrome, and exactly 0px on every full-bleed data surface — investigation canvases, digital twin views, charts, timelines — so that the instrument surfaces read as instruments and the interactive chrome around them reads as controls. The one true circle in the system, `{rounded.full}`, is reserved for status dots, toggles, and avatars: the analog-gauge shape, used only where a live reading or an identity is being represented.

**Key Characteristics:**
- A single graphite-black canvas and a five-step surface ladder carry every unit of depth; there is no shadow token anywhere in the system.
- One chromatic accent, `{colors.signal}` — a desaturated steel cyan — carries general navigation and action; every other hue in the palette is a semantic instrument reading with one and only one meaning.
- A single type family across the full hierarchy, held to a compressed 400–650 weight range — no light-weight editorial voice, no black-weight shouting.
- Radius is use-coded: 2–8px on chrome, 0px on data canvases, full-round reserved for live status dots, toggles, and avatars only.
- AI output renders in the same card language as human-authored analysis — no chat bubbles, no avatar, no floating widget. Every AI-derived claim carries a visible confidence reading and a source citation as a structural requirement, not a stylistic option.
- Simulated and predicted data is never allowed to visually resemble live operational data: dashed strokes, a distinct hue family, and a persistent label are all present simultaneously wherever synthetic data appears.
- Motion is short, linear-feeling, and mechanical. Nothing bounces, springs, or overshoots. The one exception — a slow traveling dash on an active pipeline edge — represents an actual flow of material or data, never decoration.

## Colors

### Canvas & Surface
The surface ladder is the single mechanism SENTINEL uses to express hierarchy on a dark ground.

| Token | Value | Use |
|---|---|---|
| `{colors.surface-inset}` | #08090A | Recessed surfaces: terminal/log panels, code blocks, digital twin and investigation canvas backgrounds — anywhere raw system output or a spatial scene needs to sit visibly *below* the UI chrome around it |
| `{colors.canvas}` | #0B0D0F | The base page surface; also the sidebar and top command bar, which stay at canvas level so navigation chrome recedes and content elevates |
| `{colors.surface-1}` | #131619 | First lift — default cards: metric, decision, evidence, knowledge, alert, risk cards; the main content region of a page |
| `{colors.surface-2}` | #1A1E22 | Second lift — drawers, nested cards inside a card, hovered rows |
| `{colors.surface-3}` | #22262B | Third lift — dropdown panels, context menus, command bar, dialogs |
| `{colors.surface-4}` | #2A2F35 | Fourth lift — tooltips, the topmost popover layer |

### Borders
| Token | Value | Use |
|---|---|---|
| `{colors.hairline-soft}` | #1D2024 | The quietest divider — data-grid row separators, dense table rules |
| `{colors.hairline}` | #2B3036 | Default 1px border — cards, inputs, panel edges |
| `{colors.hairline-strong}` | #3A4048 | Emphasized border — dropdown panels, dialogs, focus-adjacent chrome |

### Typography
| Token | Value | Use |
|---|---|---|
| `{colors.ink}` | #F2F4F6 | Primary text — an off-white, never pure white, to reduce glare on a control-room display |
| `{colors.ink-muted}` | #ADB5BD | Secondary text — labels, nav items, captions |
| `{colors.ink-subtle}` | #767E87 | Tertiary text — timestamps, placeholder, disabled |
| `{colors.ink-faint}` | #4A5058 | Quaternary text — the quietest label in the system, section dividers |
| `{colors.on-signal}` | #06181B | Dark text set on a signal-cyan fill |
| `{colors.on-critical}` | #FFFFFF | White text set on a critical-red fill |
| `{colors.on-decision}` | #FFFFFF | White text set on a decision-blue fill |

### Signal (the single chromatic accent)
| Token | Value | Use |
|---|---|---|
| `{colors.signal}` | #3FAAB8 | Primary buttons, links, focus rings, active nav state, selected rows, default chart series |
| `{colors.signal-bright}` | #5CC4D1 | Hover state of any signal-colored control |
| `{colors.signal-dim}` | #2C7885 | Pressed/active state of any signal-colored control |
| `{colors.signal-wash}` | rgba(63,170,184,0.12) | Background tint for a selected row, an active nav item, a focused panel — never a full-strength fill |

Signal is used for general wayfinding and action — "click here to proceed, this is where you are." It is never used to represent operational severity, evidence, or a consequential decision; those each have their own token below, specifically so a user can never mistake "navigate" for "approve a shutdown."

### Operational State
| Token | Value | Use |
|---|---|---|
| `{colors.success}` | #3FA66B | Nominal / healthy / completed states; live-sensor status dots |
| `{colors.success-dim}` | #2C7A4C | Success state on a dark chip background |
| `{colors.warning}` | #C98A3F | Caution states; stale-sensor status dots; the timeline "now" marker |
| `{colors.warning-dim}` | #9C6B2E | Warning state on a dark chip background |
| `{colors.critical}` | #C4453A | Fault / alarm / rejected states; fault-sensor status dots |
| `{colors.critical-dim}` | #96332A | Critical state on a dark chip background |
| `{colors.critical-bright}` | #E85A4D | Active/unacknowledged alarm emphasis — used only for the brief pulse on a newly-raised critical alert |
| `{colors.offline}` | #565C64 | Asset or sensor offline, or state genuinely unknown — deliberately neutral, never implies severity |

### Domain Semantics
This is SENTINEL's signature palette layer — colors that exist because the product's information model requires them, not because a marketing page needed a fifth accent.

| Token | Value | Meaning |
|---|---|---|
| `{colors.investigation}` | #7B7FC4 | Investigation-mode chrome, forensic threads, root-cause panels |
| `{colors.evidence}` | #B9A46C | Evidence cards, citations, source documents, chain-of-custody markers |
| `{colors.knowledge}` | #4E9B94 | Knowledge graph nodes, the document library, ontology tags |
| `{colors.decision}` | #5C8FC7 | Decision cards, recommended-action chrome, approval controls |
| `{colors.decision-dim}` | #43699B | Decision state on a dark chip background |
| `{colors.prediction}` | #9A8FD6 | Forecast values and projected states — always rendered with a dashed stroke, never a solid fill |
| `{colors.simulation}` | #A66B9E | "What-if" / hypothetical scenario output — always paired with a dashed outline and a persistent "SIMULATED" label |
| `{colors.twin}` | #2FB6C4 | Live spatial elements inside the Digital Twin Canvas only — a distinct, slightly brighter cousin of signal so twin-specific chrome never gets confused with generic UI |

### Risk Gradient
| Token | Value | Use |
|---|---|---|
| `{colors.risk-low}` | #3FA66B | Low-risk cells in a risk matrix or heatmap (reuses `{colors.success}`) |
| `{colors.risk-mid}` | #C98A3F | Medium-risk cells (reuses `{colors.warning}`) |
| `{colors.risk-high}` | #C4453A | High-risk cells (reuses `{colors.critical}`) |

Risk visualizations interpolate through exactly these three stops — never a rainbow or "jet" colormap, which reads as decorative rather than instrumented and is not reliably colorblind-safe.

### Overlay
| Token | Value | Use |
|---|---|---|
| `{colors.overlay-scrim}` | rgba(8,9,10,0.72) | The scrim behind a modal dialog |

Every semantic token above maps to exactly one meaning across the entire product. If a new feature needs a new color, it needs a new named token with a documented meaning — SENTINEL never reaches for an existing token because "it happens to look right" in a new context.

## Typography

### Font Family
SENTINEL runs a single family, **Datum Sans**, across the entire hierarchy — display headlines, body copy, table cells, button labels, status text. Fallback stack: `Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif`. A companion monospace, **Datum Mono** (fallback: `JetBrains Mono, ui-monospace, "SF Mono", monospace`), is reserved exclusively for code, logs, terminal output, and evidentiary identifiers — anywhere exact characters matter more than voice.

Weight is held to a compressed range: 400 (body), 500 (medium — table headers, metadata), 600 (emphasis — headlines, titles, buttons), and a single custom 650 (structural — the largest display sizes and metric numerals only). SENTINEL never drops to a light editorial weight and never reaches for a black display weight; the narrow range itself communicates engineering restraint rather than either softness or aggression.

### Hierarchy

| Token | Size | Weight | Line Height | Tracking | Use |
|---|---|---|---|---|---|
| `{typography.display-xl}` | 56px | 650 | 1.10 | -0.01em | Presentation / mission-control wall headline |
| `{typography.display-lg}` | 40px | 650 | 1.12 | -0.01em | Page-level display headline |
| `{typography.display-md}` | 32px | 600 | 1.15 | 0 | Section display |
| `{typography.headline}` | 24px | 600 | 1.20 | 0 | Panel headline |
| `{typography.title}` | 20px | 600 | 1.25 | 0 | Card title, dialog title |
| `{typography.subtitle}` | 17px | 500 | 1.35 | 0 | Lead paragraph, card subtitle |
| `{typography.body}` | 15px | 400 | 1.60 | 0 | Default body copy |
| `{typography.body-sm}` | 13px | 400 | 1.55 | 0 | Secondary body, dense list rows |
| `{typography.caption}` | 12px | 400 | 1.45 | 0 | Captions, helper text |
| `{typography.metadata}` | 11px | 500 | 1.40 | 0.02em | Timestamps, IDs, byline meta |
| `{typography.label}` | 11px | 600 | 1.30 | 0.08em, uppercase | Index Label — section eyebrows, table headers, status text |
| `{typography.button}` | 13px | 600 | 1.20 | 0.02em | Button labels |
| `{typography.table-header}` | 11px | 600 | 1.30 | 0.06em, uppercase | Data-grid column headers |
| `{typography.table-cell}` | 13px | 400 | 1.50 | 0, tabular-nums | Data-grid cell content |
| `{typography.code}` | 13px | 400 | 1.60 | 0 | Inline code, evidence hashes, sensor IDs |
| `{typography.log-line}` | 12px | 400 | 1.70 | 0 | Log stream / terminal output |
| `{typography.chart-label}` | 11px | 500 | 1.30 | 0.01em | Chart axis labels, legends |
| `{typography.chart-value}` | 14px | 600 | 1.20 | 0, tabular-nums | Data-point callouts on charts |
| `{typography.metric-value}` | 36px | 650 | 1.05 | -0.01em, tabular-nums | The large numeral inside a metric card |
| `{typography.graph-node-label}` | 11px | 500 | 1.20 | 0 | Knowledge / network graph node captions |
| `{typography.timeline-label}` | 11px | 500 | 1.30 | 0.02em | Timeline tick labels |
| `{typography.decision-title}` | 17px | 600 | 1.30 | 0 | Decision-card headline |
| `{typography.evidence-citation}` | 12px | 400 | 1.50 | 0 | Evidence source citation line |
| `{typography.alert-title}` | 15px | 600 | 1.30 | 0 | Alert / incident card title |
| `{typography.mobile-display}` | 28px | 650 | 1.15 | 0 | Compressed display for mobile / field tablet |

### Principles
- **One family, held to 400–650.** The weight range is the brand's typographic signature: never lighter, never heavier. There is no "light editorial" mode and no "black display" mode anywhere in SENTINEL.
- **Tight on display, relaxed on data.** Display line-heights sit at 1.05–1.20; body, table, and log line-heights open up to 1.45–1.70 so dense sensor tables and log streams stay legible at long viewing sessions rather than reading as a marketing headline stack.
- **Tracking is restrained everywhere except the Index Label.** Display type carries only a hairline -0.01em; body carries none at all. The one place tracking works hard is `{typography.label}` — an uppercase, 0.08em-tracked device used as section eyebrows, table headers, and status text throughout the system. It is SENTINEL's one consistent typographic signature and appears above nearly every structural boundary in the product.
- **Numerals are always tabular.** Any place a number can change at runtime — metric values, table cells, chart callouts — uses tabular figures so digits don't shift the layout as they update.
- **Mono is a citation, not a voice.** Datum Mono appears only where the literal character sequence is the content itself: code, logs, hashes, IDs. It never appears in headlines or marketing-style callouts.

### Note on Font Substitutes
Datum Sans and Datum Mono are the documented internal names for SENTINEL's typographic system. Until a custom cut exists, **Inter** (variable, weights 400/500/600/650-approximated-as-650-or-nearest-available) is the production substitute for Datum Sans, and **JetBrains Mono** at weight 400 is the substitute for Datum Mono.

## Layout

### Spacing System
- **Base unit:** 8px, on a strict 4px sub-grid for icon- and border-level fine adjustment only.
- **Tokens:** `{spacing.hair}` 1px · `{spacing.2xs}` 2px · `{spacing.xs}` 4px · `{spacing.sm}` 8px · `{spacing.md}` 12px · `{spacing.lg}` 16px · `{spacing.xl}` 24px · `{spacing.2xl}` 32px · `{spacing.3xl}` 48px · `{spacing.4xl}` 64px · `{spacing.section}` 96px.
- **Card interior padding:** `{spacing.xl}` (24px) for metric, decision, and risk cards; `{spacing.lg}` (16px) for evidence, knowledge, and alert cards, which run denser.
- **Panel and canvas toolbar padding:** `{spacing.sm}`–`{spacing.md}` (8–12px) — canvases themselves run full-bleed with zero outer padding; only their floating toolbars carry interior padding.
- **Section rhythm:** `{spacing.section}` (96px) between major page sections on report-style and settings surfaces. Operational dashboards, which are density-first rather than editorial, instead use `{spacing.xl}` (24px) between panel rows.

### Grid & Container
- **Application shell:** a fixed three-region layout — a `{component.sidebar}` (240px, collapsible to a 64px icon rail), a `{component.top-command-bar}` (56px), and a fluid main region that fills the remainder.
- **Dashboard grid:** 12-column, `{spacing.lg}` (16px) gutters, with metric cards typically spanning 3 columns (4-up), decision and alert cards spanning 4 columns (3-up), and canvases (investigation, digital twin, timeline) spanning the full 12.
- **Report / document surfaces:** a single content column capped at 840px for long-form reading (incident reports, investigation summaries).
- **Data-grid surfaces:** full-width, no max — wide sensor and asset tables are allowed to run edge-to-edge with horizontal scroll and a sticky identifying column.

### Whitespace Philosophy
The dark canvas carries the whitespace the way it does throughout SENTINEL's surface ladder — separation comes from a surface stepping up, not from a gap opening in white. Within an operational dashboard, density is a feature: an operator scanning forty sensor readings benefits from tight, consistent `{spacing.lg}` rhythm between metric cards, not generous air. Within a report, investigation summary, or onboarding surface, the system relaxes to full `{spacing.section}` rhythm — SENTINEL deliberately runs two whitespace registers, dense-operational and relaxed-editorial, and a designer chooses the register based on whether the surface is being *scanned* or *read*.

## Elevation & Depth

| Level | Treatment | Use |
|---|---|---|
| Recessed | `{colors.surface-inset}` background, no border | Terminal/log panels, code blocks, investigation and digital twin canvas grounds — signals "raw system, not designed chrome" |
| Flat | `{colors.canvas}` background, no shadow, no border | Sidebar, top command bar, page body, footer |
| Lift 1 | `{colors.surface-1}` + 1px `{colors.hairline}` | Default cards — metric, decision, evidence, knowledge, alert, risk |
| Lift 2 | `{colors.surface-2}` + 1px `{colors.hairline}` | Drawers, nested cards, hovered rows |
| Lift 3 | `{colors.surface-3}` + 1px `{colors.hairline-strong}` | Dropdown panels, dialogs, command bar |
| Lift 4 | `{colors.surface-4}`, no border | Tooltips, topmost popovers |
| Glow | 2px `{colors.signal}` outline at 30% opacity, no shadow | Focused input, focused button, active canvas selection |

SENTINEL never uses a drop shadow. The surface ladder alone carries every unit of depth in the system, and where a shadow would traditionally mark focus or activity, SENTINEL substitutes an **instrument glow** — a soft cyan outline rather than a dark cast shadow. This is a deliberate, singular device: light communicates "live and selected," never darkness pooling beneath an element.

### Decorative Depth
- **Instrument glow** — the only decorative effect in the system; reserved for focus rings and live-selection state, always signal-cyan, always subtle (≤30% opacity).
- **Status-dot pulse** — a slow, gentle opacity breathing (see Motion) applied only to live/nominal sensor dots. Stale and fault dots hold static, so "stops breathing" itself becomes a legible signal.
- **No gradients, no atmospheric lighting, no illustrative background art** anywhere in the operational product. Illustration is reserved for empty states only (see Iconography).

## Shapes

### Border Radius Scale

| Token | Value | Use |
|---|---|---|
| `{rounded.none}` | 0px | Every full-bleed data canvas — investigation canvas, digital twin canvas, simulation panel, charts, timelines. Data reads as instrumentation, not as a card. |
| `{rounded.xs}` | 2px | Checkboxes, small chips, table-row hover state |
| `{rounded.sm}` | 4px | Buttons, inputs, tags — the dominant control radius |
| `{rounded.md}` | 6px | Cards, dropdown panels |
| `{rounded.lg}` | 8px | Dialogs, drawers, large panels |
| `{rounded.xl}` | 12px | Large illustrative containers (rare — onboarding, empty states) |
| `{rounded.full}` | 9999px | Status dots, toggles, avatars — the one true circle in the system, reserved for live readings and identity |

The radius hierarchy is **use-coded, not aesthetic**: chrome gets small precise corners (2–8px), data canvases get none at all, and full-round is earned only by things that represent a live analog reading or a person. A new component never defaults to `{rounded.xl}` or larger without a specific justification tied to onboarding or empty-state illustration.

## Iconography

SENTINEL's icon set is line-drawn, never filled, with one deliberate exception: severity and status glyphs, which fill solid specifically so they read at a glance and compete visually with nothing around them.

- **Stroke weight:** 1.5px, constant across every size.
- **Construction:** built on a 24×24px canvas with a 20×20px live area (2px of internal padding on each side), aligned to the 4px sub-grid so icons sit crisply against text baselines.
- **Sizes:** 16px (inline with body/table text), 20px (buttons, nav items), 24px (panel headers, empty states).
- **Corner radius inside glyphs:** 2px, matching `{rounded.xs}`, so icon geometry echoes the chrome radius scale rather than introducing its own.
- **Fill rule:** outline-only for every navigational, structural, and action icon. Filled glyphs are reserved for the small library of severity and status icons (critical, warning, success, offline) and for status dots — filled shapes are earned by urgency, not used decoratively.
- **Illustration:** reserved exclusively for empty states (an empty investigation canvas, an empty knowledge library) — simple, single-color line illustrations built from the same 1.5px stroke, never full-color or playful.
- **Semantic consistency:** an icon glyph always maps to the same meaning everywhere it appears — a triangle-exclamation is always warning-severity, a shield is always evidence/chain-of-custody, a node-cluster glyph is always knowledge-graph. Icons are never reused decoratively for an unrelated feature.

## Motion

Motion in SENTINEL is short, linear-feeling, and mechanical — it should read like a well-machined control responding, not like a spring or a bounce. Nothing in the system overshoots or oscillates, with the single exception of the live status-dot breathing pulse and the pipeline flow-dash, both of which represent an actual live condition rather than decoration.

### Duration Tokens
| Token | Duration | Use |
|---|---|---|
| `instant` | 80ms | Hover states, focus-ring appearance |
| `fast` | 120ms | Button press, checkbox/toggle switch, tab underline move |
| `base` | 180ms | Panel expand/collapse, dialog open, command bar open |
| `moderate` | 240ms | Drawer slide, dropdown panel open |
| `slow` | 320ms | Canvas pan/zoom settle, graph re-layout, page transition |

### Easing
| Token | Curve | Use |
|---|---|---|
| `ease-engineered` | cubic-bezier(0.2, 0, 0, 1) | The default curve for nearly everything — fast start, precise, decisive stop, never an overshoot |
| `ease-snap` | cubic-bezier(0.4, 0, 0.2, 1) at `fast` duration | Toggles, checkboxes — a slightly crisper, near-linear snap |
| `ease-glide` | cubic-bezier(0.3, 0, 0.1, 1) at `slow` duration | Canvas pan/zoom, graph layout transitions — the same family of curve, held longer for large-surface movement |

### Principles
- **State changes that matter are instant, not eased.** A new critical alert appears with no fade-in and no easing — softening an alarm's arrival with a pleasant transition would work against the alert's purpose.
- **Live numbers count, they don't jump.** When a metric-card value changes because of new live data, the numeral animates through the delta over 400–600ms (tabular figures, no layout shift) rather than snapping — this communicates "the system is alive and watching," distinct from a user-triggered UI change, which uses the standard `fast`/`base` tokens instead.
- **No spinners.** A rotating brand-mark spinner reads as "buffering consumer app." SENTINEL uses a determinate linear progress bar wherever percentage-complete is knowable, and a low-amplitude opacity-pulse skeleton (`{component.skeleton-loader}`, 0.5↔0.7 opacity, 1.2s ease-in-out, looping) everywhere else.
- **The one looping decorative motion in the system** is a slow traveling dash along an active pipeline edge in an operational-flow diagram, looping at `slow` duration — and it is permitted only because it represents literal material or data flow, not because motion is being used for delight.

## Components

### Buttons

**`button-primary`** — The default action button. Background `{colors.signal}`, text `{colors.on-signal}`, type `{typography.button}`, padding 10px 16px, rounded `{rounded.sm}`. Hover shifts to `button-primary-hover` (`{colors.signal-bright}`); press shifts to `button-primary-pressed` (`{colors.signal-dim}`); disabled shifts to `button-primary-disabled` (`{colors.surface-3}` / `{colors.ink-faint}`).

**`button-secondary`** — Charcoal button with a hairline border. Background `{colors.surface-2}`, text `{colors.ink}`, 1px `{colors.hairline-strong}` border, same shape as primary. Used for "Cancel," "Read documentation," secondary flows.

**`button-tertiary`** — Bare text button. Transparent background, `{colors.ink-muted}` text, no border. Used for low-emphasis inline actions.

**`button-destructive`** — Background `{colors.critical}`, text `{colors.on-critical}`. Reserved for genuinely destructive actions (delete, revoke access) — never used for "reject a recommendation," which belongs to `button-decision` below.

**`button-decision`** — Background `{colors.decision}`, text `{colors.on-decision}`. Used exclusively inside decision cards and approval flows — "Approve," "Reject," "Defer." This is a deliberately separate token from `button-primary` so a user's eye can never confuse "navigate forward" with "approve a consequential action."

**`button-icon`** — A 32×32px square icon-only button. Transparent by default, `{colors.surface-2}` on hover, `{colors.ink-muted}` icon color.

### Inputs & Forms

**`text-input`** + **`text-input-focus`** + **`text-input-error`** — Background `{colors.surface-1}`, text `{colors.ink}`, type `{typography.body}`, rounded `{rounded.sm}`, padding 8px 12px, 1px `{colors.hairline}` border. On focus the border thickens to 1.5px `{colors.signal}` and the input gains an instrument glow. On validation failure the border shifts to 1.5px `{colors.critical}` with helper text below in `{colors.critical}` / `{typography.caption}`.

**`textarea`** — Identical construction to `text-input`, minimum height 80px, resizable vertically only.

**`select`** — Same shell as `text-input` with a trailing chevron icon; opens a `{component.dropdown-panel}`.

**`checkbox`** + **`checkbox-checked`** — 16×16px, rounded `{rounded.xs}`. Unchecked: transparent fill, 1px `{colors.hairline-strong}` border. Checked: `{colors.signal}` fill with an `{colors.on-signal}` check glyph.

**`radio`** — 16×16px, fully circular (the standard universal exception to the square-corner control system), same state logic as checkbox.

**`toggle`** — A 36×20px track, `{rounded.full}`. Off: `{colors.surface-3}` track, `{colors.ink-subtle}` knob. On: `{colors.signal}` track, `{colors.ink}` knob. Transitions on `ease-snap`.

**`segmented-control`** — A pill-shaped container (`{colors.surface-1}`, `{rounded.sm}`, 1px `{colors.hairline}`, 2px interior padding) holding 2–5 segments. The active segment lifts to `{colors.surface-3}` with `{colors.ink}` text — deliberately **not** signal-colored, so a segmented control never competes visually with a true primary action elsewhere on the same screen.

### Tabs

**`tab-item`** + **`tab-item-active`** — Inactive: `{colors.ink-muted}` text, `{typography.body-sm}`, transparent 2px bottom border. Active: `{colors.ink}` text, 2px `{colors.signal}` bottom border. The tab bar container sits on `{colors.surface-1}` with a full-width bottom hairline.

### Navigation

**`sidebar`** — Fixed at 240px (collapsible to a 64px icon rail), background `{colors.canvas}` — deliberately held at the flat canvas level rather than lifted, so navigation chrome recedes and content is what elevates. Grouped into labeled sections (Operations / Investigations / Knowledge / Administration) using `{typography.label}` in `{colors.ink-faint}` as section headers.

**`sidebar-nav-item`** + **`sidebar-nav-item-active`** — Inactive: icon + label in `{colors.ink-muted}`. Active: a `{colors.signal-wash}` background tint, a 2px `{colors.signal}` left-rail indicator, and `{colors.ink}` text — the text itself stays neutral; only the wash and rail carry color, so active state reads clearly without the row looking "painted."

**`top-command-bar`** — 56px, background `{colors.canvas}`, bottom 1px `{colors.hairline}`. Left: workspace/plant selector. Center: the global Command Bar trigger (see below). Right: alert bell with a `{component.status-badge}` count, user menu.

**`breadcrumb`** — `{typography.body-sm}` in `{colors.ink-muted}`, "›" separators, current page in `{colors.ink}`.

**`context-menu`** — Same shell as `{component.dropdown-panel}`: `{colors.surface-3}`, `{rounded.md}`, 1px `{colors.hairline-strong}`.

### Cards & Data Display

**`metric-card`** — The primary "mission control" tile. Background `{colors.surface-1}`, `{rounded.md}`, 1px `{colors.hairline}`, padding 24px. Top row: `{typography.label}` metric name + an optional `{component.status-dot}`. Center: the reading in `{typography.metric-value}` alongside a small delta chip (success- or critical-colored, with a directional arrow). Bottom: an optional sparkline or trend caption in `{typography.caption}`.

**`decision-card`** — Background `{colors.surface-1}`, `{rounded.md}`, 1px `{colors.hairline}`, a **3px `{colors.decision}` left border** — the one card type in the system that carries a colored edge, so it visually announces "this requires a human decision" before it's even read. Header: `{typography.label}` "RECOMMENDED ACTION" + a `{component.confidence-indicator}`. Body: `{typography.decision-title}` + 2–3 lines of rationale with a "View reasoning" disclosure. Footer: an evidence-count chip + an Approve / Reject / Defer row built from `{component.button-decision}`.

**`evidence-card`** — Background `{colors.surface-1}`, `{rounded.sm}`, 1px `{colors.hairline}`, padding 16px. Top: a small `{colors.evidence}` dot + source label (`{typography.label}`) + timestamp (`{typography.metadata}`). Body: excerpt text in `{typography.body-sm}` with the specific cited span underlined in `{colors.evidence}` — never block-colored, always a precise underline. Footer: an "Open source" text link.

**`knowledge-card`** — Background `{colors.surface-1}`, `{rounded.sm}`, 1px `{colors.hairline}`, padding 16px. A `{colors.knowledge}` `{typography.label}` tag, a `{typography.title}` heading, a two-line description, and a row of small pill tags (`{rounded.full}`, `{colors.surface-2}`, `{colors.ink-muted}`) for taxonomy terms.

**`alert-card`** — Background `{colors.surface-1}`, `{rounded.sm}`, 1px `{colors.hairline}`, a 3px left border colored by severity (`{colors.critical}` / `{colors.warning}` / `{colors.investigation}`). Header: a `{typography.label}` severity tag + asset name + timestamp. Body: `{typography.body-sm}` alert message. Footer: Acknowledge / Escalate (`button-tertiary`) + a `{component.status-badge}` (Open / Acknowledged / Resolved).

**`risk-card`** — Background `{colors.surface-1}`, `{rounded.sm}`, 1px `{colors.hairline}`, padding 16px. A `{typography.label}` "RISK ASSESSMENT" header, a compact 5×5 risk-matrix swatch, a large risk-score numeral rendered in the corresponding risk-gradient color, and a one-line risk statement.

**`status-badge`** — `{rounded.full}`, padding 2px 10px, `{typography.label}`, color-coded per state. Always paired with a small leading dot of the same hue — color is never the sole carrier of meaning; shape and position redundancy make every badge colorblind-legible.

**`tree-view`** — Used for plant/asset hierarchies and knowledge trees. 16px indent per level, an outline disclosure triangle that rotates 90° on expand (`ease-engineered`, `fast`), 32px row height, `{colors.surface-1}` on hover, `{colors.signal-wash}` + 2px left rail on select.

**`activity-feed`** — A vertical list where each row places its timestamp in a fixed-width left gutter (`{typography.metadata}`) so timestamps align in a straight column regardless of description length — critical for fast scanning of dense event logs — connected by a thin hairline "spine" running down the row.

**`data-grid`** — Sticky `{component.data-grid-header}` in `{typography.table-header}` on `{colors.surface-1}`. Body rows (`{component.data-grid-row}`) run on `{colors.canvas}` at 40px height with `{colors.hairline-soft}` dividers — **no zebra striping**, which is visually noisy at industrial data density. Numeric columns are right-aligned with tabular figures. Selected rows shift to `{component.data-grid-row-selected}` (`{colors.signal-wash}` + left rail). Wide sensor tables keep the identifying column sticky during horizontal scroll.

**`terminal-panel`** — Background `{colors.surface-inset}` — the one place the UI drops darker than the base canvas, signaling raw system output rather than designed chrome. Type `{typography.log-line}` in `{colors.ink-muted}`, fixed-width timestamp gutter, and a 2px left-edge severity tick per line (`{colors.ink-subtle}` for INFO, `{colors.warning}` for WARNING, `{colors.critical}` for ERROR) rather than coloring the full line — keeps a busy log scannable instead of turning into a wall of color.

### Command & AI

**`command-bar`** — The global ⌘K launcher. A centered `{colors.surface-3}` panel, `{rounded.lg}`, 1px `{colors.hairline-strong}`, appearing via a 98%→100% scale-and-fade on `ease-engineered` at `base` duration — never a slide-up or bounce. Results group under `{typography.label}` section headers (Actions / Assets / Documents / People); each row shows an icon, title, a small context tag, and a keyboard-shortcut hint right-aligned in `{colors.ink-faint}` mono.

**`copilot-panel`** — Docked, not floating: a 360px right-side panel on `{colors.surface-1}` that opens alongside the working canvas rather than covering it, so analysis happens side-by-side with the evidence it's about. Header reads `{typography.label}` "ANALYSIS" — deliberately unbranded, no sparkle icon, no assistant name, no avatar.

**`copilot-message` (system)** — Renders using the *same* card language as the rest of the product: a stack of `evidence-card`s, a `decision-card` where relevant, and plain `{typography.body}` reasoning text. There is no chat-bubble shape, no rounded speech-tail, no avatar. The goal is that an AI-generated analysis is visually indistinguishable in craft from a human analyst's report.

**`copilot-message` (user query)** — Rendered plainly at `{typography.body}` in `{colors.ink-muted}`, left-aligned, minimal chrome — intentionally de-emphasized relative to the evidence-backed response beneath it.

**`confidence-indicator`** — A five-segment horizontal bar (each segment 3×10px, `{rounded.xs}`), filled left-to-right in `{colors.signal}` to represent confidence level, paired with a `{typography.metadata}` percentage. Appears next to every AI-derived value in the system as a structural requirement, never an optional annotation.

**`source-citation-chip`** — A small numbered chip (`[1]`), `{rounded.xs}`, 1px `{colors.evidence}` border, `{colors.evidence}` text at `{typography.metadata}`. Clicking or hovering opens the corresponding `evidence-card`. Every AI-authored claim in SENTINEL must carry at least one citation chip — enforced as a component contract, not a style suggestion.

**`reasoning-disclosure`** — A collapsed-by-default "Show reasoning" link (`{colors.ink-muted}`, `{typography.label}` caps) that expands a step-by-step trace in `{typography.body-sm}`. Reasoning is always available and never hidden behind a paywall or a separate screen, but it never forces itself onto the primary surface.

### Investigation & Analysis Canvases

**`investigation-canvas`** — Full-bleed, `{rounded.none}`, background `{colors.surface-inset}`. An infinite pan/zoom node-graph workspace where evidence, knowledge, and decision items appear as compact chips (icon + title + `{typography.label}`) connected by edges. A persistent minimap sits bottom-left (`{colors.surface-2}`, `{rounded.sm}`, 120×80px); a floating toolbar (zoom / fit / layout, built from `{component.button-icon}` on a `{colors.surface-2}` pill) sits top-right. Node color defaults to neutral `{colors.ink-muted}`, with `{colors.investigation}` used for the canvas's own selection and thread-tracing chrome.

**`knowledge-graph-panel`** — The identical canvas primitive as `investigation-canvas`, used specifically for ontology and document-relationship views. The only difference is the default node tint, which shifts to `{colors.knowledge}` instead of neutral — a named variant, not a rebuilt component, so the two surfaces never drift apart in interaction behavior.

**`digital-twin-canvas`** — Full-bleed, `{rounded.none}`, background `{colors.surface-inset}` so a spatial 3D render reads correctly against a near-black ground, the way an instrument reads against a dark cockpit panel. Chrome (layer toggles, the asset-info drawer) floats as `{colors.surface-2}` panels at the canvas edges. Live sensor readings render as `{component.status-dot}` markers pinned to spatial coordinates, colored by `status-dot-live` / `-stale` / `-fault`. Live dots pulse gently (1.6s opacity breathing) — stale and fault dots hold static, so "the dot stopped breathing" is itself a legible failure signal.

**`simulation-panel`** — Visually the same shell as `digital-twin-canvas`, but every element tints to `{colors.simulation}` and every piece of synthetic or projected geometry carries a mandatory dashed 1px outline. A persistent `{typography.label}` banner — "SIMULATED — NOT LIVE DATA" — pins to the canvas corner in `{colors.simulation}`. This triple redundancy (distinct hue, dashed stroke, persistent label) exists specifically so simulated output can never be mistaken for operational reality in a mission-critical tool.

**`decision-canvas` / timeline** — A horizontal timeline track (`{colors.surface-2}`, 4px tall). Events plot as small `{rounded.full}` markers colored by severity; a vertical "now" marker renders in `{colors.warning}` with a flag label. Time-bound decision cards can pin directly to a timeline position (e.g., "approve by 14:00"). Zoom and scrub happen via horizontal drag, snapping to the underlying time grid.

**`evidence-viewer`** — A split pane: the left side renders the native source (a PDF page, a log excerpt, a chart) inside a `{colors.surface-inset}` frame; the right side stacks the extracted `evidence-card`s. A "jump to source" link scroll-syncs the two panes and highlights the exact cited span in a `{colors.evidence}` underline.

### Feedback & Overlays

**`dialog`** — Centered, `{colors.surface-3}`, `{rounded.lg}`, 1px `{colors.hairline-strong}`, padding 24px. Scrim is `{colors.overlay-scrim}`. Opens via a 96%→100% scale-and-fade on `ease-engineered` at `base` duration.

**`drawer`** — Slides in from the right on `{colors.surface-2}`, `{rounded.lg}` on the leading edge only, `ease-glide` at `moderate` duration.

**`toast-critical`** / informational toast — `{colors.surface-3}`, `{rounded.sm}`, 1px `{colors.hairline-strong}`, a 3px left severity tick matching `alert-card`'s convention. Informational toasts auto-dismiss after 6 seconds; **critical toasts never auto-dismiss** — they persist until manually acknowledged, a deliberate safety rule so an urgent notification cannot silently vanish unseen.

**`tooltip`** — `{colors.surface-4}`, `{rounded.xs}`, `{typography.caption}`, 4px offset, `instant`-duration fade, no arrow tail — a clean rectangle rather than a speech-bubble shape.

**`skeleton-loader`** — A `{colors.surface-2}` block pulsing between 0.5 and 0.7 opacity on a 1.2s `ease-in-out` loop, shaped to match the content it's replacing. SENTINEL never uses a shimmer-sweep gradient, which reads as a consumer/marketing loading pattern rather than an instrument state.

## Data Visualization

SENTINEL's charts and graphs reuse the semantic color system rather than inventing a separate "chart palette" — the same discipline that keeps the rest of the product coherent applies here: a color in a chart means the same thing it means everywhere else in the product.

### Charts (line, bar, area)
- Default single-series color: `{colors.signal}`.
- Multi-series categorical order: `{colors.signal}` → `{colors.knowledge}` → `{colors.decision}` → `{colors.evidence}` → `{colors.investigation}` → `{colors.simulation}` — the same six hues that already carry meaning elsewhere, used in this fixed order so a legend never needs an arbitrary rainbow.
- Axis labels and legends in `{typography.chart-label}`; callout values in `{typography.chart-value}` with tabular figures.
- Gridlines at `{colors.hairline-soft}`; axis lines at `{colors.hairline}`.
- Forecast/projected segments render as a `{colors.prediction}` dashed continuation of the series — never a solid line, so a viewer can tell projection from measurement at a glance without reading a legend.

### Risk Matrix
A 5×5 Likelihood × Severity grid. Each cell shades along the three-stop `risk-low` → `risk-mid` → `risk-high` gradient and displays its numeric risk score. The organization's current position on the matrix gets a 2px `{colors.signal}` ring — the one place signal-cyan is allowed inside an otherwise risk-colored surface, specifically to mark "you are here" without being mistaken for a risk reading itself.

### Heatmaps
Single-hue intensity ramps only — `{colors.signal}` at 10–100% opacity for activity/volume heatmaps, or the three-stop risk gradient for risk heatmaps. SENTINEL never uses a multi-hue "jet" colormap: it is not reliably colorblind-safe and reads as generic BI decoration rather than an instrument reading.

### Knowledge & Network Graphs
Force-directed or hierarchical layout. Nodes are sized by importance/degree and carry **shape redundancy alongside color** so meaning survives colorblindness and grayscale printing: assets render as neutral `{colors.ink-muted}` circles, documents as `{colors.evidence}` rounded squares, people as `{colors.decision}` circles with an initials glyph, events as `{colors.warning}` triangles. Edges default to `{colors.hairline-strong}`; an active or traced path highlights in `{colors.signal}`.

### Plant Maps, Dependency Graphs & Operational Pipelines
Process/flow nodes render as `{rounded.sm}` rectangles on `{colors.surface-1}`; directional edges use `{colors.hairline-strong}` when idle and `{colors.signal}` when actively carrying flow. An active edge may carry the single permitted looping motion in the system — a slow traveling dash — to represent literal material or data throughput, never for decoration.

### Decision Trees
Branches already taken render as solid `{colors.signal}` lines; untaken or pruned branches render dashed in `{colors.ink-faint}` — the same solid/dashed convention used everywhere else to distinguish "actual" from "hypothetical."

### Execution Flow / Sensor Views / Timeline / Evidence Relationships
All reuse the primitives defined above and in the Components section (`decision-canvas`, `activity-feed`, `data-grid`, `evidence-viewer`) rather than introducing new visual language — SENTINEL's data-visualization system is deliberately a small, closed set of primitives recombined by context, not an ever-growing library of one-off chart types.

## Dashboard Philosophy

SENTINEL's dashboards are built as **mission control**, not as a general-purpose BI canvas. Three principles hold that idea together:

**A single-glance status strip leads every operational view.** The top of any dashboard is a row of `metric-card`s summarizing the state of the system being watched — the "bridge readout." A user should be able to tell whether everything is nominal from across the room before they read a single word of detail beneath it.

**Depth is drill-down, not clutter.** Information architecture moves from plant-level, to unit-level, to asset-level, to individual sensor — each level a deliberate navigation, never all four crammed onto one screen. Every chart and panel exists to answer a specific operational question; SENTINEL does not ship "vanity" visualizations that exist because a widget slot needed filling.

**Dashboards are role-based and opinionated, not infinitely customizable.** Rather than a blank canvas the user drags widgets onto, SENTINEL ships fixed, purpose-built templates — an Operator view, an Engineer view, an Executive view, an Investigator view — each with a defined information hierarchy suited to that role's decisions. Users can drill in and filter within a view, but the overall structure of "what this screen is for" is designed, not assembled ad hoc. This is what keeps forty engineers across a plant looking at the same instrument the same way.

## AI Design

AI in SENTINEL is deliberately invisible. What's visible is the evidence, the reasoning, the confidence, the sources, and the decision itself — the model producing them stays out of the frame. Four rules carry this principle through the product:

1. **No chat metaphor.** The `copilot-panel` docks beside the working surface rather than floating over it, and `copilot-message`s render in the same `evidence-card` / `decision-card` / plain-text language as everything else in the product. There is no avatar, no bubble, no assistant persona.
2. **Confidence is never hidden.** Every AI-derived value carries a `confidence-indicator` as a structural requirement of the component, not an optional annotation a designer might skip under deadline pressure.
3. **Every claim is sourced.** A `source-citation-chip` links each AI-authored statement back to the `evidence-card` that supports it. An unsourced AI claim is treated as a defect, not a stylistic choice.
4. **Reasoning is available on demand, never forced.** The `reasoning-disclosure` pattern keeps step-by-step reasoning one click away and collapsed by default, so the primary surface stays calm and legible while the full trace remains fully auditable.

The net effect: an engineer reading SENTINEL's output should feel like they're reading a colleague's well-documented analysis, not talking to a chatbot.

## Responsive Behavior

SENTINEL does not attempt to force every surface onto every device. Each device class is scoped to the tasks it is actually suited for.

| Device Class | Width / Context | Behavior |
|---|---|---|
| Desktop | ≥ 1440px | Full three-region shell; investigation, digital twin, and simulation canvases available at full capability; 12-column dashboard grid at 4-up metric cards |
| Laptop | 1280–1439px | Sidebar collapses to the 64px icon rail by default; dashboard grid drops to 3-up |
| Tablet | 1024–1279px | Sidebar becomes an overlay drawer rather than a persistent column; canvases remain available but toolbars condense into a single overflow menu |
| Field Tablet | 768–1023px, rugged/outdoor context | Single-pane, task-first layouts; touch targets bump to 48px minimum; a persistent offline/sync-status indicator is always visible; canvases simplify to read-only unless explicitly entering an edit task |
| Industrial Touch Display | Fixed wall/console, 32–55" | Typically a non-interactive or lightly-interactive glanceable view. Typography scales **up**, not down — `metric-value` may render at 48–64px for viewing distance — and the status strip becomes the entire screen rather than the top of a longer scroll |
| Mobile | < 768px | Deliberately scoped to notification and approval tasks — alerts, decision approvals, quick status checks — rendered as a single-card stack. The investigation canvas, digital twin canvas, and simulation panel are **not** available on mobile; they require the screen real estate the analysis genuinely needs, and SENTINEL does not pretend otherwise |

### Touch Targets
- Standard desktop/tablet minimum: 40px.
- Field Tablet and any touch-primary context: 48px minimum.
- Gloves Mode (below): 56px minimum, with increased spacing between adjacent controls.

### Collapsing Strategy
- Sidebar: persistent column → overlay drawer (tablet) → bottom navigation (mobile).
- Dashboard grid: 4-up → 3-up → 2-up → 1-up card stack.
- Data grids: sticky identifying column persists at every breakpoint; secondary columns collapse into an expandable row detail below 768px.
- Canvases (investigation, digital twin, simulation): full toolbar → condensed overflow menu (tablet) → read-only or unavailable (field tablet / mobile, respectively).

## Accessibility

SENTINEL treats accessibility as an operational requirement, not a compliance checklist — a missed alert or an unreadable gauge in a control room has real-world consequences.

- **Keyboard navigation:** every action reachable by mouse is reachable by keyboard; the `command-bar` functions as a keyboard-first launcher for any action in the system; data grids, tree views, and canvases all support arrow-key navigation between elements.
- **Screen reader support:** semantic roles on every component; new critical alerts announce via an ARIA live region immediately on arrival; every chart, graph, and heatmap ships a "View as table" fallback so no data visualization is screen-reader-inaccessible.
- **Color redundancy:** every semantic color pairing (status badges, node kinds, severity ticks) carries a second non-color signal — an icon, a shape, or a position — so the system remains fully legible under protanopia, deuteranopia, and tritanopia, and in grayscale printing.
- **High Contrast Mode:** a documented alternate token set — `{colors.canvas}` shifts to pure black, `{colors.ink}` to pure white, hairlines strengthen by one full step, and every semantic color shifts to a higher-contrast, higher-saturation variant while preserving its hue identity, so "critical is still recognizably the same red" even at higher contrast.
- **Touch targets:** 40px standard minimum, 48px on touch-primary contexts, 56px in Gloves Mode — see Responsive Behavior above.
- **Gloves Mode:** for industrial environments where operators wear protective gloves. All touch targets bump to 56px minimum, spacing between adjacent interactive elements increases to prevent mis-taps, and any interaction that depends on hover-only affordances is disabled in favor of an explicit tap-to-reveal pattern, since gloved touch has no hover state.
- **Outdoor Sunlight Mode:** a higher-luminance, higher-contrast token variant for field-tablet use in direct sunlight. Reliance on low-opacity washes (like `{colors.signal-wash}`) is reduced in favor of solid fills and thicker hairlines, since subtle opacity effects wash out entirely under direct sun.
- **Night Shift Mode:** a warmer, dimmer token variant for control rooms operating through the night. Overall luminance is capped, the signal accent shifts slightly warmer, and the system leans further into `{colors.surface-inset}`-range darkness to help protect operators' night vision — a genuine, not cosmetic, adaptation for 24-hour operational environments.

## Do's and Don'ts

### Do
- Hold every element of the system to the five-step surface ladder for depth — never introduce a shadow.
- Reserve `{colors.signal}` for general navigation and action; use the domain-semantic tokens (`evidence`, `investigation`, `knowledge`, `decision`, `prediction`, `simulation`, `twin`) for anything that carries operational meaning.
- Keep display and structural type inside the 400–650 weight range, always.
- Set every full-bleed data canvas to `{rounded.none}`; keep every piece of UI chrome inside the 2–8px range.
- Pair every semantic color with a non-color redundancy — icon, shape, or position.
- Render AI output in the same card language as human-authored content, with a visible confidence reading and at least one source citation on every claim.
- Mark every simulated or predicted element with a dashed stroke, a distinct hue, and — for full simulations — a persistent label.
- Let critical alerts persist until acknowledged; never auto-dismiss them.

### Don't
- Don't add a drop shadow anywhere. Depth is surface-lift and, on focus, glow.
- Don't use `{colors.signal}` for a consequential approve/reject action — that's `{colors.decision}`'s job.
- Don't drop type lighter than 400 or push it heavier than 650.
- Don't round a data canvas's corners, and don't square off a status dot, toggle, or avatar.
- Don't use a multi-hue "jet" colormap on any heatmap or risk visualization.
- Don't give the AI copilot an avatar, a chat bubble, or a persona name.
- Don't render simulated or predicted data with a solid fill and no label — it must always be visually distinguishable from live operational data.
- Don't build a customizable, drag-and-drop dashboard canvas; SENTINEL ships opinionated, role-based views.
- Don't rely on a spinner for loading state; use a determinate progress bar or an opacity-pulse skeleton.

## Governance & Extension

1. **Reference tokens, never inline values.** Every new component references `{colors.*}`, `{typography.*}`, `{rounded.*}`, and `{spacing.*}` tokens — a raw hex code or pixel value in a component spec is a defect, not a shortcut.
2. **A new color requires a documented meaning before it requires a hex value.** If a feature seems to need a new semantic color, the first question is what operational concept it represents — the token is named for that concept, not for its appearance.
3. **New canvases extend existing primitives before inventing new ones.** `knowledge-graph-panel` is a named variant of `investigation-canvas`, not a separate build — new analytical surfaces should look for the closest existing canvas primitive to extend before writing a new one.
4. **Variants live as sibling entries.** States like `-hover`, `-active`, `-disabled`, `-selected`, and severity variants (`-critical`, `-warning`) are documented as separate entries under the base component's name, never overloaded onto a single ambiguous token.
5. **AI-surfaced content is held to the same component contract as human-authored content.** A confidence indicator and at least one source citation are required, not optional, wherever a value is AI-derived.
6. **Every new component states which device classes it supports.** A component that cannot reasonably work on Mobile or Field Tablet says so explicitly (as the analysis canvases do) rather than shipping a degraded, confusing version everywhere.
7. **The Index Label typography (`{typography.label}`) marks every meaningful section boundary.** A new panel or card group without one reads as unanchored — it is the system's one consistent structural signature and should not be skipped.
