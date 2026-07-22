// Shared primitives for the single-page app. Every value comes from tokens.css.
import type { CSSProperties, ReactNode } from "react";
import type { ConfidenceState } from "../lib/types";

/* ---------- Atmospheric gradient orb ----------
 * Decoration only: a soft radial bloom behind copy. Never a button fill, text colour,
 * or card background. */
export function Orb({
  color,
  size = 420,
  style,
}: {
  color: "mint" | "peach" | "lavender" | "sky" | "rose";
  size?: number;
  style?: CSSProperties;
}) {
  return (
    <div
      aria-hidden="true"
      className="orb orb--drift"
      style={{
        width: size,
        height: size,
        background: `radial-gradient(circle, var(--gradient-${color}) 0%, transparent 70%)`,
        ...style,
      }}
    />
  );
}

/* ---------- Section wrapper ----------
 * Every section carries a plain-language title and a one-line "what this does" helper
 * directly beneath it — the layman-clarity requirement, enforced structurally. */
export function Section({
  id,
  label,
  title,
  help,
  children,
  soft,
  action,
}: {
  id: string;
  label: string;
  title: string;
  help: string;
  children: ReactNode;
  soft?: boolean;
  action?: ReactNode;
}) {
  return (
    <section id={id} className={`section${soft ? " section--soft" : ""}`}>
      <div className="container">
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "flex-end",
            gap: "var(--sp-lg)",
            flexWrap: "wrap",
            marginBottom: "var(--sp-xl)",
          }}
        >
          <div style={{ maxWidth: 640 }}>
            <div className="t-label" style={{ marginBottom: "var(--sp-sm)" }}>
              {label}
            </div>
            <h2 className="page-title">{title}</h2>
            <p className="t-body" style={{ marginTop: "var(--sp-sm)", color: "var(--body)" }}>
              {help}
            </p>
          </div>
          {action}
        </div>
        {children}
      </div>
    </section>
  );
}

/* ---------- View header ----------
 * Every view leads with a display headline and a one-line plain-language helper. */
export function ViewHeader({
  title,
  helper,
  action,
}: {
  title: string;
  helper: string;
  action?: ReactNode;
}) {
  return (
    <div
      style={{
        display: "flex",
        justifyContent: "space-between",
        alignItems: "flex-end",
        gap: "var(--sp-lg)",
        flexWrap: "wrap",
        marginBottom: "var(--sp-xl)",
      }}
    >
      <div style={{ maxWidth: 680 }}>
        <h1 className="page-title">{title}</h1>
        <p className="t-body" style={{ marginTop: "var(--sp-xs)" }}>
          {helper}
        </p>
      </div>
      {action}
    </div>
  );
}

/* ---------- Degradation notice ----------
 * The backend drops to lower capability rungs and says so. Surfaced calmly and honestly —
 * never hidden, never a red alarm. */
const RUNG_COPY: Record<string, string> = {
  "-model": "Answers are structured rather than written out — the reasoning model is unavailable.",
  "-vector": "Semantic search is unavailable, so this used graph-linked results only.",
  "-graph": "The knowledge graph is unavailable, so this used cached answers and document search.",
  "-everything": "Live reasoning is unavailable — showing who to ask instead.",
};

export function DegradationNotice({ rung }: { rung: string }) {
  if (!rung || rung === "full") return null;
  return (
    <div
      role="status"
      style={{
        display: "flex",
        gap: "var(--sp-xs)",
        padding: "var(--sp-sm) var(--sp-base)",
        borderRadius: "var(--r-md)",
        border: "1px solid var(--hairline-strong)",
        background: "var(--surface-strong)",
        marginBottom: "var(--sp-base)",
      }}
    >
      <span aria-hidden="true" className="t-body-sm">
        ◐
      </span>
      <span>
        <span className="t-body-strong" style={{ display: "block" }}>
          Running at reduced capability
        </span>
        <span className="t-body-sm">
          {RUNG_COPY[rung] ?? "Some capabilities are unavailable right now."} Answers are still
          cited, and it will still refuse rather than guess.
        </span>
      </span>
    </div>
  );
}

/* ---------- Empty states ----------
 * Never a blank box: always says what goes here and offers the next action. */
