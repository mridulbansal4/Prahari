// REST client for the core API. Bearer token from auth context; /v1 proxied to core in dev.
const TOKEN_KEY = "prahari.token";

export function setToken(t: string | null): void {
  if (t) localStorage.setItem(TOKEN_KEY, t);
  else localStorage.removeItem(TOKEN_KEY);
}
export function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY);
}

async function req<T>(method: string, path: string, body?: unknown): Promise<T> {
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  const token = getToken();
  if (token) headers.Authorization = `Bearer ${token}`;
  const res = await fetch(path, {
    method,
    headers,
    body: body !== undefined ? JSON.stringify(body) : undefined,
  });
  if (!res.ok) {
    let detail = res.statusText;
    try {
      const j = await res.json();
      detail = j?.error?.message || detail;
    } catch {
      /* non-JSON */
    }
    throw new ApiError(res.status, detail);
  }
  return (await res.json()) as T;
}

export class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
  ) {
    super(message);
  }
}

export const api = {
  login: (username: string) =>
    req<{ token: string; name: string; role: string; tenant: string }>("POST", "/v1/auth/login", {
      username,
    }),
  me: () => req<import("./types").Me>("GET", "/v1/auth/me"),

  askInvestigation: (question: string, as_of?: string, context?: { asset_id?: string }) =>
    req<{ investigation_id: string }>("POST", "/v1/investigations", { question, as_of, context }),
  getInvestigation: (id: string) =>
    req<import("./types").InvestigationResult>("GET", `/v1/investigations/${id}`),
  recentInvestigations: () =>
    req<{ items: { investigation_id: string; question: string; abstained: boolean }[] }>(
      "GET",
      "/v1/investigations",
    ),

  resolutionQueue: () =>
    req<{ proposals: import("./types").ResolutionProposal[]; corpus_size: number }>(
      "GET",
      "/v1/resolution/queue",
    ),
  adjudicate: (
    id: string,
    decision: "merge" | "separate",
    approver: string,
    corrected_target_asset_id?: string,
  ) =>
    req<{ resulting_asset_id: string | null; reversible_id: string | null }>(
      "POST",
      `/v1/resolution/${id}/adjudicate`,
      { decision, approver, corrected: !!corrected_target_asset_id, corrected_target_asset_id },
    ),
  unmerge: (mergeId: string) =>
    req<{ restored: boolean }>("POST", `/v1/resolution/unmerge/${mergeId}`),
  resolutionHistory: (assetId: string) =>
    req<{ history?: any[]; entries?: any[] }>(
      "GET",
      `/v1/resolution/assets/${assetId}/history`,
    ),

  assets: () =>
    req<{ assets: { id: string; tag: string; name: string; iso_class: string }[] }>(
      "GET",
      "/v1/assets",
    ),

  compliance: (assetId: string) =>
    req<{ rows: import("./types").ComplianceRow[]; coverage: import("./types").Coverage }>(
      "GET",
      `/v1/compliance/assets/${assetId}`,
    ),

  draftWorkOrder: (asset_id: string, symptom: string, investigation_id?: string) =>
    req<{ draft_id: string; preview: Record<string, unknown>; status: string }>(
      "POST",
      "/v1/actions/work-order/draft",
      { asset_id, symptom, investigation_id },
    ),
  submitWorkOrder: (draft_id: string, approver: string, cmms_ok = true) =>
    req<{ cmms_work_order_id: string; status: string }>("POST", "/v1/actions/work-order/submit", {
      draft_id,
      approver,
      cmms_ok,
    }),
  rejectWorkOrder: (draft_id: string, reason?: string) =>
    req<{ status: string }>("POST", "/v1/actions/work-order/reject", { draft_id, reason }),
  listActions: () => req<{ drafts: any[] }>("GET", "/v1/actions"),

  submitCorrection: (payload: {
    target_kind: string;
    target_ref: string;
    new_value: string;
    rationale: string;
    author: string;
    prior_value?: string;
  }) => req<{ correction_id: string }>("POST", "/v1/corrections", payload),
  corrections: (target_ref?: string) =>
    req<{ corrections: any[] }>(
      "GET",
      `/v1/corrections${target_ref ? `?target_ref=${target_ref}` : ""}`,
    ),

  audit: (q: { actor?: string; action?: string } = {}) => {
    const p = new URLSearchParams(q as Record<string, string>).toString();
    return req<{ entries: any[] }>("GET", `/v1/audit${p ? `?${p}` : ""}`);
  },
  analytics: () => req<any>("GET", "/v1/analytics"),
  orgMemory: () => req<{ people: import("./types").ExpertiseRecord[] }>("GET", "/v1/org-memory"),
  captureKnowledge: (payload: {
    person_id: string;
    target_ref: string;
    expertise: string;
    text: string;
    kind: string;
    tags: string[];
  }) =>
    req<{ ok: boolean; item: import("./types").KnowledgeItem }>(
      "POST",
      "/v1/org-memory/knows",
      payload,
    ),
  knowledgeHealth: () => req<{ flags: any[]; last_run: any }>("GET", "/v1/knowledge/health"),
  runDecay: () => req<{ flags: any[] }>("POST", "/v1/knowledge/run-decay"),
  decisions: () => req<{ decisions: any[] }>("GET", "/v1/decisions"),
  replay: (id: string) => req<any>("GET", `/v1/decisions/${id}/replay`),

  uploadDocument: async (file: File) => {
    const form = new FormData();
    form.append("file", file);
    const token = getToken();
    const res = await fetch("/v1/documents", {
      method: "POST",
      headers: token ? { Authorization: `Bearer ${token}` } : {},
      body: form,
    });
    if (!res.ok) {
      let m = res.statusText;
      try {
        m = (await res.json())?.error?.message || m;
      } catch {
        /* non-JSON */
      }
      throw new ApiError(res.status, m);
    }
    return (await res.json()) as { doc_id: string; job_id: string; status: string };
  },
  ingestionJobs: () => req<{ jobs: any[]; quarantined: any[] }>("GET", "/v1/ingestion"),
  setDegradation: (rung: string) =>
    req<{ rung: string }>("POST", `/v1/admin/degrade?rung=${encodeURIComponent(rung)}`),
  health: () => req<any>("GET", "/v1/health"),
};
