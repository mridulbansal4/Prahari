// The answer surface. Rendered as a documented analysis — plain answer, then each claim with
// its sources and confidence. No chat bubble, no avatar, no assistant persona.
import { useState } from "react";
import type { Citation, Claim, InvestigationResult } from "../lib/types";
import { Badge, Confidence } from "./ui";

function CitationPeek({ citation }: { citation: Citation }) {
  return (
    <div
      style={{
        marginTop: "var(--sp-sm)",
        padding: "var(--sp-base)",
        background: "var(--canvas-soft)",
        border: "1px solid var(--hairline)",
        borderRadius: "var(--r-md)",
      }}
    >
      <div className="t-label" style={{ marginBottom: "var(--sp-xxs)" }}>
        {citation.doc_id}
        {citation.page != null ? ` · page ${citation.page}` : ""}
      </div>
      <p className="t-body-sm" style={{ color: "var(--body)" }}>
        {citation.excerpt ?? `Source passage ${citation.span_id}`}
      </p>
    </div>
  );
}

/**
 * Numbered citation chips with an inline peek. Exported so any surface that cites evidence —
 * the answer, a replayed decision — shows sources identically. `excerpt` may be null when the
 * source endpoint returns only a reference; the peek then names the passage instead of
 * quoting it, rather than showing an empty box.
 */
export function CitationChips({ citations }: { citations: Citation[] }) {
  const [open, setOpen] = useState<number | null>(null);
  if (!citations.length) return null;
  return (
    <>
      {citations.map((c, i) => (
        <button
          key={`${c.span_id}-${i}`}
          type="button"
          onClick={() => setOpen(open === i ? null : i)}
          aria-label={`Show the source for this statement: ${c.doc_id}`}
          aria-expanded={open === i}
          style={{
            font: "var(--t-caption)",
            color: open === i ? "var(--on-primary)" : "var(--ink)",
            background: open === i ? "var(--ink)" : "var(--surface-strong)",
            border: "none",
            borderRadius: "var(--r-pill)",
            padding: "1px 8px",
            marginLeft: 2,
            cursor: "pointer",
            verticalAlign: "baseline",
          }}
        >
          {i + 1}
        </button>
      ))}
      {open !== null && citations[open] && <CitationPeek citation={citations[open]} />}
    </>
  );
}

function ClaimRow({ claim, index }: { claim: Claim; index: number }) {
  const [open, setOpen] = useState<number | null>(null);
  return (
    <li
      style={{
        listStyle: "none",
        padding: "var(--sp-base) 0",
        borderTop: index === 0 ? "none" : "1px solid var(--hairline)",
      }}
    >
      <div
        style={{
          display: "flex",
          gap: "var(--sp-base)",
          alignItems: "flex-start",
          justifyContent: "space-between",
          flexWrap: "wrap",
        }}
      >
        <p className="t-body" style={{ color: "var(--ink)", flex: "1 1 320px", margin: 0 }}>
          {claim.text}{" "}
          {claim.citations.map((c, i) => (
            <button
              key={`${c.span_id}-${i}`}
              type="button"
              onClick={() => setOpen(open === i ? null : i)}
              aria-label={`Show the source for this statement: ${c.doc_id}`}
              aria-expanded={open === i}
              style={{
                font: "var(--t-caption)",
                color: open === i ? "var(--on-primary)" : "var(--ink)",
                background: open === i ? "var(--ink)" : "var(--surface-strong)",
                border: "none",
                borderRadius: "var(--r-pill)",
                padding: "1px 8px",
                marginLeft: 2,
                cursor: "pointer",
                verticalAlign: "baseline",
              }}
            >
              {i + 1}
            </button>
          ))}
        </p>
        <Confidence state={claim.confidence} />
      </div>
      {open !== null && claim.citations[open] && <CitationPeek citation={claim.citations[open]} />}
    </li>
  );
}

export function AnswerCard({ result }: { result: InvestigationResult }) {
  return (
    <article className="card card--pad-lg">
      <div
        className="row"
        style={{ justifyContent: "space-between", gap: "var(--sp-base)", flexWrap: "wrap" }}
      >
        <Badge>Answer</Badge>
        <span className="t-caption muted-soft">
          Every statement below links to the document it came from
        </span>
      </div>

      <p
        className="t-body"
        style={{ color: "var(--ink)", marginTop: "var(--sp-base)", fontSize: 17, lineHeight: 1.6 }}
      >
        {result.answer}
      </p>

      {result.claims.length > 0 && (
        <>
          <div
            className="t-label"
            style={{ marginTop: "var(--sp-xl)", marginBottom: "var(--sp-xxs)" }}
          >
            What this is based on
          </div>
          <ul style={{ margin: 0, padding: 0 }}>
            {result.claims.map((c, i) => (
              <ClaimRow key={i} claim={c} index={i} />
            ))}
          </ul>
        </>
      )}
    </article>
  );
}

/* The refusal. Deliberately a calm, confident outcome — never styled as an error. */
export function AbstainCard({ result }: { result: InvestigationResult }) {
  return (
    <article className="card card--pad-lg">
      <Badge>No answer given</Badge>
      <h3 className="t-display-md" style={{ marginTop: "var(--sp-base)" }}>
        I won&rsquo;t guess on this one.
      </h3>
      <p className="t-body" style={{ marginTop: "var(--sp-sm)", maxWidth: 560 }}>
        Nothing in your documents supports a confident answer. In a plant, a wrong answer is worse
        than no answer — so here is exactly what is missing, and who can fill the gap.
      </p>

      {result.unresolved.length > 0 && (
        <div style={{ marginTop: "var(--sp-xl)" }}>
          <div className="t-label" style={{ marginBottom: "var(--sp-xs)" }}>
            What I couldn&rsquo;t find
          </div>
          <ul style={{ paddingLeft: "var(--sp-md)" }}>
            {result.unresolved.map((u, i) => (
              <li key={i} className="t-body" style={{ marginBottom: "var(--sp-xxs)" }}>
                {u}
              </li>
            ))}
          </ul>
        </div>
      )}

      {result.who_to_ask.length > 0 && (
        <div style={{ marginTop: "var(--sp-xl)" }}>
          <div className="t-label" style={{ marginBottom: "var(--sp-xs)" }}>
            Who to ask instead
          </div>
          <div style={{ display: "grid", gap: "var(--sp-sm)" }}>
            {result.who_to_ask.map((p, i) => (
              <div
                key={i}
                className="row"
                style={{
                  gap: "var(--sp-sm)",
                  padding: "var(--sp-sm) var(--sp-base)",
                  background: "var(--canvas-soft)",
                  border: "1px solid var(--hairline)",
                  borderRadius: "var(--r-md)",
                }}
              >
                <span
                  aria-hidden="true"
                  className="row"
                  style={{
                    width: 32,
                    height: 32,
                    borderRadius: "var(--r-full)",
                    background: "var(--surface-strong)",
                    justifyContent: "center",
                    font: "var(--t-body-strong)",
                    color: "var(--ink)",
                    flexShrink: 0,
                  }}
                >
                  {p.person.charAt(0)}
                </span>
                <span>
                  <span className="t-body-strong">{p.person}</span>{" "}
                  <span className="t-body-sm muted">
                    — {p.expertise}
                    {p.tenure_years ? ` · ${p.tenure_years} years here` : ""}
                  </span>
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </article>
  );
}
