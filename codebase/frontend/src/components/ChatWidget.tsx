// Floating "ask anywhere" widget — a small launcher bottom-right that opens a chat-style panel.
//
// It reuses the real investigation flow and the same AnswerCard / citation components as the
// main Ask surface, so an answer here is grounded and cited exactly like one on the Ask page —
// it just lives in a corner and can be summoned with context by any "Ask about this" affordance.
import { useEffect, useRef, useState } from "react";
import { onOpenChat } from "../lib/chat";
import { stageLabel, useInvestigation } from "../lib/useInvestigation";
import { AbstainCard, AnswerCard } from "./AnswerCard";
import { LogoMark } from "./LogoMark";
import { LoadingBar, Notice } from "./ui";

export function ChatWidget({ onOpenFull }: { onOpenFull: (question: string) => void }) {
  const [open, setOpen] = useState(false);
  const [context, setContext] = useState<string | null>(null);
  const [value, setValue] = useState("");
  const [asked, setAsked] = useState("");
  const { run, ask } = useInvestigation();
  const bodyRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Any "Ask about this" affordance opens the panel here. The question lands in the ask box
  // (visible and editable) and runs; the context is shown above it.
  useEffect(
    () =>
      onOpenChat(({ prompt, context: ctx }) => {
        setContext(ctx ?? null);
        setOpen(true);
        if (prompt.trim()) {
          // The question is run and shown via the "Ask about" label — it is deliberately NOT
          // dropped into the input box, which stays empty and ready for the next question.
          setValue("");
          setAsked(prompt);
          ask(prompt);
        }
        setTimeout(() => inputRef.current?.focus(), 50);
      }),
    [ask],
  );

  // Keep the newest content in view as the answer streams in.
  useEffect(() => {
    const el = bodyRef.current;
    if (el) el.scrollTop = el.scrollHeight;
  }, [run.answerText, run.result, run.running]);

  function submit(e: React.FormEvent) {
    e.preventDefault();
    if (!value.trim() || run.running) return;
    setAsked(value);
    setContext(null); // a freshly typed question isn't "about" the previous context
    ask(value);
  }

  const idle = !run.running && !run.result && !run.error;
  const fullQuestion = run.result?.question || asked || value;

  if (!open) {
    return (
      <button
        type="button"
        className="chat-fab"
        onClick={() => {
          setOpen(true);
          setTimeout(() => inputRef.current?.focus(), 50);
        }}
        aria-label="Ask a question"
        title="Ask a question"
      >
        <LogoMark width={34} />
      </button>
    );
  }

  return (
    <section className="chat-panel" role="dialog" aria-label="Ask Prahari">
      <header className="chat-head">
        <span className="row" style={{ gap: "var(--sp-xs)" }}>
          <LogoMark width={24} />
          <span className="t-body-strong">Ask Prahari</span>
        </span>
        <button
          type="button"
          className="chat-icon-btn"
          onClick={() => setOpen(false)}
          aria-label="Close"
        >
          ✕
        </button>
      </header>

      {context && (
        <div className="chat-context">
          <span className="t-label">Ask about</span>
          <span className="t-body-sm ink" style={{ display: "block", marginTop: 2 }}>
            {context}
          </span>
        </div>
      )}

      <div className="chat-body" ref={bodyRef}>
        {idle && (
          <p className="t-body-sm muted">
            Ask anything about your documents. Every answer names the document behind each
            statement.
          </p>
        )}

        {run.running && (
          <div>
            <LoadingBar stage={stageLabel(run.stage?.stage)} />
            {run.answerText && (
              <p className="t-body-sm" style={{ marginTop: "var(--sp-sm)", color: "var(--ink)" }}>
                {run.answerText}
              </p>
            )}
          </div>
        )}

        {run.error && <Notice tone="error">{run.error}</Notice>}
        {run.result && !run.result.abstained && <AnswerCard result={run.result} />}
        {run.result?.abstained && <AbstainCard result={run.result} />}

        {run.result && (
          <button
            type="button"
            className="btn btn--outline"
            style={{ marginTop: "var(--sp-base)", width: "100%" }}
            onClick={() => {
              onOpenFull(fullQuestion);
              setOpen(false);
            }}
          >
            Understand better →
          </button>
        )}
      </div>

      <form className="chat-input" onSubmit={submit}>
        <input
          ref={inputRef}
          className="input"
          placeholder="Ask a question…"
          value={value}
          onChange={(e) => setValue(e.target.value)}
        />
        <button type="submit" className="btn btn--primary" disabled={run.running || !value.trim()}>
          {run.running ? "…" : "Ask"}
        </button>
      </form>
    </section>
  );
}
