/* AndyTV Plus - Service Worker PWA */
const CACHE_NAME = 'andytv-plus-v2';
const ASSETS_TO_CACHE = [
  './',
  './index.html',
  './manifest.json',
  './icon.svg',
  './hls.min.js',
  './channels.js',
  './epg.js',
  './channels.json'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS_TO_CACHE);
    }).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))
      );
    }).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);

  // No interceptar streams de video ni llamadas dinámicas externas
  if (url.pathname.endsWith('.m3u8') || url.pathname.endsWith('.ts') ||
      url.hostname.includes('youtube.com') || url.hostname.includes('githubusercontent.com') ||
      url.hostname.includes('workers.dev') || url.hostname.includes('lambda-url') ||
      url.hostname.includes('mdstrm.com') || url.hostname.includes('vodgc.net') ||
      url.hostname !== self.location.hostname) {
    return;
  }

  // Network-First: intentar siempre red para tener la última versión y usar caché si no hay conexión
  event.respondWith(
    fetch(event.request)
      .then((networkResponse) => {
        if (networkResponse && networkResponse.status === 200) {
          const cloned = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(event.request, cloned));
        }
        return networkResponse;
      })
      .catch(() => caches.match(event.request))
  );
});
