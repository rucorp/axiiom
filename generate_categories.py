#!/usr/bin/env python3
from datetime import datetime
import os
from string import Template

CATEGORIES = {
    'fintech': {
        'name': 'Fintech',
        'title': 'Fintech разработка — 8 решений для банков, бирж и кошельков',
        'desc': 'Разработка fintech-продуктов: KYC по 161-ФЗ, мультивалютные кошельки с SBP/QR/NFC, P2P-маркетплейсы, trading engine 100k RPS, токенизация, investment CRM, real-time аналитика, краудфандинг. PCI DSS, Vault/HSM, 50+ проектов.',
        'h1': 'Fintech разработка под ключ — от KYC до биржи',
        'hero': '8 готовых fintech-решений: KYC с биометрией, кошельки с SBP и escrow, P2P с арбитражем, trading engine на Go, токенизация с депозитарием. Проходим 161-ФЗ/PCI DSS, интеграция со Сбер/Альфа/Тинькофф. MVP от 2 млн ₽, Discovery бесплатно.',
        'price': 'от 2 млн ₽',
        'price_num': '2000000',
        'timeline': '3 месяца',
        'bonus': 'Discovery бесплатно',
        'slugs': ['kyc-onboarding','multi-currency-wallet','p2p-marketplace','trading-engine','asset-tokenization','investment-crm','real-time-analytics','kraudfanding'],
        'trust': '161-ФЗ / PCI DSS',
        'icon': '<svg width="400" height="400" viewBox="0 0 400 400" fill="none"><rect x="100" y="80" width="200" height="140" rx="16" stroke="currentColor" stroke-width="2" opacity=".15"/><rect x="120" y="100" width="60" height="12" rx="6" fill="currentColor" opacity=".12"/><rect x="120" y="130" width="100" height="8" rx="4" fill="currentColor" opacity=".08"/><circle cx="260" cy="140" r="24" stroke="currentColor" stroke-width="2" opacity=".15"/><path d="M250 140 L255 145 L270 130" stroke="currentColor" stroke-width="2" opacity=".15"/><rect x="140" y="260" width="120" height="80" rx="12" stroke="currentColor" stroke-width="2" opacity=".1"/><path d="M160 280 h80 M160 300 h60" stroke="currentColor" stroke-width="2" opacity=".1"/></svg>',
    },
    'horeca': {
        'name': 'HoReCa & Retail',
        'title': 'Автоматизация ресторанов, доставки и отелей — 4 решения',
        'desc': 'Автоматизация HoReCa: рестораны с iiko/r_keeper и KDS, доставка еды с трекингом курьеров, бронирование отелей с Channel Manager и динамическими ценами, фитнес-приложения с геймификацией. 54-ФЗ, LOVII лояльность.',
        'h1': 'HoReCa и Retail — автоматизация ресторанов, доставки и отелей',
        'hero': '4 решения для HoReCa: единое окно POS+CRM, KDS, трекинг курьеров, Channel Manager, динамическое ценообразование, CRM с LTV. Интеграция iiko, r_keeper, Яндекс.Еда, СДЭК, 1С, 54-ФЗ. MVP от 400к ₽, запуск 6 недель, аудит бесплатно.',
        'price': 'от 400к ₽',
        'price_num': '400000',
        'timeline': '6 недель',
        'bonus': 'Аудит бесплатно',
        'slugs': ['avtomatizaciya-restoranov','dostavka-edy','bronirovanie-gostinits','fitness-apps'],
        'trust': 'iiko / r_keeper / 54-ФЗ',
        'icon': '<svg width="400" height="400" viewBox="0 0 400 400" fill="none"><circle cx="200" cy="180" r="80" stroke="currentColor" stroke-width="2" opacity=".12"/><path d="M160 160 L200 120 L240 160 L200 240 Z" stroke="currentColor" stroke-width="2" opacity=".12"/><rect x="140" y="260" width="120" height="60" rx="12" stroke="currentColor" stroke-width="2" opacity=".1"/><circle cx="170" cy="290" r="8" fill="currentColor" opacity=".1"/><circle cx="230" cy="290" r="8" fill="currentColor" opacity=".1"/></svg>',
    },
    'b2b': {
        'name': 'B2B & Enterprise',
        'title': 'B2B и Enterprise разработка — 10 решений: CRM, ERP, логистика',
        'desc': 'B2B разработка: CRM для медцентров, недвижимости, стройкомпаний, ERP для производства, логистика с GPS, SCM, ПО для юрфирм, автосервиса, HR, сельского хозяйства. 1С, BIM, WMS, ЭДО, OPC UA. 50+ проектов.',
        'h1': 'B2B и Enterprise — CRM, ERP, логистика и отраслевое ПО',
        'hero': '10 B2B-решений: CRM для клиник и недвижимости, ERP для производства и стройки, логистика с оптимизацией маршрутов, SCM с прогнозом ML, HR с парсингом HH, автосервис с VIN. Интеграция 1С, BIM, WMS, ЭДО, СДЭК. MVP от 800к ₽, 2 месяца, аудит бесплатно.',
        'price': 'от 800к ₽',
        'price_num': '800000',
        'timeline': '2 месяца',
        'bonus': 'Аудит и ТЗ бесплатно',
        'slugs': ['crm-medcentry','crm-nedvizhimost','po-stroitelnye-kompanii','erp-proizvodstvo','sistemy-logistika','upravlenie-cepochkami','pravovie-firmu','avtoservice','hr-podbor-personala','selskokhozyaystvo'],
        'trust': '1С / BIM / WMS / ЭДО',
        'icon': '<svg width="400" height="400" viewBox="0 0 400 400" fill="none"><rect x="80" y="80" width="240" height="160" rx="12" stroke="currentColor" stroke-width="2" opacity=".12"/><line x1="80" y1="120" x2="320" y2="120" stroke="currentColor" stroke-width="2" opacity=".08"/><rect x="100" y="140" width="60" height="60" rx="8" stroke="currentColor" stroke-width="2" opacity=".1"/><rect x="180" y="140" width="60" height="60" rx="8" stroke="currentColor" stroke-width="2" opacity=".1"/><rect x="100" y="260" width="200" height="40" rx="8" stroke="currentColor" stroke-width="2" opacity=".08"/></svg>',
    },
    'saas': {
        'name': 'SaaS & Digital',
        'title': 'SaaS разработка для стартапов — 7 решений: LMS, IoT, маркетплейсы',
        'desc': 'SaaS для стартапов: мультитенантность, биллинг, API, LMS с вебинарами на 1000+, фриланс-маркетплейс с escrow, IoT умный дом 50+ брендов, маркетинг-аналитика, управление проектами, удалённая работа. Kubernetes, Yandex Cloud.',
        'h1': 'SaaS и Digital — платформы для стартапов, обучения и IoT',
        'hero': '7 SaaS-решений: мультитенантные платформы с биллингом и API, LMS с геймификацией, фриланс с escrow, IoT с Zigbee/Z-Wave, маркетинг-аналитика с атрибуцией, управление проектами с Гантом. MVP от 600к ₽, 2 месяца, консультация бесплатно.',
        'price': 'от 600к ₽',
        'price_num': '600000',
        'timeline': '2 месяца',
        'bonus': 'Консультация бесплатно',
        'slugs': ['saas-startupy','online-obuchenie','platforma-frilans','iot-umnyy-dom','marketing-analitika','upravlenie-proektami','udalennaya-rabota'],
        'trust': 'Kubernetes / Highload 99.99%',
        'icon': '<svg width="400" height="400" viewBox="0 0 400 400" fill="none"><rect x="80" y="100" width="240" height="160" rx="16" stroke="currentColor" stroke-width="2" opacity=".12"/><circle cx="120" cy="130" r="6" fill="currentColor" opacity=".15"/><circle cx="140" cy="130" r="6" fill="currentColor" opacity=".12"/><circle cx="160" cy="130" r="6" fill="currentColor" opacity=".09"/><path d="M100 160 L300 160 M100 180 L250 180 M100 200 L280 200" stroke="currentColor" stroke-width="2" opacity=".08"/><rect x="120" y="280" width="160" height="60" rx="30" stroke="currentColor" stroke-width="2" opacity=".1"/></svg>',
    },
    'security': {
        'name': 'Security',
        'title': 'Кибербезопасность для бизнеса — аудит, SIEM, 152-ФЗ',
        'desc': 'Кибербезопасность: SIEM, EDR, WAF, DLP, шифрование, VPN с MFA, backup 3-2-1, обучение с фишинговыми симуляциями. Готовим к 152-ФЗ/PCI DSS/161-ФЗ, Vault, SonarQube.',
        'h1': 'Кибербезопасность — защита бизнеса под ключ',
        'hero': 'Security-решения: SIEM, EDR, корреляция событий, фишинг-тесты, шифрование, DLP, VPN с MFA, backup 3-2-1. Готовим к аудиту 152-ФЗ/PCI DSS/161-ФЗ, Vault, SonarQube. MVP от 500к ₽, 1 месяц, аудит безопасности бесплатно.',
        'price': 'от 500к ₽',
        'price_num': '500000',
        'timeline': '1 месяц',
        'bonus': 'Аудит безопасности бесплатно',
        'slugs': ['kiberbezopasnost'],
        'trust': '152-ФЗ / PCI DSS / 161-ФЗ',
        'icon': '<svg width="400" height="400" viewBox="0 0 400 400" fill="none"><path d="M200 60 L300 100 L300 200 C300 260 250 310 200 340 C150 310 100 260 100 200 L100 100 Z" stroke="currentColor" stroke-width="2" opacity=".12"/><circle cx="200" cy="190" r="40" stroke="currentColor" stroke-width="2" opacity=".12"/><path d="M180 190 L195 205 L220 175" stroke="currentColor" stroke-width="2" opacity=".15"/></svg>',
    },
}

