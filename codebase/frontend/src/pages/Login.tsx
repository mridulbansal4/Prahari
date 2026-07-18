// Login (PRB §2.1) — federated SSO in production; a persona picker stub in the hackathon
// profile (ADR-P04). No local password field: identity is federated.
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../lib/auth";

const PERSONAS = [
  { id: "ravi", name: "Ravi", role: "Technician", note: "night-shift, the 02:40 story" },
  { id: "meera", name: "Meera", role: "Reliability", note: "the economic buyer / approver" },
  { id: "deepak", name: "Deepak", role: "Admin / OT Security", note: "the veto holder" },
  { id: "anil", name: "Anil", role: "Reliability", note: "34-year veteran, the corpus source" },
  { id: "compliance", name: "Compliance Officer", role: "Compliance", note: "EHS / audit" },
  { id: "auditor", name: "Auditor", role: "Auditor", note: "read-only audit access" },
];

export function Login() {
  const { login } = useAuth();
  const nav = useNavigate();
  const [busy, setBusy] = useState<string | null>(null);
  const [err, setErr] = useState<string | null>(null);

  async function pick(id: string) {
    setBusy(id);
    setErr(null);
    try {
      await login(id);
      nav("/investigate");
    } catch {
      setErr("Can't reach your organization's sign-in. Try again, or contact your admin.");
      setBusy(null);
    }
  }

  return (
    <div
      style={{
        minHeight: "100vh",
        display: "grid",
        placeItems: "center",
        background: "var(--canvas)",
      }}
    >
      <div className="col" style={{ width: 560, maxWidth: "90vw" }}>
        <div>
          <div className="t-display-md" style={{ letterSpacing: "0.02em" }}>
            SENTINEL
          </div>
          <div className="t-subtitle ink-muted">Industrial Decision Intelligence Operating System</div>
        </div>
        <div className="card">
          <div className="t-label" style={{ marginBottom: "var(--sp-md)" }}>
            Sign in with organization SSO
          </div>
          <div className="col" style={{ gap: "var(--sp-sm)" }}>
            {PERSONAS.map((p) => (
              <button
                key={p.id}
                className="btn btn-secondary between"
                style={{ justifyContent: "space-between", width: "100%" }}
                disabled={!!busy}
                onClick={() => pick(p.id)}
              >
                <span>
                  {busy === p.id ? "Signing in…" : `${p.name} — ${p.role}`}
                </span>
                <span className="t-metadata">{p.note}</span>
              </button>
            ))}
          </div>
          {err && (
            <div className="t-caption" style={{ color: "var(--critical)", marginTop: "var(--sp-md)" }}>
              {err}
            </div>
          )}
          <div className="t-metadata" style={{ marginTop: "var(--sp-lg)" }}>
            Demo profile: identity is a signed dev token (ADR-P04). Production federates to the
            customer IdP (OIDC).
          </div>
        </div>
      </div>
    </div>
  );
}
