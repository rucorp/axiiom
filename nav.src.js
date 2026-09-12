(function(w, d) {
  'use strict';

  // Навигация AXIIOM — анти-дорвей + конверсия
  // - 30 отраслевых решений сгруппированы по 5 категориям (mega-меню)
  // - Все страницы в sitemap, в меню теперь все 30 (было 13) — улучшает перелинковку и SEO
  // - Добавлены лендинги категорий /industries/fintech/ и т.д.
  var TREE = [
    {
      name: 'Главная',
      path: '/',
      children: [
        { name: 'Услуги', path: '/#services' },
        { name: 'Кейсы', path: '/#cases' },
        { name: 'Процесс', path: '/#process' },
        { name: 'Контакты', path: '/#contact' }
      ]
    },
    {
      name: 'Решения',
      path: '/industries/',
      children: [
        { header: true, name: 'Fintech — 8 решений' },
        { name: 'KYC и онбординг', path: '/industries/kyc-onboarding.html' },
        { name: 'Мультивалютный кошелёк', path: '/industries/multi-currency-wallet.html' },
        { name: 'P2P-маркетплейс', path: '/industries/p2p-marketplace.html' },
        { name: 'Trading Engine', path: '/industries/trading-engine.html' },
        { name: 'Токенизация активов', path: '/industries/asset-tokenization.html' },
        { name: 'Investment CRM', path: '/industries/investment-crm.html' },
        { name: 'Real-time аналитика', path: '/industries/real-time-analytics.html' },
        { name: 'Краудфандинг', path: '/industries/kraudfanding.html' },
        { separator: true },
        { header: true, name: 'HoReCa & Retail — 4 решения' },
        { name: 'Автоматизация ресторанов', path: '/industries/avtomatizaciya-restoranov.html' },
        { name: 'Доставка еды', path: '/industries/dostavka-edy.html' },
        { name: 'Бронирование гостиниц', path: '/industries/bronirovanie-gostinits.html' },
        { name: 'Фитнес-приложения', path: '/industries/fitness-apps.html' },
        { separator: true },
        { header: true, name: 'B2B & Enterprise — 10 решений' },
        { name: 'CRM для медцентров', path: '/industries/crm-medcentry.html' },
        { name: 'CRM для недвижимости', path: '/industries/crm-nedvizhimost.html' },
        { name: 'ПО для стройкомпаний', path: '/industries/po-stroitelnye-kompanii.html' },
        { name: 'ERP для производства', path: '/industries/erp-proizvodstvo.html' },
        { name: 'Логистика и грузоперевозки', path: '/industries/sistemy-logistika.html' },
        { name: 'Управление цепочками', path: '/industries/upravlenie-cepochkami.html' },
        { name: 'ПО для юрфирм', path: '/industries/pravovie-firmu.html' },
        { name: 'ПО для автосервиса', path: '/industries/avtoservice.html' },
        { name: 'HR и подбор', path: '/industries/hr-podbor-personala.html' },
        { name: 'Сельское хозяйство', path: '/industries/selskokhozyaystvo.html' },
        { separator: true },
        { header: true, name: 'SaaS & Digital — 7 решений' },
        { name: 'SaaS для стартапов', path: '/industries/saas-startupy.html' },
        { name: 'Онлайн-обучение', path: '/industries/online-obuchenie.html' },
        { name: 'Платформа фриланса', path: '/industries/platforma-frilans.html' },
        { name: 'IoT умный дом', path: '/industries/iot-umnyy-dom.html' },
        { name: 'Маркетинг-аналитика', path: '/industries/marketing-analitika.html' },
        { name: 'Управление проектами', path: '/industries/upravlenie-proektami.html' },
        { name: 'Удалённая работа', path: '/industries/udalennaya-rabota.html' },
        { separator: true },
        { header: true, name: 'Security' },
        { name: 'Кибербезопасность', path: '/industries/kiberbezopasnost.html' },
        { separator: true },
        { name: 'Все 30 решений →', path: '/industries/' },
        { name: 'Калькулятор стоимости →', path: '/calculator/' }
      ]
    },
    {
      name: 'Демо',
      path: '/demo/app/',
      children: [
        { header: true, name: 'Все демо' },
        { name: 'Все демо AXIIOM', path: '/demo/app/' },
        { separator: true },
        { header: true, name: 'Финтех' },
        { name: 'Платежный шлюз', path: '/demo/app/payment-gateway/' },
        { name: 'Кредитный конвейер', path: '/demo/app/credit-conveyor/' },
        { name: 'Маркетплейс', path: '/demo/app/marketplace/' },
        { name: 'Платежная страница', path: '/demo/app/payment-page/' },
        { name: 'Финтех-конструктор', path: '/demo/app/fintech-constructor/' },
        { separator: true },
        { header: true, name: 'Лояльность' },
        { name: 'Программа лояльности', path: '/demo/app/loyalty-program/' },
        { name: 'Система лояльности', path: '/demo/app/loyalty-system/' },
        { separator: true },
        { header: true, name: 'Аналитика' },
        { name: 'Аналитическая панель', path: '/demo/app/analytics-dashboard/' },
        { name: 'Мониторинг инцидентов', path: '/demo/app/incident-monitoring/' },
        { name: 'Портфель проектов', path: '/demo/app/project-portfolio/' },
        { separator: true },
        { header: true, name: 'Сервисы' },
        { name: 'Чат-бот техподдержки', path: '/demo/app/chatbot-support/' },
        { name: 'Витрина в Telegram', path: '/demo/app/telegram-storefront/' },
        { name: 'Онбординг пользователей', path: '/demo/app/user-onboarding/' },
        { name: 'Платежный терминал', path: '/demo/app/payment-terminal/' }
      ]
    },
    {
      name: 'Портфолио',
      path: '/projects/',
      children: [
        { header: true, name: 'Избранные' },
        { name: 'PadelPro — SAAS для падел-клубов', path: '/projects/#padelpro' },
        { name: 'Каталог заведений', path: '/projects/#catalog' },
        { name: 'Grand Hotel — бронирование', path: '/projects/#booking' },
        { name: 'UniverID — экосистема вуза', path: '/projects/#univerid' },
        { name: 'LOVII — платформа лояльности', path: '/projects/#lovii' },
        { name: 'AMBAR — фудтех', path: '/projects/#ambar' },
        { separator: true },
        { name: 'Все проекты →', path: '/projects/' }
      ]
    },
    {
      name: 'Блог',
      path: '/blog/',
      children: [
        { name: 'Архитектура highload-систем', path: '/blog/highload-architecture/' },
        { name: 'PCI DSS Compliance', path: '/blog/pci-dss-compliance/' },
        { name: 'Тренды финтеха 2026', path: '/blog/fintech-trends-2026/' },
        { name: 'ROI платформы лояльности', path: '/blog/loyalty-program-roi/' },
        { name: '161-ФЗ: руководство для стартапов', path: '/blog/161-fz-guideline/' },
        { name: 'UX платёжных мобильных приложений', path: '/blog/mobile-payment-ux/' },
        { name: 'Платформа лояльности — необходимость', path: '/blog/loyalty-platform-not-option-necessity/' },
        { separator: true },
        { name: 'Все статьи →', path: '/blog/' }
      ]
    },
    {
      name: 'Инструменты',
      path: '/tools/',
      children: [
        { name: 'Счётчик символов', path: '/tools/char-counter/' },
        { name: 'Генератор паролей', path: '/tools/password-gen/' },
        { name: 'Транслитератор', path: '/tools/translit/' },
        { name: 'Base64', path: '/tools/base64/' },
        { name: 'URL Encode', path: '/tools/url-encode/' },
        { name: 'Lorem Ipsum', path: '/tools/lorem-ipsum/' },
        { name: 'Color Picker', path: '/tools/color-picker/' },
        { name: 'Конвертер валют', path: '/tools/currency/' },
        { name: 'Калькулятор дат', path: '/tools/date-calc/' },
        { name: 'Конвертер единиц', path: '/tools/unit-converter/' },
        { name: 'SEO Сниппет', path: '/tools/snippet-gen/' },
        { name: 'Чек-листы', path: '/tools/checklist/' },
        { separator: true },
        { name: 'Все инструменты →', path: '/tools/' }
      ]
    },
    { name: 'Калькулятор', path: '/calculator/' },
    { name: 'Контакты', path: '/#contact' },
    { name: 'Политика конфиденциальности', path: '/privacy/', footerOnly: true },
    { name: 'Пользовательское соглашение', path: '/terms/', footerOnly: true },
    { name: 'Документация', path: '/docs/', footerOnly: true }
  ];

  function $(id) { return d.getElementById(id); }

  function el(tag, attrs, children) {
    var e = d.createElement(tag);
    if (attrs) for (var k in attrs) e.setAttribute(k, attrs[k]);
    if (children) for (var i = 0; i < children.length; i++) e.appendChild(children[i]);
    return e;
  }

  function tx(text) { return d.createTextNode(text); }

  var Nav = {
    opts: {},
    currentPath: '',

    init: function(options) {
      this.opts = { cta: true, breadcrumbs: true };
      if (options) for (var k in options) this.opts[k] = options[k];

      this.currentPath = this._normalizePath(w.location.pathname);

      this._renderDesktop();
      this._renderMobile();
      this._renderFooter();
      if (this.opts.breadcrumbs) this._renderBreadcrumbs();
      this._toggleCta();
      this._initEvents();
    },

    _normalizePath: function(p) {
      if (p.indexOf('/index.html') > 0) p = p.replace('/index.html', '');
      if (p.length > 1 && p.charAt(p.length - 1) === '/') p = p.slice(0, -1);
      if (p === '') p = '/';
      return p;
    },

    _pathMatch: function(nodePath, urlPath) {
      var a = nodePath;
      if (a.length > 1 && a.charAt(a.length - 1) === '/') a = a.slice(0, -1);
      var b = urlPath;
      if (b.length > 1 && b.charAt(b.length - 1) === '/') b = b.slice(0, -1);
      return a === b;
    },

    _activeSection: function() {
      var path = this.currentPath;
      if (path === '/') return null;

      var candidates = [];
      for (var i = 0; i < TREE.length; i++) {
        var n = TREE[i];
        if (n.footerOnly) continue;
        var base = n.path;
        if (base.length > 1 && base.charAt(base.length - 1) === '/') base = base.slice(0, -1);
        if (path === base || path.indexOf(base + '/') === 0 || path.indexOf(base + '.') === 0) {
          candidates.push({ node: n, baseLen: base.length });
        }
      }
      candidates.sort(function(a, b) { return b.baseLen - a.baseLen; });
      return candidates.length > 0 ? candidates[0].node : null;
    },

    _findNode: function(path) {
      function search(nodes, parents) {
        for (var i = 0; i < nodes.length; i++) {
          var n = nodes[i];
          if (n.separator || n.header) continue;
          if (this._pathMatch(n.path, path)) return { node: n, parents: parents };
          if (n.children) {
            var result = search.call(this, n.children, parents.concat([n]));
            if (result) return result;
          }
        }
        return null;
      }
      return search.call(this, TREE, []);
    },

    _hasHash: function(p) {
      return p.indexOf('#') !== -1;
    },

    _renderDesktop: function() {
      var container = $('desktopNav');
      if (!container) return;

      var active = this._activeSection();

      for (var i = 0; i < TREE.length; i++) {
        var n = TREE[i];
        if (n.footerOnly) continue;
        if (n.path.indexOf('#') !== -1) continue;

        var link = el('a', { href: n.path }, [tx(n.name)]);
        if (active && n.path === active.path) {
          link.className = 'nav-active';
          link.setAttribute('aria-current', 'page');
        }

        var li = el('li', {}, [link]);

        if (n.children && n.children.length > 0) {
          li.className = 'nav-has-dropdown';
          var ddClass = n.children.length > 15 ? 'nav-dropdown mega' : 'nav-dropdown';
          var dd = el('ul', { 'class': ddClass });
          for (var j = 0; j < n.children.length; j++) {
            var ch = n.children[j];
            if (ch.separator) {
              dd.appendChild(el('li', { 'class': 'nav-dropdown-sep' }));
            } else if (ch.header) {
              dd.appendChild(el('li', { 'class': 'nav-dropdown-hdr' }, [el('span', {}, [tx(ch.name)])]));
            } else {
              var cl = el('a', { href: ch.path }, [tx(ch.name)]);
              dd.appendChild(el('li', {}, [cl]));
            }
          }
          li.appendChild(dd);
        }

        container.appendChild(li);
      }
    },

    _renderMobile: function() {
      var container = $('mobileNav');
      if (!container) return;
      var self = this;

      function renderNode(node) {
        var link = el('a', { href: node.path }, [tx(node.name)]);
        var match = self._activeSection();
        if (match && node.path === match.path) {
          link.className = 'nav-active';
          link.setAttribute('aria-current', 'page');
        }
        if (!match && self._pathMatch(node.path, self.currentPath)) {
          link.className = 'nav-active';
          link.setAttribute('aria-current', 'page');
        }

        var li = el('li', {}, [link]);

        if (node.children && node.children.length > 0) {
          li.className = 'nav-has-children';
          var btn = el('button', { 'class': 'nav-expand', 'aria-label': '\u0420\u0430\u0437\u0432\u0435\u0440\u043D\u0443\u0442\u044C' }, [tx('+')]);
          li.appendChild(btn);
          var sub = el('ul', { 'class': 'nav-sub' });
          for (var i = 0; i < node.children.length; i++) {
            var ch2 = node.children[i];
            if (ch2.separator) {
              sub.appendChild(el('li', { 'class': 'nav-sub-sep' }));
            } else if (ch2.header) {
              sub.appendChild(el('li', { 'class': 'nav-sub-hdr' }, [el('span', {}, [tx(ch2.name)])]));
            } else {
              sub.appendChild(renderNode(ch2));
            }
          }
          li.appendChild(sub);
        }

        return li;
      }

      for (var i = 0; i < TREE.length; i++) {
        if (TREE[i].footerOnly) continue;
        container.appendChild(renderNode(TREE[i]));
      }
    },

    _renderBreadcrumbs: function() {
      var container = $('breadcrumbs');
      if (!container) return;

      var html = '<div class=\"container\"><ol class=\"breadcrumbs-list\">';
      html += this._bcItem('\u0413\u043B\u0430\u0432\u043D\u0430\u044F', '/', 1);

      var match = this._findNode(this.currentPath);
      if (match) {
        var pos = 2;
        for (var i = 0; i < match.parents.length; i++) {
          html += this._bcItem(match.parents[i].name, match.parents[i].path, pos++);
        }
        html += this._bcItemCurrent(match.node.name, pos);
      } else {
        var pretty = this.currentPath.replace(/-/g, ' ').replace(/\//g, ' ').trim();
        if (pretty && this.currentPath !== '/') {
          html += this._bcItemCurrent(pretty, 2);
        } else {
          html += this._bcItemCurrent('\u0421\u0442\u0440\u0430\u043D\u0438\u0446\u0430', 2);
        }
      }

      html += '</ol></div>';
      container.innerHTML = html;
    },

    _bcItem: function(name, href, pos) {
      return '<li>' +
        '<a href=\"' + href + '\"><span>' + name + '</span></a>' +
        '</li>';
    },

    _bcItemCurrent: function(name, pos) {
      return '<li class=\"current\"><span>' + name + '</span>' +
        '</li>';
    },

    _renderFooter: function() {
      var container = $('footerCopy');
      if (!container) return;
      var cfg = w.AXIIOM_CONFIG || {};
      var c = cfg.company || {};
      var mainLinks = [];
      var legalLinks = [];
      for (var i = 0; i < TREE.length; i++) {
        var n = TREE[i];
        if (n.footerOnly) { legalLinks.push(n); }
        else if (!this._hasHash(n.path)) { mainLinks.push(n); }
      }

      var html = '<p class=\"copy\">';
      for (var i = 0; i < mainLinks.length; i++) {
        if (i > 0) html += ' \u00B7 ';
        var name = mainLinks[i].path === '/' ? (c.shortName || '\u0410\u041A\u0421\u0418\u041E\u041C\u0410') : mainLinks[i].name;
        html += '<a href=\"' + mainLinks[i].path + '\" class=\"footer-link\">' + name + '</a>';
      }
      html += '</p>';

      if (legalLinks.length > 0) {
        html += '<p class=\"copy\" style=\"font-size:.7rem;margin-top:8px;border:none;padding-top:0;\">';
        for (var i = 0; i < legalLinks.length; i++) {
          if (i > 0) html += ' \u00B7 ';
          html += '<a href=\"' + legalLinks[i].path + '\" class=\"footer-link\">' + legalLinks[i].name + '</a>';
        }
        html += '</p>';
      }

      var year = new Date().getFullYear();
      var start = c.copyrightStart || 2024;
      html += '<p class=\"copy\" style=\"font-size:.65rem;margin-top:8px;border:none;padding-top:0;text-transform:none;letter-spacing:0;\">' +
        '\u00A9 ' + start + '\u2013' + year + ' ' + (c.name || 'AXIIOM') + ' (' + (c.nameRu || '\u041E\u041E\u041E \u0410\u043A\u0441\u0438\u043E\u043C\u0430') + '). \u0412\u0441\u0435 \u043F\u0440\u0430\u0432\u0430 \u0437\u0430\u0449\u0438\u0449\u0435\u043D\u044B.' +
      '</p>';

      container.innerHTML = html;
    },

    _toggleCta: function() {
      var cta = $('ctaBtn');
      if (!cta && this.opts.cta) {
        var wrap = d.querySelector('.nav-actions');
        if (wrap) {
          cta = el('a', { href: '/#contact', 'class': 'btn btn-nav', id: 'ctaBtn' }, [tx('\u041E\u0431\u0441\u0443\u0434\u0438\u0442\u044C \u043F\u0440\u043E\u0435\u043A\u0442')]);
          wrap.insertBefore(cta, wrap.firstChild);
        }
      }
      if (cta) cta.style.display = this.opts.cta ? '' : 'none';
    },

    _initEvents: function() {
      var overlay = $('navOverlay');
      var toggle = $('navToggle');

      if (overlay) {
        overlay.addEventListener('click', function(e) {
          if (e.target === overlay) {
            overlay.classList.remove('open');
            if (toggle) toggle.classList.remove('active');
            d.body.style.overflow = '';
          }
        });

        overlay.querySelectorAll('a').forEach(function(link) {
          link.addEventListener('click', function(e) {
            var li = this.parentNode;
            if (li && li.classList.contains('nav-has-children')) {
              e.preventDefault();
              var btn = li.querySelector('.nav-expand');
              var sub = li.querySelector('.nav-sub');
              var isExpanding = !li.classList.contains('nav-expanded');
              if (sub) {
                if (isExpanding) {
                  var prev = sub.style.maxHeight;
                  sub.style.maxHeight = 'none';
                  var h = sub.scrollHeight;
                  sub.style.maxHeight = prev || '0';
                  sub.offsetHeight;
                  sub.style.maxHeight = h + 'px';
                } else {
                  sub.style.maxHeight = '0';
                }
              }
              li.classList.toggle('nav-expanded');
              if (btn) btn.textContent = isExpanding ? '\u2212' : '+';
              return;
            }
            overlay.classList.remove('open');
            if (toggle) toggle.classList.remove('active');
            d.body.style.overflow = '';
          });
        });

        overlay.querySelectorAll('.nav-expand').forEach(function(btn) {
          btn.addEventListener('click', function(e) {
            e.stopPropagation();
            var p = btn.parentNode;
            var sub = p.querySelector('.nav-sub');
            var isExpanding = !p.classList.contains('nav-expanded');
            if (sub) {
              if (isExpanding) {
                var prev = sub.style.maxHeight;
                sub.style.maxHeight = 'none';
                var h = sub.scrollHeight;
                sub.style.maxHeight = prev || '0';
                sub.offsetHeight;
                sub.style.maxHeight = h + 'px';
              } else {
                sub.style.maxHeight = '0';
              }
            }
            p.classList.toggle('nav-expanded');
            btn.textContent = isExpanding ? '\u2212' : '+';
          });
        });
      }

      var header = $('header');
      if (header) {
        w.addEventListener('scroll', function() {
          header.classList.toggle('scrolled', w.scrollY > 40);
        }, { passive: true });
      }

      // Sticky CTA logic for industries
      var sticky = d.getElementById('stickyCta');
      if (sticky) {
        var showAt = 600;
        w.addEventListener('scroll', function() {
          if (w.scrollY > showAt) sticky.classList.add('visible');
          else sticky.classList.remove('visible');
        }, { passive: true });
      }
    },

    _initReveal: function() {
      // Global safety net for .reveal elements: covers pages without an inline
      // observer and nodes injected later via JS. Idempotent — pages with their
      // own IntersectionObserver keep working as before.
      if (!('IntersectionObserver' in w)) {
        var all = d.querySelectorAll('.reveal');
        for (var j = 0; j < all.length; j++) all[j].classList.add('visible');
        return;
      }
      var io = new IntersectionObserver(function(entries) {
        for (var i = 0; i < entries.length; i++) {
          if (entries[i].isIntersecting) {
            entries[i].target.classList.add('visible');
            io.unobserve(entries[i].target);
          }
        }
      }, { threshold: 0.15 });
      function watch(root) {
        var nodes = root.querySelectorAll('.reveal:not(.visible)');
        for (var i = 0; i < nodes.length; i++) io.observe(nodes[i]);
      }
      watch(d);
      if ('MutationObserver' in w) {
        var mo = new MutationObserver(function(muts) {
          for (var i = 0; i < muts.length; i++) {
            var added = muts[i].addedNodes;
            for (var k = 0; k < added.length; k++) {
              var n = added[k];
              if (n.nodeType !== 1) continue;
              if (n.classList && n.classList.contains('reveal') && !n.classList.contains('visible')) io.observe(n);
              watch(n);
            }
          }
        });
        mo.observe(d.body || d.documentElement, { childList: true, subtree: true });
      }
    }
  };

  w.Nav = Nav;
})(window, document);
