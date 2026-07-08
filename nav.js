(function(w, d) {
  'use strict';

  var TREE = [
    {
      name: 'Главная',
      path: '/',
      children: [
        { name: 'Услуги', path: '/#services' },
        { name: 'Проблемы', path: '/#problems' },
        { name: 'Кейсы', path: '/#cases' },
        { name: 'Процесс', path: '/#process' },
        { name: 'Технологии', path: '/#stack' },
        { name: 'Интеграции', path: '/#integrations' },
        { name: 'Демо', path: '/#demos' },
        { name: 'FAQ', path: '/#faq' }
      ]
    },
    {
      name: 'Решения',
      path: '/industries/',
      children: [
        { name: 'Автоматизация ресторанов', path: '/industries/avtomatizaciya-restoranov.html' },
        { name: 'ПО для строительных компаний', path: '/industries/po-stroitelnye-kompanii.html' },
        { name: 'CRM для медицинских центров', path: '/industries/crm-medcentry.html' },
        { name: 'Системы для логистики и грузоперевозок', path: '/industries/sistemy-logistika.html' },
        { name: 'SaaS для стартапов', path: '/industries/saas-startupy.html' },
        { name: 'ERP для производства', path: '/industries/erp-proizvodstvo.html' },
        { name: 'Системы учета для сельского хозяйства', path: '/industries/selskokhozyaystvo.html' },
        { name: 'Мобильные приложения для фитнеса', path: '/industries/fitness-apps.html' },
        { name: 'Платформы для онлайн-обучения', path: '/industries/online-obuchenie.html' },
        { name: 'Системы бронирования для гостиниц', path: '/industries/bronirovanie-gostinits.html' },
        { name: 'CRM для недвижимости', path: '/industries/crm-nedvizhimost.html' },
        { name: 'Инструменты для удаленной работы', path: '/industries/udalennaya-rabota.html' },
        { name: 'Аналитика для маркетинга', path: '/industries/marketing-analitika.html' },
        { name: 'Кибербезопасность для малого бизнеса', path: '/industries/kiberbezopasnost.html' },
        { name: 'Системы управления проектами', path: '/industries/upravlenie-proektami.html' },
        { name: 'Платформы для фриланса', path: '/industries/platforma-frilans.html' },
        { name: 'IoT для умного дома', path: '/industries/iot-umnyy-dom.html' },
        { name: 'Платформы для краудфандинга', path: '/industries/kraudfanding.html' },
        { name: 'Системы управления цепочками поставок', path: '/industries/upravlenie-cepochkami.html' },
        { name: 'ПО для юридических фирм', path: '/industries/pravovie-firmu.html' },
        { name: 'ПО для автосервиса', path: '/industries/avtoservice.html' },
        { name: 'Платформы для доставки еды', path: '/industries/dostavka-edy.html' },
        { name: 'HR для подбора персонала', path: '/industries/hr-podbor-personala.html' }
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
        { name: 'Чек-листы', path: '/tools/checklist/' }
      ]
    },
    {
      name: 'Документация',
      path: '/docs/',
      children: [
        { header: true, name: 'SRS / Техническая документация' },
        { name: 'SRS v2 — Спецификация', path: '/docs/srs-v2/' },
        { name: 'Аудит системы (AS IS)', path: '/docs/audit-as-is/' },
        { name: 'Бизнес-модель', path: '/docs/business-model/' },
        { name: 'Оценка сроков', path: '/docs/estimation/' },
        { name: 'Карта фич', path: '/docs/feature-map/' },
        { name: 'OTP через мессенджеры', path: '/docs/otp-via-messengers/' },
        { separator: true },
        { header: true, name: 'Статьи' },
        { name: 'Архитектура highload-систем', path: '/blog/highload-architecture/' },
        { name: 'PCI DSS Compliance', path: '/blog/pci-dss-compliance/' },
        { name: 'Тренды финтеха 2026', path: '/blog/fintech-trends-2026/' },
        { name: 'ROI платформы лояльности', path: '/blog/loyalty-program-roi/' },
        { name: '161-ФЗ: руководство для стартапов', path: '/blog/161-fz-guideline/' },
        { name: 'UX платёжных мобильных приложений', path: '/blog/mobile-payment-ux/' },
        { name: 'Платформа лояльности — необходимость', path: '/blog/loyalty-platform-not-option-necessity/' },
        { separator: true },
        { header: true, name: 'Проектная документация' },
        { name: 'Платформа «Витрина»', path: '/docs/vitrina/' },
        { name: 'AMBAR — Фудтех', path: '/docs/ambar-proposal/' },
        { name: 'ИТ-Архитектура (шаблон)', path: '/docs/it-architecture-template/' },
        { name: 'UniverID — концепция', path: '/docs/univerid-concept/' },
        { separator: true },
        { header: true, name: 'Юридическая документация' },
        { name: 'Юр. структура финтех-платформы', path: '/docs/yur-struktura-platformy/' },
        { separator: true },
        { header: true, name: 'Референсы' },
        { name: 'API супермаркетов', path: '/docs/store-apis-research/' },
        { name: 'Все документы', path: '/docs/' },
      ]
    },
    { name: 'Калькулятор', path: '/calculator/' },
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
        { name: 'Lovii — веб-приложение', path: 'https://app.lovii.ru/' },
        { name: 'Lovii — B2B-портал', path: 'https://b2b.lovii.ru/' },
        { name: 'Lovii — Админ-панель', path: 'https://admin.lovii.ru/' },
        { name: 'Lovii — мобильная', path: 'https://lovii.mobiap.com/mobile.html' },
        { separator: true },
        { header: true, name: 'Аналитика и мониторинг' },
        { name: 'Аналитическая панель', path: '/demo/app/analytics-dashboard/' },
        { name: 'Мониторинг инцидентов', path: '/demo/app/incident-monitoring/' },
        { name: 'Карта функциональных требований', path: 'https://bestdeejay-design.github.io/srs-docs/visualizations/07-force-graph.html' },
        { name: 'Портфель проектов', path: '/demo/app/project-portfolio/' },
        { separator: true },
        { header: true, name: 'Сервисы' },
        { name: 'Чат-бот техподдержки', path: '/demo/app/chatbot-support/' },
        { name: 'Витрина в Telegram', path: '/demo/app/telegram-storefront/' },
        { name: 'Онбординг пользователей', path: '/demo/app/user-onboarding/' },
        { name: 'Платежный терминал', path: '/demo/app/payment-terminal/' },
        { separator: true },
        { header: true, name: 'Проекты' },
        { name: 'PadelPro', path: 'https://bestdeejay-design.github.io/padl/' },
        { name: 'Каталог заведений', path: 'https://bestdeejay-design.github.io/catalog/' },
        { name: 'Grand Hotel', path: 'https://bestdeejay-design.github.io/booking/' },
        { name: 'UniverID', path: 'https://univerid.ru/' },
        { name: 'University Portal', path: '/demo/app/demo-template/' },
        { name: 'Foodie', path: 'https://bestdeejay-design.github.io/foodie/' },
        { name: 'eSIM Travel', path: 'https://bestdeejay-design.github.io/mvno/' },
        { name: 'AXIIOM Logistics', path: 'https://bestdeejay-design.github.io/logistics/' },
        { name: 'HR Motivation', path: 'https://bestdeejay-design.github.io/hrmodule/' },
        { name: 'Мобильная касса', path: 'https://bestdeejay-design.github.io/cashier/' },
        { name: 'Primary — Премиум такси', path: 'https://bestdeejay-design.github.io/primary/' },
        { name: 'Alfred', path: 'https://bestdeejay-design.github.io/alfred/' },
        { name: 'Qbik', path: 'https://bestdeejay-design.github.io/qbik/' },
        { name: 'Код Доступа', path: 'https://bestdeejay-design.github.io/kodstudy/' },
        { name: 'DAJET', path: 'https://dajet.ru/' },
        { name: 'Hype', path: 'https://hype-marketplace-1.web.app/' },
        { name: 'AMBAR', path: 'https://bestdeejay-design.github.io/ambar/' },
        { name: 'Мини-игры', path: 'https://bestdeejay-design.github.io/minigames/' }
      ]
    },
    { name: 'Контакты', path: '/#contact' },
    { name: 'Политика конфиденциальности', path: '/privacy/', footerOnly: true },
    { name: 'Пользовательское соглашение', path: '/terms/', footerOnly: true }
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
        if (active && n.path === active.path) link.className = 'nav-active';

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
        if (match && node.path === match.path) link.className = 'nav-active';
        if (!match && self._pathMatch(node.path, self.currentPath)) link.className = 'nav-active';

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

      var html = '<div class="container"><ol itemscope itemtype="https://schema.org/BreadcrumbList">';
      html += this._bcItem('\u0413\u043B\u0430\u0432\u043D\u0430\u044F', '/', 1);

      var match = this._findNode(this.currentPath);
      if (match) {
        var pos = 2;
        for (var i = 0; i < match.parents.length; i++) {
          html += this._bcItem(match.parents[i].name, match.parents[i].path, pos++);
        }
        html += this._bcItemCurrent(match.node.name, pos);
      } else {
        html += this._bcItemCurrent('\u0421\u0442\u0440\u0430\u043D\u0438\u0446\u0430', 2);
      }

      html += '</ol></div>';
      container.innerHTML = html;
    },

    _bcItem: function(name, href, pos) {
      return '<li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">' +
        '<a itemprop="item" href="' + href + '"><span itemprop="name">' + name + '</span></a>' +
        '<meta itemprop="position" content="' + pos + '"></li>';
    },

    _bcItemCurrent: function(name, pos) {
      return '<li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">' +
        '<span itemprop="name">' + name + '</span>' +
        '<meta itemprop="position" content="' + pos + '"></li>';
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

      var html = '<p class="copy">';
      for (var i = 0; i < mainLinks.length; i++) {
        if (i > 0) html += ' \u00B7 ';
        var name = mainLinks[i].path === '/' ? (c.shortName || '\u0410\u041A\u0421\u0418\u041E\u041C\u0410') : mainLinks[i].name;
        html += '<a href="' + mainLinks[i].path + '" class="footer-link">' + name + '</a>';
      }
      html += '</p>';

      if (legalLinks.length > 0) {
        html += '<p class="copy" style="font-size:.7rem;margin-top:8px;border:none;padding-top:0;">';
        for (var i = 0; i < legalLinks.length; i++) {
          if (i > 0) html += ' \u00B7 ';
          html += '<a href="' + legalLinks[i].path + '" class="footer-link">' + legalLinks[i].name + '</a>';
        }
        html += '</p>';
      }

      var year = new Date().getFullYear();
      var start = c.copyrightStart || 2024;
      html += '<p class="copy" style="font-size:.65rem;margin-top:8px;border:none;padding-top:0;text-transform:none;letter-spacing:0;">' +
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
    }
  };

  w.Nav = Nav;
})(window, document);
