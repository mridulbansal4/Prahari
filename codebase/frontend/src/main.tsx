import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import { ensureSession } from "./lib/session";
import "./design/global.css";

// Obtain the dev token before first paint so the page's own fetches are authorised. The user
// never sees this — there is no login surface any more.
ensureSession().catch(() => {
  /* Sections surface their own errors; a failed bootstrap must not blank the page. */
});

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);

// Service worker: PRODUCTION ONLY.
//
// The worker caches the app shell cache-first, which is correct for an offline-capable field
// PWA but actively harmful in development: every shell change came back as "the old UI is
// still there" until the worker was manually purged. In dev we do the opposite — tear down any
// worker and cache that a previous build registered, so a reload always shows current code.
if ("serviceWorker" in navigator) {
  if (import.meta.env.PROD) {
    window.addEventListener("load", () => {
      navigator.serviceWorker.register("/sw.js").catch(() => {
        /* offline support is progressive — failure never blocks the app */
      });
    });
  } else {
    navigator.serviceWorker
      .getRegistrations()
      .then((regs) => Promise.all(regs.map((r) => r.unregister())))
      .catch(() => {});
    caches
      ?.keys()
      .then((keys) => Promise.all(keys.map((k) => caches.delete(k))))
      .catch(() => {});
  }
}
