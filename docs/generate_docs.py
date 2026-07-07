#!/usr/bin/env python3
"""Generate documentation HTML pages from markdown sources."""

import os
import re
import markdown
import shutil

SRC = os.path.dirname(os.path.abspath(__file__))
OUT = SRC

def slugify(name):
    s = name.lower().strip()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[-\s]+', '-', s)
    return s

DOCS = [
    # ── SRS / Техническая документация ──
    {
        "slug": "srs-v2",
        "title": "Software Requirements Specification",
        "subtitle": "Агрегатор доставки продуктов из супермаркетов",
        "desc": "Полная спецификация программного продукта: 2 тома, 14 бизнес-процессов, 7 ADR, архитектура, data model, API, тестирование.",
        "category": "SRS / Техническая документация",
        "source": "SRS-main/SRS-v2.md",
        "tags": ["SRS", "specification", "architecture", "API", "microservices"],
    },
    {
        "slug": "audit-as-is",
        "title": "Аудит текущего состояния системы (AS IS)",
        "desc": "Детальный анализ существующей системы: 178 таблиц PostgreSQL, 100 API endpoint'ов, технологический стек, алгоритмы.",
        "category": "SRS / Техническая документация",
        "source": "SRS-main/AUDIT_AS_IS.md",
        "tags": ["audit", "database", "PostgreSQL", "API", "architecture"],
    },
    {
        "slug": "business-model",
        "title": "Бизнес-модель и юнит-экономика",
        "desc": "Доходы, расходы, юнит-экономика, ценообразование, ключевые метрики дашборда. Реальные данные за фев–май 2026.",
        "category": "SRS / Техническая документация",
        "source": "SRS-main/business_model.md",
        "tags": ["business model", "unit economics", "pricing", "metrics"],
    },
    {
        "slug": "estimation",
        "title": "Оценка сроков разработки",
        "desc": "Оценка трудозатрат по всем бизнес-процессам, стоимость интеграций, распределение команды.",
        "category": "SRS / Техническая документация",
        "source": "SRS-main/ESTIMATION.md",
        "tags": ["estimation", "timeline", "effort", "planning"],
    },
    {
        "slug": "feature-map",
        "title": "Карта функциональных требований",
        "desc": "15 модулей, 80+ фич: полный список функций продукта с 6 интерактивными визуализациями — Treemap, Mindmap, таблица, Roadmap, Kanban, Force Graph.",
        "category": "SRS / Техническая документация",
        "type": "feature-viz",
        "tags": ["features", "mindmap", "requirements", "functional", "visualization"],
    },
    {
        "slug": "finops",
        "title": "FinOps — оптимизация расходов на инфраструктуру",
        "desc": "Стоимость инфраструктуры, оптимизация облачных расходов, бюджетирование и мониторинг затрат.",
        "category": "SRS / Техническая документация",
        "source": "SRS-main/finops.md",
        "tags": ["finops", "cloud", "costs", "infrastructure"],
    },
    {
        "slug": "otp-via-messengers",
        "title": "OTP-доставка через мессенджеры",
        "desc": "Спецификация доставки одноразовых кодов через Telegram, WhatsApp и другие мессенджеры.",
        "category": "SRS / Техническая документация",
        "source": "OTP_VIA_MESSENGERS.md",
        "tags": ["OTP", "messengers", "auth", "security"],
    },
    {
        "slug": "srs-docs",
        "title": "SRS Docs — опубликованная документация",
        "desc": "Полная SRS-документация в веб-формате: интерактивные визуализации, карта функций, mindmap, treemap и другие диаграммы требований.",
        "category": "SRS / Техническая документация",
        "url": "https://bestdeejay-design.github.io/srs-docs/",
        "tags": ["SRS", "docs", "published", "visualization"],
    },
    
    # ── Проектная документация ──
    {
        "slug": "vitrina",
        "title": "Платформа «Витрина»",
        "subtitle": "Технико-коммерческое описание",
        "desc": "Каталог электронной коммерции нового поколения: объединение розничных сетей, локальных магазинов и производителей.",
        "category": "Проектная документация",
        "source": "vitrina/Витрина_Проектный_документ.md",
        "tags": ["e-commerce", "marketplace", "platform", "retail"],
    },
    {
        "slug": "vitrina-context",
        "title": "Контекст проекта «Витрина»",
        "desc": "Краткий и подробный контекст проекта: цели, задачи, предпосылки, анализ рынка.",
        "category": "Проектная документация",
        "source": "vitrina/Подробный_контекст.md",
        "tags": ["context", "project", "market analysis"],
    },
    {
        "slug": "vitrina-plan",
        "title": "План реализации «Витрина» (W1–W12)",
        "desc": "Поэтапный план реализации платформы: 12 недель, 4 этапа, команда, бюджет, метрики успеха.",
        "category": "Проектная документация",
        "source": "vitrina/План_W1-W12_Полный.md",
        "tags": ["roadmap", "plan", "implementation", "weeks"],
    },
    {
        "slug": "vitrina-faq",
        "title": "FAQ проекта «Витрина»",
        "desc": "Часто задаваемые вопросы о платформе «Витрина»: бизнес-модель, конкуренты, технологии.",
        "category": "Проектная документация",
        "source": "vitrina/FAQ_Вопросы_и_ответы.md",
        "tags": ["faq", "questions", "answers", "vitrina"],
    },
    {
        "slug": "ambar-proposal",
        "title": "AMBAR — Фудтех-проект",
        "desc": "Концепция фудтех-проекта: инфраструктура для фудкорта, ИТ-решения, кухня, инвестиции.",
        "category": "Проектная документация",
        "source": "additional/ambar/ambar-proposal.md",
        "tags": ["foodtech", "foodcourt", "investment", "infrastructure"],
    },
    {
        "slug": "it-architecture-template",
        "title": "Шаблон проекта ИТ-архитектуры",
        "desc": "План реализации ИТ-архитектуры предприятия: 6 этапов от инициации до Go-Live. Подходит для любого проекта внедрения.",
        "category": "Проектная документация",
        "source": "Проект_ИТ_Архитектуры_Шаблон.pdf",
        "type": "pdf",
        "tags": ["IT architecture", "template", "implementation", "infrastructure"],
    },
    {
        "slug": "airport-restaurants",
        "title": "Драфт для общепита + аэропорт",
        "desc": "Техническое задание: PWA-приложение для заказа еды в ресторанах аэропорта. iiko, ЮKassa, три способа получения, 4 месяца разработки.",
        "category": "Проектная документация",
        "source": "airport_restaurants_tz.txt",
        "tags": ["foodtech", "airport", "PWA", "iiko", "delivery"],
    },

    # ── Юридическая документация ──
    {
        "slug": "yur-struktura-platformy",
        "title": "Юридическая структура финтех-платформы для фудкортов",
        "desc": "Полная юридическая модель: сплит-платежи 70/20/6.5, матрица из 5 договоров, 54-ФЗ, налоговые аспекты, риски.",
        "category": "Юридическая документация",
        "source": "Юридическая_структура_платформы.docx",
        "type": "docx",
        "tags": ["legal", "fintech", "split payments", "54-FZ", "tax"],
    },

    # ── API, БД и интеграции ──
    {
        "slug": "arbat38-api",
        "title": "API документация",
        "desc": "API endpoints, PROJECT_SUMMARY, схема базы данных.",
        "category": "API, БД и интеграции",
        "source": "additional/arbat38/API.md",
        "tags": ["API", "database", "documentation"],
        "process": "strip_h1",
    },
    {
        "slug": "ybase-tsp",
        "title": "Ybase TSP — документация",
        "desc": "Схема базы данных, парсеры, руководство по экспорту, PROJECT_OVERVIEW, PROJECT_STRUCTURE.",
        "category": "API, БД и интеграции",
        "source": "additional/ybase-tsp/PROJECT_OVERVIEW.md",
        "tags": ["database", "schema", "parser", "export", "tsp"],
    },
    {
        "slug": "napolipizza-guide",
        "title": "Napoli Pizza — проектная документация",
        "desc": "Полный набор документов: PROJECT_GUIDE, STRUCTURE, DEPLOY, QUICKSTART, DONE.",
        "category": "API, БД и интеграции",
        "source": "additional/napolipizza/PROJECT_GUIDE.md",
        "tags": ["pizza", "project", "guide", "deploy"],
    },

    # ── Референсы и исследования ──
    {
        "slug": "store-apis-research",
        "title": "Исследование API супермаркетов",
        "desc": "Анализ API и интеграционных возможностей федеральных сетей: Лента, METRO, ВкусВилл, Globus и других.",
        "category": "Референсы и исследования",
        "source": "references/github/store-apis-research.md",
        "tags": ["research", "API", "retail", "supermarkets", "integration"],
    },
    {
        "slug": "booking-docs",
        "title": "Grand Hotel — архитектура и документация",
        "desc": "Архитектура, модель данных, план имплементации и функциональные возможности системы бронирования отеля.",
        "category": "Референсы и исследования",
        "source": "additional/booking/architecture.md",
        "tags": ["booking", "hotel", "architecture", "data model"],
    },
    {
        "slug": "padl-docs",
        "title": "PadelPro — проектная документация",
        "desc": "Контекст проекта, features, design system, план демо — SAAS-платформа для управления падел-клубом.",
        "category": "Референсы и исследования",
        "source": "additional/padl/context_padelpro_project.txt",
        "tags": ["sports", "padel", "SAAS", "club management"],
    },
    {
        "slug": "blog-audit",
        "title": "Аудит и гайд по интеграции блога",
        "desc": "AUDIT_REPORT, INTEGRATION_GUIDE, MEDIA_GUIDE, SETUP — полная документация по системе блогов.",
        "category": "Референсы и исследования",
        "source": "additional/blog/AUDIT_REPORT.md",
        "tags": ["blog", "audit", "integration", "media", "setup"],
    },
    {
        "slug": "lovii-design-system",
        "title": "LOVII — Design System",
        "desc": "Дизайн-система платформы лояльности LOVII: компоненты, стили, промпты для генерации интерфейсов.",
        "category": "Референсы и исследования",
        "source": "additional/lovii_demo/design_system_prompt.md",
        "tags": ["design system", "LOVII", "loyalty", "UI", "components"],
    },
    {
        "slug": "univerid-concept",
        "title": "UniverID — концепция цифровой экосистемы университета",
        "desc": "Полная концепция: структура проекта, roadmap, договор, mind map. Цифровая экосистема для вузов.",
        "category": "Референсы и исследования",
        "source": "additional/univerid/",
        "tags": ["university", "ecosystem", "digital", "concept", "roadmap"],
    },
]

