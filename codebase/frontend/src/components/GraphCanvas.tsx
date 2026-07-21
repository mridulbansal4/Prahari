// Knowledge map — renders the traversal hop-by-hop as it is retrieved. Data source and shape
// are unchanged; this is a restyle onto the editorial light canvas.
//
// Node kind is carried by SHAPE, not colour, so the map stays legible in greyscale and under
// every form of colour blindness. The legend below names each shape.
import type { GraphHop } from "../lib/types";

export type NodeKind =
  | "Asset"
  | "FailureMode"
  | "Inspection"
  | "Incident"
  | "Sensor"
  | "Identifier"
  | "WorkOrder";

export const NODE_LEGEND: { kind: NodeKind; label: string }[] = [
  { kind: "Asset", label: "Equipment" },
  { kind: "FailureMode", label: "Failure mode" },
  { kind: "Inspection", label: "Inspection" },
  { kind: "Incident", label: "Incident" },
  { kind: "Sensor", label: "Sensor" },
  { kind: "Identifier", label: "Other name for it" },
  { kind: "WorkOrder", label: "Work order" },
];

/** One glyph per node kind. Shape is the signal; everything is ink on white. */
export function NodeGlyph({ kind, cx, cy, r = 9 }: { kind: string; cx: number; cy: number; r?: number }) {
  const ink = "var(--ink)";
  const paper = "var(--surface-card)";
  switch (kind) {
    case "Asset":
      return <circle cx={cx} cy={cy} r={r} fill={ink} />;
    case "FailureMode":
      return (
        <polygon
          points={`${cx},${cy - r} ${cx + r},${cy + r * 0.8} ${cx - r},${cy + r * 0.8}`}
          fill={paper}
          stroke={ink}
          strokeWidth={1.75}
        />
      );
    case "Incident":
      return (
        <rect
          x={cx - r * 0.8}
          y={cy - r * 0.8}
          width={r * 1.6}
          height={r * 1.6}
          fill={paper}
          stroke={ink}
          strokeWidth={1.75}
          transform={`rotate(45 ${cx} ${cy})`}
        />
      );
    case "Inspection":
      return (
        <rect
          x={cx - r * 0.85}
          y={cy - r * 0.85}
          width={r * 1.7}
          height={r * 1.7}
          rx={2}
          fill={paper}
          stroke={ink}
          strokeWidth={1.75}
        />
      );
    case "Sensor":
      return <circle cx={cx} cy={cy} r={r * 0.55} fill={paper} stroke={ink} strokeWidth={1.75} />;
    case "Identifier":
      return (
        <circle
          cx={cx}
          cy={cy}
          r={r}
          fill={paper}
          stroke={ink}
          strokeWidth={1.5}
          strokeDasharray="3 2.5"
        />
      );
    case "WorkOrder":
      return (
        <rect
          x={cx - r}
          y={cy - r * 0.7}
          width={r * 2}
          height={r * 1.4}
          rx={2}
          fill={paper}
          stroke={ink}
          strokeWidth={1.75}
        />
      );
    // --- reasoning-chain kinds, used by the decision replay path ---
    case "Decision":
      // The committed choice: solid, like an Asset — this is the thing that happened.
      return <circle cx={cx} cy={cy} r={r} fill={ink} />;
    case "Alternative":
      // Considered and not taken — dashed, so "rejected" reads without colour.
      return (
        <rect
          x={cx - r * 0.85}
          y={cy - r * 0.85}
          width={r * 1.7}
          height={r * 1.7}
          rx={2}
          fill={paper}
          stroke={ink}
          strokeWidth={1.5}
          strokeDasharray="3 2.5"
        />
      );
    case "Hypothesis":
      return (
        <circle
          cx={cx}
          cy={cy}
          r={r}
          fill={paper}
          stroke={ink}
          strokeWidth={1.5}
          strokeDasharray="3 2.5"
        />
      );
    case "Observation":
      return <circle cx={cx} cy={cy} r={r * 0.6} fill={ink} opacity={0.55} />;
    case "Evidence":
      return (
        <rect
          x={cx - r * 0.85}
          y={cy - r * 0.85}
          width={r * 1.7}
          height={r * 1.7}
          rx={2}
          fill={paper}
          stroke={ink}
          strokeWidth={1.75}
        />
      );
    case "RiskAccepted":
      return (
        <polygon
          points={`${cx},${cy - r} ${cx + r},${cy + r * 0.8} ${cx - r},${cy + r * 0.8}`}
          fill={paper}
          stroke={ink}
          strokeWidth={1.5}
          strokeDasharray="3 2"
        />
      );
    case "Outcome":
      return (
        <>
          <circle cx={cx} cy={cy} r={r} fill={paper} stroke={ink} strokeWidth={1.75} />
          <circle cx={cx} cy={cy} r={r * 0.45} fill={ink} />
        </>
      );
    case "LessonLearned":
      return (
        <rect
          x={cx - r * 0.8}
          y={cy - r * 0.8}
          width={r * 1.6}
          height={r * 1.6}
          fill={ink}
          transform={`rotate(45 ${cx} ${cy})`}
        />
      );
    default:
      return <circle cx={cx} cy={cy} r={r} fill={paper} stroke={ink} strokeWidth={1.75} />;
  }
}

