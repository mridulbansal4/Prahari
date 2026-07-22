// Asset map — the moat, surfaced. One physical thing goes by many names across drawings,
// sensors, work orders and conversation; this shows them resolved into one asset.
import { openChat } from "../lib/chat";
import { useEffect, useState } from "react";
import { Badge, EmptyState, Skeleton, ViewHeader } from "../components/ui";
import { api } from "../lib/api";
import type { Alert } from "../lib/alerts";
import { ensureSession } from "../lib/session";

interface Asset {
  id: string;
  tag: string;
  name: string;
  iso_class: string;
}

interface Merge {
  merge_id: string;
  identifier_ids: string[];
  approver: string;
  created_at: string;
  auto: boolean;
  reversed: boolean;
}

/** Identifier records come back as refs like "ident-bfpb"; show the meaningful part. */
function identifierName(ref: string): string {
  return ref.replace(/^ident-/, "").replace(/[-_]/g, " ");
}

export function AssetMapView({
  alerts,
}: {
  alerts: Alert[];
}) {
  const [assets, setAssets] = useState<Asset[] | null>(null);
  const [selected, setSelected] = useState<string | null>(null);
  const [merges, setMerges] = useState<Merge[] | null>(null);
  const [corpusSize, setCorpusSize] = useState<number | null>(null);

  useEffect(() => {
    ensureSession()
      .then(() => Promise.all([api.assets(), api.resolutionQueue().catch(() => null)]))
      .then(([a, q]) => {
        setAssets(a.assets);
        setSelected((prev) => prev ?? a.assets[0]?.id ?? null);
        if (q) setCorpusSize(q.corpus_size);
      })
      .catch(() => setAssets([]));
  }, []);

  useEffect(() => {
    if (!selected) return;
    setMerges(null);
    api
      .resolutionHistory(selected)
      .then((r) => setMerges(((r.history ?? []) as Merge[]).filter((m) => !m.reversed)))
      .catch(() => setMerges([]));
  }, [selected]);

  const asset = assets?.find((a) => a.id === selected) ?? null;
  const assetAlerts = asset ? alerts.filter((a) => a.assetTag === asset.tag) : [];
  const resolvedNames = [...new Set((merges ?? []).flatMap((m) => m.identifier_ids))];

  return (
    <>
      <ViewHeader
        title="One piece of equipment, many names"
        helper="The same pump appears as a tag on a drawing, a sensor name, a work-order reference and a nickname. This is how they resolve into one thing."
        action={
          corpusSize !== null ? (
            <div className="card" style={{ padding: "var(--sp-sm) var(--sp-base)" }}>
              <div className="t-label">Resolved identities</div>
              <div className="t-display-sm">{corpusSize}</div>
            </div>
          ) : undefined
        }
      />

      {assets === null && <Skeleton height={200} />}

      {assets?.length === 0 && (
        <EmptyState
          title="No equipment registered yet"
          body="Add documents that mention equipment and it will start appearing here."
        />
      )}

      {assets && assets.length > 0 && (
        <>
          <div className="row" style={{ gap: "var(--sp-xs)", flexWrap: "wrap", marginBottom: "var(--sp-lg)" }}>
            {assets.map((a) => (
              <button
                key={a.id}
                type="button"
                onClick={() => setSelected(a.id)}
                aria-pressed={selected === a.id}
                className={selected === a.id ? "btn btn--primary" : "btn btn--outline"}
                style={{ minHeight: 38 }}
              >
                {a.tag}
              </button>
            ))}
          </div>

          {asset && (
            <div className="ask-grid" style={{ display: "grid", gap: "var(--sp-base)" }}>
              <div className="stack" style={{ gap: "var(--sp-base)" }}>
                <div className="card card--pad-lg">
                  <div className="t-label">Canonical equipment</div>
                  <h2 className="t-display-md" style={{ marginTop: "var(--sp-xxs)" }}>
                    {asset.tag}
                  </h2>
                  <p className="t-body">{asset.name}</p>
                  <p className="t-caption" style={{ marginTop: "var(--sp-xxs)" }}>
                    {asset.id} · class {asset.iso_class}
                  </p>

                  <div className="t-label" style={{ margin: "var(--sp-lg) 0 var(--sp-xs)" }}>
                    Known by these names
                  </div>
                  {merges === null && <Skeleton height={60} />}
                  {merges?.length === 0 && (
                    <p className="t-body-sm muted">
                      No alternative names have been resolved for this equipment yet. As
                      documents that call it something else are read, they&rsquo;ll be linked
                      here.
                    </p>
                  )}

                  {/* The identifier set is shown once, as the union across every active merge —
                      the same asset can be confirmed more than once, and repeating the whole
                      list per event reads as a duplication bug. */}
                  {merges && merges.length > 0 && (
                    <>
                      <p className="t-body" style={{ marginBottom: "var(--sp-sm)" }}>
                        <strong>{resolvedNames.length} different names</strong> in your documents
                        were confirmed to mean this one piece of equipment.
                      </p>
                      <div className="row" style={{ gap: "var(--sp-xs)", flexWrap: "wrap" }}>
                        {resolvedNames.map((ref) => (
                          <span
                            key={ref}
                            style={{
                              padding: "var(--sp-xs) var(--sp-sm)",
                              border: "1px solid var(--hairline-strong)",
                              borderRadius: "var(--r-md)",
                              background: "var(--canvas-soft)",
                            }}
                          >
                            <span className="t-body-sm ink" style={{ display: "block" }}>
                              {identifierName(ref)}
                            </span>
                            <span className="t-caption">{ref}</span>
                          </span>
                        ))}
                      </div>

                      <div className="t-label" style={{ margin: "var(--sp-base) 0 var(--sp-xxs)" }}>
                        Confirmed by a person
                      </div>
                      <ul style={{ listStyle: "none", padding: 0 }}>
                        {merges.map((m) => (
                          <li key={m.merge_id} className="t-caption" style={{ padding: "2px 0" }}>
                            {m.auto ? "Resolved automatically" : `Confirmed by ${m.approver}`} on{" "}
                            {m.created_at.slice(0, 10)} · reversible, and in the audit trail.
                          </li>
                        ))}
                      </ul>
                    </>
                  )}

                  <button
                    type="button"
                    className="btn btn--primary"
                    style={{ marginTop: "var(--sp-lg)" }}
                    onClick={() =>
                      openChat({
                        prompt: `What should I know about ${asset.tag}?`,
                        context: `${asset.tag} — ${asset.name}`,
                      })
                    }
                  >
                    Ask about {asset.tag}
                  </button>
                </div>
              </div>

              <div className="card">
                <div className="t-label" style={{ marginBottom: "var(--sp-xs)" }}>
                  Open alerts on this equipment
                </div>
                {assetAlerts.length === 0 && (
                  <p className="t-body-sm muted">Nothing flagged on {asset.tag} right now.</p>
                )}
                <div className="stack" style={{ gap: "var(--sp-sm)" }}>
                  {assetAlerts.map((a) => (
                    <div key={a.id}>
                      <div className="row" style={{ gap: "var(--sp-xs)", marginBottom: 2 }}>
                        <Badge tone={a.kind === "overdue" ? "error" : "neutral"}>
                          {a.kind === "overdue" ? "Overdue" : "Note"}
                        </Badge>
                      </div>
                      <div className="t-body-sm ink">{a.title}</div>
                      <div className="t-caption">{a.detail}</div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </>
      )}
    </>
  );
}
