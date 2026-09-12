#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import os

# Ensure dir
os.makedirs('og/industries', exist_ok=True)

# Define categories colors
CAT_COLORS = {
    'Fintech': ('#0A0A0F', '#D4A574'),
    'HoReCa & Retail': ('#0E0E14', '#FF8A65'),
    'B2B & Enterprise': ('#12121A', '#8B9D83'),
    'SaaS & Digital': ('#0A0A0F', '#64B5F6'),
    'Security & Fintech': ('#0A0A0F', '#EF5350'),
}

# Load titles
titles = {}
cats = {}
try:
    with open('industries/industries.txt', encoding='utf-8') as f:
        for line in f:
            parts=line.strip().split('|')
            if len(parts)>=4:
                titles[parts[0]] = parts[1]
except:
    pass

# category map same as generator
CATEGORY_MAP = {
    'avtomatizaciya-restoranov': 'HoReCa & Retail',
    'dostavka-edy': 'HoReCa & Retail',
    'fitness-apps': 'HoReCa & Retail',
    'bronirovanie-gostinits': 'HoReCa & Retail',
    'kiberbezopasnost': 'Security & Fintech',
    'kyc-onboarding': 'Fintech',
    'multi-currency-wallet': 'Fintech',
    'p2p-marketplace': 'Fintech',
    'trading-engine': 'Fintech',
    'investment-crm': 'Fintech',
    'real-time-analytics': 'Fintech',
    'asset-tokenization': 'Fintech',
    'kraudfanding': 'Fintech',
    'crm-medcentry': 'B2B & Enterprise',
    'crm-nedvizhimost': 'B2B & Enterprise',
    'po-stroitelnye-kompanii': 'B2B & Enterprise',
    'erp-proizvodstvo': 'B2B & Enterprise',
    'sistemy-logistika': 'B2B & Enterprise',
    'upravlenie-cepochkami': 'B2B & Enterprise',
    'pravovie-firmu': 'B2B & Enterprise',
    'avtoservice': 'B2B & Enterprise',
    'hr-podbor-personala': 'B2B & Enterprise',
    'selskokhozyaystvo': 'B2B & Enterprise',
    'saas-startupy': 'SaaS & Digital',
    'online-obuchenie': 'SaaS & Digital',
    'platforma-frilans': 'SaaS & Digital',
    'iot-umnyy-dom': 'SaaS & Digital',
    'marketing-analitika': 'SaaS & Digital',
    'upravlenie-proektami': 'SaaS & Digital',
    'udalennaya-rabota': 'SaaS & Digital',
    'fintech': 'Fintech',
    'horeca': 'HoReCa & Retail',
    'b2b': 'B2B & Enterprise',
    'saas': 'SaaS & Digital',
    'security': 'Security & Fintech',
}

PRICE_MAP = {
    'Fintech': 'от 2 млн ₽',
    'HoReCa & Retail': 'от 400к ₽',
    'B2B & Enterprise': 'от 800к ₽',
    'SaaS & Digital': 'от 600к ₽',
    'Security & Fintech': 'от 500к ₽',
}

def draw_og(slug, title, category, price):
    W, H = 1200, 630
    bg_color, accent = CAT_COLORS.get(category, ('#0A0A0F', '#D4A574'))
    # Create image
    img = Image.new('RGB', (W, H), bg_color)
    draw = ImageDraw.Draw(img)
    # Gradient-like circles
    for i in range(3):
        x = 900 + i*40
        y = 150 + i*60
        r = 200 + i*80
        # draw semi-transparent circle via ellipse with low alpha? Use overlay
        # Simple: draw ellipse outline
        draw.ellipse([x-r, y-r, x+r, y+r], outline=accent, width=2)
    # Grid overlay
    for x in range(0, W, 60):
        draw.line([(x,0),(x,H)], fill=(255,255,255,10), width=1)
    for y in range(0, H, 60):
        draw.line([(0,y),(W,y)], fill=(255,255,255,10), width=1)

    # Try to load font
    try:
        # Use DejaVu if available
        font_bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 56)
        font_regular = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
    except:
        font_bold = ImageFont.load_default()
        font_regular = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # AXIIOM logo text top left
    draw.text((60, 40), "AXIIOM", fill="#F5F5F7", font=font_regular)
    draw.text((200, 44), f"• {category}", fill=accent, font=font_small)

    # Price badge
    draw.rounded_rectangle([60, 100, 60+200, 140], radius=20, fill=accent)
    draw.text((80, 108), f"MVP {price}", fill="#0A0A0F", font=font_small)

    # Title - wrap
    # Simple wrap by words
    words = title.split()
    lines = []
    cur = ""
    for w in words:
        test = cur + " " + w if cur else w
        # estimate width
        bbox = draw.textbbox((0,0), test, font=font_bold)
        if bbox[2]-bbox[0] > 700:
            lines.append(cur)
            cur = w
        else:
            cur = test
    if cur:
        lines.append(cur)
    # Limit to 3 lines
    lines = lines[:3]
    y = 170
    for line in lines:
        draw.text((60, y), line, fill="#F5F5F7", font=font_bold)
        y += 70

    # Subtitle
    draw.text((60, y+10), "Разработка под ключ • 50+ проектов • 99.99% uptime", fill="#8E8E93", font=font_small)

    # Bottom trust
    draw.text((60, H-60), f"axiiom.ru/industries/{slug}  •  Обсудим за 1 час", fill="#78787D", font=font_small)

    # Accent line bottom
    draw.rectangle([0, H-8, W, H], fill=accent)

    # Icon right side - simple geometric
    # Draw a rounded rect as mockup
    draw.rounded_rectangle([850, 180, 1120, 450], radius=24, outline=(255,255,255,30), width=2)
    draw.rounded_rectangle([880, 210, 1090, 260], radius=12, fill=(255,255,255,20))
    draw.rounded_rectangle([880, 280, 1000, 310], radius=8, fill=(255,255,255,10))
    draw.rounded_rectangle([880, 330, 1050, 360], radius=8, fill=(255,255,255,10))

    return img

all_slugs = list(CATEGORY_MAP.keys())
for slug in all_slugs:
    cat = CATEGORY_MAP.get(slug, 'B2B & Enterprise')
    title = titles.get(slug, slug.replace('-', ' ').title())
    if slug in ('fintech','horeca','b2b','saas','security'):
        # category titles
        cat_titles = {
            'fintech': 'Fintech — 8 решений для банков и бирж',
            'horeca': 'HoReCa — автоматизация ресторанов и отелей',
            'b2b': 'B2B — 10 решений CRM, ERP, логистика',
            'saas': 'SaaS — 7 платформ для стартапов',
            'security': 'Security — кибербезопасность бизнеса',
        }
        title = cat_titles.get(slug, title)
    price = PRICE_MAP.get(cat, 'от 600к ₽')
    img = draw_og(slug, title, cat, price)
    out_path = f'og/industries/{slug}.png'
    img.save(out_path, 'PNG', optimize=True)
    print(f'Created {out_path} — {cat} — {title[:40]}')

print('Done OG generation')
