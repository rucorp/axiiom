#!/usr/bin/env python3
"""Генерация industries/index.html — анти-дорвей каталог, сгруппированный по категориям, с CTA и FAQ."""
from pathlib import Path
from collections import defaultdict

CATEGORY_MAP = {
    'avtomatizaciya-restoranov': 'HoReCa & Retail',
    'dostavka-edy': 'HoReCa & Retail',
    'fitness-apps': 'HoReCa & Retail',
    'bronirovanie-gostinits': 'HoReCa & Retail',
    'kiberbezopasnost': 'Security & Fintech',
    'kyc-onboarding': 'Fintech',
    'multi-currency-wallet': 'Fintech',
    'p2p-marketplace': 'Fintech',
    'trading-engine': 'Fintech',
    'investment-crm': 'Fintech',
    'real-time-analytics': 'Fintech',
    'asset-tokenization': 'Fintech',
    'kraudfanding': 'Fintech',
    'crm-medcentry': 'B2B & Enterprise',
    'crm-nedvizhimost': 'B2B & Enterprise',
    'po-stroitelnye-kompanii': 'B2B & Enterprise',
    'erp-proizvodstvo': 'B2B & Enterprise',
    'sistemy-logistika': 'B2B & Enterprise',
    'upravlenie-cepochkami': 'B2B & Enterprise',
    'pravovie-firmu': 'B2B & Enterprise',
    'avtoservice': 'B2B & Enterprise',
    'hr-podbor-personala': 'B2B & Enterprise',
    'selskokhozyaystvo': 'B2B & Enterprise',
    'saas-startupy': 'SaaS & Digital',
    'online-obuchenie': 'SaaS & Digital',
    'platforma-frilans': 'SaaS & Digital',
    'iot-umnyy-dom': 'SaaS & Digital',
    'marketing-analitika': 'SaaS & Digital',
    'upravlenie-proektami': 'SaaS & Digital',
    'udalennaya-rabota': 'SaaS & Digital',
}

EXTRA_TITLES = {
    'kyc-onboarding': ('KYC и онбординг', 'eKYC, AML, биометрия, допуск за 2 мин, 161-ФЗ'),
    'multi-currency-wallet': ('Мультивалютный кошелёк', 'Счета, конвертация, SBP/QR/NFC, PCI DSS, escrow'),
    'p2p-marketplace': ('P2P-маркетплейс', 'Escrow, рейтинги, арбитраж, сплит, highload'),
    'trading-engine': ('Торговый движок', 'Matching <10ms, 100k RPS, FIX API, ликвидность'),
    'investment-crm': ('Investment CRM', 'Воронка инвесторов, KYC, портфель, ЭДО'),
    'real-time-analytics': ('Real-time аналитика', 'ClickHouse, Kafka, дашборды за секунды'),
    'asset-tokenization': ('Токенизация активов', 'Выпуск токенов, смарт-контракты, вторичный рынок'),
}

# Load titles from industries.txt
txt_titles = {}
txt_descs = {}
try:
    with open('industries/industries.txt', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts)>=3:
                txt_titles[parts[0]] = parts[1]
                txt_descs[parts[0]] = parts[2]
except:
    pass

# merge
all_titles = {}
all_descs = {}
for slug, cat in CATEGORY_MAP.items():
    if slug in txt_titles:
        all_titles[slug] = txt_titles[slug]
        all_descs[slug] = txt_descs.get(slug, '')
    elif slug in EXTRA_TITLES:
        all_titles[slug] = EXTRA_TITLES[slug][0]
        all_descs[slug] = EXTRA_TITLES[slug][1]
    else:
        all_titles[slug] = slug.replace('-', ' ').title()
        all_descs[slug] = 'Разработка под ключ, интеграция, поддержка 24/7'

# Group by category
grouped = defaultdict(list)
for slug, cat in CATEGORY_MAP.items():
    grouped[cat].append(slug)

