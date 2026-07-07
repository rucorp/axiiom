#!/usr/bin/env python3
"""
test_site.py — AXIIOM site validator

Source of truth: nav.js TREE. Only validates pages users see.
Automatically discovers new pages added to TREE.

Usage:
    python3 test_site.py
    python3 test_site.py --serve
    python3 test_site.py --output report.html --exit-code
"""

import argparse
import json
import os
import re
import sys
import urllib.request
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote

SITE_ROOT = Path(__file__).resolve().parent
DEFAULT_OUTPUT = SITE_ROOT / "test-report.html"
LIVE_URL = "http://axiiom-dev.orb.local"

# ——————————————————————————————————————————————————————
# nav.js TREE parser
# ——————————————————————————————————————————————————————

def parse_tree(nav_path):
    """Parse nav.js TREE into a flat list of {path, name, parent, parent_name}.
    Uses brace-counting to correctly handle nested objects."""
    raw = nav_path.read_text("utf-8")
    start = raw.index("var TREE = [") + len("var TREE = [")
    depth = 1  # we already consumed the opening [
    i = start
    while i < len(raw):
        c = raw[i]
        if c == "[":
            depth += 1
        elif c == "]":
            depth -= 1
            if depth == 0:
                break
        i += 1
    tree_js = raw[start:i]

    pages = []

    def extract_objects(text, parent_path=None, parent_name=None):
        """Extract top-level object blocks from text using brace counting."""
        i = 0
        while i < len(text):
            # Find next '{'
            brace_start = text.find("{", i)
            if brace_start == -1:
                break
            depth = 0
            j = brace_start
            while j < len(text):
                c = text[j]
                if c == "{": depth += 1
                elif c == "}":
                    depth -= 1
                    if depth == 0:
                        block = text[brace_start + 1:j]
                        name_m = re.search(r"name:\s*'([^']*)'", block)
                        path_m = re.search(r"path:\s*'([^']+)'", block)
                        name = name_m.group(1) if name_m else ""
                        path = path_m.group(1) if path_m else ""
                        if path and not path.startswith("http") and not path.startswith("https") and "#" not in path:
                            norm = path.rstrip("/") if path != "/" else "/"
                            pages.append({
                                "path": norm,
                                "name": name,
                                "parent": parent_path,
                                "parent_name": parent_name,
                            })
                        ch_start = block.find("children:")
                        if ch_start != -1:
                            arr_start = block.index("[", ch_start)
                            arr_depth = 1
                            k = arr_start + 1
                            while k < len(block):
                                ck = block[k]
                                if ck == "[": arr_depth += 1
                                elif ck == "]":
                                    arr_depth -= 1
                                    if arr_depth == 0:
                                        children_text = block[arr_start + 1:k]
                                        extract_objects(children_text, path, name)
                                        break
                                k += 1
                        i = j + 1
                        break
                j += 1
            else:
                break  # malformed
        return

    extract_objects(tree_js)
    return pages


# ——————————————————————————————————————————————————————
# Page classification from TREE
# ——————————————————————————————————————————————————————

def build_page_registry(nav_path):
    """Build dict mapping URL → {type, name, parent_type, parent_name}
    using nav.js TREE plus hardcoded entry points."""
    tree_pages = parse_tree(nav_path)

    # Classify each page based on its parent in the TREE
    reg = {}

    # Entry points not in TREE
    reg["/"] = {"type": "landing", "name": "Главная"}
    reg["/404.html"] = {"type": "404", "name": "404"}
    reg["/blog"] = {"type": "blog-index", "name": "Блог"}
    reg["/industries"] = {"type": "industry-index", "name": "Решения"}
    reg["/tools"] = {"type": "tool-index", "name": "Инструменты"}
    reg["/docs"] = {"type": "docs-index", "name": "Документация"}
    reg["/demo/app"] = {"type": "demo-index", "name": "Демо"}

    for tp in tree_pages:
        url = tp["path"]
        parent = (tp.get("parent") or "").rstrip("/")
        parent_name = tp.get("parent_name")
        name = tp.get("name", "")

        # Determine type from parent
        ptype = "other"
        if parent == "":
            ptype = "top-level"  # top-level nav items
        elif parent == "/industries":
            ptype = "industry"
        elif parent == "/tools":
            ptype = "tool-sub"
        elif parent == "/docs":
            ptype = "docs"
        elif parent == "/blog" or parent_name == "Статьи":
            ptype = "blog"
        elif parent == "/demo/app":
            ptype = "demo-sub"
        elif url == "/calculator":
            ptype = "calculator"
        elif url in ("/privacy", "/terms"):
            ptype = "legal"
        else:
            ptype = "other"

        # URL-pattern overrides (take priority over parent-based)
        if url.startswith("/blog/"):
            ptype = "blog"
        if url == "/":
            ptype = "root"
        elif url == "/docs":
            ptype = "docs-index"
        elif url == "/blog":
            ptype = "blog-index"
        elif url == "/tools":
            ptype = "tool-index"
        elif url == "/industries":
            ptype = "industry-index"
        elif url == "/demo/app":
            ptype = "demo-index"
        elif url == "/calculator":
            ptype = "calculator"
        elif url == "/privacy" or url == "/terms":
            ptype = "legal"

        reg[url] = {"type": ptype, "name": name}

    return reg


