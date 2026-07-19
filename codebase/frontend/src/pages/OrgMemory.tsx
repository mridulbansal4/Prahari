// Expert Knowledge Capture Workspace — M5 Organizational Memory
// Purpose: preserve decades of engineering knowledge before it retires.

import { useEffect, useRef, useState } from "react";

// ─── Types ────────────────────────────────────────────────────────────────────
type Severity = "info" | "warning" | "critical" | "near-miss";
type Category = "faq" | "tip" | "asset" | "decision" | "lesson" | "incident" | "myth" | "manual-gap" | "mistake" | "tribal" | "practice" | "interview";

interface KnowledgeEntry {
  id: string;
  category: Category;
  title: string;
  content: string;
  asset?: string;
  tags: string[];
  severity?: Severity;
  ts: string;
}

interface AiMessage {
  role: "ai" | "user";
  text: string;
}

// ─── Demo seed data ────────────────────────────────────────────────────────────
const SEED: KnowledgeEntry[] = [
  {
    id: "k1", category: "tip", title: "Pump restart sequence",
    content: "Never restart Pump A before Pump B after a shutdown. B must reach stable flow first or you get cavitation in the header.",
    tags: ["startup", "pump", "sequence"], ts: "2024-03-12T08:00:00Z"
  },
  {
    id: "k2", category: "faq", title: "Why does P-201 vibrate every summer?",
    content: "Ambient temperature above 42 C causes thermal expansion in the bearing housing. We shimmed it in 2021 but never documented it in the OEM file. Add 0.15 mm shim on the drive-end bearing.",
    tags: ["P-201", "vibration", "bearing", "summer"], ts: "2024-04-05T10:30:00Z"
  },
  {
    id: "k3", category: "myth", title: "High vibration means bearing failure",
    content: "MYTH: High vibration always means bearing failure.\n\nREALITY: 70% of the time it is shaft misalignment. Check coupling alignment first before ordering bearings.",
    tags: ["vibration", "bearing", "alignment"], ts: "2024-01-20T14:00:00Z"
  },
  {
    id: "k4", category: "lesson", title: "2019 Compressor C3 trip",
    content: "Compressor C3 tripped mid-shift during monsoon. Root cause was condensation in the inlet filter causing pressure drop. Manual drain was skipped during the previous shift. Added a checklist item — never skip drain check in monsoon season.",
    tags: ["C3", "compressor", "monsoon", "inlet-filter"], severity: "warning", ts: "2024-02-01T09:00:00Z"
  },
  {
    id: "k5", category: "tribal", title: "Vendor XYZ seal quality",
    content: "Seals from Vendor XYZ (Mumbai) fail within 6 months compared to OEM 18-month life. Finance prefers them for cost but plant pays in downtime. Use Vendor ABC for P-101B and C3.",
    tags: ["vendor", "seal", "reliability"], ts: "2024-05-10T11:00:00Z"
  },
];

const ASSETS = [
  "P-101A – Boiler Feed Pump A",
  "P-101B – Boiler Feed Pump B",
  "P-201 – Cooling Water Pump",
  "C3 – Compressor 3",
  "V12 – Isolation Valve 12",
  "T-04 – Heat Exchanger 4",
];

const AI_QUESTIONS = [
  "What is one equipment failure every new engineer at this plant should know about?",
  "Which asset worries you the most right now, and why?",
  "What mistake do junior technicians keep repeating?",
  "Is there a maintenance shortcut that should never be taken?",
  "What incident changed how you personally approach your work?",
  "What important practice is completely undocumented?",
  "What decision made years ago do you wish you could revisit?",
  "What hidden relationship exists between two assets that nobody talks about?",
  "What seasonal behaviour should every shift engineer know?",
  "What does the OEM manual get wrong for this plant's conditions?",
];

const COMPLETION_MODULES = [
  { key: "faq",      label: "FAQ Coverage" },
  { key: "asset",    label: "Asset Knowledge" },
  { key: "incident", label: "Incident Coverage" },
  { key: "lesson",   label: "Lessons Learned" },
  { key: "decision", label: "Decision Memory" },
  { key: "tip",      label: "Hidden Tips" },
  { key: "myth",     label: "Myth Busting" },
  { key: "tribal",   label: "Tribal Knowledge" },
  { key: "practice", label: "Best Practices" },
];

// ─── Helpers ───────────────────────────────────────────────────────────────────
function uid() { return Math.random().toString(36).slice(2, 10); }
function fmt(ts: string) {
  return new Date(ts).toLocaleDateString("en-IN", { day: "numeric", month: "short", year: "numeric" });
}

// ─── Category config ──────────────────────────────────────────────────────────
const CAT_COLOR: Record<string, string> = {
  faq: "var(--knowledge)", tip: "var(--signal)", asset: "var(--decision)",
  decision: "var(--decision)", lesson: "var(--warning)", incident: "var(--critical)",
  myth: "var(--investigation)", "manual-gap": "var(--evidence)",
  mistake: "var(--warning)", tribal: "var(--knowledge)",
  practice: "var(--success)", interview: "var(--investigation)",
};

const CAT_LABEL: Record<string, string> = {
  faq: "FAQ", tip: "Tip", asset: "Asset", decision: "Decision",
  lesson: "Lesson", incident: "Incident", myth: "Myth", "manual-gap": "Manual Gap",
  mistake: "Mistake", tribal: "Tribal", practice: "Practice", interview: "AI Interview",
};

