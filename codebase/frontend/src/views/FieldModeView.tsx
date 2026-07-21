// Field mode — for a technician on a phone, on the plant floor, at 02:40. One big box,
// big result text, minimal chrome, large tap targets. Same tokens throughout.
import { useState } from "react";
import { AbstainCard, AnswerCard } from "../components/AnswerCard";
import { TraversalTrace } from "../components/GraphCanvas";
import { DegradationNotice, LoadingBar, Notice } from "../components/ui";
import { stageLabel, type RunState } from "../lib/useInvestigation";

export function FieldModeView({
  run,
  onAsk,
}: {
  run: RunState;
  onAsk: (q: string) => void;
}) {
  const [value, setValue] = useState("");

  function submit(e: React.FormEvent) {
    e.preventDefault();
    if (!value.trim()) return;
    onAsk(value);
  }

  return (
    <div style={{ maxWidth: 640, margin: "0 auto" }}>
      <h1 className="t-display-md">Field mode</h1>
      <p className="t-body" style={{ marginTop: "var(--sp-xxs)", marginBottom: "var(--sp-lg)" }}>
        One question, one answer. Built for a phone in your hand on the floor.
      </p>

      <DegradationNotice rung={run.rung} />

      <form onSubmit={submit} className="stack" style={{ gap: "var(--sp-sm)" }}>
        <label htmlFor="field-ask" className="t-label">
          What do you need to know?
        </label>
        <textarea
          id="field-ask"
          className="input"
          rows={3}
          style={{ fontSize: 18, minHeight: 96, resize: "vertical", lineHeight: 1.5 }}
          placeholder="e.g. why is P-101B running hot?"
          value={value}
          onChange={(e) => setValue(e.target.value)}
        />
        <button
          type="submit"
          className="btn btn--primary"
          style={{ minHeight: 56, fontSize: 17, width: "100%" }}
          disabled={run.running}
        >
          {run.running ? "Working…" : "Ask"}
        </button>
      </form>

      <div style={{ marginTop: "var(--sp-lg)" }}>
        {run.error && <Notice tone="error">{run.error}</Notice>}

        {run.running && (
          <div className="card">
            <LoadingBar stage={stageLabel(run.stage?.stage)} />
          </div>
        )}

        {run.result && !run.result.abstained && <AnswerCard result={run.result} />}
        {run.result?.abstained && <AbstainCard result={run.result} />}

        {run.result && run.hops.length > 0 && (
          <div className="card" style={{ marginTop: "var(--sp-base)" }}>
            <div className="t-label" style={{ marginBottom: "var(--sp-sm)" }}>
              Where this came from
            </div>
            <TraversalTrace hops={run.hops} />
          </div>
        )}
      </div>
    </div>
  );
}
