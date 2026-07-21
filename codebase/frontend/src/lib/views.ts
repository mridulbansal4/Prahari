// The workspace's information architecture, in one place.
//
// Order encodes the mental model: ask -> understand your plant -> its memory -> trust it.
// Labels are plain language only: no module codes (M5), no engineering names.

export type ViewId =
  | "ask"
  | "past"
  | "documents"
  | "alerts"
  | "map"
  | "assets"
  | "expert"
  | "decisions"
  | "audit"
  | "coverage"
  | "field";

export type GroupId = "ASK" | "YOUR PLANT" | "MEMORY" | "TRUST";

export interface ViewDef {
  id: ViewId;
  group: GroupId;
  label: string;
  /** One-line "what this does", shown as the sidebar helper and the view subtitle. */
  helper: string;
  /** Display headline for the main area. */
  title: string;
  /** Single glyph for the collapsed icon rail. Shape, never colour. */
  glyph: string;
}

export const GROUPS: GroupId[] = ["ASK", "YOUR PLANT", "MEMORY", "TRUST"];

export const VIEWS: ViewDef[] = [
  {
    id: "ask",
    group: "ASK",
    label: "Ask a question",
    helper: "Ask anything about your documents and get a cited answer.",
    title: "Ask about your documents",
    glyph: "◆",
  },
  {
    id: "past",
    group: "ASK",
    label: "Past answers",
    helper: "Revisit and compare every question already asked here.",
    title: "Past answers",
    glyph: "◷",
  },
  {
    id: "documents",
    group: "YOUR PLANT",
    label: "Documents",
    helper: "Everything the system has read, and where to add more.",
    title: "Your documents",
    glyph: "▤",
  },
  {
    id: "alerts",
    group: "YOUR PLANT",
    label: "Alerts",
    helper: "What the system noticed on its own, without being asked.",
    title: "What the system noticed on its own",
    glyph: "▲",
  },
  {
    id: "map",
    group: "YOUR PLANT",
    label: "Knowledge map",
    helper: "How your equipment, documents and records connect.",
    title: "How everything connects",
    glyph: "❋",
  },
  {
    id: "assets",
    group: "YOUR PLANT",
    label: "Asset map",
    helper: "Every name for a piece of equipment, resolved to one thing.",
    title: "One piece of equipment, many names",
    glyph: "◎",
  },
  {
    id: "expert",
    group: "MEMORY",
    label: "Expert knowledge",
    helper: "What your most experienced people know that isn't written down.",
    title: "Expert knowledge",
    glyph: "✦",
  },
  {
    id: "decisions",
    group: "MEMORY",
    label: "Decisions & replay",
    helper: "Past decisions, and the reasoning behind them.",
    title: "Decisions & replay",
    glyph: "⟲",
  },
  {
    id: "audit",
    group: "TRUST",
    label: "Audit trail",
    helper: "Every action recorded. Nothing edits or deletes.",
    title: "Audit trail",
    glyph: "≡",
  },
  {
    id: "coverage",
    group: "TRUST",
    label: "Coverage",
    helper: "Exactly what this system checks — and what it does not.",
    title: "What this system checks",
    glyph: "◐",
  },
];

/** Field mode sits outside the groups, pinned to the foot of the sidebar. */
export const FIELD_VIEW: ViewDef = {
  id: "field",
  group: "TRUST",
  label: "Field mode",
  helper: "One big question box for a phone, on the plant floor.",
  title: "Field mode",
  glyph: "◍",
};

export function viewById(id: ViewId): ViewDef {
  return id === "field" ? FIELD_VIEW : (VIEWS.find((v) => v.id === id) ?? VIEWS[0]);
}
