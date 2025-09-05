const CACHE_NAME = "stlite-cache-v1";
const urlsToCache = [
  "/index.html",
  "/Home.py",
  "/manifest.json",
  "/pages/Page1.py",
  "/assets/icons/icon.png",
  "/assets/icons/icon-192.png",
  "/assets/icons/icon-512.png",
  "/assets/icons/check.png",
  "https://cdn.jsdelivr.net/npm/@stlite/mountable@0.58.3/build/stlite.js",
  "https://cdn.jsdelivr.net/npm/@stlite/mountable@0.58.3/build/stlite.css"
];

self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(urlsToCache))
  );
});

self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.map(key => {
        if (key !== CACHE_NAME) return caches.delete(key);
      }))
    )
  );
  return self.clients.claim();
});

self.addEventListener("fetch", event => {
  event.respondWith(
    fetch(event.request).catch(() => caches.match(event.request))
  );
});



