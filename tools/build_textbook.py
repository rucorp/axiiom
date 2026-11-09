#!/usr/bin/env python3
"""build_textbook.py — собирает раздел /textbook/ из исходного HTML учебника.

Вход:  tools/textbook/source.html — снимок учебника (один файл, как в репозитории ailab)
Выход: textbook/index.html, textbook/<slug>/index.html

Почему генератор, а не ручные страницы: учебник правится вовне, а раздел сайта должен
оставаться в шаблоне AXIIOM (nav, breadcrumbs, footer, метрика, SEO). Скрипт берёт
содержимое глав и оборачивает его в шаблон страницы статьи.

Запуск: python3 tools/build_textbook.py
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "tools" / "textbook" / "source.html"
TEMPLATE = ROOT / "blog" / "fintech-trends-2026" / "index.html"
OUT = ROOT / "textbook"

SITE = "https://axiiom.ru"
TODAY = "2026-11-10"

CHAPTERS = [
    ("intro", "vvedenie", "Введение"),
    ("ch1", "glava-1-teoreticheskie-osnovy", "Глава 1. Теоретические основы искусственного интеллекта"),
    ("ch2", "glava-2-biologicheskie-neirony", "Глава 2. Биологические нейроны и их математические модели"),
    ("ch3", "glava-3-neironnye-seti", "Глава 3. Нейронные сети и архитектуры памяти"),
    ("ch4", "glava-4-obuchenie-pamyat", "Глава 4. Обучение, память и ассоциации"),
    ("ch5", "glava-5-raspoznavanie-obrazov", "Глава 5. Распознавание образов и компьютерное зрение"),
    ("ch6", "glava-6-robototehnika", "Глава 6. Робототехника и автоматное программирование"),
    ("ch7", "glava-7-instrumenty", "Глава 7. Инструменты разработки ИИ"),
    ("ch8", "glava-8-filosofiya-etika", "Глава 8. Философские и этические аспекты ИИ"),
]

TAIL_SECTIONS = ["references", "questions", "glossary"]
TAIL_SLUG = "materialy"
TAIL_TITLE = "Материалы: литература, вопросы, глоссарий"


# SEO-метаданные пишутся вручную: автогенерация из текста давала обрубки
# («2.1. Структура и функция...») и дубли описаний — плохо для индексации.
SEO = {
    "intro": (
        "Введение в учебник по искусственному интеллекту | AXIIOM",
        "Как устроен учебник, на каких первоисточниках он построен и в каком порядке читать главы: нейроны, сети, память, зрение, роботы, этика ИИ.",
    ),
    "ch1": (
        "Глава 1. Теоретические основы ИИ | AXIIOM",
        "Символьный и связистский подходы к ИИ, «сильный» и «слабый» интеллект, кризис идей и почему для прорыва нужна новая теория сложных систем.",
    ),
    "ch2": (
        "Глава 2. Биологические нейроны и их модели | AXIIOM",
        "Как устроен нейрон, модель Маккаллока — Питтса 1943 года, функции активации, импульсные потоки и квазибиологическая модель выживания нейрона.",
    ),
    "ch3": (
        "Глава 3. Нейронные сети и архитектуры памяти | AXIIOM",
        "Многоуровневая модель памяти Бахшиева, нейронные ансамбли, когнитивные системы Станкевича, эволюционный подход к «сильному» ИИ и среда Neuro Modeler.",
    ),
    "ch4": (
        "Глава 4. Обучение, память и ассоциации | AXIIOM",
        "Кратковременная память человека, заучивание пространственной информации, ассоциативная и голографическая память, модель Фрейда — Юнга и волновая активность мозга.",
    ),
    "ch5": (
        "Глава 5. Распознавание образов и зрение | AXIIOM",
        "Байесовский критерий и принцип минимальной длины описания, теория разумных систем Безобразова, модель зрительного внимания и сети глубокого обучения.",
    ),
    "ch6": (
        "Глава 6. Робототехника и автоматное программирование | AXIIOM",
        "Автоматное программирование Шалыто, конечный автомат, управление мобильными роботами и вертолётом, координация группы роботов обучением с подкреплением.",
    ),
    "ch7": (
        "Глава 7. Инструменты разработки ИИ | AXIIOM",
        "RDK, Neuro Modeler, NMSDK и MySDK: среда моделирования нейронных сетей, SDK с исходными кодами и каталог семинарских материалов.",
    ),
    "ch8": (
        "Глава 8. Философия и этика ИИ | AXIIOM",
        "Лимиты картезианской парадигмы, может ли машина мыслить, психические явления и мозг, нарушения мышления, этика ИИ и кодекс разработчика.",
    ),
    "materialy": (
        "Материалы: литература, вопросы, глоссарий | AXIIOM",
        "Список первоисточников, контрольные вопросы по всем главам и глоссарий терминов: от нейрона и синапса до когнитивной архитектуры.",
    ),
    "index": (
        "Учебник по искусственному интеллекту | AXIIOM",
        "Открытый учебник по ИИ: модели нейрона, нейронные сети, память и обучение, распознавание образов, робототехника, этика. Восемь глав, глоссарий, вопросы.",
    ),
}

TB_STYLE = """
<style>
  .tb-code { background: var(--clr-surface, #14141c); border: 1px solid var(--clr-border, #2a2a36);
             border-radius: 12px; padding: 16px 18px; margin: 18px 0; overflow-x: auto;
             font: 500 .95rem/1.7 ui-monospace, SFMono-Regular, Menlo, monospace;
             color: var(--clr-heading, #f2f2f7); }
  .tb-source { font-size: .85rem; color: var(--clr-muted, #9a9aa8); border-left: 2px solid var(--clr-border, #2a2a36);
               padding-left: 12px; margin: 18px 0; }
  .tb-note { background: rgba(120, 120, 255, .08); border: 1px solid var(--clr-border, #2a2a36);
             border-radius: 12px; padding: 16px 18px; margin: 22px 0; }
  .tb-note h4 { margin: 0 0 8px; font-size: .95rem; letter-spacing: .04em; text-transform: uppercase;
                color: var(--clr-muted, #9a9aa8); }
  .article-wrap table { width: 100%; border-collapse: collapse; margin: 20px 0; font-size: .92rem; }
  .article-wrap th, .article-wrap td { border: 1px solid var(--clr-border, #2a2a36);
                                       padding: 9px 11px; text-align: left; vertical-align: top; }
  .article-wrap th { background: rgba(255,255,255,.04); font-weight: 600; }
  .tb-nav { display: flex; flex-wrap: wrap; gap: 10px; justify-content: space-between;
            margin: 36px 0 0; padding-top: 20px; border-top: 1px solid var(--clr-border, #2a2a36); }
  .tb-nav a { font-size: .92rem; }
  .tb-toc { margin: 8px 0 0; padding-left: 20px; }
  .tb-toc li { margin: 7px 0; }
</style>
"""


def sections(src: str) -> dict[str, str]:
    """Возвращает {section_id: внутренний HTML}."""
    main = src.split("<main", 1)[1].split("</main>", 1)[0]
    out = {}
    for m in re.finditer(r'<section[^>]*id="([^"]+)"[^>]*>(.*?)</section>', main, re.S):
        out[m.group(1)] = m.group(2).strip()
    return out


def convert(html: str) -> str:
    """Приводит разметку учебника к тому, что умеет .article-wrap сайта."""
    html = re.sub(r'<div class="code-block">(.*?)</div>',
                  lambda m: f'<div class="tb-code">{m.group(1).strip()}</div>', html, flags=re.S)
    html = re.sub(r'<p class="citation">(.*?)</p>',
                  lambda m: f'<p class="tb-source">{m.group(1).strip()}</p>', html, flags=re.S)
    html = re.sub(r'<div class="key-box">(.*?)</div>',
                  lambda m: f'<div class="tb-note">{m.group(1).strip()}</div>', html, flags=re.S)
    # внутренние якоря учебника (#s2-1) на сайте не нужны — оставляем текст
    html = re.sub(r'\s+id="s\d+-\d+"', "", html)
    return html.strip()


def strip_h1(html: str) -> str:
    return re.sub(r"<h1[^>]*>.*?</h1>", "", html, count=1, flags=re.S).strip()


def plain(html: str) -> str:
    txt = re.sub(r"<[^>]+>", " ", html)
    txt = re.sub(r"\s+", " ", txt)
    return txt.strip()


def head(tpl: str, *, title: str, description: str, url: str, h1: str, og_image: str) -> str:
    """Подставляет SEO-поля в <head> шаблона и добавляет стили раздела."""
    head = tpl.split("</head>", 1)[0] + "</head>"
    head = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", head, flags=re.S)
    head = re.sub(r'<meta name="description" content="[^"]*">',
                  f'<meta name="description" content="{description}">', head)
    head = re.sub(r'<link rel="canonical" href="[^"]*">',
                  f'<link rel="canonical" href="{url}">', head)
    for prop, value in (
        ("og:url", url),
        ("og:title", title),
        ("og:description", description),
        ("og:image", og_image),
        ("twitter:url", url),
        ("twitter:title", title),
        ("twitter:description", description),
        ("twitter:image", og_image),
    ):
        head = re.sub(rf'<meta (property|name)="{prop}" content="[^"]*">',
                      lambda m, v=value, p=prop: f'<meta {m.group(1)}="{p}" content="{v}">', head)
    jsonld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Article",
                "headline": h1,
                "description": description,
                "datePublished": TODAY,
                "dateModified": TODAY,
                "inLanguage": "ru",
                "author": {"@type": "Organization", "name": "AXIIOM", "url": f"{SITE}/"},
                "publisher": {"@type": "Organization", "name": "AXIIOM", "url": f"{SITE}/"},
                "mainEntityOfPage": {"@type": "WebPage", "@id": url},
                "image": og_image,
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Главная", "item": f"{SITE}/"},
                    {"@type": "ListItem", "position": 2, "name": "Учебник по ИИ", "item": f"{SITE}/textbook/"},
                    {"@type": "ListItem", "position": 3, "name": h1, "item": url},
                ],
            },
        ],
    }
    head = re.sub(r'<script type="application/ld\+json">.*?</script>',
                  f'<script type="application/ld+json">\n{json.dumps(jsonld, ensure_ascii=False, indent=2)}\n</script>',
                  head, flags=re.S)
    head = head.replace("</head>", TB_STYLE + "</head>")
    return head


def body_shell(tpl: str) -> tuple[str, str]:
    """Возвращает (верх шаблона до статьи, низ после статьи)."""
    top = tpl.split('<section class="article-page">', 1)[0]
    bottom = tpl.split("</section>", 1)[1]
    return top, bottom


def page(head_html: str, tpl_top: str, tpl_bottom: str, *, title: str, description: str, url: str,
         h1: str, date_label: str, content: str, nav: str) -> str:
    return f"""{head_html}{tpl_top.replace("@@HEAD@@", "")}<section class="article-page">
    <div class="container">
        <div class="article-wrap">
            <span class="art-date">{date_label}</span>
            <h1>{h1}</h1>
            <div>
{content}
            </div>
            <div class="glass-card card-pad-md" style="margin-top:32px">
                <p class="label">AXIIOM</p>
                <h3 style="font-size:1.15rem;margin:8px 0 10px">Разрабатываем финтех-продукты и ИИ-решения</h3>
                <p style="margin:0 0 14px">Сайты, мобильные приложения, платёжные интеграции и внедрение ИИ — от стратегии до поддержки.</p>
                <p style="margin:0"><a class="link-accent" href="https://axiiom.ru/">Перейти на axiiom.ru →</a> &nbsp;·&nbsp; <a class="link-accent" href="https://axiiom.ru/#contact">Обсудить проект</a></p>
            </div>
            <nav class="tb-nav">{nav}</nav>
        </div>
    </div>
</section>{tpl_bottom}"""


def main() -> None:
    src = SRC.read_text(encoding="utf-8")
    tpl = TEMPLATE.read_text(encoding="utf-8")
    secs = sections(src)

    head_tpl = tpl.split("</head>", 1)[0] + "</head>"
    tpl_top, tpl_bottom = body_shell(tpl)
    # <head> шаблона заменяем целиком на сгенерированный
    tpl_top = tpl_top.replace(head_tpl, "@@HEAD@@")

    pages: list[tuple[str, str, str, str]] = []  # (slug, h1, description, url)

    # --- главы ---
    for i, (sid, slug, h1) in enumerate(CHAPTERS):
        raw = strip_h1(convert(secs[sid]))
        title, desc = SEO[sid]
        url = f"{SITE}/textbook/{slug}/"
        og_image = f"{SITE}/og/textbook/{slug}.png"
        prev_link = ""
        next_link = ""
        seq = [c[1] for c in CHAPTERS] + [TAIL_SLUG]
        idx = seq.index(slug)
        if idx > 0:
            prev_link = f'<a href="/textbook/{seq[idx-1]}/">← {dict((c[1], c[2]) for c in CHAPTERS).get(seq[idx-1], "Материалы")}</a>'
        next_link = f'<a href="/textbook/{seq[idx+1]}/">{"Материалы" if seq[idx+1] == TAIL_SLUG else CHAPTERS[idx+1][2]} →</a>'
        nav = f'<a href="/textbook/">Содержание</a>{prev_link}{next_link}'
        html = page(head(head_tpl, title=title, description=desc, url=url, h1=h1, og_image=og_image),
            tpl_top, tpl_bottom, title=title, description=desc, url=url, h1=h1,
            date_label=f"Учебник · {i + 1} из {len(CHAPTERS)}", content=raw, nav=nav)
        out = OUT / slug / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html, encoding="utf-8")
        pages.append((slug, h1, desc, url))

    # --- материалы ---
    tail_raw = "\n".join(convert(secs[s]) for s in TAIL_SECTIONS)
    tail_raw = strip_h1(tail_raw)
    title, desc = SEO["materialy"]
    url = f"{SITE}/textbook/{TAIL_SLUG}/"
    og_image = f"{SITE}/og/textbook/{TAIL_SLUG}.png"
    nav = '<a href="/textbook/">Содержание</a><a href="/textbook/glava-8-filosofiya-etika/">← Глава 8</a>'
    html = page(head(head_tpl, title=title, description=desc, url=url, h1=TAIL_TITLE, og_image=og_image),
        tpl_top, tpl_bottom, title=title, description=desc, url=url, h1=TAIL_TITLE,
        date_label="Учебник · материалы", content=tail_raw, nav=nav)
    (OUT / TAIL_SLUG).mkdir(parents=True, exist_ok=True)
    (OUT / TAIL_SLUG / "index.html").write_text(html, encoding="utf-8")
    pages.append((TAIL_SLUG, TAIL_TITLE, desc, url))

    # --- лендинг раздела ---
    items = "\n".join(
        f'        <li><a href="/textbook/{slug}/">{h1}</a></li>' for slug, h1, _, _ in pages)
    landing_body = f"""<p>Учебник по искусственному интеллекту: от математических моделей биологического нейрона до когнитивных архитектур, систем распознавания образов и группового управления роботами. Материал собран из научных семинаров и публикаций исследовательской группы, авторство указано в каждом разделе.</p>
<p>Изложение охватывает четыре линии: нейрофизиологическую (модели нейрона, импульсные потоки, модели выживания), когнитивную (память, обучение, когнитивные архитектуры), прикладную (распознавание образов, автоматное программирование, координация роботов, инструменты разработки) и философско-методологическую (границы алгоритмической реализуемости интеллекта, этика ИИ).</p>
<h2>Содержание</h2>
<ul class="tb-toc">
{items}
</ul>
<h2>Как читать</h2>
<p>Главы независимы, но выстроены в логическом порядке: сначала формальные основы и модели нейрона, затем сети и память, потом прикладные разделы, и в конце — философия и этика. Для быстрого входа начните с <a href="/textbook/glava-2-biologicheskie-neirony/">главы 2</a> — там разобрана модель Маккаллока — Питтса и её ограничения.</p>
<h2>Авторы материалов</h2>
<p>А.С. Потапов, А.В. Бахшиев, В.А. Ляховецкий, В.Ф. Соломатин, А.С. Неверов, А.А. Шалыто, В.В. Александров, А. Редозубов, Д. Ерусалимчик, М.В. Безобразов, Т.В. Чередникова, А.А. Меклер и другие исследователи.</p>"""
    url = f"{SITE}/textbook/"
    title, desc = SEO["index"]
    og_image = f"{SITE}/og/textbook/index.png"
    nav = '<a href="/textbook/vvedenie/">С первой главы →</a>'
    html = page(head(head_tpl, title=title, description=desc, url=url, h1="Учебник по искусственному интеллекту", og_image=og_image),
        tpl_top, tpl_bottom, title=title, description=desc, url=url,
        h1="Учебник по искусственному интеллекту", date_label="Открытый учебник",
        content=landing_body, nav=nav)
    (OUT / "index.html").write_text(html, encoding="utf-8")

    print(f"готово: {len(pages) + 1} страниц в {OUT}")


if __name__ == "__main__":
    main()
