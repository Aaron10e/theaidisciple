#!/usr/bin/env python3
"""Static build for theaidisciple.com — composes pages from fragments in pages/."""
import json, os, re, datetime, html, pathlib

ROOT = pathlib.Path(__file__).parent
SITE = "https://www.theaidisciple.com"
TODAY = datetime.date.today().isoformat()

LOGO = (
    '<svg class="brand__mark" viewBox="0 0 100 100" aria-hidden="true"><path d="M50,73.0 L50,81.5" stroke="var(--color-accent)" stroke-width="4.0"/><path d="M33.0,84.5 L67.0,84.5" stroke="var(--color-accent)" stroke-width="4.0" stroke-linecap="round"/><rect x="4.0" y="15.0" width="92.0" height="58.0" rx="6.0" ry="6.0" fill="#0b0e14" stroke="var(--color-accent)" stroke-width="4.0"/><g transform="translate(11.07,3.48) scale(0.7945)" fill="none" stroke="#ffffff" stroke-width="8.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12,75 L29,27 L46,75 M17.4,59.6 L40.6,59.6"/><path d="M59,26.3 L59,75.7"/><path d="M59,26.3 C77,26.3 86,36 86,51 C86,66 77,75.7 59,75.7"/></g></svg>'
)


def asset_v(rel):
    """Short content hash for cache busting.

    .htaccess serves css/js as `immutable, max-age=31536000`, so a returning
    visitor would keep the old file for up to a year. HTML is must-revalidate,
    so versioning the URL here is what actually ships CSS/JS changes.
    """
    import hashlib
    f = ROOT / rel.lstrip("/")
    if not f.exists():
        return ""
    return "?v=" + hashlib.md5(f.read_bytes()).hexdigest()[:8]


NAV = [
    ("/services.html", "Services"),
    ("/for-churches.html", "For Churches"),
    ("/free-training.html", "Free Training"),
    ("/videos.html", "Videos"),
    ("/about.html", "About"),
    ("/faq.html", "FAQ"),
]

SOCIALS = [
    ("YouTube", "https://www.youtube.com/@theaidiscipledesk",
     '<path d="M23.5 6.2a3 3 0 0 0-2.1-2.1C19.5 3.5 12 3.5 12 3.5s-7.5 0-9.4.6A3 3 0 0 0 .5 6.2C0 8.1 0 12 0 12s0 3.9.5 5.8a3 3 0 0 0 2.1 2.1c1.9.6 9.4.6 9.4.6s7.5 0 9.4-.6a3 3 0 0 0 2.1-2.1c.5-1.9.5-5.8.5-5.8s0-3.9-.5-5.8zM9.5 15.6V8.4L15.8 12l-6.3 3.6z"/>'),
    ("Facebook", "https://www.facebook.com/theaidiscipledesk",
     '<path d="M24 12.07C24 5.44 18.63.07 12 .07S0 5.44 0 12.07c0 5.99 4.39 10.95 10.13 11.85v-8.38H7.08v-3.47h3.05V9.43c0-3.01 1.79-4.67 4.53-4.67 1.31 0 2.69.24 2.69.24v2.95h-1.51c-1.49 0-1.96.93-1.96 1.87v2.25h3.33l-.53 3.47h-2.8v8.38C19.61 23.02 24 18.06 24 12.07z"/>'),
    ("Instagram", "https://www.instagram.com/theaidiscipledesk",
     '<path d="M12 2.16c3.2 0 3.58.01 4.85.07 3.25.15 4.77 1.69 4.92 4.92.06 1.27.07 1.64.07 4.85s-.01 3.58-.07 4.85c-.15 3.23-1.66 4.77-4.92 4.92-1.27.06-1.64.07-4.85.07s-3.58-.01-4.85-.07c-3.26-.15-4.77-1.7-4.92-4.92C2.17 15.58 2.16 15.2 2.16 12s.01-3.58.07-4.85c.15-3.23 1.66-4.77 4.92-4.92C8.42 2.17 8.8 2.16 12 2.16zm0-2.16C8.74 0 8.33.01 7.05.07c-4.36.2-6.78 2.62-6.98 6.98C.01 8.33 0 8.74 0 12s.01 3.67.07 4.95c.2 4.36 2.62 6.78 6.98 6.98 1.28.06 1.69.07 4.95.07s3.67-.01 4.95-.07c4.35-.2 6.78-2.62 6.98-6.98.06-1.28.07-1.69.07-4.95s-.01-3.67-.07-4.95c-.2-4.35-2.62-6.78-6.98-6.98C15.67.01 15.26 0 12 0zm0 5.84a6.16 6.16 0 1 0 0 12.32 6.16 6.16 0 0 0 0-12.32zm0 10.16a4 4 0 1 1 0-8 4 4 0 0 1 0 8zm6.41-11.85a1.44 1.44 0 1 0 0 2.88 1.44 1.44 0 0 0 0-2.88z"/>'),
    ("TikTok", "https://www.tiktok.com/@theaidisciple",
     '<path d="M19.59 6.69a4.83 4.83 0 0 1-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 0 1-5.2 1.74 2.89 2.89 0 0 1 2.31-4.64 2.93 2.93 0 0 1 .88.13V9.4a6.84 6.84 0 0 0-1-.05A6.33 6.33 0 0 0 5 20.1a6.34 6.34 0 0 0 10.86-4.43v-7a8.16 8.16 0 0 0 4.77 1.52v-3.4a4.85 4.85 0 0 1-1-.1z"/>'),
    ("Pinterest", "https://www.pinterest.com/theaidisciple",
     '<path d="M12 0C5.37 0 0 5.37 0 12c0 5.08 3.16 9.42 7.59 11.2-.1-.95-.2-2.41.04-3.45.22-.95 1.4-6.05 1.4-6.05s-.36-.72-.36-1.78c0-1.66.97-2.9 2.17-2.9 1.02 0 1.51.76 1.51 1.68 0 1.02-.65 2.55-.99 3.97-.28 1.19.6 2.16 1.78 2.16 2.13 0 3.78-2.25 3.78-5.5 0-2.86-2.06-4.87-5-4.87-3.41 0-5.41 2.56-5.41 5.19 0 1.03.39 2.12.88 2.72a.35.35 0 0 1 .08.34c-.09.37-.29 1.19-.33 1.35-.05.22-.17.26-.4.16-1.49-.69-2.42-2.86-2.42-4.61 0-3.75 2.72-7.2 7.84-7.2 4.11 0 7.31 2.94 7.31 6.86 0 4.09-2.58 7.38-6.17 7.38-1.2 0-2.34-.62-2.72-1.36l-.74 2.82c-.27 1 1 1.87 2.95 1.87C18.63 24 24 18.63 24 12 24 5.37 18.63 0 12 0z"/>'),
]