SITE_URL = "https://axiiom.ru"
OG_IMAGE = "https://axiiom.ru/og-image.png"

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def md_to_html(md_text):
    md_text = re.sub(r'[\U0001F300-\U0001F9FF\u2600-\u27BF]', '', md_text)
    extensions = ['extra', 'codehilite', 'toc', 'tables', 'fenced_code', 'sane_lists']
    html = markdown.markdown(md_text, extensions=extensions)
    return html

def page_template(title, desc, slug, content_html, breadcrumbs_extra=None):
    full_title = f"{title} | Документация AXIIOM"
    url = f"{SITE_URL}/docs/{slug}/"
    breadcrumbs = f'''<nav class="breadcrumbs" id="breadcrumbs" aria-label="Breadcrumb">
    <div class="container"><ol itemscope itemtype="https://schema.org/BreadcrumbList">
      <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
        <a itemprop="item" href="/"><span itemprop="name">Главная</span></a>
        <meta itemprop="position" content="1">
      </li>
      <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
        <a itemprop="item" href="/docs/"><span itemprop="name">Документация</span></a>
        <meta itemprop="position" content="2">
      </li>'''
    if breadcrumbs_extra:
        breadcrumbs += breadcrumbs_extra
    breadcrumbs += f'''
      <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
        <span itemprop="name">{title}</span>
        <meta itemprop="position" content="3">
      </li>
    </ol></div></nav>'''

    return f'''<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="theme-color" content="#0A0A0F">
    <title>{full_title}</title>
    <meta name="description" content="{desc}">
    <link rel="canonical" href="{url}">
    <link rel="icon" type="image/svg+xml" href="/favicon.svg">
    <meta property="og:type" content="article">
    <meta property="og:url" content="{url}">
    <meta property="og:title" content="{full_title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:image" content="{OG_IMAGE}">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:locale" content="ru_RU">
    <meta property="og:site_name" content="AXIIOM">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:url" content="{url}">
    <meta name="twitter:title" content="{full_title}">
    <meta name="twitter:description" content="{desc}">
    <meta name="twitter:image" content="{OG_IMAGE}">
    <script type="application/ld+json">{{"@context":"https://schema.org","@type":"TechArticle","headline":"{title}","description":"{desc}","url":"{url}","author":{{"@type":"Organization","name":"AXIIOM"}},"isPartOf":{{"@type":"WebSite","name":"AXIIOM","url":"{SITE_URL}"}}}}</script>
    <style>*{{margin:0;padding:0;box-sizing:border-box}}html{{font-size:16px;scroll-behavior:smooth}}body{{font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:1.0625rem;background:#0A0A0F;color:#C7C7CC;line-height:1.65;-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;overflow-x:hidden}}.noise{{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:9999;opacity:.025;background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E")}}.grid-overlay{{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0;background-image:linear-gradient(rgba(255,255,255,.06) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.06) 1px,transparent 1px);background-size:60px 60px}}.container{{max-width:1200px;margin:0 auto;padding:0 24px;position:relative;z-index:1}}.reveal{{opacity:0;transform:translateY(30px);transition:opacity .7s cubic-bezier(.22,1,.36,1),transform .7s cubic-bezier(.22,1,.36,1)}}.reveal.visible{{opacity:1;transform:translateY(0)}}</style>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="preload" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" as="style">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/styles.css">
    <link rel="stylesheet" href="/docs/styles.css">
</head>
<body>
<div class="noise"></div>
<div class="grid-overlay"></div>
<div class="nav-overlay" id="navOverlay">
    <ul class="nav-links" id="mobileNav"></ul>
</div>
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
<div class="nav-overlay" id="navOverlay">
    <ul class="nav-links" id="mobileNav"></ul>
</div>
{breadcrumbs}
<article class="docs-article">
    <div class="container">
        <div class="docs-content">
            {content_html}
        </div>
    </div>
</article>
<footer class="footer"><div class="container"><div id="footerCopy"></div></div></footer>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-HFS4BDGTV4"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','G-HFS4BDGTV4');</script>
<script src="/metrika.js"></script>
<script src="/config.js"></script>
<script src="/nav.js"></script>
<script>Nav.init({{breadcrumbs:false}});</script>
<script src="/theme.js"></script>
<script src="/preloader.js"></script>
<script>
(function(){{var r=document.querySelectorAll('.reveal');if(r.length){{var o=new IntersectionObserver(function(e){{e.forEach(function(e){{if(e.isIntersecting){{e.target.classList.add('visible')}}}})}},{{threshold:0.15}});for(var i=0;i<r.length;i++){{o.observe(r[i])}}}}}})();
</script>
<script>
(function(){{var t=document.getElementById('navToggle');var o=document.getElementById('navOverlay');if(!t||!o)return;t.addEventListener('click',function(e){{e.stopPropagation();o.classList.toggle('open');t.classList.toggle('active');document.body.style.overflow=o.classList.contains('open')?'hidden':''}})}})();
</script>
</body>
</html>'''

