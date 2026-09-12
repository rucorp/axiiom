#!/usr/bin/env python3
path = 'calculator/index.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Mapping for industry -> service and text
mapping_js = """
// Industry prefill from ?industry=slug
(function(){
  var INDUSTRY_MAP = {
    'kyc-onboarding': {service:'fintech', label:'KYC и онбординг по 161-ФЗ'},
    'multi-currency-wallet': {service:'fintech', label:'Мультивалютный кошелёк'},
    'p2p-marketplace': {service:'fintech', label:'P2P-маркетплейс'},
    'trading-engine': {service:'fintech', label:'Торговый движок / биржа'},
    'asset-tokenization': {service:'fintech', label:'Токенизация активов'},
    'investment-crm': {service:'fintech', label:'Investment CRM'},
    'real-time-analytics': {service:'highload', label:'Real-time аналитика'},
    'kraudfanding': {service:'fintech', label:'Краудфандинг-платформа'},
    'avtomatizaciya-restoranov': {service:'webapp', label:'Автоматизация ресторанов'},
    'dostavka-edy': {service:'mobile', label:'Доставка еды'},
    'bronirovanie-gostinits': {service:'webapp', label:'Бронирование гостиниц'},
    'fitness-apps': {service:'mobile', label:'Фитнес-приложение'},
    'crm-medcentry': {service:'webapp', label:'CRM для медцентров'},
    'crm-nedvizhimost': {service:'webapp', label:'CRM для недвижимости'},
    'po-stroitelnye-kompanii': {service:'webapp', label:'ПО для стройкомпаний'},
    'erp-proizvodstvo': {service:'highload', label:'ERP для производства'},
    'sistemy-logistika': {service:'highload', label:'Логистика'},
    'upravlenie-cepochkami': {service:'highload', label:'Управление цепочками'},
    'pravovie-firmu': {service:'webapp', label:'ПО для юрфирм'},
    'avtoservice': {service:'webapp', label:'ПО для автосервиса'},
    'hr-podbor-personala': {service:'webapp', label:'HR и подбор'},
    'selskokhozyaystvo': {service:'webapp', label:'Сельское хозяйство'},
    'saas-startupy': {service:'highload', label:'SaaS для стартапов'},
    'online-obuchenie': {service:'webapp', label:'Онлайн-обучение'},
    'platforma-frilans': {service:'webapp', label:'Платформа фриланса'},
    'iot-umnyy-dom': {service:'highload', label:'IoT умный дом'},
    'marketing-analitika': {service:'highload', label:'Маркетинг-аналитика'},
    'upravlenie-proektami': {service:'webapp', label:'Управление проектами'},
    'udalennaya-rabota': {service:'webapp', label:'Удалённая работа'},
    'kiberbezopasnost': {service:'security', label:'Кибербезопасность'},
    'fintech': {service:'fintech', label:'Fintech'},
    'horeca': {service:'webapp', label:'HoReCa & Retail'},
    'b2b': {service:'highload', label:'B2B & Enterprise'},
    'saas': {service:'highload', label:'SaaS & Digital'},
    'security': {service:'security', label:'Security'}
  };
  var params = new URLSearchParams(window.location.search);
  var industry = params.get('industry');
  if(!industry) return;
  var mapped = INDUSTRY_MAP[industry];
  if(!mapped) return;
  // Show banner
  var banner = document.createElement('div');
  banner.className = 'glass-card';
  banner.style.cssText = 'max-width:520px;margin:0 auto 24px;padding:16px 20px;text-align:left;display:flex;gap:12px;align-items:center';
  banner.innerHTML = '<span style="font-size:1.2rem">⚡</span><div><strong style="color:var(--clr-heading)">'+mapped.label+'</strong><br><span style="font-size:.85rem;color:var(--clr-muted)">Калькулятор предзаполнен для отрасли <code>'+industry+'</code>. Выберите параметры — получите смету за 30 сек.</span></div>';
  var calcDesc = document.querySelector('.calc-desc');
  if(calcDesc && calcDesc.parentNode) calcDesc.parentNode.insertBefore(banner, calcDesc.nextSibling);
  // Preselect service after renderServices
  var trySelect = function(){
    var grid = document.getElementById('serviceGrid');
    if(!grid || !grid.querySelectorAll) return false;
    var el = grid.querySelector('[data-id=\"'+mapped.service+'\"]');
    if(el){
      el.click();
      // highlight
      el.scrollIntoView({behavior:'smooth', block:'center'});
      return true;
    }
    return false;
  };
  // Wait for render
  var attempts = 0;
  var iv = setInterval(function(){
    attempts++;
    if(trySelect() || attempts>20) clearInterval(iv);
  }, 300);
})();
"""

# inject before closing </script> of main calc script
# find "// Init" section
if 'INDUSTRY_MAP' in content:
    print('already injected')
else:
    # inject after calculatePrice function definition, before // Init
    content = content.replace('// Init\n', mapping_js + '\n// Init\n')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('injected calculator prefill')

