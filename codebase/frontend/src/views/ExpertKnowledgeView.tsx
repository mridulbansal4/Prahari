// Expert knowledge (M5) — the capture half of the product.
//
// The page's claim is that knowledge walks out of the door when someone retires. That only
// means anything if the knowledge itself is here: not "Anil knows about strainers" but the
// actual rule he'd tell you. So each item shows its text, and the capture form writes new
// text through the real endpoint rather than pretending to.
import { openChat } from "../lib/chat";
import { useCallback, useEffect, useState } from "react";
import { Badge, EmptyState, LoadingBar, Notice, Skeleton, ViewHeader } from "../components/ui";
import { api } from "../lib/api";
import { ensureSession } from "../lib/session";
import type { ExpertiseRecord, KnowledgeItem } from "../lib/types";

const KIND_LABEL: Record<string, string> = {
  rule: "Rule",
  tip: "Tip",
  faq: "FAQ",
  lesson: "Lesson",
  incident: "Incident",
};

const KIND_OPTIONS = [
  { value: "tip", label: "Tip — a practical shortcut" },
  { value: "rule", label: "Rule — something you must always/never do" },
  { value: "faq", label: "FAQ — a question people keep asking" },
  { value: "lesson", label: "Lesson — learned the hard way" },
  { value: "incident", label: "Incident — what happened that time" },
];

/* --------------------------------------------------------------- one item */