// ─── Mini components ──────────────────────────────────────────────────────────
function SectionHeader({ title, sub }: { title: string; sub: string }) {
  return (
    <div style={{ marginBottom: "var(--sp-xl)" }}>
      <div className="t-headline">{title}</div>
      <div className="t-body-sm ink-muted" style={{ marginTop: 4 }}>{sub}</div>
    </div>
  );
}

function TagPills({ tags }: { tags: string[] }) {
  return (
    <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
      {tags.map(t => (
        <span key={t} style={{
          background: "var(--surface-3)", color: "var(--ink-muted)",
          fontSize: 11, padding: "2px 8px", borderRadius: "var(--r-full)",
          fontWeight: 500, letterSpacing: "0.04em",
        }}>{t}</span>
      ))}
    </div>
  );
}

function SeverityBadge({ s }: { s?: Severity }) {
  if (!s) return null;
  const map: Record<Severity, { bg: string; label: string }> = {
    info:       { bg: "var(--signal)",     label: "INFO" },
    warning:    { bg: "var(--warning)",    label: "WARNING" },
    critical:   { bg: "var(--critical)",   label: "CRITICAL" },
    "near-miss": { bg: "var(--prediction)", label: "NEAR MISS" },
  };
  return (
    <span style={{
      background: map[s].bg, color: "#fff", fontSize: 10, fontWeight: 700,
      padding: "2px 8px", borderRadius: "var(--r-full)", letterSpacing: "0.08em",
    }}>{map[s].label}</span>
  );
}

