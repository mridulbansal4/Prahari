// Decision memory & replay.
//
// The replay half is the page's whole promise: not "what was decided" but "what else was on
// the table, and why it wasn't chosen". Everything rendered here comes from the replay
// endpoint; where the design asked for a field the backend does not return, this shows an
// honest note instead of a plausible-looking placeholder.
import { useCallback, useEffect, useState } from "react";
import { CitationChips } from "../components/AnswerCard";
import { DECISION_LEGEND, LegendRow } from "../components/GraphCanvas";
import { NetworkGraph, type NetLink, type NetNode } from "../components/NetworkGraph";
import { Badge, EmptyState, Notice, Skeleton, ViewHeader } from "../components/ui";
import {
  loadDecisions,
  loadReplay,
  shapeReplay,
  toCitations,
  type DecisionSummary,
  type Replay,
  type ReplayShape,
  type ReplayStep,
} from "../lib/decisions";

/** Deep-link support without introducing routing: `#decisions/<id>`. */
const HASH_PREFIX = "#decisions/";

function readHash(): string | null {
  const h = window.location.hash;
  return h.startsWith(HASH_PREFIX) ? decodeURIComponent(h.slice(HASH_PREFIX.length)) : null;
}

/* ------------------------------------------------------------------ list */

function DecisionCard({
  decision,
  onOpen,
}: {
  decision: DecisionSummary;
  onOpen: () => void;
}) {
  return (
    <article className="card card--hover">
      <div
        className="row"
        style={{ justifyContent: "space-between", gap: "var(--sp-sm)", flexWrap: "wrap" }}
      >
        <h3 className="t-title-md" style={{ flex: "1 1 260px" }}>
          {decision.title}
        </h3>
        <Badge>Decision recorded</Badge>
      </div>

      <p className="t-caption" style={{ marginTop: "var(--sp-xxs)" }}>
        {decision.date}
        {decision.asset_tag ? ` · ${decision.asset_tag}` : ` · ${decision.asset_id}`}
      </p>

      <div className="row" style={{ gap: "var(--sp-xs)", marginTop: "var(--sp-base)" }}>
        <button type="button" className="btn btn--primary" onClick={onOpen}>
          Replay the reasoning
        </button>
      </div>
    </article>
  );
}

/* ---------------------------------------------------------------- replay */

function StepBlock({ step, muted }: { step: ReplayStep; muted?: boolean }) {
  const citations = toCitations(step);
  return (
    <div
      style={{
        padding: "var(--sp-sm) var(--sp-base)",
        border: "1px solid var(--hairline)",
        borderLeft: `3px solid ${muted ? "var(--hairline-strong)" : "var(--ink)"}`,
        borderRadius: "var(--r-md)",
        background: "var(--canvas-soft)",
        opacity: muted ? 0.85 : 1,
      }}
    >
      <div className="t-body-strong">
        {step.title} <CitationChips citations={citations} />
      </div>
      {step.detail && (
        <p className="t-body-sm" style={{ marginTop: "var(--sp-xxs)" }}>
          {step.detail}
        </p>
      )}
    </div>
  );
}

function chainToNet(shape: ReplayShape): { nodes: NetNode[]; links: NetLink[] } {
  const nodes: NetNode[] = shape.ordered.map((s) => ({
    id: s.id,
    kind: s.kind,
    detail: s.title.length > 40 ? `${s.title.slice(0, 39)}…` : s.title,
  }));
  const links: NetLink[] = [];
  for (let i = 1; i < shape.ordered.length; i++) {
    links.push({
      source: shape.ordered[i - 1].id,
      target: shape.ordered[i].id,
      edge: "led to",
    });
  }
  return { nodes, links };
}