# ——————————————————————————————————————————————————————
# Known URLs → filesystem resolution
# ——————————————————————————————————————————————————————

def resolve_page_path(site_root, url):
    """Given a normalized URL like /docs/srs-v2, return the expected filesystem path."""
    url = url.rstrip("/")
    candidates = [
        site_root / url.lstrip("/") / "index.html",
        site_root / (url.lstrip("/") + ".html"),
        site_root / url.lstrip("/"),
    ]
    for c in candidates:
        if c.is_file():
            return c.resolve()
    # Try URL-decoded version
    try:
        decoded = unquote(url.lstrip("/"))
        c2 = site_root / decoded
        if c2.is_file():
            return c2.resolve()
        c3 = site_root / decoded / "index.html"
        if c3.is_file():
            return c3.resolve()
    except Exception:
        pass
    return None


def discover_project_pages(site_root, page_registry):
    """Find all HTML files matching registered URLs."""
    pages = []
    for url, info in page_registry.items():
        fpath = resolve_page_path(site_root, url)
        if fpath is None:
            pages.append({
                "path": None,
                "rel": None,
                "url": url,
                "type": info["type"],
                "name": info["name"],
                "content": None,
                "missing": True,
            })
            continue
        rel = fpath.relative_to(site_root).as_posix()
        try:
            content = fpath.read_text("utf-8", errors="replace")
        except Exception:
            content = None
        pages.append({
            "path": fpath,
            "rel": rel,
            "url": url,
            "type": info["type"],
            "name": info["name"],
            "content": content,
            "missing": False,
        })
    return pages


# ——————————————————————————————————————————————————————
# Feature baselines PER PAGE TYPE
# ——————————————————————————————————————————————————————

FEATURES = {
    "doctype":       "HTML5 DOCTYPE",
    "lang-ru":       "lang='ru' on <html>",
    "charset":       "meta charset UTF-8",
    "viewport":      "meta viewport",
    "theme-color":   "meta theme-color",
    "description":   "meta description",
    "title":         "<title> tag",
    "canonical":     "link canonical",
    "robots-correct":"robots meta correct",
    "og-title":      "og:title",
    "og-desc":       "og:description",
    "og-url":        "og:url",
    "og-type":       "og:type",
    "og-image":      "og:image",
    "twitter-card":  "twitter:card",
    "twitter-title": "twitter:title",
    "twitter-desc":  "twitter:description",
    "twitter-img":   "twitter:image",
    "json-ld":       "JSON-LD structured data",
    "fonts":         "Google Fonts preconnect/load",
    "styles-css":    "styles.css",
    "preloader-css": "preloader.css",
    "favicon":       "favicon",
    "preloader":     "preloader div",
    "noise":         "noise overlay div",
    "grid-overlay":  "grid-overlay div",
    "nav-overlay":   "navOverlay",
    "mobile-nav":    "mobileNav ul",
    "header":        "header element",
    "desktop-nav":   "desktopNav ul",
    "nav-toggle":    "navToggle button",
    "footer":        "footer element",
    "footer-copy":   "footerCopy div",
    "breadcrumbs":   "breadcrumbs nav",
    "cta-btn":       "CTA button",
    "nav-js":        "/nav.js script",
    "theme-js":      "/theme.js script",
    "config-js":     "/config.js script",
    "preloader-js":  "/preloader.js script",
    "nav-init":      "Nav.init() call",
    "gtag":          "Google Analytics",
    "ym":            "Yandex Metrika",
    "content-marker":"Type-specific content section",
    "hero-svg":      "Hero SVG animation (if hero exists)",
    "links":         "No broken internal links",
}


