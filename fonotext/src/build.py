#!/usr/bin/env python3
"""Сборка саб-сайта fonotext/ из markdown-источников fonotext/src/.

Канон оформления — корп стиль axiiom (как у mock-services/, но статический HTML
без рантайма). URL-схема: fonotext.ru/docs/NN-slug.html -> axiiom.ru/fonotext/NN-slug,
fonotext.ru/docs/10-feature-specs/NN-slug.html -> axiiom.ru/fonotext/specs/NN-slug.

Запуск: python3 fonotext/src/build.py   (из корня репозитория axiiom)
"""
from __future__ import annotations

import hashlib
import html as html_mod
import json
import re
import shutil
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parents[2]  # корень репозитория axiiom
SRC = Path(__file__).resolve().parent
OUT = ROOT / "fonotext"
SITE = "https://axiiom.ru"
BASE = "/fonotext"
LANDING = "https://fonotext.ru/"

MAIN_PAGES = {  # slug -> (title, description)
    "00-product-presentation": (
        "Fonotext: презентация продукта",
        "Что такое Fonotext: расшифровка и классификация 100 % звонков, контроль скриптов "
        "с доказательствами, дашборды. 12 тезисов для руководителя контакт-центра.",
    ),
    "01-integration": (
        "Интеграция и анкета подключения | Fonotext",
        "Как подключить Fonotext к телефонии: REST API, вебхуки, SFTP/S3, форматы аудио, "
        "анкета подключения и что получает заказчик после интеграции.",
    ),
    "02-architecture": (
        "Архитектура Fonotext",
        "Конвейер обработки звонков: транскрибация, классификация, контроль скриптов, "
        "хранение транскриптов в ClickHouse и S3, риски и их закрытие.",
    ),
    "03-models": (
        "Модели и качество распознавания | Fonotext",
        "Каскад моделей: Whisper, GigaAM, T-one; LLM-классификация, методика оценки качества "
        "в пилоте (WER, F1), выбор моделей под телефонию.",
    ),
    "04-hardware": (
        "Мощности и оборудование | Fonotext",
        "Расчёт GPU-мощностей под объём звонков, арендованные GPU с автоскейлом, "
        "требования к серверам для коробочной поставки.",
    ),
    "05-poc-plan": (
        "План пилота Fonotext",
        "Измерительный пилот 4–6 недель: этапы, метрики (WER, F1, полнота скриптов), "
        "критерии Go/No-Go, риски пилота и как они снимаются.",
    ),
    "07-deployment": (
        "Поставка, SLA и развёртывание | Fonotext",
        "Три сценария поставки: облако в РФ, выделенный шард с BYOK, коробка on-prem. "
        "Конфигурации серверов, SLA, обновления модели.",
    ),
    "08-api": (
        "API Fonotext",
        "Асинхронный API: загрузка звонков, статусы, вебхуки, выгрузка транскриптов и "
        "результатов классификации, формат карточки звонка.",
    ),
    "13-bezopasnost-i-152-fz": (
        "Безопасность и 152-ФЗ | Fonotext",
        "Обработка и хранение данных на территории РФ, роли оператора и обработчика ПДн, "
        "ролевая модель, SSO/AD, маскирование данных в выгрузках.",
    ),
    "14-chto-novogo-v1-1": (
        "Что нового в Fonotext 1.1",
        "Изменения версии 1.1: новые возможности классификации, контроля скриптов "
        "и отчётности.",
    ),
}

SPEC_ORDER = [
    ("01-full-coverage", "Покрытие 100 % звонков"),
    ("02-taxonomy-builder", "Конструктор таксономии"),
    ("03-script-evidence", "Скрипты с доказательствами"),
    ("04-archive", "Разбор архива"),
    ("05-private-shard", "Выделенный шард"),
    ("06-ask-your-calls", "Спроси свои звонки"),
    ("07-quality-drift", "Контроль дрейфа качества"),
    ("08-alerts-actions", "Оповещения и действия"),
    ("09-integrations", "Интеграции (CRM, BI)"),
    ("10-dashboards", "Дашборды"),
    ("11-qa-checklists", "Чек-листы контроля качества"),
    ("12-copilot", "Отчётный копилот"),
]

