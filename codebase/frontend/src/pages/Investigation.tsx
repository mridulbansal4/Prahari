// M1 Decision Investigation (PRB §2.2) — question bar + streamed AnswerCard + live GraphCanvas +
// per-agent-stage loading + abstention. Presents as an argument to inspect hop by hop, never a
// chat transcript.
import { useEffect, useState } from "react";
import { AbstainCard, AnswerCard } from "../components/AnswerCard";
import { GraphCanvas } from "../components/GraphCanvas";
import { StageIndicator } from "../components/primitives";
import { api } from "../lib/api";
import { streamInvestigation } from "../lib/stream";
import type { GraphHop, InvestigationResult, StreamEvent } from "../lib/types";

interface RunState {
  running: boolean;
  stage?: { stage: string; detail?: string };
  answerText: string;
  hops: GraphHop[];
  result?: InvestigationResult;
}

const EMPTY: RunState = { running: false, answerText: "", hops: [] };

export function Investigation({ onRung }: { onRung: (r: string) => void }) {
  const [question, setQuestion] = useState("");
  const [asOf, setAsOf] = useState("");
  const [run, setRun] = useState<RunState>(EMPTY);
  const [recent, setRecent] = useState<{ investigation_id: string; question: string; abstained: boolean }[]>([]);

  useEffect(() => {
    api
      .recentInvestigations()
      // Don't surface injection/eval probe strings as clickable suggestions.
      .then((r) => setRecent(r.items.filter((i) => !/ignore previous|password|fatigue life/i.test(i.question))))
      .catch(() => {});
  }, [run.result]);

  async function ask(q: string) {
    if (!q.trim()) return;
    setRun({ ...EMPTY, running: true });
    const { investigation_id } = await api.askInvestigation(q, asOf || undefined);
    streamInvestigation(investigation_id, (ev: StreamEvent) => {
      // Banner updates App state — do it OUTSIDE the setRun updater (never setState another
      // component during this one's render).
      if (ev.type === "banner") {
        onRung(String(ev.rung ?? "full"));
        return;
      }
      setRun((prev) => reduce(prev, ev));
    });
  }

  return (
    <div className="col">
      <div>
        <div className="t-label">Decision Investigation</div>
        <div className="t-display-md">Navigate organizational memory</div>
      </div>

      {/* Question bar */}
      <div className="card">
        <div className="row" style={{ alignItems: "flex-end" }}>
          <div className="grow col" style={{ gap: "var(--sp-xs)" }}>
            <label className="t-label">Question</label>
            <input
              className="input"
              placeholder="why is P-101B running hot?"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && ask(question)}
            />
          </div>
          <div className="col" style={{ gap: "var(--sp-xs)" }}>
            <label className="t-label">As of</label>
            <input className="input" type="date" value={asOf} onChange={(e) => setAsOf(e.target.value)} />
          </div>
          <button className="btn btn-primary" disabled={run.running} onClick={() => ask(question)}>
            {run.running ? "Investigating…" : "Investigate"}
          </button>
        </div>
      </div>

      {/* Empty state — never a bare box (PRB §2.2) */}
      {!run.running && !run.result && (
        <div className="card">
          <div className="t-label" style={{ marginBottom: "var(--sp-sm)" }}>
            Things people are asking at this site
          </div>
          {recent.length === 0 ? (
            <div className="col" style={{ gap: "var(--sp-xs)" }}>
              {["why is P-101B running hot?", "which OISD inspections are overdue on P-101B?"].map((q) => (
                <button key={q} className="btn btn-tertiary" style={{ justifyContent: "flex-start" }} onClick={() => { setQuestion(q); ask(q); }}>
                  {q}
                </button>
              ))}
            </div>
          ) : (
            recent.map((r) => (
              <button key={r.investigation_id} className="btn btn-tertiary" style={{ display: "block", textAlign: "left" }}
                onClick={() => { setQuestion(r.question); ask(r.question); }}>
                {r.question} {r.abstained && <span className="t-metadata">· abstained</span>}
              </button>
            ))
          )}
        </div>
      )}

      {/* Running / result */}
      {(run.running || run.result) && (
        <div className="grid-2" style={{ gridTemplateColumns: "1fr 540px", alignItems: "start" }}>
          <div className="col">
            {run.running && run.stage && <div className="card"><StageIndicator stage={run.stage.stage} detail={run.stage.detail} /></div>}
            {run.running && run.answerText && (
              <div className="card card-investigation"><p className="t-subtitle">{run.answerText}</p></div>
            )}
            {run.result && !run.result.abstained && <AnswerCard result={run.result} />}
            {run.result && run.result.abstained && <AbstainCard result={run.result} />}
            {run.result && !run.result.abstained && (
              <DraftAction assetId={run.result.graph_path.find((h) => h.node_label === "Asset")?.node} investigationId={run.result.investigation_id} question={run.result.question} />
            )}
          </div>
          <div className="card" style={{ padding: 0, height: 560, overflow: "hidden" }}>
            <GraphCanvas hops={run.hops} />
          </div>
        </div>
      )}
    </div>
  );
}

function DraftAction({ assetId, investigationId, question }: { assetId?: string | null; investigationId: string; question: string }) {
  const [state, setState] = useState<string | null>(null);
  if (!assetId) return null;
  async function draft() {
    setState("drafting");
    try {
      const d = await api.draftWorkOrder(assetId!, question, investigationId);
      setState(`Draft ${d.draft_id} created — open Execution Center to approve.`);
    } catch (e) {
      setState("Drafting failed — retry.");
    }
  }
  return (
    <div className="card card-decision">
      <div className="t-label" style={{ marginBottom: "var(--sp-sm)" }}>Recommended next step</div>
      <button className="btn btn-decision" onClick={draft} disabled={state === "drafting"}>
        Draft a work order from this hypothesis
      </button>
      {state && state !== "drafting" && <div className="t-caption" style={{ marginTop: "var(--sp-sm)" }}>{state}</div>}
    </div>
  );
}

function reduce(prev: RunState, ev: StreamEvent): RunState {
  switch (ev.type) {
    case "stage":
      return { ...prev, stage: { stage: String(ev.stage), detail: ev.detail as string } };
    case "graph_hop":
      return { ...prev, hops: [...prev.hops, ev.hop as GraphHop] };
    case "token":
      return { ...prev, answerText: prev.answerText + String(ev.text ?? "") };
    case "abstain":
      return { ...prev, running: false, result: ev.result as InvestigationResult };
    case "done":
      return { ...prev, running: false, result: ev.result as InvestigationResult };
    default:
      return prev;
  }
}