def baseline(page_type):
    """Return dict of feature → 'required' | 'optional' | 'no' for a page type.
    
    STANDARD TEMPLATE (all user-facing pages must match):
    - Structure: doctype, lang, charset, viewport
    - SEO: title, description, canonical, OG (5), Twitter (4)
    - JSON-LD (BreadcrumbList + WebPage/Article)
    - Styles: fonts, styles.css, preloader.css, favicon
    - Components: preloader, noise, grid-overlay, nav-overlay, mobile-nav,
      header, desktop-nav, nav-toggle, footer, footer-copy, breadcrumbs, cta-btn
    - Scripts: nav.js, Nav.init(), theme.js, preloader.js, gtag, ym
    - Content: type-specific section marker
    - Links: no broken internal links
    
    Deviations only for pages that are NOT part of the site template.
    """
    b = {}
    ALL_REQUIRED = [
        "doctype", "lang-ru", "charset", "viewport", "theme-color", "description",
        "title", "canonical", "og-title", "og-desc", "og-url", "og-type", "og-image",
        "twitter-card", "twitter-title", "twitter-desc", "twitter-img",
        "json-ld", "fonts", "styles-css", "preloader-css", "favicon",
        "preloader", "noise", "grid-overlay", "nav-overlay", "mobile-nav",
        "header", "desktop-nav", "nav-toggle", "footer", "footer-copy",
        "breadcrumbs", "cta-btn",
        "nav-js", "theme-js", "preloader-js", "gtag", "ym",
        "nav-init", "content-marker", "hero-svg", "links",
    ]
    for f in ALL_REQUIRED:
        b[f] = "required"
    b["config-js"] = "required"

    # --- EXCEPTIONS (pages that opt OUT of standard template) ---
    if page_type == "demo-sub":
        # Standalone app pages — not part of site template
        for k in b:
            b[k] = "no"

    elif page_type == "anchor":
        for k in b:
            b[k] = "no"

    elif page_type == "top-level":
        for k in b:
            b[k] = "no"

    elif page_type == "other":
        for k in b:
            b[k] = "no"

    # --- MINOR DEVIATIONS within standard template ---
    if page_type == "404":
        b["breadcrumbs"] = "no"
        b["footer"] = "no"
        b["footer-copy"] = "no"
        b["json-ld"] = "no"
        b["content-marker"] = "required"  # 404 has .err section

    if page_type == "landing":
        b["breadcrumbs"] = "no"
        b["content-marker"] = "required"

    if page_type in ("blog", "blog-index", "tool-sub", "tool-index", "industry-index", "demo-index", "calculator", "legal"):
        b["cta-btn"] = "no"
        b["content-marker"] = "required"

    if page_type in ("docs", "docs-index"):
        b["preloader"] = "no"
        b["preloader-css"] = "no"
        b["preloader-js"] = "no"
        b["content-marker"] = "required"

    if page_type == "root":
        b["breadcrumbs"] = "no"
        b["content-marker"] = "required"

    return b


# ——————————————————————————————————————————————————————
# Checkers
# ——————————————————————————————————————————————————————

def check_doctype(content):
    if not re.search(r"<!DOCTYPE\s+html\s*>", content, re.IGNORECASE):
        return "FAIL", "DOCTYPE missing"
    if "<!DOCTYPE html>" in content:
        return "PASS", "correct"
    return "PASS", "lowercase (valid)"


def check_lang(content):
    m = re.search(r'<html\s[^>]*>', content, re.IGNORECASE)
    if not m: return "FAIL", "<html> tag not found"
    if 'lang="ru"' in m.group(): return "PASS", "lang='ru'"
    m2 = re.search(r'lang="([^"]+)"', m.group())
    if m2: return "FAIL", f'lang="{m2.group(1)}" instead of "ru"'
    return "FAIL", "lang attribute missing"


def check_charset(content):
    if re.search(r'<meta\s+charset\s*=\s*["\']?\s*UTF-8\s*["\']?\s*/?\s*>', content, re.IGNORECASE):
        return "PASS", "UTF-8"
    return "FAIL", "missing or not UTF-8"


def check_viewport(content):
    m = re.search(r'<meta\s+name\s*=\s*["\']viewport["\'][^>]*>', content, re.IGNORECASE)
    if not m: return "FAIL", "missing"
    if "user-scalable=no" in m.group(): return "WARN", "has user-scalable=no"
    return "PASS", "present"


def check_meta(content, name):
    pat = rf'<meta\s+name\s*=\s*["\']{name}["\'][^>]*>'
    if re.search(pat, content, re.IGNORECASE):
        return "PASS", "present"
    return "WARN", f"{name} missing"


def check_title(content):
    m = re.search(r'<title>(.*?)</title>', content, re.DOTALL | re.IGNORECASE)
    if not m: return "FAIL", "missing"
    t = m.group(1).strip()
    if not t: return "FAIL", "empty"
    return "PASS", t[:80]


def check_canonical(content, expected_url):
    m = re.search(r'<link\s+rel\s*=\s*["\']canonical["\'][^>]*href\s*=\s*["\']([^"\']+)["\']', content, re.IGNORECASE)
    if not m: return "FAIL", "missing"
    href = m.group(1).rstrip("/")
    exp = f"https://axiiom.ru{expected_url}".rstrip("/")
    if href == exp: return "PASS", m.group(1)
    return "WARN", f"{m.group(1)} (expected {exp})"


def check_robots(content):
    m = re.search(r'<meta\s+name\s*=\s*["\']robots["\'][^>]*content\s*=\s*["\']([^"\']+)["\']', content, re.IGNORECASE)
    return ("PASS", m.group(1)) if m else ("PASS", "not needed")


def check_og_tag(content, tag):
    pat = rf'<meta\s+property\s*=\s*["\']{tag}["\'][^>]*>'
    return "PASS" if re.search(pat, content, re.IGNORECASE) else "FAIL"


def check_twitter_tag(content, tag):
    pat = rf'<meta\s+name\s*=\s*["\']{tag}["\'][^>]*>'
    return "PASS" if re.search(pat, content, re.IGNORECASE) else "FAIL"


def check_jsonld(content):
    if '<script type="application/ld+json">' not in content:
        return "WARN", "missing"
    m = re.search(r'<script\s+type="application/ld\+json">(.*?)</script>', content, re.DOTALL)
    if not m: return "PASS", "present"
    try:
        d = json.loads(m.group(1))
        if "@graph" in d:
            types = [i.get("@type", "") for i in d["@graph"]]
            return "PASS", ", ".join(types)
        if "@type" in d: return "PASS", d["@type"]
        return "PASS", "present"
    except json.JSONDecodeError:
        return "FAIL", "invalid JSON"


