// M2 Living Asset Map (PRB §2.3) — the moat, on screen. Medium-confidence proposals; a human
// confirms/corrects one; the corpus grows. Reversible (unmerge). This is the primary wow moment.
import { useEffect, useState } from "react";
import { api } from "../lib/api";
import { useAuth } from "../lib/auth";
import type { ResolutionProposal } from "../lib/types";

export function AssetMap() {
  const { me } = useAuth();
  const [proposals, setProposals] = useState<ResolutionProposal[]>([]);
  const [corpus, setCorpus] = useState(0);
  const [loading, setLoading] = useState(true);
  const [lastMerge, setLastMerge] = useState<string | null>(null);
  const [msg, setMsg] = useState<string | null>(null);

  async function load() {
    setLoading(true);
    const q = await api.resolutionQueue();
    setProposals(q.proposals);
    setCorpus(q.corpus_size);
    setLoading(false);
  }
  useEffect(() => {
    load();
  }, []);

  const canAdjudicate = me?.role === "reliability" || me?.role === "admin";

  async function decide(p: ResolutionProposal, decision: "merge" | "separate") {
    if (!me) return;
    try {
      const res = await api.adjudicate(p.proposal_id, decision, me.subject);
      if (decision === "merge") {
        setLastMerge(res.reversible_id);
        setMsg(`Merged into ${res.resulting_asset_id}. The graph learned. Any prior answer referencing this asset now returns the unified result.`);
      } else {
        setMsg("Kept separate — identifiers remain distinct.");
      }
      await load();
    } catch (e: any) {
      setMsg(e?.message ?? "Already resolved by someone else — refreshed.");
      await load();
    }
  }

  async function undo() {
    if (!lastMerge) return;
    await api.unmerge(lastMerge);
    setMsg("Unmerged — the prior identifier→asset mapping was restored exactly (reversible, BR-4).");
    setLastMerge(null);
    await load();
  }

  return (
    <div className="col">
      <div className="row between center">
        <div>
          <div className="t-label">Living Asset Map</div>
          <div className="t-display-md">Which name means which physical thing</div>
        </div>
        <div className="card card-dense" style={{ textAlign: "right" }}>
          <div className="t-label">Resolution corpus</div>
          <div className="t-metric" style={{ color: "var(--signal)" }}>{corpus}</div>
          <div className="t-metadata">human adjudications — the moat, compounding</div>
        </div>
      </div>

      {msg && (
        <div className="card" style={{ borderLeft: "3px solid var(--knowledge)" }}>
          <span className="t-body-sm">{msg}</span>
          {lastMerge && (
            <button className="btn btn-tertiary" style={{ marginLeft: "var(--sp-md)" }} onClick={undo}>
              Unmerge (admin)
            </button>
          )}
        </div>
      )}

      {loading ? (
        <div className="card"><div className="skeleton" style={{ height: 120 }} /></div>
      ) : proposals.length === 0 ? (
        <div className="card">
          <div className="t-title">No pending resolutions</div>
          <div className="t-body ink-muted">The asset map is fully adjudicated — a good state.</div>
        </div>
      ) : (
        proposals.map((p) => <ProposalCard key={p.proposal_id} p={p} canAdjudicate={canAdjudicate} onDecide={decide} />)
      )}
    </div>
  );
}

function ProposalCard({
  p,
  canAdjudicate,
  onDecide,
}: {
  p: ResolutionProposal;
  canAdjudicate: boolean;
  onDecide: (p: ResolutionProposal, d: "merge" | "separate") => void;
}) {
  return (
    <div className="card">
      <div className="row between center" style={{ marginBottom: "var(--sp-lg)" }}>
        <span className="t-label">Proposed merge · confidence {(p.score * 100).toFixed(0)}%</span>
        <span className="t-metadata t-mono">{p.method}</span>
      </div>
      <div className="row center" style={{ gap: "var(--sp-lg)", flexWrap: "wrap" }}>
        <div className="col" style={{ gap: "var(--sp-sm)", flex: 1 }}>
          {p.identifiers.map((id) => (
            <div key={id.id} className="card card-dense" style={{ borderLeft: "3px solid var(--investigation)" }}>
              <div className="t-body">{id.value}</div>
              <div className="t-metadata t-mono">{id.source_system}:{id.vocabulary}</div>
            </div>
          ))}
        </div>
        <div style={{ fontSize: 24, color: "var(--signal)" }}>→</div>
        <div className="card card-dense" style={{ borderLeft: "3px solid var(--knowledge)", minWidth: 200 }}>
          <div className="t-label" style={{ color: "var(--knowledge)" }}>Canonical asset</div>
          <div className="t-title">{p.canonical_tag}</div>
          <div className="t-metadata t-mono">{p.canonical_asset_id}</div>
        </div>
      </div>
      <div className="row" style={{ marginTop: "var(--sp-lg)", gap: "var(--sp-sm)" }}>
        {canAdjudicate ? (
          <>
            <button className="btn btn-primary" onClick={() => onDecide(p, "merge")}>Confirm merge</button>
            <button className="btn btn-secondary" onClick={() => onDecide(p, "separate")}>Keep separate</button>
            <span className="t-metadata" style={{ alignSelf: "center" }}>
              This is reversible and versioned — a confirmed merge can be undone (BR-4).
            </span>
          </>
        ) : (
          <span className="t-metadata">View-only — adjudication requires reliability or admin.</span>
        )}
      </div>
      <div className="row wrap" style={{ marginTop: "var(--sp-md)", gap: "var(--sp-md)" }}>
        {Object.entries(p.features).map(([k, v]) => (
          <span key={k} className="t-metadata">
            {k}: <span className="tabular" style={{ color: "var(--ink)" }}>{v.toFixed(2)}</span>
          </span>
        ))}
      </div>
    </div>
  );
}