MD_EXT = ("tables", "fenced_code", "sane_lists", "toc")

# Группировка для навигации
NAV_SECTIONS = [
    ("Обзор", ["00-product-presentation", "14-chto-novogo-v1-1"]),
    ("Внедрение", ["01-integration", "05-poc-plan", "08-api"]),
    ("Технология", ["02-architecture", "03-models", "04-hardware"]),
    ("Эксплуатация", ["07-deployment", "13-bezopasnost-i-152-fz"]),
]

ORG = {
    "name": "ООО «Аксиома»",
    "inn": "ИНН 7842223709",
    "ogrn": "ОГРН 1247800067690",
    "address": "192029, г. Санкт-Петербург, ул. Профессора Качалова, д. 15А, литера А",
    "email": "axiiom@ya.ru",
    "phone": "+7 (812) 928-74-78",
}


def rewrite_links(md_text: str, current: str) -> str:
    """Переписать внутренние ссылки md на целевые URL саб-сайта."""
    base = current.split("/")[0]  # "" для главных, "specs" для спек

    def repl(m: re.Match) -> str:
        target, suffix = m.group(1), m.group(2) or ""
        t = target.strip()
        # Лендинг и демо остаются на fonotext.ru
        if t in ("index.html", "./index.html"):
            return f"]({LANDING}{suffix})"
        if t.startswith("demo/"):
            return f"](https://fonotext.ru/{t}{suffix})"
        # Ссылки на страницы, не перенесённые по контент-канону
        stem = t.split("/")[-1].removesuffix(".md").removesuffix(".html")
        if stem in ("06-pricing", "09-competitive-landscape",
                    "12-kak-ustroena-nasha-cena", "we-vs-market-2026"):
            return f"]({LANDING}{suffix})"
        # md-ссылки на документацию
        if t.endswith(".md"):
            if t.startswith("../"):
                slug = t[3:].removesuffix(".md")
                return f"]({BASE}/{slug}/{suffix})"
            if t == "README.md" or t.endswith("/README.md"):
                return f"]({BASE}/specs/{suffix})"
            if "/" in t:  # 10-feature-specs/NN-slug.md
                slug = t.split("/")[-1].removesuffix(".md")
                return f"]({BASE}/specs/{slug}/{suffix})"
            if base == "specs":
                return f"]({BASE}/specs/{t.removesuffix('.md')}/{suffix})"
            return f"]({BASE}/{t.removesuffix('.md')}/{suffix})"
        # html-ссылки на каталог спек
        if t in ("10-feature-specs/", "10-feature-specs"):
            return f"]({BASE}/specs/{suffix})"
        if t.startswith("10-feature-specs/") and not t.endswith(".md"):
            slug = t.split("/")[-1].removesuffix(".html")
            return f"]({BASE}/specs/{slug}/{suffix})"
        # html-ссылки на перенесённые страницы (в т.ч. ../ из спек)
        if t.endswith(".html"):
            stem = t.split("/")[-1].removesuffix(".html")
            if stem in MAIN_PAGES:
                return f"]({BASE}/{stem}/{suffix})"
            if stem in {s for s, _ in SPEC_ORDER}:
                return f"]({BASE}/specs/{stem}/{suffix})"
        # Якоря и прочее — как есть
        return m.group(0)

    md_text = re.sub(r"\]\(([^)]+?)(#[^)]*)?\)", repl, md_text)
    return md_text


def strip_version_lines(md_text: str) -> str:
    return md_text


