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

  // Сквозной CTA: помогает читателю документации перейти от тестовой интеграции
  // к обсуждению разработки с AXIIOM. Встраивается после гидратации VitePress.
  function ensureCtaStyles() {
    if (document.getElementById('axiiom-mock-cta-style')) return;
    var style = document.createElement('style');
    style.id = 'axiiom-mock-cta-style';
    style.textContent = [
      '.axiiom-mock-cta{margin:2.5rem 0 1rem;padding:1.25rem 1.5rem;border:1px solid var(--vp-c-divider,#d8d8d8);border-radius:12px;background:var(--vp-c-bg-soft,#f6f6f7);color:var(--vp-c-text-1,#333)}',
      '.axiiom-mock-cta h2{margin:0 0 .5rem;font-size:1.2rem;line-height:1.4}',
      '.axiiom-mock-cta p{margin:.4rem 0 1rem;color:var(--vp-c-text-2,#555)}',
      '.axiiom-mock-cta a{display:inline-block;padding:.55rem .9rem;border-radius:8px;background:var(--vp-c-brand-1,#3451b2);color:#fff;text-decoration:none;font-weight:600}',
      '.axiiom-mock-cta a:hover{opacity:.88}',
      '@media(prefers-reduced-motion:reduce){.axiiom-mock-cta a{transition:none}}'
    ].join('');
    document.head.appendChild(style);
  }

  function addBusinessCta() {
    var content = document.querySelector('#VPContent .vp-doc');
    if (!content || content.querySelector('.axiiom-mock-cta')) return;
    ensureCtaStyles();

    var section = document.createElement('aside');
    section.className = 'axiiom-mock-cta';
    section.setAttribute('aria-label', 'Разработка финтех-продуктов AXIIOM');

    var heading = document.createElement('h2');
    heading.textContent = 'Переход от теста к запуску';
    var description = document.createElement('p');
    description.textContent = 'Нужна помощь с платёжной интеграцией, онлайн-кассой или финтех-продуктом? Команда AXIIOM поможет обсудить архитектуру и план разработки.';
    var link = document.createElement('a');
    link.href = 'https://axiiom.ru/#contact';
    link.textContent = 'Обсудить проект с AXIIOM';
    link.addEventListener('click', function () {
      try { if (typeof window.ym === 'function') window.ym(YM_ID, 'reachGoal', 'mock_services_cta'); } catch (e) { /* no-op */ }
      try { window.gtag('event', 'mock_services_cta', { page_path: location.pathname }); } catch (e) { /* no-op */ }
    });

    section.appendChild(heading);
    section.appendChild(description);
    section.appendChild(link);
    content.appendChild(section);
  }

  if (typeof MutationObserver === 'function' && document.documentElement) {
    var ctaObserver = new MutationObserver(addBusinessCta);
    ctaObserver.observe(document.documentElement, { childList: true, subtree: true });
  }
  addBusinessCta();
})();
