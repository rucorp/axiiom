#!/usr/bin/env python3
"""Generate sitemap.xml from actual site files (не из меню — чтобы ничего не терялось).

Включает все HTML-страницы сайта, исключая служебные и внутренние каталоги.
404.html и noindex-страницы в sitemap не попадают (правильная практика).

Новая логика (2026-09-11):
- Исключаем визуализации и техдоки с низким SEO-весом
- Портфолио /projects/ имеет высокий приоритет
- Приоритеты: главная 1.0, блог/индустрии/тулзы/проекты 0.9, демо/калькулятор 0.8, отраслевые/блог-посты 0.7, доки/тулзы/демки 0.6, privacy 0.3, визуализации 0.2
"""
from html.parser import HTMLParser
from pathlib import Path
import re

root = Path(__file__).resolve().parent

EXCLUDE_PARTS = (
    ".git", "node_modules", "docs/archive", "docs/source", "docs/additional",
    "docs/references", "docs/SRS-main", "_github",
    "docs/visualizations", "docs/feature-map-viz", "docs/feature-map",
)
EXCLUDE_FILES = {"test-report.html", "404.html", "feature-map.html"}  # служебные/noindex/визуализации


class HeadMetaParser(HTMLParser):
    """Read indexing directives without third-party HTML dependencies."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_head = False
        self.robots = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag.lower() == "head":
            self.in_head = True
        elif tag.lower() == "meta" and self.in_head:
            name = (attrs.get("name") or "").lower()
            if name in {"robots", "googlebot", "yandex"}:
                self.robots.append((attrs.get("content") or "").lower())

    def handle_endtag(self, tag):
        if tag.lower() == "head":
            self.in_head = False


def has_noindex(p: Path) -> bool:
    """Honor explicit noindex directives so sitemap and page policy agree."""
    parser = HeadMetaParser()
    try:
        parser.feed(p.read_text("utf-8", errors="replace"))
    except OSError:
        return False
    return any(re.search(r"(?:^|[,\s])(?:noindex|none)(?:$|[,\s])", value)
               for value in parser.robots)


def is_excluded(p: Path) -> bool:
    rel = p.relative_to(root).as_posix()
    if rel in EXCLUDE_FILES or p.name in EXCLUDE_FILES:
        return True
    # A reusable demo scaffold is not a real user-facing demo page.
    if "demo-template" in p.parts:
        return True
    return any(ex in rel for ex in EXCLUDE_PARTS)


pages = []
for p in root.rglob("*.html"):
    if is_excluded(p) or has_noindex(p):
        continue
    pages.append("/" + p.relative_to(root).as_posix())

def url_of(rel: str) -> str:
    if rel == "/index.html":
        return "https://axiiom.ru/"
    if rel.endswith("/index.html"):
        return "https://axiiom.ru" + rel[:-len("index.html")]
    return "https://axiiom.ru" + rel

priority_map = {
    "https://axiiom.ru/": 1.0,
    "https://axiiom.ru/blog/": 0.9,
    "https://axiiom.ru/industries/": 0.9,
    "https://axiiom.ru/tools/": 0.9,
    "https://axiiom.ru/projects/": 0.9,
    "https://axiiom.ru/docs/": 0.6,
    "https://axiiom.ru/mock-services/": 0.8,
    "https://axiiom.ru/demo/app/": 0.8,
    "https://axiiom.ru/calculator/": 0.8,
}
freq_map = {
    "https://axiiom.ru/": "weekly",
    "https://axiiom.ru/blog/": "weekly",
    "https://axiiom.ru/industries/": "weekly",
    "https://axiiom.ru/tools/": "weekly",
    "https://axiiom.ru/projects/": "weekly",
    "https://axiiom.ru/docs/": "monthly",
    "https://axiiom.ru/mock-services/": "weekly",
    "https://axiiom.ru/demo/app/": "monthly",
}

def prio(url: str) -> float:
    if url in priority_map:
        return priority_map[url]
    if "/blog/" in url:
        return 0.7
    if "/industries/" in url:
        return 0.7
    if "/projects/" in url:
        return 0.8
    if "/tools/" in url or "/demo/app/" in url:
        return 0.6
    if "/mock-services/" in url:
        return 0.6
    if "/docs/" in url:
        return 0.4
    if "/privacy/" in url or "/terms/" in url:
        return 0.3
    return 0.5

def freq(url: str) -> str:
    if url in freq_map:
        return freq_map[url]
    if "/blog/" in url:
        return "weekly"
    if "/docs/" in url:
        return "monthly"
    if "/mock-services/" in url:
        return "monthly"
    return "monthly"

urls = sorted({url_of(p) for p in pages})
lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
]
for u in urls:
    lines += [
        "  <url>",
        "    <loc>" + u + "</loc>",
        "    <changefreq>" + freq(u) + "</changefreq>",
        "    <priority>" + str(prio(u)) + "</priority>",
        "  </url>",
    ]
lines.append("</urlset>")

with open(root / "sitemap.xml", "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

print("sitemap.xml: " + str(len(urls)) + " URLs")