def og_image(canonical: str) -> str:
    """Путь к og:image страницы: персональная картинка og/fonotext/<name>.png.

    Имя файла согласовано с generate_og_fonotext.py. Для служебной 404 —
    общая карточка сайта.
    """
    if canonical.endswith("404.html"):
        return f"{SITE}/og-image.png"
    rel = canonical[len(BASE):].strip("/")
    if rel == "":
        name = "index"
    elif rel == "specs":
        name = "specs-index"
    else:
        name = rel.replace("/", "-")
    return f"{SITE}/og/fonotext/{name}.png"


def page_html(*, title: str, desc: str, canonical: str, body: str,
              active: str, crumb: str) -> str:
    nav_items = []
    for section, slugs in NAV_SECTIONS:
        links = []
        for slug in slugs:
            t = MAIN_PAGES[slug][0].split("|")[0]
            links.append(f'<li><a href="{BASE}/{slug}/"{active(slug)}>{html_mod.escape(t)}</a></li>')
        nav_items.append(
            f'<section><h2>{section}</h2><ul>{"".join(links)}</ul></section>')
    specs_links = "".join(
        f'<li><a href="{BASE}/specs/{slug}/"{active("specs/" + slug)}>'
        f'{html_mod.escape(name)}</a></li>'
        for slug, name in SPEC_ORDER)
    nav_items.append(f'<section><h2>Спецификации функций</h2><ul>{specs_links}</ul></section>')
    sidebar = "".join(nav_items)

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html_mod.escape(title)}</title>
<meta name="description" content="{html_mod.escape(desc)}">
<link rel="canonical" href="{SITE}{canonical}">
<link rel="icon" href="{BASE}/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{BASE}/assets/style.css">
<meta property="og:type" content="article">
<meta property="og:site_name" content="AXIIOM — Fonotext">
<meta property="og:title" content="{html_mod.escape(title)}">
<meta property="og:description" content="{html_mod.escape(desc)}">
<meta property="og:url" content="{SITE}{canonical}">
<meta property="og:locale" content="ru_RU">
<meta property="og:image" content="{og_image(canonical)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{og_image(canonical)}">
<script src="/metrika.js?v=20261105" defer></script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-HFS4BDGTV4"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'G-HFS4BDGTV4');
</script>
</head>
<body>
<noscript><div><img src="https://mc.yandex.ru/watch/109391253" style="position:absolute;left:-9999px" alt=""></div></noscript>
<a href="#main" class="skip-link">Перейти к содержанию</a>
<header class="site-header">
  <div class="wrap header-row">
    <a href="/" class="brand">AXIIOM</a>
    <nav class="crumbs" aria-label="Хлебные крошки">
      <a href="/fonotext/">Fonotext</a><span aria-hidden="true">/</span><span>{crumb}</span>
    </nav>
    <a href="{LANDING}" class="ext" rel="noopener">Fonotext</a>
  </div>
</header>
<div class="wrap layout">
  <aside class="sidebar" aria-label="Навигация по документации">{sidebar}</aside>
  <main id="main" class="doc">
{body}
  </main>
</div>
<footer class="site-footer">
  <div class="wrap">
    <p><strong>Fonotext</strong> — сервис речевой аналитики. Проект компании AXIIOM
       (<a href="/" rel="noopener">axiiom.ru</a>). Сайт проекта:
       <a href="{LANDING}" rel="noopener">fonotext.ru</a>.</p>
    <p>{ORG["name"]}, {ORG["inn"]}, {ORG["ogrn"]}. {ORG["address"]}.</p>
    <p>Пилот и демо: <a href="mailto:{ORG["email"]}">{ORG["email"]}</a>,
       <a href="tel:+78129287478">{ORG["phone"]}</a>.
       Коммерческие условия — по запросу.</p>
  </div>
