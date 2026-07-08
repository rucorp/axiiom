#!/usr/bin/env python3
from string import Template
import os

MODULES_TMPL = Template('''
<section class="section">
<div class="container">
<h2>Что мы предлагаем</h2>
<div class="tools-grid">
${items}
</div>
</div>
</section>''')

MODULE_ITEM = '''
<div class="card reveal">
<div class="card-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 6L9 17l-5-5"/></svg></div>
<h3>${name}</h3>
<p>${desc}</p>
</div>'''

CTA_TMPL = Template('''
<section class="section cta-section">
<div class="container">
<div class="cta-card">
<h2>${title}</h2>
<p>${text}</p>
<a href="/#contact" class="btn">Обсудить проект</a>
</div>
</div>
</section>''')

FLOW_VERT = Template('''
<section class="section dark">
<div class="container">
<h2>${heading}</h2>
<div class="flow-diagram">
<div class="flow-spine"></div>
${stages}
</div>
</div>
</section>''')

FLOW_V_STAGE = '''
<div class="flow-stage reveal">
<div class="flow-node">
<div class="flow-dot"></div>
<div class="flow-card">
<h3>${title}</h3>
<p>${subtitle}</p>
</div>
</div>
<div class="flow-services">
${tags}
</div>
</div>'''

FLOW_HORZ = Template('''
<section class="section dark">
<div class="container">
<h2>${heading}</h2>
<div class="flow-horizontal">
${stages}
</div>
</div>
</section>''')

FLOW_H_STAGE = '''
<div class="flow-h-stage reveal">
<div class="flow-h-line"></div>
<div class="flow-h-card">
<h3>${title}</h3>
<p>${subtitle}</p>
</div>
<div class="flow-h-tags">
${tags}
</div>
</div>'''

