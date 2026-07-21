// Past answers — a new question no longer destroys the previous one. Each entry re-opens
// read-only with its claims, citations and traversal intact.
import { useEffect, useState } from "react";
import { AbstainCard, AnswerCard } from "../components/AnswerCard";
import { NetworkGraph } from "../components/NetworkGraph";
import { Badge, EmptyState, Skeleton, ViewHeader } from "../components/ui";
import { api } from "../lib/api";
import { traversalToNet } from "../lib/graph";
import { ensureSession } from "../lib/session";
import type { InvestigationResult } from "../lib/types";

interface Item {
  investigation_id: string;
  question: string;
  abstained: boolean;
}

export function PastAnswersView({ onAsk }: { onAsk: (q: string) => void }) {
  const [items, setItems] = useState<Item[] | null>(null);
  const [openId, setOpenId] = useState<string | null>(null);
  const [detail, setDetail] = useState<InvestigationResult | null>(null);
  const [loadingDetail, setLoadingDetail] = useState(false);

  useEffect(() => {
    ensureSession()
      .then(() => api.recentInvestigations())
      .then((r) => setItems(r.items))
      .catch(() => setItems([]));
  }, []);

  function open(id: string) {
    if (openId === id) {
      setOpenId(null);
      setDetail(null);
      return;
    }
    setOpenId(id);
    setDetail(null);
    setLoadingDetail(true);
    api
      .getInvestigation(id)
      .then(setDetail)
      .catch(() => setDetail(null))
      .finally(() => setLoadingDetail(false));
  }

  const net = detail ? traversalToNet(detail.graph_path) : null;

  return (
    <>
      <ViewHeader
        title="Past answers"
        helper="Every question asked here, and the answer it produced. Open one to see its sources again."
      />

      {items === null && (
        <div className="stack" style={{ gap: "var(--sp-xs)" }}>
          <Skeleton height={64} />
          <Skeleton height={64} />
          <Skeleton height={64} />
        </div>
      )}

      {items?.length === 0 && (
        <EmptyState
          title="No questions yet"
          body="Once you ask something, it's kept here so you can revisit the answer and its sources."
        >
          <button type="button" className="btn btn--primary" onClick={() => onAsk("")}>
            Ask your first question
          </button>
        </EmptyState>
      )}

      <div className="stack" style={{ gap: "var(--sp-sm)" }}>
        {items?.map((it) => (
          <div key={it.investigation_id} className="card card--hover">
            <div
              className="row"
              style={{ justifyContent: "space-between", gap: "var(--sp-sm)", flexWrap: "wrap" }}
            >
              <span className="t-body-strong" style={{ flex: "1 1 260px" }}>
                {it.question}
              </span>
              <div className="row" style={{ gap: "var(--sp-xs)" }}>
                <Badge tone={it.abstained ? "neutral" : "success"}>
                  {it.abstained ? "No answer given" : "Answered"}
                </Badge>
                <button
                  type="button"
                  className="btn btn--text"
                  onClick={() => open(it.investigation_id)}
                  aria-expanded={openId === it.investigation_id}
                >
                  {openId === it.investigation_id ? "Close" : "Open"}
                </button>
                <button
                  type="button"
                  className="btn btn--text"
                  onClick={() => onAsk(it.question)}
                  title="Run this question again"
                >
                  Ask again
                </button>
              </div>
            </div>

            {openId === it.investigation_id && (
              <div style={{ marginTop: "var(--sp-base)" }}>
                {loadingDetail && <Skeleton height={180} />}
                {!loadingDetail && !detail && (
                  <p className="t-body-sm muted">Couldn&rsquo;t load this answer.</p>
                )}
                {detail && (
                  <div className="stack" style={{ gap: "var(--sp-base)" }}>
                    {detail.abstained ? (
                      <AbstainCard result={detail} />
                    ) : (
                      <AnswerCard result={detail} />
                    )}
                    {net && net.nodes.length > 0 && (
                      <div>
                        <div className="t-label" style={{ marginBottom: "var(--sp-xs)" }}>
                          The path it took
                        </div>
                        <NetworkGraph
                          nodes={net.nodes}
                          links={net.links}
                          height={300}
                          layout="stacked"
                        />
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}
          </div>
        ))}
      </div>
    </>
  );
}
