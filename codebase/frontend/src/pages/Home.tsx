// Role-based home dashboards (design.md "Dashboard Philosophy": opinionated, role-scoped views;
// PRB §1.2 persona primary-modules, §1.4 access matrix). Each role lands on a different surface
// composed from the endpoints that role is permitted to call — no shared, generic dashboard.
import { useEffect, useState, type ReactNode } from "react";
import { useNavigate } from "react-router-dom";
import { Badge } from "../components/primitives";
import { api } from "../lib/api";
import { useAuth } from "../lib/auth";

// ---------------------------------------------------------------------------- shared bits
function StatTile({
  label,
  value,
  hint,
  accent,
  onClick,
}: {
  label: string;
  value: ReactNode;
  hint?: string;
  accent?: string;
  onClick?: () => void;
}) {
  return (
    <div
      className="card metric-card"
      onClick={onClick}
      style={{ cursor: onClick ? "pointer" : "default" }}
    >
      <div className="t-label">{label}</div>
      <div className="t-metric" style={{ color: accent ?? "var(--ink)" }}>
        {value}
      </div>
      {hint && <div className="t-caption">{hint}</div>}
    </div>
  );
}

function Panel({ title, children, action }: { title: string; children: ReactNode; action?: ReactNode }) {
  return (
    <div className="card">
      <div className="row between center" style={{ marginBottom: "var(--sp-md)" }}>
        <span className="t-label">{title}</span>
        {action}
      </div>
      {children}
    </div>
  );
}

function DashHeader({ eyebrow, title, sub }: { eyebrow: string; title: string; sub: string }) {
  return (
    <div>
      <div className="t-label">{eyebrow}</div>
      <div className="t-display-md">{title}</div>
      <div className="t-body ink-muted">{sub}</div>
    </div>
  );
}

// ============================================================ TECHNICIAN — Operator view (Ravi)
function OperatorDashboard() {
  const { me } = useAuth();
  const nav = useNavigate();
  const [recent, setRecent] = useState<any[]>([]);
  const [drafts, setDrafts] = useState<any[]>([]);

  useEffect(() => {
    api.recentInvestigations().then((r) => setRecent(r.items)).catch(() => {});
    api.listActions().then((d) => setDrafts(d.drafts.filter((x: any) => x.drafter === me?.subject))).catch(() => {});
  }, [me?.subject]);

  return (
    <div className="col">
      <DashHeader eyebrow="Operator" title={`Good shift, ${me?.name}`}
        sub="Turn a symptom into a grounded, cited hypothesis — in 90 seconds." />

      {/* Primary action for the field technician (his north-star path) */}
      <div className="card card-investigation">
        <div className="row between center">
          <div>
            <div className="t-title">Start a Decision Investigation</div>
            <div className="t-body-sm ink-muted">Ask why something is happening; watch the traversal, hop by hop.</div>
          </div>
          <div className="row" style={{ gap: "var(--sp-sm)" }}>
            <button className="btn btn-primary" onClick={() => nav("/investigate")}>Investigate</button>
            <button className="btn btn-secondary" onClick={() => nav("/field")}>Field Mode</button>
          </div>
        </div>
      </div>

      <div className="grid-2">
        <Panel title="Your recent investigations" action={<button className="btn btn-tertiary" onClick={() => nav("/investigate")}>Open</button>}>
          {recent.length === 0 ? (
            <div className="t-body-sm ink-muted">No investigations yet — ask your first question.</div>
          ) : (
            recent.slice(0, 5).map((r) => (
              <div key={r.investigation_id} className="row between center" style={{ padding: "6px 0", borderBottom: "1px solid var(--hairline-soft)" }}>
                <span className="t-body-sm">{r.question}</span>
                {r.abstained ? <Badge kind="warning">Abstained</Badge> : <Badge kind="success">Answered</Badge>}
              </div>
            ))
          )}
        </Panel>
        <Panel title="Your drafted work orders" action={<button className="btn btn-tertiary" onClick={() => nav("/execution")}>Execution Center</button>}>
          {drafts.length === 0 ? (
            <div className="t-body-sm ink-muted">No drafts. Draft one from an investigation hypothesis — approval is a separate, gated step.</div>
          ) : (
            drafts.slice(0, 5).map((d) => (
              <div key={d.draft_id} className="row between center" style={{ padding: "6px 0" }}>
                <span className="t-body-sm">{d.asset_tag} — {d.symptom}</span>
                <Badge kind={d.status === "committed" ? "success" : "warning"}>{d.status}</Badge>
              </div>
            ))
          )}
        </Panel>
      </div>
    </div>
  );
}