function ReplayDetail({
  decision,
  replay,
  onBack,
}: {
  decision: DecisionSummary | null;
  replay: Replay;
  onBack: () => void;
}) {
  const shape = shapeReplay(replay);
  const net = chainToNet(shape);

  return (
    <>
      <button
        type="button"
        className="btn btn--text"
        onClick={onBack}
        style={{ marginBottom: "var(--sp-sm)" }}
      >
        ← All decisions
      </button>

      <ViewHeader
        title={replay.title}
        helper={
          decision
            ? `Decided ${decision.date}${
                decision.asset_tag ? ` · ${decision.asset_tag}` : ""
              } — the reasoning as it was recorded at the time.`
            : "The reasoning as it was recorded at the time."
        }
      />

      <div className="stack" style={{ gap: "var(--sp-xl)" }}>
        {/* --- Options considered: the reason this page exists --- */}
        <section>
          <div className="t-label" style={{ marginBottom: "var(--sp-sm)" }}>
            Options considered
          </div>
          <div className="stack" style={{ gap: "var(--sp-sm)" }}>
            {shape.decision && (
              <div>
                <div className="row" style={{ gap: "var(--sp-xs)", marginBottom: "var(--sp-xxs)" }}>
                  <Badge tone="success">Chosen</Badge>
                </div>
                <StepBlock step={shape.decision} />
              </div>
            )}
            {shape.alternatives.map((alt) => (
              <div key={alt.id}>
                <div className="row" style={{ gap: "var(--sp-xs)", marginBottom: "var(--sp-xxs)" }}>
                  <Badge>Rejected</Badge>
                </div>
                <StepBlock step={alt} muted />
              </div>
            ))}
            {!shape.alternatives.length && (
              <p className="t-body-sm muted">
                No rejected options were recorded for this decision.
              </p>
            )}
          </div>
          {shape.riskAccepted && (
            <div style={{ marginTop: "var(--sp-base)" }}>
              <div className="t-label" style={{ marginBottom: "var(--sp-xxs)" }}>
                Risk accepted
              </div>
              <StepBlock step={shape.riskAccepted} muted />
            </div>
          )}
        </section>

        {/* --- Evidence trail --- */}
        <section>
          <div className="t-label" style={{ marginBottom: "var(--sp-sm)" }}>
            What it was based on
          </div>
          {shape.evidence.length === 0 && (
            <p className="t-body-sm muted">No sources were recorded against this decision.</p>
          )}
          <div className="stack" style={{ gap: "var(--sp-sm)" }}>
            {shape.evidence.map((s) => (
              <StepBlock key={s.id} step={s} />
            ))}
          </div>
        </section>

        {/* --- How it got there --- */}
        <section>
          <div className="t-label" style={{ marginBottom: "var(--sp-sm)" }}>
            How it got there
          </div>
          <div className="card" style={{ marginBottom: "var(--sp-base)", padding: "var(--sp-base) var(--sp-lg)" }}>
            <LegendRow items={DECISION_LEGEND} />
          </div>
          {net.nodes.length > 0 ? (
            <NetworkGraph nodes={net.nodes} links={net.links} height={420} layout="stacked" />
          ) : (
            <p className="t-body-sm muted">No reasoning chain was recorded.</p>
          )}
        </section>

        {/* --- Outcome --- */}
        {(shape.outcome || shape.lesson) && (
          <section>
            <div className="t-label" style={{ marginBottom: "var(--sp-sm)" }}>
              What actually happened
            </div>
            <div className="stack" style={{ gap: "var(--sp-sm)" }}>
              {shape.outcome && <StepBlock step={shape.outcome} />}
              {shape.lesson && <StepBlock step={shape.lesson} muted />}
            </div>
          </section>
        )}

      </div>
    </>
  );
}

/* ------------------------------------------------------------------ view */

