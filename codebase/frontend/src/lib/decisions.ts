// Decision memory — data layer.
//
// Everything here is derived from what `/v1/decisions` and `/v1/decisions/{id}/replay`
// actually return. Where the design calls for a field the backend does not expose, this file
// records the absence in `MISSING_FROM_API` instead of inventing a value — a fabricated
// "Applied" badge or a made-up confidence would be exactly the kind of unsupported claim the
// rest of the product refuses to make.
import { api } from "./api";
import { ensureSession } from "./session";
import type { Citation } from "./types";

/** A step of the recorded reasoning chain, exactly as the replay endpoint returns it. */
export interface ReplayStep {
  id: string;
  kind: string; // Observation | Hypothesis | Evidence | Decision | Alternative | RiskAccepted | Outcome | LessonLearned
  title: string;
  detail: string;
  citations: { doc_id: string; page: number | null; span_id: string }[];
  order: number;
}

export interface DecisionSummary {
  decision_id: string;
  title: string;
  date: string;
  asset_id: string;
  /** Resolved from /v1/assets — the list endpoint returns only the opaque asset_id. */
  asset_tag?: string;
}

export interface Replay {
  decision_id: string;
  title: string;
  steps: ReplayStep[];
}

/** The reasoning chain, sorted into the roles the replay view presents. */
export interface ReplayShape {
  observation?: ReplayStep;
  hypothesis?: ReplayStep;
  decision?: ReplayStep;
  /** Rejected options. `detail` carries the rejection rationale when the backend recorded one. */
  alternatives: ReplayStep[];
  /** Any step that cites a source — the evidence trail. */
  evidence: ReplayStep[];
  riskAccepted?: ReplayStep;
  outcome?: ReplayStep;
  lesson?: ReplayStep;
  /** Steps in recorded order, for the graph path. */
  ordered: ReplayStep[];
}

/**
 * Fields the design asks for that the API does not return. Surfaced in the UI as an honest
 * note rather than filled with plausible-looking defaults.
 */
export const MISSING_FROM_API = {
  list: [
    "decision-maker type (Operator decision / System recommendation)",
    "confidence",
    "status (Applied / Overridden)",
    "originating investigation or alert (the trigger)",
    "chosen-vs-rejected summary (only the per-decision replay carries options)",
  ],
  replay: [
    "date and asset on the replay payload (carried over from the list instead)",
    "citation excerpt text — citations resolve to doc · page · span only",
    "known-then-vs-now / whether the decision still holds",
  ],
} as const;

export function shapeReplay(replay: Replay): ReplayShape {
  const ordered = [...replay.steps].sort((a, b) => a.order - b.order);
  const byKind = (k: string) => ordered.find((s) => s.kind === k);
  return {
    observation: byKind("Observation"),
    hypothesis: byKind("Hypothesis"),
    decision: byKind("Decision"),
    alternatives: ordered.filter((s) => s.kind === "Alternative"),
    evidence: ordered.filter((s) => s.citations.length > 0),
    riskAccepted: byKind("RiskAccepted"),
    outcome: byKind("Outcome"),
    lesson: byKind("LessonLearned"),
    ordered,
  };
}

/** Replay citations carry no excerpt; adapt to the shared Citation shape with excerpt null. */
export function toCitations(step: ReplayStep): Citation[] {
  return step.citations.map((c) => ({
    doc_id: c.doc_id,
    page: c.page,
    span_id: c.span_id,
    excerpt: null,
  }));
}

export async function loadDecisions(): Promise<DecisionSummary[]> {
  await ensureSession();
  const [list, assets] = await Promise.all([
    api.decisions(),
    api.assets().catch(() => ({ assets: [] as { id: string; tag: string }[] })),
  ]);
  const tagById = new Map(assets.assets.map((a) => [a.id, a.tag]));
  return (list.decisions ?? []).map((d: DecisionSummary) => ({
    ...d,
    asset_tag: tagById.get(d.asset_id),
  }));
}

export async function loadReplay(id: string): Promise<Replay> {
  await ensureSession();
  return (await api.replay(id)) as Replay;
}
