# Superseded multi-page UI

These files are the previous routed, role-gated console. They are **excluded from the build**
(see `tsconfig.json` → `exclude`) and nothing in `src/` imports them. They are kept only so the
prior work is recoverable.

Superseded by the single-page app when the login/auth system was removed and every feature was
collapsed onto one scrollable page:

| Was | Now |
|---|---|
| `pages/Investigation.tsx` | `sections/AskSection.tsx` |
| `pages/Modules.tsx` (Admin & Ingestion) | `sections/DocumentsSection.tsx` |
| `pages/Compliance.tsx` + `Modules.tsx` (Knowledge Evolution) | `sections/AlertsSection.tsx` |
| `components/Shell.tsx` | `sections/TopNav.tsx` |
| `lib/auth.tsx` + `pages/Login.tsx` (both deleted) | `lib/session.ts` — silent dev token, no UI |

Features present here that the single page does **not** currently surface: entity-resolution
adjudication (Living Asset Map), the work-order draft/approve flow (Execution Center),
Organizational Memory capture, Decision Memory & Replay, Decision Analytics, the audit log,
Field Mode, and the correction composer ("This is wrong"). Their backend endpoints are all
still live and untouched.
