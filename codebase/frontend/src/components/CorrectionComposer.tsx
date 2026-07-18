// The cross-cutting CorrectionAffordance + composer (M8, CP-10). Appears on every claim/edge.
// Framed as "teaching the system something it will remember forever", not "reporting a bug".
import { useState } from "react";
import { api } from "../lib/api";
import { useAuth } from "../lib/auth";

export function CorrectionAffordance({
  targetKind,
  targetRef,
  priorValue,
}: {
  targetKind: string;
  targetRef: string;
  priorValue?: string;
}) {
  const { me } = useAuth();
  const [open, setOpen] = useState(false);
  const [value, setValue] = useState("");
  const [rationale, setRationale] = useState("");
  const [state, setState] = useState<"idle" | "saving" | "done" | "error">("idle");

  if (!open)
    return (
      <button
        className="btn btn-tertiary"
        style={{ fontSize: 11, padding: "2px 6px" }}
        onClick={() => setOpen(true)}
      >
        This is wrong
      </button>
    );

  async function submit() {
    if (!me) return;
    setState("saving");
    try {
      await api.submitCorrection({
        target_kind: targetKind,
        target_ref: targetRef,
        new_value: value,
        rationale,
        author: me.subject,
        prior_value: priorValue,
      });
      setState("done");
    } catch {
      setState("error");
    }
  }

  if (state === "done")
    return (
      <div className="card-dense card" style={{ borderLeft: "3px solid var(--knowledge)" }}>
        <span className="t-body-sm">
          Thank you — this is now part of the organization's memory. It will improve future
          answers, attributed to you.
        </span>
      </div>
    );

  return (
    <div className="card card-dense" style={{ marginTop: "var(--sp-sm)" }}>
      <div className="t-label" style={{ marginBottom: "var(--sp-sm)" }}>
        Teach Prahari
      </div>
      <textarea
        className="textarea"
        placeholder="What is the correct value?"
        value={value}
        onChange={(e) => setValue(e.target.value)}
      />
      <input
        className="input"
        style={{ marginTop: "var(--sp-sm)" }}
        placeholder="Why? (rationale — recorded, attributed, permanent)"
        value={rationale}
        onChange={(e) => setRationale(e.target.value)}
      />
      <div className="row" style={{ marginTop: "var(--sp-sm)" }}>
        <button
          className="btn btn-primary"
          disabled={!value || !rationale || state === "saving"}
          onClick={submit}
        >
          {state === "saving" ? "Recording correction…" : "Submit correction"}
        </button>
        <button className="btn btn-tertiary" onClick={() => setOpen(false)}>
          Cancel
        </button>
      </div>
      {state === "error" && (
        <div className="t-caption" style={{ color: "var(--critical)", marginTop: "var(--sp-sm)" }}>
          Couldn't save right now — your text is kept; try again shortly.
        </div>
      )}
      <div className="t-metadata" style={{ marginTop: "var(--sp-sm)" }}>
        This will be recorded as a correction attributed to {me?.name}.
      </div>
    </div>
  );
}
