// Small design-system primitives. Every visual value comes from a token (ui_rules #1).
import type { ReactNode } from "react";
import type { ConfidenceState } from "../lib/types";

/** A metric reading. design.md's 36px metric-value numeral is for NUMBERS; a long string value
 * (e.g. "immediate (same session)") must not render at that size or it overflows. Numbers →
 * large tabular numeral; short/long text → contained title style that wraps cleanly. */
export function MetricValue({ value, accent }: { value: ReactNode; accent?: string }) {
  const s = value === null || value === undefined ? "—" : String(value);
  const isNumeric = /^[\d.,%+\-/x ]{1,8}$/.test(s.trim());
  return (
    <div
      className={isNumeric ? "t-metric" : "t-title"}
      style={{ color: accent ?? "var(--ink)", overflowWrap: "anywhere", lineHeight: isNumeric ? 1.05 : 1.25 }}
    >
      {s}
    </div>
  );
}

const CONF_LABEL: Record<ConfidenceState, string> = {
  grounded: "Grounded",
  inferred: "Inferred",
  unsupported: "Unsupported",
  abstained: "Abstained",
};
const CONF_VAR: Record<ConfidenceState, string> = {
  grounded: "var(--grounded)",
  inferred: "var(--inferred)",
  unsupported: "var(--unsupported)",
  abstained: "var(--abstain)",
};

/** Confidence is never colour-only — always a label too (NFR-10). */
export function ConfidenceIndicator({ state }: { state: ConfidenceState }) {
  const filled = { grounded: 5, inferred: 3, unsupported: 1, abstained: 0 }[state];
  return (
    <span className="confidence" title={`Confidence: ${CONF_LABEL[state]}`}>
      <span className="segs">
        {[0, 1, 2, 3, 4].map((i) => (
          <span
            key={i}
            className={`seg${i < filled ? " on" : ""}`}
            style={i < filled ? { background: CONF_VAR[state] } : undefined}
          />
        ))}
      </span>
      <span className="t-metadata" style={{ color: CONF_VAR[state] }}>
        {CONF_LABEL[state]}
      </span>
    </span>
  );
}

/** The persistent confidence legend (Global Shell, PRB §2.1). */
export function ConfidenceLegend() {
  const states: ConfidenceState[] = ["grounded", "inferred", "unsupported", "abstained"];
  return (
    <div className="row" style={{ gap: "var(--sp-md)", alignItems: "center", flexWrap: "wrap" }}>
      <span className="t-label">Confidence</span>
      {states.map((s) => (
        <span key={s} className="row center" style={{ gap: "var(--sp-xs)" }}>
          <span
            className="badge .dot"
            style={{
              width: 8,
              height: 8,
              borderRadius: "var(--r-full)",
              background: CONF_VAR[s],
              display: "inline-block",
            }}
          />
          <span className="t-metadata">{CONF_LABEL[s]}</span>
        </span>
      ))}
    </div>
  );
}

export function CitationChip({ n, onClick }: { n: number; onClick?: () => void }) {
  return (
    <button className="citation-chip" onClick={onClick} title="Open source span">
      [{n}]
    </button>
  );
}

export function Badge({
  children,
  kind,
}: {
  children: React.ReactNode;
  kind?: "success" | "warning" | "critical" | "offline";
}) {
  return (
    <span className={`badge${kind ? ` badge-${kind}` : ""}`}>
      <span className="dot" />
      {children}
    </span>
  );
}

export function Skeleton({ h = 16, w = "100%" }: { h?: number; w?: number | string }) {
  return <div className="skeleton" style={{ height: h, width: w }} />;
}

/** Named per-agent-stage loading — honest, never a generic spinner (PRB §2.2). */
export function StageIndicator({ stage, detail }: { stage: string; detail?: string }) {
  const stages = ["Planner", "Retriever", "Executor", "Critic", "Verifier"];
  const idx = stages.indexOf(stage);
  const pct = idx >= 0 ? ((idx + 1) / stages.length) * 100 : 20;
  return (
    <div className="col" style={{ gap: "var(--sp-sm)" }}>
      <div className="row between center">
        <span className="t-label" style={{ color: "var(--signal)" }}>
          {stage}
        </span>
        <span className="t-metadata">{detail}</span>
      </div>
      <div className="progress">
        <span style={{ width: `${pct}%` }} />
      </div>
      <div className="row" style={{ gap: "var(--sp-xs)" }}>
        {stages.map((s, i) => (
          <span
            key={s}
            className="t-metadata"
            style={{ color: i <= idx ? "var(--ink)" : "var(--ink-faint)" }}
          >
            {s}
            {i < stages.length - 1 ? " ›" : ""}
          </span>
        ))}
      </div>
    </div>
  );
}
