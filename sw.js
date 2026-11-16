// Odin's service worker. It lets a phone or computer install Odin as an app, and shows a short page when the
// school network can't be reached. It keeps NO student data: only this offline page and the app icons are stored
// on the device, and every request for Odin's data goes straight to the server, never to a cache.
const SHELL = "odin-shell-0.7.0-alpha";
const KEEP = ["offline.html", "icons/icon-192.png"];
self.addEventListener("install", e => { e.waitUntil(caches.open(SHELL).then(c => c.addAll(KEEP))); self.skipWaiting(); });
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== SHELL).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener("fetch", e => {
  if (e.request.mode !== "navigate") return;   // data, scripts and pictures: the network only
  e.respondWith(fetch(e.request).catch(() => caches.match("offline.html")));
});