def check_google_fonts(content):
    if "fonts.googleapis.com" not in content:
        return "WARN", "not referenced"
    parts = [
        ("preconnect googleapis", r'<link[^>]*rel\s*=\s*["\']preconnect["\'][^>]*fonts\.googleapis\.com'),
        ("preconnect gstatic",    r'<link[^>]*rel\s*=\s*["\']preconnect["\'][^>]*fonts\.gstatic\.com'),
        ("preload Inter",         r'<link[^>]*rel\s*=\s*["\']preload["\'][^>]*Inter'),
        ("Inter stylesheet",      r'fonts\.googleapis\.com[^"\']*Inter[^"\']*display=swap'),
    ]
    missing = [l for l, p in parts if not re.search(p, content, re.IGNORECASE)]
    if not missing: return "PASS", "all present"
    return "WARN", f"missing: {', '.join(missing)}"


def check_styles_css(content):
    m = re.search(r'<link[^>]*rel\s*=\s*["\']stylesheet["\'][^>]*styles\.css', content, re.IGNORECASE)
    return ("PASS", "linked") if m else ("FAIL", "NOT linked")


def check_preloader_css(content):
    has_link = bool(re.search(r'<link[^>]*rel\s*=\s*["\']stylesheet["\'][^>]*preloader\.css', content, re.IGNORECASE))
    has_div = '<div id="preloader"' in content
    if has_link and has_div: return "PASS", "linked"
    if has_link and not has_div: return "WARN", "linked but no preloader div"
    if has_div and not has_link: return "WARN", "NOT linked but preloader div exists"
    return "PASS", "not needed"


def check_favicon(content):
    if re.search(r'<link[^>]*rel\s*=\s*["\'](?:icon|shortcut icon)["\'][^>]*>', content, re.IGNORECASE):
        return "PASS", "linked"
    return "WARN", "not linked"


def check_ui(content, check_id):
    pats = {
        "preloader":     r'<div\s+id\s*=\s*["\']preloader["\']',
        "noise":         r'<div\s+class\s*=\s*["\']noise["\']',
        "grid-overlay":  r'<div\s+class\s*=\s*["\']grid-overlay["\']',
        "nav-overlay":   r'id\s*=\s*["\']navOverlay["\']',
        "mobile-nav":    r'id\s*=\s*["\']mobileNav["\']',
        "header":        r'<header[^>]*id\s*=\s*["\']header["\']',
        "desktop-nav":   r'id\s*=\s*["\']desktopNav["\']',
        "nav-toggle":    r'id\s*=\s*["\']navToggle["\']',
        "footer":        r'class\s*=\s*["\'][^"\']*\bfooter\b[^"\']*["\']',
        "footer-copy":   r'id\s*=\s*["\']footerCopy["\']',
        "breadcrumbs":   r'<nav[^>]*id\s*=\s*["\']breadcrumbs["\']',
        "cta-btn":       r'id\s*=\s*["\']ctaBtn["\']',
    }
    pat = pats.get(check_id)
    if not pat: return "WARN", "unknown check"
    found = bool(re.search(pat, content, re.IGNORECASE))
    if check_id == "footer" and not found:
        # Alternative: check for <footer>
        found = bool(re.search(r'<footer', content, re.IGNORECASE))
    return ("PASS", "present") if found else ("FAIL", "MISSING")


def check_script(content, script_src):
    pat = rf'<script[^>]*src\s*=\s*["\']/?{re.escape(script_src.lstrip("/"))}["\'][^>]*>'
    return ("PASS", "loaded") if re.search(pat, content, re.IGNORECASE) else ("WARN", "NOT loaded")


def check_nav_init(content):
    m = re.search(r'Nav\.init\(\s*\{([^}]*)\}\s*\)', content)
    if not m: return "FAIL", "NOT called"
    return "PASS", "{" + m.group(1) + "}"


def check_gtag(content):
    return ("PASS", "loaded") if "googletagmanager.com/gtag/js" in content else ("WARN", "NOT loaded")


def check_ym(content):
    if "/metrika.js" in content or "mc.yandex.ru/metrika" in content:
        return ("PASS", "loaded via /metrika.js")
    return ("WARN", "NOT loaded")


def check_content_marker(content, page_type):
    pats = {
        "landing":        r'hero',
        "industry":       r'industries-hero',
        "industry-index": r'industries-hero',
        "tool-sub":       r'tool-page',
        "tool-index":     r'tools-hero',
        "blog":           r'article-page',
        "blog-index":     r'blog',
        "docs":           r'docs-article|<section',
        "docs-index":     r'<section',
        "demo-index":     r'demo',
        "demo-sub":       r'app-content|app-header|bottom-nav|demo-page-hero|hero-content',
        "calculator":     r'calc-section',
        "legal":          r'class\s*=\s*["\']legal["\']',
        "404":            r'class\s*=\s*["\']err["\']',
        "root":           r'hero',
    }
    pat = pats.get(page_type)
    if not pat: return "FAIL", "no content marker for this page type"
    if re.search(pat, content, re.IGNORECASE):
        return "PASS", "found"
    return "FAIL", "NOT found"