/** Legend for a replayed decision chain — separate from the plant legend above so the
 *  knowledge map is not cluttered with reasoning kinds it never renders. */
export const DECISION_LEGEND: { kind: string; label: string }[] = [
  { kind: "Observation", label: "What was seen" },
  { kind: "Hypothesis", label: "Working theory" },
  { kind: "Evidence", label: "Evidence" },
  { kind: "Decision", label: "Decision taken" },
  { kind: "Alternative", label: "Option rejected" },
  { kind: "RiskAccepted", label: "Risk accepted" },
  { kind: "Outcome", label: "What happened" },
  { kind: "LessonLearned", label: "Lesson" },
];

export function LegendRow({ items }: { items: { kind: string; label: string }[] }) {
  return (
    <div className="row" style={{ gap: "var(--sp-base)", flexWrap: "wrap", rowGap: "var(--sp-xs)" }}>
      {items.map(({ kind, label }) => (
        <span key={kind} className="row" style={{ gap: "var(--sp-xxs)" }}>
          <svg width={20} height={20} aria-hidden="true">
            <NodeGlyph kind={kind} cx={10} cy={10} r={6} />
          </svg>
          <span className="t-caption">{label}</span>
        </span>
      ))}
    </div>
  );
}

export function GraphLegend() {
  return (
    <div
      className="row"
      style={{ gap: "var(--sp-base)", flexWrap: "wrap", rowGap: "var(--sp-xs)" }}
    >
      {NODE_LEGEND.map(({ kind, label }) => (
        <span key={kind} className="row" style={{ gap: "var(--sp-xxs)" }}>
          <svg width={20} height={20} aria-hidden="true">
            <NodeGlyph kind={kind} cx={10} cy={10} r={6} />
          </svg>
          <span className="t-caption">{label}</span>
        </span>
      ))}
    </div>
  );
}

export function GraphCanvas({ hops }: { hops: GraphHop[] }) {
  const nodes = hops.filter((h) => h.node);
  const width = 520;
  const rowH = 78;
  const height = Math.max(220, nodes.length * rowH + 48);

  if (!nodes.length) return null;

  return (
    <div
      style={{
        background: "var(--canvas-soft)",
        border: "1px solid var(--hairline)",
        borderRadius: "var(--r-xl)",
        overflow: "auto",
        maxHeight: 560,
      }}
    >
      <div
        className="row"
        style={{
          justifyContent: "space-between",
          padding: "var(--sp-sm) var(--sp-base)",
          position: "sticky",
          top: 0,
          background: "var(--canvas-soft)",
          borderBottom: "1px solid var(--hairline)",
          zIndex: 1,
        }}
      >
        <span className="t-label">How it connected the dots</span>
        <span className="t-caption">{nodes.length} steps</span>
      </div>
      <svg
        width={width}
        height={height}
        style={{ display: "block", margin: "0 auto" }}
        role="img"
        aria-label={`Traversal across ${nodes.length} connected records`}
      >
        {nodes.map((h, i) => {
          const y = 40 + i * rowH;
          const prevY = 40 + (i - 1) * rowH;
          const cx = 84;
          return (
            <g key={i}>
              {i > 0 && (
                <>
                  <line
                    x1={cx}
                    y1={prevY + 20}
                    x2={cx}
                    y2={y - 20}
                    stroke="var(--hairline-strong)"
                    strokeWidth={1.5}
                  />
                  {h.edge && (
                    <text
                      x={cx + 14}
                      y={(prevY + y) / 2 + 4}
                      fill="var(--muted)"
                      fontSize={11}
                      fontFamily="var(--font-body)"
                    >
                      {h.edge.toLowerCase().replace(/_/g, " ")}
                    </text>
                  )}
                </>
              )}
              <NodeGlyph kind={h.node_label ?? ""} cx={cx} cy={y} />
              <text
                x={cx + 24}
                y={y - 1}
                fill="var(--ink)"
                fontSize={14}
                fontFamily="var(--font-body)"
              >
                {h.detail ?? h.node}
              </text>
              <text
                x={cx + 24}
                y={y + 15}
                fill="var(--muted)"
                fontSize={11}
                fontFamily="var(--font-body)"
                letterSpacing="0.5"
              >
                {NODE_LEGEND.find((n) => n.kind === h.node_label)?.label ?? h.node_label}
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
}

/** Static linear equivalent for reduced-motion and narrow viewports. */
export function TraversalTrace({ hops }: { hops: GraphHop[] }) {
  return (
    <ol className="stack" style={{ gap: "var(--sp-xs)", listStyle: "none" }}>
      {hops
        .filter((h) => h.node)
        .map((h, i) => (
          <li key={i} className="row" style={{ gap: "var(--sp-xs)", flexWrap: "wrap" }}>
            {h.edge && (
              <span className="t-caption">{h.edge.toLowerCase().replace(/_/g, " ")} ›</span>
            )}
            <span className="t-body-sm ink">{h.detail ?? h.node}</span>
            <span className="t-caption muted-soft">{h.node_label}</span>
          </li>
        ))}
    </ol>
  );
}
