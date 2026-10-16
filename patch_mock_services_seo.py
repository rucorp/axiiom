#!/usr/bin/env python3
"""Post-process the checked-in VitePress export for consistent SEO metadata.

The upstream repository contains the Markdown documentation but not the website
build configuration. Run this after refreshing mock-services/ so static HTML,
client-side page data and their content-addressed URLs stay in sync.
"""

import ast
from html import escape
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "mock-services"
ASSETS = SITE / "assets"

# title, description — written for search snippets and kept deliberately factual.
SEO = {
    ".": (
        "Моки банков и касс для тестирования API | AXIIOM",
        "Открытый тестовый стенд AXIIOM: моки эквайринга, онлайн-касс и ОФД по публичным API-протоколам. Быстрый запуск, сценарии и гайды интеграции.",
    ),
    "AGENTS": (
        "Правила ИИ-агентов для mock-services | AXIIOM",
        "Правила для ИИ-агентов, работающих с репозиторием mock-services: структура проекта, ограничения, проверки, ссылки на документацию и безопасные изменения.",
    ),
    "CHANGELOG": (
        "История изменений mock-services | AXIIOM",
        "История изменений mock-services AXIIOM: версии, новые банковские и кассовые адаптеры, изменения API и обновления тестового стенда.",
    ),
    "CONTRIBUTING": (
        "Как участвовать в mock-services | AXIIOM",
        "Как внести вклад в mock-services AXIIOM: настройка окружения, требования к изменениям, запуск проверок и подготовка pull request.",
    ),
    "SECURITY": (
        "Безопасность mock-services — рекомендации по запуску | AXIIOM",
        "Практические правила безопасности mock-services: ограничения тестового стенда, безопасная конфигурация, запуск в Docker и сообщение об уязвимостях.",
    ),
    "docs/capabilities": (
        "Моки банков, касс и ОФД — матрица возможностей | AXIIOM",
        "Сравните возможности 10 mock-адаптеров AXIIOM: банки, платежные сервисы, онлайн-кассы и ОФД, поддерживаемые сценарии и ограничения.",
    ),
    "docs/hardening": (
        "Безопасный запуск mock-services в Docker | AXIIOM",
        "Как безопасно запускать mock-services в Docker: контейнерные ограничения, graceful shutdown и согласованные настройки для сервисов.",
    ),
    "docs/integration/alfa": (
        "Мок Альфа-Банк REST API — тестирование эквайринга | AXIIOM",
        "Руководство по тестированию интернет-эквайринга Альфа-Банка через mock: REST API, регистрация платежа, перенаправление и callback-сценарии.",
    ),
    "docs/integration/atol": (
        "Мок АТОЛ Онлайн API v4 — тестирование кассы | AXIIOM",
        "Интеграция с mock АТОЛ Онлайн API v4: получение токена, тестовые фискальные операции и обработка ответа кассы по протоколу ФФД 1.05.",
    ),
    "docs/integration/ferma-ofd": (
        "OFD Ferma — интеграция облачной кассы через mock | AXIIOM",
        "Проверьте интеграцию OFD Ferma через mock: получение токена, продажи и возвраты, отчёты и callback-уведомления в тестовом контуре.",
    ),
    "docs/integration/first-ofd": (
        "Первый ОФД OKassa — интеграция через mock | AXIIOM",
        "Инструкция по интеграции с тестовой OKassa Первого ОФД: авторизация, запросы к API и обработка документов в локальном mock-сервисе.",
    ),
    "docs/integration/kontur-ofd": (
        "Контур.ОФД API — тестирование чтения данных | AXIIOM",
        "Тестируйте чтение фискальных данных из Контур.ОФД через mock: авторизация, организации, кассы, документы и разбор ошибок API.",
    ),
    "docs/integration/sber": (
        "Мок Сбербанк Ecom REST API v1.1.11.1 | AXIIOM",
        "Мок Сбербанк Ecom REST v1.1.11.1 для проверки платежной интеграции: тестовые запросы, callbacks, ответы API и сценарии отказа.",
    ),
    "docs/integration/taxcom": (
        "Такском API v2 — интеграция через mock | AXIIOM",
        "Интеграция read-only API Такском v2 через mock: авторизация, создание сессии и тестирование чтения аккаунтов и фискальных документов.",
    ),
    "docs/integration/tbank-eacq": (
        "Мок Т-Банк EACQ API — тестирование эквайринга | AXIIOM",
        "Проверьте интеграцию Т-Банк EACQ через mock: Init, платёжная форма, уведомления, Confirm/Cancel, проверка счёта и E2C-выплаты.",
    ),
    "docs/integration/vtb": (
        "Мок ВТБ SMB E-commerce API — тестирование | AXIIOM",
        "Интеграция ВТБ SMB E-commerce API через mock-сервис: тестирование REST-запросов, платежных сценариев и обработки callback.",
    ),
    "docs/integration/yookassa": (
        "Мок ЮKassa API v3 — тестирование платежей | AXIIOM",
        "Тестируйте API ЮKassa /v3 через mock: создание и подтверждение платежей, отмена операций и возвраты в тестовом контуре.",
    ),
    "docs/overview": (
        "Документация мок-сервисов: быстрый старт и интеграции | AXIIOM",
        "Карта документации mock-services AXIIOM: быстрый запуск, возможности тестовых банковских и кассовых API, инструкции и ссылки на адаптеры.",
    ),
    "docs/rfc/RFC-001-multi-tenant-sandboxes": (
        "RFC-001: изоляция песочниц mock-сервиса | AXIIOM",
        "RFC-001 описывает изоляцию песочниц в публичном mock-сервисе: архитектурное решение, ограничения и статус реализации мультиарендности.",
    ),
    "docs/roadmap": (
        "Дорожная карта mock-services | AXIIOM",
        "План развития mock-services AXIIOM: завершённые этапы, текущий статус и запланированные направления для банковских и кассовых адаптеров.",
    ),
    "docs/tables": (
        "Таблицы и API mock-services | AXIIOM",
        "Справочник таблиц документации mock-services: таблицы из руководств, описаний API и сервисов, собранные в одном реестре и проверяемые автоматически.",
    ),
    "packages/core/README": (
        "Ядро mock-services — документация | AXIIOM",
        "Документация ядра mock-services: общие HTTP-инструменты, состояние и сценарии, используемые банковскими и кассовыми адаптерами.",
    ),
    "services/alfa-mock/README": (
        "alfa-mock — эмулятор Альфа-Банк REST API | AXIIOM",
        "alfa-mock эмулирует REST API интернет-эквайринга Альфа-Банка (*.do). Описание запросов, ответов, тестовых сценариев и запуска локального сервиса.",
    ),
    "services/atol-mock/README": (
        "atol-mock — эмулятор АТОЛ Онлайн API v4 | AXIIOM",
        "atol-mock — тестовый эмулятор АТОЛ Онлайн API v4 (ФФД 1.05). Изучите эндпоинты, форматы запросов, примеры и настройки запуска.",
    ),
    "services/first-ofd-mock/README": (
        "first-ofd-mock — эмулятор ОФД OKassa | AXIIOM",
        "first-ofd-mock эмулирует OKassa Первого ОФД: документация API, авторизация, сценарии обработки и запуск тестовой кассы.",
    ),
    "services/kassa-mock/README": (
        "kassa-mock — эмулятор облачной кассы OFD Ferma | AXIIOM",
        "kassa-mock эмулирует облачную кассу OFD Ferma: инструкция по API, токену, продажам, возвратам, отчётам и запуску mock-сервиса.",
    ),
    "services/kontur-ofd-mock/README": (
        "kontur-ofd-mock — эмулятор Контур.ОФД API | AXIIOM",
        "kontur-ofd-mock — read-only эмулятор Контур.ОФД для сверки фискальных документов. API, авторизация и запуск локального тестового сервиса.",
    ),
    "services/sber-mock/README": (
        "sber-mock — эмулятор Сбербанк Ecom REST API | AXIIOM",
        "sber-mock — эмулятор Сбербанк Ecom REST v1.1.11.1 для тестирования эквайринга. Описание API, callbacks, сценарии и запуск.",
    ),
    "services/taxcom-mock/README": (
        "taxcom-mock — эмулятор Такском API v2 | AXIIOM",
        "taxcom-mock — read-only эмулятор Такском API v2 для чтения данных ОФД. Документация авторизации, запросов, документов и запуска.",
    ),
    "services/tbank-mock/README": (
        "tbank-mock — эмулятор Т-Банк EACQ API | AXIIOM",
        "tbank-mock эмулирует API Т-Банк эквайринга, Мультирасчётов и E2C. Документация сценариев, эндпоинтов и запуска тестового сервиса.",
    ),
    "services/vtb-mock/README": (
        "vtb-mock — эмулятор ВТБ SMB E-commerce API | AXIIOM",
        "vtb-mock эмулирует ВТБ SMB E-commerce API: документация платежных запросов, ответов, callback и запуска локального тестового сервиса.",
    ),
    "services/yookassa-mock/README": (
        "yookassa-mock — эмулятор ЮKassa REST API v3 | AXIIOM",
        "yookassa-mock — эмулятор REST API ЮKassa /v3. Инструкция по платежам, подтверждению, отмене, возвратам и запуску тестового сервиса.",
    ),
}

