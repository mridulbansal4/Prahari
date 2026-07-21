// Alerts — the differentiator. What the system found without being asked.
import { useState } from "react";
import { Badge, EmptyState, Skeleton, ViewHeader } from "../components/ui";
import {
  loadTriage,
  saveTriage,
  type Alert,
  type AlertKind,
  type TriageState,
} from "../lib/alerts";
import type { Coverage } from "../lib/types";

const KIND_COPY: Record<AlertKind, { badge: string; tone: "error" | "neutral" }> = {
  overdue: { badge: "Overdue", tone: "error" },
  contradiction: { badge: "Conflict", tone: "error" },
  due: { badge: "Coming due", tone: "neutral" },
  knowledge: { badge: "At risk", tone: "neutral" },
};

function AlertCard({
  alert,
  triage,
  onTriage,
  onAsk,
}: {
  alert: Alert;
  triage?: TriageState;
  onTriage: (s: TriageState | null) => void;
  onAsk: (q: string) => void;
}) {
  const [open, setOpen] = useState(false);
  const copy = KIND_COPY[alert.kind];
  const muted = triage === "snoozed" || triage === "reviewed";

  return (
    <div className="card card--hover" style={{ opacity: muted ? 0.6 : 1 }}>
      <div
        className="row"
        style={{ justifyContent: "space-between", gap: "var(--sp-xs)", flexWrap: "wrap" }}
      >
        <h3 className="t-title-md">{alert.title}</h3>
        <div className="row" style={{ gap: "var(--sp-xxs)" }}>
          {triage && <Badge>{triage}</Badge>}
          <Badge tone={copy.tone}>{copy.badge}</Badge>
        </div>
      </div>

      <p className="t-body-sm" style={{ marginTop: "var(--sp-xs)" }}>
        {alert.detail}
      </p>

      {/* Contradictions show the two sides next to each other — that is the whole point. */}
      {alert.conflict && (
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "1fr auto 1fr",
            gap: "var(--sp-xs)",
            alignItems: "center",
            marginTop: "var(--sp-sm)",
          }}
        >
          <div
            style={{
              padding: "var(--sp-xs) var(--sp-sm)",
              background: "var(--canvas-soft)",
              border: "1px solid var(--hairline)",
              borderRadius: "var(--r-md)",
            }}
          >
            <div className="t-label">Source A</div>
            <div className="t-body-sm ink" style={{ wordBreak: "break-word" }}>
              {alert.conflict.left}
            </div>
          </div>
          <span aria-hidden="true" className="t-caption">
            vs
          </span>
          <div
            style={{
              padding: "var(--sp-xs) var(--sp-sm)",
              background: "var(--canvas-soft)",
              border: "1px solid var(--hairline)",
              borderRadius: "var(--r-md)",
            }}
          >
            <div className="t-label">Source B</div>
            <div className="t-body-sm ink" style={{ wordBreak: "break-word" }}>
              {alert.conflict.right}
            </div>
          </div>
        </div>
      )}

      <div
        className="row"
        style={{
          justifyContent: "space-between",
          marginTop: "var(--sp-base)",
          gap: "var(--sp-xs)",
          flexWrap: "wrap",
        }}
      >
        <span className="t-caption">{alert.involves}</span>
        <button type="button" className="btn btn--text" onClick={() => setOpen((v) => !v)}>
          {open ? "Hide details" : "View details"}
        </button>
      </div>

      {open && (
        <div
          style={{
            marginTop: "var(--sp-sm)",
            paddingTop: "var(--sp-sm)",
            borderTop: "1px solid var(--hairline)",
          }}
        >
          <div className="t-label" style={{ marginBottom: "var(--sp-xxs)" }}>
            What this involves
          </div>
          <p className="t-body-sm">
            {alert.assetTag ? `Equipment: ${alert.assetTag}. ` : ""}
            {alert.source
              ? `Most recent supporting document: ${alert.source}.`
              : "No supporting document has been found for this yet."}
          </p>

          <div className="row" style={{ gap: "var(--sp-xs)", marginTop: "var(--sp-sm)", flexWrap: "wrap" }}>
            <button
              type="button"
              className="btn btn--outline"
              style={{ minHeight: 34 }}
              onClick={() =>
                onAsk(
                  alert.assetTag
                    ? `What should I know about ${alert.assetTag}?`
                    : `Tell me about ${alert.involves}`,
                )
              }
            >
              Ask about this
            </button>
            <button
              type="button"
              className="btn btn--text"
              onClick={() => onTriage(triage === "reviewed" ? null : "reviewed")}
            >
              {triage === "reviewed" ? "Undo reviewed" : "Mark reviewed"}
            </button>
            <button
              type="button"
              className="btn btn--text"
              onClick={() => onTriage(triage === "snoozed" ? null : "snoozed")}
            >
              {triage === "snoozed" ? "Un-snooze" : "Snooze"}
            </button>
            <button type="button" className="btn btn--text" onClick={() => onTriage("dismissed")}>
              Dismiss
            </button>
          </div>
          <p className="t-caption" style={{ marginTop: "var(--sp-xs)" }}>
            Triage is saved in this browser only — it is not shared with your team yet.
          </p>
        </div>
      )}
    </div>
  );
}

