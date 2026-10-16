(function () {
  'use strict';
  var YM_ID = 109391253;          // тот же счётчик, что и на основном сайте (axiiom.ru)
  var GA_ID = 'G-HFS4BDGTV4';     // тот же ресурс GA4, что и на основном сайте

  // --- Яндекс.Метрика: переиспользуем централизованный /metrika.js (в нём есть защита от дублей) ---
  var m = document.createElement('script');
  m.src = '/metrika.js?v=20260912';
  m.defer = true;
  document.head.appendChild(m);

  // --- GA4: загружаем gtag.js и конфигурируем ресурс ---
  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
  window.gtag('js', new Date());
  window.gtag('config', GA_ID, { page_path: location.pathname });
  var g = document.createElement('script');
  g.async = true;
  g.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
  document.head.appendChild(g);

  // --- SPA-трекинг: VitePress ходит по страницам через History API, а не полной загрузкой.
  // Хукаем pushState/replaceState/popstate и досылаем "виртуальные" хиты. ---
  var last = location.pathname + location.search;

  function track() {
    var key = location.pathname + location.search;
    if (key === last) return;            // не дублируем хиты (в т.ч. на хэш-якорях)
    last = key;
    try {
      if (typeof window.ym === 'function') {
        window.ym(YM_ID, 'hit', location.pathname + location.search + location.hash);
      }
    } catch (e) { /* no-op */ }
    try {
      window.gtag('event', 'page_view', {
        page_path: location.pathname,
        page_title: document.title
      });
    } catch (e) { /* no-op */ }
  }

  ['pushState', 'replaceState'].forEach(function (name) {
    var orig = history[name];
    if (typeof orig !== 'function') return;
    history[name] = function () {
      var r = orig.apply(this, arguments);
      setTimeout(track, 0);              // даём VitePress обновить title после перехода
      return r;
    };
  });
  window.addEventListener('popstate', track);
})();
