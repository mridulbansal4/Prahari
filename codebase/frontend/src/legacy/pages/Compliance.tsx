// M6 Compliance Intelligence (PRB §2.4) — obligations vs graph state. The honest coverage footer
// is mandatory on every view (BR-3/FM-6); silence over noise — only genuine gaps are emphasized.
import { useEffect, useState } from "react";
import { Badge } from "../components/primitives";
import { api } from "../lib/api";
import type { ComplianceRow, Coverage } from "../lib/types";

export function Compliance() {
  const [rows, setRows] = useState<ComplianceRow[]>([]);
  const [coverage, setCoverage] = useState<Coverage | null>(null);
  const [assets, setAssets] = useState<{ id: string; tag: string; name: string }[]>([]);
  const [assetId, setAssetId] = useState<string>("");

  // Load the tenant's assets and default to the first — no hardcoded asset id.
  useEffect(() => {
    api.assets().then((d) => {
      setAssets(d.assets);
      if (d.assets.length && !assetId) setAssetId(d.assets[0].id);
    });
  }, []);

  useEffect(() => {
    if (!assetId) return;
    api.compliance(assetId).then((d) => {
      setRows(d.rows);
      setCoverage(d.coverage);
    });
  }, [assetId]);

  return (
    <div className="col">
      <div className="row between center wrap">
        <div>
          <div className="t-label">Compliance Intelligence</div>
          <div className="t-display-md">Evidence and gaps — never a legal opinion</div>
        </div>
        <div className="col" style={{ gap: "var(--sp-xs)" }}>
          <label className="t-label">Asset</label>
          <select className="input" value={assetId} onChange={(e) => setAssetId(e.target.value)} style={{ minWidth: 220 }}>
            {assets.map((a) => (
              <option key={a.id} value={a.id}>
                {a.tag} — {a.name}
              </option>
            ))}
          </select>
        </div>
      </div>
      <div className="card" style={{ padding: 0 }}>
        <table className="grid-table">
          <thead>
            <tr>
              <th>Clause</th>
              <th>Instrument</th>
              <th>Asset</th>
              <th>Periodicity</th>
              <th>Last evidence</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((r) => (
              <tr key={r.clause}>
                <td className="t-mono">{r.clause}</td>
                <td>{r.instrument}</td>
                <td>{r.asset_tag}</td>
                <td className="tabular">{r.periodicity_months} mo</td>
                <td>{r.last_evidence_date ?? "—"}</td>
                <td>
                  {r.status === "overdue" ? (
                    <Badge kind="critical">Overdue</Badge>
                  ) : r.status === "due" ? (
                    <Badge kind="warning">Due</Badge>
                  ) : (
                    <Badge kind="success">Satisfied</Badge>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* The mandatory, always-visible coverage footer — never collapsible (PRB §2.4). */}
      {coverage && (
        <div className="card card-dense" style={{ borderLeft: "3px solid var(--evidence)" }}>
          <div className="t-label" style={{ color: "var(--evidence)" }}>Coverage</div>
          <div className="t-body-sm">{coverage.disclaimer}</div>
          <div className="row wrap" style={{ gap: "var(--sp-lg)", marginTop: "var(--sp-sm)" }}>
            {Object.entries(coverage.by_instrument).map(([inst, v]) => (
              <span key={inst} className="t-metadata">
                {inst}: <span className="tabular" style={{ color: "var(--ink)" }}>{v.encoded}/{v.total}</span> clauses encoded
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