export function DecisionsView({ onAsk }: { onAsk: (q: string) => void }) {
  const [decisions, setDecisions] = useState<DecisionSummary[] | null>(null);
  const [listError, setListError] = useState<string | null>(null);
  const [openId, setOpenId] = useState<string | null>(() => readHash());
  const [replay, setReplay] = useState<Replay | null>(null);
  const [replayError, setReplayError] = useState<string | null>(null);
  const [loadingReplay, setLoadingReplay] = useState(false);
  const [assetFilter, setAssetFilter] = useState("all");

  useEffect(() => {
    loadDecisions()
      .then(setDecisions)
      .catch(() => {
        setDecisions([]);
        setListError("Couldn't load decisions. Check that the backend is running.");
      });
  }, []);

  // Deep links and the browser back button both drive the same state.
  useEffect(() => {
    const onHash = () => setOpenId(readHash());
    window.addEventListener("hashchange", onHash);
    return () => window.removeEventListener("hashchange", onHash);
  }, []);

  useEffect(() => {
    if (!openId) {
      setReplay(null);
      setReplayError(null);
      return;
    }
    setLoadingReplay(true);
    setReplayError(null);
    loadReplay(openId)
      .then(setReplay)
      .catch(() => setReplayError("Couldn't load this decision's reasoning."))
      .finally(() => setLoadingReplay(false));
  }, [openId]);

  const open = useCallback((id: string) => {
    window.location.hash = `${HASH_PREFIX}${encodeURIComponent(id)}`;
    setOpenId(id);
  }, []);

  const back = useCallback(() => {
    if (window.location.hash.startsWith(HASH_PREFIX)) {
      window.history.replaceState(null, "", window.location.pathname + window.location.search);
    }
    setOpenId(null);
  }, []);

  // Clear a stale deep link when this view unmounts, so switching pages doesn't leave the
  // hash pointing at a decision that is no longer on screen.
  useEffect(() => {
    return () => {
      if (window.location.hash.startsWith(HASH_PREFIX)) {
        window.history.replaceState(null, "", window.location.pathname + window.location.search);
      }
    };
  }, []);

  /* ---- replay detail ---- */
  if (openId) {
    const summary = decisions?.find((d) => d.decision_id === openId) ?? null;
    if (loadingReplay) {
      return (
        <>
          <button type="button" className="btn btn--text" onClick={back}>
            ← All decisions
          </button>
          <div className="stack" style={{ gap: "var(--sp-base)", marginTop: "var(--sp-base)" }}>
            <Skeleton height={80} />
            <Skeleton height={200} />
            <Skeleton height={320} />
          </div>
        </>
      );
    }
    if (replayError || !replay) {
      return (
        <>
          <button type="button" className="btn btn--text" onClick={back}>
            ← All decisions
          </button>
          <div style={{ marginTop: "var(--sp-base)" }}>
            <Notice tone="error">{replayError ?? "This decision has no recorded reasoning."}</Notice>
          </div>
        </>
      );
    }
    return <ReplayDetail decision={summary} replay={replay} onBack={back} />;
  }

  /* ---- list ---- */
  const assets = [...new Set((decisions ?? []).map((d) => d.asset_tag ?? d.asset_id))];
  const shown = (decisions ?? []).filter(
    (d) => assetFilter === "all" || (d.asset_tag ?? d.asset_id) === assetFilter,
  );
  const showFilter = (decisions?.length ?? 0) > 4 && assets.length > 1;

  return (
    <>
      <ViewHeader
        title="Decisions & replay"
        helper="Decisions made in the past, and the reasoning behind them — including the options that were considered and rejected."
        action={
          showFilter ? (
            <label className="stack" style={{ gap: "var(--sp-xxs)" }}>
              <span className="t-label">Equipment</span>
              <select
                className="input"
                style={{ minWidth: 180 }}
                value={assetFilter}
                onChange={(e) => setAssetFilter(e.target.value)}
              >
                <option value="all">All equipment</option>
                {assets.map((a) => (
                  <option key={a} value={a}>
                    {a}
                  </option>
                ))}
              </select>
            </label>
          ) : undefined
        }
      />

      {decisions === null && (
        <div className="stack" style={{ gap: "var(--sp-sm)" }}>
          <Skeleton height={130} />
          <Skeleton height={130} />
        </div>
      )}

      {listError && (
        <div style={{ marginBottom: "var(--sp-base)" }}>
          <Notice tone="error">{listError}</Notice>
        </div>
      )}

      {decisions !== null && decisions.length === 0 && !listError && (
        <EmptyState
          title="No decisions recorded yet"
          body="When someone records why a call was made — what was chosen, what was rejected and why — it is kept here so the reasoning can be replayed later instead of being lost."
        >
          <button
            type="button"
            className="btn btn--primary"
            onClick={() => onAsk("why is P-101B running hot?")}
          >
            Ask a question
          </button>
        </EmptyState>
      )}

      {shown.length > 0 && (
        <div className="stack" style={{ gap: "var(--sp-sm)" }}>
          {shown.map((d) => (
            <DecisionCard
              key={d.decision_id}
              decision={d}
              onOpen={() => open(d.decision_id)}
            />
          ))}
        </div>
      )}

      {decisions !== null && decisions.length > 0 && (
        <p className="t-caption" style={{ marginTop: "var(--sp-lg)", maxWidth: 640 }}>
          Open a decision to replay the full reasoning — the options considered, the ones
          rejected and why, the evidence, and what happened.
        </p>
      )}
    </>
  );
}
