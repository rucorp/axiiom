#!/usr/bin/env python3
"""inject_metrika_noscript.py — канонический noscript-фолбэк Яндекс.Метрики.

Добавляет после открытия <body> канонический блок Метрики 109391253:

    <noscript><div><img src="https://mc.yandex.ru/watch/109391253"
    style="position:absolute;left:-9999px" alt=""></div></noscript>

на все страницы, где подключена Метрика:

  * корневые/корпоративные HTML с явным <script src="/metrika.js">;
  * mock-services/ — HTML, где Метрика подключается через analytics.js
    (динамическая загрузка /metrika.js). Как и patch_mock_services_seo.py,
    скрипт нужно перезапустить после обновления VitePress-сборки.

fonotext/ пропускается: там тот же блок вставляется шаблоном
fonotext/src/build.py и переживает пересборку сам.

Скрипт идемпотентен: страницы, где блок уже есть, не трогаются.

Запуск: python3 inject_metrika_noscript.py   (из корня репозитория)
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

NOSCRIPT = (
    '<noscript><div><img src="https://mc.yandex.ru/watch/109391253" '
    'style="position:absolute;left:-9999px" alt=""></div></noscript>'
)

BODY_RE = re.compile(r"(<body[^>]*>)", re.IGNORECASE)


def main() -> None:
    touched, skipped = [], []
    for f in sorted(ROOT.rglob("*.html")):
        parts = f.relative_to(ROOT).parts
        if not parts or parts[0] in (".git", "node_modules", "archive") \
                or "_github" in parts or parts[0] == "fonotext":
            continue
        html = f.read_text("utf-8", errors="replace")
        if "mc.yandex.ru/watch/109391253" in html:
            skipped.append(f)
            continue
        # цель — страницы с Метрикой: явный metrika.js или mock-services
        # (там metrika.js загружается через analytics.js)
        has_metrika = "/metrika.js" in html or parts[0] == "mock-services"
        if not has_metrika:
            continue
        new, n = BODY_RE.subn(lambda m: m.group(1) + NOSCRIPT, html, count=1)
        if n:
            f.write_text(new, encoding="utf-8")
            touched.append(f)
    print(f"✅ noscript добавлен: {len(touched)} страниц")
    print(f"⏭ уже был: {len(skipped)} страниц")


if __name__ == "__main__":
    main()