# ---------------------------------------------------------------- shared schema
ORG = {
    "@type": ["ProfessionalService", "Organization"],
    "@id": f"{SITE}/#organization",
    "name": "The AI Disciple",
    "alternateName": "The AI Disciple — AI Consulting by Aaron Tenney",
    "url": f"{SITE}/",
    "logo": {"@type": "ImageObject", "url": f"{SITE}/assets/img/logo.png", "width": 512, "height": 512},
    "image": f"{SITE}/assets/img/og-home.png",
    "email": "aaron@theaidisciple.com",
    "telephone": "+1-559-718-1480",
    "founder": {"@id": f"{SITE}/#aaron"},
    "foundingDate": "2025",
    "slogan": "Practical AI without the hype.",
    "description": (
        "The AI Disciple is an AI consulting and training practice run by Aaron Tenney in Fresno, "
        "California. It helps small businesses, churches and nonprofits replace mundane, repetitive "
        "work with reliable, reusable AI workflows — and trains their teams to run those workflows "
        "without help."
    ),
    "knowsAbout": [
        "AI consulting", "AI workflow automation", "AI training for employees",
        "Generative AI adoption", "AI for nonprofits", "AI for churches",
        "Prompt engineering", "AI research workflows", "Web development", "Software modernization",
        "AI social media marketing", "AI avatar and voice clones", "Short-form video strategy",
    ],
    "areaServed": [
        {"@type": "City", "name": "Fresno", "containedInPlace": {"@type": "State", "name": "California"}},
        {"@type": "City", "name": "Clovis", "containedInPlace": {"@type": "State", "name": "California"}},
        {"@type": "AdministrativeArea", "name": "Central Valley, California"},
        {"@type": "Country", "name": "United States"},
    ],
    "serviceType": [
        "AI consulting", "AI strategy assessment", "AI workflow design",
        "AI staff training", "AI support retainer", "Website and software modernization",
        "AI social media marketing", "Personal brand AI clones",
    ],
    "availableLanguage": [
        {"@type": "Language", "name": "English"},
        {"@type": "Language", "name": "Urdu"},
    ],
    "address": {"@type": "PostalAddress", "addressLocality": "Fresno", "addressRegion": "CA", "addressCountry": "US"},
    "sameAs": ["https://www.linkedin.com/in/aaron10e"] + [s[1] for s in SOCIALS],
    "contactPoint": {
        "@type": "ContactPoint",
        "contactType": "Sales and inquiries",
        "email": "aaron@theaidisciple.com",
        "telephone": "+1-559-718-1480",
        "areaServed": "US",
        "availableLanguage": ["English", "Urdu"],
    },
}