function KnowledgeCard({ entry, onDelete }: { entry: KnowledgeEntry; onDelete: (id: string) => void }) {
  return (
    <div
      className="card"
      style={{
        borderLeft: `3px solid ${CAT_COLOR[entry.category] ?? "var(--hairline)"}`,
        padding: "var(--sp-lg)",
        transition: "transform var(--dur-fast) var(--ease-snap)",
      }}
      onMouseEnter={e => (e.currentTarget.style.transform = "translateY(-1px)")}
      onMouseLeave={e => (e.currentTarget.style.transform = "translateY(0)")}
    >
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", gap: "var(--sp-sm)" }}>
        <div style={{ display: "flex", gap: "var(--sp-sm)", alignItems: "center", flexWrap: "wrap" }}>
          <span style={{
            fontSize: 10, fontWeight: 700, letterSpacing: "0.08em", textTransform: "uppercase",
            color: CAT_COLOR[entry.category] ?? "var(--ink-muted)",
          }}>{CAT_LABEL[entry.category] ?? entry.category}</span>
          <span style={{ fontWeight: 600, fontSize: 14 }}>{entry.title}</span>
          <SeverityBadge s={entry.severity} />
        </div>
        <button
          onClick={() => onDelete(entry.id)}
          style={{
            background: "none", border: "none", cursor: "pointer",
            color: "var(--ink-faint)", fontSize: 14, padding: "0 4px", flexShrink: 0,
          }}
          title="Remove"
        >✕</button>
      </div>
      {entry.asset && (
        <div style={{ fontSize: 11, color: "var(--decision)", fontWeight: 600, marginTop: 4, letterSpacing: "0.04em" }}>
          {entry.asset}
        </div>
      )}
      <div className="t-body-sm" style={{ marginTop: "var(--sp-sm)", whiteSpace: "pre-wrap", color: "var(--ink-muted)" }}>
        {entry.content}
      </div>
      <div style={{ marginTop: "var(--sp-sm)", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <TagPills tags={entry.tags} />
        <span className="t-metadata">{fmt(entry.ts)}</span>
      </div>
    </div>
  );
}

// ─── Quick Input ───────────────────────────────────────────────────────────────
function QuickInput({ onAdd }: { onAdd: (e: KnowledgeEntry) => void }) {
  const [text, setText] = useState("");
  const [category, setCategory] = useState<Category>("tip");
  const [tags, setTags] = useState("");

  const examples = [
    "Pump P-101B usually fails after monsoon season",
    "Ignore OEM manual on valve V12 — we changed it in 2018",
    "Compressor C3 always overheats when Line-3 starts",
    "Pressure gauge P102 reads 5 psi higher than actual",
  ];

  function submit() {
    if (!text.trim()) return;
    onAdd({
      id: uid(), category,
      title: text.slice(0, 60) + (text.length > 60 ? "…" : ""),
      content: text,
      tags: tags.split(",").map(t => t.trim()).filter(Boolean),
      ts: new Date().toISOString(),
    });
    setText(""); setTags("");
  }

  return (
    <div className="card" style={{ background: "var(--surface-2)", border: "1px solid var(--hairline-strong)" }}>
      <SectionHeader title="Quick Knowledge Input"
        sub="Share anything you have learned that future engineers should know." />

      <div style={{ display: "flex", flexDirection: "column", gap: "var(--sp-md)" }}>
        <textarea
          className="textarea"
          rows={5}
          value={text}
          onChange={e => setText(e.target.value)}
          placeholder={"Share anything you've learned that future engineers should know...\n\nE.g. 'This pump usually fails after monsoon' or 'Ignore OEM manual here because we changed this valve in 2018'"}
          style={{ fontSize: 15, lineHeight: 1.7, resize: "vertical", minHeight: 120 }}
        />

        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "var(--sp-md)" }}>
          <div>
            <div className="t-label" style={{ marginBottom: 6 }}>Category</div>
            <select
              value={category}
              onChange={e => setCategory(e.target.value as Category)}
              style={{
                background: "var(--surface-1)", color: "var(--ink)", border: "1px solid var(--hairline)",
                borderRadius: "var(--r-sm)", padding: "8px 12px", width: "100%", fontSize: 14,
              }}
            >
              <option value="tip">Tip / Trick</option>
              <option value="faq">FAQ Answer</option>
              <option value="asset">Asset Knowledge</option>
              <option value="lesson">Lesson Learned</option>
              <option value="incident">Incident Story</option>
              <option value="decision">Decision Memory</option>
              <option value="myth">Myth vs Reality</option>
              <option value="manual-gap">Manual Gap</option>
              <option value="mistake">Common Mistake</option>
              <option value="tribal">Tribal Knowledge</option>
              <option value="practice">Best Practice</option>
            </select>
          </div>
          <div>
            <div className="t-label" style={{ marginBottom: 6 }}>Tags (comma separated)</div>
            <input
              className="input"
              value={tags}
              onChange={e => setTags(e.target.value)}
              placeholder="pump, vibration, monsoon…"
            />
          </div>
        </div>

        <div style={{ display: "flex", gap: "var(--sp-md)", alignItems: "center", flexWrap: "wrap" }}>
          <button className="btn btn-primary" onClick={submit} disabled={!text.trim()}>
            Add to Knowledge Base
          </button>
          <label className="btn btn-secondary" style={{ cursor: "pointer" }}>
            Attach file
            <input type="file" style={{ display: "none" }} />
          </label>
          <button className="btn btn-secondary">Voice note</button>
        </div>

        <div>
          <div className="t-label" style={{ marginBottom: 8 }}>Examples — click to fill</div>
          <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
            {examples.map((ex, i) => (
              <button
                key={i}
                onClick={() => setText(ex)}
                style={{
                  background: "var(--surface-3)", color: "var(--ink-muted)",
                  border: "1px solid var(--hairline)", borderRadius: "var(--r-full)",
                  padding: "4px 12px", fontSize: 12, cursor: "pointer",
                  transition: "background var(--dur-fast) var(--ease-snap)",
                }}
                onMouseEnter={e => (e.currentTarget.style.background = "var(--surface-4)")}
                onMouseLeave={e => (e.currentTarget.style.background = "var(--surface-3)")}
              >{ex}</button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

// ─── AI Interview ──────────────────────────────────────────────────────────────
function AIInterview({ onAdd }: { onAdd: (e: KnowledgeEntry) => void }) {
  const [messages, setMessages] = useState<AiMessage[]>([
    { role: "ai", text: "I am here to help capture your expertise before it is lost. Let us start with something important.\n\n" + AI_QUESTIONS[0] }
  ]);
  const [input, setInput] = useState("");
  const [qIndex, setQIndex] = useState(1);
  const [isTyping, setIsTyping] = useState(false);
  const [extracted, setExtracted] = useState<string[]>([]);
  const [sessionEnded, setSessionEnded] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isTyping]);

  function sendMessage() {
    if (!input.trim()) return;
    const userMsg = input.trim();
    setMessages(m => [...m, { role: "user", text: userMsg }]);
    setInput("");
    setIsTyping(true);

    onAdd({
      id: uid(), category: "interview",
      title: userMsg.slice(0, 60) + (userMsg.length > 60 ? "…" : ""),
      content: userMsg, tags: ["ai-interview"],
      ts: new Date().toISOString(),
    });
    setExtracted(ex => [...ex, userMsg.slice(0, 50) + "…"]);

    setTimeout(() => {
      setIsTyping(false);
      let followUp: string;
      if (qIndex < AI_QUESTIONS.length) {
        const leads = [
          "That is incredibly valuable — 34 years of insight right there. Next: ",
          "This is exactly the kind of knowledge that saves new engineers months of trial and error. ",
          "Captured. Now — ",
          "Noted. This will be searchable by every engineer on every shift. ",
        ];
        followUp = leads[Math.floor(Math.random() * leads.length)] + AI_QUESTIONS[qIndex];
        setQIndex(q => q + 1);
      } else {
        followUp = "We have covered a tremendous amount of ground. Would you like to continue with a different topic, or shall I generate the knowledge summary now?";
        setSessionEnded(true);
      }
      setMessages(m => [...m, { role: "ai", text: followUp }]);
    }, 1200 + Math.random() * 600);
  }

  function endSession() {
    setMessages(m => [...m, {
      role: "ai",
      text: `Session complete. Here is what was extracted:\n\n` +
        `${extracted.length} knowledge items captured\n` +
        `Assets referenced: P-201, C3, P-101B (auto-detected)\n` +
        `Failure modes: 3 identified\n` +
        `Procedures: 2 undocumented steps found\n` +
        `Risks: 4 flagged for review\n` +
        `Asset relationships: 2 extracted\n` +
        `Knowledge Confidence: 87%\n\n` +
        `All entries are now searchable by the entire organization.`
    }]);
    setSessionEnded(false);
  }

  return (
    <div className="card" style={{ padding: 0, overflow: "hidden", border: "1px solid var(--investigation)" }}>
      <div style={{
        background: "var(--surface-2)",
        padding: "var(--sp-xl)",
        borderBottom: "1px solid var(--hairline)",
      }}>
        <SectionHeader title="AI Interview Mode"
          sub="The AI interviews you like an experienced knowledge engineer — extracting everything only you know." />
        <div style={{ display: "flex", gap: 8 }}>
          {["Active Listening", "Auto-Extracting", "Contextually Aware"].map(tag => (
            <span key={tag} style={{
              background: "rgba(123,127,196,0.12)", color: "var(--investigation)",
              fontSize: 11, padding: "3px 10px", borderRadius: "var(--r-full)", fontWeight: 600,
            }}>{tag}</span>
          ))}
        </div>
      </div>

      <div style={{ height: 480, overflowY: "auto", padding: "var(--sp-xl)", display: "flex", flexDirection: "column", gap: "var(--sp-md)" }}>
        {messages.map((msg, i) => (
          <div key={i} style={{
            display: "flex",
            flexDirection: msg.role === "user" ? "row-reverse" : "row",
            gap: "var(--sp-sm)", alignItems: "flex-start",
          }}>
            <div style={{
              width: 32, height: 32, borderRadius: "var(--r-full)", flexShrink: 0,
              background: msg.role === "ai" ? "var(--investigation)" : "var(--decision)",
              display: "flex", alignItems: "center", justifyContent: "center",
              fontSize: 11, fontWeight: 700, color: "#fff",
            }}>
              {msg.role === "ai" ? "AI" : "A"}
            </div>
            <div style={{
              maxWidth: "75%",
              background: msg.role === "ai" ? "var(--surface-2)" : "var(--signal-wash)",
              border: `1px solid ${msg.role === "ai" ? "var(--hairline)" : "rgba(63,170,184,0.3)"}`,
              borderRadius: msg.role === "ai" ? "2px 12px 12px 12px" : "12px 2px 12px 12px",
              padding: "var(--sp-md) var(--sp-lg)",
              fontSize: 14, lineHeight: 1.65,
              whiteSpace: "pre-wrap",
            }}>
              {msg.text}
            </div>
          </div>
        ))}
        {isTyping && (
          <div style={{ display: "flex", gap: "var(--sp-sm)", alignItems: "center" }}>
            <div style={{
              width: 32, height: 32, borderRadius: "var(--r-full)", flexShrink: 0,
              background: "var(--investigation)", display: "flex", alignItems: "center",
              justifyContent: "center", fontSize: 11, fontWeight: 700, color: "#fff",
            }}>AI</div>
            <div style={{
              background: "var(--surface-2)", border: "1px solid var(--hairline)",
              borderRadius: "2px 12px 12px 12px", padding: "var(--sp-md) var(--sp-lg)",
            }}>
              <div style={{ display: "flex", gap: 4 }}>
                {[0, 1, 2].map(i => (
                  <span key={i} style={{
                    width: 6, height: 6, borderRadius: "50%", background: "var(--ink-muted)",
                    animation: `pulse 1s ease-in-out ${i * 0.2}s infinite`,
                  }} />
                ))}
              </div>
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {extracted.length > 0 && (
        <div style={{
          background: "rgba(78,155,148,0.08)", borderTop: "1px solid var(--hairline)",
          padding: "var(--sp-md) var(--sp-xl)", display: "flex", gap: 8, alignItems: "center", flexWrap: "wrap",
        }}>
          <span style={{ color: "var(--knowledge)", fontSize: 12, fontWeight: 700 }}>Captured: {extracted.length}</span>
          {extracted.slice(-3).map((e, i) => (
            <span key={i} style={{ fontSize: 11, color: "var(--ink-subtle)", background: "var(--surface-2)", padding: "2px 8px", borderRadius: "var(--r-full)" }}>
              {e}
            </span>
          ))}
        </div>
      )}

      <div style={{ padding: "var(--sp-md) var(--sp-xl) var(--sp-xl)", borderTop: "1px solid var(--hairline)", display: "flex", gap: "var(--sp-md)" }}>
        <input
          className="input"
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === "Enter" && !isTyping && sendMessage()}
          placeholder="Share your knowledge… (Enter to send)"
          disabled={isTyping}
          style={{ flex: 1 }}
        />
        <button className="btn btn-primary" onClick={sendMessage} disabled={!input.trim() || isTyping}>
          Send
        </button>
        {sessionEnded && (
          <button className="btn btn-decision" onClick={endSession}>
            Summarize
          </button>
        )}
      </div>
    </div>
  );
}

// ─── Completeness tracker ──────────────────────────────────────────────────────
function CompletenessTracker({ entries }: { entries: KnowledgeEntry[] }) {
  const targets: Record<string, number> = {
    faq: 5, asset: 6, incident: 3, lesson: 5, decision: 4, tip: 8, myth: 3, tribal: 4, practice: 5,
  };
  return (
    <div className="card">
      <SectionHeader title="Knowledge Completeness" sub="How much of Anil's expertise has been captured." />
      <div style={{ display: "flex", flexDirection: "column", gap: "var(--sp-md)" }}>
        {COMPLETION_MODULES.map(mod => {
          const count = entries.filter(e => e.category === mod.key).length;
          const target = targets[mod.key] ?? 5;
          const pct = Math.min(100, Math.round((count / target) * 100));
          const color = pct < 30 ? "var(--critical)" : pct < 70 ? "var(--warning)" : "var(--success)";
          return (
            <div key={mod.key}>
              <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 6 }}>
                <span style={{ fontSize: 13 }}>{mod.label}</span>
                <span style={{ fontSize: 12, color, fontWeight: 700 }}>{count}/{target} — {pct}%</span>
              </div>
              <div className="progress">
                <span style={{ width: `${pct}%`, background: color }} />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

// ─── Knowledge Timeline ────────────────────────────────────────────────────────
function KnowledgeTimeline({ entries }: { entries: KnowledgeEntry[] }) {
  const sorted = [...entries].sort((a, b) => new Date(b.ts).getTime() - new Date(a.ts).getTime()).slice(0, 12);
  return (
    <div className="card">
      <SectionHeader title="Knowledge Timeline" sub="Chronological record of everything contributed." />
      <div style={{ position: "relative", paddingLeft: 24 }}>
        <div style={{ position: "absolute", left: 8, top: 0, bottom: 0, width: 2, background: "var(--hairline)" }} />
        {sorted.map(entry => (
          <div key={entry.id} style={{ position: "relative", marginBottom: 20, paddingLeft: 24 }}>
            <div style={{
              position: "absolute", left: -20, top: 4, width: 10, height: 10, borderRadius: "50%",
              background: CAT_COLOR[entry.category] ?? "var(--signal)",
              border: "2px solid var(--canvas)",
            }} />
            <div style={{ fontSize: 11, color: "var(--ink-subtle)", marginBottom: 2 }}>
              <span style={{ color: CAT_COLOR[entry.category], fontWeight: 600 }}>{CAT_LABEL[entry.category]}</span>
              {" · "}{fmt(entry.ts)}
            </div>
            <div style={{ fontSize: 13, fontWeight: 500 }}>{entry.title}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

// ─── Search ────────────────────────────────────────────────────────────────────
function KnowledgeSearch({ entries, onDelete }: { entries: KnowledgeEntry[]; onDelete: (id: string) => void }) {
  const [q, setQ] = useState("");
  const [filter, setFilter] = useState<Category | "all">("all");
  const results = entries
    .filter(e => filter === "all" || e.category === filter)
    .filter(e => {
      const s = q.toLowerCase();
      return !s || e.title.toLowerCase().includes(s) || e.content.toLowerCase().includes(s) || e.tags.some(t => t.toLowerCase().includes(s));
    });

  return (
    <div className="card">
      <SectionHeader title="Search Knowledge Base" sub="Instantly search across all captured knowledge." />
      <div style={{ display: "flex", gap: "var(--sp-md)", marginBottom: "var(--sp-lg)", flexWrap: "wrap" }}>
        <input
          className="input"
          style={{ flex: 1, minWidth: 200 }}
          value={q}
          onChange={e => setQ(e.target.value)}
          placeholder="Search by keyword, tag, asset…"
        />
        <select
          value={filter}
          onChange={e => setFilter(e.target.value as Category | "all")}
          style={{
            background: "var(--surface-1)", color: "var(--ink)", border: "1px solid var(--hairline)",
            borderRadius: "var(--r-sm)", padding: "8px 12px", fontSize: 14,
          }}
        >
          <option value="all">All types</option>
          <option value="faq">FAQ</option>
          <option value="tip">Tips</option>
          <option value="asset">Asset knowledge</option>
          <option value="lesson">Lessons</option>
          <option value="incident">Incidents</option>
          <option value="decision">Decision memory</option>
          <option value="myth">Myths</option>
          <option value="tribal">Tribal</option>
          <option value="practice">Best practices</option>
        </select>
      </div>
      <div style={{ fontSize: 12, color: "var(--ink-subtle)", marginBottom: "var(--sp-md)" }}>
        {results.length} of {entries.length} items
      </div>
      <div style={{ display: "flex", flexDirection: "column", gap: "var(--sp-md)" }}>
        {results.length === 0 && (
          <div style={{ textAlign: "center", color: "var(--ink-muted)", padding: "var(--sp-2xl) 0", fontSize: 13 }}>
            No results. Try a different search.
          </div>
        )}
        {results.map(e => <KnowledgeCard key={e.id} entry={e} onDelete={onDelete} />)}
      </div>
    </div>
  );
}

// ─── Recognition Panel ─────────────────────────────────────────────────────────
function RecognitionPanel({ entries }: { entries: KnowledgeEntry[] }) {
  const score = Math.min(100, entries.length * 6);
  const assets = new Set(entries.filter(e => e.asset).map(e => e.asset)).size;
  return (
    <div className="card" style={{ border: "1px solid var(--knowledge)" }}>
      <SectionHeader title="Expert Recognition" sub="Your contributions to this organization's collective intelligence." />
      <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "var(--sp-lg)" }}>
        {[
          { label: "Knowledge Score", value: `${score}`, unit: "/ 100",    color: "var(--knowledge)" },
          { label: "Contributions",   value: `${entries.length}`, unit: "items",    color: "var(--signal)" },
          { label: "Assets Covered",  value: `${assets}`,         unit: "assets",   color: "var(--decision)" },
          { label: "Years Preserved", value: "34",                unit: "years exp.",color: "var(--warning)" },
          { label: "Engineers Helped",value: "All",               unit: "future shifts", color: "var(--success)" },
          { label: "AI Sessions",     value: `${entries.filter(e => e.category === "interview").length}`, unit: "interviews", color: "var(--investigation)" },
        ].map(m => (
          <div key={m.label} style={{ textAlign: "center", padding: "var(--sp-lg)" }}>
            <div style={{ fontSize: 32, fontWeight: 700, color: m.color, lineHeight: 1.1 }}>{m.value}</div>
            <div style={{ fontSize: 11, color: "var(--ink-subtle)" }}>{m.unit}</div>
            <div className="t-label" style={{ marginTop: 4 }}>{m.label}</div>
          </div>
        ))}
      </div>
      {score >= 30 && (
        <div style={{
          marginTop: "var(--sp-lg)", padding: "var(--sp-md) var(--sp-lg)",
          background: "rgba(63,166,107,0.08)", borderRadius: "var(--r-md)",
          border: "1px solid rgba(63,166,107,0.2)", fontSize: 13, color: "var(--success)",
        }}>
          Outstanding contributor — your knowledge is now a permanent part of this plant's institutional memory.
        </div>
      )}
    </div>
  );
}

// ─── AI Suggestions ────────────────────────────────────────────────────────────
function AISuggestions({ entries }: { entries: KnowledgeEntry[] }) {
  const suggestions = [
    entries.some(e => e.tags.includes("P-201")) && "Link P-201 vibration knowledge to Asset Map entry P-201",
    entries.filter(e => e.category === "faq").length >= 2 && `${entries.filter(e => e.category === "faq").length} FAQs ready to publish to the plant knowledge base`,
    entries.some(e => e.category === "tip") && "Convert best tips to formal Best Practices for new-engineer onboarding",
    entries.some(e => e.category === "incident") && "Incident knowledge flagged for safety review — attach to Compliance module",
    entries.some(e => e.category === "tribal") && "Tribal knowledge about vendors should link to Execution Center procurement workflow",
  ].filter(Boolean) as string[];

  if (!suggestions.length) return null;

  return (
    <div className="card" style={{ borderLeft: "3px solid var(--investigation)" }}>
      <div className="t-title" style={{ marginBottom: "var(--sp-lg)" }}>AI Suggestions</div>
      <div style={{ display: "flex", flexDirection: "column", gap: "var(--sp-sm)" }}>
        {suggestions.map((s, i) => (
          <div key={i} style={{
            display: "flex", alignItems: "flex-start", gap: "var(--sp-md)",
            background: "var(--surface-2)", padding: "var(--sp-md)", borderRadius: "var(--r-md)",
          }}>
            <span style={{ color: "var(--investigation)", flexShrink: 0, fontWeight: 700 }}>—</span>
            <span style={{ fontSize: 13 }}>{s}</span>
            <button className="btn btn-secondary" style={{ marginLeft: "auto", flexShrink: 0, fontSize: 11, padding: "4px 10px" }}>
              Apply
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

// ─── Generic structured form module ───────────────────────────────────────────
interface StructuredFormConfig {
  title: string; sub: string; category: Category;
  fields: { key: string; label: string; placeholder: string; type?: "text" | "textarea" | "select"; options?: string[] }[];
}

function StructuredModule({ config, entries, onAdd, onDelete }: {
  config: StructuredFormConfig;
  entries: KnowledgeEntry[];
  onAdd: (e: KnowledgeEntry) => void;
  onDelete: (id: string) => void;
}) {
  const initState = () => Object.fromEntries(config.fields.map(f => [f.key, ""]));
  const [form, setForm] = useState<Record<string, string>>(initState());
  const [open, setOpen] = useState(false);

  const relevant = entries.filter(e => e.category === config.category);

  function submit() {
    const primary = config.fields[0];
    if (!form[primary.key]?.trim()) return;
    const content = config.fields.map(f => `${f.label}:\n${form[f.key]}`).join("\n\n");
    onAdd({
      id: uid(), category: config.category,
      title: form[primary.key].slice(0, 70),
      content, tags: [],
      ts: new Date().toISOString(),
    });
    setForm(initState());
    setOpen(false);
  }

  return (
    <div className="card">
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "var(--sp-lg)" }}>
        <div>
          <div className="t-title">{config.title}</div>
          <div className="t-caption" style={{ marginTop: 4 }}>{config.sub}</div>
        </div>
        <div style={{ display: "flex", gap: 12, alignItems: "center" }}>
          <span style={{ fontSize: 12, color: "var(--knowledge)", fontWeight: 700 }}>{relevant.length} captured</span>
          <button className="btn btn-secondary" onClick={() => setOpen(o => !o)}>
            {open ? "Close" : "+ Add"}
          </button>
        </div>
      </div>

      {open && (
        <div style={{
          background: "var(--surface-2)", border: "1px solid var(--hairline)",
          borderRadius: "var(--r-md)", padding: "var(--sp-xl)", marginBottom: "var(--sp-lg)",
        }}>
          {config.fields.map(f => (
            <div key={f.key} style={{ marginBottom: "var(--sp-md)" }}>
              <div className="t-label" style={{ marginBottom: 6 }}>{f.label}</div>
              {f.type === "textarea" ? (
                <textarea
                  className="textarea"
                  value={form[f.key]}
                  onChange={e => setForm(fm => ({ ...fm, [f.key]: e.target.value }))}
                  placeholder={f.placeholder}
                  rows={3}
                />
              ) : f.type === "select" ? (
                <select
                  value={form[f.key]}
                  onChange={e => setForm(fm => ({ ...fm, [f.key]: e.target.value }))}
                  style={{
                    background: "var(--surface-1)", color: "var(--ink)", border: "1px solid var(--hairline)",
                    borderRadius: "var(--r-sm)", padding: "8px 12px", width: "100%", fontSize: 14,
                  }}
                >
                  <option value="">— Select —</option>
                  {(f.options ?? ASSETS).map(o => <option key={o} value={o}>{o}</option>)}
                </select>
              ) : (
                <input
                  className="input"
                  value={form[f.key]}
                  onChange={e => setForm(fm => ({ ...fm, [f.key]: e.target.value }))}
                  placeholder={f.placeholder}
                />
              )}
            </div>
          ))}
          <button className="btn btn-primary" onClick={submit}>Save</button>
        </div>
      )}

      {relevant.length === 0 && !open && (
        <div style={{ textAlign: "center", color: "var(--ink-subtle)", padding: "var(--sp-2xl) 0", fontSize: 13 }}>
          Nothing captured yet. Click "+ Add" to start.
        </div>
      )}
      <div style={{ display: "flex", flexDirection: "column", gap: "var(--sp-md)" }}>
        {relevant.map(e => <KnowledgeCard key={e.id} entry={e} onDelete={onDelete} />)}
      </div>
    </div>
  );
}

// ─── Module configs ────────────────────────────────────────────────────────────
const MODULES: Record<string, StructuredFormConfig> = {
  faq: {
    title: "Frequently Asked Questions", category: "faq",
    sub: "Questions you get asked repeatedly — make the answers searchable for everyone.",
    fields: [
      { key: "question", label: "Question", placeholder: "Why does Pump P-201 vibrate every summer?" },
      { key: "answer", label: "Answer", placeholder: "Detailed answer that future engineers can trust…", type: "textarea" },
      { key: "asset", label: "Related asset (optional)", placeholder: "e.g. P-201, C3…" },
    ],
  },
  tips: {
    title: "Tips & Tricks", category: "tip",
    sub: "Small practical things every engineer should know but nobody writes down.",
    fields: [
      { key: "title", label: "The tip", placeholder: "Never restart Pump A before Pump B" },
      { key: "content", label: "Full explanation", placeholder: "Why this matters and what happens if ignored…", type: "textarea" },
    ],
  },
  assets: {
    title: "Asset-Specific Knowledge", category: "asset",
    sub: "Attach your expertise directly to specific equipment.",
    fields: [
      { key: "asset", label: "Asset", placeholder: "Select asset", type: "select" },
      { key: "knowledge", label: "What do you know about this asset?", placeholder: "This seal usually leaks after 18 months…", type: "textarea" },
      { key: "source", label: "Source", placeholder: "e.g. Personal observation, 34 years" },
    ],
  },
  decisions: {
    title: "Decision Memory", category: "decision",
    sub: "Capture why decisions were made — so no failure repeats because the plant forgot.",
    fields: [
      { key: "decision", label: "Decision made", placeholder: "e.g. Replaced Pump A instead of repairing it" },
      { key: "reason", label: "Reason", placeholder: "Why was this the right call at the time?", type: "textarea" },
      { key: "alternatives", label: "Alternatives considered", placeholder: "What other options were evaluated?", type: "textarea" },
      { key: "why_rejected", label: "Why alternatives were rejected", placeholder: "Cost, time, risk, technical constraints…", type: "textarea" },
      { key: "outcome", label: "Outcome", placeholder: "What actually happened?", type: "textarea" },
      { key: "revisit", label: "Would you do it differently today?", placeholder: "Honest reflection…", type: "textarea" },
    ],
  },
  lessons: {
    title: "Lessons Learned", category: "lesson",
    sub: "What the plant learned — so the next team does not pay the same price.",
    fields: [
      { key: "title", label: "Title", placeholder: "e.g. Compressor C3 Monsoon Trip 2019" },
      { key: "description", label: "What happened and what was learned", placeholder: "Describe the lesson in detail…", type: "textarea" },
      { key: "tags", label: "Tags (comma separated)", placeholder: "monsoon, compressor, inlet-filter" },
    ],
  },
  incidents: {
    title: "Incident Stories", category: "incident",
    sub: "Engineering case studies. What happened, what caused it, what fixed it, what everyone must remember.",
    fields: [
      { key: "title", label: "Incident title", placeholder: "e.g. Boiler feed pump cavitation — July 2021" },
      { key: "what_happened", label: "What happened", placeholder: "Timeline of events…", type: "textarea" },
      { key: "cause", label: "Root cause", placeholder: "What actually caused it?", type: "textarea" },
      { key: "fix", label: "What fixed it", placeholder: "How was it resolved?", type: "textarea" },
      { key: "remember", label: "What everyone must remember", placeholder: "The one thing not to forget…", type: "textarea" },
    ],
  },
  myths: {
    title: "Myth vs Reality", category: "myth",
    sub: "Correct dangerous misconceptions before they cause another incident.",
    fields: [
      { key: "myth", label: "The Myth", placeholder: "High vibration means bearing failure" },
      { key: "reality", label: "The Reality", placeholder: "70% of the time it is shaft misalignment…", type: "textarea" },
      { key: "asset", label: "Applies to", placeholder: "All rotating equipment, or specific?" },
    ],
  },
  manuals: {
    title: "Things Manuals Don't Tell You", category: "manual-gap",
    sub: "Undocumented knowledge that experienced engineers carry in their heads.",
    fields: [
      { key: "title", label: "What the manual does not cover", placeholder: "e.g. Valve V12 requires manual tightening before start" },
      { key: "content", label: "The full story", placeholder: "What do you know that is not written anywhere?", type: "textarea" },
      { key: "asset", label: "Asset or system", placeholder: "Select asset", type: "select" },
    ],
  },
  mistakes: {
    title: "Common Mistakes New Engineers Make", category: "mistake",
    sub: "Save them years of painful learning by writing it down now.",
    fields: [
      { key: "mistake", label: "The mistake", placeholder: "Forgetting to isolate pressure before opening the seal" },
      { key: "consequence", label: "What happens when they make it", placeholder: "Consequence or near-miss scenario", type: "textarea" },
      { key: "correct", label: "The correct approach", placeholder: "What should they do instead?", type: "textarea" },
    ],
  },
  tribal: {
    title: "Tribal Knowledge", category: "tribal",
    sub: "Unwritten knowledge about vendors, shifts, seasonal behaviour, quirks, workarounds.",
    fields: [
      { key: "title", label: "What do you know that most people do not?", placeholder: "e.g. Vendor XYZ seals fail in 6 months" },
      { key: "content", label: "Full details", placeholder: "The complete picture — be specific", type: "textarea" },
      { key: "tags", label: "Category tags", placeholder: "vendor, shift, seasonal, workaround, quirk…" },
    ],
  },
  practices: {
    title: "Best Practices", category: "practice",
    sub: "Proven recommendations — what to do, what not to do, and why.",
    fields: [
      { key: "do", label: "Always Do", placeholder: "Inspect seal visually before startup" },
      { key: "dont", label: "Never Do", placeholder: "Never skip lubrication interval under time pressure" },
      { key: "why", label: "Why (the reasoning that makes it stick)", placeholder: "What failure have you seen from not following this?", type: "textarea" },
      { key: "asset", label: "Applies to", placeholder: "Select asset", type: "select" },
    ],
  },
};

// ─── Tab definition ────────────────────────────────────────────────────────────
const TABS = [
  { id: "overview",   label: "Overview" },
  { id: "capture",    label: "Quick Capture" },
  { id: "interview",  label: "AI Interview" },
  { id: "faq",        label: "FAQs" },
  { id: "tips",       label: "Tips & Tricks" },
  { id: "assets",     label: "Asset Knowledge" },
  { id: "decisions",  label: "Decision Memory" },
  { id: "lessons",    label: "Lessons Learned" },
  { id: "incidents",  label: "Incidents" },
  { id: "myths",      label: "Myth vs Reality" },
  { id: "manuals",    label: "Manual Gaps" },
  { id: "mistakes",   label: "Mistakes" },
  { id: "tribal",     label: "Tribal Knowledge" },
  { id: "practices",  label: "Best Practices" },
  { id: "search",     label: "Search" },
];

// ─── Main export ───────────────────────────────────────────────────────────────
export function OrgMemory() {
  const [entries, setEntries] = useState<KnowledgeEntry[]>(SEED);
  const [tab, setTab] = useState("overview");

  function addEntry(e: KnowledgeEntry) { setEntries(prev => [e, ...prev]); }
  function deleteEntry(id: string)     { setEntries(prev => prev.filter(e => e.id !== id)); }

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100%", minHeight: 0 }}>

      {/* Hero header */}
      <div style={{
        background: "var(--surface-1)",
        borderBottom: "1px solid var(--hairline)",
        padding: "var(--sp-xl) var(--sp-xl) 0",
        flexShrink: 0,
      }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "var(--sp-xl)", flexWrap: "wrap", gap: "var(--sp-lg)" }}>
          <div>
            <div className="t-label" style={{ color: "var(--knowledge)", marginBottom: 6 }}>M5 · Organizational Memory</div>
            <div className="t-display-md">Expert Knowledge Capture</div>
            <div className="t-subtitle ink-muted" style={{ marginTop: 6 }}>
              Anil Kumar · Reliability Engineer · 34 years · Preserving institutional memory
            </div>
          </div>
          <div style={{ display: "flex", gap: "var(--sp-md)" }}>
            <div style={{
              background: "var(--surface-2)", border: "1px solid var(--knowledge)",
              borderRadius: "var(--r-md)", padding: "var(--sp-sm) var(--sp-lg)", textAlign: "center",
            }}>
              <div style={{ fontSize: 28, fontWeight: 700, color: "var(--knowledge)" }}>{entries.length}</div>
              <div className="t-label">Items captured</div>
            </div>
            <div style={{
              background: "var(--surface-2)", border: "1px solid var(--decision)",
              borderRadius: "var(--r-md)", padding: "var(--sp-sm) var(--sp-lg)", textAlign: "center",
            }}>
              <div style={{ fontSize: 28, fontWeight: 700, color: "var(--decision)" }}>
                {Math.min(100, entries.length * 6)}%
              </div>
              <div className="t-label">Completeness</div>
            </div>
          </div>
        </div>

        {/* Tab bar */}
        <div style={{ display: "flex", gap: 0, overflowX: "auto" }}>
          {TABS.map(t => (
            <button
              key={t.id}
              onClick={() => setTab(t.id)}
              style={{
                background: "none", border: "none", cursor: "pointer",
                padding: "10px 16px", fontSize: 13, fontWeight: 600,
                whiteSpace: "nowrap", flexShrink: 0,
                color: tab === t.id ? "var(--ink)" : "var(--ink-muted)",
                borderBottom: tab === t.id ? "2px solid var(--signal)" : "2px solid transparent",
                transition: "color var(--dur-fast) var(--ease-snap)",
              }}
            >{t.label}</button>
          ))}
        </div>
      </div>

      {/* Content */}
      <div style={{ flex: 1, overflowY: "auto", padding: "var(--sp-xl)" }}>
        <div style={{ maxWidth: 960, margin: "0 auto", display: "flex", flexDirection: "column", gap: "var(--sp-xl)" }}>

          {tab === "overview" && (
            <>
              <RecognitionPanel entries={entries} />
              <AISuggestions entries={entries} />
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "var(--sp-xl)" }}>
                <CompletenessTracker entries={entries} />
                <KnowledgeTimeline entries={entries} />
              </div>
              <div>
                <div className="t-label" style={{ marginBottom: "var(--sp-md)" }}>Recent Contributions</div>
                <div style={{ display: "flex", flexDirection: "column", gap: "var(--sp-md)" }}>
                  {entries.slice(0, 5).map(e => <KnowledgeCard key={e.id} entry={e} onDelete={deleteEntry} />)}
                </div>
              </div>
            </>
          )}

          {tab === "capture"   && <QuickInput onAdd={addEntry} />}
          {tab === "interview" && <AIInterview onAdd={addEntry} />}
          {tab === "search"    && <KnowledgeSearch entries={entries} onDelete={deleteEntry} />}

          {(["faq","tips","assets","decisions","lessons","incidents","myths","manuals","mistakes","tribal","practices"] as const)
            .filter(k => tab === k)
            .map(k => (
              <StructuredModule
                key={k}
                config={MODULES[k]}
                entries={entries}
                onAdd={addEntry}
                onDelete={deleteEntry}
              />
            ))
          }

        </div>
      </div>
    </div>
  );
}