export function EmptyState({
  title,
  body,
  children,
}: {
  title: string;
  body: string;
  children?: ReactNode;
}) {
  return (
    <div
      className="card"
      style={{
        textAlign: "center",
        padding: "var(--sp-xxl) var(--sp-lg)",
        borderStyle: "dashed",
        borderColor: "var(--hairline-strong)",
        background: "var(--canvas-soft)",
      }}
    >
      <div className="t-display-sm" style={{ marginBottom: "var(--sp-xs)" }}>
        {title}
      </div>
      <p className="t-body" style={{ maxWidth: 480, margin: "0 auto var(--sp-lg)" }}>
        {body}
      </p>
      {children}
    </div>
  );
}

export function Badge({
  children,
  tone = "neutral",
}: {
  children: ReactNode;
  tone?: "neutral" | "success" | "error";
}) {
  const color =
    tone === "success" ? "var(--success)" : tone === "error" ? "var(--error)" : "var(--ink)";
  return (
    <span className="badge" style={{ color }}>
      {/* Shape + text carry the meaning; colour is only ever a third signal. */}
      {tone !== "neutral" && (
        <span
          aria-hidden="true"
          style={{
            width: 6,
            height: 6,
            borderRadius: "var(--r-full)",
            background: color,
            display: "inline-block",
          }}
        />
      )}
      {children}
    </span>
  );
}

export function Chip({ children, onClick }: { children: ReactNode; onClick: () => void }) {
  return (
    <button type="button" className="chip" onClick={onClick}>
      {children}
    </button>
  );
}

export function Skeleton({ height = 16, width = "100%" }: { height?: number; width?: number | string }) {
  return <div className="skeleton" style={{ height, width }} />;
}

/* ---------- Confidence ----------
 * Structural, never optional, and never conveyed by colour alone: the text label is
 * always present alongside the segments. */
const CONFIDENCE: Record<ConfidenceState, { label: string; filled: number }> = {
  grounded: { label: "Backed by your documents", filled: 3 },
  inferred: { label: "Reasoned, partly inferred", filled: 2 },
  unsupported: { label: "Not supported by a source", filled: 1 },
  abstained: { label: "Not answered", filled: 0 },
};

export function Confidence({ state, source }: { state: ConfidenceState; source?: string }) {
  const { label, filled } = CONFIDENCE[state] ?? CONFIDENCE.inferred;
  return (
    <span
      className="row"
      style={{ gap: "var(--sp-xs)", flexShrink: 0 }}
      title={source ? `${source} — ${label}` : `Confidence: ${label}`}
    >
      <span aria-hidden="true" className="row" style={{ gap: 3 }}>
        {[0, 1, 2].map((i) => (
          <span
            key={i}
            style={{
              width: 14,
              height: 3,
              borderRadius: "var(--r-pill)",
              background: i < filled ? "var(--ink)" : "var(--hairline-strong)",
            }}
          />
        ))}
      </span>
      <span className="t-caption" style={{ color: "var(--muted)" }}>
        {/* The source document that backs this claim, named ahead of the confidence label. */}
        {source && (
          <span className="ink" style={{ fontWeight: 500 }}>
            {source}
          </span>
        )}
        {source ? " · " : ""}
        {label}
      </span>
    </span>
  );
}

/* ---------- Loading ----------
 * A calm determinate-feeling bar and a named stage, never a clashing spinner. */
export function LoadingBar({ stage }: { stage?: string }) {
  return (
    <div className="stack" style={{ gap: "var(--sp-sm)" }}>
      <div className="progress" />
      <span className="t-caption">{stage ?? "Working…"}</span>
    </div>
  );
}

export function Notice({
  tone,
  children,
}: {
  tone: "success" | "error";
  children: ReactNode;
}) {
  const color = tone === "success" ? "var(--success)" : "var(--error)";
  return (
    <div
      role="status"
      className="row"
      style={{
        gap: "var(--sp-xs)",
        padding: "var(--sp-sm) var(--sp-base)",
        borderRadius: "var(--r-md)",
        border: `1px solid ${color}`,
        background: "var(--surface-card)",
        color: "var(--ink)",
        font: "var(--t-body-sm)",
      }}
    >
      <span aria-hidden="true" style={{ color }}>
        {tone === "success" ? "✓" : "!"}
      </span>
      {children}
    </div>
  );
}