PERSON = {
    "@type": "Person",
    "@id": f"{SITE}/#aaron",
    "name": "Aaron Tenney",
    "givenName": "Aaron",
    "familyName": "Tenney",
    "jobTitle": "AI Consultant and Trainer",
    "url": f"{SITE}/about.html",
    "image": f"{SITE}/assets/img/aaron-tenney.jpg",
    "email": "aaron@theaidisciple.com",
    "worksFor": {"@id": f"{SITE}/#organization"},
    "homeLocation": {"@type": "Place", "address": {"@type": "PostalAddress", "addressLocality": "Fresno", "addressRegion": "CA", "addressCountry": "US"}},
    "description": (
        "Aaron Tenney is an AI consultant and trainer based in Fresno, California, with 35 years of "
        "professional software development experience and five years working hands-on with generative "
        "AI. He helps small businesses, churches and nonprofits adopt AI workflows that survive contact "
        "with real staff and real deadlines."
    ),
    "knowsAbout": [
        "Generative AI", "Large language models", "AI workflow automation",
        "Prompt engineering", "C#", "ASP.NET", "Angular", "TypeScript",
        "AI video production", "Bilingual content production",
        "AI avatar clones", "Social media marketing",
    ],
    "knowsLanguage": ["English", "Urdu"],
    "sameAs": ["https://www.linkedin.com/in/aaron10e"] + [s[1] for s in SOCIALS],
}

WEBSITE = {
    "@type": "WebSite",
    "@id": f"{SITE}/#website",
    "url": f"{SITE}/",
    "name": "The AI Disciple",
    "description": "Practical AI consulting and training for small businesses, churches and nonprofits.",
    "publisher": {"@id": f"{SITE}/#organization"},
    "inLanguage": "en-US",
}


def breadcrumbs(trail):
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name,
             "item": SITE + path}
            for i, (path, name) in enumerate(trail)
        ],
    }


HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<meta name="author" content="Aaron Tenney">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
<meta name="geo.region" content="US-CA">
<meta name="geo.placename" content="Fresno, California">

