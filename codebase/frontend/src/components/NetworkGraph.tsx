// Interactive network graph. Replaces the old vertical spine — this is a real node/edge
// network with pan, zoom, hover-highlight, click-to-inspect and filtering.
//
// No graph library: a small force-directed layout runs synchronously on mount (fast for the
// hundreds of nodes this corpus produces) so there is no animation loop burning CPU and
// nothing to tear down. Node kind is carried by SHAPE, never colour.
import { useEffect, useMemo, useRef, useState } from "react";
import { NodeGlyph, NODE_LEGEND } from "./GraphCanvas";

export interface NetNode {
  id: string;
  kind: string;
  detail: string;
}
export interface NetLink {
  source: string;
  target: string;
  edge: string;
}

interface Positioned extends NetNode {
  x: number;
  y: number;
}

/**
 * Force-directed layout: link springs + all-pairs repulsion + weak centering gravity.
 * Deterministic — seeded from a circle, no randomness — so the map doesn't reshuffle
 * between renders.
 */
function layout(nodes: NetNode[], links: NetLink[], w: number, h: number): Positioned[] {
  const n = nodes.length;
  if (!n) return [];
  const cx = w / 2;
  const cy = h / 2;
  const radius = Math.min(w, h) * 0.36;

  const pos: Positioned[] = nodes.map((node, i) => ({
    ...node,
    x: cx + radius * Math.cos((2 * Math.PI * i) / n),
    y: cy + radius * Math.sin((2 * Math.PI * i) / n),
  }));
  const index = new Map(pos.map((p, i) => [p.id, i]));

  const edges = links
    .map((l) => ({ s: index.get(l.source), t: index.get(l.target) }))
    .filter((e): e is { s: number; t: number } => e.s !== undefined && e.t !== undefined);

  const IDEAL = Math.max(90, Math.min(w, h) / Math.sqrt(n + 1));
  const REPULSION = IDEAL * IDEAL * 0.9;

  for (let step = 0; step < 320; step++) {
    const cool = 1 - step / 320;
    const dx = new Float64Array(n);
    const dy = new Float64Array(n);

    // Repulsion — every pair pushes apart.
    for (let i = 0; i < n; i++) {
      for (let j = i + 1; j < n; j++) {
        let ax = pos[i].x - pos[j].x;
        let ay = pos[i].y - pos[j].y;
        let d2 = ax * ax + ay * ay;
        if (d2 < 0.01) {
          ax = (i - j) * 0.5 + 0.6;
          ay = (j - i) * 0.35 + 0.4;
          d2 = ax * ax + ay * ay;
        }
        const f = REPULSION / d2;
        const d = Math.sqrt(d2);
        const ux = (ax / d) * f;
        const uy = (ay / d) * f;
        dx[i] += ux;
        dy[i] += uy;
        dx[j] -= ux;
        dy[j] -= uy;
      }
    }

    // Link springs — connected nodes pull to the ideal distance.
    for (const { s, t } of edges) {
      const ax = pos[t].x - pos[s].x;
      const ay = pos[t].y - pos[s].y;
      const d = Math.max(0.01, Math.hypot(ax, ay));
      const f = (d - IDEAL) * 0.08;
      const ux = (ax / d) * f;
      const uy = (ay / d) * f;
      dx[s] += ux;
      dy[s] += uy;
      dx[t] -= ux;
      dy[t] -= uy;
    }

    // Weak gravity keeps disconnected components from drifting off-canvas.
    for (let i = 0; i < n; i++) {
      dx[i] += (cx - pos[i].x) * 0.012;
      dy[i] += (cy - pos[i].y) * 0.012;
      const max = 26 * cool;
      const m = Math.hypot(dx[i], dy[i]);
      const scale = m > max ? max / m : 1;
      pos[i].x += dx[i] * scale;
      pos[i].y += dy[i] * scale;
    }
  }
  return pos;
}

const KIND_LABEL = (kind: string) =>
  NODE_LEGEND.find((n) => n.kind === kind)?.label ?? kind;