// ========================================================= RELIABILITY — Engineer view (Meera)
function ReliabilityDashboard() {
  const { me } = useAuth();
  const nav = useNavigate();
  const [queue, setQueue] = useState<{ n: number; corpus: number }>({ n: 0, corpus: 0 });
  const [pending, setPending] = useState(0);
  const [kpis, setKpis] = useState<any[]>([]);
  const [risks, setRisks] = useState(0);

  useEffect(() => {
    api.resolutionQueue().then((q) => setQueue({ n: q.proposals.length, corpus: q.corpus_size })).catch(() => {});
    api.listActions().then((d) => setPending(d.drafts.filter((x: any) => x.status === "pending").length)).catch(() => {});
    api.analytics().then((a) => setKpis(a.kpis)).catch(() => {});
    api.knowledgeHealth().then((k) => setRisks(k.flags.length)).catch(() => {});
  }, []);

  const corpusKpi = kpis.find((k) => k.key === "resolution_corpus");

  return (
    <div className="col">
      <DashHeader eyebrow="Reliability" title={`Reliability overview, ${me?.name}`}
        sub="Adjudicate the asset map, approve actions, and watch the moat compound." />

      {/* Bridge readout — single-glance status strip (design.md) */}
      <div className="grid-4">
        <StatTile label="Resolutions to adjudicate" value={queue.n} accent="var(--signal)"
          hint="four names → one pump" onClick={() => nav("/assets")} />
        <StatTile label="Actions awaiting approval" value={pending} accent={pending ? "var(--decision)" : "var(--ink)"}
          hint="gated writes (CP-3)" onClick={() => nav("/execution")} />
        <StatTile label="Resolution corpus" value={queue.corpus} accent="var(--knowledge)"
          hint="the moat, compounding" onClick={() => nav("/analytics")} />
        <StatTile label="Knowledge risks" value={risks} accent={risks ? "var(--warning)" : "var(--ink)"}
          hint="stale / decayed facts" onClick={() => nav("/knowledge")} />
      </div>

      <div className="grid-2">
        <Panel title="Decision analytics" action={<button className="btn btn-tertiary" onClick={() => nav("/analytics")}>Full dashboard</button>}>
          {kpis.filter((k) => ["recurrence_rate", "wo_from_prahari", "correction_to_improvement"].includes(k.key)).map((k) => (
            <div key={k.key} className="row between center" style={{ padding: "6px 0", borderBottom: "1px solid var(--hairline-soft)" }}>
              <span className="t-body-sm">{k.label}</span>
              <span className="t-body-sm tabular ink-muted">actual {String(k.actual ?? "—")} · target {k.target}</span>
            </div>
          ))}
          {corpusKpi && <div className="t-metadata" style={{ marginTop: "var(--sp-sm)" }}>Targets are estimates pending eval validation — never shown as achieved.</div>}
        </Panel>
        <Panel title="Jump to" >
          <div className="col" style={{ gap: "var(--sp-sm)" }}>
            <button className="btn btn-secondary" onClick={() => nav("/compliance")}>Compliance Intelligence</button>
            <button className="btn btn-secondary" onClick={() => nav("/replay")}>Decision Memory &amp; Replay</button>
            <button className="btn btn-secondary" onClick={() => nav("/investigate")}>Run an investigation</button>
          </div>
        </Panel>
      </div>
    </div>
  );
}

// ========================================================= COMPLIANCE — Compliance officer view
function ComplianceDashboard() {
  const { me } = useAuth();
  const nav = useNavigate();
  const [overdue, setOverdue] = useState<any[]>([]);
  const [coverage, setCoverage] = useState<any>(null);

  useEffect(() => {
    (async () => {
      try {
        const { assets } = await api.assets();
        const rows: any[] = [];
        let cov = null;
        for (const a of assets) {
          const d = await api.compliance(a.id);
          cov = d.coverage;
          rows.push(...d.rows.filter((r) => r.status === "overdue"));
        }
        setOverdue(rows);
        setCoverage(cov);
      } catch { /* view-only */ }
    })();
  }, []);

  return (
    <div className="col">
      <DashHeader eyebrow="Compliance" title={`Compliance posture, ${me?.name}`}
        sub="Evidence and gaps against statutory instruments — never a legal opinion." />

      <div className="grid-4">
        <StatTile label="Overdue obligations" value={overdue.length} accent={overdue.length ? "var(--critical)" : "var(--success)"}
          hint="genuine gaps only" onClick={() => nav("/compliance")} />
        <StatTile label="Clauses encoded" value={coverage ? `${coverage.encoded_clauses}/${coverage.total_applicable_clauses}` : "—"}
          accent="var(--evidence)" hint="not a completeness guarantee" onClick={() => nav("/compliance")} />
      </div>

      <Panel title="Overdue obligations — walk-in evidence pack" action={<button className="btn btn-tertiary" onClick={() => nav("/compliance")}>Open matrix</button>}>
        {overdue.length === 0 ? (
          <div className="t-body-sm ink-muted">No overdue obligations across encoded clauses.</div>
        ) : (
          overdue.map((r) => (
            <div key={r.clause + r.asset_id} className="row between center" style={{ padding: "6px 0", borderBottom: "1px solid var(--hairline-soft)" }}>
              <span className="t-body-sm t-mono">{r.clause} · {r.asset_tag}</span>
              <Badge kind="critical">Overdue</Badge>
            </div>
          ))
        )}
      </Panel>
      {coverage && <div className="card card-dense" style={{ borderLeft: "3px solid var(--evidence)" }}><span className="t-body-sm">{coverage.disclaimer}</span></div>}
    </div>
  );
}

