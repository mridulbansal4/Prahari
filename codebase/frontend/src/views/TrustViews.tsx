// Trust group: Coverage (what we do and don't check) and the read-only Audit trail.
import { useEffect, useMemo, useState } from "react";
import { EmptyState, Skeleton, ViewHeader } from "../components/ui";
import { api } from "../lib/api";
import { ensureSession } from "../lib/session";
import type { Coverage } from "../lib/types";

/* ---------- Coverage ---------- */
export function CoverageView({ coverage }: { coverage: Coverage | null }) {
  return (
    <>
      <ViewHeader
        title="What this system checks"
        helper="Being clear about the limits is part of being trustworthy. Here is exactly what is and isn't covered."
      />

      <div className="stack" style={{ gap: "var(--sp-base)", maxWidth: 840 }}>
        <div className="card card--pad-lg">
          <div className="t-label" style={{ marginBottom: "var(--sp-xs)" }}>
            What it does
          </div>
          <ul style={{ paddingLeft: "var(--sp-md)" }}>
            {[
              "Reads the documents you give it and keeps a link from every fact back to the page it came from.",
              "Answers questions by connecting records across different documents, and shows you that path.",
              "Refuses to answer when it cannot ground a claim, and tells you who to ask instead.",
              "Checks your equipment against the compliance rules it has been given, and flags what is overdue.",
              "Flags when two documents disagree, and when knowledge is at risk of being lost.",
            ].map((t) => (
              <li key={t} className="t-body" style={{ marginBottom: "var(--sp-xxs)" }}>
                {t}
              </li>
            ))}
          </ul>
        </div>

        <div className="card card--pad-lg">
          <div className="t-label" style={{ marginBottom: "var(--sp-xs)" }}>
            What it does not do
          </div>
          <ul style={{ paddingLeft: "var(--sp-md)" }}>
            {[
              "It does not check every regulation — only the clauses that have been encoded, listed below.",
              "It does not give legal or safety sign-off. It produces evidence and gaps, not a ruling.",
              "It does not know anything that isn't in the documents you have added.",
              "It does not act on your behalf. Anything it drafts still needs a person to approve it.",
            ].map((t) => (
              <li key={t} className="t-body" style={{ marginBottom: "var(--sp-xxs)" }}>
                {t}
              </li>
            ))}
          </ul>
        </div>

        {coverage ? (
          <div className="card card--pad-lg">
            <div className="t-label" style={{ marginBottom: "var(--sp-xs)" }}>
              Rules encoded right now
            </div>
            <p className="t-body" style={{ marginBottom: "var(--sp-base)" }}>
              {coverage.disclaimer}
            </p>
            <div className="stack" style={{ gap: "var(--sp-sm)" }}>
              {Object.entries(coverage.by_instrument).map(([name, v]) => {
                const pct = v.total ? Math.round((v.encoded / v.total) * 100) : 0;
                return (
                  <div key={name}>
                    <div
                      className="row"
                      style={{ justifyContent: "space-between", marginBottom: 4 }}
                    >
                      <span className="t-body-sm ink">{name}</span>
                      <span className="t-caption">
                        {v.encoded} of {v.total} rules · {pct}%
                      </span>
                    </div>
                    <div
                      style={{
                        height: 4,
                        background: "var(--hairline)",
                        borderRadius: "var(--r-pill)",
                        overflow: "hidden",
                      }}
                    >
                      <div
                        style={{
                          width: `${Math.max(pct, 1)}%`,
                          height: "100%",
                          background: "var(--ink)",
                        }}
                      />
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        ) : (
          <Skeleton height={160} />
        )}
      </div>
    </>
  );
}

/* ---------- Audit trail ---------- */
interface Entry {
  ts?: string;
  actor?: string;
  action?: string;
  target?: string;
  [k: string]: unknown;
}

export function AuditView() {
  const [entries, setEntries] = useState<Entry[] | null>(null);
  const [filter, setFilter] = useState("");

  useEffect(() => {
    ensureSession()
      .then(() => api.audit())
      .then((r) => setEntries(r.entries ?? []))
      .catch(() => setEntries([]));
  }, []);

  const shown = useMemo(() => {
    const list = entries ?? [];
    if (!filter.trim()) return list.slice(0, 200);
    const q = filter.toLowerCase();
    return list
      .filter((e) =>
        [e.action, e.actor, e.target].some((v) => String(v ?? "").toLowerCase().includes(q)),
      )
      .slice(0, 200);
  }, [entries, filter]);

  return (
    <>
      <ViewHeader
        title="Audit trail"
        helper="Every action the system recorded, in order. This log is append-only — nothing here can be edited or deleted."
      />

      <input
        className="input"
        style={{ maxWidth: 380, marginBottom: "var(--sp-base)" }}
        placeholder="Filter by action, person or target…"
        value={filter}
        onChange={(e) => setFilter(e.target.value)}
        aria-label="Filter the audit trail"
      />

      {entries === null && <Skeleton height={240} />}

      {entries?.length === 0 && (
        <EmptyState title="Nothing recorded yet" body="Actions will appear here as the system is used." />
      )}

      {shown.length > 0 && (
        <div className="card" style={{ padding: 0, overflowX: "auto" }}>
          <table style={{ width: "100%", borderCollapse: "collapse", minWidth: 560 }}>
            <thead>
              <tr>
                {["When", "Who", "What happened", "To what"].map((h) => (
                  <th
                    key={h}
                    className="t-label"
                    style={{
                      textAlign: "left",
                      padding: "var(--sp-sm) var(--sp-base)",
                      borderBottom: "1px solid var(--hairline)",
                      whiteSpace: "nowrap",
                    }}
                  >
                    {h}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {shown.map((e, i) => (
                <tr key={i}>
                  <td
                    className="t-caption"
                    style={{
                      padding: "var(--sp-sm) var(--sp-base)",
                      borderBottom: "1px solid var(--hairline)",
                      whiteSpace: "nowrap",
                    }}
                  >
                    {String(e.ts ?? "").replace("T", " ").slice(0, 19) || "—"}
                  </td>
                  <td
                    className="t-body-sm"
                    style={{
                      padding: "var(--sp-sm) var(--sp-base)",
                      borderBottom: "1px solid var(--hairline)",
                    }}
                  >
                    {String(e.actor ?? "—")}
                  </td>
                  <td
                    className="t-body-sm ink"
                    style={{
                      padding: "var(--sp-sm) var(--sp-base)",
                      borderBottom: "1px solid var(--hairline)",
                    }}
                  >
                    {String(e.action ?? "—")}
                  </td>
                  <td
                    className="t-caption"
                    style={{
                      padding: "var(--sp-sm) var(--sp-base)",
                      borderBottom: "1px solid var(--hairline)",
                      wordBreak: "break-word",
                    }}
                  >
                    {String(e.target ?? "—")}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {entries && entries.length > shown.length && (
        <p className="t-caption" style={{ marginTop: "var(--sp-xs)" }}>
          Showing the most recent {shown.length} of {entries.length} entries.
        </p>
      )}
    </>
  );
}
