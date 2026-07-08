var INDUSTRIES = [
  { name: 'Автоматизация ресторанов', path: 'avtomatizaciya-restoranov.html' },
  { name: 'ПО для строительных компаний', path: 'po-stroitelnye-kompanii.html' },
  { name: 'CRM для медицинских центров', path: 'crm-medcentry.html' },
  { name: 'Системы для логистики и грузоперевозок', path: 'sistemy-logistika.html' },
  { name: 'SaaS для стартапов', path: 'saas-startupy.html' },
  { name: 'ERP для производства', path: 'erp-proizvodstvo.html' },
  { name: 'Системы учета для сельского хозяйства', path: 'selskokhozyaystvo.html' },
  { name: 'Мобильные приложения для фитнеса', path: 'fitness-apps.html' },
  { name: 'Платформы для онлайн-обучения', path: 'online-obuchenie.html' },
  { name: 'Системы бронирования для гостиниц', path: 'bronirovanie-gostinits.html' },
  { name: 'CRM для недвижимости', path: 'crm-nedvizhimost.html' },
  { name: 'Инструменты для удаленной работы', path: 'udalennaya-rabota.html' },
  { name: 'Аналитика для маркетинга', path: 'marketing-analitika.html' },
  { name: 'Кибербезопасность для малого бизнеса', path: 'kiberbezopasnost.html' },
  { name: 'Системы управления проектами', path: 'upravlenie-proektami.html' },
  { name: 'Платформы для фриланса', path: 'platforma-frilans.html' },
  { name: 'IoT для умного дома', path: 'iot-umnyy-dom.html' },
  { name: 'Платформы для краудфандинга', path: 'kraudfanding.html' },
  { name: 'Системы управления цепочками поставок', path: 'upravlenie-cepochkami.html' },
  { name: 'ПО для юридических фирм', path: 'pravovie-firmu.html' },
  { name: 'ПО для автосервиса', path: 'avtoservice.html' },
  { name: 'Платформы для доставки еды', path: 'dostavka-edy.html' }
];

function initIndustriesNav(currentPath) {
  var base = '/industries/';
  var desktopNav = document.getElementById('industriesNav');
  var mobileNav = document.getElementById('industriesNavMobile');

  if (mobileNav) {
    var extraLinks = [
      { name: 'На главную axiiom.ru', href: '/' },
      { name: 'Отраслевые решения', href: '/industries/' }
    ];
    extraLinks.forEach(function(e) {
      var a = document.createElement('a');
      a.href = e.href;
      a.textContent = e.name;
      var li = document.createElement('li');
      li.className = 'nav-extra-link';
      li.appendChild(a);
      mobileNav.appendChild(li);
    });
    var sep = document.createElement('li');
    sep.className = 'nav-separator';
    mobileNav.appendChild(sep);
  }

  INDUSTRIES.forEach(function(t) {
    var isActive = t.path === currentPath;
    var link = document.createElement('a');
    link.href = base + t.path;
    link.textContent = t.name;
    if (isActive) link.className = 'nav-active';
    var li = document.createElement('li');
    li.appendChild(link);
    if (desktopNav) {
      desktopNav.appendChild(li.cloneNode(true));
    }
    if (mobileNav) {
      mobileNav.appendChild(li.cloneNode(true));
    }
  });
}