function KnowledgeRow({ item }: { item: KnowledgeItem }) {
  const [open, setOpen] = useState(false);
  const hasText = item.text.trim().length > 0;

  return (
    <div
      style={{
        border: "1px solid var(--hairline)",
        borderRadius: "var(--r-md)",
        background: "var(--canvas-soft)",
        overflow: "hidden",
      }}
    >
      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        aria-expanded={open}
        disabled={!hasText}
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          gap: "var(--sp-xs)",
          width: "100%",
          padding: "var(--sp-sm) var(--sp-base)",
          background: "transparent",
          border: "none",
          cursor: hasText ? "pointer" : "default",
          textAlign: "left",
          minHeight: 44,
        }}
      >
        <span className="row" style={{ gap: "var(--sp-xs)", flexWrap: "wrap" }}>
          <span className="t-body-strong">{item.label}</span>
          <Badge>{KIND_LABEL[item.kind] ?? item.kind}</Badge>
          {item.used_in_answers > 0 && (
            <Badge tone="success">
              Used in {item.used_in_answers} {item.used_in_answers === 1 ? "answer" : "answers"}
            </Badge>
          )}
        </span>
        {hasText && (
          <span aria-hidden="true" className="t-caption">
            {open ? "−" : "+"}
          </span>
        )}
      </button>

      {open && hasText && (
        <div
          style={{
            padding: "0 var(--sp-base) var(--sp-base)",
            borderTop: "1px solid var(--hairline)",
            paddingTop: "var(--sp-sm)",
          }}
        >
          <p className="t-body" style={{ color: "var(--ink)" }}>
            {item.text}
          </p>

          {item.tags.length > 0 && (
            <div className="row" style={{ gap: "var(--sp-xxs)", flexWrap: "wrap", marginTop: "var(--sp-sm)" }}>
              {item.tags.map((t) => (
                <span
                  key={t}
                  className="t-caption"
                  style={{
                    padding: "2px 8px",
                    border: "1px solid var(--hairline-strong)",
                    borderRadius: "var(--r-pill)",
                  }}
                >
                  {t}
                </span>
              ))}
            </div>
          )}

          <div
            className="row"
            style={{ justifyContent: "space-between", marginTop: "var(--sp-sm)", gap: "var(--sp-xs)", flexWrap: "wrap" }}
          >
            <span className="t-caption">
              {item.target_ref}
              {item.captured_on ? ` · captured ${item.captured_on}` : ""}
              {item.span_id ? " · citable in answers" : " · not citable (no text stored)"}
            </span>
            <button
              type="button"
              className="btn btn--text"
              onClick={() =>
                openChat({
                  prompt: `What do we know about ${item.label}?`,
                  context: item.label,
                })
              }
            >
              Ask about this →
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

/* ------------------------------------------------------------ capture form */

function CaptureForm({
  people,
  assets,
  onCaptured,
}: {
  people: ExpertiseRecord[];
  assets: { id: string; tag: string }[];
  onCaptured: () => Promise<void>;
}) {
  const [open, setOpen] = useState(false);
  const [personId, setPersonId] = useState(people[0]?.person_id ?? "");
  const [target, setTarget] = useState(assets[0]?.id ?? "");
  const [title, setTitle] = useState("");
  const [text, setText] = useState("");
  const [kind, setKind] = useState("tip");
  const [tags, setTags] = useState("");
  const [state, setState] = useState<"idle" | "saving" | "done" | "error">("idle");
  const [error, setError] = useState<string | null>(null);

  const canSave = personId && target && title.trim() && text.trim() && state !== "saving";

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (!canSave) return;
    setState("saving");
    setError(null);
    try {
      const res = await api.captureKnowledge({
        person_id: personId,
        target_ref: target,
        expertise: title.trim(),
        text: text.trim(),
        kind,
        tags: tags.split(",").map((t) => t.trim()).filter(Boolean),
      });
      // Confirm the backend kept the knowledge rather than trusting a bare ok:true — a
      // capture form that appears to work while dropping the text is the worst outcome.
      if (!res.item?.text?.trim()) {
        setState("error");
        setError("The server accepted the entry but did not store the knowledge text.");
        return;
      }
      await onCaptured();
      setState("done");
      setTitle("");
      setText("");
      setTags("");
    } catch (err: any) {
      setState("error");
      setError(err?.message ? `Couldn't save: ${err.message}` : "Couldn't save this entry.");
    }
  }

  if (!open) {
    return (
      <button type="button" className="btn btn--primary" onClick={() => setOpen(true)}>
        Add knowledge
      </button>
    );
  }

  const field = { display: "block", marginBottom: "var(--sp-xxs)" } as const;

  return (
    <form onSubmit={submit} className="card card--pad-lg" style={{ maxWidth: 760 }}>
      <div className="row" style={{ justifyContent: "space-between", marginBottom: "var(--sp-base)" }}>
        <h3 className="t-title-md">Capture what someone knows</h3>
        <button type="button" className="btn btn--text" onClick={() => setOpen(false)}>
          Cancel
        </button>
      </div>

      <div className="stack" style={{ gap: "var(--sp-base)" }}>
        <div className="doc-grid" style={{ display: "grid", gap: "var(--sp-base)" }}>
          <label>
            <span className="t-label" style={field}>
              Who knows this
            </span>
            <select className="input" value={personId} onChange={(e) => setPersonId(e.target.value)}>
              {people.map((p) => (
                <option key={p.person_id} value={p.person_id}>
                  {p.name} — {p.role}
                </option>
              ))}
            </select>
          </label>

          <label>
            <span className="t-label" style={field}>
              What it's about
            </span>
            <select className="input" value={target} onChange={(e) => setTarget(e.target.value)}>
              {assets.map((a) => (
                <option key={a.id} value={a.id}>
                  {a.tag}
                </option>
              ))}
            </select>
          </label>

          <label>
            <span className="t-label" style={field}>
              Type
            </span>
            <select className="input" value={kind} onChange={(e) => setKind(e.target.value)}>
              {KIND_OPTIONS.map((k) => (
                <option key={k.value} value={k.value}>
                  {k.label}
                </option>
              ))}
            </select>
          </label>
        </div>

        <label>
          <span className="t-label" style={field}>
            Title
          </span>
          <input
            className="input"
            placeholder="e.g. Restart sequence for the parallel BFPs"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />
        </label>

        <label>
          <span className="t-label" style={field}>
            What do you know?
          </span>
          <textarea
            className="input"
            rows={5}
            style={{ minHeight: 130, resize: "vertical", lineHeight: 1.55 }}
            placeholder="Write it the way you'd tell a colleague on shift. The specifics are the point — which valve, which order, what goes wrong if you don't."
            value={text}
            onChange={(e) => setText(e.target.value)}
          />
        </label>

        <label>
          <span className="t-label" style={field}>
            Tags <span className="muted-soft">(comma separated, optional)</span>
          </span>
          <input
            className="input"
            placeholder="restart, cavitation, P-101B"
            value={tags}
            onChange={(e) => setTags(e.target.value)}
          />
        </label>

        {state === "saving" && <LoadingBar stage="Saving and indexing so it can be cited…" />}
        {state === "error" && error && <Notice tone="error">{error}</Notice>}
        {state === "done" && (
          <Notice tone="success">
            Captured. It is now searchable and can be cited in an answer like any document.
          </Notice>
        )}

        <div className="row" style={{ gap: "var(--sp-xs)" }}>
          <button type="submit" className="btn btn--primary" disabled={!canSave}>
            {state === "saving" ? "Saving…" : "Save knowledge"}
          </button>
        </div>
      </div>
    </form>
  );
}

/* ------------------------------------------------------------------- view */

export function ExpertKnowledgeView({
  onOpenAlerts,
}: {
  onOpenAlerts: () => void;
}) {
  const [people, setPeople] = useState<ExpertiseRecord[] | null>(null);
  const [assets, setAssets] = useState<{ id: string; tag: string }[]>([]);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    await ensureSession();
    const [dir, reg] = await Promise.all([
      api.orgMemory(),
      api.assets().catch(() => ({ assets: [] as { id: string; tag: string }[] })),
    ]);
    setPeople(dir.people ?? []);
    setAssets(reg.assets ?? []);
  }, []);

  useEffect(() => {
    load().catch(() => {
      setPeople([]);
      setError("Couldn't load the expert directory. Check that the backend is running.");
    });
  }, [load]);

  const totalCaptured = (people ?? []).reduce((n, p) => n + p.knows.length, 0);
  const atRisk = (people ?? []).filter((p) => p.retirement_risk);

  return (
    <>
      <ViewHeader
        title="Expert knowledge"
        helper="What your most experienced people know that isn't written down anywhere — captured, searchable, and citable in answers."
        action={
          people && people.length > 0 ? (
            <div className="card" style={{ padding: "var(--sp-sm) var(--sp-base)" }}>
              <div className="t-label">Captured</div>
              <div className="t-display-sm">{totalCaptured}</div>
            </div>
          ) : undefined
        }
      />

      {atRisk.length > 0 && (
        <div className="card" style={{ marginBottom: "var(--sp-lg)", maxWidth: 760 }}>
          <div className="row" style={{ gap: "var(--sp-xs)", flexWrap: "wrap" }}>
            <Badge>Retirement risk</Badge>
            <span className="t-body-sm">
              {atRisk.map((p) => p.name).join(", ")}{" "}
              {atRisk.length === 1 ? "is" : "are"} flagged as at risk of leaving. Everything they
              alone know is also raised in Alerts.
            </span>
          </div>
          <button
            type="button"
            className="btn btn--text"
            style={{ marginTop: "var(--sp-xs)" }}
            onClick={onOpenAlerts}
          >
            See the knowledge-at-risk alerts →
          </button>
        </div>
      )}

      <div style={{ marginBottom: "var(--sp-xl)" }}>
        {people && (
          <CaptureForm people={people} assets={assets} onCaptured={load} />
        )}
      </div>

      {people === null && (
        <div className="stack" style={{ gap: "var(--sp-base)" }}>
          <Skeleton height={180} />
          <Skeleton height={180} />
        </div>
      )}

      {error && <Notice tone="error">{error}</Notice>}

      {people?.length === 0 && !error && (
        <EmptyState
          title="No expert knowledge recorded yet"
          body="Nothing has been captured. Add the first entry above — a rule, a hard-won lesson, the thing you'd tell a new engineer on their first shift — and it becomes searchable evidence the moment it's saved."
        />
      )}

      <div className="stack" style={{ gap: "var(--sp-base)" }}>
        {people?.map((p) => (
          <article key={p.person_id} className="card card--hover">
            <div
              className="row"
              style={{ justifyContent: "space-between", gap: "var(--sp-xs)", flexWrap: "wrap" }}
            >
              <div className="row" style={{ gap: "var(--sp-sm)" }}>
                <span
                  aria-hidden="true"
                  className="row"
                  style={{
                    width: 40,
                    height: 40,
                    borderRadius: "var(--r-full)",
                    background: "var(--surface-strong)",
                    justifyContent: "center",
                    font: "var(--t-title-md)",
                    color: "var(--ink)",
                    flexShrink: 0,
                  }}
                >
                  {p.name.charAt(0)}
                </span>
                <span>
                  <span className="t-title-md" style={{ display: "block" }}>
                    {p.name}
                  </span>
                  <span className="t-caption">
                    {p.role} · {p.tenure_years} years here · {p.knows.length}{" "}
                    {p.knows.length === 1 ? "item" : "items"} captured
                  </span>
                </span>
              </div>
              {p.retirement_risk && (
                <button
                  type="button"
                  onClick={onOpenAlerts}
                  title="See the knowledge-at-risk alert for this person"
                  style={{ background: "none", border: "none", padding: 0, cursor: "pointer" }}
                >
                  <Badge>At risk of leaving</Badge>
                </button>
              )}
            </div>

            <div className="t-label" style={{ margin: "var(--sp-base) 0 var(--sp-xs)" }}>
              Knows about
            </div>
            {p.knows.length === 0 ? (
              <p className="t-body-sm muted">
                Nothing captured from {p.name} yet — everything they know is still only in their
                head.
              </p>
            ) : (
              <div className="stack" style={{ gap: "var(--sp-xs)" }}>
                {p.knows.map((k, i) => (
                  <KnowledgeRow key={`${k.target_ref}-${i}`} item={k} />
                ))}
              </div>
            )}
          </article>
        ))}
      </div>

      {people && people.length > 0 && (
        <div
          style={{
            marginTop: "var(--sp-xl)",
            paddingTop: "var(--sp-base)",
            borderTop: "1px solid var(--hairline)",
          }}
        >
          <div className="t-label" style={{ marginBottom: "var(--sp-xxs)" }}>
            About the capture count
          </div>
          <p className="t-body-sm" style={{ maxWidth: 720 }}>
            The number above counts what has actually been captured. There is deliberately no
            &ldquo;% of what they know&rdquo; figure — nobody can measure the denominator, and a
            percentage invented for a dashboard would be exactly the kind of unsupported number
            this system refuses to show elsewhere.
          </p>
        </div>
      )}
    </>
  );
}
