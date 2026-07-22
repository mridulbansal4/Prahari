// A clean, organised reading view of a document's content.
//
// Renders the format it actually is: markdown with its headings and tables intact, CSV as a
// real table, JSON pretty-printed. A second tab shows the extracted passages — the citable
// units the system reasons over — so you can see exactly what a citation points at.
import { useState } from "react";
import type { DocumentContent as Content } from "../lib/types";
import { Badge } from "./ui";
import { Markdown } from "./Markdown";

function CsvTable({ text }: { text: string }) {
  const rows = text
    .replace(/\r\n/g, "\n")
    .split("\n")
    .filter((r) => r.trim())
    .map((r) => r.split(","));
  if (!rows.length) return null;
  const [head, ...body] = rows;
  return (
    <div style={{ overflowX: "auto" }}>
      <table style={{ width: "100%", borderCollapse: "collapse", minWidth: 480 }}>
        <thead>
          <tr>
            {head.map((c, i) => (
              <th
                key={i}
                style={{
                  textAlign: "left",
                  padding: "8px 12px",
                  borderBottom: "1px solid var(--hairline-strong)",
                  font: "var(--t-label)",
                  letterSpacing: "var(--ls-label)",
                  textTransform: "uppercase",
                  color: "var(--muted)",
                  whiteSpace: "nowrap",
                }}
              >
                {c.trim()}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {body.map((r, ri) => (
            <tr key={ri}>
              {head.map((_, ci) => (
                <td
                  key={ci}
                  className="t-body-sm"
                  style={{ padding: "8px 12px", borderBottom: "1px solid var(--hairline)", verticalAlign: "top" }}
                >
                  {(r[ci] ?? "").trim()}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function Reading({ content }: { content: Content }) {
  if (content.format === "csv") return <CsvTable text={content.text} />;
  if (content.format === "markdown") return <Markdown text={content.text} />;
  return (
    <pre
      className="t-body-sm"
      style={{
        whiteSpace: "pre-wrap",
        wordBreak: "break-word",
        fontFamily: content.format === "json" ? "ui-monospace, monospace" : "inherit",
        lineHeight: 1.6,
        margin: 0,
      }}
    >
      {content.text}
    </pre>
  );
}

export function DocumentContentView({ content }: { content: Content }) {
  const [tab, setTab] = useState<"reading" | "passages">("reading");

  return (
    <div>
      <div className="row" style={{ gap: "var(--sp-xxs)", marginBottom: "var(--sp-base)" }}>
        {(
          [
            { id: "reading" as const, label: "Reading view" },
            { id: "passages" as const, label: `Extracted passages · ${content.passage_count}` },
          ]
        ).map((t) => (
          <button
            key={t.id}
            type="button"
            onClick={() => setTab(t.id)}
            aria-pressed={tab === t.id}
            className={tab === t.id ? "btn btn--primary" : "btn btn--outline"}
            style={{ minHeight: 34, padding: "0 16px" }}
          >
            {t.label}
          </button>
        ))}
        {content.source === "parsed" && (
          <span className="t-caption" style={{ marginLeft: "var(--sp-xs)" }}>
            reconstructed from extracted passages
          </span>
        )}
      </div>

      {tab === "reading" ? (
        <article
          className="card card--pad-lg"
          style={{ maxWidth: 840, color: "var(--ink)" }}
        >
          <Reading content={content} />
        </article>
      ) : (
        <div className="stack" style={{ gap: "var(--sp-xs)", maxWidth: 840 }}>
          {content.passages.map((p) => (
            <div
              key={p.span_id}
              style={{
                padding: "var(--sp-sm) var(--sp-base)",
                border: "1px solid var(--hairline)",
                borderRadius: "var(--r-md)",
                background: "var(--canvas-soft)",
              }}
            >
              <div className="row" style={{ justifyContent: "space-between", gap: "var(--sp-xs)" }}>
                <span className="t-label">{p.span_id}</span>
                {p.page != null && <Badge>page {p.page}</Badge>}
              </div>
              <p className="t-body-sm" style={{ marginTop: "var(--sp-xxs)", color: "var(--ink)", whiteSpace: "pre-wrap" }}>
                {p.text}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