OG_IMAGE = "https://axiiom.ru/og-image.png"


def route_key(page):
    rel = page.parent.relative_to(SITE).as_posix()
    return "." if rel == "." else rel


def bundle_prefix(route):
    if route == ".":
        return "index.md"
    return route.replace("/", "_") + ".md"


def source_key(route):
    return bundle_prefix(route).lower()


def page_url(route):
    return "https://axiiom.ru/mock-services/" + ("" if route == "." else route + "/")


def upsert_meta(content, attr, key, value):
    escaped = escape(value, quote=True)
    pattern = rf'<meta\s+{attr}="{re.escape(key)}"\s+content=".*?"\s*/?>'
    tag = f'<meta {attr}="{key}" content="{escaped}">'
    if re.search(pattern, content, flags=re.S):
        return re.sub(pattern, tag, content, count=1, flags=re.S)
    return content.replace("</head>", "    " + tag + "\n  </head>", 1)


def page_schema(route, title, description):
    url = page_url(route)
    if route == ".":
        schema = {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "WebSite",
                    "@id": "https://axiiom.ru/mock-services/#website",
                    "url": "https://axiiom.ru/mock-services/",
                    "name": "Mock Services AXIIOM",
                    "description": description,
                    "inLanguage": "ru-RU",
                    "publisher": {"@type": "Organization", "name": "AXIIOM", "url": "https://axiiom.ru/"},
                },
                {
                    "@type": "SoftwareSourceCode",
                    "@id": "https://axiiom.ru/mock-services/#software",
                    "name": "mock-services AXIIOM",
                    "description": description,
                    "url": "https://axiiom.ru/mock-services/",
                    "codeRepository": "https://github.com/rucorp/mock-services",
                    "programmingLanguage": "JavaScript",
                    "runtimePlatform": "Node.js",
                    "license": "https://www.apache.org/licenses/LICENSE-2.0",
                    "inLanguage": "ru-RU",
                },
            ],
        }
    else:
        schema = {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "@id": url + "#webpage",
            "url": url,
            "name": title,
            "description": description,
            "inLanguage": "ru-RU",
            "isPartOf": {"@id": "https://axiiom.ru/mock-services/#website"},
            "publisher": {"@type": "Organization", "name": "AXIIOM", "url": "https://axiiom.ru/"},
        }
    return schema


