#!/usr/bin/env python3
"""Generate sitemap.xml from actual site files (не из меню — чтобы ничего не терялось).

Включает все HTML-страницы сайта, исключая служебные и внутренние каталоги.
404.html и noindex-страницы в sitemap не попадают (правильная практика).
"""
from datetime import datetime, timezone
from pathlib import Path

root = Path(__file__).resolve().parent

EXCLUDE_PARTS = (
    ".git", "node_modules", "docs/archive", "docs/source", "docs/additional",
    "docs/references", "docs/SRS-main", "_github",
)
EXCLUDE_FILES = {"test-report.html", "404.html"}  # служебные/noindex

def is_excluded(p: Path) -> bool:
    rel = p.relative_to(root).as_posix()
    if rel in EXCLUDE_FILES:
        return True
    return any(ex in rel for ex in EXCLUDE_PARTS)

pages = []
for p in root.rglob("*.html"):
    if is_excluded(p):
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
    "https://axiiom.ru/docs/": 0.9, "https://axiiom.ru/blog/": 0.9,
    "https://axiiom.ru/industries/": 0.9, "https://axiiom.ru/tools/": 0.9,
    "https://axiiom.ru/demo/app/": 0.8, "https://axiiom.ru/calculator/": 0.8,
}
freq_map = {
    "https://axiiom.ru/": "weekly",
    "https://axiiom.ru/docs/": "weekly", "https://axiiom.ru/blog/": "weekly",
    "https://axiiom.ru/industries/": "weekly", "https://axiiom.ru/tools/": "weekly",
    "https://axiiom.ru/demo/app/": "monthly",
}

def prio(url: str) -> float:
    if url in priority_map:
        return priority_map[url]
    if "/blog/" in url or "/industries/" in url:
        return 0.7
    if "/docs/" in url or "/tools/" in url or "/demo/app/" in url:
        return 0.6
    if "/privacy/" in url or "/terms/" in url:
        return 0.3
    return 0.5

def freq(url: str) -> str:
    if url in freq_map:
        return freq_map[url]
    return "weekly" if "/blog/" in url else "monthly"

today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

urls = sorted({url_of(p) for p in pages})
lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
]
for u in urls:
    lines += [
        "  <url>",
        "    <loc>" + u + "</loc>",
        "    <lastmod>" + today + "</lastmod>",
        "    <changefreq>" + freq(u) + "</changefreq>",
        "    <priority>" + str(prio(u)) + "</priority>",
        "  </url>",
    ]
lines.append("</urlset>")

with open(root / "sitemap.xml", "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

print("sitemap.xml: " + str(len(urls)) + " URLs")
