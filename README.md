<div align="center"><img src="assets/banner.svg" width="100%"><h1>SitemapLint</h1><p>Validate sitemap XML before search engines encounter it.</p></div>

## Checks
- Recognizes both `urlset` and `sitemapindex`.
- Requires absolute HTTP(S) locations.
- Detects duplicate locations and malformed `lastmod` values.
- Reports entry counts and machine-readable JSON.
- Does not crawl URLs or send network requests.

## Run
```bash
python app.py sitemap.xml
python app.py sitemap.xml --json
```
Python 3.9+, standard library only. Supports sitemap XML files that fit in memory.

## Tests
```bash
python -m unittest discover -s tests -v
```
MIT License.