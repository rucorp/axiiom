# AXIIOM — Repository Reference for AI Agents

## Quick Facts
- **Domain:** https://axiiom.ru (CNAME: `axiiom.ru`)
- **Company:** ООО «Аксиома» / AXIIOM, founded 2004, SPb & Moscow
- **Stack:** Static site, vanilla HTML/CSS/JS, built with `build.py` (esbuild `--minify --charset=utf8`) from `nav.src.js`/`styles.src.css` sources; artifacts `nav.js` and `styles.css` are minified single-line files
- **Deploy:** `nginx:alpine` Docker image, copies files to `/usr/share/nginx/html`, port 80
- **Language:** Russian (content), English (brand name)
- **Analytics:** Yandex Metrika `109391253` + Google Analytics `G-HFS4BDGTV4`

---

## Directory Structure

```
axiiom/
├── config.js                      # Global config (company, legal, analytics IDs)
├── styles.css                     # Design system (minified, ~35.8 KB, sources in styles.src.css)
├── nav.js                         # Universal navigation tree + renderer (minified, ~15.8 KB, source in nav.src.js)
├── theme.js                       # Dark/light theme toggle with localStorage
├── footer.js                      # Footer rendering
├── preloader.js / preloader.css   # Animated preloader
├── build.py                       # Build pipeline: minify + ?v= cache-bust + node --check + test_site.py
├── nav.src.js                     # Source for nav.js (pre-minify)
├── styles.src.css                 # Source for styles.css (pre-minify)
├── DESIGN.md                      # Design system contract
├── test_site.py                   # 79-page regression suite
├── test-report.html               # Latest test report output
├── generate_sitemap.py            # Sitemap generator
├── fill_industries.py             # Industry data helper
├── Makefile                       # Build/test automation
├── index.html                     # Homepage (929 lines, hero, services, cases, etc.)
├── 404.html                       # Custom 404 with nav + analytics
├── favicon.svg / og-image.png     # Brand assets
├── robots.txt / sitemap.xml       # SEO
├── Dockerfile                     # nginx:alpine deployment
│
├── blog/                          # Content marketing (7 posts)
│   ├── index.html                 # Blog listing (dynamic from posts.js)
│   ├── posts.js                   # POSTS array (slug, title, date, desc)
│   └── {slug}/index.html          # Each post is a subdirectory
│
├── tools/                         # 12 utility tools
│   ├── index.html                 # Tools listing page
│   └── {tool-name}/index.html     # Each is a standalone HTML app
│                                  # (tool-specific styles live in main styles.css)
│
├── industries/                    # 23 industry solution pages
│   ├── index.html                 # Industries listing
│   ├── nav.js                     # Industries-specific nav
│   ├── industries.txt             # Source data (pipe-delimited)
│   ├── generate_industries.py     # Auto-generator from template
│   └── {slug}.html                # Flat HTML files (not subdirs)
│
├── calculator/
│   └── index.html                 # Interactive cost estimator (985 lines)
│
├── demo/app/                      # 16 interactive demos
│   ├── index.html                 # Demo hub listing (751 lines)
│   ├── generate_demos.py          # Auto-generator from DEMOS array
│   ├── demo-template/             # Reusable SPA template
│   └── {demo-slug}/               # Each demo has index.html
│
├── privacy/  → index.html         # Privacy policy (noindex)
├── terms/    → index.html         # Terms of service (noindex)
└── docs/                          # Docs site: ~30 subpages incl. visualizations/ and feature-map-viz/
```

---

## Navigation System (`nav.js`)

The `TREE` array (lines 4-137) defines all navigation items:

```js
var TREE = [
  { name: 'Главная', path: '/', children: [...] },           // 8 anchors to #sections
  { name: 'Отраслевые решения', path: '/industries/', ... }, // 23 industries
  { name: 'Блог', path: '/blog/', ... },                     // 7 blog posts
  { name: 'Инструменты', path: '/tools/', ... },             // 12 tools
  { name: 'Калькулятор', path: '/calculator/' },             // No children
  { name: 'Демо-платформы', path: '/demo/app/', ... },      // 30+ items with groups
  { name: 'Контакты', path: '/#contact' },                   // Anchor link
  // footerOnly items:
  { name: 'Политика конфиденциальности', path: '/privacy/', footerOnly: true },
  { name: 'Пользовательское соглашение', path: '/terms/', footerOnly: true }
];
```

Special node properties:
- `footerOnly: true` — only in footer, not in nav bars
- `header: true` — group header in mega-dropdown (no link)
- `separator: true` — divider line in dropdown
- `children.length > 15` → gets `mega` class (wider dropdown for Industries, Demos)

Each page calls:
```js
Nav.init({ cta: true/false, breadcrumbs: true/false });
```

Required DOM IDs: `desktopNav`, `mobileNav`, `breadcrumbs`, `footerCopy`, `navToggle`, `navOverlay`, `header`.

---

## Design System (`styles.css`)

CSS custom properties on `:root` define the theme:

| Variable | Dark | Light |
|----------|------|-------|
| `--clr-bg` | `#0A0A0F` | `#F5F5F7` |
| `--clr-surface` | `#12121A` | `#FFFFFF` |
| `--clr-text` | `#C7C7CC` | `#1D1D1F` |
| `--clr-heading` | `#F5F5F7` | `#1D1D1F` |
| `--clr-accent` | `#D4A574` (gold) | `#A67A45` |
| `--clr-accent2` | `#8B9D83` (sage) | `#6B7D63` |

Font: `Inter` (400, 500, 600, 700) from Google Fonts.

---

## Adding a New Blog Post