def check_hero_svg(content):
    """Check if hero section has animated SVG background."""
    if 'hero' not in content:
        return "PASS", "no hero section"
    if 'hero-bg-svg' in content:
        return "PASS", "has hero SVG"
    if '<section' in content or 'hero' in content:
        for m in __import__('re').finditer(r'(?:<section[^>]*class="[^"]*hero[^"]*"|<header[^>]*class="[^"]*hero[^"]*")[^>]*>.*?<svg', content, re.DOTALL):
            return "PASS", "has inline SVG"
    return "WARN", "hero without SVG animation"


# ——————————————————————————————————————————————————————
# Run checks against baselines
# ——————————————————————————————————————————————————————

def run_checks(page, baseline_map, all_pages_list):
    content = page["content"]
    ptype = page["type"]
    bl = baseline_map
    checks = []

    if content is None:
        for feat in bl:
            checks.append({"feature": feat, "label": FEATURES.get(feat, feat), "status": "FAIL", "detail": "FILE NOT FOUND"})
        return checks

    # Check each feature against baseline
    for feat, requirement in bl.items():
        label = FEATURES.get(feat, feat)
        result = None

        try:
            if requirement == "no":
                result = ("PASS", "skipped")
            elif feat == "doctype":
                result = check_doctype(content)
            elif feat == "lang-ru":
                result = check_lang(content)
            elif feat == "charset":
                result = check_charset(content)
            elif feat == "viewport":
                result = check_viewport(content)
            elif feat == "theme-color":
                result = check_meta(content, "theme-color")
            elif feat == "description":
                result = check_meta(content, "description")
            elif feat == "title":
                result = check_title(content)
            elif feat == "canonical":
                result = check_canonical(content, page["url"])
            elif feat == "robots-correct":
                result = check_robots(content)
            elif feat.startswith("og-"):
                og_map = {"og-title": "og:title", "og-desc": "og:description", "og-url": "og:url",
                          "og-type": "og:type", "og-image": "og:image"}
                og_tag = og_map.get(feat)
                if og_tag:
                    s = check_og_tag(content, og_tag)
                    result = (s, "present" if s == "PASS" else "missing")
                else:
                    result = ("WARN", "unknown og tag")
            elif feat.startswith("twitter-"):
                tw_map = {"twitter-card": "twitter:card", "twitter-title": "twitter:title",
                          "twitter-desc": "twitter:description", "twitter-img": "twitter:image"}
                tw_tag = tw_map.get(feat)
                if tw_tag:
                    s = check_twitter_tag(content, tw_tag)
                    result = (s, "present" if s == "PASS" else "missing")
                else:
                    result = ("WARN", "unknown twitter tag")
            elif feat == "json-ld":
                result = check_jsonld(content)
            elif feat == "fonts":
                result = check_google_fonts(content)
            elif feat == "styles-css":
                result = check_styles_css(content)
            elif feat == "preloader-css":
                result = check_preloader_css(content)
            elif feat == "favicon":
                result = check_favicon(content)
            elif feat in ("preloader", "noise", "grid-overlay", "nav-overlay", "mobile-nav",
                          "header", "desktop-nav", "nav-toggle", "footer", "footer-copy",
                          "breadcrumbs", "cta-btn"):
                result = check_ui(content, feat)
            elif feat == "nav-js":
                result = check_script(content, "/nav.js")
            elif feat == "theme-js":
                result = check_script(content, "/theme.js")
            elif feat == "config-js":
                result = check_script(content, "/config.js")
            elif feat == "preloader-js":
                result = check_script(content, "/preloader.js")
            elif feat == "nav-init":
                result = check_nav_init(content)
            elif feat == "gtag":
                result = check_gtag(content)
            elif feat == "ym":
                result = check_ym(content)
            elif feat == "content-marker":
                result = check_content_marker(content, ptype)
            elif feat == "hero-svg":
                result = check_hero_svg(content)
            elif feat == "links":
                result = check_broken_links(content, page, all_pages_list)
            else:
                result = ("PASS", "unknown check")
        except Exception as e:
            result = ("FAIL", f"check threw: {e}")

        status, detail = result if result else ("WARN", "not implemented")

        # Map status to requirement
        if requirement == "required":
            pass  # keep original status
        elif requirement == "optional":
            # Downgrade FAIL to WARN for optional features
            if status == "FAIL":
                status = "WARN"

        checks.append({"feature": feat, "label": label, "status": status, "detail": detail})

    return checks


def check_broken_links(content, page, all_pages):
    """Minimal broken link check: internal /path links against known pages."""
    known = set()
    for p in all_pages:
        if p["url"]:
            known.add(p["url"])
    known.add("/")
    known.add("/privacy")
    known.add("/terms")

    broken = []
    for m in re.finditer(r'href\s*=\s*["\']([^"\']+)["\']', content):
        href = m.group(1)
        if re.match(r'https?://', href): continue
        if href.startswith("#") or href.startswith("mailto:") or href.startswith("tel:"): continue
        if href.startswith("//"): continue
        if href.startswith("data:"): continue
        clean = href.split("#")[0].split("?")[0].rstrip("/")
        if not clean.startswith("/"): continue
        if clean in known: continue
        # Check filesystem
        rel = clean.lstrip("/")
        resolved = SITE_ROOT / rel
        if resolved.exists(): continue
        try:
            decoded = unquote(rel)
            if (SITE_ROOT / decoded).exists(): continue
        except Exception: pass
        broken.append(href)

    if broken:
        detail = "; ".join(broken[:5])
        if len(broken) > 5: detail += f" ... +{len(broken) - 5} more"
        return "FAIL", f"{len(broken)} broken: {detail}"
    return "PASS", "ok"


