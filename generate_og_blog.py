#!/usr/bin/env python3
"""OG-картинки (1200×630) для старых постов блога (issue #18).

Тот же визуальный язык, что и в generate_og_help.py / generate_og.py:
тёмный фон, акцентная линия, сетка, заголовок слева и геометрия справа.
Запуск: python3 generate_og_blog.py
Зависимость: pillow.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "og" / "blog"
OUT.mkdir(parents=True, exist_ok=True)

BG = "#0A0A0F"
HEADING = "#F5F5F7"
MUTED = "#8E8E93"
FAINT = "#78787D"
ACCENT = "#D4A574"

POSTS = [
    ("161-fz-guideline", "161-ФЗ: руководство для финтех-стартапов", "Финтех · комплаенс", "axiiom.ru/blog/161-fz-guideline/"),
    ("fintech-trends-2026", "Главные тренды финтеха в 2026 году", "Финтех · аналитика", "axiiom.ru/blog/fintech-trends-2026/"),
    ("highload-architecture", "Архитектура highload-систем", "Опыт AXIIOM · highload", "axiiom.ru/blog/highload-architecture/"),
    ("loyalty-platform-not-option-necessity", "Платформа лояльности — не опция, а необходимость", "Лояльность · платформы", "axiiom.ru/blog/loyalty-platform-not-option-necessity/"),
    ("loyalty-program-roi", "Как окупается платформа лояльности: расчёт ROI", "Лояльность · экономика", "axiiom.ru/blog/loyalty-program-roi/"),
    ("mobile-payment-ux", "UX платёжных мобильных приложений", "Мобильные платежи · UX", "axiiom.ru/blog/mobile-payment-ux/"),
    ("pci-dss-compliance", "PCI DSS: сертификация без потери денег и репутации", "Безопасность · PCI DSS", "axiiom.ru/blog/pci-dss-compliance/"),
]


def font(size, bold=True):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    for path in (f"/usr/share/fonts/truetype/dejavu/{name}",
                 "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold
                 else "/System/Library/Fonts/Supplemental/Arial.ttf"):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
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
    d.rounded_rectangle([60, 118, 280, 158], radius=20, fill=ACCENT)
    d.text((80, 126), "Блог AXIIOM", fill="#0A0A0F", font=f_badge)

    y = 196
    for line in wrap(d, title, f_title, 700)[:3]:
        d.text((60, y), line, fill=HEADING, font=f_title)
        y += 64

    d.text((60, y + 34), "Разбираем на практике · опыт проектов AXIIOM", fill=MUTED, font=f_small)
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


for slug, title, kicker, url in POSTS:
    draw_og(slug, title, kicker, url)
print("done")