base_html = Template('''<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="theme-color" content="#0A0A0F">
<title>${title} — AXIIOM</title>
<meta name="description" content="${desc}">
<link rel="canonical" href="https://axiiom.ru/industries/${slug}.html">
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "WebPage",
      "name": "${title}",
      "description": "${desc}",
      "url": "https://axiiom.ru/industries/${slug}.html",
      "isPartOf": { "@type": "WebSite", "name": "AXIIOM", "url": "https://axiiom.ru/" }
    },
    {
      "@type": "BreadcrumbList",
      "itemListElement": [
        { "@type": "ListItem", "position": 1, "name": "Главная", "item": "https://axiiom.ru/" },
        { "@type": "ListItem", "position": 2, "name": "${title}", "item": "https://axiiom.ru/industries/${slug}.html" }
      ]
    }
  ]
}
</script>
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" as="style">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<meta property="og:type" content="website">
<meta property="og:url" content="https://axiiom.ru/industries/${slug}.html">
<meta property="og:title" content="${title} — AXIIOM">
<meta property="og:description" content="${desc}">
<meta property="og:image" content="https://axiiom.ru/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="ru_RU">
<meta property="og:site_name" content="AXIIOM">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:url" content="https://axiiom.ru/industries/${slug}.html">
<meta name="twitter:title" content="${title} — AXIIOM">
<meta name="twitter:description" content="${desc}">
<meta name="twitter:image" content="https://axiiom.ru/og-image.png">
<link rel="stylesheet" href="/styles.css">
<link rel="stylesheet" href="/preloader.css">
</head>
<body>
<div id="preloader">
<script>(function(){var p=document.getElementById('preloader');if(!p)return;if(sessionStorage.getItem('_seen')){p.style.display='none';return}sessionStorage.setItem('_seen','1');var t=Date.now();p._start=t;setTimeout(function(){p.classList.add('_rdy')},500);window.addEventListener('load',function(){var e=Date.now()-t;if(e<2000){setTimeout(function(){p.classList.add('hidden');setTimeout(function(){p.classList.add('hidden-done')},500)},2000-e)}else{p.classList.add('hidden');setTimeout(function(){p.classList.add('hidden-done')},500)}})})()</script>
<svg class="preloader-svg" viewBox="0 0 36 36" width="80" height="80"><rect class="pr1" x="2" y="2" width="14" height="14" rx="2"/><rect class="pr2" x="20" y="2" width="14" height="14" rx="2"/><rect class="pr3" x="2" y="20" width="14" height="14" rx="2"/><rect class="pr4" x="20" y="20" width="14" height="14" rx="2"/><circle class="pc" cx="27" cy="27" r="3"/></svg>
</div>
<div class="noise"></div>
<div class="grid-overlay"></div>
<div class="nav-overlay" id="navOverlay">
    <ul class="nav-links" id="mobileNav"></ul>
</div>
<header class="header" id="header">
    <div class="container">
        <nav class="nav">
            <a href="/" class="logo">
                <svg width="36" height="36" viewBox="0 0 36 36" fill="none"><rect x="2" y="2" width="14" height="14" rx="2" stroke="currentColor" stroke-width="1.5" opacity=".4"/><rect x="20" y="2" width="14" height="14" rx="2" stroke="currentColor" stroke-width="1.5" opacity=".4"/><rect x="2" y="20" width="14" height="14" rx="2" stroke="currentColor" stroke-width="1.5" opacity=".4"/><rect x="20" y="20" width="14" height="14" rx="2" stroke="currentColor" stroke-width="1.5"/><circle cx="27" cy="27" r="3" fill="currentColor" opacity=".8"/></svg>
                <span>AXIIOM</span>
            </a>
            <ul class="nav-links nav-links--desktop" id="desktopNav"></ul>
            <div class="nav-actions">
                <a href="/#contact" class="btn btn-nav" id="ctaBtn">Обсудить проект</a>
                <button class="theme-btn" id="themeToggle" aria-label="Сменить тему">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"/></svg>
                </button>
                <button class="nav-toggle" id="navToggle" aria-label="Меню">
                    <span></span><span></span><span></span>
                </button>
            </div>
        </nav>
    </div>
</header>
<nav class="breadcrumbs" id="breadcrumbs" aria-label="Breadcrumb">
    <div class="container"></div>
</nav>
<section class="hero industries-hero">
<div class="container"><div class="hero-content">
<div class="hero-bg-svg"><svg width="800" height="600" viewBox="0 0 800 600" fill="none"><circle cx="400" cy="300" r="280" stroke="rgba(255,255,255,0.03)" stroke-width="1"/><circle cx="400" cy="300" r="200" stroke="rgba(255,255,255,0.04)" stroke-width="1"/><circle cx="400" cy="300" r="120" stroke="rgba(255,255,255,0.06)" stroke-width="1"/><line x1="50" y1="300" x2="750" y2="300" stroke="rgba(255,255,255,0.03)" stroke-width="1"/><line x1="400" y1="20" x2="400" y2="580" stroke="rgba(255,255,255,0.03)" stroke-width="1"/><path d="M200 300 L400 100 L600 300 L400 500 Z" stroke="rgba(255,255,255,0.04)" stroke-width="1" fill="none"/><circle cx="400" cy="300" r="4" fill="rgba(255,255,255,0.1)"/></svg></div>
<div class="badge-row"><p class="badge">Отраслевые решения</p></div>
<h1>${h1}</h1>
<p class="hero-desc">${hero}</p></div></div></section>
<section class="section"><div class="container"><h2>Решения</h2><p class="content-wrapper">${desc}</p></div></section>
${modules_html}
${flow_html}
${cta_html}
<footer class="footer">
    <div class="container">
        <div id="footerCopy"></div>
    </div>
</footer>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-HFS4BDGTV4"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag("js",new Date());gtag("config","G-HFS4BDGTV4");</script>
<script src="/metrika.js"></script>
<script src="/config.js"></script>
<script src="/nav.js"></script>
<script>Nav.init({ cta: true, breadcrumbs: true });</script>
<script src="/theme.js"></script>
<script src="/preloader.js"></script>
<script>
(function() {
  var t = document.getElementById('navToggle');
  var o = document.getElementById('navOverlay');
  if (!t || !o) return;
  t.addEventListener('click', function(e) {
    e.stopPropagation();
    o.classList.toggle('open');
    t.classList.toggle('active');
    document.body.style.overflow = o.classList.contains('open') ? 'hidden' : '';
  });
})();
</script>
<script>
var reveals = document.querySelectorAll('.reveal');
var ro = new IntersectionObserver(function(e) {
  e.forEach(function(entry) {
    if (entry.isIntersecting) { entry.target.classList.add('visible'); }
  });
}, { threshold: .15 });
reveals.forEach(function(r) { ro.observe(r); });
</script>
</body>
</html>''')

