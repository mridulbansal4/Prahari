// M7 Execution Center (PRB §2.5, CP-3) — draft → ApprovalSheet → committed. A drafted action and
// a committed action are never confusable (NFR-13). The CP-3 gate is made visible, not hidden.
import { useEffect, useState } from "react";
import { Badge } from "../components/primitives";
import { api } from "../lib/api";
import { useAuth } from "../lib/auth";

interface Draft {
  draft_id: string;
  asset_tag: string;
  symptom: string;
  status: string;
  drafter: string;
  approver: string | null;
  cmms_work_order_id: string | null;
  investigation_id: string | null;
}

export function Execution() {
  const { me } = useAuth();
  const [drafts, setDrafts] = useState<Draft[]>([]);
  const [msg, setMsg] = useState<string | null>(null);
  const canApprove = me?.role === "reliability" || me?.role === "admin";

  async function load() {
    const d = await api.listActions();
    setDrafts(d.drafts);
  }
  useEffect(() => {
    load();
  }, []);

  async function approve(d: Draft, cmms_ok = true) {
    if (!me) return;
    try {
      const res = await api.submitWorkOrder(d.draft_id, me.subject, cmms_ok);
      setMsg(`Committed to CMMS as ${res.cmms_work_order_id}, approved by ${me.name}.`);
    } catch (e: any) {
      setMsg(e?.message ?? "Not committed.");
    }
    await load();
  }
  async function reject(d: Draft) {
    await api.rejectWorkOrder(d.draft_id, "Rejected on review");
    await load();
  }

  return (
    <div className="col">
      <div>
        <div className="t-label">Execution Center</div>
        <div className="t-display-md">No write without an approval</div>
      </div>
      {msg && <div className="card card-dense" style={{ borderLeft: "3px solid var(--decision)" }}><span className="t-body-sm">{msg}</span></div>}
      {drafts.length === 0 && <div className="card"><span className="t-body ink-muted">No drafts yet. Draft one from a Decision Investigation hypothesis.</span></div>}
      {drafts.map((d) => (
        <div key={d.draft_id} className={`card ${d.status === "committed" ? "" : "card-decision"}`}>
          <div className="row between center">
            <div>
              <div className="t-title">{d.asset_tag} — {d.symptom}</div>
              <div className="t-metadata t-mono">draft {d.draft_id} · by {d.drafter}{d.investigation_id ? ` · from ${d.investigation_id}` : ""}</div>
            </div>
            {d.status === "committed" ? (
              <Badge kind="success">Committed · {d.cmms_work_order_id}</Badge>
            ) : d.status === "rejected" ? (
              <Badge kind="offline">Rejected</Badge>
            ) : (
              <Badge kind="warning">Draft — awaiting approval</Badge>
            )}
          </div>
          {d.status === "pending" && (
            <div className="row" style={{ marginTop: "var(--sp-md)", gap: "var(--sp-sm)" }}>
              {canApprove ? (
                <>
                  <button className="btn btn-decision" onClick={() => approve(d)}>Approve &amp; submit to CMMS</button>
                  <button className="btn btn-secondary" onClick={() => reject(d)}>Reject</button>
                  <button className="btn btn-tertiary" onClick={() => approve(d, false)} title="Exercise the CMMS-unreachable failure path">
                    Simulate CMMS unreachable
                  </button>
                </>
              ) : (
                <span className="t-metadata">Awaiting approval from reliability/admin — you drafted this; a distinct approver must commit it (CP-3).</span>
              )}
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