</footer>
</body>
</html>
"""


def active(current: str):
    def f(slug: str) -> str:
        return ' class="active"' if slug == current else ""
    return f


def render_doc(slug: str, md_text: str) -> str:
    md = rewrite_links(md_text, "docs")
    title, desc = MAIN_PAGES[slug]
    body = markdown.markdown(md, extensions=MD_EXT, output_format="html5")
    body = body.replace('<h1', '<h1 class="doc-title"', 1)
    return page_html(title=title, desc=desc, canonical=f"{BASE}/{slug}/",
                     body=body, active=active(slug), crumb=MAIN_PAGES[slug][0].split("|")[0])


def render_spec(slug: str, name: str, md_text: str) -> str:
    md = rewrite_links(md_text, "specs")
    body = markdown.markdown(md, extensions=MD_EXT, output_format="html5")
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", body, re.S)
    heading = re.sub(r"<[^>]+>", "", h1.group(1)).strip() if h1 else name
    body = body.replace("<h1", '<h1 class="doc-title"', 1)
    desc = f"Спецификация функции Fonotext: {name}. Сценарий работы, данные, интерфейс, метрики приёмки и ограничения."
    return page_html(title=f"{heading} | Спецификация Fonotext",
                     desc=desc, canonical=f"{BASE}/specs/{slug}/",
                     body=body, active=active("specs/" + slug), crumb=f"Спецификации / {heading}")


def render_specs_index(md_text: str) -> str:
    md = rewrite_links(md_text, "specs")
    body = markdown.markdown(md, extensions=MD_EXT, output_format="html5")
    body = body.replace("<h1", '<h1 class="doc-title"', 1)
    return page_html(
        title="Спецификации функций | Fonotext",
        desc="12 спецификаций функций Fonotext: покрытие звонков, таксономия, контроль скриптов "
             "с доказательствами, разбор архива, выделенный шард, дашборды, интеграции.",
        canonical=f"{BASE}/specs/", body=body, active=active("specs/index"),
        crumb="Спецификации функций")


def render_index() -> str:
    cards_main = "".join(
        f'<a class="card" href="{BASE}/{slug}/"><h2>{html_mod.escape(MAIN_PAGES[slug][0])}</h2>'
        f"<p>{html_mod.escape(MAIN_PAGES[slug][1])}</p></a>"
        for section, slugs in NAV_SECTIONS for slug in slugs)
    cards_specs = "".join(
        f'<a class="card card-sm" href="{BASE}/specs/{slug}/">'
        f"<h2>{html_mod.escape(name)}</h2></a>"
        for slug, name in SPEC_ORDER)
    body = f"""<section class="hero">
<h1 class="doc-title">Документация Fonotext</h1>
<p>Fonotext — сервис речевой аналитики телефонных разговоров: расшифровка звонков со спикерами,
автоматическая классификация каждого звонка, контроль соблюдения скриптов с доказательствами
(цитата + таймкод + канал), дашборды для руководства и разбор накопленных архивов. Обработка и
хранение данных — на территории РФ (152-ФЗ). Fonotext — проект компании AXIIOM.</p>
<p class="cta"><a class="btn" href="{LANDING}" rel="noopener">Fonotext</a>
<a class="btn btn-ghost" href="{BASE}/00-product-presentation/">Начать с обзора</a></p>
</section>
<section><h2>Документация</h2><div class="grid">{cards_main}</div></section>
<section><h2>Спецификации функций</h2><div class="grid grid-sm">{cards_specs}</div></section>
"""
    return page_html(
        title="Документация Fonotext | AXIIOM",
        desc="Документация сервиса речевой аналитики Fonotext: интеграция с телефонией, "
             "архитектура, модели, безопасность и 152-ФЗ, API, план пилота и спецификации функций.",
        canonical=f"{BASE}/", body=body, active=lambda s: "", crumb="Документация")


def render_404() -> str:
    body = """<section class="hero">