# ——————————————————————————————————————————————————————
# HTML Report
# ——————————————————————————————————————————————————————

REPORT_CSS = """
:root{--bg:#0a0a0f;--bg-card:#14141c;--bg-hover:#1c1c28;--border:#2a2a3a;--text:#e8e8ed;--text-dim:#8888a0;--green:#22c55e;--yellow:#eab308;--red:#ef4444;--blue:#3b82f6;--orange:#f97316}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Inter',system-ui,sans-serif;background:var(--bg);color:var(--text);line-height:1.6;padding:20px}
h1{font-size:1.6rem;margin-bottom:2px}
h2{font-size:1.1rem;margin:20px 0 10px;color:var(--text-dim)}
.subtitle{color:var(--text-dim);margin-bottom:20px;font-size:.85rem}
.summary{display:flex;gap:12px;margin:16px 0 24px;flex-wrap:wrap}
.stat{background:var(--bg-card);border:1px solid var(--border);border-radius:8px;padding:12px 20px;min-width:90px;text-align:center}
.stat .num{font-size:1.8rem;font-weight:700;display:block}
.stat .lbl{font-size:.7rem;color:var(--text-dim);text-transform:uppercase;letter-spacing:.05em}
.stat.pass .num{color:var(--green)}.stat.fail .num{color:var(--red)}.stat.warn .num{color:var(--yellow)}.stat.total .num{color:var(--blue)}
.filters{display:flex;gap:6px;margin-bottom:16px;flex-wrap:wrap}
.filter-btn{background:var(--bg-card);border:1px solid var(--border);color:var(--text);padding:5px 12px;border-radius:5px;cursor:pointer;font-size:.75rem}
.filter-btn:hover{background:var(--bg-hover)}.filter-btn.active{border-color:var(--blue);background:rgba(59,130,246,.15)}
.page-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(380px,1fr));gap:12px}
.page-card{background:var(--bg-card);border:1px solid var(--border);border-radius:8px;padding:12px;transition:border-color .2s}
.page-card:hover{border-color:var(--text-dim)}
.page-card.passed{border-left:3px solid var(--green)}
.page-card.failed{border-left:3px solid var(--red)}
.page-card.warned{border-left:3px solid var(--yellow)}
.card-header{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:6px;gap:8px}
.card-path{font-size:.82rem;word-break:break-all;color:var(--blue);font-weight:500}
.card-type{font-size:.65rem;background:rgba(59,130,246,.15);color:var(--blue);padding:2px 7px;border-radius:4px;white-space:nowrap}
.card-stats{display:flex;gap:6px;margin:6px 0}
.card-stat{font-size:.7rem;padding:1px 7px;border-radius:3px}
.card-stat.pass{background:rgba(34,197,94,.12);color:var(--green)}
.card-stat.fail{background:rgba(239,68,68,.12);color:var(--red)}
.card-stat.warn{background:rgba(234,179,8,.12);color:var(--yellow)}
.card-stat.omit{background:rgba(136,136,160,.12);color:var(--text-dim)}
.card-checks{max-height:0;overflow:hidden;transition:max-height .3s ease;font-size:.75rem;line-height:1.5}
.card-checks.open{max-height:3000px}
.check-toggle{background:none;border:none;color:var(--text-dim);cursor:pointer;font-size:.72rem;padding:3px 0}
.check-toggle:hover{color:var(--text)}
.check-row{display:flex;gap:6px;padding:2px 0;align-items:baseline}
.check-icon{flex-shrink:0;width:16px;text-align:center;font-size:.8rem}
.check-label{font-weight:500;min-width:130px}.check-detail{color:var(--text-dim)}
.row-pass .check-icon{color:var(--green)}.row-fail .check-icon{color:var(--red)}.row-warn .check-icon{color:var(--yellow)}.row-no .check-icon{color:var(--text-dim);opacity:.5}
.site-map{background:var(--bg-card);border:1px solid var(--border);border-radius:8px;padding:16px;margin:20px 0}
.map-tree{font-family:monospace;font-size:.78rem;line-height:1.7}
.map-tree .node{display:flex;align-items:center;gap:4px}
.map-tree .indent{display:inline-block;width:18px}
.icon-pass{color:var(--green)}.icon-fail{color:var(--red)}.icon-warn{color:var(--yellow)}.icon-none{color:var(--text-dim)}
.report-footer{margin-top:32px;padding-top:12px;border-top:1px solid var(--border);font-size:.7rem;color:var(--text-dim)}
"""


