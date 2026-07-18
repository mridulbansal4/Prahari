// M12 Field Mode (PRB §2.13) — the 90-second field path. Same M1 pathway under a stacked,
// one-handed, high-contrast layout. Includes the demo's closing move: disable the graph and ask
// again to see the honest refusal (CP-4/CP-9). Glare mode = high-contrast token set.
import { useState } from "react";
import { AbstainCard, AnswerCard } from "../components/AnswerCard";
import { TraversalTrace } from "../components/GraphCanvas";
import { StageIndicator } from "../components/primitives";
import { api } from "../lib/api";
import { streamInvestigation } from "../lib/stream";
import { useAuth } from "../lib/auth";
import type { GraphHop, InvestigationResult, StreamEvent } from "../lib/types";

export function FieldMode({ onRung, rung }: { onRung: (r: string) => void; rung: string }) {
  const { me } = useAuth();
  const [q, setQ] = useState("why is P-101B running hot?");
  const [glare, setGlare] = useState(false);
  const [stage, setStage] = useState<{ stage: string; detail?: string } | null>(null);
  const [hops, setHops] = useState<GraphHop[]>([]);
  const [result, setResult] = useState<InvestigationResult | null>(null);
  const [running, setRunning] = useState(false);

  async function ask() {
    setRunning(true);
    setResult(null);
    setHops([]);
    setStage(null);
    const { investigation_id } = await api.askInvestigation(q);
    streamInvestigation(investigation_id, (ev: StreamEvent) => {
      if (ev.type === "banner") onRung(String(ev.rung ?? "full"));
      if (ev.type === "stage") setStage({ stage: String(ev.stage), detail: ev.detail as string });
      if (ev.type === "graph_hop") setHops((h) => [...h, ev.hop as GraphHop]);
      if (ev.type === "done" || ev.type === "abstain") {
        setResult(ev.result as InvestigationResult);
        setRunning(false);
      }
    });
  }

  async function toggleGraph(disable: boolean) {
    // The refusal demo — admin exposes the existing CP-9 rung mechanism.
    if (me?.role === "admin") await api.setDegradation(disable ? "-graph" : "full");
  }

  return (
    <div
      data-contrast={glare ? "high" : undefined}
      style={{ maxWidth: 640, margin: "0 auto", display: "flex", flexDirection: "column", gap: "var(--sp-lg)" }}
    >
      <div className="row between center">
        <div className="t-title">Field Mode</div>
        <button className="btn btn-secondary" style={{ minHeight: 44 }} onClick={() => setGlare(!glare)}>
          {glare ? "Glare mode: ON" : "Glare mode"}
        </button>
      </div>

      <textarea className="textarea" value={q} onChange={(e) => setQ(e.target.value)} style={{ fontSize: 17, minHeight: 64 }} />
      <button className="btn btn-primary" style={{ minHeight: 56, fontSize: 15 }} disabled={running} onClick={ask}>
        {running ? "Investigating…" : "Investigate"}
      </button>

      {me?.role === "admin" && (
        <div className="card card-dense">
          <div className="t-label" style={{ marginBottom: "var(--sp-sm)" }}>Demo · the closing move</div>
          <div className="row" style={{ gap: "var(--sp-sm)" }}>
            <button className="btn btn-secondary" style={{ minHeight: 44 }} onClick={() => toggleGraph(true)}>Disable the graph</button>
            <button className="btn btn-tertiary" style={{ minHeight: 44 }} onClick={() => toggleGraph(false)}>Restore</button>
          </div>
          <div className="t-metadata" style={{ marginTop: "var(--sp-sm)" }}>
            Disable, then ask again — SENTINEL refuses honestly and names who to ask. A wrong answer is worse than none.
          </div>
        </div>
      )}

      {running && stage && <div className="card"><StageIndicator stage={stage.stage} detail={stage.detail} /></div>}
      {result && !result.abstained && (
        <>
          <AnswerCard result={result} />
          <div className="card"><div className="t-label" style={{ marginBottom: "var(--sp-sm)" }}>Traversal</div><TraversalTrace hops={hops} /></div>
        </>
      )}
      {result && result.abstained && <AbstainCard result={result} />}
      {rung && rung !== "full" && <div className="t-metadata" style={{ color: "var(--warning)" }}>Degradation rung: {rung}</div>}
    </div>
  );
}
