// AnswerCard + AbstainCard — AI output in the SAME card language as human analysis (design.md
// AI rules): no chat bubble, no avatar. Every claim carries a confidence reading + a citation.
import { useState } from "react";
import type { Citation, Claim, InvestigationResult } from "../lib/types";
import { CitationChip, ConfidenceIndicator } from "./primitives";
import { CorrectionAffordance } from "./CorrectionComposer";

function CitationPeek({ c }: { c: Citation }) {
  return (
    <div className="card card-dense card-evidence" style={{ marginTop: "var(--sp-xs)" }}>
      <div className="t-label" style={{ color: "var(--evidence)" }}>
        {c.doc_id} {c.page ? `· p.${c.page}` : ""}
      </div>
      <div className="t-body-sm" style={{ marginTop: 4 }}>
        {c.excerpt ?? c.span_id}
      </div>
      <div className="t-metadata t-mono" style={{ marginTop: 4 }}>
        span: {c.span_id}
      </div>
    </div>
  );
}

function ClaimRow({ claim, index }: { claim: Claim; index: number }) {
  const [openCite, setOpenCite] = useState<number | null>(null);
  return (
    <div style={{ padding: "var(--sp-md) 0", borderBottom: "1px solid var(--hairline-soft)" }}>
      <div className="row between" style={{ alignItems: "flex-start", gap: "var(--sp-md)" }}>
        <div className="grow">
          <span className="t-body">{claim.text}</span>{" "}
          {claim.citations.map((_, i) => (
            <CitationChip key={i} n={i + 1} onClick={() => setOpenCite(openCite === i ? null : i)} />
          ))}
        </div>
        <ConfidenceIndicator state={claim.confidence} />
      </div>
      {openCite !== null && claim.citations[openCite] && (
        <CitationPeek c={claim.citations[openCite]} />
      )}
      <div style={{ marginTop: "var(--sp-xs)" }}>
        <CorrectionAffordance targetKind="claim" targetRef={`claim:${index}`} priorValue={claim.text} />
      </div>
    </div>
  );
}

export function AnswerCard({ result }: { result: InvestigationResult }) {
  return (
    <div className="card card-investigation">
      <div className="row between center" style={{ marginBottom: "var(--sp-md)" }}>
        <span className="t-label">Hypothesis</span>
        <span className="t-metadata t-mono" title="prompt manifest hash · model (reproducibility, CP-7)">
          {result.model_id} · {result.prompt_manifest_hash}
        </span>
      </div>
      <p className="t-subtitle" style={{ marginBottom: "var(--sp-md)" }}>
        {result.answer}
      </p>
      {result.claims.map((c, i) => (
        <ClaimRow key={i} claim={c} index={i} />
      ))}
    </div>
  );
}

/** A designed, positive success state — never error-red (BR-6, ui_rules abstention rule). */
export function AbstainCard({ result }: { result: InvestigationResult }) {
  return (
    <div className="card" style={{ borderLeft: "3px solid var(--investigation)" }}>
      <div className="row center" style={{ gap: "var(--sp-sm)", marginBottom: "var(--sp-md)" }}>
        <span className="t-label" style={{ color: "var(--investigation)" }}>
          Abstained — I won't guess
        </span>
      </div>
      <p className="t-body ink-muted">
        In a plant, a wrong answer is worse than no answer. Here is what I can and cannot ground:
      </p>

      <div className="t-label" style={{ marginTop: "var(--sp-lg)" }}>
        What I could not ground
      </div>
      <ul style={{ marginLeft: "var(--sp-lg)", marginTop: "var(--sp-xs)" }}>
        {result.unresolved.map((u, i) => (
          <li key={i} className="t-body-sm">
            {u}
          </li>
        ))}
      </ul>

      {result.who_to_ask.length > 0 && (
        <>
          <div className="t-label" style={{ marginTop: "var(--sp-lg)" }}>
            Who to ask
          </div>
          <div className="col" style={{ gap: "var(--sp-sm)", marginTop: "var(--sp-xs)" }}>
            {result.who_to_ask.map((w, i) => (
              <div key={i} className="card card-dense">
                <span className="t-body">{w.person}</span>{" "}
                <span className="t-caption">
                  — {w.expertise}
                  {w.tenure_years ? ` · ${w.tenure_years}y tenure` : ""}
                </span>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
