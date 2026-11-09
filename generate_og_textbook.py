#!/usr/bin/env python3
"""OG-картинки (1200×630) для раздела /textbook/.

Тот же визуальный язык, что generate_og_blog.py: тёмный фон, акцентная линия,
сетка, заголовок слева, геометрия справа. Бейдж — «Учебник по ИИ».
Запуск: python3 generate_og_textbook.py
Зависимость: pillow.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "og" / "textbook"
OUT.mkdir(parents=True, exist_ok=True)

BG = "#0A0A0F"
HEADING = "#F5F5F7"
MUTED = "#8E8E93"
FAINT = "#78787D"
ACCENT = "#D4A574"

PAGES = [
    ("index", "Учебник по искусственному интеллекту", "Открытый учебник · 8 глав", "axiiom.ru/textbook/"),
    ("vvedenie", "Введение", "Как устроен учебник", "axiiom.ru/textbook/vvedenie/"),
    ("glava-1-teoreticheskie-osnovy", "Теоретические основы ИИ", "Глава 1 · парадигмы и пределы", "axiiom.ru/textbook/glava-1-teoreticheskie-osnovy/"),
    ("glava-2-biologicheskie-neirony", "Биологические нейроны и их модели", "Глава 2 · от клетки к формуле", "axiiom.ru/textbook/glava-2-biologicheskie-neirony/"),
    ("glava-3-neironnye-seti", "Нейронные сети и архитектуры памяти", "Глава 3 · память и ансамбли", "axiiom.ru/textbook/glava-3-neironnye-seti/"),
    ("glava-4-obuchenie-pamyat", "Обучение, память и ассоциации", "Глава 4 · как учится мозг", "axiiom.ru/textbook/glava-4-obuchenie-pamyat/"),
    ("glava-5-raspoznavanie-obrazov", "Распознавание образов и зрение", "Глава 5 · от MDL до внимания", "axiiom.ru/textbook/glava-5-raspoznavanie-obrazov/"),
    ("glava-6-robototehnika", "Робототехника и автоматное программирование", "Глава 6 · автоматы и роботы", "axiiom.ru/textbook/glava-6-robototehnika/"),
    ("glava-7-instrumenty", "Инструменты разработки ИИ", "Глава 7 · RDK, Neuro Modeler, SDK", "axiiom.ru/textbook/glava-7-instrumenty/"),
    ("glava-8-filosofiya-etika", "Философия и этика ИИ", "Глава 8 · границы и ответственность", "axiiom.ru/textbook/glava-8-filosofiya-etika/"),
    ("materialy", "Материалы: литература, вопросы, глоссарий", "Приложение к учебнику", "axiiom.ru/textbook/materialy/"),
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

    for i in range(3):
        x, y, r = 900 + i * 40, 150 + i * 60, 200 + i * 80
        d.ellipse([x - r, y - r, x + r, y + r], outline=ACCENT, width=2)

    for x in range(0, W, 60):
        d.line([(x, 0), (x, H)], fill=(255, 255, 255, 10), width=1)
    for y in range(0, H, 60):
        d.line([(0, y), (W, y)], fill=(255, 255, 255, 10), width=1)

    f_logo = font(28, False)
    f_kicker = font(20, False)
    f_badge = font(20, False)
    f_title = font(50, True)
    f_small = font(20, False)

    d.text((60, 40), "AXIIOM", fill=HEADING, font=f_logo)
    d.text((60, 78), kicker, fill=ACCENT, font=f_kicker)

    d.rounded_rectangle([60, 118, 300, 158], radius=20, fill=ACCENT)
    d.text((80, 126), "Учебник по ИИ", fill="#0A0A0F", font=f_badge)

    y = 196
    for line in wrap(d, title, f_title, 720)[:3]:
        d.text((60, y), line, fill=HEADING, font=f_title)
        y += 60

    d.text((60, y + 34), "Модели нейрона · память · зрение · роботы · этика", fill=MUTED, font=f_small)
    d.text((60, H - 60), f"{url}  •  Раздел axiiom.ru", fill=FAINT, font=f_small)
    d.rectangle([0, H - 8, W, H], fill=ACCENT)

    d.rounded_rectangle([860, 210, 1120, 460], radius=24, outline=(255, 255, 255, 30), width=2)
    for i in range(4):
        d.rounded_rectangle([892, 250 + i * 44, 1000 + (i % 2) * 60, 274 + i * 44], radius=8,
                            fill=(255, 255, 255, 14))

    img.save(OUT / f"{slug}.png", "PNG", optimize=True)
    print("created", OUT / f"{slug}.png")


for slug, title, kicker, url in PAGES:
    draw_og(slug, title, kicker, url)
print("done")
