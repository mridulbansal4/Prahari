// GraphCanvas — full-bleed data canvas (radius 0), renders the traversal hop-by-hop as it is
// retrieved (Bible §7.4, §10.5). Reduced-motion users get the linear TraversalTrace instead
// (accessibility, PRB §3.7). Node colour neutral; investigation-indigo carries thread chrome.
import type { GraphHop } from "../lib/types";

const LABEL_COLOR: Record<string, string> = {
  Asset: "var(--ink-muted)",
  FailureMode: "var(--critical)",
  Inspection: "var(--evidence)",
  Incident: "var(--warning)",
  Sensor: "var(--knowledge)",
  Identifier: "var(--investigation)",
};

export function GraphCanvas({ hops }: { hops: GraphHop[] }) {
  // Lay hops out on a simple vertical spine; edges labelled between nodes.
  const nodes = hops.filter((h) => h.node);
  const width = 520;
  const rowH = 78;
  const height = Math.max(220, nodes.length * rowH + 40);
  return (
    <div className="canvas" style={{ padding: 0, overflow: "auto", height: "100%", minHeight: 320 }}>
      <div
        className="row between center"
        style={{ padding: "var(--sp-sm) var(--sp-md)", position: "sticky", top: 0, background: "var(--surface-inset)" }}
      >
        <span className="t-label" style={{ color: "var(--investigation)" }}>
          Traversal
        </span>
        <span className="t-metadata">{nodes.length} nodes</span>
      </div>
      <svg width={width} height={height} style={{ display: "block", margin: "0 auto" }}>
        {nodes.map((h, i) => {
          const y = 40 + i * rowH;
          const prevY = 40 + (i - 1) * rowH;
          const color = LABEL_COLOR[h.node_label ?? ""] ?? "var(--ink-muted)";
          return (
            <g key={i}>
              {i > 0 && (
                <>
                  <line
                    x1={width / 2}
                    y1={prevY + 22}
                    x2={width / 2}
                    y2={y - 22}
                    stroke="var(--hairline-strong)"
                    strokeWidth={1.5}
                  />
                  {hops[hops.indexOf(h)]?.edge && (
                    <text
                      x={width / 2 + 10}
                      y={(prevY + y) / 2 + 4}
                      fill="var(--ink-subtle)"
                      fontSize={10}
                      fontFamily="var(--font-mono)"
                    >
                      {h.edge}
                    </text>
                  )}
                </>
              )}
              <circle cx={width / 2} cy={y} r={9} fill="var(--surface-inset)" stroke={color} strokeWidth={2} />
              <text x={width / 2 + 22} y={y - 2} fill="var(--ink)" fontSize={13}>
                {h.detail ?? h.node}
              </text>
              <text x={width / 2 + 22} y={y + 13} fill="var(--ink-faint)" fontSize={10} letterSpacing="0.06em">
                {(h.node_label ?? "").toUpperCase()}
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
}

/** Static linear equivalent for Field Mode / reduced motion (PRB §3.7, §2.13). */
export function TraversalTrace({ hops }: { hops: GraphHop[] }) {
  return (
    <ol className="col" style={{ gap: "var(--sp-xs)", listStyle: "none" }}>
      {hops
        .filter((h) => h.node)
        .map((h, i) => (
          <li key={i} className="row center" style={{ gap: "var(--sp-sm)" }}>
            {h.edge && <span className="t-metadata t-mono">{h.edge} ›</span>}
            <span className="t-body-sm">{h.detail ?? h.node}</span>
            <span className="t-metadata">{h.node_label}</span>
          </li>
        ))}
    </ol>
  );
}