# Order categories
cat_order = ['Fintech', 'HoReCa & Retail', 'B2B & Enterprise', 'SaaS & Digital', 'Security & Fintech']
# sort slugs within category alphabetically by title
for cat in grouped:
    grouped[cat] = sorted(grouped[cat], key=lambda s: all_titles[s])

# Build HTML cards
def card_html(slug):
    title = all_titles[slug]
    desc = all_descs[slug][:160]
    return f'''
            <a href="{slug}.html" class="tool-card blog-card reveal">
                <h3>{title}</h3>
                <p>{desc}</p>
                <span class="blog-read">Подробнее →</span>
            </a>'''

sections_html = ""
for cat in cat_order:
    slugs = grouped.get(cat, [])
    if not slugs:
        continue
    cards = "\n".join(card_html(s) for s in slugs)
    sections_html += f'''
        <div class="container" style="margin-top:48px">
            <p class="label reveal">{cat}</p>
            <h2 class="reveal">{cat} — {len(slugs)} решений</h2>
            <div class="tools-grid">
                {cards}
            </div>
        </div>
'''

html = f'''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="theme-color" content="#0A0A0F">
    <script>try{{var t=localStorage.getItem('theme')||(window.matchMedia('(prefers-color-scheme: light)').matches?'light':'');document.documentElement.setAttribute('data-theme',t)}}catch(e){{}}</script>
    <title>Отраслевые решения — 30 кейсов AXIIOM | Fintech, HoReCa, B2B, SaaS</title>
    <meta name="description" content="30 отраслевых решений AXIIOM: финтех (KYC, кошельки, P2P, трейдинг, токенизация), HoReCa (рестораны, доставка, отели, фитнес), B2B (CRM, ERP, логистика, стройка), SaaS (обучение, фриланс, IoT, аналитика). Кейсы, модули, стек, интеграции, сроки от 6 недель.">
    <link rel="canonical" href="https://axiiom.ru/industries/">
    <link rel="icon" type="image/svg+xml" href="/favicon.svg">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="preload" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" as="style">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://axiiom.ru/industries/">
    <meta property="og:title" content="Отраслевые решения — 30 кейсов AXIIOM">
    <meta property="og:description" content="Финтех, HoReCa, B2B, SaaS — 30 готовых решений с кейсами, модулями и интеграциями. Запуск от 6 недель, 50+ проектов.">
    <meta property="og:image" content="https://axiiom.ru/og-image.png">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:locale" content="ru_RU">
    <meta property="og:site_name" content="AXIIOM">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:url" content="https://axiiom.ru/industries/">
    <meta name="twitter:title" content="Отраслевые решения — 30 кейсов AXIIOM">
    <meta name="twitter:description" content="Финтех, HoReCa, B2B, SaaS — 30 готовых решений с кейсами, модулями и интеграциями.">
    <meta name="twitter:image" content="https://axiiom.ru/og-image.png">
    <link rel="stylesheet" href="/styles.css?v=20260911">
    <link rel="stylesheet" href="/preloader.css?v=20260911">
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "Organization",
      "name": "AXIIOM",
      "alternateName": "ООО Аксиома",
      "description": "IT-компания, специализирующаяся на разработке финтех-платформ, систем лояльности и highload-систем.",
      "url": "https://axiiom.ru/",
      "foundingDate": "2004",
      "logo": "https://axiiom.ru/og-image.png",
      "address": [{{"@type": "PostalAddress","streetAddress": "192029, г. Санкт-Петербург, ул. Профессора Качалова, 15А","addressLocality": "Санкт-Петербург","addressCountry": "RU"}}],
      "contactPoint": {{"@type": "ContactPoint","telephone": "+7-812-928-74-78","contactType": "customer service","email": "hello@axiiom.ru","availableLanguage": "Russian"}},
      "sameAs": ["https://t.me/axiiom"]
    }}
    </script>
    <script type="application/ld+json">
    {{
      "@context":"https://schema.org",
      "@type":"BreadcrumbList",
      "itemListElement":[{{"@type":"ListItem","position":1,"name":"Главная","item":"https://axiiom.ru/"}},{{"@type":"ListItem","position":2,"name":"Отраслевые решения","item":"https://axiiom.ru/industries/"}}]
    }}
    </script>
    <script type="application/ld+json">
    {{
      "@context":"https://schema.org",
      "@type":"FAQPage",
      "mainEntity":[
        {{"@type":"Question","name":"Это не дорвеи?","acceptedAnswer":{{"@type":"Answer","text":"Нет. Каждая страница — полноценный лендинг с уникальными болями, модулями, стеком, интеграциями, кейсами и FAQ. 50+ проектов в портфолио, 99.99% uptime."}}}},
        {{"@type":"Question","name":"Сколько стоит?","acceptedAnswer":{{"@type":"Answer","text":"MVP от 400к ₽ для HoReCa, от 2 млн ₽ для финтеха. Точная смета после бесплатной Discovery 1–2 недели."}}}},
        {{"@type":"Question","name":"Даёте демо?","acceptedAnswer":{{"@type":"Answer","text":"Да, sandbox, архитектурная схема и смета за 24 часа. Смотрите /demo/app/ и /projects/."}}}}
      ]
    }}
    </script>
    <link rel="manifest" href="/manifest.webmanifest">
    <link rel="apple-touch-icon" sizes="180x180" href="/icons/apple-touch-icon.png">
</head>
<body>
<a href="#main" class="skip-link">Перейти к содержанию</a>
<div id="preloader">
<script>(function(){{var p=document.getElementById('preloader');if(!p)return;if(sessionStorage.getItem('_seen')){{p.style.display='none';return}}sessionStorage.setItem('_seen','1');var t=Date.now();p._start=t;setTimeout(function(){{p.classList.add('_rdy')}},500);window.addEventListener('load',function(){{var e=Date.now()-t;if(e<900){{setTimeout(function(){{p.classList.add('hidden');setTimeout(function(){{p.classList.add('hidden-done')}},500)}},900-e)}}else{{p.classList.add('hidden');setTimeout(function(){{p.classList.add('hidden-done')}},500)}}}})}})()</script>
  <svg class="preloader-svg" viewBox="0 0 36 36" width="80" height="80">
    <rect class="pr1" x="2" y="2" width="14" height="14" rx="2"/>
    <rect class="pr2" x="20" y="2" width="14" height="14" rx="2"/>
    <rect class="pr3" x="2" y="20" width="14" height="14" rx="2"/>
    <rect class="pr4" x="20" y="20" width="14" height="14" rx="2"/>
    <circle class="pc" cx="27" cy="27" r="3"/>
  </svg>
</div>
<div class="noise"></div>
<div class="grid-overlay"></div>
<header class="header" id="header">
    <div class="container">
        <nav class="nav">
            <a href="/" class="logo">
                <svg width="30" height="30" viewBox="0 0 36 36" fill="none"><rect x="2" y="2" width="14" height="14" rx="2" stroke="currentColor" stroke-width="1.5" opacity=".4"/><rect x="20" y="2" width="14" height="14" rx="2" stroke="currentColor" stroke-width="1.5" opacity=".4"/><rect x="2" y="20" width="14" height="14" rx="2" stroke="currentColor" stroke-width="1.5" opacity=".4"/><rect x="20" y="20" width="14" height="14" rx="2" stroke="currentColor" stroke-width="1.5"/><circle cx="27" cy="27" r="3" fill="currentColor" opacity=".8"/></svg>
                <span>AXIIOM</span>
            </a>
            <ul class="nav-links nav-links--desktop" id="desktopNav"></ul>
            <div class="nav-actions">
                <a href="/#contact" class="btn btn-nav" id="ctaBtn">Обсудить проект</a>
                <button class="theme-btn" id="themeToggle" aria-label="Сменить тему"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"/></svg></button>
                <button class="nav-toggle" id="navToggle" aria-label="Меню"><span></span><span></span><span></span></button>
            </div>
        </nav>
    </div>
</header>
<div class="nav-overlay" id="navOverlay"><ul class="nav-links" id="mobileNav"></ul></div>
<nav class="breadcrumbs" id="breadcrumbs" aria-label="Breadcrumb"><div class="container"></div></nav>
<main id="main">
<section class="hero industries-hero">
    <div class="container">
        <div class="hero-content">
            <div class="hero-bg-svg"><svg width="800" height="600" viewBox="0 0 800 600" fill="none"><circle cx="400" cy="300" r="280" stroke="rgba(255,255,255,0.05)" stroke-width="2"/><circle cx="400" cy="300" r="200" stroke="rgba(255,255,255,0.06)" stroke-width="2"/><circle cx="400" cy="300" r="120" stroke="rgba(255,255,255,0.08)" stroke-width="2"/><line x1="50" y1="300" x2="750" y2="300" stroke="rgba(255,255,255,0.04)" stroke-width="2"/><line x1="400" y1="20" x2="400" y2="580" stroke="rgba(255,255,255,0.04)" stroke-width="2"/><path d="M200 300 L400 100 L600 300 L400 500 Z" stroke="rgba(255,255,255,0.05)" stroke-width="2" fill="none"/><circle cx="400" cy="300" r="4" fill="rgba(255,255,255,0.12)"/></svg></div>
            <div class="badge-row"><p class="badge">AXIIOM Industries • 30 решений</p><button class="share-btn" onclick="copyPageUrl(this)" aria-label="Поделиться"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 12v8a2 2 0 002 2h12a2 2 0 002-2v-8"/><polyline points="16 6 12 2 8 6"/><line x1="12" y1="2" x2="12" y2="15"/></svg><span class="share-tooltip">Ссылка скопирована</span></button></div>
            <h1>Отраслевые решения AXIIOM — 30 готовых кейсов для вашего бизнеса</h1>
            <p class="hero-desc">Не дорвеи, а полноценные лендинги: уникальные боли, модули, стек, интеграции, кейсы с цифрами, FAQ и CTA. Fintech, HoReCa, B2B, SaaS — запуск от 6 недель, 50+ проектов, 99.99% uptime, 161-ФЗ/PCI DSS. Каждая страница — инструмент привлечения IT-заказов, а не SEO-спам.</p>
            <div class="hero-btns"><a href="/#contact" class="btn">Обсудить проект</a><a href="/calculator/" class="btn btn-outline">Калькулятор стоимости</a></div>
            <div class="hero-trust"><span><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--clr-accent)" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg> 30 решений</span><span><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--clr-accent)" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg> 50+ проектов</span><span><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--clr-accent)" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg> 99.99% Uptime</span></div>
        </div>
    </div>
</section>

<section class="section">
    <div class="container">
        <p class="label reveal">Как мы делаем</p>
        <h2 class="reveal">От боли к результату — не шаблон, а решение</h2>
        <p class="content-wrapper reveal" style="max-width:720px;margin:0 auto;color:var(--clr-muted)">Каждая отраслевая страница построена по одной схеме, но с уникальным контентом: 3 боли отрасли с решением, 10 модулей, путь заказа, стек (Backend/Frontend/Mobile/Infra), интеграции (банки, 1С, iiko, СДЭК...), 2 кейса с задачей/решением/результатом, FAQ с JSON-LD, related-решения и двойной CTA (контакт + калькулятор). Это не дорвей, а посадочная для привлечения IT-заказов — с портфолио, демо и прозрачной сметой.</p>
        <div class="problems-grid" style="margin-top:32px">
            <div class="glass-card reveal card-pad-md"><p class="problem-text">Разработчики обещали, но проект застрял</p><p class="solution-text"><strong>Решение: фиксируем scope, бюджет и сроки на Discovery, спринты по 2 недели с демо, SLA 24/7.</strong></p></div>
            <div class="glass-card reveal card-pad-md"><p class="problem-text">Нет интеграции с банками/1С/iiko</p><p class="solution-text"><strong>Решение: API-first, готовые коннекторы — Сбер, Альфа, Тинькофф, SBP, 1С, iiko, СДЭК, Яндекс.</strong></p></div>
            <div class="glass-card reveal card-pad-md"><p class="problem-text">Падает в пик, нет аналитики</p><p class="solution-text"><strong>Решение: highload — Go, Kafka, ClickHouse, Kubernetes, 99.99% uptime, real-time дашборды.</strong></p></div>
        </div>
    </div>
</section>

{sections_html}

<section class="section dark">
    <div class="container">
        <p class="label reveal">FAQ</p>
        <h2 class="reveal">Частые вопросы</h2>
        <div class="faq-grid reveal">
            <div class="glass-card card-pad-md"><h3>Это не дорвеи?</h3><p>Нет. Каждая страница — уникальный лендинг с болями, модулями, стеком, интеграциями, кейсами, FAQ, JSON-LD Service+FAQPage, траст-бейджами и двойным CTA. 50+ проектов, 99.99% uptime, 161-ФЗ/PCI DSS.</p></div>
            <div class="glass-card card-pad-md"><h3>Сколько стоит?</h3><p>MVP от 400к ₽ для HoReCa, от 2 млн ₽ для финтеха. Точная смета после бесплатной Discovery 1–2 недели. Есть калькулятор /calculator/.</p></div>
            <div class="glass-card card-pad-md"><h3>Даёте демо?</h3><p>Да, sandbox, схема архитектуры и смета за 24 часа. Смотрите /demo/app/ и /projects/.</p></div>
        </div>
    </div>
</section>

<section class="section cta-section">
<div class="container">
<div class="glass-card cta-card reveal">
<h2>Нужна разработка под вашу отрасль?</h2>
<p>Оставьте заявку — подберём решение из 30 кейсов, покажем демо, подготовим архитектуру и смету за 24 часа. Бесплатная Discovery 1–2 недели.</p>
<div class="cta-contacts">
<a href="/#contact" class="btn">Обсудить проект</a>
<a href="/calculator/" class="btn btn-outline">Рассчитать стоимость</a>
</div>
<p style="margin-top:16px;font-size:.85rem;color:var(--clr-muted)">Или посмотрите <a href="/projects/" class="link-accent">портфолио</a> и <a href="/demo/app/" class="link-accent">демо</a></p>
</div>
</div>
</section>

</main>
<footer class="footer"><div class="container"><div id="footerCopy"></div></div></footer>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-HFS4BDGTV4"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag("js",new Date());gtag("config","G-HFS4BDGTV4");</script>
<script src="/metrika.js?v=20260911" defer></script>
<script src="/config.js?v=20260911"></script>
<script src="/nav.js?v=20260911"></script>
<script>Nav.init({{ cta: true, breadcrumbs: true }});</script>
<script src="/theme.js?v=20260911"></script>
<script src="/preloader.js?v=20260911"></script>
<script>
(function(){{var t=document.getElementById('navToggle');var o=document.getElementById('navOverlay');if(!t||!o)return;t.addEventListener('click',function(e){{e.stopPropagation();o.classList.toggle('open');t.classList.toggle('active');document.body.style.overflow=o.classList.contains('open')?'hidden':'';}});}})();
function copyPageUrl(btn){{var url=window.location.href;var ta=document.createElement('textarea');ta.value=url;ta.style.position='fixed';ta.style.left='0';ta.style.top='0';ta.style.width='2em';ta.style.height='2em';ta.style.padding='0';ta.style.border='none';ta.style.outline='none';ta.style.background='transparent';ta.style.color='transparent';document.body.appendChild(ta);ta.focus();ta.select();document.execCommand('copy');document.body.removeChild(ta);var tip=btn.querySelector('.share-tooltip');if(tip){{tip.classList.add('show');setTimeout(function(){{tip.classList.remove('show');}},2000);}}}}
var reveals=document.querySelectorAll('.reveal');var ro=new IntersectionObserver(function(e){{e.forEach(function(entry){{if(entry.isIntersecting)entry.target.classList.add('visible');}});}},{{threshold:.15}});reveals.forEach(function(r){{ro.observe(r);}});
</script>
</body>
</html>
'''

with open('industries/index.html','w',encoding='utf-8') as f:
    f.write(html)

print(f"industries/index.html generated: {len(all_titles)} solutions grouped")
