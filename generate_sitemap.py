#!/usr/bin/env python3
"""Generate sitemap.xml from nav.js TREE."""
import re
from datetime import datetime, timezone
from pathlib import Path

root = Path(__file__).resolve().parent
nav = root / 'nav.js'

raw = nav.read_text('utf-8')
start = raw.index('var TREE = [') + len('var TREE = [')
depth = 1
i = start
while i < len(raw):
    c = raw[i]
    if c == '[':
        depth += 1
    elif c == ']':
        depth -= 1
        if depth == 0:
            break
    i += 1
tree_js = raw[start:i]

def extract_paths(text):
    paths = []
    i = 0
    while i < len(text):
        bs = text.find('{', i)
        if bs == -1:
            break
        d = 0
        j = bs
        while j < len(text):
            c = text[j]
            if c == '{':
                d += 1
            elif c == '}':
                d -= 1
                if d == 0:
                    block = text[bs + 1:j]
                    pm = re.search(r"path:\s*'([^']+)'", block)
                    p = pm.group(1) if pm else ''
                    if p and not p.startswith('http') and '#' not in p:
                        paths.append(p.rstrip('/') if p != '/' else '/')
                    cm = re.search(r"children:\s*\[([\s\S]*?)\]", block)
                    if cm:
                        paths.extend(extract_paths(cm.group(1)))
                    i = j + 1
                    break
            j += 1
        else:
            break
    return paths

all_paths = set(extract_paths(tree_js))
all_paths.update(['/404.html', '/privacy', '/terms', '/blog', '/tools', '/industries', '/demo/app'])
all_paths.discard('/')  # will add explicitly
all_paths = sorted(all_paths, key=lambda x: (x.count('/'), x))

today = datetime.now(timezone.utc).strftime('%Y-%m-%d')

priority_map = {
    '/': 1.0, '/docs/': 0.9, '/blog/': 0.9, '/industries/': 0.9, '/tools/': 0.9, '/calculator/': 0.8,
}
freq_map = {
    '/': 'weekly', '/docs/': 'weekly', '/blog/': 'weekly', '/industries/': 'weekly', '/tools/': 'weekly',
}

def prio(p):
    if p in priority_map:
        return priority_map[p]
    if p.startswith('/docs/'):
        return 0.7
    if p.startswith('/blog/'):
        return 0.7
    if any(p.startswith(x) for x in ['/industries/', '/tools/', '/demo/app/']):
        return 0.7
    if p in ('/privacy', '/terms'):
        return 0.3
    if p == '/404.html':
        return 0.1
    return 0.5

def freq(p):
    if p in freq_map:
        return freq_map[p]
    return 'monthly'

def fmt_url(p):
    if p == '/':
        return 'https://axiiom.ru/'
    if p.endswith('.html'):
        return 'https://axiiom.ru' + p
    return 'https://axiiom.ru' + p + '/'

lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
]
for p in ['/'] + all_paths:
    lines.append('  <url>')
    lines.append('    <loc>' + fmt_url(p) + '</loc>')
    lines.append('    <lastmod>' + today + '</lastmod>')
    lines.append('    <changefreq>' + freq(p) + '</changefreq>')
    lines.append('    <priority>' + str(prio(p)) + '</priority>')
    lines.append('  </url>')
lines.append('</urlset>')

with open(root / 'sitemap.xml', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines) + '\n')

total = len(all_paths) + 1
print('sitemap.xml: ' + str(total) + ' URLs')
