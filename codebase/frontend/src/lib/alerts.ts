// Proactive insights — the things the system found on its own, merged from existing backend
// sources. No new endpoints; no change to any data contract.
//
//   compliance rows  -> overdue / due statutory obligations        (M6)
//   knowledge health -> contradictions, expert departure, drift    (M4)
//
// Contradictions are real, not decorative: backend `knowledge/decay.py` raises a flag with
// trigger "contradiction" for every CONTRADICTS edge between two spans. If the corpus holds
// no contradicting evidence, none appear — we never synthesise one.
import { api } from "./api";
import { ensureSession } from "./session";
import type { Coverage } from "./types";

export type AlertKind = "overdue" | "due" | "contradiction" | "knowledge";

export interface Alert {
  id: string;
  kind: AlertKind;
  title: string;
  detail: string;
  involves: string;
  assetTag?: string;
  assetId?: string;
  source?: string;
  /** For contradictions: the two things that disagree, shown side by side. */
  conflict?: { left: string; right: string };
  trigger?: string;
}

export interface AlertsPayload {
  alerts: Alert[];
  coverage: Coverage | null;
}

const KIND_RANK: Record<AlertKind, number> = {
  overdue: 0,
  contradiction: 1,
  knowledge: 2,
  due: 3,
};

const TRIGGER_TITLE: Record<string, string> = {
  expert_departure: "Knowledge at risk of being lost",
  vendor_change: "A vendor change may have made facts stale",
  sop_change: "A procedure change may have made facts stale",
  equipment_change: "An equipment change may have made facts stale",
};

export async function loadAlerts(): Promise<AlertsPayload> {
  await ensureSession();

  const [{ assets }, health] = await Promise.all([
    api.assets(),
    api.knowledgeHealth().catch(() => ({ flags: [] as any[], last_run: null })),
  ]);

  const alerts: Alert[] = [];
  let coverage: Coverage | null = null;

  // Compliance is per-asset, so fan out across the register and merge.
  // NOTE: this is N+1 by necessity — there is no bulk compliance endpoint. Fine at three
  // assets; a `GET /v1/compliance` returning all rows would be the fix at plant scale.
  const perAsset = await Promise.all(
    assets.map((a) =>
      api
        .compliance(a.id)
        .then((r) => ({ asset: a, ...r }))
        .catch(() => null),
    ),
  );

  for (const entry of perAsset) {
    if (!entry) continue;
    coverage ??= entry.coverage;
    for (const row of entry.rows) {
      if (row.status !== "overdue" && row.status !== "due") continue;
      alerts.push({
        id: `${row.asset_id}-${row.clause}`,
        kind: row.status,
        title:
          row.status === "overdue"
            ? `Overdue inspection on ${row.asset_tag}`
            : `Inspection coming due on ${row.asset_tag}`,
        detail:
          `${row.instrument} clause ${row.clause} expects a check every ` +
          `${row.periodicity_months} months. ` +
          (row.last_evidence_date
            ? `The last record on file is dated ${row.last_evidence_date}.`
            : `No record of this check has been found in your documents.`),
        involves: `${row.asset_tag} · ${row.instrument} ${row.clause}`,
        assetTag: row.asset_tag,
        assetId: row.asset_id,
        source: row.last_evidence_doc ?? undefined,
      });
    }
  }

  for (const flag of health.flags ?? []) {
    if (flag.resolved) continue;
    const trigger = String(flag.trigger ?? "");
    const isConflict = trigger === "contradiction";
    const description = String(flag.description ?? "");

    // The backend phrases contradictions as "Contradictory evidence between X and Y."
    const pair = description.match(/between (\S+) and (\S+)/i);

    alerts.push({
      id: String(flag.flag_id),
      kind: isConflict ? "contradiction" : "knowledge",
      title: isConflict
        ? "Two documents disagree"
        : (TRIGGER_TITLE[trigger] ?? "Knowledge at risk"),
      detail: description,
      involves: String(flag.affected_fact_ref ?? ""),
      trigger,
      conflict:
        isConflict && pair ? { left: pair[1].replace(/\.$/, ""), right: pair[2].replace(/\.$/, "") } : undefined,
    });
  }

  alerts.sort((a, b) => KIND_RANK[a.kind] - KIND_RANK[b.kind]);
  return { alerts, coverage };
}

/* ---------- Triage ----------
 * Local-only. There is no backend endpoint to persist a dismissal or a snooze, so this lives
 * in localStorage and is scoped to this browser. FLAGGED: making triage real needs a server
 * change (something like POST /v1/alerts/{id}/status). We do not fake it as if it synced. */
const TRIAGE_KEY = "prahari.alert-triage";
export type TriageState = "reviewed" | "snoozed" | "dismissed";

export function loadTriage(): Record<string, TriageState> {
  try {
    return JSON.parse(localStorage.getItem(TRIAGE_KEY) ?? "{}");
  } catch {
    return {};
  }
}

export function saveTriage(map: Record<string, TriageState>): void {
  try {
    localStorage.setItem(TRIAGE_KEY, JSON.stringify(map));
  } catch {
    /* storage unavailable — triage simply won't persist */
  }
}