def generate_report(pages, checks_map, timestamp=None):
    if timestamp is None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    all_checks = [c for cl in checks_map.values() for c in cl]
    total = len(pages)
    passed = sum(1 for c in all_checks if c["status"] == "PASS")
    failed = sum(1 for c in all_checks if c["status"] == "FAIL")
    warned = sum(1 for c in all_checks if c["status"] == "WARN")

    cards = ""
    sitemap = ""
    sitemap_items = []

    for page in pages:
        checks = checks_map.get(page["url"], [])
        n_pass = sum(1 for c in checks if c["status"] == "PASS")
        n_fail = sum(1 for c in checks if c["status"] == "FAIL")
        n_warn = sum(1 for c in checks if c["status"] == "WARN")

        if n_fail > 0: card_class, worst = "failed", "fail"
        elif n_warn > 0: card_class, worst = "warned", "warn"
        else: card_class, worst = "passed", "pass"

        ptype = page["type"]
        checks_html = ""
        for c in checks:
            icon = {"PASS": "✓", "FAIL": "✗", "WARN": "△"}.get(c["status"], "·")
            row_class = {"PASS": "row-pass", "FAIL": "row-fail", "WARN": "row-warn"}.get(c["status"], "row-no")
            detail = f'<span class="check-detail">— {c["detail"][:120]}</span>' if c["detail"] else ""
            checks_html += f'<div class="check-row {row_class}"><span class="check-icon">{icon}</span><span class="check-label">{c["label"]}</span> {detail}</div>'

        card_id = page["url"].replace("/", "-").replace(".", "-") or "root"
        cards += f"""
<div class="page-card {card_class}" data-type="{ptype}" data-status="{worst}">
  <div class="card-header">
    <div>
      <div class="card-path">{page["url"] or "/"}</div>
    </div>
    <span class="card-type">{ptype}</span>
  </div>
  <div class="card-stats">
    <span class="card-stat pass">✓ {n_pass}</span>
    <span class="card-stat fail">✗ {n_fail}</span>
    <span class="card-stat warn">△ {n_warn}</span>
  </div>
  <button class="check-toggle" onclick="var e=document.getElementById('c{card_id}');e.classList.toggle('open');this.textContent=e.classList.contains('open')?'▲ Hide':'▼ Details'">▼ Details</button>
  <div class="card-checks" id="c{card_id}">{checks_html}</div>
</div>"""

        status_icon = {"pass": "●", "fail": "●", "warn": "●"}.get(worst, "○")
        status_cls = {"pass": "icon-pass", "fail": "icon-fail", "warn": "icon-warn"}.get(worst, "icon-none")
        sitemap_items.append({"url": page["url"], "type": ptype, "status": worst, "icon": status_icon, "cls": status_cls})

    # Sitemap grouped by section
    sections = {"landing": [], "industry": [], "tool-index": [], "tool-sub": [],
                "blog": [], "docs": [], "demo-index": [], "demo-sub": [],
                "calculator": [], "legal": [], "404": [], "other": [], "blog-index": [],
                "docs-index": [], "industry-index": []}
    for item in sitemap_items:
        t = item["type"]
        base = t.split("-")[0] if "-" in t else t
        if base not in sections: base = "other"
        sections.setdefault(base, []).append(item)

    section_labels = {
        "landing": "🏠 Главная", "industry": "🏭 Решения", "tool": "🔧 Инструменты",
        "blog": "📝 Блог", "docs": "📄 Документация",
        "demo": "🎮 Демо", "calculator": "🧮 Калькулятор",
        "legal": "⚖️ Юридическое", "404": "⚠️ 404",
    }

    for section_key in ["landing", "industry", "tool", "blog", "docs", "demo", "calculator", "legal", "404"]:
        items = sections.get(section_key, [])
        if not items:
            # Also check plural/base keys
            for k, v in list(sections.items()):
                if k.startswith(section_key):
                    items.extend(v)
        if not items:
            continue
        label = section_labels.get(section_key, section_key)
        sitemap += f'<div class="node" style="margin-top:4px;font-weight:500"><span class="icon-none">▸</span> {label}</div>'
        for item in items:
            name = item["url"].rsplit("/", 1)[-1] if "/" in item["url"].strip("/") else item["url"]
            sitemap += f'<div class="node"><span class="indent"></span><span class="{item["cls"]}">{item["icon"]}</span> {item["url"]} <span class="card-type">{item["type"]}</span></div>'

    # Filter buttons
    types = sorted(set(p["type"] for p in pages if p["type"] != "anchor"))
    filter_btns = '<button class="filter-btn active" data-f="all" onclick="filterAll()">All</button>'
    for t in types:
        filter_btns += f'<button class="filter-btn" data-f="type_{t}" onclick="filterType(\'{t}\')">{t}</button>'

    return f"""<!DOCTYPE html>
<html lang="ru">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>AXIIOM Site Test Report</title>
<style>{REPORT_CSS}</style>
<script>
var _ft={{type:null,status:null}};
function _ap(){{
  document.querySelectorAll('.page-card').forEach(c=>{{
    var s=true;
    if(_ft.type&&c.getAttribute('data-type')!==_ft.type)s=false;
    if(_ft.status&&c.getAttribute('data-status')!==_ft.status)s=false;
    c.style.display=s?'':'none';
  }});
  document.querySelectorAll('.filter-btn').forEach(b=>b.classList.remove('active'));
  document.querySelectorAll('.filter-btn').forEach(b=>{{
    var f=b.getAttribute('data-f');
    if(!f)return;
    if(f==='all'&&!_ft.type&&!_ft.status)b.classList.add('active');
    if(f.startsWith('type_')&&f==='type_'+_ft.type)b.classList.add('active');
    if(f.startsWith('stat_')&&f==='stat_'+_ft.status)b.classList.add('active');
  }});
}}
function filterType(t){{_ft.type=t;_ft.status=null;_ap();}}
function filterStatus(s){{_ft.status=s;_ft.type=null;_ap();}}
function filterAll(){{_ft.type=null;_ft.status=null;_ap();}}
</script></head>
<body>
<h1>AXIIOM Site Test Report</h1>
<p class="subtitle">{timestamp} — {total} pages, {len(all_checks)} checks</p>
<div class="summary">
  <div class="stat total"><span class="num">{total}</span><span class="lbl">Pages</span></div>
  <div class="stat pass"><span class="num">{passed}</span><span class="lbl">Passed</span></div>
  <div class="stat fail"><span class="num">{failed}</span><span class="lbl">Failed</span></div>
  <div class="stat warn"><span class="num">{warned}</span><span class="lbl">Warnings</span></div>
</div>

<h2>Site Map</h2>
<div class="site-map"><div class="map-tree">{sitemap}</div></div>

<h2>Filters</h2>
<div class="filters">{filter_btns}</div>
<div class="filters" style="margin-top:-12px">
  <button class="filter-btn" data-f="stat_fail" onclick="filterStatus('fail')">🔴 Failed only</button>
  <button class="filter-btn" data-f="stat_warn" onclick="filterStatus('warn')">🟡 Warnings only</button>
  <button class="filter-btn" data-f="all" onclick="filterAll()">🟢 All</button>
</div>

<h2>Pages</h2>
<div class="page-grid">{cards}</div>

<div class="report-footer">AXIIOM Site Validator — {timestamp}</div>
</body></html>"""


