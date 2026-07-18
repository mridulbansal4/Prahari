// Prahari service worker (M12 / NFR-12) — makes Field Mode usable with zero network.
// App shell: cache-first. API GETs: network-first with a cache fallback so the last-known
// cached answers/graph slice render offline (CP-9 field mode), honestly labelled by the app.
const SHELL = "prahari-shell-v1";
const API = "prahari-api-v1";
const SHELL_ASSETS = ["/", "/index.html", "/manifest.webmanifest", "/icon.svg"];

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(SHELL).then((c) => c.addAll(SHELL_ASSETS)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => ![SHELL, API].includes(k)).map((k) => caches.delete(k))),
    ).then(() => self.clients.claim()),
  );
});

self.addEventListener("fetch", (event) => {
  const { request } = event;
  if (request.method !== "GET") return; // never cache writes (CP-3 stays online)
  const url = new URL(request.url);

  if (url.pathname.startsWith("/v1/")) {
    // API: network-first, fall back to cache when offline (last-known state).
    event.respondWith(
      fetch(request)
        .then((res) => {
          const copy = res.clone();
          caches.open(API).then((c) => c.put(request, copy));
          return res;
        })
        .catch(() => caches.match(request)),
    );
    return;
  }

  // App shell / static: cache-first, then network.
  event.respondWith(
    caches.match(request).then((cached) => cached || fetch(request).then((res) => {
      const copy = res.clone();
      caches.open(SHELL).then((c) => c.put(request, copy));
      return res;
    }).catch(() => caches.match("/index.html"))),
  );
});
