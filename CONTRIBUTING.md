# Contributing to AXIIOM

Thank you for your interest in contributing to **AXIIOM** (ООО «Аксиома»), the
source of the [axiiom.ru](https://axiiom.ru) website. This document explains how
to work with this repository.

## What this repository is

This is a **pure static site** built from vanilla HTML, CSS, and JavaScript.
There is no framework, no bundler runtime, and no server-side code in the
repository itself. The site is generated and validated by two Python scripts:

* `build.py` — bundles the source assets (`nav.src.js`, `styles.src.css`) into
  minified artifacts (`nav.js`, `styles.css`) using `esbuild --minify`.
* `test_site.py` — runs the regression suite (currently **79 pages** and
  **3476 checks**). Pass `--dynamic` to also validate theme (dark/light)
  behavior in a headless browser.

## Ground rules

1. **Never edit the minified artifacts directly.** Do not hand-edit `nav.js` or
   `styles.css`. Edit the source files `nav.src.js` and `styles.src.css`, then
   rebuild.
2. **Rebuild after changing sources.** After editing `nav.src.js` or
   `styles.src.css`, run the build so the committed artifacts stay in sync.
3. **Keep the sitemap and navigation in sync.** When you add a new page, add it
   to `sitemap.xml` **and** register it in `nav.src.js` so it appears in the
   site navigation.
4. **Run the tests before opening a PR.** Make sure `python3 test_site.py`
   passes locally. Use `python3 test_site.py --dynamic` for theme-related
   changes.

## Development workflow

```bash
# 1. Make your changes to source files (HTML, *.src.js, *.src.css)
# 2. Rebuild minified assets
python3 build.py

# 3. Run the regression suite
python3 test_site.py
# Optional: validate dark/light theme behavior
python3 test_site.py --dynamic
```

## Commit message style

Conventional Commits are **optional** but appreciated. A clean history helps
reviewers and powers the auto-generated release notes (see `.github/release.yml`).

Examples:

* `feat: add fintech API demo page`
* `fix: correct contrast on dark theme footer`
* `docs: clarify build steps in CONTRIBUTING`
* `chore: bump esbuild version`

## Pull request flow

1. Fork the repository and create a branch from `main` (e.g.
   `fix/footer-contrast` or `feat/api-demo`).
2. Make your changes following the ground rules above.
3. Run `python3 build.py` and `python3 test_site.py` (add `--dynamic` for
   theme work). Ensure both succeed.
4. Open a pull request against `main` and fill in the PR template.
5. Describe what changed, why, and how you verified it. Link any related issue.
6. A maintainer will review. Please be responsive to feedback.

## Reporting issues

Use the GitHub issue templates:

* **Bug report** — for broken pages, layout, or behavior.
* **Feature request** — for new pages, demos, or tools.

For security vulnerabilities, follow [SECURITY.md](./SECURITY.md) and report
privately to **hello@axiiom.ru**. Do not open a public issue for security
problems.

## Code of conduct

By participating, you agree to abide by our
[Code of Conduct](./CODE_OF_CONDUCT.md).

## Maintainer

Repository maintained by [@bestdeejay-design](https://github.com/bestdeejay-design)
on behalf of ООО «Аксиома». Contact: **hello@axiiom.ru**.
