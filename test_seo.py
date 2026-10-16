#!/usr/bin/env python3
"""Site-wide SEO regression checks for the static AXIIOM site."""

from collections import defaultdict
from html.parser import HTMLParser
import ast
from pathlib import Path
import json
import re
import sys
import xml.etree.ElementTree as ET
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
SITEMAP = ROOT / "sitemap.xml"
BASE_URL = "https://axiiom.ru"


class SEOHTMLParser(HTMLParser):
    """Collect the small set of HTML signals this project needs to validate."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_head = False
        self.in_title = False
        self.in_script = False
        self.in_jsonld = False
        self.title = []
        self.jsonld_text = []
        self.jsonld_documents = []
        self.meta_name = defaultdict(list)
        self.meta_property = defaultdict(list)
        self.canonicals = []
        self.links = []
        self.h1_count = 0
        self.visible_text = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        tag = tag.lower()
        if tag == "head":
            self.in_head = True
        elif tag == "body":
            self.in_head = False
        elif tag == "title":
            self.in_title = True
        elif tag == "meta" and self.in_head:
            name = (attrs.get("name") or "").lower()
            prop = (attrs.get("property") or "").lower()
            if name:
                self.meta_name[name].append(attrs.get("content") or "")
            if prop:
                self.meta_property[prop].append(attrs.get("content") or "")
        elif tag == "link" and (attrs.get("rel") or "").lower() == "canonical":
            self.canonicals.append(attrs.get("href") or "")
        elif tag == "a" and not self.in_script:
            self.links.append(attrs.get("href") or "")
        elif tag == "h1" and not self.in_script:
            self.h1_count += 1
        elif tag == "script":
            self.in_script = True
            self.in_jsonld = (attrs.get("type") or "").lower() == "application/ld+json"
            self.jsonld_text = []

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag == "head":
            self.in_head = False
        elif tag == "title":
            self.in_title = False
        elif tag == "script":
            if self.in_jsonld:
                self.jsonld_documents.append("".join(self.jsonld_text).strip())
            self.in_script = False
            self.in_jsonld = False
            self.jsonld_text = []

    def handle_data(self, data):
        if self.in_title:
            self.title.append(data)
        if self.in_jsonld:
            self.jsonld_text.append(data)
        elif not self.in_script and not self.in_head:
            self.visible_text.append(data)


def read_page(url):
    path = urlparse(url).path
    local = ROOT / path.lstrip("/")
    if path.endswith("/") or local.is_dir():
        local = local / "index.html"
    return local


def parse_page(path):
    parser = SEOHTMLParser()
    parser.feed(path.read_text(encoding="utf-8", errors="replace"))
    return parser


def read_vitepress_page_data(path):
    source = path.read_text(encoding="utf-8")
    marker = "JSON.parse("
    start = source.index(marker) + len(marker)
    quote = source[start]
    if quote not in ("'", '\"'):
        raise ValueError("unknown JSON.parse string delimiter")
    pos = start + 1
    escaped = False
    while pos < len(source):
        char = source[pos]
        if escaped:
            escaped = False
        elif char == "\\":
            escaped = True
        elif char == quote:
            break
        pos += 1
    literal = quote + source[start + 1:pos] + quote
    return json.loads(ast.literal_eval(literal))


def is_noindex(parser):
    values = parser.meta_name.get("robots", []) + parser.meta_name.get("googlebot", []) + parser.meta_name.get("yandex", [])
    return any(re.search(r"(?:^|[,\s])(?:noindex|none)(?:$|[,\s])", value.lower()) for value in values)


def robots_allows(path, robots_text):
    """Apply the basic robots.txt longest-match rule for the current * group."""
    active = False
    rules = []
    for raw_line in robots_text.splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if not line or ":" not in line:
            continue
        key, value = (part.strip() for part in line.split(":", 1))
        key = key.lower()
        if key == "user-agent":
            active = value == "*"
        elif active and key in ("allow", "disallow") and value:
            wildcard = value.endswith("$")
            rule = value[:-1] if wildcard else value
            regex = "^" + ".*".join(re.escape(part) for part in rule.split("*"))
            if wildcard:
                regex += "$"
            if re.search(regex, path):
                specificity = len(rule.replace("*", ""))
                rules.append((specificity, key == "allow"))
    if not rules:
        return True
    return max(rules, key=lambda item: (item[0], item[1]))[1]


def fail(message):
    print(f"❌ {message}")
    return 1


def main():
    errors = []
    try:
        xml_root = ET.parse(SITEMAP).getroot()
    except (OSError, ET.ParseError) as exc:
        return fail(f"sitemap.xml нельзя прочитать: {exc}")

    namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = [node.text or "" for node in xml_root.findall("sm:url/sm:loc", namespace)]
    if len(urls) != len(set(urls)):
        errors.append("в sitemap.xml есть повторяющиеся URL")

    titles = defaultdict(list)
    canonical_urls = defaultdict(list)
    mock_count = 0
    mock_root_schema_types = []
    mock_page_urls = set()

    for url in urls:
        path = read_page(url)
        if not path.is_file():
            errors.append(f"URL из sitemap не найден в статической сборке: {url}")
            continue
        page = parse_page(path)
        title = "".join(page.title).strip()
        description = (page.meta_name.get("description") or [""])[0].strip()
        if not title:
            errors.append(f"нет <title>: {url}")
        else:
            titles[title].append(url)
        if not description:
            errors.append(f"нет meta description: {url}")
        if len(page.canonicals) != 1 or page.canonicals[0] != url:
            errors.append(f"canonical должен точно совпадать с URL: {url} -> {page.canonicals}")
        if is_noindex(page):
            errors.append(f"noindex-страница находится в sitemap: {url}")
        canonical_urls[page.canonicals[0] if page.canonicals else ""].append(url)

        if url.startswith(BASE_URL + "/mock-services/"):
            mock_count += 1
            mock_page_urls.add(url)
            if not 100 <= len(description) <= 160:
                errors.append(f"описание mock-services должно быть в диапазоне 100–160 символов ({len(description)}): {url}")
            for prop in ("og:title", "og:description", "og:url", "og:image"):
                if not page.meta_property.get(prop):
                    errors.append(f"на mock-странице нет {prop}: {url}")
            for name in ("twitter:card", "twitter:title", "twitter:description", "twitter:image"):
                if not page.meta_name.get(name):
                    errors.append(f"на mock-странице нет {name}: {url}")
            if page.meta_property.get("og:url", [""])[0] != url:
                errors.append(f"og:url не совпадает с canonical: {url}")
            if not page.jsonld_documents:
                errors.append(f"на mock-странице нет JSON-LD: {url}")
            else:
                try:
                    schema = json.loads(page.jsonld_documents[0])
                    if url == BASE_URL + "/mock-services/":
                        graph = schema.get("@graph", [])
                        mock_root_schema_types = [item.get("@type") for item in graph]
                        if "WebSite" not in mock_root_schema_types or "SoftwareSourceCode" not in mock_root_schema_types:
                            errors.append("на главной mock-services ожидались WebSite и SoftwareSourceCode в JSON-LD")
                    elif schema.get("@type") != "WebPage":
                        errors.append(f"для документа mock-services ожидался JSON-LD WebPage: {url}")
                except (json.JSONDecodeError, TypeError) as exc:
                    errors.append(f"JSON-LD невалиден ({exc}): {url}")
            if page.h1_count < 1 or "vp-doc" not in path.read_text(encoding="utf-8", errors="replace"):
                errors.append(f"контент mock-страницы должен быть отрендерен в HTML, а не только загружаться JavaScript: {url}")

    for title, pages in titles.items():
        if len(pages) > 1:
            errors.append(f"одинаковый title у {len(pages)} страниц: {title!r}")
    for canonical, pages in canonical_urls.items():
        if canonical and len(pages) > 1:
            errors.append(f"canonical используется несколькими URL: {canonical}")

    # Public mock documents are already generated as static HTML. All actual
    # route pages should be in the sitemap; only the standalone 404 is excluded.
    mock_files = [p for p in (ROOT / "mock-services").rglob("index.html")]
    expected_mock_urls = set()
    for page_path in mock_files:
        rel = page_path.parent.relative_to(ROOT / "mock-services").as_posix()
        expected_mock_urls.add(BASE_URL + "/mock-services/" + ("" if rel == "." else rel + "/"))
    if expected_mock_urls != mock_page_urls:
        missing = sorted(expected_mock_urls - mock_page_urls)
        unexpected = sorted(mock_page_urls - expected_mock_urls)
        errors.append(f"sitemap не соответствует prerendered mock-страницам; missing={missing}, unexpected={unexpected}")

    # Keep client-side VitePress metadata in sync with the prerendered HTML.
    hashmap_path = ROOT / "mock-services/hashmap.json"
    try:
        hashmap = json.loads(hashmap_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        hashmap = {}
        errors.append(f"hashmap.json нельзя прочитать: {exc}")
    for page_path in mock_files:
        rel = page_path.parent.relative_to(ROOT / "mock-services").as_posix()
        route = "." if rel == "." else rel
        prefix = "index.md" if route == "." else route.replace("/", "_") + ".md"
        source_key = prefix.lower()
        digest = hashmap.get(source_key)
        if not digest:
            errors.append(f"нет hash для client-side страницы {source_key}")
            continue
        page = parse_page(page_path)
        title = "".join(page.title).strip()
        description = (page.meta_name.get("description") or [""])[0].strip()
        raw_html = page_path.read_text(encoding="utf-8", errors="replace")
        expected_preload = f"/mock-services/assets/{prefix}.{digest}.lean.js"
        if expected_preload not in raw_html or digest not in raw_html:
            errors.append(f"prerendered route не ссылается на актуальные bundles/hashmap: {page_path}")
        escaped_quote = chr(92) + '"'
        if escaped_quote + "title" + escaped_quote + ":" + escaped_quote + "AXIIOM" + escaped_quote not in raw_html:
            errors.append(f"глобальный title VitePress не использует бренд AXIIOM: {page_path}")
        for suffix in (".js", ".lean.js"):
            bundle = ROOT / "mock-services/assets" / f"{prefix}.{digest}{suffix}"
            if not bundle.is_file():
                errors.append(f"не найден client-side page bundle: {bundle.name}")
                continue
            try:
                data = read_vitepress_page_data(bundle)
                dynamic_title = title.removesuffix(" | AXIIOM")
                if data.get("title") != dynamic_title or data.get("description") != description:
                    errors.append(f"client-side title/description не совпадают с HTML: {bundle.name}")
            except (ValueError, SyntaxError, json.JSONDecodeError) as exc:
                errors.append(f"ошибка чтения VitePress page bundle {bundle.name}: {exc}")

    # A scaffold is not a public demo. It must be crawlable for noindex to be
    # observed, but it must not appear in the sitemap.
    template_url = BASE_URL + "/demo/app/demo-template/"
    if template_url in urls:
        errors.append("demo-template находится в sitemap.xml")
    template = ROOT / "demo/app/demo-template/index.html"
    if template.is_file() and not is_noindex(parse_page(template)):
        errors.append("demo-template должен иметь meta robots noindex, follow")

    # Blog cards were previously created only by JavaScript. Keep every article
    # link in the source HTML so crawlers can discover posts before hydration.
    posts_js = (ROOT / "blog/posts.js").read_text(encoding="utf-8")
    post_slugs = set(re.findall(r"slug:\s*'([^']+)'", posts_js))
    blog_page = parse_page(ROOT / "blog/index.html")
    blog_links = {link.rstrip("/").split("/")[-1] for link in blog_page.links if link.startswith("/blog/")}
    missing_blog_links = sorted(post_slugs - blog_links)
    if missing_blog_links:
        errors.append(f"в HTML блога нет статических ссылок на статьи: {missing_blog_links}")

    robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
    if "Allow: /mock-services/" not in robots:
        errors.append("robots.txt должен явно разрешать /mock-services/")
    blocked_urls = [url for url in urls if not robots_allows(urlparse(url).path, robots)]
    if blocked_urls:
        errors.append(f"robots.txt блокирует URL из sitemap: {blocked_urls}")
    if any(url in urls for url in (BASE_URL + "/privacy/", BASE_URL + "/terms/")):
        errors.append("noindex-страницы privacy/terms не должны находиться в sitemap.xml")

    if errors:
        for item in errors:
            print(f"❌ {item}")
        print(f"SEO checks: {len(errors)} ошибок; проверено URL в sitemap: {len(urls)}")
        return 1

    print(f"✅ SEO checks: {len(urls)} индексируемых URL, {mock_count} prerendered mock-страниц")
    print("✅ Canonical, title, robots, sitemap, Open Graph, JSON-LD, VitePress bundles и SSR-блог проверены")
    return 0


if __name__ == "__main__":
    sys.exit(main())