export function AlertsView({
  alerts,
  coverage,
  loading,
  onAsk,
}: {
  alerts: Alert[];
  coverage: Coverage | null;
  loading: boolean;
  onAsk: (q: string) => void;
}) {
  const [triage, setTriage] = useState<Record<string, TriageState>>(() => loadTriage());
  const [showDismissed, setShowDismissed] = useState(false);

  function setOne(id: string, s: TriageState | null) {
    setTriage((prev) => {
      const next = { ...prev };
      if (s === null) delete next[id];
      else next[id] = s;
      saveTriage(next);
      return next;
    });
  }

  const dismissed = alerts.filter((a) => triage[a.id] === "dismissed");
  const visible = alerts.filter((a) => triage[a.id] !== "dismissed");

  return (
    <>
      <ViewHeader
        title="What the system noticed on its own"
        helper="Nobody asked for these. They surfaced while reading your documents — missed checks, documents that disagree, and knowledge about to walk out the door."
      />

      {loading && (
        <div className="alert-grid" style={{ display: "grid", gap: "var(--sp-base)" }}>
          <Skeleton height={150} />
          <Skeleton height={150} />
          <Skeleton height={150} />
        </div>
      )}

      {!loading && visible.length === 0 && (
        <EmptyState
          title={dismissed.length ? "Everything here is dismissed" : "Nothing flagged right now"}
          body={
            dismissed.length
              ? "You've dismissed every current finding. You can bring them back below."
              : "When the system spots a missed inspection, a conflict between two documents, or knowledge at risk of being lost, it will appear here."
          }
        />
      )}

      {!loading && visible.length > 0 && (
        <div className="alert-grid" style={{ display: "grid", gap: "var(--sp-base)" }}>
          {visible.map((a) => (
            <AlertCard
              key={a.id}
              alert={a}
              triage={triage[a.id]}
              onTriage={(s) => setOne(a.id, s)}
              onAsk={onAsk}
            />
          ))}
        </div>
      )}

      {dismissed.length > 0 && (
        <div style={{ marginTop: "var(--sp-lg)" }}>
          <button
            type="button"
            className="btn btn--text"
            onClick={() => setShowDismissed((v) => !v)}
          >
            {showDismissed ? "Hide" : "Show"} {dismissed.length} dismissed
          </button>
          {showDismissed && (
            <div
              className="alert-grid"
              style={{ display: "grid", gap: "var(--sp-base)", marginTop: "var(--sp-sm)" }}
            >
              {dismissed.map((a) => (
                <AlertCard
                  key={a.id}
                  alert={a}
                  triage={triage[a.id]}
                  onTriage={(s) => setOne(a.id, s)}
                  onAsk={onAsk}
                />
              ))}
            </div>
          )}
        </div>
      )}

      {/* Permanent, non-collapsible. The system must never imply it checks more than it encodes. */}
      {coverage && (
        <div
          style={{
            marginTop: "var(--sp-xl)",
            paddingTop: "var(--sp-base)",
            borderTop: "1px solid var(--hairline)",
          }}
        >
          <div className="t-label" style={{ marginBottom: "var(--sp-xxs)" }}>
            What this covers
          </div>
          <p className="t-body-sm" style={{ maxWidth: 720 }}>
            {coverage.disclaimer}
          </p>
          <p className="t-caption" style={{ marginTop: "var(--sp-xxs)" }}>
            {Object.entries(coverage.by_instrument)
              .map(([name, v]) => `${name}: ${v.encoded} of ${v.total} rules checked`)
              .join(" · ")}
          </p>
        </div>
      )}
    </>
  );
}