def update_html(page, route, title, description):
    content = page.read_text(encoding="utf-8")
    content, title_count = re.subn(r"<title>.*?</title>", f"<title>{escape(title, quote=False)}</title>", content, count=1, flags=re.S)
    if title_count != 1:
        raise ValueError(f"title не найден: {page}")
    content = upsert_meta(content, "name", "description", description)
    url = page_url(route)
    props = {
        "og:title": title,
        "og:description": description,
        "og:url": url,
        "og:type": "website",
        "og:site_name": "AXIIOM — Mock Services",
        "og:locale": "ru_RU",
        "og:image": OG_IMAGE,
        "og:image:width": "1200",
        "og:image:height": "630",
        "og:image:alt": "Документация AXIIOM о тестовых mock-сервисах",
    }
    names = {
        "twitter:card": "summary_large_image",
        "twitter:title": title,
        "twitter:description": description,
        "twitter:image": OG_IMAGE,
        "twitter:url": url,
    }
    for key, value in props.items():
        content = upsert_meta(content, "property", key, value)
    for key, value in names.items():
        content = upsert_meta(content, "name", key, value)

    schema = json.dumps(page_schema(route, title, description), ensure_ascii=False, separators=(",", ":"))
    script = '<script type="application/ld+json">' + schema + "</script>"
    ld_pattern = r'<script\s+type="application/ld\+json">.*?</script>'
    if re.search(ld_pattern, content, flags=re.S):
        content = re.sub(ld_pattern, script, content, count=1, flags=re.S)
    else:
        content = content.replace("</head>", "    " + script + "\n  </head>", 1)
    # VitePress's default title template appends site.title to page.title.
    # Keep the visible site brand and dynamic browser title aligned with our HTML.
    escaped_quote = chr(92) + '"'
    content = content.replace(escaped_quote + 'title' + escaped_quote + ':' + escaped_quote + 'mock-services' + escaped_quote,
                              escaped_quote + 'title' + escaped_quote + ':' + escaped_quote + 'AXIIOM' + escaped_quote)
    content = content.replace(escaped_quote + 'siteTitle' + escaped_quote + ':' + escaped_quote + 'mock-services' + escaped_quote,
                              escaped_quote + 'siteTitle' + escaped_quote + ':' + escaped_quote + 'AXIIOM' + escaped_quote)
    content = content.replace("analytics.js?v=20260916", "analytics.js?v=20261016")
    page.write_text(content, encoding="utf-8")


