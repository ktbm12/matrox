self.addEventListener('install', function(event) {
  self.skipWaiting();
  event.waitUntil(
    caches.open('matrox-pwa-v1').then(function(cache) {
      return cache.addAll([
        '/',
        '/static/css/output.css',
        '/static/images/pwa-icon.png'
      ]);
    })
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(clients.claim());
});

self.addEventListener('fetch', function(event) {
  // Simple network-first strategy to ensure dynamic content works
  if (event.request.method !== 'GET') return;
  
  event.respondWith(
    fetch(event.request)
      .then(function(response) {
        let responseClone = response.clone();
        caches.open('matrox-pwa-v1').then(function(cache) {
          cache.put(event.request, responseClone);
        });
        return response;
      })
      .catch(function() {
        return caches.match(event.request);
      })
  );
});
