#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генератор статей блога под коммерческие запросы.

Каждая статья ведёт на страницу услуги — это и есть смысл: человек
ищет «сколько стоит CRM», читает и попадает на /services/crm-erp/.

Запуск: python3 tools/gen_blog.py
"""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
TPL = ROOT / "blog" / "vneshniy-cto-malyy-biznes" / "index.html"
BASE = "https://axiiom.ru"

MONTHS = ["января", "февраля", "марта", "апреля", "мая", "июня",
          "июля", "августа", "сентября", "октября", "ноября", "декабря"]


def human_date(iso):
    y, m, d = iso.split("-")
    return f"{int(d)} {MONTHS[int(m) - 1]} {y}"


def body_html(blocks):
    out = []
    for b in blocks:
        kind = b[0]
        if kind == "p":
            out.append(f"<p>{b[1]}</p>")
        elif kind == "h2":
            out.append(f"<h2>{b[1]}</h2>")
        elif kind == "h3":
            out.append(f"<h3>{b[1]}</h3>")
        elif kind == "ul":
            items = "".join(f"<li>{i}</li>" for i in b[1])
            out.append(f"<ul>{items}</ul>")
        elif kind == "table":
            head = "".join(f"<th>{h}</th>" for h in b[1])
            rows = "".join(
                "<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in b[2]
            )
            out.append(f'<table><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table>')
        elif kind == "quote":
            out.append(
                f'<blockquote style="border-left:3px solid var(--clr-accent);'
                f'padding-left:16px;margin:24px 0;color:var(--clr-muted)">{b[1]}</blockquote>'
            )
    return "\n".join(out)


def build(a, tpl):
    url = f'{BASE}/blog/{a["slug"]}/'
    i = tpl.find("<body")
    head_start = 0
    head = tpl[:i]
    rest = tpl[i:]

    # --- head ---
    head = re.sub(r"<title>.*?</title>", f'<title>{a["title"]}</title>', head, flags=re.S)
    head = re.sub(r'<meta name="description" content=".*?">',
                  f'<meta name="description" content="{a["desc"]}">', head, count=1, flags=re.S)
    head = re.sub(r'<link rel="canonical" href=".*?">',
                  f'<link rel="canonical" href="{url}">', head, count=1)
    head = re.sub(r'<meta property="og:url" content=".*?">',
                  f'<meta property="og:url" content="{url}">', head, count=1)
    head = re.sub(r'<meta property="og:title" content=".*?">',
                  f'<meta property="og:title" content="{a["title"]}">', head, count=1)
    head = re.sub(r'<meta property="og:description" content=".*?">',
                  f'<meta property="og:description" content="{a["desc"]}">', head, count=1)
    head = re.sub(r'<meta name="twitter:url" content=".*?">',
                  f'<meta name="twitter:url" content="{url}">', head, count=1)
    head = re.sub(r'<meta name="twitter:title" content=".*?">',
                  f'<meta name="twitter:title" content="{a["title"]}">', head, count=1)
    head = re.sub(r'<meta name="twitter:description" content=".*?">',
                  f'<meta name="twitter:description" content="{a["desc"]}">', head, count=1)

    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Article",
                "headline": a["h1"],
                "description": a["desc"],
                "datePublished": a["date"],
                "dateModified": a["date"],
                "author": {"@type": "Organization", "name": "AXIIOM", "url": BASE + "/"},
                "publisher": {"@type": "Organization", "name": "AXIIOM", "url": BASE + "/"},
                "mainEntityOfPage": {"@type": "WebPage", "@id": url},
                "image": f'{BASE}/og/help/{a["slug"]}.png',
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Главная", "item": BASE + "/"},
                    {"@type": "ListItem", "position": 2, "name": "Блог", "item": BASE + "/blog/"},
                    {"@type": "ListItem", "position": 3, "name": a["h1"], "item": url},
                ],
            },
        ],
    }
    head = re.sub(
        r'<script type="application/ld\+json">.*?</script>',
        '<script type="application/ld+json">\n'
        + json.dumps(ld, ensure_ascii=False, indent=2)
        + "\n</script>",
        head, count=1, flags=re.S,
    )

    # --- тело статьи ---
    related = "".join(
        f'<li><a href="{href}" class="link-accent">{text}</a></li>'
        for href, text in a["related"]
    )
    faq = "".join(f"<h3>{q}</h3><p>{p}</p>" for q, p in a["faq"])

    article = f'''<section class="article-page">
    <div class="container">
        <div class="article-wrap">
            <span class="art-date">{human_date(a["date"])} · AXIIOM</span>
            <h1>{a["h1"]}</h1>
            <div>
{body_html(a["body"])}
            </div>

<div class="glass-card card-pad-md" style="margin-top:32px">
<p class="label">Вопросы и ответы</p>
{faq}
</div>
<div class="glass-card card-pad-md" style="margin-top:32px">
<p class="label">Читайте также</p>
<h3 style="font-size:1.1rem;margin-bottom:12px;color:var(--clr-heading)">Вам может пригодиться</h3>
<ul style="padding-left:20px;margin:0">
{related}
</ul>
<p style="margin-top:16px;font-size:.85rem;color:var(--clr-muted)"><a href="{a["cta_href"]}" class="link-accent">{a["cta_text"]}</a> · <a href="/projects/" class="link-accent">Портфолио AXIIOM</a></p>
</div>
        </div>
    </div>
</section>'''

    # вырезаем старую статью из rest
    s0 = rest.find('<section class="article-page">')
    s1 = rest.find("</section>", s0) + len("</section>")
    return head + rest[:s0] + article + rest[s1:]


def main():
    tpl = TPL.read_text(encoding="utf-8")
    data = json.loads((ROOT / "tools" / "blog_data.json").read_text(encoding="utf-8"))
    for a in data:
        page = build(a, tpl)
        out = ROOT / "blog" / a["slug"] / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page, encoding="utf-8")
        print(f'  ✅ /blog/{a["slug"]}/  ({len(page)} байт)')


if __name__ == "__main__":
    main()
