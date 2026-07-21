// The CP-9 DegradedBanner (PRB §2.1) — persistent, non-dismissible below the "Full" rung.
// CP-9 must be VISIBLE to the user, not just survivable in the backend.
const COPY: Record<string, string> = {
  full: "",
  "-model": "Answers are structured, not narrated — the reasoning model is unavailable.",
  "-vector": "Semantic search is unavailable — showing graph-linked results only.",
  "-graph": "Showing cached answers and document search only.",
  "-everything": "Live reasoning is unavailable — showing who to ask.",
};

export function DegradedBanner({ rung }: { rung: string }) {
  if (!rung || rung === "full") return null;
  return (
    <div
      role="status"
      style={{
        background: "var(--surface-2)",
        borderBottom: "1px solid var(--warning-dim)",
        borderLeft: "3px solid var(--warning)",
        padding: "var(--sp-sm) var(--sp-lg)",
        display: "flex",
        gap: "var(--sp-md)",
        alignItems: "center",
      }}
    >
      <span className="t-label" style={{ color: "var(--warning)" }}>
        Degraded · {rung}
      </span>
      <span className="t-body-sm ink-muted">{COPY[rung] ?? "Operating on a lower rung."}</span>
    </div>
  );
}
