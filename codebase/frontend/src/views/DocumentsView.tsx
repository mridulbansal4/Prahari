// Documents — upload plus the library, grouped by the doc_type the backend actually detected
// (previously this was guessed from the filename, which mis-filed anything oddly named).
import { useCallback, useEffect, useRef, useState } from "react";
import { DocumentContentView } from "../components/DocumentContent";
import { Badge, EmptyState, Notice, Skeleton, ViewHeader } from "../components/ui";
import { api } from "../lib/api";
import { ensureSession } from "../lib/session";
import type { DocumentContent } from "../lib/types";

interface Job {
  job_id: string;
  doc_id: string;
  filename: string;
  status: string;
  node_count: number;
  edge_count: number;
  span_count: number;
  quarantine_reason: string | null;
  stage_log?: { stage: string; doc_type?: string; entities?: number }[];
}

/** The backend's detected doc_type, mapped to plain language. */
const TYPE_LABEL: Record<string, string> = {
  pid: "Drawings & diagrams",
  drawing: "Drawings & diagrams",
  csv: "Spreadsheets & data",
  xlsx: "Spreadsheets & data",
  tsv: "Spreadsheets & data",
  maintenance: "Maintenance records",
  workorder: "Maintenance records",
  inspection: "Inspection reports",
  safety: "Safety & procedures",
  procedure: "Safety & procedures",
  text: "Notes & text",
  md: "Notes & text",
  pdf: "Reports & documents",
  json: "Structured data",
};

function detectedType(job: Job): string {
  const detect = job.stage_log?.find((s) => s.doc_type);
  return detect?.doc_type ?? "";
}

/** Fallback used only when the backend's detected type carries no meaning. */
const NAME_RULES: { label: string; test: RegExp }[] = [
  { label: "Drawings & diagrams", test: /p&?id|drawing|dwg|isometric|layout|schematic/i },
  { label: "Inspection reports", test: /inspect|condition_monitoring|ndt|thickness|survey/i },
  { label: "Safety & procedures", test: /safety|loto|sop|procedure|permit|operating_manual|compliance/i },
  { label: "Maintenance records", test: /maint|workorder|work_order|wo_|repair|strainer/i },
  { label: "Incidents & lessons", test: /incident|lesson|rca|near_miss/i },
  { label: "Equipment data", test: /datasheet|register|identifiers|tag/i },
];

function groupLabel(job: Job): string {
  const t = detectedType(job);
  // The backend detects type from the file extension only, so every .md comes back as "text".
  // That would file a P&ID, an incident report and a LOTO procedure in one bucket, so for the
  // generic types we infer from the filename instead.
  if (t && t !== "text" && TYPE_LABEL[t]) return TYPE_LABEL[t];
  const byName = NAME_RULES.find((r) => r.test.test(job.filename));
  if (byName) return byName.label;
  return TYPE_LABEL[t] ?? (t ? `${t.toUpperCase()} files` : "Other documents");
}

/** Pipeline stages the backend reports, in plain language. */
const STAGE_LABEL: Record<string, string> = {
  detect: "Working out what kind of file it is",
  parse: "Reading the contents",
  extract: "Pulling out equipment and relationships",
  resolution_handoff: "Linking it to what you already have",
};

interface Upload {
  name: string;
  state: "waiting" | "uploading" | "done" | "error";
  message?: string;
}

