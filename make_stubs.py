#!/usr/bin/env python3
"""Write a real index.html redirect page for every analytitech.com path.

GitHub Pages serves 404.html with HTTP status 404, and app-store review bots
treat that as a broken link even though browsers follow the JS redirect. A
real <path>/index.html returns 200, so the old .net privacy/support/terms
URLs that shipped apps and store listings use stay valid.

Run:  python3 make_stubs.py   (paths come from analytitech.com/sitemap.xml
plus EXTRA_PATHS), then commit and push.
"""
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXTRA_PATHS = ["/diversion/", "/diversion/privacy/"]  # used by app builds, not in sitemap yet

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>AnalytiTech has moved to analytitech.com</title>
<link rel="canonical" href="https://analytitech.com{path}">
<script>
  // Send this page to the same page on analytitech.com (apps and old links use .net paths).
  location.replace("https://analytitech.com" + location.pathname + location.search + location.hash);
</script>
<meta http-equiv="refresh" content="1; url=https://analytitech.com{path}">
<style>body{{font:16px/1.5 system-ui,sans-serif;background:#071417;color:#E7F3F1;display:grid;place-items:center;min-height:100vh;margin:0}}a{{color:#2FD6BE}}</style>
</head>
<body>
<p>AnalytiTech has moved. This page is now at <a href="https://analytitech.com{path}">analytitech.com{path}</a>.</p>
</body>
</html>
"""


def main():
    xml = urllib.request.urlopen("https://analytitech.com/sitemap.xml").read().decode()
    paths = {re.sub(r"^https://analytitech\.com", "", u) or "/" for u in re.findall(r"<loc>([^<]+)</loc>", xml)}
    paths |= set(EXTRA_PATHS)
    for p in sorted(paths):
        if p == "/":
            continue  # index.html at the root already handles the homepage
        out = ROOT / p.strip("/") / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(TEMPLATE.format(path=p))
        print("wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    main()