<h1 class="doc-title">Страница не найдена</h1>
<p>Такой страницы в документации Fonotext нет. Выберите раздел в каталоге.</p>
<p class="cta"><a class="btn" href="/fonotext/">Каталог документации</a>
<a class="btn btn-ghost" href="/" rel="noopener">На главную axiiom.ru</a></p>
</section>"""
    return page_html(title="Страница не найдена | Fonotext",
                     desc="Страница не найдена. Каталог документации Fonotext на axiiom.ru.",
                     canonical=f"{BASE}/404.html", body=body,
                     active=lambda s: "", crumb="404")


def main() -> None:
    # Каркас
    (OUT / "assets").mkdir(parents=True, exist_ok=True)
    (OUT / "specs").mkdir(exist_ok=True)
    (OUT / ".nojekyll").write_text("")
    shutil.copy(ROOT / "mock-services" / "favicon.svg", OUT / "favicon.svg")
    shutil.copy(SRC / "style.css", OUT / "assets" / "style.css")

    hashmap: dict[str, str] = {}
    for p in sorted(SRC.glob("*.md")):
        hashmap[f"docs_{p.name.lower()}"] = hashlib.sha256(
            p.read_bytes()).hexdigest()[:8]
    for p in sorted((SRC / "specs").glob("*.md")):
        hashmap[f"docs_10-feature-specs_{p.name.lower()}"] = hashlib.sha256(
            p.read_bytes()).hexdigest()[:8]
    (OUT / "hashmap.json").write_text(
        json.dumps(hashmap, indent=1, sort_keys=True) + "\n", encoding="utf-8")

    # Страницы документации
    for slug, (_t, _d) in MAIN_PAGES.items():
        d = OUT / slug
        d.mkdir(exist_ok=True)
        (d / "index.html").write_text(
            render_doc(slug, (SRC / f"{slug}.md").read_text("utf-8")), encoding="utf-8")

    # Спецификации
    (OUT / "specs" / "index.html").write_text(
        render_specs_index((SRC / "specs" / "README.md").read_text("utf-8")),
        encoding="utf-8")
    for slug, name in SPEC_ORDER:
        (OUT / "specs" / slug).mkdir(exist_ok=True)
        (OUT / "specs" / slug / "index.html").write_text(
            render_spec(slug, name, (SRC / "specs" / f"{slug}.md").read_text("utf-8")),
            encoding="utf-8")

    # Обложка и 404
    (OUT / "index.html").write_text(render_index(), encoding="utf-8")
    (OUT / "404.html").write_text(render_404(), encoding="utf-8")

    # llms.txt — машиночитаемый каталог с актуальными URL
    lines = [
        "# Fonotext",
        "",
        "> Fonotext — сервис речевой аналитики телефонных разговоров: расшифровка звонков со",
        "> спикерами, автоматическая классификация, контроль скриптов с доказательствами,",
        "> дашборды и разбор архивов. Данные обрабатываются и хранятся в РФ (152-ФЗ).",
        "> Fonotext — проект компании AXIIOM.",
        "",
        f"Сайт проекта: {LANDING}",
        f"Документация: {SITE}{BASE}/",
        f"Репозиторий документации: https://github.com/rucorp/axiiom (каталог fonotext/)",
        "",
        "## Документы",
        "",
    ]
    for slug, (t, d) in MAIN_PAGES.items():
        lines.append(f"- [{t}]({SITE}{BASE}/{slug}/): {d}")
    lines += ["", "## Спецификации функций", ""]
    for slug, name in SPEC_ORDER:
        lines.append(f"- [{name}]({SITE}{BASE}/specs/{slug}/)")
    lines += [
        "",
        "## Правообладатель и контакты",
        "",
        f"- {ORG['name']}, {ORG['inn']}, {ORG['ogrn']}. {ORG['address']}.",
        f"- Пилот, демо, коммерческое предложение: {ORG['email']}, {ORG['phone']}.",
        "- Коммерческие условия и тарифы на сайте не публикуются — обсуждаются на пилоте.",
        "",
    ]
    (OUT / "llms.txt").write_text("\n".join(lines), encoding="utf-8")

    print(f"OK: {len(MAIN_PAGES)} docs + {len(SPEC_ORDER)} specs + index/404/llms.txt -> {OUT}")


if __name__ == "__main__":
    main()