// =============================================================== ADMIN — Security view (Deepak)
function AdminDashboard() {
  const { me } = useAuth();
  const nav = useNavigate();
  const [audit, setAudit] = useState<any[]>([]);
  const [ingest, setIngest] = useState<{ jobs: number; quarantined: number }>({ jobs: 0, quarantined: 0 });
  const [health, setHealth] = useState<any>(null);
  const [risks, setRisks] = useState(0);

  useEffect(() => {
    api.audit().then((a) => setAudit(a.entries.slice(0, 8))).catch(() => {});
    api.ingestionJobs().then((d) => setIngest({ jobs: d.jobs.length, quarantined: d.quarantined.length })).catch(() => {});
    api.health().then(setHealth).catch(() => {});
    api.knowledgeHealth().then((k) => setRisks(k.flags.length)).catch(() => {});
  }, []);

  const writeEvents = audit.filter((e) => /submitted|adjudicated|correction|unmerged/.test(e.action)).length;

  return (
    <div className="col">
      <DashHeader eyebrow="OT Security &amp; Admin" title={`Guardian console, ${me?.name}`}
        sub="Every write is attributed and audited; nothing leaves the boundary." />

      <div className="grid-4">
        <StatTile label="System state" value={health ? (health.forced_rung === "full" ? "Full" : health.forced_rung) : "—"}
          accent={health?.forced_rung === "full" ? "var(--success)" : "var(--warning)"} hint="CP-9 degradation rung" />
        <StatTile label="Write events (recent)" value={writeEvents} accent="var(--decision)" hint="all attributed (CP-3)" onClick={() => nav("/audit")} />
        <StatTile label="Documents ingested" value={ingest.jobs} accent="var(--knowledge)" hint={`${ingest.quarantined} quarantined`} onClick={() => nav("/admin")} />
        <StatTile label="Knowledge risks" value={risks} accent={risks ? "var(--warning)" : "var(--ink)"} onClick={() => nav("/knowledge")} />
      </div>

      <div className="grid-2">
        <Panel title="Recent audit trail" action={<button className="btn btn-tertiary" onClick={() => nav("/audit")}>Full log</button>}>
          {audit.length === 0 ? <div className="t-body-sm ink-muted">No activity.</div> : (
            audit.map((e) => (
              <div key={e.entry_id} className="row between center" style={{ padding: "4px 0" }}>
                <span className="t-metadata t-mono">{e.action}</span>
                <span className="t-metadata ink-subtle">{e.actor} · {new Date(e.ts).toLocaleTimeString()}</span>
              </div>
            ))
          )}
        </Panel>
        <Panel title="Guardian controls">
          <div className="col" style={{ gap: "var(--sp-sm)" }}>
            <button className="btn btn-secondary" onClick={() => nav("/admin")}>Ingestion &amp; RBAC</button>
            <button className="btn btn-secondary" onClick={() => nav("/audit")}>Audit &amp; Provenance</button>
            <button className="btn btn-secondary" onClick={() => nav("/field")}>Field Mode (degradation demo)</button>
          </div>
        </Panel>
      </div>
    </div>
  );
}

// =============================================================== AUDITOR — read-only oversight
function AuditorDashboard() {
  const { me } = useAuth();
  const nav = useNavigate();
  const [audit, setAudit] = useState<any[]>([]);
  useEffect(() => { api.audit().then((a) => setAudit(a.entries.slice(0, 12))).catch(() => {}); }, []);
  return (
    <div className="col">
      <DashHeader eyebrow="Auditor" title={`Audit overview, ${me?.name}`}
        sub="Append-only, reproducible. Read-only by design." />
      <StatTile label="Recorded events (recent)" value={audit.length} accent="var(--signal)" onClick={() => nav("/audit")} />
      <Panel title="Recent activity" action={<button className="btn btn-tertiary" onClick={() => nav("/audit")}>Full log</button>}>
        {audit.map((e) => (
          <div key={e.entry_id} className="row between center" style={{ padding: "4px 0" }}>
            <span className="t-metadata t-mono">{e.action}</span>
            <span className="t-metadata ink-subtle">{e.actor} · {new Date(e.ts).toLocaleString()}</span>
          </div>
        ))}
      </Panel>
    </div>
  );
}

// ==================================================================================== switch
export function Home() {
  const { me } = useAuth();
  switch (me?.role) {
    case "technician":
      return <OperatorDashboard />;
    case "reliability":
      return <ReliabilityDashboard />;
    case "compliance":
      return <ComplianceDashboard />;
    case "admin":
      return <AdminDashboard />;
    case "auditor":
      return <AuditorDashboard />;
    default:
      return <OperatorDashboard />;
  }
}