1. Create directory `blog/{slug}/`
2. Copy `index.html` from an existing post (it's a full HTML file)
3. Update: `<title>`, `<meta name="description">`, canonical URL, OG/Twitter tags, JSON-LD, breadcrumbs, article content
4. Add entry to `blog/posts.js` (slug, title, date, desc)
5. Add to `nav.js` TREE under blog children
6. Add to `sitemap.xml`

---

## Adding a New Industry Page

1. Edit `industries/industries.txt` — add line: `slug|Title|Description|Hero Text`
2. Run: `cd axiiom && python3 generate_industries.py`
3. Add to `nav.js` TREE under industries children
4. Add to `sitemap.xml`

---

## Adding a New Tool

1. Create `tools/{tool-name}/index.html` (standalone HTML app)
2. Add card to `tools/index.html` — find the tools grid and add a new `.tool-card`
3. Add to `nav.js` TREE under tools children
4. Add to `sitemap.xml`

---

## Adding a New Demo

1. Edit `demo/app/generate_demos.py` — add entry to `DEMOS` array with slug, title, desc, features, tags, code, widget_html
2. Run: `cd axiiom/demo/app && python3 generate_demos.py`
3. Add to `nav.js` TREE under demo children (add to the right group)
4. Add to `sitemap.xml`

---

## Key Patterns

### Page Template
Every page includes (in order):
```html
<script src="/config.js"></script>
<link rel="stylesheet" href="/preloader.css">
<link rel="stylesheet" href="/styles.css">
<!-- header/nav HTML -->
<div class="noise"></div>
<div class="grid-overlay"></div>
<header class="header" id="header">...<nav>...</nav></header>
<nav class="breadcrumbs" id="breadcrumbs">...</nav>
<div class="nav-overlay" id="navOverlay">...</div>
<!-- page content -->
<footer class="footer">...</footer>
<script>Nav.init({...})</script>
<script src="/theme.js"></script>
<script src="/footer.js"></script>
<!-- Yandex Metrika + Google Analytics -->
<!-- preloader HTML + init script -->
```

### Preloader
- Hidden via `sessionStorage.getItem('_seen')` after first visit
- Shows for min 2 seconds on first load
- Has `.hidden` → `.hidden-done` CSS transition

---

## Known Issues / Gotchas

1. ~~**sitemap.xml** had a duplicate homepage entry — RESOLVED: sitemap now has 79 unique URLs, no duplicates~~
2. **sitemap.xml** doesn't include demo subpages (only `/demo/app/`) — should add individual demo URLs
3. ~~**nav.js** had a Cyrillic URL `dostavka-ed%D1%8B.html` — RESOLVED: file renamed to `dostavka-edy.html`, sitemap updated~~
4. **Industry pages** are `.html` flat files (not `index.html` in subdirs) — inconsistent with blog/demo pattern
5. ~~**Industry nav.js** loads separately at `/industries/nav.js` with `initIndustriesNav()` — not using the main Nav system~~ RESOLVED: both `/industries/nav.js` and `/tools/nav.js` were removed; all sections now use the unified `/nav.js` Nav system
6. ~~**Tools nav.js** loads separately at `/tools/nav.js` — also not using main Nav~~ RESOLVED (see #5)
7. ~~**Performance:** no critical CSS inlining — RESOLVED: critical CSS is now inlined in `index.html` `<head>` (restored), and `styles.css` loads with `media="print"` `onload` trick on `index.html` and `calculator/index.html`. Preloader still shows on every page load unless `_seen` is set.~~
8. **No 301 redirects** — if pages move, old URLs will 404
9. **404.html** is a full page but Nginx needs explicit `error_page 404` config (not in Dockerfile)
10. **Demo pages** are generated with embedded widget HTML/CSS/JS inside `generate_demos.py` — hard to edit individually
11. **No service worker** — no offline support or caching strategy beyond browser defaults
12. **Footer** is rendered twice on some pages (from `nav.js` `_renderFooter` + `footer.js`)
13. **Versioning script** must preserve `media="print"` `onload` on `styles.css` links and the inline critical CSS in `index.html` — both were accidentally destroyed once by automated versioning and restored

---

## SEO Architecture

- Full Open Graph + Twitter Card meta on every page
- JSON-LD structured data: Organization, BreadcrumbList, Article, FAQPage, WebPage, CollectionPage
- Canonical URLs on all pages
- `robots.txt`: allows all, disallows `/admin/` and `/demo/*/admin/`
- Privacy/Terms pages: `<meta name="robots" content="noindex, follow">`
- Sitemap: 79 URLs (main, 23 industries, 12 tools, 7 blog, calculator, demo hub, 16 demos, docs pages, privacy, terms)

---

## External Services

- **Lovii ecosystem** — loyalty platform product at `lovii.ru`, linked from demos section
- **GitHub Pages** — various portfolio projects hosted at `bestdeejay-design.github.io/{project}/`
- **Own projects:** `univerid.ru`, `dajet.ru`, `hype-marketplace-1.web.app`

---

## Contact / Config

From `config.js`:
```js
window.AXIIOM_CONFIG = {
  company: { name: 'AXIIOM', nameRu: 'ООО Аксиома', domain: 'axiiom.ru', ... },
  contact: { email: 'hello@axiiom.ru', phone: '+7 (812) 928-74-78', telegram: 'https://t.me/axiiom' },
  address: { spb: 'СПб, Большой В.О. пр-кт, 83А, офис 329', msk: 'Москва, ул. Перерва, д. 16' },
  legal: { inn: '7842223709', ogrn: '1247800067690', ... },
  analytics: { yandexMetrika: '109391253', googleAnalytics: 'G-HFS4BDGTV4' }
};
```

---

## Active Issues / Tasks Remaining

1. Add individual demo subpage URLs to sitemap.xml
2. Consider normalizing URL structure (industries should use subdirectories instead of `.html`)
3. Set up Nginx error_page 404 config in Dockerfile
4. Clean up footer double-rendering issue
5. `test_site.py --dynamic` flag validates both themes (14/14 PASS)