with open('industries/industries.txt', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line: continue
        parts = line.split('|')
        if len(parts) < 4: continue
        slug = parts[0]
        title = parts[1]
        desc = parts[2]
        h1 = parts[3] if len(parts) > 3 and parts[3].strip() else title
        hero = parts[4] if len(parts) > 4 and parts[4].strip() else title

        modules_html = ''
        if len(parts) > 5 and parts[5].strip():
            items = ''
            for module in parts[5].split(':::'):
                module = module.strip()
                if not module: continue
                if '::' in module:
                    m_name, m_desc = module.split('::', 1)
                    items += MODULE_ITEM.replace('${name}', m_name.strip()).replace('${desc}', m_desc.strip())
            if items:
                modules_html = MODULES_TMPL.substitute(items=items)

        cta_html = ''
        if len(parts) > 6 and parts[6].strip():
            cta_parts = parts[6].split('::', 1)
            cta_title = cta_parts[0].strip()
            cta_text = cta_parts[1].strip() if len(cta_parts) > 1 else 'Оставьте заявку — мы свяжемся с вами в ближайшее время.'
            cta_html = CTA_TMPL.substitute(title=cta_title, text=cta_text)

        flow_html = ''
        if len(parts) > 7 and parts[7].strip():
            raw = parts[7].strip()
            flow_type = 'vertical'
            flow_heading = 'Путь заказа'

            if raw.startswith('vertical:::'):
                flow_type = 'vertical'
                raw = raw[len('vertical:::'):]
            elif raw.startswith('horizontal:::'):
                flow_type = 'horizontal'
                flow_heading = 'Маршрут'
                raw = raw[len('horizontal:::'):]

            stages = ''
            for stage in raw.split(':::'):
                stage = stage.strip()
                if not stage: continue
                parts_s = stage.split('::')
                if len(parts_s) >= 2:
                    s_title = parts_s[0].strip()
                    s_sub = parts_s[1].strip()
                    s_tags = parts_s[2].strip() if len(parts_s) > 2 else ''
                    tags_html = ''.join(f'<span class="tag">{t.strip()}</span>' for t in s_tags.split(',') if t.strip())
                    if flow_type == 'horizontal':
                        stages += FLOW_H_STAGE.replace('${title}', s_title).replace('${subtitle}', s_sub).replace('${tags}', tags_html)
                    else:
                        stages += FLOW_V_STAGE.replace('${title}', s_title).replace('${subtitle}', s_sub).replace('${tags}', tags_html)

            if stages:
                if flow_type == 'horizontal':
                    flow_html = FLOW_HORZ.substitute(heading=flow_heading, stages=stages)
                else:
                    flow_html = FLOW_VERT.substitute(heading=flow_heading, stages=stages)

        html = base_html.substitute(slug=slug, title=title, desc=desc, h1=h1, hero=hero, modules_html=modules_html, flow_html=flow_html, cta_html=cta_html)
        with open(f'industries/{slug}.html', 'w', encoding='utf-8') as fw:
            fw.write(html)
print('Pages generated')
