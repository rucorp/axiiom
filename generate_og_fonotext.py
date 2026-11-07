#!/usr/bin/env python3
"""OG-картинки (1200×630) для раздела /fonotext/ и его страниц.

По образцу generate_og_help.py (тот же визуальный язык, что и generate_og.py
для /industries/): тёмный фон, акцентная линия, сетка, заголовок слева,
геометрия справа. Заголовки и описания берутся из собранных страниц
fonotext/**/index.html (мета og:title / og:description), поэтому генератор
запускается после fonotext/src/build.py.

Запуск: python3 generate_og_fonotext.py
Зависимость: pillow.
"""
from __future__ import annotations

import html as html_mod
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "og" / "fonotext"
OUT.mkdir(parents=True, exist_ok=True)

BG = "#0A0A0F"
HEADING = "#F5F5F7"
MUTED = "#8E8E93"
ACCENT = "#D4A574"
BASE = "/fonotext"

FONT_CANDIDATES = {
    True: [  # bold
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold Italic.ttf",
    ],
    False: [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    ],
}

_font_cache: dict[tuple[int, bool], ImageFont.FreeTypeFont] = {}


def font(size: int, bold: bool = True) -> ImageFont.FreeTypeFont:
    key = (size, bold)
    if key in _font_cache:
        return _font_cache[key]
    for path in FONT_CANDIDATES[bold]:
        try:
            fnt = ImageFont.truetype(path, size)
            _font_cache[key] = fnt
            return fnt
        except OSError:
            continue
    raise SystemExit("Не найден TTF-шрифт с кириллицей (DejaVu/Arial)")


def wrap(draw: ImageDraw.ImageDraw, text: str, fnt, limit: int) -> list[str]:
    words, lines, cur = text.split(), [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if draw.textbbox((0, 0), test, font=fnt)[2] > limit and cur:
            lines.append(cur)
            cur = w
        else:
            cur = test
    if cur:
        lines.append(cur)
    return lines


def og_image_name(canonical: str) -> str:
    """Согласовано с og_image() в fonotext/src/build.py."""
    rel = canonical[len(BASE):].strip("/")
    if rel == "":
        return "index"
    if rel == "specs":
        return "specs-index"
    return rel.replace("/", "-")


def collect_pages() -> list[tuple[str, str, str, str]]:
    """(имя файла, title, desc, url-подпись) из собранных fonotext-страниц."""
    pages = []
    for path in sorted((ROOT / "fonotext").rglob("index.html")):
        text = path.read_text(encoding="utf-8")
        title = re.search(r'<meta property="og:title" content="([^"]*)"', text)
        desc = re.search(r'<meta property="og:description" content="([^"]*)"', text)
        url = re.search(r'<meta property="og:url" content="([^"]*)"', text)
        if not (title and desc and url):
            raise SystemExit(f"Нет og-мета на {path}")
        canonical = url.group(1)
        if not canonical.startswith("https://axiiom.ru" + BASE):
            continue
        name = og_image_name(canonical[len("https://axiiom.ru"):])
        pages.append((name, title.group(1), desc.group(1),
                      canonical[len("https://axiiom.ru/"):]))
    return pages


def draw_og(name: str, title: str, desc: str, url: str) -> None:
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # геометрия справа (как в generate_og.py / generate_og_help.py)
    for i in range(3):
        x, y, r = 900 + i * 40, 150 + i * 60, 200 + i * 80
        d.ellipse([x - r, y - r, x + r, y + r], outline=ACCENT, width=2)

    # сетка
    for x in range(0, W, 60):
        d.line([(x, 0), (x, H)], fill=(255, 255, 255, 10), width=1)
    for y in range(0, H, 60):
        d.line([(0, y), (W, y)], fill=(255, 255, 255, 10), width=1)

    f_logo = font(28, False)
    f_kicker = font(20, False)
    f_title = font(52, True)
    f_desc = font(24, False)
    f_small = font(20, False)

    d.text((60, 40), "AXIIOM", fill=HEADING, font=f_logo)
    d.text((60, 78), "Fonotext · речевая аналитика звонков", fill=ACCENT, font=f_kicker)
    d.line([(60, 130), (320, 130)], fill=ACCENT, width=3)

    y = 170
    for line in wrap(d, title, f_title, 700)[:3]:
        d.text((60, y), line, fill=HEADING, font=f_title)
        y += 64

    y += 16
    for line in wrap(d, desc, f_desc, 700)[:3]:
        d.text((60, y), line, fill=MUTED, font=f_desc)
        y += 34

    d.text((60, H - 60), url, fill=MUTED, font=f_small)

    img.save(OUT / f"{name}.png")


def main() -> None:
    pages = collect_pages()
    for name, title, desc, url in pages:
        draw_og(name, html_mod.unescape(title), html_mod.unescape(desc), url)
        print(f"og/fonotext/{name}.png  <-  {title}")
    print(f"Итого: {len(pages)} картинок")


if __name__ == "__main__":
    main()