def page_data_asset(asset):
    """Return (JSON page data, start, end, quote) from VitePress's JSON.parse string."""
    marker = "JSON.parse("
    start = asset.index(marker) + len(marker)
    quote = asset[start]
    if quote not in ("'", '"'):
        raise ValueError("неизвестное quoting в VitePress page bundle")
    pos = start + 1
    escaped = False
    while pos < len(asset):
        char = asset[pos]
        if escaped:
            escaped = False
        elif char == "\\":
            escaped = True
        elif char == quote:
            break
        pos += 1
    if pos >= len(asset):
        raise ValueError("не закрыта строка JSON.parse в page bundle")
    literal = quote + asset[start + 1:pos] + quote
    decoded = ast.literal_eval(literal)
    return json.loads(decoded), start + 1, pos, quote


def replace_page_data_asset(asset, title, description):
    data, start, end, quote = page_data_asset(asset)
    data["title"] = title
    data["description"] = description
    serialized = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    js_string = serialized.replace("\\", "\\\\").replace(quote, "\\" + quote)
    return asset[:start] + js_string + asset[end:]


def main():
    pages = {route_key(page): page for page in SITE.rglob("index.html")}
    if set(pages) != set(SEO):
        raise SystemExit(f"Набор mock-страниц изменился: ожидается {sorted(SEO)}, найдено {sorted(pages)}")

    hash_path = SITE / "hashmap.json"
    hash_map = json.loads(hash_path.read_text(encoding="utf-8"))
    replacements = {}

    for route, (title, description) in SEO.items():
        if not 100 <= len(description) <= 160:
            raise SystemExit(f"Description {route}: {len(description)} символов")
        page = pages[route]
        update_html(page, route, title, description)

        key = source_key(route)
        old_hash = hash_map.get(key)
        if not old_hash:
            raise SystemExit(f"hashmap.json не содержит {key}")
        prefix = bundle_prefix(route)
        full_path = ASSETS / f"{prefix}.{old_hash}.js"
        lean_path = ASSETS / f"{prefix}.{old_hash}.lean.js"
        if not full_path.is_file() or not lean_path.is_file():
            raise SystemExit(f"VitePress bundles не найдены для {key}.{old_hash}")
        # VitePress appends the global site title; keep the bundle title suffix-free.
        dynamic_title = title.removesuffix(" | AXIIOM")
        full = replace_page_data_asset(full_path.read_text(encoding="utf-8"), dynamic_title, description)
        lean = replace_page_data_asset(lean_path.read_text(encoding="utf-8"), dynamic_title, description)
        new_hash = hashlib.sha256((key + "\0" + full + "\0" + lean).encode("utf-8")).hexdigest()[:8]
        replacements[old_hash] = new_hash
        for old_path, text, suffix in ((full_path, full, ".js"), (lean_path, lean, ".lean.js")):
            new_path = ASSETS / f"{prefix}.{new_hash}{suffix}"
            new_path.write_text(text, encoding="utf-8")
        hash_map[key] = new_hash

    if len(set(replacements.values())) != len(replacements):
        raise SystemExit("Коллизия новых hash-идентификаторов VitePress bundles")

    # Every prerendered route embeds the complete hash map for SPA navigation.
    hash_pattern = re.compile("|".join(re.escape(value) for value in sorted(replacements, key=len, reverse=True)))
    for page in SITE.rglob("*.html"):
        content = page.read_text(encoding="utf-8", errors="replace")
        content = hash_pattern.sub(lambda match: replacements[match.group(0)], content)
        page.write_text(content, encoding="utf-8")

    hash_path.write_text(json.dumps(hash_map, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"SEO post-process: {len(pages)} prerendered pages and client-side page bundles updated")


if __name__ == "__main__":
    main()
