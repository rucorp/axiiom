#!/usr/bin/env python3
"""OG-картинки (1200×630) для раздела /help/ и его статей.

Тот же визуальный язык, что и в generate_og.py для /industries/:
тёмный фон, акцентная линия, сетка, название раздела слева и геометрия справа.
Запуск: python3 generate_og_help.py
Зависимость: pillow.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "og" / "help"
OUT.mkdir(parents=True, exist_ok=True)

BG = "#0A0A0F"
HEADING = "#F5F5F7"
MUTED = "#8E8E93"
FAINT = "#78787D"
ACCENT = "#D4A574"

PAGES = [
    ("index", "Помощь малому бизнесу", "Внешний CTO · аудит · ИИ", "axiiom.ru/help/"),
    ("diagnostika", "Диагностика и аудит", "Карта техдолга за 2–3 недели", "axiiom.ru/help/diagnostika/"),
    ("cto", "Внешний технический директор", "Технология целиком", "axiiom.ru/help/cto/"),
    ("ai-transformaciya", "ИИ-трансформация", "Пилоты с замером за 90 дней", "axiiom.ru/help/ai-transformaciya/"),
    ("vneshniy-cto-malyy-biznes", "Когда бизнесу нужен внешний CTO", "Разбор · 6 признаков", "axiiom.ru/blog/"),
    ("diagnostika-tehdolga", "Диагностика техдолга", "Как считаем цену", "axiiom.ru/blog/"),
    ("ai-transformaciya-90-dney", "ИИ за 90 дней", "Как считать эффект", "axiiom.ru/blog/"),
]


def font(size, bold=True):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    try:
        return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/{name}", size)
    except OSError:
        return ImageFont.load_default()


def wrap(draw, text, fnt, limit):
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


def draw_og(slug, title, kicker, url):
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # геометрия справа (как в generate_og.py)
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
    f_badge = font(20, False)
    f_title = font(52, True)
    f_small = font(20, False)

    d.text((60, 40), "AXIIOM", fill=HEADING, font=f_logo)
    d.text((60, 78), kicker, fill=ACCENT, font=f_kicker)

    # бейдж раздела
    d.rounded_rectangle([60, 118, 300, 158], radius=20, fill=ACCENT)
    d.text((80, 126), "Помощь бизнесу", fill="#0A0A0F", font=f_badge)

    y = 196
    for line in wrap(d, title, f_title, 700)[:3]:
        d.text((60, y), line, fill=HEADING, font=f_title)
        y += 64

    d.text((60, y + 34), "Без штатного CTO · фиксированный результат", fill=MUTED, font=f_small)
    d.text((60, H - 60), f"{url}  •  Обсудим за 20 минут", fill=FAINT, font=f_small)
    d.rectangle([0, H - 8, W, H], fill=ACCENT)

    # правая «карточка» с планом
    d.rounded_rectangle([850, 200, 1120, 470], radius=24, outline=(255, 255, 255, 30), width=2)
    d.rounded_rectangle([880, 230, 1090, 274], radius=12, fill=(255, 255, 255, 20))
    for i in range(3):
        d.rounded_rectangle([880, 300 + i * 46, 1010 + i * 20, 326 + i * 46], radius=8,
                            fill=(255, 255, 255, 12))

    img.save(OUT / f"{slug}.png", "PNG", optimize=True)
    print("created", OUT / f"{slug}.png")


for slug, title, kicker, url in PAGES:
    draw_og(slug, title, kicker, url)
print("done")
