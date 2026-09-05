# theaidisciple.com

Static site for The AI Disciple (Aaron Tenney, Fresno CA). Server-rendered from
Python templates at build time — no runtime framework, no JS dependency for content.

## Layout

```
build.py            shared chrome: <head>, nav, footer, schema helpers, page writer
make_site.py        the build. Reads pages/*.html + data/*.json, writes the site to the repo root
faq_data.py         all FAQ Q&A. `show_on_homepage` flag controls the homepage preview block
make_og.py          regenerates assets/img/og-*.png social cards (PIL)
pages/*.html        body content only — no <head>, no nav, no footer
data/stories.json   the 84 children's Bible stories (bible-stories.html)
data/church_films.json  the 12 narrated Scripture films (for-churches.html)
assets/             css, js, images — copied as-is
```

Everything in the repo root ending in `.html`, plus `sitemap.xml`, `robots.txt`
and `llms.txt`, is **generated**. Do not hand-edit those — your changes get
overwritten on the next build. Edit `pages/` and `faq_data.py` instead.

## Build

```bash
python3 make_site.py
```

No dependencies except Pillow, and that is only needed for `make_og.py`.

## Preview locally

```bash
python3 -m http.server 8899
# http://localhost:8899
```

## Deploy to Bluehost

Upload the generated files to `public_html`:

- all `*.html` in the repo root
- `assets/`
- `robots.txt`, `sitemap.xml`, `llms.txt`, `favicon.svg`, `.htaccess`

Do **not** upload `pages/`, `data/`, `build.py`, `make_site.py`, `faq_data.py`,
`make_og.py` or `.git` — none of it is needed at runtime and `data/` would
expose the raw JSON.

`.htaccess` is a hidden file. In cPanel File Manager, enable **Show Hidden
Files** or it will silently not upload, and you lose the HTTPS redirect, the
www canonicalisation, the legacy 301s and the cache headers.

## Conventions

- **US spelling throughout** (organization, modernization, recognize, license,
  counseling). British spellings are a recurring regression — grep before shipping.
- No pricing anywhere on the site. Rates are quoted on a call, not published.
- Fonts: Zodiak (display serif) + Satoshi (body), both from Fontshare.
- Colors: cream `#faf7f1`, ink navy `#10141c`, cobalt `#0b4f9e` light /
  `#5f9ae0` dark. Defined once in `assets/css/base.css`.
- Contact form posts to Formspree. The `?interest=` query string on
  `contact.html` preselects the dropdown — see the IIFE in `assets/js/site.js`.
- Structured data (Service, Course, FAQPage, VideoObject, LocalBusiness) is
  emitted from `make_site.py`. Validate with Google's Rich Results Test after
  changing it.

## Adding a story or a film

Append to `data/stories.json` or `data/church_films.json` and rebuild. Video
thumbnails are pulled from `https://i.ytimg.com/vi/<ID>/hqdefault.jpg`, so the
YouTube ID is the only image you need to supply.
