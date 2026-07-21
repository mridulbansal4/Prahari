// Session bootstrap — replaces the removed login/auth UI.
//
// There is no sign-in surface any more: the app lands straight on the page. The backend still
// authenticates every /v1 call, so on first load we silently obtain a dev token (ADR-P04) and
// cache it. Nothing is asked of the user and no gate is rendered.
//
// The principal is the admin persona because it is the only role whose RBAC matrix row grants
// access to every module the single page touches — investigations (M1), compliance (M6),
// knowledge health (M4) and ingestion (M11, admin-only). See backend app/auth/rbac.py.
import { api, getToken, setToken } from "./api";

const DEMO_PRINCIPAL = "deepak";

let bootstrap: Promise<void> | null = null;

/** Idempotent: concurrent callers share one in-flight login. */
export function ensureSession(): Promise<void> {
  if (!bootstrap) {
    bootstrap = (async () => {
      if (getToken()) {
        try {
          const me = await api.me();
          // A *valid* token is not enough — it must also be the right principal. A token left
          // over from the old login screen (say, the technician persona) authenticates fine but
          // lacks module access, which would 403 parts of the page with no way for the user to
          // recover now that the sign-in UI is gone.
          if (me.subject === DEMO_PRINCIPAL) return;
        } catch {
          /* expired or rejected — fall through and re-issue */
        }
        setToken(null);
      }
      const res = await api.login(DEMO_PRINCIPAL);
      setToken(res.token);
    })().catch((err) => {
      bootstrap = null; // let a later call retry rather than caching the failure
      throw err;
    });
  }
  return bootstrap;
}