INDEX_HEAD = '''<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="theme-color" content="#0A0A0F">
    <title>Документация проектов | AXIIOM</title>
    <meta name="description" content="Документация проектов AXIIOM: SRS, юридическая документация, проектные документы, API-спецификации, исследования, визуализации.">
    <link rel="canonical" href="https://axiiom.ru/docs/">
    <link rel="icon" type="image/svg+xml" href="/favicon.svg">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://axiiom.ru/docs/">
    <meta property="og:title" content="Документация проектов | AXIIOM">
    <meta property="og:description" content="Документация проектов AXIIOM: SRS, юридическая документация, проектные документы, API-спецификации, исследования, визуализации.">
    <meta property="og:image" content="https://axiiom.ru/og-image.png">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:locale" content="ru_RU">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:url" content="https://axiiom.ru/docs/">
    <meta name="twitter:title" content="Документация проектов | AXIIOM">
    <meta name="twitter:description" content="Документация проектов AXIIOM: SRS, юридическая документация, проектные документы.">
    <meta name="twitter:image" content="https://axiiom.ru/og-image.png">
    <script type="application/ld+json">{"@context":"https://schema.org","@type":"CollectionPage","name":"Документация проектов AXIIOM","description":"Документация проектов AXIIOM: SRS, юридическая документация, проектные документы.","url":"https://axiiom.ru/docs/","isPartOf":{"@type":"WebSite","name":"AXIIOM","url":"https://axiiom.ru/"}}</script>
    <style>*{margin:0;padding:0;box-sizing:border-box}html{font-size:16px;scroll-behavior:smooth}body{font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:1.0625rem;background:#0A0A0F;color:#C7C7CC;line-height:1.65;-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;overflow-x:hidden}.noise{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:9999;opacity:.025;background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E")}.grid-overlay{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0;background-image:linear-gradient(rgba(255,255,255,.06) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.06) 1px,transparent 1px);background-size:60px 60px}.container{max-width:1200px;margin:0 auto;padding:0 24px;position:relative;z-index:1}</style>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="preload" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" as="style">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/styles.css">
    <link rel="stylesheet" href="/docs/styles.css">
</head>
<body>
<div class="noise"></div>
<div class="grid-overlay"></div>
<div class="nav-overlay" id="navOverlay">
    <ul class="nav-links" id="mobileNav"></ul>
</div>
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
<div class="nav-overlay" id="navOverlay">
    <ul class="nav-links" id="mobileNav"></ul>
</div>
<nav class="breadcrumbs" id="breadcrumbs" aria-label="Breadcrumb">
    <div class="container"><ol itemscope itemtype="https://schema.org/BreadcrumbList">
      <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
        <a itemprop="item" href="/"><span itemprop="name">Главная</span></a>
        <meta itemprop="position" content="1">
      </li>
      <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
        <span itemprop="name">Документация</span>
        <meta itemprop="position" content="2">
      </li>
    </ol></div>
</nav>
<section class="hero docs-hero">
    <div class="container">
        <div class="hero-content">
            <div class="hero-bg-svg"><svg width="800" height="600" viewBox="0 0 800 600" fill="none">
  <rect x="60" y="40" width="80" height="80" rx="10" stroke="rgba(255,255,255,0.3)" stroke-width="2" fill="none" transform="rotate(-5 100 80)"/>
  <rect x="540" y="30" width="90" height="90" rx="10" stroke="rgba(255,255,255,0.25)" stroke-width="2" fill="none" transform="rotate(10 585 75)"/>
  <rect x="40" y="450" width="85" height="85" rx="10" stroke="rgba(255,255,255,0.28)" stroke-width="2" fill="none" transform="rotate(-8 82 492)"/>
  <rect x="620" y="470" width="75" height="75" rx="10" stroke="rgba(255,255,255,0.32)" stroke-width="2" fill="none" transform="rotate(12 657 507)"/>
  <rect x="250" y="80" width="30" height="30" rx="5" stroke="rgba(255,255,255,0.15)" stroke-width="2" fill="none" transform="rotate(45 265 95)"/>
  <rect x="520" y="280" width="25" height="25" rx="4" stroke="rgba(255,255,255,0.12)" stroke-width="2" fill="none" transform="rotate(-30 532 292)"/>
  <rect x="260" y="480" width="28" height="28" rx="4" stroke="rgba(255,255,255,0.14)" stroke-width="2" fill="none" transform="rotate(20 274 494)"/>
  <circle cx="400" cy="300" r="3" fill="none" stroke="rgba(255,255,255,0.2)" stroke-width="2"/>
  <circle cx="400" cy="300" r="140" stroke="rgba(255,255,255,0.1)" stroke-width="1.5" fill="none"/>
  <circle cx="400" cy="300" r="220" stroke="rgba(255,255,255,0.06)" stroke-width="1.5" fill="none"/>
  <line x1="100" y1="80" x2="700" y2="520" stroke="rgba(255,255,255,0.06)" stroke-width="1.5"/>
  <line x1="700" y1="80" x2="100" y2="520" stroke="rgba(255,255,255,0.06)" stroke-width="1.5"/>
  <circle cx="140" cy="180" r="3" fill="none" stroke="rgba(255,255,255,0.15)" stroke-width="1.5"/>
  <circle cx="660" cy="420" r="4" fill="none" stroke="rgba(255,255,255,0.12)" stroke-width="1.5"/>
  <circle cx="300" cy="520" r="2" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="1.5"/>
  <circle cx="500" cy="80" r="3" fill="none" stroke="rgba(255,255,255,0.12)" stroke-width="1.5"/>
</svg></div>
            <div class="badge-row">
                <p class="badge">Документация</p>
            </div>
            <h1>Примеры документов AXIIOM</h1>
            <p class="hero-desc">Спецификации, юридическая документация, проектные документы, API-гайды, исследования и визуализации — всё в одном месте.</p>
        </div>
    </div>
</section>
<section class="section">
    <div class="container">
'''

