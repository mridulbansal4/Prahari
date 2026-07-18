// The remaining modules — read-mostly surfaces. Each honours its PRB spec: honest empty states,
// no target-as-achieved (BR-8), append-only audit (no edit/delete affordance), PII-minimal.
import { useEffect, useState } from "react";
import { Badge } from "../components/primitives";
import { api } from "../lib/api";

// -------------------------------------------------------------------- M9 Audit & Provenance
export function Audit() {
  const [entries, setEntries] = useState<any[]>([]);
  const [action, setAction] = useState("");
  useEffect(() => {
    api.audit(action ? { action } : {}).then((d) => setEntries(d.entries));
  }, [action]);
  return (
    <div className="col">
      <div><div className="t-label">Audit &amp; Provenance</div><div className="t-display-md">Append-only. Nothing edits or deletes.</div></div>
      <div className="row"><input className="input" placeholder="filter by action (e.g. action.submitted)" value={action} onChange={(e) => setAction(e.target.value)} /></div>
      <div className="card" style={{ padding: 0 }}>
        <table className="grid-table">
          <thead><tr><th>When</th><th>Actor</th><th>Action</th><th>Target</th></tr></thead>
          <tbody>
            {entries.map((e) => (
              <tr key={e.entry_id}>
                <td className="t-mono">{new Date(e.ts).toLocaleString()}</td>
                <td>{e.actor}</td>
                <td className="t-mono">{e.action}</td>
                <td className="t-mono t-metadata">{e.target ?? "—"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

// ------------------------------------------------------------------------- M10 Decision Analytics
export function Analytics() {
  const [data, setData] = useState<any>(null);
  useEffect(() => { api.analytics().then(setData); }, []);
  if (!data) return <div className="card"><div className="skeleton" style={{ height: 100 }} /></div>;
  return (
    <div className="col">
      <div><div className="t-label">Decision Analytics</div><div className="t-display-md">The flywheel, as a number</div></div>
      <div className="grid-4">
        {data.kpis.map((k: any) => (
          <div key={k.key} className={`card ${k.is_flywheel ? "card-investigation" : ""}`}>
            <div className="t-label">{k.label}</div>
            <div className="t-metric" style={{ color: k.is_flywheel ? "var(--signal)" : "var(--ink)" }}>
              {k.actual ?? "—"}
            </div>
            <div className="t-metadata">target: {k.target}</div>
            {k.note && <div className="t-caption" style={{ marginTop: 4 }}>{k.note}</div>}
          </div>
        ))}
      </div>
      <div className="card card-dense"><span className="t-metadata">{data.disclaimer}</span></div>
    </div>
  );
}

// ---------------------------------------------------------------------- M5 Organizational Memory
export function OrgMemory() {
  const [people, setPeople] = useState<any[]>([]);
  useEffect(() => { api.orgMemory().then((d) => setPeople(d.people)); }, []);
  return (
    <div className="col">
      <div><div className="t-label">Organizational Memory</div><div className="t-display-md">Capture judgement before it retires</div></div>
      {people.map((p) => (
        <div key={p.person_id} className="card">
          <div className="row between center">
            <div><span className="t-title">{p.name}</span> <span className="t-metadata">{p.role} · {p.tenure_years}y</span></div>
            {p.retirement_risk && <Badge kind="warning">Retirement risk</Badge>}
          </div>
          <div className="row wrap" style={{ gap: "var(--sp-sm)", marginTop: "var(--sp-sm)" }}>
            {p.knows.map((k: any, i: number) => (
              <span key={i} className="badge">{k.label || k.target_ref}</span>
            ))}
          </div>
        </div>
      ))}
      <div className="t-metadata">PII-minimal: role, expertise, tenure, retirement-risk only — never an HR record (BR-9).</div>
    </div>
  );
}

// ------------------------------------------------------------------------- M4 Knowledge Evolution
export function Knowledge() {
  const [flags, setFlags] = useState<any[]>([]);
  const [lastRun, setLastRun] = useState<any>(null);
  async function load() { const d = await api.knowledgeHealth(); setFlags(d.flags); setLastRun(d.last_run); }
  useEffect(() => { load(); }, []);
  return (
    <div className="col">
      <div className="row between center">
        <div><div className="t-label">Knowledge Evolution</div><div className="t-display-md">Knowledge decays — SENTINEL notices</div></div>
        <button className="btn btn-secondary" onClick={async () => { await api.runDecay(); load(); }}>Run decay job</button>
      </div>
      {lastRun && <div className="t-metadata">Last computed {lastRun.date} · {lastRun.count} flags</div>}
      {flags.length === 0 ? (
        <div className="card"><span className="t-body ink-muted">No knowledge currently flagged as at-risk — a good state.</span></div>
      ) : (
        flags.map((f) => (
          <div key={f.flag_id} className="card card-dense" style={{ borderLeft: "3px solid var(--warning)" }}>
            <div className="row between center">
              <span className="t-label" style={{ color: "var(--warning)" }}>{f.trigger.replace("_", " ")}</span>
              <span className="t-metadata t-mono">{f.affected_fact_ref}</span>
            </div>
            <div className="t-body-sm" style={{ marginTop: 4 }}>{f.description}</div>
          </div>
        ))
      )}
    </div>
  );
}

// -------------------------------------------------------------------- M3 Decision Memory & Replay
export function Replay() {
  const [decisions, setDecisions] = useState<any[]>([]);
  const [chain, setChain] = useState<any>(null);
  useEffect(() => { api.decisions().then((d) => setDecisions(d.decisions)); }, []);
  return (
    <div className="col">
      <div><div className="t-label">Decision Memory &amp; Replay</div><div className="t-display-md">Replay the reasoning, not just the timeline</div></div>
      <div className="row wrap" style={{ gap: "var(--sp-sm)" }}>
        {decisions.map((d) => (
          <button key={d.decision_id} className="btn btn-secondary" onClick={async () => setChain(await api.replay(d.decision_id))}>
            {d.title}
          </button>
        ))}
      </div>
      {chain && (
        <div className="col">
          {chain.steps?.length ? chain.steps.map((s: any) => (
            <div key={s.id} className="card card-dense" style={{ borderLeft: `3px solid ${s.kind === "Alternative" ? "var(--ink-faint)" : "var(--decision)"}` }}>
              <div className="t-label">{s.kind}</div>
              <div className="t-body">{s.title}</div>
              {s.detail && <div className="t-body-sm ink-muted" style={{ marginTop: 4 }}>{s.detail}</div>}
              {s.citations?.length > 0 && <div className="t-metadata t-mono" style={{ marginTop: 4 }}>cited: {s.citations.map((c: any) => c.span_id).join(", ")}</div>}
            </div>
          )) : <div className="card"><span className="t-body ink-muted">{chain.note}</span></div>}
        </div>
      )}
    </div>
  );
}

// ----------------------------------------------------------------------- M11 Admin & Ingestion
export function Admin() {
  const [jobs, setJobs] = useState<any[]>([]);
  const [quarantined, setQuarantined] = useState<any[]>([]);
  useEffect(() => { api.ingestionJobs().then((d) => { setJobs(d.jobs); setQuarantined(d.quarantined); }); }, []);
  return (
    <div className="col">
      <div><div className="t-label">Admin &amp; Ingestion Console</div><div className="t-display-md">Documents in, provenance out</div></div>
      <div className="card" style={{ padding: 0 }}>
        <table className="grid-table">
          <thead><tr><th>Document</th><th>Status</th><th>Nodes</th><th>Edges</th><th>Spans</th></tr></thead>
          <tbody>
            {jobs.map((j) => (
              <tr key={j.job_id}>
                <td className="t-mono">{j.filename}</td>
                <td>{j.status === "complete" ? <Badge kind="success">Complete</Badge> : j.status === "quarantined" ? <Badge kind="critical">Quarantined</Badge> : <Badge kind="warning">{j.status}</Badge>}</td>
                <td className="tabular">{j.node_count}</td>
                <td className="tabular">{j.edge_count}</td>
                <td className="tabular">{j.span_count}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {quarantined.length > 0 && (
        <div className="card card-critical">
          <div className="t-label">Quarantine — never promoted to a fact (BR-1)</div>
          {quarantined.map((q) => <div key={q.job_id} className="t-body-sm">{q.filename}: {q.quarantine_reason}</div>)}
        </div>
      )}
      <div className="t-metadata">Ingested document text is treated strictly as data, never as instruction (ADR-011/FM-7).</div>
    </div>
  );
}
