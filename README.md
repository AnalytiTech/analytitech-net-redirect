# analytitech.net → analytitech.com

GitHub Pages site for the old analytitech.net domain. Every URL (including
paths used by the shipped apps, like /privacy/ and /bodyblitz/support/) is
sent to the same path on analytitech.com. 404.html does the work for every
path; index.html covers the homepage. The real site lives in formforward-website.

Each known page also has its own `<path>/index.html` (made by
`python3 make_stubs.py` from analytitech.com/sitemap.xml) so those URLs return
HTTP 200 instead of 404. App-store review bots reject 404 privacy/support
links even when a browser would follow the redirect. Re-run the script when
the main site gains pages.
