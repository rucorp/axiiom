#!/usr/bin/env python3
"""build.py — сборка styles.css и nav.js из исходников + cache-busting версии.

Использует esbuild (через npx) с теми же параметрами, что и текущая сборка:
    esbuild <src> --minify --charset=utf8

После сборки обновляет ?v=<дата> во всех HTML-ссылках на статику и прогоняет
test_site.py для верификации.

Usage:
    python3 build.py                # собрать и обновить версию на сегодняшнюю
    python3 build.py --version 20260819   # указать версию вручную
    python3 build.py --no-test      # не запускать test_site.py
"""

import argparse
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STATIC = ["/styles.css", "/nav.js", "/config.js", "/theme.js",
          "/preloader.js", "/preloader.css", "/metrika.js"]
PAIRS = [
    (ROOT / "styles.src.css", ROOT / "styles.css"),
    (ROOT / "nav.src.js", ROOT / "nav.js"),
]


def run(cmd, cwd=ROOT):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"❌ {cmd[0]} failed:\n{r.stderr[-800:]}")
        sys.exit(1)
    return r.stdout


def build():
    for src, out in PAIRS:
        if not src.exists():
            print(f"❌ source missing: {src}")
            sys.exit(1)
        run(["npx", "esbuild", str(src), "--minify", "--charset=utf8", "--outfile=" + str(out)])
        print(f"✅ {src.name} → {out.name} ({out.stat().st_size} Б)")


def bump_version(version):
    pattern = r'(\?v=)(\d{8})'
    n = 0
    for f in ROOT.rglob("*.html"):
        if "_github" in f.parts or "node_modules" in f.parts or "archive" in f.parts:
            continue
        html = f.read_text("utf-8", errors="replace")
        new, count = re.subn(pattern, rf"\g<1>{version}", html)
        if count:
            f.write_text(new)
            n += count
    print(f"✅ версия → v={version}: обновлено {n} ссылок")
    return n


def verify():
    print("🔬 node --check nav.js...")
    run(["node", "--check", str(ROOT / "nav.js")])
    print("✅ nav.js валиден")
    print("🔬 test_site.py...")
    run([sys.executable, str(ROOT / "test_site.py")])


def main():
    parser = argparse.ArgumentParser(description="AXIIOM build: minify + cache-bust")
    parser.add_argument("--version", default=datetime.now().strftime("%Y%m%d"))
    parser.add_argument("--no-test", action="store_true", help="skip test_site.py")
    args = parser.parse_args()
    build()
    bump_version(args.version)
    if not args.no_test:
        verify()
    print("✅ build done")


if __name__ == "__main__":
    main()