INDEX_TAIL = '''
    </div>
</section>
<footer class="footer"><div class="container"><div id="footerCopy"></div></div></footer>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-HFS4BDGTV4"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}gtag('js',new Date());gtag('config','G-HFS4BDGTV4');</script>
<script src="/metrika.js"></script>
<script src="/config.js"></script>
<script src="/nav.js"></script>
<script>Nav.init({breadcrumbs:false});</script>
<script src="/theme.js"></script>
<script src="/preloader.js"></script>
<script>
(function(){var r=document.querySelectorAll('.reveal');if(r.length){var o=new IntersectionObserver(function(e){e.forEach(function(e){if(e.isIntersecting){e.target.classList.add('visible')}})},{threshold:0.15});r.forEach(function(e){o.observe(e)})}})();
</script>
<script>
(function(){var t=document.getElementById('navToggle');var o=document.getElementById('navOverlay');if(!t||!o)return;t.addEventListener('click',function(e){e.stopPropagation();o.classList.toggle('open');t.classList.toggle('active');document.body.style.overflow=o.classList.contains('open')?'hidden':''})})();
</script>
</body>
</html>'''

_S = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">'

CATEGORY_ICONS = {
    "SRS": _S + '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>',
    "Проектная": _S + '<path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>',
    "Юридическая": _S + '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
    "API": _S + '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33"/><path d="M4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 8.92 4.6"/><path d="M12 3v3"/><path d="M12 18v3"/><path d="M3 12h3"/><path d="M18 12h3"/></svg>',
    "Референсы": _S + '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
}

def category_icon(cat):
    for key, icon in CATEGORY_ICONS.items():
        if key in cat:
            return icon
    return _S + '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>'

def clean_html_title(md_source):
    lines = md_source.split('\n')
    for line in lines:
        if line.startswith('# '):
            return line[2:].strip()
    return ''

def generate_index():
    sections = {}
    for doc in DOCS:
        cat = doc["category"]
        if cat not in sections:
            sections[cat] = []
        sections[cat].append(doc)

    html = INDEX_HEAD
    for cat, docs in sections.items():
        html += f'''<h2 class="reveal index-section-title">{category_icon(cat)}<span>{cat}</span></h2>
            <div class="tools-grid">'''
        for doc in docs:
            doc_url = doc.get("url", f'/docs/{doc["slug"]}/')
            dtype = doc.get("type", "md")
            if dtype == "pdf":
                icon_svg = '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M14 3v4a1 1 0 001 1h4"/><path d="M17 21H7a2 2 0 01-2-2V5a2 2 0 012-2h7l5 5v11a2 2 0 01-2 2z"/><rect x="9" y="13" width="6" height="5" rx="1"/><path d="M11 13v-1a1 1 0 012 0v1"/></svg>'
            elif dtype == "docx":
                icon_svg = '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M14 3v4a1 1 0 001 1h4"/><path d="M17 21H7a2 2 0 01-2-2V5a2 2 0 012-2h7l5 5v11a2 2 0 01-2 2z"/><line x1="12" y1="11" x2="12" y2="17"/><line x1="9" y1="14" x2="15" y2="14"/></svg>'
            else:
                icon_svg = '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M14 3v4a1 1 0 001 1h4"/><path d="M17 21H7a2 2 0 01-2-2V5a2 2 0 012-2h7l5 5v11a2 2 0 01-2 2z"/><line x1="9" y1="12" x2="15" y2="12"/><line x1="9" y1="16" x2="13" y2="16"/></svg>'
            html += f'''<a href="{doc_url}" class="tool-card blog-card reveal"{' target="_blank"' if doc.get("url") else ''}>
                <div class="tool-icon">{icon_svg}</div>
                <h3>{doc["title"]}</h3>
                <p>{doc["desc"][:180]}{"…" if len(doc["desc"]) > 180 else ""}</p>
                <span class="blog-read">{"Открыть" if doc.get("url") else "Открыть"} →</span>
            </a>'''
        html += '</div>'
    # Blog articles section at bottom
    blog_articles = [
        ("Архитектура highload-систем", "Принципы построения отказоустойчивых highload-систем: балансировка, кэширование, шардирование, CQRS, Event Sourcing.", "/blog/highload-architecture/"),
        ("PCI DSS Compliance", "Полное руководство по соответствию стандарту PCI DSS для стартапов и платёжных систем: требования, аудит, сертификация.", "/blog/pci-dss-compliance/"),
        ("Тренды финтеха 2026", "Главные тренды финтех-индустрии 2026: Embedded Finance, Open Banking, DeFi, CBDC, AI в финансовых услугах.", "/blog/fintech-trends-2026/"),
        ("ROI платформы лояльности", "Расчёт окупаемости внедрения платформы лояльности: метрики, кейсы, сроки возврата инвестиций.", "/blog/loyalty-program-roi/"),
        ("161-ФЗ: руководство для стартапов", "Как соответствовать 161-ФЗ «О национальной платёжной системе»: требования, санкции, пошаговый план внедрения.", "/blog/161-fz-guideline/"),
        ("UX платёжных мобильных приложений", "Лучшие практики UX/UI для платёжных приложений: безопасность, конверсия, доступность, анимации.", "/blog/mobile-payment-ux/"),
        ("Платформа лояльности — необходимость", "Почему программа лояльности — must-have для e-commerce: анализ рынка, ARPU, LTV, retention.", "/blog/loyalty-platform-not-option-necessity/"),
    ]
    html += f'''<h2 class="reveal index-section-title">{_S}<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg><span>Статьи</span></h2>
        <div class="tools-grid">'''
    for title, desc, link in blog_articles:
        html += f'''<a href="{link}" class="tool-card blog-card reveal">
            <div class="tool-icon"><svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M14 3v4a1 1 0 001 1h4"/><path d="M17 21H7a2 2 0 01-2-2V5a2 2 0 012-2h7l5 5v11a2 2 0 01-2 2z"/><line x1="9" y1="12" x2="15" y2="12"/><line x1="9" y1="16" x2="13" y2="16"/></svg></div>
            <h3>{title}</h3>
            <p>{desc}</p>
            <span class="blog-read">Читать →</span>
        </a>'''
    html += '</div>'
    html += INDEX_TAIL
    return html

def _add_sub_headings(text):
    """Convert plain section labels in roadmap to markdown headings."""
    headings = [
        'ЭТАПЫ И РЕЗУЛЬТАТЫ РАБОТ',
        'КЛЮЧЕВЫЕ ВЕХИ',
        'ОЖИДАЕМЫЕ РЕЗУЛЬТАТЫ',
        'ДОПУЩЕНИЯ И РИСКИ',
    ]
    lines = text.split('\n')
    for i, line in enumerate(lines):
        stripped = line.strip().rstrip(':')
        if any(stripped.startswith(h) for h in headings):
            lines[i] = '## ' + line.strip()
    return '\n'.join(lines)

