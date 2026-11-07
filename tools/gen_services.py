#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генератор страниц услуг /services/*.

Каркас (шапка, подвал, скрипты) берётся из пилотной страницы мобильных
приложений, меняется только содержимое <main> и метаданные.

Запуск: python3 tools/gen_services.py
"""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
PILOT = ROOT / "services" / "mobilnye-prilozheniya" / "index.html"

BASE = "https://axiiom.ru"


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def problems(items):
    out = []
    for pain, sol in items:
        out.append(
            '<div class="glass-card reveal card-pad-md">\n'
            f'<p class="problem-text">{pain}</p>\n'
            f'<p class="solution-text"><strong>Решение: {sol}</strong></p>\n'
            "</div>"
        )
    return "\n".join(out)


def cards(items, icon='<path d="M20 6L9 17l-5-5"/>'):
    out = []
    for h, p, note in items:
        note_html = f'<p style="margin-top:12px;color:var(--clr-accent);font-size:.85rem">{note}</p>' if note else ""
        out.append(
            '<div class="card reveal">\n'
            f'<div class="card-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" '
            f'stroke="currentColor" stroke-width="2">{icon}</svg></div>\n'
            f"<h3>{h}</h3>\n<p>{p}</p>\n{note_html}\n</div>"
        )
    return "\n".join(out)


def process(items):
    out = []
    for i, (h, p) in enumerate(items, 1):
        out.append(
            '<div class="glass-card reveal card-pad-md">'
            f'<div class="process-num">{i:02d}</div>'
            f"<h3>{h}</h3><p>{p}</p></div>"
        )
    return "\n".join(out)


def cases(items):
    out = []
    for href, status_cls, status, title, text, tags, link in items:
        ext = ' target="_blank" rel="noopener"' if href.startswith("http") else ""
        tag_html = "".join(f"<span>{t}</span>" for t in tags)
        out.append(
            f'<a href="{href}"{ext} class="project-card project-card--md reveal">\n'
            f'<div class="demo-accent" style="background:linear-gradient(135deg,#a29bfe,#6c5ce7)"></div>\n'
            '<div class="demo-body">\n'
            f'<div class="project-status {status_cls}">{status}</div>\n'
            f"<h3>{title}</h3>\n<p>{text}</p>\n"
            f'<div class="demo-tags">{tag_html}</div>\n'
            f'<span class="demo-link">{link}</span>\n'
            "</div></a>"
        )
    return "\n".join(out)


def faq(items):
    out = []
    for q, a in items:
        out.append(
            '<div class="glass-card card-pad-md">'
            f"<h3>{q}</h3><p>{a}</p></div>"
        )
    return "\n".join(out)


def related(items):
    out = []
    for h, p, link, text in items:
        out.append(
            '<div class="card reveal">'
            f"<h3>{h}</h3><p>{p}</p>"
            f'<p style="margin-top:12px"><a href="{link}" class="link-accent">{text} →</a></p>'
            "</div>"
        )
    return "\n".join(out)


def build_main(d):
    return f'''<main id="main">
<section class="hero industries-hero">
<div class="container"><div class="hero-content">
<div class="hero-bg-svg"><svg width="800" height="600" viewBox="0 0 800 600" fill="none"><circle cx="400" cy="300" r="280" stroke="rgba(255,255,255,0.05)" stroke-width="2"/><circle cx="400" cy="300" r="200" stroke="rgba(255,255,255,0.06)" stroke-width="2"/><circle cx="400" cy="300" r="120" stroke="rgba(255,255,255,0.08)" stroke-width="2"/><line x1="50" y1="300" x2="750" y2="300" stroke="rgba(255,255,255,0.04)" stroke-width="2"/><line x1="400" y1="20" x2="400" y2="580" stroke="rgba(255,255,255,0.04)" stroke-width="2"/><circle cx="400" cy="300" r="4" fill="rgba(255,255,255,0.12)"/></svg></div>
<div class="hero-category-icon"><svg width="400" height="400" viewBox="0 0 400 400" fill="none">{d["icon"]}</svg></div>
<div class="badge-row"><p class="badge">Услуга • Разработка</p><button class="share-btn" onclick="copyPageUrl(this)" aria-label="Поделиться"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 12v8a2 2 0 002 2h12a2 2 0 002-2v-8"/><polyline points="16 6 12 2 8 6"/><line x1="12" y1="2" x2="12" y2="15"/></svg><span class="share-tooltip">Ссылка скопирована</span></button></div>
<h1>{d["h1"]}</h1>
<p class="hero-desc">{d["desc"]}</p>
<div class="price-anchor reveal">{d["badges"]}</div>
<div class="hero-btns"><a href="/#contact" class="btn">Обсудить проект за 1 час</a><a href="/calculator/{d["calc"]}" class="btn btn-outline">Рассчитать смету →</a></div>
<div class="hero-trust">{d["trust"]}</div>
<div class="author-block reveal"><span class="author-avatar">AX</span><div><strong>Команда AXIIOM</strong> • 22 года в разработке • <span class="author-date">Обновлено: {d["date"]}</span></div></div>
</div></div></section>

<section class="section">
<div class="container">
<p class="label reveal">Что решаем</p>
<h2 class="reveal">{d["problems_h2"]}</h2>
<div class="problems-grid">
{problems(d["problems"])}
</div>
</div>
</section>

<section class="section dark">
<div class="container">
<p class="label reveal">Смета</p>
<h2 class="reveal">{d["price_h2"]}</h2>
<p class="content-wrapper reveal" style="max-width:680px;margin:16px auto 0;color:var(--clr-muted)">{d["price_lead"]}</p>
<div class="tools-grid">
{cards(d["price_factors"])}
</div>
<div style="text-align:center;margin-top:32px" class="reveal">
<a href="/calculator/{d["calc"]}" class="btn">Посчитать в калькуляторе →</a>
</div>
</div>
</section>

<section class="section">
<div class="container">
<p class="label reveal">Процесс</p>
<h2 class="reveal">{d["process_h2"]}</h2>
<div class="process-grid">
{process(d["process"])}
</div>
</div>
</section>

<section class="section dark">
<div class="container">
<p class="label reveal">Стек</p>
<h2 class="reveal">{d["stack_h2"]}</h2>
<div class="tools-grid">
{cards(d["stack"])}
</div>
</div>
</section>

<section class="section">
<div class="container">
<p class="label reveal">Кейсы</p>
<h2 class="reveal">{d["cases_h2"]}</h2>
<div class="demo-grid">
{cases(d["cases"])}
</div>
</div>
</section>

<section class="section dark">
<div class="container">
<p class="label reveal">Вопросы</p>
<h2 class="reveal">Частые вопросы</h2>
<div class="faq-grid reveal">
{faq(d["faq"])}
</div>
</div>
</section>

<section class="section">
<div class="container">
<p class="label reveal">Ещё услуги</p>
<h2 class="reveal">Смежное, если пригодится</h2>
<div class="tools-grid">
{related(d["related"])}
</div>
</div>
</section>

<section class="section cta-section">
<div class="container">
<div class="glass-card cta-card reveal">
<h2>{d["cta_h2"]}</h2>
<p>{d["cta_text"]}</p>
<div class="cta-contacts">
<a href="/#contact" class="btn">Обсудить проект</a>
<a href="tel:+78129287478" class="btn btn-outline">+7 (812) 928-74-78</a>
</div>
<p style="margin-top:16px;font-size:.85rem;color:var(--clr-muted)">Или напишите на <a href="mailto:axiiom@ya.ru" class="link-accent">axiiom@ya.ru</a> — ответим в течение рабочего дня</p>
</div>
</div>
</section>
</main>'''


def build_head(d, chrome_head):
    url = f'{BASE}/services/{d["slug"]}/'
    g = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebPage",
                "name": d["h1"],
                "description": d["meta_desc"],
                "url": url,
                "isPartOf": {"@type": "WebSite", "name": "AXIIOM", "url": BASE + "/"},
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Главная", "item": BASE + "/"},
                    {"@type": "ListItem", "position": 2, "name": "Услуги", "item": BASE + "/services/"},
                    {"@type": "ListItem", "position": 3, "name": d["short"], "item": url},
                ],
            },
            {
                "@type": "Service",
                "serviceType": d["h1"],
                "provider": {"@type": "Organization", "name": "AXIIOM", "url": BASE + "/"},
                "areaServed": {"@type": "Country", "name": "Россия"},
                "description": d["meta_desc"],
            },
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a},
                    }
                    for q, a in d["faq"]
                ],
            },
        ],
    }
    ld = (
        '<script type="application/ld+json">\n'
        + json.dumps(g, ensure_ascii=False, indent=2)
        + "\n</script>"
    )

    head = f'''<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="theme-color" content="#0A0A0F">
<title>{d["title"]}</title>
<meta name="description" content="{d["meta_desc"]}">
<link rel="canonical" href="{url}">
{ld}
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{d["og_title"]}">
<meta property="og:description" content="{d["og_desc"]}">
<meta property="og:image" content="{BASE}/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="ru_RU">
<meta property="og:site_name" content="AXIIOM">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:url" content="{url}">
<meta name="twitter:title" content="{d["og_title"]}">
<meta name="twitter:description" content="{d["og_desc"]}">
<meta name="twitter:image" content="{BASE}/og-image.png">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="preload" href="/assets/fonts/inter-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/styles.css?v=20261107">
<link rel="stylesheet" href="/preloader.css?v=20261107">
<link rel="manifest" href="/manifest.webmanifest">
<link rel="apple-touch-icon" sizes="180x180" href="/icons/apple-touch-icon.png">'''
    return head


def main():
    pilot = PILOT.read_text(encoding="utf-8")
    body_start = pilot.find("<body")
    main_start = pilot.find('<main id="main">')
    main_end = pilot.find("</main>") + len("</main>")
    body_chrome = pilot[body_start:main_start]
    footer_chrome = pilot[main_end:]

    data = json.loads((ROOT / "tools" / "services_data.json").read_text(encoding="utf-8"))
    for d in data:
        head = build_head(d, None)
        page = (
            '<!DOCTYPE html>\n<html lang="ru">\n<head>\n'
            + head
            + "\n</head>\n"
            + body_chrome
            + build_main(d)
            + footer_chrome
        )
        out = ROOT / "services" / d["slug"] / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page, encoding="utf-8")
        print(f"  ✅ /services/{d['slug']}/  ({len(page)} байт)")


if __name__ == "__main__":
    main()
