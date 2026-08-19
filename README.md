![AXIIOM](assets/header.svg)

# AXIIOM

Fintech development: websites, mobile apps, UI/UX design.

**🌐 Versions:** [English](README.md) · [Русский](README.ru.md) · [Website](https://axiiom.ru)

[![Static Site](https://img.shields.io/badge/site-static%20HTML%2FCSS%2FJS-blue)](https://axiiom.ru)
[![Accessibility](https://img.shields.io/badge/Lighthouse%20a11y-100-brightgreen)](https://axiiom.ru)
[![SEO](https://img.shields.io/badge/Lighthouse%20SEO-100-brightgreen)](https://axiiom.ru)
[![Pages Checked](https://img.shields.io/badge/test_site-79%20pages%20%2F%203476%20checks-brightgreen)](https://axiiom.ru)
[![License](https://img.shields.io/badge/license-MIT-blue)](https://axiiom.ru)
[![Deploy](https://img.shields.io/badge/deploy-nginx%3Aalpine-blue)](https://axiiom.ru)

## Status

| Check | Result |
|---|---|
| `test_site.py` pages | 79 |
| `test_site.py` checks | 3476 |
| `test_site.py` failed | 0 |
| `test_site.py` run count | 3232 passed / 244 warnings |
| Lighthouse accessibility | 100 |
| Lighthouse SEO | 100 |

## About

AXIIOM (ООО «Аксиома») is a Russian fintech development company founded in 2004, with offices in Saint Petersburg and Moscow. The company builds fintech solutions: payment systems, loyalty platforms, and credit conveyors. Services include websites, mobile apps, and UI/UX design. The site content is written in Russian.

This repository is the source of the public website [https://axiiom.ru](https://axiiom.ru). It is a pure static site with no backend framework.

## Quick start

Run a local copy with any static server:

```bash
python3 -m http.server 8000
# then open http://localhost:8000
```

Or build the production bundle and serve it with nginx via Docker:

```bash
python3 build.py
docker build -t axiiom .
docker run -p 8080:80 axiiom
```

## Build

`build.py` minifies the source assets with esbuild and produces the deployable output:

```bash
python3 build.py
```

## Repository structure

```
axiiom/
├── build.py                 # esbuild minification + build pipeline
├── nav.src.js               # navigation source (rendered by nav.js)
├── styles.src.css           # stylesheet source (CSS tokens in DESIGN.md)
├── DESIGN.md                # design system, CSS tokens, dark/light theme
├── test_site.py             # site checker (79 pages, 3476 checks)
├── config.js                # site configuration
├── theme.js                 # dark/light theme switch
├── preloader.js             # page preloader
├── metrika.js               # Yandex Metrika integration
├── footer.js                # footer rendering
├── index.html               # homepage
├── 404.html                 # error page
├── industries/              # 23 industry pages
├── blog/                    # 7 blog posts
├── tools/                   # 12 tools
├── calculator/              # calculator page
├── demo/app/                # 16 demo pages
├── docs/                    # documentation
├── privacy/                 # privacy policy
├── terms/                   # terms of use
├── robots.txt
├── sitemap.xml              # 79 URLs
├── Dockerfile               # nginx:alpine deploy image
├── Makefile
├── CNAME                    # axiiom.ru
└── assets/                  # generated SVG (header.svg, footer.svg)
```

## Stack

- **Vanilla HTML/CSS/JS** with no frontend framework.
- **esbuild** minification driven by `build.py`.
- **nginx:alpine** Docker image for deployment.
- **Yandex Metrika** and **Google Analytics** for analytics (`metrika.js`).
- **CSS design tokens** for the dark/light theme, documented in `DESIGN.md`.
- Navigation is rendered by `nav.js` from the `nav.src.js` source.

## Deployment

The site is published at [https://axiiom.ru](https://axiiom.ru) (set in `CNAME`). Set the GitHub Pages homepage to the same URL in the repository About section.

## Keywords

fintech, static site, design system, accessibility, UI/UX, payment systems, loyalty platforms, credit conveyors.

![AXIIOM](assets/footer.svg)