def _add_md_headings(text):
    """Add ## to section headings in flat listing like UniveriD.md."""
    lines = text.split('\n')
    out = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            out.append(line)
            continue
        if line.startswith(('- ', '* ', '+ ', '#')):
            out.append(line)
            continue
        # Look ahead to see if next non-blank line is a list item
        is_section = False
        for j in range(i + 1, min(i + 3, len(lines))):
            nxt = lines[j]
            if not nxt:
                continue
            if nxt.startswith('- '):
                is_section = True
            break
        if out and out[-1].startswith('- ') and line[0].islower():
            out[-1] += ' ' + line
        elif is_section:
            out.append('## ' + line)
        else:
            out.append(line)
    return '\n'.join(out)

def build_page(doc):
    slug = doc["slug"]
    title = doc["title"]
    desc = doc["desc"]
    dtype = doc.get("type", "md")
    src = doc.get("source", "")

    out_dir = os.path.join(OUT, slug)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "index.html")

    if dtype == "pdf":
        src_path = os.path.join(SRC, src)
        dst = os.path.join(OUT, slug, os.path.basename(src))
        if os.path.exists(src_path):
            shutil.copy2(src_path, dst)

        # Extract text from PDF for rich content page
        phases_html = ""
        try:
            import fitz
            pdf_doc = fitz.open(src_path)
            text = ""
            for page in pdf_doc:
                text += page.get_text() + "\n"
            pdf_doc.close()

            # Find phase headings in page order (skip TOC pages)
            phases = []
            seen_headings = set()
            lines = text.split('\n')
            i = 0
            while i < len(lines):
                line = lines[i].strip()
                # Real content heading: "Этап N: Title" (not "N.  Этап" from TOC)
                if re.match(r'^Этап\s+\d+:', line) and not re.match(r'^\d+\.[\s.]*Этап', line):
                    heading = line
                    i += 1
                    # Collect continuation lines (until we hit a known category or numbered item)
                    while i < len(lines):
                        nxt = lines[i].strip()
                        if not nxt:
                            i += 1
                            continue
                        if re.match(r'^\d+\.', nxt) or nxt.startswith('Деятельность'):
                            break
                        if re.match(r'^[А-Я][а-я]+:', nxt) and nxt.split(':')[0] in ('Цель', 'Результат'):
                            break
                        heading += ' ' + nxt
                        i += 1
                    heading = re.sub(r'\s+', ' ', heading).strip()
                    # Skip if we already processed this heading (TOC duplicate)
                    norm = heading.lower().split(':')[0].strip() if ':' in heading else heading.lower()
                    if norm in seen_headings:
                        continue
                    seen_headings.add(norm)
                    # Collect body
                    body_lines = []
                    while i < len(lines):
                        nxt = lines[i].strip()
                        if re.match(r'^Этап\s+\d+:', nxt) and not re.match(r'^\d+\.[\s.]*Этап', nxt):
                            break
                        body_lines.append(lines[i])
                        i += 1
                    phases.append((heading, '\n'.join(body_lines)))
                else:
                    i += 1

            for heading, body in phases:
                phase_match = re.match(r'Этап\s+(\d+):\s*(.*)', heading)
                if phase_match:
                    phase_num = phase_match.group(1)
                    phase_title = phase_match.group(2).strip()
                else:
                    phase_num = ""
                    phase_title = heading

                phase_num_str = f"0{phase_num}" if phase_num and int(phase_num) < 10 else phase_num

                # Split body into sections and results
                sections = []
                results = []
                current_section = []
                in_results = False
                for line in body.split('\n'):
                    line = line.strip()
                    if not line:
                        continue
                    if 'Результат' in line and ('Этап' in line or ':' in line[:30]):
                        in_results = True
                        if current_section:
                            sections.append('\n'.join(current_section))
                            current_section = []
                        results.append(line)
                        continue
                    if in_results and re.match(r'^[А-Я]', line):
                        # Check if this is a new section (uppercase start after results)
                        pass
                    if in_results:
                        results.append(line)
                        continue
                    current_section.append(line)
                if current_section:
                    sections.append('\n'.join(current_section))

                phase_html = f'''<div class="feature-module">
                    <h2 class="feature-module-title">Этап {phase_num_str}: {phase_title}</h2>'''
                for sec_text in sections:
                    formatted = re.sub(r'^(\d+(?:\.\d+)*)\s*\.\s*', r'<strong>\1.</strong> ', sec_text, flags=re.MULTILINE)
                    formatted = re.sub(r'\n+', '<br>', formatted)
                    formatted = re.sub(r'\s*-\s+', '<br>— ', formatted)
                    phase_html += f'<p>{formatted}</p>'
                if results:
                    phase_html += '<div class="doc-results">'
                    for r in results:
                        r_formatted = re.sub(r'^(\d+(?:\.\d+)*)\s*\.\s*', r'<strong>\1.</strong> ', r)
                        r_formatted = re.sub(r'\s*-\s+', '<br>— ', r_formatted)
                        phase_html += f'<p>{r_formatted}</p>'
                    phase_html += '</div>'
                phase_html += '</div>'
                phases_html += phase_html

        except ImportError:
            phases_html = f"<p>{desc}</p>"
        except Exception as e:
            phases_html = f"<p>{desc}</p>"

        disclaimer = '''<div class="doc-disclaimer">
            <p>Данный документ является демонстрационным шаблоном и <strong>не является официальной проектной документацией</strong>. Материал иллюстрирует структуру и состав разделов, которые рекомендуется учитывать при разработке ИТ-архитектуры. Для получения полной версии шаблона или консультации по вашему проекту обращайтесь:</p>
            <p><a href="mailto:admin@axiiom.ru">admin@axiiom.ru</a>&nbsp;|&nbsp;<a href="https://axiiom.ru">axiiom.ru</a></p>
        </div>'''

        content = f'''<div class="feature-page-hero">
            <h1>{title}</h1>
            <p>{desc}</p>
            <div class="doc-actions">
                <a href="{os.path.basename(src)}" class="btn" download>Скачать PDF</a>
                <a href="/docs/" class="btn btn-outline">← Все документы</a>
            </div>
        </div>
        {phases_html}
        {disclaimer}'''
        page = page_template(title, desc, slug, content)
        write_file(out_path, page)
        return

    if dtype == "docx":
        src_path = os.path.join(SRC, src)
        dst = os.path.join(OUT, slug, os.path.basename(src))
        if os.path.exists(src_path):
            shutil.copy2(src_path, dst)

        content_html = ""
        try:
            from docx import Document as DocxDoc
            d = DocxDoc(src_path)
            in_list = False
            for p in d.paragraphs:
                txt = p.text.strip()
                if not txt:
                    if in_list:
                        content_html += '</ul>'
                        in_list = False
                    continue
                style = p.style.name if p.style else ""
                if 'Heading 1' in style:
                    if in_list:
                        content_html += '</ul>'
                        in_list = False
                    content_html += f'<h2>{txt}</h2>'
                elif 'Heading 2' in style:
                    if in_list:
                        content_html += '</ul>'
                        in_list = False
                    content_html += f'<h3>{txt}</h3>'
                elif 'Heading 3' in style:
                    if in_list:
                        content_html += '</ul>'
                        in_list = False
                    content_html += f'<h4>{txt}</h4>'
                elif 'List' in style or txt.startswith('- ') or txt.startswith('• '):
                    if not in_list:
                        content_html += '<ul>'
                        in_list = True
                    item = txt.lstrip('- •').strip()
                    content_html += f'<li>{item}</li>'
                else:
                    if in_list:
                        content_html += '</ul>'
                        in_list = False
                    content_html += f'<p>{txt}</p>'
            if in_list:
                content_html += '</ul>'
        except ImportError:
            content_html = f"<p>{desc}</p>"
        except Exception as e:
            content_html = f"<p>{desc}</p>"

        disclaimer = '''<div class="doc-disclaimer">
            <p>Данный документ является демонстрационным шаблоном и <strong>не является официальной проектной документацией</strong>. Материал приведён в ознакомительных целях и не может использоваться в качестве юридической консультации. Для получения полной версии документа или консультации по вашему проекту обращайтесь:</p>
            <p><a href="mailto:admin@axiiom.ru">admin@axiiom.ru</a>&nbsp;|&nbsp;<a href="https://axiiom.ru">axiiom.ru</a></p>
        </div>'''

        content = f'''<div class="feature-page-hero">
            <h1>{title}</h1>
            <p>{desc}</p>
            <div class="doc-actions">
                <a href="{os.path.basename(src)}" class="btn" download>Скачать DOCX</a>
                <a href="/docs/" class="btn btn-outline">← Все документы</a>
            </div>
        </div>
        {content_html}
        {disclaimer}'''
        page = page_template(title, desc, slug, content)
        write_file(out_path, page)
        return

    if dtype == "feature-viz":
        BASE = "https://bestdeejay-design.github.io/srs-docs/visualizations"
        SVG_BASE = '<svg width="32" height="32" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">'
        icons = {
            "Treemap": SVG_BASE + '<rect x="3" y="3" width="12" height="12" rx="1"/><rect x="17" y="3" width="12" height="6" rx="1"/><rect x="17" y="11" width="12" height="4" rx="1"/><rect x="3" y="17" width="8" height="12" rx="1"/><rect x="13" y="17" width="16" height="5" rx="1"/><rect x="13" y="24" width="7" height="5" rx="1"/><rect x="22" y="24" width="7" height="5" rx="1"/></svg>',
            "Mindmap": SVG_BASE + '<circle cx="16" cy="6" r="3"/><circle cx="6" cy="18" r="2.5"/><circle cx="16" cy="26" r="2.5"/><circle cx="26" cy="18" r="2.5"/><line x1="14" y1="8.5" x2="8" y2="16"/><line x1="16" y1="9" x2="16" y2="23"/><line x1="18" y1="8.5" x2="24" y2="16"/></svg>',
            "Таблица": SVG_BASE + '<rect x="3" y="3" width="26" height="26" rx="2"/><line x1="3" y1="10" x2="29" y2="10"/><line x1="12" y1="3" x2="12" y2="29"/><line x1="20" y1="3" x2="20" y2="29"/><rect x="4" y="4" width="9" height="5" rx="1" fill="currentColor" opacity=".15"/><rect x="13" y="4" width="8" height="5" rx="1" fill="currentColor" opacity=".15"/><rect x="21" y="4" width="7" height="5" rx="1" fill="currentColor" opacity=".15"/></svg>',
            "Roadmap": SVG_BASE + '<line x1="4" y1="16" x2="28" y2="16"/><circle cx="8" cy="16" r="3" fill="currentColor"/><circle cx="16" cy="16" r="3" fill="currentColor"/><circle cx="24" cy="16" r="3" fill="currentColor"/><polyline points="26,12 30,16 26,20" stroke-width="2"/></svg>',
            "Kanban": SVG_BASE + '<rect x="3" y="3" width="8" height="26" rx="1.5"/><rect x="12" y="3" width="8" height="26" rx="1.5"/><rect x="21" y="3" width="8" height="26" rx="1.5"/><rect x="5" y="6" width="4" height="2" rx=".5" fill="currentColor" opacity=".2"/><rect x="14" y="6" width="4" height="2" rx=".5" fill="currentColor" opacity=".2"/><rect x="23" y="6" width="4" height="2" rx=".5" fill="currentColor" opacity=".2"/><rect x="5" y="10" width="4" height="3" rx=".5" fill="currentColor" opacity=".12"/><rect x="14" y="10" width="4" height="4" rx=".5" fill="currentColor" opacity=".12"/><rect x="23" y="10" width="4" height="2" rx=".5" fill="currentColor" opacity=".12"/></svg>',
            "Force Graph": SVG_BASE + '<circle cx="10" cy="8" r="3" fill="currentColor" opacity=".8"/><circle cx="22" cy="10" r="2.5" fill="currentColor" opacity=".8"/><circle cx="16" cy="20" r="2" fill="currentColor" opacity=".8"/><circle cx="6" cy="24" r="1.5" fill="currentColor" opacity=".8"/><circle cx="26" cy="22" r="2" fill="currentColor" opacity=".8"/><line x1="12.5" y1="10" x2="20" y2="11.5"/><line x1="17" y1="18.5" x2="14" y2="11"/><line x1="8" y1="22" x2="7" y2="10"/><line x1="21" y1="12" x2="24.5" y2="20.5"/><line x1="12.5" y1="18" x2="14.5" y2="22.5"/><line x1="24.5" y1="12" x2="17" y2="20.5"/></svg>',
        }
        vizz = [
            ("02-treemap.html", "Treemap", "Прямоугольное дерево. Размер прямоугольника = количество фич. Сравнение объёмов модулей.", "D3.js"),
            ("03-mindmap.html", "Mindmap", "Майнд-карта от центра. Привычный формат для мозговых штурмов и презентаций. Zoom + pan.", "D3.js"),
            ("04-table.html", "Таблица", "Структурированный список: модули, фичи, описания, приоритеты. Поиск, сортировка, фильтрация.", "HTML/CSS"),
            ("05-roadmap.html", "Roadmap", "Дорожная карта по фазам: MVP → V2 → V3 → Future. Понятно, что и когда делать.", "HTML/CSS"),
            ("06-kanban.html", "Kanban", "Доска с drag-n-drop: Backlog → To Do → In Progress → Done. Для командной работы над задачами.", "HTML5 Drag & Drop"),
            ("07-force-graph.html", "Force Graph", "Силовой граф. Связи между модулями и фичами. Показывает зависимости и пересечения.", "D3.js Force"),
        ]
        viz_cards = ""
        for fname, name, desc_v, tag in vizz:
            svg = icons.get(name, "")
            viz_cards += f'''<a href="{BASE}/{fname}" class="tool-card blog-card reveal" target="_blank">
                <div class="tool-icon">{svg}</div>
                <h3>{name}</h3>
                <p>{desc_v}</p>
                <span class="viz-tag">{tag}</span>
            </a>'''

        features = [
            ("Регистрация и безопасность", [
                "Вход по телефону", "SMS-подтверждение",
                "Роли: клиент/пикер/курьер/админ/суперадмин",
                "JWT access + refresh токены", "Rate limiting", "Audit log"]),
            ("Каталог", [
                "Выбор магазина по адресу", "Категории (3 уровня)",
                "Поиск (Elasticsearch)", "Динамические фильтры (по категории)",
                "Карточка товара", "Нормализация данных сетей",
                "Маппинг категорий сети → платформа",
                "Адаптеры сетей (Лента, METRO, Вкусвилл и др.)",
                "Синхронизация цен/остатков (шедулер)"]),
            ("Корзина", [
                "Добавление товаров", "Промокоды и баллы",
                "Dynamic Pricing (надбавка за время/погоду/загрузку)",
                "Пересчёт стоимости", "Оформление"]),
            ("Заказы", [
                "Создание",
                "Статусы (оплачен → сборка → доставка → завершён)",
                "Добавление товаров после оформления", "История",
                "Замена товара (пикер → звонок → альтернатива)",
                "Возврат и отмена (до/после сборки, комиссия)",
                "Event Sourcing (цепочка событий заказа)"]),
            ("Доставка", [
                "Временные слоты (3 дня вперёд)",
                "Dispatch (multi-objective optimization)",
                "ETA (OSRM + ML гибрид)", "Трекинг для клиента",
                "Опция «Можно раньше»"]),
            ("Платежи", [
                "Т-Банк (онлайн, 3DSecure)", "СБП (QR от курьера)",
                "Карта курьеру (POS-терминал)", "Наличные",
                "Refund (полный/частичный)", "Чек (54-ФЗ, ОФД)"]),
            ("Уведомления", [
                "Push (FCM)", "SMS", "Email", "Telegram",
                "События: заказ создан, сборка начата, курьер выехал, доставлен"]),
            ("Админка", [
                "Управление заказами (CRUD, статусы, комментарии)",
                "Управление товарами (CRUD, импорт/экспорт CSV)",
                "Пользователи (блокировка, роли)", "Промокоды (создание, статистика)",
                "Курьеры и пикеры (зоны, рейтинг)",
                "Магазины и зоны доставки (полигоны)",
                "Управление сетями-адаптерами (вкл/выкл)",
                "Audit log (кто, когда, что сделал)"]),
            ("B2B", [
                "Корпоративные заказы в офис",
                "Регулярные поставки (ежедневно/еженедельно)",
                "Индивидуальные цены по договору",
                "Отсрочка платежа (3–30 дней)",
                "ЭДО (Диадок / СБИС, УПД)",
                "Счета и закрывающие документы"]),
            ("Dynamic Pricing", [
                "Факторы: загрузка курьеров, время, погода, расстояние, вес",
                "Формула: base_fee × product(multipliers)",
                "Max надбавка: 2×",
                "Отображение в корзине до подтверждения"]),
            ("Приложение пикера", [
                "Список заказов (FIFO)", "Сканер штрихкодов (Scandit)",
                "Замены товаров (поиск альтернатив)",
                "Звонок клиенту (скрытый номер)",
                "Offline-режим (Firestore cache)",
                "Smart Sync Queue (batch upload)",
                "Подтверждение упаковки"]),
            ("Приложение курьера", [
                "Навигация с multi-stop маршрутом",
                "Offline-режим (Hive + Smart Sync)",
                "Off-route detection (визуальный + звуковой алерт)",
                "Приём оплаты (офлайн hold → sync)",
                "Digital Signature (POD)", "Photo POD", "Сканер",
                "Статусы доставки"]),
            ("Инфраструктура", [
                "CI/CD (GitHub Actions, testcontainers)",
                "Docker Compose → Kubernetes",
                "Мониторинг (Prometheus + Grafana + Loki + Jaeger)",
                "Sentry (error tracking)",
                "Feature flags (Flipper / LaunchDarkly)",
                "Rollback (git revert + rolling update)"]),
            ("Тестирование", [
                "Unit (mockery + testify)",
                "Integration (testcontainers)",
                "Contract (Pact CDC)", "E2E (Cypress + K6)",
                "Load (K6: stress, soak, spike)",
                "Security (SonarCloud + Trivy + Aikido)"]),
            ("Аналитика", [
                "Дашборды (Grafana)",
                "Отчёты (выручка, заказы, конверсия)",
                "Метрики (DAU/MAU, время сборки, ETA, топ товаров)"]),
        ]

        feat_html = ""
        for mod_name, items in features:
            badges = ""
            for item in items:
                badges += f'<span class="feature-badge">{item}</span>'
            feat_html += f'''<div class="feature-module reveal">
                <h3 class="feature-module-title">{mod_name}</h3>
                <div class="feature-badges">{badges}</div>
            </div>'''

        content = f'''<div class="feature-page-hero">
    <h1>{title}</h1>
    <p>15 модулей, 80+ функций — полная карта продукта. Ниже — интерактивные визуализации в 6 форматах.</p>
    <div class="tools-grid">{viz_cards}</div>
    <div class="viz-section">
        <h2>Список всех функций</h2>
        <p>15 модулей, каждый со своим набором возможностей.</p>
        {feat_html}
    </div>
    <a href="/docs/" class="btn btn-outline back-link">← Все документы</a>
</div>'''
        page = page_template(title, desc, slug, content)
        write_file(out_path, page)
        print(f"  OK: /docs/{slug}/ (feature-viz)")
        return

    if src.endswith('/') or os.path.isdir(os.path.join(SRC, src.rstrip('/'))):
        base = src.rstrip('/')
        dir_path = os.path.join(SRC, base)

        # For concept directories with markdown content, render merged page
        if slug in ('univerid-concept',):
            md_keep = [
                ('UniveriD.md', 'Функциональная спецификация'),
                ('СТРУКТУРА-ПРОЕКТА.md', 'Структура проекта'),
                ('roadmap-univerid.md', 'Дорожная карта'),
            ]
            md_files = []
            pdf_files = []
            for fname, _ in md_keep:
                fp = os.path.join(dir_path, fname)
                if os.path.exists(fp):
                    md_files.append((fname, fp))
            for f in sorted(os.listdir(dir_path)):
                if f.endswith('.pdf'):
                    pdf_files.append(f)

            merged = ""
            for fname, label in md_keep:
                fp = os.path.join(dir_path, fname)
                if not os.path.exists(fp):
                    continue
                with open(fp, 'r', encoding='utf-8', errors='replace') as fh:
                    raw = fh.read()
                # Strip contract header and signatures
                raw = raw.rsplit('\nПОДПИСИ СТОРОН:', 1)[0]
                if fname == 'roadmap-univerid.md':
                    ta = raw.find('ЭТАПЫ И РЕЗУЛЬТАТЫ РАБОТ')
                    if ta != -1:
                        raw = raw[ta:]
                if fname == 'UniveriD.md':
                    # Strip redundant branding header (lines 1-6)
                    raw = '\n'.join(raw.split('\n')[6:])
                    raw = _add_md_headings(raw)
                if fname == 'СТРУКТУРА-ПРОЕКТА.md':
                    raw = re.sub(r'[\U0001F300-\U0001F9FF\u2600-\u27BF]', '', raw)
                    # Remove the inner h1 heading (duplicated by feature-module title)
                    raw = re.sub(r'^# .*', '', raw, flags=re.MULTILINE)
                    raw = raw.lstrip('\n')
                if fname == 'roadmap-univerid.md':
                    raw = _add_sub_headings(raw)
                html_content = markdown.markdown(raw, extensions=['fenced_code', 'codehilite', 'tables'])
                # Add human-readable IDs to h2 tags
                html_content = re.sub(
                    r'<h2>(.*?)</h2>',
                    lambda m: f'<h2 id="{slugify(m.group(1))}">{m.group(1)}</h2>',
                    html_content
                )
                merged += f'<div class="feature-module"><h2 class="feature-module-title" id="section-{slugify(label)}">{label}</h2>{html_content}</div>\n'

                pdf_labels = {
                    'UniveriD.pdf': 'Спецификация UniveriD',
                    'ЦИФРОВАЯ_ЭКОСИСТЕМА_УНИВЕРСИТЕТА_—_MIND_MAP.pdf': 'Mind Map',
                }
                pdf_links = ""
                for pf in pdf_files:
                    rel = os.path.join(src.rstrip('/'), pf)
                    label = pdf_labels.get(pf, pf.rsplit('.', 1)[0])
                    pdf_links += f'<a href="/docs/source/{rel}" class="btn" download>{label}</a>'
                presentation_link = '<a href="https://univerid.ru/quest.html" class="btn" target="_blank">Презентация проекта</a>'

            # Build TOC from h2 headings, excluding granular technical items
            toc_items = re.findall(r'<h2[^>]*id="([^"]*)"[^>]*>(.*?)</h2>', merged)
            toc_filtered = []
            skip_labels = {'ДАННЫЕ appData (полный список)', 'ФАЙЛЫ ПРОЕКТА', 'СТАТУС РАЗРАБОТКИ'}
            for id_, text in toc_items:
                clean = re.sub(r'<[^>]+>', '', text).strip()
                if clean in skip_labels or re.match(r'^\d+[\.\s]', clean):
                    continue
                toc_filtered.append((id_, clean))
            toc_html = ''
            if toc_filtered:
                toc_html = '<nav class="doc-toc"><ul>'
                for id_, clean in toc_filtered:
                    toc_html += f'<li><a href="#{id_}">{clean}</a></li>'
                toc_html += '</ul></nav>'

            disclaimer = '''<div class="doc-disclaimer">
                <p>Данный документ является демонстрационным материалом и <strong>не является официальной проектной документацией</strong>. Материал иллюстрирует структуру и состав концепции цифровой экосистемы университета. Для получения полной версии или консультации по вашему проекту обращайтесь:</p>
                <p><a href="mailto:admin@axiiom.ru">admin@axiiom.ru</a>&nbsp;|&nbsp;<a href="https://axiiom.ru">axiiom.ru</a></p>
            </div>'''

            content = f'''<div class="feature-page-hero">
                <h1>{title}</h1>
                <p>{desc}</p>
                <div class="doc-actions">{pdf_links}{presentation_link}
                    <a href="/docs/" class="btn btn-outline">← Все документы</a>
                </div>
            </div>
            {toc_html}
            {merged}
            {disclaimer}'''
            page = page_template(title, desc, slug, content)
            write_file(out_path, page)
            print(f"  OK: /docs/{slug}/ (merged directory)")
            return

        files = []
        if os.path.isdir(dir_path):
            for f in sorted(os.listdir(dir_path)):
                if f.endswith(('.md', '.txt', '.sql', '.docx', '.pdf', '.html')):
                    rel = os.path.join(src.rstrip('/'), f)
                    files.append((f, rel))
        items = []
        for fname, rel in files:
            items.append(f'<li><a href="/docs/source/{rel}" target="_blank">{fname}</a></li>')
        content = f'''<div class="doc-dir">
            <h1>{title}</h1>
            <p>{desc}</p>
            <ul>{"".join(items)}</ul>
            <a href="/docs/" class="btn btn-outline">← Все документы</a>
        </div>'''
        page = page_template(title, desc, slug, content)
        write_file(out_path, page)
        return

    if dtype == "html":
        dst = os.path.join(OUT, slug, os.path.basename(src))
        os.makedirs(os.path.join(OUT, slug), exist_ok=True)
        if os.path.exists(os.path.join(SRC, src)):
            shutil.copy2(os.path.join(SRC, src), dst)
        content = f'''<div class="doc-download">
            <div class="doc-download-inner">
                <h1>{title}</h1>
                <p class="doc-download-desc">{desc}</p>
                <a href="{os.path.basename(src)}" class="btn" target="_blank">Открыть визуализацию</a>
                <a href="/docs/" class="btn btn-outline">← Все документы</a>
            </div>
        </div>'''
        page = page_template(title, desc, slug, content)
        write_file(out_path, page)
        print(f"  OK: /docs/{slug}/")
        return

    src_path = os.path.join(SRC, src)
    if not os.path.exists(src_path):
        print(f"  SKIP (not found): {src}")
        return

    if src.endswith('.txt'):
        text_content = read_file(src_path)
        text_content = re.sub(r'[\U0001F300-\U0001F9FF\u2600-\u27BF]', '', text_content)
        content = f'<div class="feature-page-hero"><h1>{title}</h1><p>{desc}</p><div class="doc-actions"><a href="/docs/" class="btn btn-outline">← Все документы</a></div></div><pre class="doc-text-pre">{text_content}</pre>'
    else:
        md_content = read_file(src_path)
        if doc.get("process") == "strip_h1":
            md_content = re.sub(r'\A#\s+.*(\n|$)', '', md_content)
            md_content = md_content.replace('arbat38.ru', 'example.ru')
        html_content = md_to_html(md_content)
        content = f'<div class="feature-page-hero"><h1>{title}</h1><p>{desc}</p><div class="doc-actions"><a href="/docs/" class="btn btn-outline">← Все документы</a></div></div>{html_content}'
    page = page_template(title, desc, slug, content)
    write_file(out_path, page)
    print(f"  OK: /docs/{slug}/")

def main():
    print("Generating documentation pages...")
    for doc in DOCS:
        if doc.get("url"):
            print(f"  EXT: /docs/{doc['slug']}/ -> {doc['url']}")
        else:
            build_page(doc)
    print("Generating index...")
    index_html = generate_index()
    write_file(os.path.join(OUT, "index.html"), index_html)
    print(f"Done! Generated {len(DOCS)} docs + index.html")

if __name__ == "__main__":
    main()
