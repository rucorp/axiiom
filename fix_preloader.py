#!/usr/bin/env python3
import pathlib, re

# Find all html
for p in pathlib.Path('.').rglob('*.html'):
    if '_github' in str(p) or 'node_modules' in str(p):
        continue
    try:
        html = p.read_text(encoding='utf-8')
    except:
        continue
    if "sessionStorage.getItem('_seen')" not in html:
        continue
    # If already has fallback marker, skip
    if "preloader-fallback" in html:
        continue
    # Replace the inline script that handles preloader
    # Original ends with )})()
    # We want to add setTimeout fallback before final )})()
    # Pattern: window.addEventListener('load',function(){...}}})()
    # Add after that: ;setTimeout(function(){var q=document.getElementById('preloader');if(q){q.classList.add('hidden');setTimeout(function(){q.classList.add('hidden-done')},500)}},2500);/*preloader-fallback*/
    # Simple replacement: replace "})})()" with "});setTimeout(function(){var q=document.getElementById('preloader');if(q){q.classList.add('hidden');setTimeout(function(){q.classList.add('hidden-done')},500)}},2500)/*preloader-fallback*/})()"
    # Need to be careful: there are two })() - one for inner load, one for outer IIFE
    # The script is: (function(){var p=...;...window.addEventListener('load',function(){...})})()
    # So we want to insert fallback before the final })()
    # Let's do regex for window.addEventListener('load',function(){...}})()
    # Simpler: replace the exact ending "}}})()" with "}});setTimeout(...},2500)/*preloader-fallback*/})()"
    if "}}})()" in html:
        html = html.replace("}}})()", "}});setTimeout(function(){var q=document.getElementById('preloader');if(q){q.classList.add('hidden');setTimeout(function(){q.classList.add('hidden-done')},500)}},2500)/*preloader-fallback*/})()", 1)
        p.write_text(html, encoding='utf-8')
        print(f"fixed {p}")
    else:
        # try alternative pattern
        # Look for window.addEventListener('load',function(){...}})()
        # We'll just append fallback before </script> of preloader
        # Find <script>(function(){var p=document.getElementById('preloader')
        # and insert fallback before </script>
        m = re.search(r"(<script>\(function\(\)\{var p=document\.getElementById\('preloader'\).*?)</script>", html, re.DOTALL)
        if m:
            old = m.group(1)
            new = old + ";setTimeout(function(){var q=document.getElementById('preloader');if(q){q.classList.add('hidden');setTimeout(function(){q.classList.add('hidden-done')},500)}},2500)/*preloader-fallback*/"
            html = html.replace(old, new, 1)
            p.write_text(html, encoding='utf-8')
            print(f"fixed alt {p}")

print("done")
