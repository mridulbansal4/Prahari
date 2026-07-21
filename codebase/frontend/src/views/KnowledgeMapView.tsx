// Knowledge map — two modes: the current answer's trace, and a plant-wide browse assembled
// from every traversal walked so far (see lib/graph.ts for why that assembly is necessary).
import { useEffect, useState } from "react";
import { GraphLegend, TraversalTrace } from "../components/GraphCanvas";
import { NetworkGraph, type NetNode } from "../components/NetworkGraph";
import { EmptyState, Skeleton, ViewHeader } from "../components/ui";
import { loadPlantGraph, traversalToNet, type PlantGraph } from "../lib/graph";
import type { RunState } from "../lib/useInvestigation";

type Mode = "trace" | "plant";

export function KnowledgeMapView({
  run,
  onAskAbout,
}: {
  run: RunState;
  onAskAbout: (q: string) => void;
}) {
  const hasTrace = run.hops.length > 0;
  const [mode, setMode] = useState<Mode>(hasTrace ? "trace" : "plant");
  const [plant, setPlant] = useState<PlantGraph | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (mode !== "plant" || plant) return;
    setLoading(true);
    loadPlantGraph()
      .then(setPlant)
      .catch(() => setPlant({ nodes: [], links: [], sourceCount: 0, partial: true }))
      .finally(() => setLoading(false));
  }, [mode, plant]);

  const trace = traversalToNet(run.hops);
  const active = mode === "trace" ? trace : (plant ?? { nodes: [], links: [] });

  return (
    <>
      <ViewHeader
        title="How everything connects"
        helper="Your equipment, drawings, procedures and records as a network — drag to explore, click any node for detail."
      />

      {/* Mode switch */}
      <div className="row" style={{ gap: "var(--sp-xxs)", marginBottom: "var(--sp-base)" }}>
        {(
          [
            { id: "trace" as Mode, label: "This answer's path", disabled: !hasTrace },
            { id: "plant" as Mode, label: "Everything mapped so far", disabled: false },
          ]
        ).map((t) => (
          <button
            key={t.id}
            type="button"
            disabled={t.disabled}
            onClick={() => setMode(t.id)}
            aria-pressed={mode === t.id}
            className={mode === t.id ? "btn btn--primary" : "btn btn--outline"}
            style={{ minHeight: 36, padding: "0 18px" }}
          >
            {t.label}
          </button>
        ))}
      </div>

      <div className="card" style={{ marginBottom: "var(--sp-base)", padding: "var(--sp-base) var(--sp-lg)" }}>
        <div className="t-label" style={{ marginBottom: "var(--sp-xs)" }}>
          Legend — shape shows what kind of record it is
        </div>
        <GraphLegend />
      </div>

      {loading && <Skeleton height={420} />}

      {!loading && mode === "trace" && !hasTrace && (
        <EmptyState
          title="Ask a question to see its path"
          body="The map draws itself as the system moves from one record to the next, so you can see exactly which documents an answer travelled through."
        />
      )}

      {!loading && active.nodes.length > 0 && (
        <>
          <NetworkGraph
            nodes={active.nodes}
            links={active.links}
            height={560}
            onAskAbout={(n: NetNode) => onAskAbout(`Tell me about ${n.detail}`)}
          />

          {mode === "plant" && plant && (
            <p className="t-caption" style={{ marginTop: "var(--sp-sm)" }}>
              Assembled from {plant.sourceCount} past{" "}
              {plant.sourceCount === 1 ? "question" : "questions"} plus the asset register. This
              shows everything the system has walked so far — not necessarily every record it
              holds.
            </p>
          )}

          {mode === "trace" && (
            <div className="card" style={{ marginTop: "var(--sp-base)" }}>
              <div className="t-label" style={{ marginBottom: "var(--sp-sm)" }}>
                The same path, in words
              </div>
              <TraversalTrace hops={run.hops} />
            </div>
          )}
        </>
      )}

      {!loading && mode === "plant" && active.nodes.length === 0 && (
        <EmptyState
          title="Nothing mapped yet"
          body="Ask a question or add documents, and the connections between your records will start appearing here."
        />
      )}
    </>
  );
}
