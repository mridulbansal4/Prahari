// Ask — the home view and the beating heart. ONE ask box (the old hero/section duplication
// is gone). A run started here survives navigating away and back, because the controller
// lives at App level.
import { useEffect, useState } from "react";
import { AbstainCard, AnswerCard } from "../components/AnswerCard";
import { NetworkGraph } from "../components/NetworkGraph";
import { Chip, DegradationNotice, LoadingBar, Notice, Orb, ViewHeader } from "../components/ui";
import { api } from "../lib/api";
import type { Alert } from "../lib/alerts";
import { traversalToNet } from "../lib/graph";
import { stageLabel, type RunState } from "../lib/useInvestigation";

const EXAMPLES = [
  "Why is P-101B running hot?",
  "Pump P-101B is vibrating — what should I check before servicing it?",
  "Which inspections are overdue on P-101B?",
];

const NOT_A_SUGGESTION = /ignore previous|password|fatigue life/i;

export function AskView({
  run,
  onAsk,
  alerts,
  onOpenMap,
  onOpenAlerts,
}: {
  run: RunState;
  onAsk: (q: string) => void;
  alerts: Alert[];
  onOpenMap: () => void;
  onOpenAlerts: () => void;
}) {
  const [value, setValue] = useState("");
  const [recent, setRecent] = useState<string[]>([]);

  useEffect(() => {
    api
      .recentInvestigations()
      .then((r) =>
        setRecent(
          r.items.filter((i) => !NOT_A_SUGGESTION.test(i.question)).map((i) => i.question),
        ),
      )
      .catch(() => {});
  }, [run.result]);

  function submit(e: React.FormEvent) {
    e.preventDefault();
    if (!value.trim()) return;
    onAsk(value);
  }

  const assetTags = new Set(
    run.result?.graph_path
      .filter((h) => h.node_label === "Asset")
      .map((h) => (h.detail ?? "").trim())
      .filter(Boolean),
  );
  const related = run.result ? alerts.filter((a) => a.assetTag && assetTags.has(a.assetTag)) : [];
  const idle = !run.running && !run.result && !run.error;
  const net = traversalToNet(run.hops);

  const suggestions = [...new Set([...EXAMPLES, ...recent])].slice(0, 4);

  return (
    // overflow:hidden clips the decorative orbs — they are positioned past the edges and
    // would otherwise widen the document and cause horizontal scroll on narrow screens.
    <div style={{ position: "relative", overflow: "hidden" }}>
      {/* Atmosphere lives on the Ask home only; the rest of the workspace stays quiet. */}
      <Orb color="mint" size={460} style={{ top: -200, left: -140, opacity: 0.4 }} />
      <Orb color="peach" size={360} style={{ top: -150, right: -90, opacity: 0.35 }} />

      <div style={{ position: "relative", zIndex: 1 }}>
        <ViewHeader
          title="Ask about your documents"
          helper="Ask the way you'd ask a colleague who had read everything. Every statement comes back with the document it came from."
        />

        <DegradationNotice rung={run.rung} />

        <form onSubmit={submit} style={{ display: "flex", gap: "var(--sp-sm)", flexWrap: "wrap" }}>
          <label htmlFor="ask-input" style={{ position: "absolute", left: -9999 }}>
            Your question
          </label>
          <input
            id="ask-input"
            className="input"
            style={{ flex: "1 1 380px", minHeight: 56, fontSize: 18 }}
            placeholder="e.g. Pump P-101B is vibrating — what should I check first?"
            value={value}
            onChange={(e) => setValue(e.target.value)}
          />
          <button
            type="submit"
            className="btn btn--primary"
            style={{ minHeight: 56, padding: "0 32px" }}
            disabled={run.running}
          >
            {run.running ? "Working…" : "Ask"}
          </button>
        </form>

        <div className="row" style={{ gap: "var(--sp-xs)", flexWrap: "wrap", marginTop: "var(--sp-base)" }}>
          <span className="t-caption" style={{ marginRight: "var(--sp-xxs)" }}>
            Try:
          </span>
          {suggestions.map((q) => (
            <Chip
              key={q}
              onClick={() => {
                setValue(q);
                onAsk(q);
              }}
            >
              {q}
            </Chip>
          ))}
        </div>

        <div style={{ marginTop: "var(--sp-xl)" }}>
          {idle && (
            <div
              className="card"
              style={{
                borderStyle: "dashed",
                borderColor: "var(--hairline-strong)",
                background: "var(--canvas-soft)",
                padding: "var(--sp-xxl) var(--sp-lg)",
                textAlign: "center",
              }}
            >
              <div className="t-display-sm" style={{ marginBottom: "var(--sp-xs)" }}>
                Your answer will appear here
              </div>
              <p className="t-body" style={{ maxWidth: 520, margin: "0 auto" }}>
                Type a question above, or pick one of the examples. Every answer shows which
                document each statement came from, so you can check it yourself.
              </p>
            </div>
          )}

          {run.error && <Notice tone="error">{run.error}</Notice>}

          {run.running && (
            <div className="card">
              <LoadingBar stage={stageLabel(run.stage?.stage)} />
              {run.answerText && (
                <p className="t-body" style={{ marginTop: "var(--sp-base)", color: "var(--ink)" }}>
                  {run.answerText}
                </p>
              )}
            </div>
          )}

          {(run.result || net.nodes.length > 0) && (
            <div className="ask-grid" style={{ display: "grid", gap: "var(--sp-base)" }}>
              <div className="stack" style={{ gap: "var(--sp-base)" }}>
                {run.result && !run.result.abstained && <AnswerCard result={run.result} />}
                {run.result?.abstained && <AbstainCard result={run.result} />}

                {related.length > 0 && (
                  <div className="card">
                    <div className="t-label" style={{ marginBottom: "var(--sp-sm)" }}>
                      Also flagged on this equipment
                    </div>
                    <div className="stack" style={{ gap: "var(--sp-sm)" }}>
                      {related.map((a) => (
                        <div key={a.id} className="row" style={{ gap: "var(--sp-xs)" }}>
                          <span
                            aria-hidden="true"
                            style={{
                              width: 4,
                              alignSelf: "stretch",
                              borderRadius: "var(--r-pill)",
                              background:
                                a.kind === "overdue" ? "var(--error)" : "var(--hairline-strong)",
                              flexShrink: 0,
                            }}
                          />
                          <div>
                            <div className="t-body-strong">{a.title}</div>
                            <div className="t-body-sm">{a.detail}</div>
                          </div>
                        </div>
                      ))}
                    </div>
                    <button
                      type="button"
                      className="btn btn--text"
                      style={{ marginTop: "var(--sp-sm)" }}
                      onClick={onOpenAlerts}
                    >
                      See everything it flagged →
                    </button>
                  </div>
                )}
              </div>

              {net.nodes.length > 0 && (
                <div className="card" style={{ padding: "var(--sp-base)" }}>
                  <div
                    className="row"
                    style={{ justifyContent: "space-between", marginBottom: "var(--sp-sm)" }}
                  >
                    <span className="t-label">How it connected the dots</span>
                    <button type="button" className="btn btn--text" onClick={onOpenMap}>
                      Open full map →
                    </button>
                  </div>
                  {/* Stacked: this panel is ~460px wide, so a side-by-side inspector would
                      squeeze the canvas down to an unreadable sliver. */}
                  <NetworkGraph
                    nodes={net.nodes}
                    links={net.links}
                    height={340}
                    layout="stacked"
                  />
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