# ——————————————————————————————————————————————————————
# Main
# ——————————————————————————————————————————————————————

def main():
    parser = argparse.ArgumentParser(description="AXIIOM Site Validator")
    parser.add_argument("--dir", default=str(SITE_ROOT))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--serve", action="store_true")
    parser.add_argument("--exit-code", action="store_true")
    args = parser.parse_args()

    site_dir = Path(args.dir)
    if not site_dir.is_dir():
        print(f"Error: {site_dir} not found", file=sys.stderr)
        sys.exit(1)

    nav_path = site_dir / "nav.js"
    if not nav_path.exists():
        print(f"Error: nav.js not found in {site_dir}", file=sys.stderr)
        sys.exit(1)

    print("📋 Parsing nav.js TREE...")
    page_registry = build_page_registry(nav_path)

    # Filter out anchor/hash pages
    page_registry = {k: v for k, v in page_registry.items() if v["type"] != "anchor"}

    print(f"📄 Building page list from TREE ({len(page_registry)} pages)...")
    pages = discover_project_pages(site_dir, page_registry)

    if args.serve:
        print(f"🌐 Fetching from {LIVE_URL}...")
        for page in pages:
            url = f"{LIVE_URL}{page['url']}"
            try:
                resp = urllib.request.urlopen(url, timeout=10)
                page["content"] = resp.read().decode("utf-8", errors="replace")
                page["missing"] = False
            except Exception:
                page["content"] = None
                page["missing"] = True

    # Compute baselines per page
    for page in pages:
        page["baseline"] = baseline(page["type"])

    missing = [p for p in pages if p["missing"]]
    if missing:
        print(f"  ⚠️  {len(missing)} page(s) not found on disk:")
        for p in missing:
            print(f"    - {p['url']} ({p['type']})")

    print("🔬 Running checks...")
    checks_map = {}
    for page in pages:
        checks_map[page["url"]] = run_checks(page, page["baseline"], pages)

    print("📊 Generating report...")
    report = generate_report(pages, checks_map)
    output_path = Path(args.output)
    output_path.write_text(report)
    print(f"📄 Report: {output_path}")

    # Summary
    all_checks = [c for cl in checks_map.values() for c in cl]
    n_pass = sum(1 for c in all_checks if c["status"] == "PASS")
    n_fail = sum(1 for c in all_checks if c["status"] == "FAIL")
    n_warn = sum(1 for c in all_checks if c["status"] == "WARN")
    print(f"\nSummary: {len(pages)} pages, {len(all_checks)} checks")
    print(f"  ✅ Passed: {n_pass}")
    print(f"  ❌ Failed: {n_fail}")
    print(f"  ⚠️  Warnings: {n_warn}")

    if n_fail > 0:
        print("\n❌ Failures:")
        for page in pages:
            for c in checks_map.get(page["url"], []):
                if c["status"] == "FAIL":
                    print(f"  [{page['type']}] {page['url']}: {c['label']} — {c['detail'][:120]}")

    if args.exit_code and n_fail > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
