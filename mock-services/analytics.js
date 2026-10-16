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

  // Сквозной CTA: компактная карточка внизу левого сайдбара документации.
  // ВАЖНО про клик (проверено на живом сайте 2026-10-17): роутер VitePress
  // вешает click-хендлер на window В CAPTURE-ФАЗЕ ({capture:!0}) и перехватывает
  // same-origin ссылки ДО любого обработчика на самой ссылке — preventDefault +
  // stopPropagation + location.assign в target-фазе не спасают, SPA всё равно
  // уводит на /mock-services/#contact. Обход — в самом коде роутера: он пропускает
  // ссылки с атрибутом target (c.hasAttribute("target") → return). Ставим
  // target="_top" (в обычной странице это тот же таб) — роутер игнорирует клик,
  // и браузер делает нативный переход на главную к блоку контактов. Работает
  // даже без JS-обработчика; обработчик оставлен только для целей аналитики.
  var CTA_URL = 'https://axiiom.ru/#contact';

  function ensureCtaStyles() {
    if (document.getElementById('axiiom-mock-cta-style')) return;
    var style = document.createElement('style');
    style.id = 'axiiom-mock-cta-style';
    style.textContent = [
      '.axiiom-mock-cta{margin:1.5rem 1rem 2rem;padding:1rem 1.1rem;border:1px solid var(--vp-c-divider,#d8d8d8);border-radius:10px;background:var(--vp-c-bg-soft,#f6f6f7)}',
      '.axiiom-mock-cta-title{margin:0 0 .6rem;font-size:.85rem;line-height:1.45;color:var(--vp-c-text-2,#555);font-weight:600}',
      '.axiiom-mock-cta a{display:block;text-align:center;padding:.5rem .75rem;border-radius:8px;background:var(--vp-c-brand-1,#3451b2);color:#fff;text-decoration:none;font-weight:600;font-size:.9rem}',
      '.axiiom-mock-cta a:hover{opacity:.88}'
    ].join('');
    document.head.appendChild(style);
  }

  function addBusinessCta() {
    var sidebarNav = document.querySelector('.VPSidebar nav.nav') || document.querySelector('.VPSidebar');
    // дедуп по всему документу: карточка могла остаться в .VPSidebar вне nav.nav
    if (!sidebarNav || document.querySelector('.axiiom-mock-cta')) return;
    ensureCtaStyles();

    var section = document.createElement('aside');
    section.className = 'axiiom-mock-cta';
    section.setAttribute('aria-label', 'Разработка финтех-продуктов AXIIOM');

    var title = document.createElement('p');
    title.className = 'axiiom-mock-cta-title';
    title.textContent = 'Нужна платёжная интеграция или онлайн-касса?';

    var link = document.createElement('a');
    link.href = CTA_URL;
    // target="_top" — ключ фикса: роутер VitePress на capture-фазе пропускает
    // любые ссылки с атрибутом target, и переход делает сам браузер нативно.
    link.setAttribute('target', '_top');
    link.textContent = 'Обсудить проект с AXIIOM';
    link.addEventListener('click', function () {
      // Только аналитика: никакой ручной навигации — её делает браузер.
      try { if (typeof window.ym === 'function') window.ym(YM_ID, 'reachGoal', 'mock_services_cta'); } catch (err) { /* no-op */ }
      try { window.gtag('event', 'mock_services_cta', { page_path: location.pathname }); } catch (err) { /* no-op */ }
    });

    section.appendChild(title);
    section.appendChild(link);
    sidebarNav.appendChild(section);
  }

  if (typeof MutationObserver === 'function' && document.documentElement) {
    var ctaObserver = new MutationObserver(addBusinessCta);
    ctaObserver.observe(document.documentElement, { childList: true, subtree: true });
  }
  addBusinessCta();
})();
