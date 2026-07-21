// Graph assembly for the knowledge map.
//
// LIMITATION (flagged, not faked): the backend exposes no plant-wide graph endpoint — there is
// no `GET /v1/graph`. The only graph data any endpoint returns is `graph_path`, the traversal
// attached to a single investigation. So "plant-wide browse" is assembled by unioning the
// traversals of every past investigation plus the asset register. It is therefore a map of
// everything the system has *walked so far*, not the complete graph. Adding a real
// `GET /v1/graph` returning nodes+edges would make this exact and is a one-endpoint change.
import { api } from "./api";
import { ensureSession } from "./session";
import type { NetLink, NetNode } from "../components/NetworkGraph";
import type { GraphHop } from "./types";

export interface Net {
  nodes: NetNode[];
  links: NetLink[];
}

/** Fold a single traversal into nodes + links. Consecutive hops are what form an edge. */
export function traversalToNet(hops: GraphHop[]): Net {
  const nodes = new Map<string, NetNode>();
  const links = new Map<string, NetLink>();
  let prev: string | null = null;

  for (const h of hops) {
    if (!h.node) continue;
    const id = h.node;
    if (!nodes.has(id)) {
      nodes.set(id, { id, kind: h.node_label ?? "", detail: h.detail ?? id });
    }
    // Self-edges carry no information on a network layout — the spine rendered them only
    // because it was a list.
    if (prev && prev !== id && h.edge) {
      const key = `${prev}->${id}:${h.edge}`;
      if (!links.has(key)) links.set(key, { source: prev, target: id, edge: h.edge });
    }
    prev = id;
  }
  return { nodes: [...nodes.values()], links: [...links.values()] };
}

function merge(into: Net, add: Net): void {
  const seen = new Set(into.nodes.map((n) => n.id));
  for (const n of add.nodes) {
    if (!seen.has(n.id)) {
      into.nodes.push(n);
      seen.add(n.id);
    }
  }
  const seenL = new Set(into.links.map((l) => `${l.source}->${l.target}:${l.edge}`));
  for (const l of add.links) {
    const key = `${l.source}->${l.target}:${l.edge}`;
    if (!seenL.has(key)) {
      into.links.push(l);
      seenL.add(key);
    }
  }
}

export interface PlantGraph extends Net {
  /** How many past investigations contributed, for the honesty note in the UI. */
  sourceCount: number;
  partial: true;
}

/** Union of every traversal the system has walked, plus the asset register. */
export async function loadPlantGraph(): Promise<PlantGraph> {
  await ensureSession();
  const net: Net = { nodes: [], links: [] };

  const [assetsRes, recent] = await Promise.all([
    api.assets().catch(() => ({ assets: [] })),
    api.recentInvestigations().catch(() => ({ items: [] })),
  ]);

  // Seed with the asset register so equipment appears even before anything is asked.
  merge(net, {
    nodes: assetsRes.assets.map((a) => ({ id: a.id, kind: "Asset", detail: a.tag })),
    links: [],
  });

  // Cap the fan-out: this is one request per investigation and the list grows unbounded.
  const ids = recent.items.slice(0, 25).map((i) => i.investigation_id);
  const results = await Promise.all(
    ids.map((id) => api.getInvestigation(id).catch(() => null)),
  );

  let contributed = 0;
  for (const r of results) {
    if (!r?.graph_path?.length) continue;
    contributed++;
    merge(net, traversalToNet(r.graph_path));
  }

  return { ...net, sourceCount: contributed, partial: true };
}
