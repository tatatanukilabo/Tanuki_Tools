const CACHE_NAME = "stlite-cache-v1";

const urlsToCache = [
  "/index.html",
  "/Home.py",
  "/manifest.json",
  "/pages/Page1.py",
  "/pages/Page2.py",
  "/pages/Page3.py",
  "/pages/99_About.py",
  "/assets/icons/icon.png",
  "/assets/icons/icon-192.png",
  "/assets/icons/icon-512.png",
  "/assets/icons/check.png",
  "https://cdn.jsdelivr.net/npm/@stlite/mountable@0.58.3/build/stlite.js",
  "https://cdn.jsdelivr.net/npm/@stlite/mountable@0.58.3/build/stlite.css"
];

self.addEventListener("install", event => {
  event.waitUntil(
    (async () => {
      const cache = await caches.open(CACHE_NAME);
      await cache.addAll(urlsToCache);

      // 🔹 list.json をキャッシュ
      try {
        const res = await fetch("/assets/data/list.json");
        const listJsonText = await res.text();
        await cache.put("/assets/data/list.json", new Response(listJsonText));

        // 🔹 画像ファイルをキャッシュ
        const list = JSON.parse(listJsonText);
        const imagePaths = Object.keys(list).map(
          filename => `/assets/data/${filename}`
        );
        await cache.addAll(imagePaths);
      } catch (err) {
        console.warn("⚠️ list.json or image fetch failed:", err);
      }
    })()
  );
});

self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys.map(key => {
          if (key !== CACHE_NAME) return caches.delete(key);
        })
      )
    )
  );
  return self.clients.claim();
});

self.addEventListener("fetch", event => {
  event.respondWith(
    fetch(event.request).catch(() => caches.match(event.request))
  );
});