export function NetworkGraph({
  nodes,
  links,
  height = 560,
  onAskAbout,
  emptyHint,
  layout: shellLayout = "split",
}: {
  nodes: NetNode[];
  links: NetLink[];
  height?: number;
  onAskAbout?: (node: NetNode) => void;
  emptyHint?: string;
  /** "stacked" puts the inspector below the canvas — for narrow panels, where splitting
   *  side-by-side would crush the graph into an unreadable strip. */
  layout?: "split" | "stacked";
}) {
  const W = 900;
  const H = height;
  const wrap = useRef<HTMLDivElement>(null);

  const [hidden, setHidden] = useState<Set<string>>(new Set());
  const [hover, setHover] = useState<string | null>(null);
  const [selected, setSelected] = useState<string | null>(null);
  const [view, setView] = useState({ x: 0, y: 0, k: 1 });
  const drag = useRef<{ x: number; y: number; vx: number; vy: number } | null>(null);

  const kinds = useMemo(() => [...new Set(nodes.map((n) => n.kind))], [nodes]);

  const visibleNodes = useMemo(
    () => nodes.filter((n) => !hidden.has(n.kind)),
    [nodes, hidden],
  );
  const visibleIds = useMemo(() => new Set(visibleNodes.map((n) => n.id)), [visibleNodes]);
  const visibleLinks = useMemo(
    () => links.filter((l) => visibleIds.has(l.source) && visibleIds.has(l.target)),
    [links, visibleIds],
  );

  const positioned = useMemo(
    () => layout(visibleNodes, visibleLinks, W, H),
    [visibleNodes, visibleLinks, H],
  );
  const byId = useMemo(() => new Map(positioned.map((p) => [p.id, p])), [positioned]);

  // Neighbours of the hovered/selected node, for the highlight pass.
  const focus = hover ?? selected;
  const neighbours = useMemo(() => {
    if (!focus) return null;
    const set = new Set<string>([focus]);
    for (const l of visibleLinks) {
      if (l.source === focus) set.add(l.target);
      if (l.target === focus) set.add(l.source);
    }
    return set;
  }, [focus, visibleLinks]);

  // Wheel zoom, bound non-passively so preventDefault actually applies.
  useEffect(() => {
    const el = wrap.current;
    if (!el) return;
    const onWheel = (e: WheelEvent) => {
      e.preventDefault();
      setView((v) => ({
        ...v,
        k: Math.min(2.6, Math.max(0.35, v.k * (e.deltaY < 0 ? 1.12 : 0.89))),
      }));
    };
    el.addEventListener("wheel", onWheel, { passive: false });
    return () => el.removeEventListener("wheel", onWheel);
  }, []);

  const selectedNode = selected ? nodes.find((n) => n.id === selected) : null;
  const selectedLinks = selected
    ? links.filter((l) => l.source === selected || l.target === selected)
    : [];

  if (!nodes.length) {
    return (
      <div
        className="card"
        style={{
          borderStyle: "dashed",
          background: "var(--canvas-soft)",
          textAlign: "center",
          padding: "var(--sp-xxl)",
        }}
      >
        <p className="t-body">{emptyHint ?? "Nothing to map yet."}</p>
      </div>
    );
  }

  return (
    <div className="stack" style={{ gap: "var(--sp-sm)" }}>
      {/* Toolbar: filter by kind + zoom */}
      <div
        className="row"
        style={{ gap: "var(--sp-xs)", flexWrap: "wrap", justifyContent: "space-between" }}
      >
        <div className="row" style={{ gap: "var(--sp-xxs)", flexWrap: "wrap" }}>
          {kinds.map((k) => {
            const off = hidden.has(k);
            return (
              <button
                key={k}
                type="button"
                onClick={() =>
                  setHidden((prev) => {
                    const next = new Set(prev);
                    if (next.has(k)) next.delete(k);
                    else next.add(k);
                    return next;
                  })
                }
                aria-pressed={!off}
                title={off ? `Show ${KIND_LABEL(k)}` : `Hide ${KIND_LABEL(k)}`}
                style={{
                  display: "inline-flex",
                  alignItems: "center",
                  gap: 5,
                  font: "var(--t-caption)",
                  color: off ? "var(--muted-soft)" : "var(--ink)",
                  background: off ? "transparent" : "var(--surface-strong)",
                  border: `1px solid ${off ? "var(--hairline-strong)" : "transparent"}`,
                  borderRadius: "var(--r-pill)",
                  padding: "4px 10px",
                  cursor: "pointer",
                  textDecoration: off ? "line-through" : "none",
                  minHeight: 30,
                }}
              >
                <svg width={14} height={14} aria-hidden="true">
                  <NodeGlyph kind={k} cx={7} cy={7} r={4.5} />
                </svg>
                {KIND_LABEL(k)}
              </button>
            );
          })}
        </div>
        <div className="row" style={{ gap: "var(--sp-xxs)" }}>
          <button
            type="button"
            className="btn btn--outline"
            style={{ minHeight: 30, padding: "4px 12px" }}
            onClick={() => setView((v) => ({ ...v, k: Math.max(0.35, v.k * 0.85) }))}
            aria-label="Zoom out"
          >
            −
          </button>
          <button
            type="button"
            className="btn btn--outline"
            style={{ minHeight: 30, padding: "4px 12px" }}
            onClick={() => setView((v) => ({ ...v, k: Math.min(2.6, v.k * 1.18) }))}
            aria-label="Zoom in"
          >
            +
          </button>
          <button
            type="button"
            className="btn btn--outline"
            style={{ minHeight: 30, padding: "4px 12px" }}
            onClick={() => {
              setView({ x: 0, y: 0, k: 1 });
              setSelected(null);
            }}
          >
            Reset
          </button>
        </div>
      </div>

      <div
        className={shellLayout === "split" ? "map-shell" : ""}
        style={{ display: "grid", gap: "var(--sp-base)", alignItems: "start" }}
      >
        <div
          ref={wrap}
          style={{
            background: "var(--canvas-soft)",
            border: "1px solid var(--hairline)",
            borderRadius: "var(--r-xl)",
            overflow: "hidden",
            cursor: drag.current ? "grabbing" : "grab",
            position: "relative",
          }}
          onPointerDown={(e) => {
            drag.current = { x: e.clientX, y: e.clientY, vx: view.x, vy: view.y };
            (e.target as Element).setPointerCapture?.(e.pointerId);
          }}
          onPointerMove={(e) => {
            if (!drag.current) return;
            setView((v) => ({
              ...v,
              x: drag.current!.vx + (e.clientX - drag.current!.x),
              y: drag.current!.vy + (e.clientY - drag.current!.y),
            }));
          }}
          onPointerUp={() => {
            drag.current = null;
          }}
          onPointerLeave={() => {
            drag.current = null;
            setHover(null);
          }}
        >
          <svg
            width="100%"
            height={H}
            viewBox={`0 0 ${W} ${H}`}
            role="img"
            aria-label={`Knowledge map: ${visibleNodes.length} records connected by ${visibleLinks.length} relationships`}
            style={{ display: "block", touchAction: "none" }}
          >
            <g transform={`translate(${view.x} ${view.y}) scale(${view.k})`}>
              {visibleLinks.map((l, i) => {
                const a = byId.get(l.source);
                const b = byId.get(l.target);
                if (!a || !b) return null;
                const dim = neighbours && !(neighbours.has(l.source) && neighbours.has(l.target));
                const mx = (a.x + b.x) / 2;
                const my = (a.y + b.y) / 2;
                return (
                  <g key={i} opacity={dim ? 0.15 : 1}>
                    <line
                      x1={a.x}
                      y1={a.y}
                      x2={b.x}
                      y2={b.y}
                      stroke="var(--hairline-strong)"
                      strokeWidth={1.25}
                    />
                    {(view.k > 0.85 || focus) && !dim && (
                      <text
                        x={mx}
                        y={my - 3}
                        fill="var(--muted)"
                        fontSize={9.5}
                        fontFamily="var(--font-body)"
                        textAnchor="middle"
                      >
                        {l.edge.toLowerCase().replace(/_/g, " ")}
                      </text>
                    )}
                  </g>
                );
              })}

              {positioned.map((p) => {
                const dim = neighbours && !neighbours.has(p.id);
                const isFocus = focus === p.id;
                return (
                  <g
                    key={p.id}
                    opacity={dim ? 0.2 : 1}
                    style={{ cursor: "pointer" }}
                    onPointerEnter={() => setHover(p.id)}
                    onPointerLeave={() => setHover(null)}
                    onClick={(e) => {
                      e.stopPropagation();
                      setSelected(selected === p.id ? null : p.id);
                    }}
                  >
                    {isFocus && (
                      <circle cx={p.x} cy={p.y} r={17} fill="none" stroke="var(--ink)" strokeWidth={1} />
                    )}
                    <circle cx={p.x} cy={p.y} r={14} fill="var(--canvas-soft)" />
                    <NodeGlyph kind={p.kind} cx={p.x} cy={p.y} r={8} />
                    {(view.k > 0.7 || isFocus) && (
                      <text
                        x={p.x}
                        y={p.y + 25}
                        fill="var(--ink)"
                        fontSize={11}
                        fontFamily="var(--font-body)"
                        textAnchor="middle"
                      >
                        {p.detail.length > 22 ? `${p.detail.slice(0, 21)}…` : p.detail}
                      </text>
                    )}
                  </g>
                );
              })}
            </g>
          </svg>

          <div
            className="t-caption"
            style={{
              position: "absolute",
              bottom: 8,
              left: 12,
              color: "var(--muted-soft)",
              pointerEvents: "none",
            }}
          >
            Drag to move · scroll to zoom · click a node for detail
          </div>
        </div>

        {/* Inspector */}
        <div className="card">
          {!selectedNode && (
            <>
              <div className="t-label" style={{ marginBottom: "var(--sp-xs)" }}>
                Inspector
              </div>
              <p className="t-body-sm">
                Click any node to see what it is, what it connects to, and to ask a question
                about it.
              </p>
              <p className="t-caption" style={{ marginTop: "var(--sp-sm)" }}>
                Showing {visibleNodes.length} of {nodes.length} records ·{" "}
                {visibleLinks.length} connections
              </p>
            </>
          )}
          {selectedNode && (
            <>
              <div
                className="row"
                style={{ gap: "var(--sp-xs)", marginBottom: "var(--sp-xs)" }}
              >
                <svg width={20} height={20} aria-hidden="true">
                  <NodeGlyph kind={selectedNode.kind} cx={10} cy={10} r={7} />
                </svg>
                <span className="t-label">{KIND_LABEL(selectedNode.kind)}</span>
              </div>
              <h3 className="t-title-md" style={{ wordBreak: "break-word" }}>
                {selectedNode.detail}
              </h3>
              <p className="t-caption" style={{ marginTop: 2 }}>
                {selectedNode.id}
              </p>

              <div className="t-label" style={{ margin: "var(--sp-base) 0 var(--sp-xxs)" }}>
                Connects to
              </div>
              {selectedLinks.length === 0 && (
                <p className="t-body-sm muted">Nothing else links to this yet.</p>
              )}
              <ul style={{ listStyle: "none", padding: 0 }}>
                {selectedLinks.slice(0, 8).map((l, i) => {
                  const otherId = l.source === selected ? l.target : l.source;
                  const other = nodes.find((n) => n.id === otherId);
                  return (
                    <li key={i} style={{ padding: "4px 0" }}>
                      <button
                        type="button"
                        className="btn btn--text"
                        style={{ textAlign: "left", padding: 0, minHeight: 0 }}
                        onClick={() => setSelected(otherId)}
                      >
                        <span className="t-caption">
                          {l.edge.toLowerCase().replace(/_/g, " ")} ›
                        </span>{" "}
                        <span className="t-body-sm ink">{other?.detail ?? otherId}</span>
                      </button>
                    </li>
                  );
                })}
              </ul>

              {onAskAbout && (
                <button
                  type="button"
                  className="btn btn--primary"
                  style={{ marginTop: "var(--sp-base)" }}
                  onClick={() => onAskAbout(selectedNode)}
                >
                  Ask about this
                </button>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}
