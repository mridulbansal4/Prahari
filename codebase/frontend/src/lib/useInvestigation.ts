// One investigation controller, shared by the hero ask box and the Ask section so both drive
// the same run. Streaming contract is unchanged from the original Investigation page.
import { useCallback, useState } from "react";
import { api } from "./api";
import { ensureSession } from "./session";
import { streamInvestigation } from "./stream";
import type { GraphHop, InvestigationResult, StreamEvent } from "./types";

export interface RunState {
  running: boolean;
  stage?: { stage: string; detail?: string };
  answerText: string;
  hops: GraphHop[];
  result?: InvestigationResult;
  error?: string;
  /** CP-9 capability rung reported by the backend's `banner` event. "full" = nothing degraded. */
  rung: string;
}

const EMPTY: RunState = { running: false, answerText: "", hops: [], rung: "full" };

/** Plain-language names for the internal agent stages — no jargon reaches the user. */
const STAGE_COPY: Record<string, string> = {
  planner: "Working out where to look…",
  retriever: "Reading your documents…",
  executor: "Connecting what it found…",
  critic: "Checking the reasoning…",
  verifier: "Verifying every statement has a source…",
};

export function stageLabel(stage?: string): string {
  if (!stage) return "Working…";
  return STAGE_COPY[stage.toLowerCase()] ?? "Working…";
}

function reduce(prev: RunState, ev: StreamEvent): RunState {
  switch (ev.type) {
    case "stage":
      return { ...prev, stage: { stage: String(ev.stage), detail: ev.detail as string } };
    case "graph_hop":
      return { ...prev, hops: [...prev.hops, ev.hop as GraphHop] };
    case "token":
      return { ...prev, answerText: prev.answerText + String(ev.text ?? "") };
    case "banner":
      return { ...prev, rung: String(ev.rung ?? "full") };
    case "abstain":
    case "done":
      return { ...prev, running: false, result: ev.result as InvestigationResult };
    case "error":
      return {
        ...prev,
        running: false,
        error: "Something went wrong while answering. Please try again.",
      };
    default:
      return prev;
  }
}

export function useInvestigation() {
  const [question, setQuestion] = useState("");
  const [run, setRun] = useState<RunState>(EMPTY);

  const ask = useCallback(async (q: string) => {
    const trimmed = q.trim();
    if (!trimmed) return;
    setQuestion(trimmed);
    setRun({ ...EMPTY, running: true });
    try {
      await ensureSession();
      const { investigation_id } = await api.askInvestigation(trimmed);
      streamInvestigation(
        investigation_id,
        (ev: StreamEvent) => setRun((prev) => reduce(prev, ev)),
        () => {
          // Socket closed without a terminal frame — recover the finished result over REST
          // rather than leaving the user on a spinner.
          setRun((prev) => {
            if (!prev.running) return prev;
            api
              .getInvestigation(investigation_id)
              .then((result) => setRun((p) => ({ ...p, running: false, result })))
              .catch(() =>
                setRun((p) => ({
                  ...p,
                  running: false,
                  error: "The connection dropped before the answer finished. Please try again.",
                })),
              );
            return prev;
          });
        },
      );
    } catch {
      setRun({
        ...EMPTY,
        error: "Couldn't reach the service. Check that the backend is running, then try again.",
      });
    }
  }, []);

  const reset = useCallback(() => setRun(EMPTY), []);

  return { question, setQuestion, run, ask, reset };
}