titles = {}
try:
    with open('industries/industries.txt', encoding='utf-8') as f:
        for line in f:
            parts=line.strip().split('|')
            if parts:
                titles[parts[0]] = (parts[1] if len(parts)>1 else parts[0], parts[2] if len(parts)>2 else '')
except:
    pass

today = datetime.now().strftime("%d.%m.%Y")

tmpl = Template('''<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="theme-color" content="#0A0A0F">
<title>$title | AXIIOM</title>
<meta name="description" content="$desc">
<link rel="canonical" href="https://axiiom.ru/industries/$slug/">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<meta property="og:type" content="website">
<meta property="og:url" content="https://axiiom.ru/industries/$slug/">
<meta property="og:title" content="$title — AXIIOM">
<meta property="og:description" content="$desc">
<meta property="og:image" content="https://axiiom.ru/og/industries/$slug.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="ru_RU">
<meta property="og:site_name" content="AXIIOM">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="$title — AXIIOM">
<meta name="twitter:description" content="$desc">
<meta name="twitter:image" content="https://axiiom.ru/og/industries/$slug.png">
<link rel="stylesheet" href="/styles.css?v=20260912">
<link rel="stylesheet" href="/preloader.css?v=20260912">
<link rel="manifest" href="/manifest.webmanifest">
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "WebPage",
      "name": "$title",
      "description": "$desc",
      "url": "https://axiiom.ru/industries/$slug/"
    },
    {
      "@type": "BreadcrumbList",
      "itemListElement": [
        { "@type": "ListItem", "position": 1, "name": "Главная", "item": "https://axiiom.ru/" },
        { "@type": "ListItem", "position": 2, "name": "Решения", "item": "https://axiiom.ru/industries/" },
        { "@type": "ListItem", "position": 3, "name": "$name", "item": "https://axiiom.ru/industries/$slug/" }
      ]
    },
    {
      "@type": "Service",
      "serviceType": "$name",
      "provider": { "@type": "Organization", "name": "AXIIOM", "url": "https://axiiom.ru/" },
      "description": "$desc",
      "offers": { "@type": "Offer", "priceCurrency": "RUB", "price": "$price_num", "url": "https://axiiom.ru/industries/$slug/" }
    }
  ]
}
</script>
</head>
<body>
<a href="#main" class="skip-link">Перейти к содержанию</a>
<div id="preloader"><script>(function(){var p=document.getElementById('preloader');if(!p)return;if(sessionStorage.getItem('_seen')){p.style.display='none';return}sessionStorage.setItem('_seen','1');var t=Date.now();p._start=t;setTimeout(function(){p.classList.add('_rdy')},500);window.addEventListener('load',function(){var e=Date.now()-t;if(e<900){setTimeout(function(){p.classList.add('hidden');setTimeout(function(){p.classList.add('hidden-done')},500)},900-e)}else{p.classList.add('hidden');setTimeout(function(){p.classList.add('hidden-done')},500)}})})()</script><svg class="preloader-svg" viewBox="0 0 36 36" width="80" height="80"><rect class="pr1" x="2" y="2" width="14" height="14" rx="2"/><rect class="pr2" x="20" y="2" width="14" height="14" rx="2"/><rect class="pr3" x="2" y="20" width="14" height="14" rx="2"/><rect class="pr4" x="20" y="20" width="14" height="14" rx="2"/><circle class="pc" cx="27" cy="27" r="3"/></svg></div>
<div class="noise"></div><div class="grid-overlay"></div>
<header class="header" id="header"><div class="container"><nav class="nav"><a href="/" class="logo"><svg width="30" height="30" viewBox="0 0 36 36" fill="none"><rect x="2" y="2" width="14" height="14" rx="2" stroke="currentColor" stroke-width="1.5" opacity=".4"/><rect x="20" y="2" width="14" height="14" rx="2" stroke="currentColor" stroke-width="1.5" opacity=".4"/><rect x="2" y="20" width="14" height="14" rx="2" stroke="currentColor" stroke-width="1.5" opacity=".4"/><rect x="20" y="20" width="14" height="14" rx="2" stroke="currentColor" stroke-width="1.5"/><circle cx="27" cy="27" r="3" fill="currentColor" opacity=".8"/></svg><span>AXIIOM</span></a><ul class="nav-links nav-links--desktop" id="desktopNav"></ul><div class="nav-actions"><a href="/#contact" class="btn btn-nav" id="ctaBtn">Обсудить проект</a><button class="theme-btn" id="themeToggle" aria-label="Сменить тему"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"/></svg></button><button class="nav-toggle" id="navToggle" aria-label="Меню"><span></span><span></span><span></span></button></div></nav></div></header>
<div class="nav-overlay" id="navOverlay"><ul class="nav-links" id="mobileNav"></ul></div>
<nav class="breadcrumbs" id="breadcrumbs" aria-label="Breadcrumb"><div class="container"></div></nav>
<main id="main">
<section class="hero industries-hero"><div class="container"><div class="hero-content"><div class="hero-bg-svg"><svg width="800" height="600" viewBox="0 0 800 600" fill="none"><circle cx="400" cy="300" r="280" stroke="rgba(255,255,255,0.05)" stroke-width="2"/><circle cx="400" cy="300" r="200" stroke="rgba(255,255,255,0.06)" stroke-width="2"/><circle cx="400" cy="300" r="120" stroke="rgba(255,255,255,0.08)" stroke-width="2"/><line x1="50" y1="300" x2="750" y2="300" stroke="rgba(255,255,255,0.04)" stroke-width="2"/><line x1="400" y1="20" x2="400" y2="580" stroke="rgba(255,255,255,0.04)" stroke-width="2"/><path d="M200 300 L400 100 L600 300 L400 500 Z" stroke="rgba(255,255,255,0.05)" stroke-width="2" fill="none"/><circle cx="400" cy="300" r="4" fill="rgba(255,255,255,0.12)"/></svg></div><div class="hero-category-icon">$icon</div><div class="badge-row"><p class="badge">$name • AXIIOM • $count решений</p><button class="share-btn" onclick="copyPageUrl(this)" aria-label="Поделиться"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 12v8a2 2 0 002 2h12a2 2 0 002-2v-8"/><polyline points="16 6 12 2 8 6"/><line x1="12" y1="2" x2="12" y2="15"/></svg><span class="share-tooltip">Ссылка скопирована</span></button></div><h1>$h1</h1><p class="hero-desc">$hero</p><div class="price-anchor reveal"><span class="price-badge">MVP $price</span><span class="price-badge">Запуск $timeline</span><span class="price-badge">$bonus</span></div><div class="hero-btns"><a href="/#contact" class="btn">Обсудить проект за 1 час</a><a href="/calculator/?industry=$slug" class="btn btn-outline">Рассчитать стоимость →</a></div><div class="hero-trust"><span><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--clr-accent)" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg> $count решений</span><span><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--clr-accent)" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg> 50+ проектов</span><span><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--clr-accent)" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg> $trust</span></div><div class="author-block reveal"><span class="author-avatar">AX</span><div><strong>Команда AXIIOM</strong> • $name разработка с 2004 года • <span class="author-date">Обновлено: $date • $count решений</span></div></div></div></div></section>

<section class="section"><div class="container"><p class="label reveal">$name</p><h2 class="reveal">Все решения для $name — выбирайте своё</h2><p class="content-wrapper reveal" style="max-width:680px;margin:0 auto;color:var(--clr-muted)">$desc Каждый лендинг — уникальные боли, модули, стек, интеграции, кейсы с цифрами, FAQ под поисковые запросы, калькулятор с предзаполнением ?industry=slug.</p><div class="proof-logos reveal"><span>Сбер</span><span>Альфа-Банк</span><span>Тинькофф</span><span>1С</span><span>iiko</span><span>СДЭК</span><span>Яндекс</span></div></div></section>

<section class="section dark">
<div class="container">
<p class="label reveal">Видео</p>
<h2 class="reveal">Как работает $name — обзор за 90 секунд</h2>
<div class="glass-card reveal" style="max-width:800px;margin:24px auto 0;padding:0;overflow:hidden;position:relative;aspect-ratio:16/9;background:var(--clr-surface);display:flex;align-items:center;justify-content:center">
<div style="text-align:center;padding:40px">
<div style="width:80px;height:80px;border-radius:50%;background:var(--clr-accent);display:flex;align-items:center;justify-content:center;margin:0 auto 16px;cursor:pointer"><svg width="32" height="32" viewBox="0 0 24 24" fill="#0A0A0F"><path d="M8 5v14l11-7z"/></svg></div>
<p style="color:var(--clr-heading);font-weight:600">Видео-обзор $name — $count решений</p>
<p style="color:var(--clr-muted);font-size:.85rem;margin-top:8px">Скоро: архитектура, UX, кейсы за 90 сек. Сейчас — <a href="/demo/app/" class="link-accent">смотрите демо</a> и <a href="/projects/" class="link-accent">портфолио 50+ проектов</a></p>
</div>
</div>
</div>
</section>

<section class="section dark"><div class="container"><div class="tools-grid">
$cards
</div></div></section>

<section class="section"><div class="container"><p class="label reveal">Процесс</p><h2 class="reveal">Как запускаем $name-проект за $timeline</h2><div class="flow-horizontal"><div class="flow-h-stage reveal"><div class="flow-h-line"></div><div class="flow-h-card"><h3>Discovery</h3><p>1–2 недели, $bonus, ТЗ, архитектура</p></div><div class="flow-h-tags"><span class="tag">Бесплатно</span><span class="tag">ТЗ</span></div></div><div class="flow-h-stage reveal"><div class="flow-h-line"></div><div class="flow-h-card"><h3>Дизайн + API</h3><p>UX, схемы, OpenAPI, интеграции</p></div><div class="flow-h-tags"><span class="tag">Figma</span><span class="tag">OpenAPI</span></div></div><div class="flow-h-stage reveal"><div class="flow-h-line"></div><div class="flow-h-card"><h3>MVP</h3><p>$price, 2–3 месяца, спринты с демо</p></div><div class="flow-h-tags"><span class="tag">MVP</span><span class="tag">Демо</span></div></div><div class="flow-h-stage reveal"><div class="flow-h-line"></div><div class="flow-h-card"><h3>Релиз + SLA</h3><p>99.99%, 24/7, мониторинг, алерты</p></div><div class="flow-h-tags"><span class="tag">SLA</span><span class="tag">24/7</span></div></div></div></div></section>

<section class="section dark"><div class="container"><p class="label reveal">FAQ</p><h2 class="reveal">Частые вопросы про $name</h2><div class="faq-grid reveal"><div class="glass-card card-pad-md"><h3>Сколько стоит $name под ключ?</h3><p>MVP $price, полный цикл — индивидуально. Точная смета после бесплатной Discovery 1–2 недели. Калькулятор /calculator/?industry=$slug</p></div><div class="glass-card card-pad-md"><h3>Какие сроки?</h3><p>Discovery 1–2 недели, MVP — $timeline, релиз с SLA 24/7, мониторинг, алерты в Telegram. Отвечаем за 1 час.</p></div><div class="glass-card card-pad-md"><h3>Даёте демо и портфолио?</h3><p>Да, sandbox, архитектурная схема и смета за 24 часа. Смотрите /projects/ и /demo/app/ — 50+ проектов, 99.99% uptime.</p></div></div></div></section>

<section class="section cta-section"><div class="container"><div class="glass-card cta-card reveal"><h2>Нужен $name-проект?</h2><p>Обсудим задачу, покажем демо из $count решений, подготовим архитектуру и смету за 24 часа. $bonus.</p><div class="cta-contacts"><a href="/#contact" class="btn">Обсудить проект</a><a href="/calculator/?industry=$slug" class="btn btn-outline">Рассчитать в калькуляторе</a></div><p style="margin-top:16px;font-size:.85rem;color:var(--clr-muted)">Или посмотрите <a href="/industries/" class="link-accent">все 30 решений</a> и <a href="/projects/" class="link-accent">портфолио</a></p></div></div></section>
</main>
<div id="stickyCta" class="sticky-cta"><p><strong>$name</strong> — MVP $price, $timeline. $bonus</p><a href="/#contact" class="btn">Обсудить проект</a><a href="/calculator/?industry=$slug" class="btn btn-outline">Калькулятор</a></div>
<footer class="footer"><div class="container"><div id="footerCopy"></div></div></footer>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-HFS4BDGTV4"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag("js",new Date());gtag("config","G-HFS4BDGTV4");</script>
<script src="/metrika.js?v=20260912" defer></script><script src="/config.js?v=20260912"></script><script src="/nav.js?v=20260912"></script><script>Nav.init({ cta: true, breadcrumbs: true });</script><script src="/theme.js?v=20260912"></script><script src="/preloader.js?v=20260912"></script>
<script>(function(){var t=document.getElementById('navToggle');var o=document.getElementById('navOverlay');if(!t||!o)return;t.addEventListener('click',function(e){e.stopPropagation();o.classList.toggle('open');t.classList.toggle('active');document.body.style.overflow=o.classList.contains('open')?'hidden':'';});})();function copyPageUrl(btn){var url=window.location.href;var ta=document.createElement('textarea');ta.value=url;ta.style.position='fixed';ta.style.left='0';ta.style.top='0';ta.style.width='2em';ta.style.height='2em';ta.style.padding='0';ta.style.border='none';ta.style.outline='none';ta.style.background='transparent';ta.style.color='transparent';document.body.appendChild(ta);ta.focus();ta.select();document.execCommand('copy');document.body.removeChild(ta);var tip=btn.querySelector('.share-tooltip');if(tip){tip.classList.add('show');setTimeout(function(){tip.classList.remove('show');},2000);}}var reveals=document.querySelectorAll('.reveal');var ro=new IntersectionObserver(function(e){e.forEach(function(entry){if(entry.isIntersecting)entry.target.classList.add('visible');});},{threshold:.15});reveals.forEach(function(r){ro.observe(r);});(function(){var s=document.getElementById('stickyCta');if(!s)return;var showAt=600;window.addEventListener('scroll',function(){if(window.scrollY>showAt)s.classList.add('visible');else s.classList.remove('visible');},{passive:true});})();</script>
</body>
</html>
''')

for slug, data in CATEGORIES.items():
    count = len(data['slugs'])
    cards_html = ""
    for s in data['slugs']:
        t, d = titles.get(s, (s.replace('-',' ').title(), 'Разработка под ключ, интеграция, поддержка 24/7'))
        cards_html += f'<a href="/industries/{s}.html" class="tool-card blog-card reveal"><h3>{t}</h3><p>{d[:160]}</p><span class="blog-read">Подробнее →</span></a>\n'
    html = tmpl.substitute(
        slug=slug,
        name=data['name'],
        title=data['title'],
        desc=data['desc'],
        h1=data['h1'],
        hero=data['hero'],
        price=data['price'],
        price_num=data['price_num'],
        timeline=data['timeline'],
        bonus=data['bonus'],
        count=count,
        trust=data['trust'],
        icon=data['icon'],
        cards=cards_html,
        date=today
    )
    dir_path = f'industries/{slug}'
    os.makedirs(dir_path, exist_ok=True)
    with open(f'{dir_path}/index.html','w',encoding='utf-8') as f:
        f.write(html)
    print(f'Created {dir_path}/index.html with {count} cards')

print('Done categories')
