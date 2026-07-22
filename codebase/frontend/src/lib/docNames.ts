// Resolves a citation's doc_id to the document's real filename as shown in the Documents area.
//
// This is not decorative: it shows the actual source file behind a claim, so "Backed by your
// documents" names WHICH document. The map is the ingested library (GET /v1/ingestion), loaded
// once and cached. A doc_id with no matching library entry (e.g. a seeded reference) falls back
// to the id itself — never a substituted or invented filename, which would be a false citation.
import { useEffect, useState } from "react";
import { api } from "./api";
import { ensureSession } from "./session";

let cache: Map<string, string> | null = null;
let inflight: Promise<Map<string, string>> | null = null;

async function load(): Promise<Map<string, string>> {
  if (cache) return cache;
  if (!inflight) {
    inflight = (async () => {
      await ensureSession();
      const r = await api.ingestionJobs().catch(() => ({ jobs: [] as { doc_id: string; filename: string }[] }));
      const m = new Map<string, string>();
      for (const j of r.jobs ?? []) {
        if (j.doc_id && j.filename) m.set(j.doc_id, j.filename);
      }
      cache = m;
      return m;
    })();
  }
  return inflight;
}

export function useDocNames(): Map<string, string> | null {
  const [map, setMap] = useState<Map<string, string> | null>(cache);
  useEffect(() => {
    let alive = true;
    load().then((m) => alive && setMap(m));
    return () => {
      alive = false;
    };
  }, []);
  return map;
}

export function docLabel(map: Map<string, string> | null, docId: string): string {
  if (!docId) return "";
  return map?.get(docId) ?? docId;
}
