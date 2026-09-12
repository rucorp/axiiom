#!/usr/bin/env python3
import os, re

BLOG_LINKS = {
    'highload-architecture': [
        ('/industries/trading-engine.html', 'Торговый движок 100k RPS на Go — разработка биржи'),
        ('/industries/real-time-analytics.html', 'Real-time аналитика на ClickHouse и Kafka'),
        ('/industries/saas-startupy.html', 'SaaS для стартапов — мультитенантность и K8s'),
        ('/industries/fintech/', 'Все Fintech-решения AXIIOM — 8 кейсов'),
    ],
    'pci-dss-compliance': [
        ('/industries/multi-currency-wallet.html', 'Мультивалютный кошелёк с PCI DSS и SBP'),
        ('/industries/kyc-onboarding.html', 'KYC и онбординг по 161-ФЗ'),
        ('/industries/p2p-marketplace.html', 'P2P-маркетплейс с escrow и PCI DSS'),
        ('/industries/fintech/', 'Fintech разработка — 8 решений'),
    ],
    'fintech-trends-2026': [
        ('/industries/kyc-onboarding.html', 'KYC и онбординг — верификация по 161-ФЗ'),
        ('/industries/multi-currency-wallet.html', 'Мультивалютный кошелёк с SBP/QR/NFC'),
        ('/industries/trading-engine.html', 'Торговый движок — разработка биржи'),
        ('/industries/fintech/', 'Все Fintech-решения →'),
        ('/calculator/?industry=fintech', 'Рассчитать стоимость Fintech-проекта в калькуляторе'),
    ],
    'loyalty-program-roi': [
        ('/industries/avtomatizaciya-restoranov.html', 'Автоматизация ресторанов с CRM LOVII и KDS'),
        ('/industries/dostavka-edy.html', 'Доставка еды с трекингом и лояльностью'),
        ('/industries/fitness-apps.html', 'Фитнес-приложения с геймификацией'),
        ('/industries/horeca/', 'HoReCa решения — 4 кейса'),
    ],
    '161-fz-guideline': [
        ('/industries/kyc-onboarding.html', 'KYC и онбординг по 161-ФЗ — от 2 млн ₽'),
        ('/industries/multi-currency-wallet.html', 'Мультивалютный кошелёк с 161-ФЗ и PCI DSS'),
        ('/industries/trading-engine.html', 'Торговый движок с KYC/AML и аудит-логом'),
        ('/industries/fintech/', 'Fintech — 8 решений с 161-ФЗ'),
        ('/calculator/?industry=kyc-onboarding', 'Калькулятор стоимости KYC-проекта'),
    ],
    'mobile-payment-ux': [
        ('/industries/multi-currency-wallet.html', 'Мультивалютный кошелёк — SBP, QR, NFC, Apple Pay'),
        ('/industries/avtomatizaciya-restoranov.html', 'Автоматизация ресторанов — QR-оплата и кэшбэк'),
        ('/industries/dostavka-edy.html', 'Доставка еды — трекинг и оплата'),
        ('/industries/fintech/', 'Fintech UX — 8 решений'),
    ],
    'loyalty-platform-not-option-necessity': [
        ('/industries/avtomatizaciya-restoranov.html', 'Автоматизация ресторанов с LOVII лояльностью'),
        ('/industries/dostavka-edy.html', 'Доставка еды — программа лояльности'),
        ('/industries/crm-nedvizhimost.html', 'CRM для недвижимости с лояльностью'),
        ('/industries/horeca/', 'HoReCa и Retail — 4 решения'),
        ('/demo/app/loyalty-program/', 'Демо: программа лояльности'),
    ],
}

for slug, links in BLOG_LINKS.items():
    path = f'blog/{slug}/index.html'
    if not os.path.exists(path):
        print(f'skip {path}')
        continue
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    # build block
    links_html = "\n".join([f'<li><a href="{href}" class="link-accent">{text}</a></li>' for href, text in links])
    block = f'''
<div class="glass-card card-pad-md" style="margin-top:32px">
<p class="label">Читайте также — решения AXIIOM</p>
<h3 style="font-size:1.1rem;margin-bottom:12px;color:var(--clr-heading)">Вам может пригодиться</h3>
<ul style="padding-left:20px;margin:0">
{links_html}
</ul>
<p style="margin-top:16px;font-size:.85rem;color:var(--clr-muted)">Или <a href="/calculator/" class="link-accent">рассчитайте стоимость</a> и <a href="/industries/" class="link-accent">посмотрите все 30 решений</a> • <a href="/projects/" class="link-accent">Портфолио 50+ проектов</a></p>
</div>
'''
    # inject before closing </div> of article-wrap (first occurrence after content)
    # find last </div> before </div> </div> of article-wrap
    # Simple: replace the pattern </div>\n        </div>\n    </div>\n</section> with block + that
    if 'Читайте также — решения AXIIOM' in content:
        print(f'already has links {slug}')
        continue
    # Insert before closing of inner div (the article content div)
    # Look for pattern: </div>\n        </div>\n    </div>\n</section>
    target = '</div>\n        </div>\n    </div>\n</section>'
    if target in content:
        content = content.replace(target, block + '\n</div>\n        </div>\n    </div>\n</section>', 1)
    else:
        # fallback: insert before </section> after article-wrap
        content = content.replace('</section>\n</main>', block + '\n</section>\n</main>', 1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'injected {slug} with {len(links)} links')

print('done')