export function DocumentsView() {
  const [jobs, setJobs] = useState<Job[] | null>(null);
  const [quarantined, setQuarantined] = useState<any[]>([]);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [uploads, setUploads] = useState<Upload[]>([]);
  const [dragging, setDragging] = useState(false);
  const fileInput = useRef<HTMLInputElement>(null);

  // The open document's content viewer.
  const [openDoc, setOpenDoc] = useState<{ id: string; filename: string } | null>(null);
  const [content, setContent] = useState<DocumentContent | null>(null);
  const [contentError, setContentError] = useState<string | null>(null);

  const openDocument = useCallback((id: string, filename: string) => {
    setOpenDoc({ id, filename });
    setContent(null);
    setContentError(null);
    ensureSession()
      .then(() => api.documentContent(id))
      .then(setContent)
      .catch(() => setContentError("Couldn't load this document's content."));
  }, []);

  const refresh = useCallback(async () => {
    try {
      await ensureSession();
      const r = await api.ingestionJobs();
      setJobs(r.jobs ?? []);
      setQuarantined(r.quarantined ?? []);
      setLoadError(null);
    } catch (e: any) {
      // Never render "no documents" for a failed load — that claims the library is empty
      // when we simply couldn't read it.
      setJobs([]);
      setLoadError(
        e?.status === 403
          ? "This session isn't allowed to list documents."
          : "Couldn't load your documents. Check that the backend is running.",
      );
    }
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  const upload = useCallback(
    async (files: FileList | null) => {
      if (!files?.length) return;
      const list = Array.from(files);
      setUploads(list.map((f) => ({ name: f.name, state: "waiting" as const })));
      await ensureSession();

      for (let i = 0; i < list.length; i++) {
        setUploads((prev) => prev.map((u, j) => (j === i ? { ...u, state: "uploading" } : u)));
        try {
          await api.uploadDocument(list[i]);
          setUploads((prev) => prev.map((u, j) => (j === i ? { ...u, state: "done" } : u)));
        } catch (e: any) {
          setUploads((prev) =>
            prev.map((u, j) =>
              j === i ? { ...u, state: "error", message: e?.message ?? "failed" } : u,
            ),
          );
        }
      }
      await refresh();
    },
    [refresh],
  );

  const busy = uploads.some((u) => u.state === "uploading" || u.state === "waiting");

  // Group by detected type.
  const groups = new Map<string, Job[]>();
  for (const j of jobs ?? []) {
    const label = groupLabel(j);
    groups.set(label, [...(groups.get(label) ?? []), j]);
  }

  return (
    <>
      <ViewHeader
        title="Your documents"
        helper="Everything the system has read. Drop in anything new — drawings, records, procedures, spreadsheets."
      />

      <div
        onDragOver={(e) => {
          e.preventDefault();
          setDragging(true);
        }}
        onDragLeave={() => setDragging(false)}
        onDrop={(e) => {
          e.preventDefault();
          setDragging(false);
          upload(e.dataTransfer.files);
        }}
        className="card"
        style={{
          borderStyle: "dashed",
          borderWidth: dragging ? 2 : 1,
          borderColor: dragging ? "var(--ink)" : "var(--hairline-strong)",
          background: dragging ? "var(--surface-strong)" : "var(--surface-card)",
          padding: "var(--sp-xxl) var(--sp-lg)",
          textAlign: "center",
          transition: "border-color var(--dur) var(--ease), background var(--dur) var(--ease)",
        }}
      >
        <div className="t-display-sm" style={{ marginBottom: "var(--sp-xs)" }}>
          Drop files here
        </div>
        <p className="t-body" style={{ maxWidth: 460, margin: "0 auto var(--sp-lg)" }}>
          PDFs, spreadsheets, text files and scans. Each one is read, and every fact taken from
          it keeps a link back to the page it came from.
        </p>
        <input
          ref={fileInput}
          type="file"
          multiple
          accept=".csv,.txt,.md,.pdf,.json,.xlsx,.tsv"
          style={{ display: "none" }}
          onChange={(e) => upload(e.target.files)}
        />
        <button
          type="button"
          className="btn btn--primary"
          onClick={() => fileInput.current?.click()}
          disabled={busy}
        >
          {busy ? "Adding…" : "Choose files"}
        </button>
      </div>

      {/* Per-file progress */}
      {uploads.length > 0 && (
        <div className="card" style={{ marginTop: "var(--sp-base)" }}>
          <div className="t-label" style={{ marginBottom: "var(--sp-sm)" }}>
            Adding {uploads.length} {uploads.length === 1 ? "file" : "files"}
          </div>
          <div className="stack" style={{ gap: "var(--sp-xs)" }}>
            {uploads.map((u, i) => (
              <div key={i} className="stack" style={{ gap: 4 }}>
                <div className="row" style={{ justifyContent: "space-between", gap: "var(--sp-xs)" }}>
                  <span className="t-body-sm ink" style={{ wordBreak: "break-word" }}>
                    {u.name}
                  </span>
                  <span
                    className="t-caption"
                    style={{ color: u.state === "error" ? "var(--error)" : "var(--muted)" }}
                  >
                    {u.state === "waiting" && "Waiting"}
                    {u.state === "uploading" && "Reading…"}
                    {u.state === "done" && "Added"}
                    {u.state === "error" && (u.message ?? "Failed")}
                  </span>
                </div>
                {u.state === "uploading" && <div className="progress" />}
                {u.state === "done" && (
                  <div
                    style={{
                      height: 2,
                      background: "var(--ink)",
                      borderRadius: "var(--r-pill)",
                    }}
                  />
                )}
              </div>
            ))}
          </div>
          {!busy && (
            <button
              type="button"
              className="btn btn--text"
              style={{ marginTop: "var(--sp-xs)" }}
              onClick={() => setUploads([])}
            >
              Clear
            </button>
          )}
        </div>
      )}

      <div style={{ marginTop: "var(--sp-xl)" }}>
        {jobs === null && (
          <div className="stack" style={{ gap: "var(--sp-xs)" }}>
            <Skeleton height={56} />
            <Skeleton height={56} />
          </div>
        )}

        {loadError && (
          <div style={{ marginBottom: "var(--sp-base)" }}>
            <Notice tone="error">{loadError}</Notice>
          </div>
        )}

        {jobs !== null && jobs.length === 0 && !loadError && (
          <EmptyState
            title="No documents yet"
            body="Once you add a file it shows up here, grouped by type, with what the system pulled out of it."
          >
            <button
              type="button"
              className="btn btn--outline"
              onClick={() => fileInput.current?.click()}
            >
              Add your first document
            </button>
          </EmptyState>
        )}

        {[...groups.entries()].map(([label, items]) => (
          <div key={label} style={{ marginBottom: "var(--sp-xl)" }}>
            <div className="t-label" style={{ marginBottom: "var(--sp-sm)" }}>
              {label} · {items.length}
            </div>
            <div className="doc-grid" style={{ display: "grid", gap: "var(--sp-sm)" }}>
              {items.map((j) => (
                <div key={j.job_id} className="card card--hover">
                  <div
                    className="row"
                    style={{ justifyContent: "space-between", gap: "var(--sp-xs)" }}
                  >
                    <span className="t-body-strong" style={{ wordBreak: "break-word" }}>
                      {j.filename}
                    </span>
                    <Badge tone={j.status === "complete" ? "success" : "neutral"}>
                      {j.status === "complete" ? "Read" : j.status}
                    </Badge>
                  </div>
                  <p className="t-caption" style={{ marginTop: "var(--sp-xs)" }}>
                    {j.node_count} {j.node_count === 1 ? "thing" : "things"} identified ·{" "}
                    {j.span_count} {j.span_count === 1 ? "passage" : "passages"} kept as evidence
                  </p>
                  <button
                    type="button"
                    className="btn btn--outline"
                    style={{ minHeight: 32, marginTop: "var(--sp-sm)" }}
                    onClick={() => openDocument(j.doc_id, j.filename)}
                  >
                    View content
                  </button>
                  {j.stage_log && j.stage_log.length > 0 && (
                    <details style={{ marginTop: "var(--sp-xs)" }}>
                      <summary
                        className="t-caption"
                        style={{ cursor: "pointer", color: "var(--muted)" }}
                      >
                        How it was read
                      </summary>
                      <ol style={{ margin: "var(--sp-xs) 0 0", paddingLeft: "var(--sp-md)" }}>
                        {j.stage_log.map((s, i) => (
                          <li key={i} className="t-caption">
                            {STAGE_LABEL[s.stage] ?? s.stage}
                            {s.entities !== undefined ? ` — ${s.entities} found` : ""}
                          </li>
                        ))}
                      </ol>
                    </details>
                  )}
                </div>
              ))}
            </div>
          </div>
        ))}

        {quarantined.length > 0 && (
          <div className="card" style={{ borderColor: "var(--error)" }}>
            <div className="t-label" style={{ marginBottom: "var(--sp-xs)", color: "var(--error)" }}>
              Set aside — not used in answers
            </div>
            <p className="t-body-sm" style={{ marginBottom: "var(--sp-sm)" }}>
              These couldn&rsquo;t be read confidently, so nothing from them is used. Nothing is
              guessed at.
            </p>
            {quarantined.map((q, i) => (
              <div key={i} className="t-body-sm">
                <strong>{q.filename}</strong> — {q.quarantine_reason ?? "unreadable"}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Content preview — a modal over the library, so the list stays put and there is no
          page navigation. Close with the ✕, the backdrop, or Escape. */}
      {openDoc && (
        <div
          className="doc-modal-scrim"
          role="dialog"
          aria-modal="true"
          aria-label={openDoc.filename}
          onClick={() => setOpenDoc(null)}
          onKeyDown={(e) => e.key === "Escape" && setOpenDoc(null)}
        >
          <div className="doc-modal" onClick={(e) => e.stopPropagation()}>
            <header className="doc-modal-head">
              <div style={{ minWidth: 0 }}>
                <div className="t-title-md" style={{ wordBreak: "break-word" }}>
                  {openDoc.filename}
                </div>
                <div className="t-caption">
                  {content
                    ? `${content.passage_count} passages · ${content.page_count} ${
                        content.page_count === 1 ? "page" : "pages"
                      } · the content the system reads and cites`
                    : "Loading…"}
                </div>
              </div>
              <button
                type="button"
                className="doc-modal-close"
                onClick={() => setOpenDoc(null)}
                aria-label="Close"
                autoFocus
              >
                ✕
              </button>
            </header>

            <div className="doc-modal-body">
              {contentError && <Notice tone="error">{contentError}</Notice>}
              {!content && !contentError && (
                <div className="stack" style={{ gap: "var(--sp-sm)" }}>
                  <Skeleton height={28} width={320} />
                  <Skeleton height={240} />
                </div>
              )}
              {content && <DocumentContentView content={content} />}
            </div>
          </div>
        </div>
      )}
    </>
  );
}