<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="The AI Disciple">
<meta property="og:locale" content="en_US">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{og_title}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{og_title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{og_image}">

<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<meta name="theme-color" content="#faf7f1" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0e1218" media="(prefers-color-scheme: dark)">

<link rel="preconnect" href="https://api.fontshare.com" crossorigin>
<link rel="preconnect" href="https://cdn.fontshare.com" crossorigin>
<link rel="stylesheet" href="https://api.fontshare.com/v2/css?f[]=satoshi@400,500,600,700&f[]=zodiak@400,500,600&display=swap">
<link rel="stylesheet" href="/assets/css/base.css{BASE_V}">
<link rel="stylesheet" href="/assets/css/site.css{SITE_V}">
{extra_head}
<script type="application/ld+json">{schema}</script>
</head>
<body>
<a class="skip-link" href="#main">Skip to main content</a>
{header}
<main id="main">
{body}
</main>
{footer}
<script src="/assets/js/site.js{JS_V}" defer></script>
</body>
</html>
"""


def header_html(active):
    links = "".join(
        f'<li><a href="{h}"{" aria-current=\"page\"" if h == active else ""}>{t}</a></li>'
        for h, t in NAV
    )
    return f"""<header class="site-header">
  <div class="container site-header__inner">
    <a class="brand" href="/" aria-label="The AI Disciple — home">
      {LOGO}
      <span class="brand__text">
        <span class="brand__name">The AI Disciple</span>
        <span class="brand__tag">AI consulting &middot; Fresno, CA</span>
      </span>
    </a>
    <nav aria-label="Main">
      <ul class="nav" id="primary-nav" data-open="false">
        {links}
        <li class="nav__cta"><a class="btn btn--primary" href="/contact.html">Book a free call</a></li>
      </ul>
    </nav>
    <div class="header__actions">
      <a class="btn btn--primary" href="/contact.html" data-desktop-cta>Book a free call</a>
      <button class="icon-btn" data-theme-toggle type="button" aria-label="Switch to dark mode">
        <svg class="sun" width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>
        <svg class="moon" width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>
      </button>
      <button class="icon-btn nav-toggle" data-nav-toggle type="button" aria-label="Open menu" aria-expanded="false" aria-controls="primary-nav">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
      </button>
    </div>
  </div>
</header>"""


def footer_html():
    socials = "".join(
        f'<a href="{url}" target="_blank" rel="noopener" aria-label="{name}">'
        f'<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">{path}</svg></a>'
        for name, url, path in SOCIALS
    )
    return f"""<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-about">
        <a class="brand" href="/" aria-label="The AI Disciple — home">
          {LOGO}
          <span class="brand__text"><span class="brand__name">The AI Disciple</span>
          <span class="brand__tag">AI consulting &middot; Fresno, CA</span></span>
        </a>
        <p>Practical AI consulting and training for small businesses, churches and nonprofits &mdash; based in Fresno, California, working with clients across the United States and overseas.</p>
        <div class="social-row">{socials}</div>
      </div>
      <div>
        <h3>Services</h3>
        <ul>
          <li><a href="/services.html#assessment">AI assessment</a></li>
          <li><a href="/services.html#workflows">Workflow design</a></li>
          <li><a href="/services.html#training">Team training</a></li>
          <li><a href="/services.html#retainer">Ongoing support</a></li>
          <li><a href="/services.html#software">Web &amp; software</a></li>
          <li><a href="/services.html#media">Church &amp; ministry video</a></li>
        </ul>
      </div>
      <div>
        <h3>Explore</h3>
        <ul>
          <li><a href="/for-churches.html">For churches</a></li>
          <li><a href="/free-training.html">Free AI training</a></li>
          <li><a href="/videos.html">Watch the work</a></li>
          <li><a href="/bible-stories.html">Bible story library</a></li>
          <li><a href="/download.html">Free AI QuickStart</a></li>
          <li><a href="/about.html">About Aaron</a></li>
          <li><a href="/faq.html">Questions answered</a></li>
          <li><a href="/contact.html">Contact</a></li>
        </ul>
      </div>
      <div>
        <h3>Get in touch</h3>
        <ul>
          <li><a href="mailto:aaron@theaidisciple.com">aaron@theaidisciple.com</a></li>
          <li><a href="tel:+15597181480">(559) 718-1480</a></li>
          <li><a href="/contact.html">Book a free 20-minute call</a></li>
          <li class="muted">Fresno &amp; Clovis, California<br>Remote across the US</li>
          <li class="muted">Replies within one business day</li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p>&copy; <span data-year>2026</span> The AI Disciple &middot; Aaron Tenney. All rights reserved.</p>
      <p>Page last reviewed {TODAY}</p>
    </div>
  </div>
</footer>"""


_ABS = re.compile(r'((?:href|src)=")/(?!/)([^"]*)"')


def _relativize(doc):
    """Root-absolute asset/page links -> document-relative, so the site works
    both at a domain root and inside a subdirectory preview."""
    return _ABS.sub(lambda m: f'{m.group(1)}{m.group(2) or "index.html"}"', doc)


def build_page(slug, title, description, body, schema_extra, active=None,
               og_title=None, og_image=None, og_type="website", extra_head=""):
    canonical = f"{SITE}/" if slug == "index.html" else f"{SITE}/{slug}"
    graph = [ORG, PERSON, WEBSITE] + schema_extra
    schema = json.dumps({"@context": "https://schema.org", "@graph": graph},
                        ensure_ascii=False, separators=(",", ":"))
    out = _relativize(HEAD.format(
        title=html.escape(title), description=html.escape(description),
        canonical=canonical, og_title=html.escape(og_title or title),
        og_image=og_image or f"{SITE}/assets/img/og-home.png",
        og_type=og_type, schema=schema, extra_head=extra_head,
        header=header_html(active or ("/" + slug if slug != "index.html" else "/")),
        body=body, footer=footer_html(),
        BASE_V=asset_v("assets/css/base.css"),
        SITE_V=asset_v("assets/css/site.css"),
        JS_V=asset_v("assets/js/site.js"),
    ))
    (ROOT / slug).write_text(out, encoding="utf-8")
    print(f"  built {slug:24s} {len(out)//1024:>4} KB")
