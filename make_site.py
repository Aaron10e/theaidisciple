#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Assemble every page of theaidisciple.com."""
import json, html, pathlib, re
from build import (ROOT, SITE, TODAY, build_page, breadcrumbs, NAV)
from faq_data import FAQS

FRAG = ROOT / "pages"
STORIES = json.loads((ROOT / "data" / "stories.json").read_text(encoding="utf-8"))
PLAYLISTS = json.loads((ROOT / "data" / "playlists.json").read_text(encoding="utf-8"))
URDU = re.compile(r"[\u0600-\u06FF]")

# (key -> true playlist size on YouTube, verified 2026-09-08, and a one-line blurb)
CAT_META = {
    "guide":      (128, "Practical teaching on using AI honestly and well."),
    "research":   (147, "Archaeology, history and the biblical text, with the sources shown."),
    "liveaction": (149, "Narrated Scripture films built for congregations and sermon use."),
    "testimony":  (34,  "True accounts from real people, in their own words."),
    "cartoons":   (84,  "Animated Bible stories for children, free for Sunday school."),
    "main":       (38,  "The main category, where the newest work lands first."),
}
PER_CAT = 15  # cards rendered per category on /videos.html


def strip_tags(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()


# ---------------------------------------------------------------- FAQ rendering
def faq_html(items):
    out = []
    for i, (q, a, _) in enumerate(items):
        out.append(
            f'<details class="faq-item"{" open" if i == 0 else ""}>'
            f'<summary><span>{q}</span>'
            f'<svg class="faq-item__icon" width="18" height="18" viewBox="0 0 24 24" fill="none" '
            f'stroke="currentColor" stroke-width="2.2" stroke-linecap="round" '
            f'aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg></summary>'
            f'<div class="faq-item__answer">{a}</div></details>'
        )
    return "\n      ".join(out)


def faq_schema(items, page_url):
    return {
        "@type": "FAQPage",
        "@id": f"{page_url}#faq",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}}
            for q, a, _ in items
        ],
    }


HOME_FAQS = [f for f in FAQS if f[2]]

# ---------------------------------------------------------------- HOME VIDEO SAMPLE
EMOJI = re.compile(
    "[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF"
    "\u2b00-\u2bff\ufe0f\u200d\u20e3\u2190-\u21ff\u2300-\u23ff]+")


def strip_emoji(text):
    """Homepage cards sit in polished consulting copy, so titles run clean."""
    out = EMOJI.sub(" ", text)
    out = re.sub(r"\s{2,}", " ", out).strip()
    return re.sub(r"^[\s\-\u2013\u2014|:,.]+", "", out).strip()


# Aaron's rate card never appears on this site. Imported YouTube copy
# occasionally quotes third-party tool prices ("$29/mo"), which a reader or an
# AI summarizer could mistake for his pricing, so drop those videos entirely.
MONEY = re.compile(r"[$\u00a3\u20ac]\s?\d|\b\d+\s?(?:USD|usd)\b")

for _cat in PLAYLISTS["categories"]:
    _cat["videos"] = [
        _v for _v in _cat["videos"]
        if not MONEY.search(_v["title"]) and not MONEY.search(_v.get("desc", ""))
    ]


def _pick_home_video(cat):
    """One representative video per category, preferring an English title."""
    for v in cat["videos"]:
        if not URDU.search(v["title"]):
            return v
    return cat["videos"][0] if cat["videos"] else None


home_video_cards = []
for cat in PLAYLISTS["categories"]:
    v = _pick_home_video(cat)
    if not v:
        continue
    total, blurb = CAT_META[cat["key"]]
    clean = strip_emoji(v["title"])
    if len(clean) > 62:
        cut = clean[:62].rsplit(" ", 1)[0].rstrip(" ,.:;|-\u2013\u2014")
        clean = cut + "\u2026"
    title = html.escape(v["title"])
    short = html.escape(clean)
    home_video_cards.append(f"""<article class="video-card reveal">
        <div class="video-frame" data-video-embed="{v['id']}" data-title="{title}">
          <img src="https://i.ytimg.com/vi/{v['id']}/hqdefault.jpg" width="480" height="360" alt="Video thumbnail: {title}" loading="lazy" decoding="async">
          <button type="button" class="video-frame__play" aria-label="Play {title}"><span><svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5.5v13l11-6.5z"/></svg></span></button>
        </div>
        <div class="video-card__body">
          <p class="video-card__cat"><a href="/videos.html?category={cat['key']}">{html.escape(cat['label'])}</a> <span>{total} videos</span></p>
          <h3>{short}</h3>
          <p>{html.escape(blurb)}</p>
        </div>
      </article>""")

# ---------------------------------------------------------------- HOME
body = (FRAG / "index.html").read_text(encoding="utf-8")
body = body.replace("__FAQ_PREVIEW__", faq_html(HOME_FAQS))
body = body.replace("__HOME_VIDEOS__", "\n      ".join(home_video_cards))

service_list = [
    ("AI Opportunity Assessment", "A structured working session that maps how a team spends its week and ranks the tasks AI can reliably take over.", "/services.html#assessment"),
    ("AI Workflow Design and Build", "Design and construction of repeatable AI workflows: prompts, templates, verification steps and written run-books.", "/services.html#workflows"),
    ("AI Team Training and Adoption", "Hands-on AI training for staff using their real work, plus follow-up clinics and a plain-language usage policy.", "/services.html#training"),
    ("Ongoing AI Support Retainer", "Monthly retained support for organizations running AI workflows, with priority response and quarterly reviews.", "/services.html#retainer"),
    ("Website and Software Modernization", "Website rebuilds and custom development in C#, ASP.NET, Angular and modern web technologies.", "/services.html#software"),
    ("Church, Ministry and Nonprofit Video Production", "Narrated Scripture films, teaching series, children's Bible cartoons and testimony films for churches and nonprofits, in English, Urdu and other languages.", "/services.html#media"),
    ("AI Social Media Marketing and Personal Brand Clones", "AI presenter clones built from a client's own face and voice with their consent, plus social media strategy, platform selection and a repeatable short-form video production workflow for YouTube, TikTok and Instagram.", "/services.html#social"),
]

offer_catalog = {
    "@type": "OfferCatalog",
    "@id": f"{SITE}/#services",
    "name": "AI consulting services",
    "itemListElement": [
        {"@type": "Offer", "itemOffered": {
            "@type": "Service", "name": n, "description": d,
            "url": SITE + u, "serviceType": n,
            "provider": {"@id": f"{SITE}/#organization"},
            "areaServed": [{"@type": "City", "name": "Fresno"}, {"@type": "Country", "name": "United States"}],
        }} for n, d, u in service_list
    ],
}

home_webpage = {
    "@type": "WebPage",
    "@id": f"{SITE}/#webpage",
    "url": f"{SITE}/",
    "name": "AI Consulting in Fresno, California | The AI Disciple",
    "isPartOf": {"@id": f"{SITE}/#website"},
    "about": {"@id": f"{SITE}/#organization"},
    "primaryImageOfPage": f"{SITE}/assets/img/og-home.png",
    "datePublished": "2025-06-01",
    "dateModified": TODAY,
    "inLanguage": "en-US",
    "description": "Practical AI consulting and training for small businesses, churches and nonprofits, based in Fresno, California.",
}

build_page(
    "index.html",
    "AI Consulting in Fresno, CA | Practical AI Training | The AI Disciple",
    "AI consulting and training for small businesses, churches and nonprofits in Fresno, California. Aaron Tenney turns repetitive work into reliable AI workflows your team will actually use. Free 20-minute call.",
    body,
    [home_webpage, offer_catalog, faq_schema(HOME_FAQS, f"{SITE}/"),
     {**breadcrumbs([("/", "Home")]), "@id": f"{SITE}/#breadcrumb"}],
    active="/",
    og_title="AI Consulting in Fresno, California — The AI Disciple",
)

# ---------------------------------------------------------------- SERVICES
build_page(
    "services.html",
    "AI Consulting Services — Assessment, Workflows, Training | The AI Disciple",
    "Seven AI consulting services for small businesses, churches and nonprofits: opportunity assessment, workflow design and build, team training, ongoing support retainer, website modernization, nonprofit media production and AI social media marketing with personal brand clones.",
    (FRAG / "services.html").read_text(encoding="utf-8"),
    [
        {"@type": "WebPage", "@id": f"{SITE}/services.html#webpage",
         "url": f"{SITE}/services.html", "name": "AI Consulting Services",
         "isPartOf": {"@id": f"{SITE}/#website"}, "dateModified": TODAY,
         "about": {"@id": f"{SITE}/#organization"}},
        offer_catalog,
        {"@type": "ItemList", "@id": f"{SITE}/services.html#list",
         "name": "AI consulting services offered by The AI Disciple",
         "numberOfItems": len(service_list),
         "itemListElement": [
             {"@type": "ListItem", "position": i + 1, "name": n, "url": SITE + u}
             for i, (n, d, u) in enumerate(service_list)]},
        {**breadcrumbs([("/", "Home"), ("/services.html", "Services")]),
         "@id": f"{SITE}/services.html#breadcrumb"},
    ],
    og_title="AI Consulting Services — The AI Disciple",
    og_image=f"{SITE}/assets/img/og-services.png",
)

# ---------------------------------------------------------------- ABOUT
build_page(
    "about.html",
    "About Aaron Tenney — AI Consultant in Fresno, California | The AI Disciple",
    "Aaron Tenney is an AI consultant and trainer in Fresno, California, with 35 years of professional software development and five years working hands-on with generative AI, including AI consulting at IBM.",
    (FRAG / "about.html").read_text(encoding="utf-8"),
    [
        {"@type": "AboutPage", "@id": f"{SITE}/about.html#webpage",
         "url": f"{SITE}/about.html", "name": "About Aaron Tenney",
         "isPartOf": {"@id": f"{SITE}/#website"}, "dateModified": TODAY,
         "mainEntity": {"@id": f"{SITE}/#aaron"}},
        {**breadcrumbs([("/", "Home"), ("/about.html", "About")]),
         "@id": f"{SITE}/about.html#breadcrumb"},
    ],
    og_title="About Aaron Tenney — AI Consultant, Fresno CA",
    og_image=f"{SITE}/assets/img/og-about.png",
    og_type="profile",
)

# ---------------------------------------------------------------- FAQ
faq_body = (FRAG / "faq.html").read_text(encoding="utf-8").replace("__FAQ_ALL__", faq_html(FAQS))
build_page(
    "faq.html",
    f"AI Consulting FAQ — {len(FAQS)} Straight Answers | The AI Disciple",
    "Answers to the questions people ask before hiring an AI consultant: what it costs, whether your data is safe, how long results take, which tools to use, and whether AI will replace your staff.",
    faq_body,
    [
        {"@type": "WebPage", "@id": f"{SITE}/faq.html#webpage",
         "url": f"{SITE}/faq.html", "name": "AI consulting questions and answers",
         "isPartOf": {"@id": f"{SITE}/#website"}, "dateModified": TODAY},
        faq_schema(FAQS, f"{SITE}/faq.html"),
        {**breadcrumbs([("/", "Home"), ("/faq.html", "FAQ")]),
         "@id": f"{SITE}/faq.html#breadcrumb"},
    ],
    og_title="AI Consulting FAQ — The AI Disciple",
    og_image=f"{SITE}/assets/img/og-faq.png",
)

# ---------------------------------------------------------------- CONTACT
build_page(
    "contact.html",
    "Book a Free 20-Minute AI Consultation | The AI Disciple, Fresno CA",
    "Book a free 20-minute call with Aaron Tenney, AI consultant in Fresno, California. No pitch, no obligation — an honest answer about whether AI can take work off your team's plate.",
    (FRAG / "contact.html").read_text(encoding="utf-8"),
    [
        {"@type": "ContactPage", "@id": f"{SITE}/contact.html#webpage",
         "url": f"{SITE}/contact.html", "name": "Contact The AI Disciple",
         "isPartOf": {"@id": f"{SITE}/#website"}, "dateModified": TODAY,
         "about": {"@id": f"{SITE}/#organization"}},
        {**breadcrumbs([("/", "Home"), ("/contact.html", "Contact")]),
         "@id": f"{SITE}/contact.html#breadcrumb"},
    ],
    og_title="Book a free 20-minute AI consultation",
    og_image=f"{SITE}/assets/img/og-contact.png",
)

# ---------------------------------------------------------------- DOWNLOAD
build_page(
    "download.html",
    "Free AI QuickStart Guide for Businesses & Ministries | The AI Disciple",
    "A free, practical AI QuickStart guide for business owners, pastors and nonprofit leaders: how to find the tasks AI can take over, what never to paste into a chat window, and how to check the output.",
    (FRAG / "download.html").read_text(encoding="utf-8"),
    [
        {"@type": "WebPage", "@id": f"{SITE}/download.html#webpage",
         "url": f"{SITE}/download.html", "name": "Free AI QuickStart Guide",
         "isPartOf": {"@id": f"{SITE}/#website"}, "dateModified": TODAY},
        {**breadcrumbs([("/", "Home"), ("/download.html", "Free Guide")]),
         "@id": f"{SITE}/download.html#breadcrumb"},
    ],
    og_title="Free AI QuickStart Guide",
    og_image=f"{SITE}/assets/img/og-download.png",
)

# ---------------------------------------------------------------- BIBLE STORIES


def lang_of(s):
    return "ur" if URDU.search(s["title"]) else "en"


cards, story_items = [], []
for i, s in enumerate(STORIES):
    lang = lang_of(s)
    date = (s.get("date") or "")[:10]
    nice = date
    title = html.escape(s["title"])
    desc = html.escape((s.get("desc") or "").strip()[:180])
    thumb = s.get("thumb") or f"https://i.ytimg.com/vi/{s['id']}/hqdefault.jpg"
    watch = f"https://www.youtube.com/watch?v={s['id']}"
    search_key = html.escape((s["title"] + " " + (s.get("desc") or "")).lower()[:300], quote=True)
    cards.append(f"""<article class="story" data-lang="{lang}" data-search="{search_key}">
        <a class="story__link" href="{watch}" data-video="{s['id']}" data-title="{title}">
          <div class="story__thumb">
            <span class="badge">{'Urdu' if lang == 'ur' else 'English'}</span>
            <img src="{thumb}" width="480" height="360" alt="Bible story film: {title}" loading="lazy" decoding="async">
            <span class="story__play"><span><svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5.5v13l11-6.5z"/></svg></span></span>
          </div>
          <div class="story__body">
            <h2 class="story__title">{title}</h2>
            <p class="story__desc">{desc}</p>
            <p class="story__meta"><time datetime="{date}">{nice}</time><span>Watch on YouTube</span></p>
          </div>
        </a>
      </article>""")
    story_items.append({
        "@type": "ListItem", "position": i + 1,
        "item": {
            "@type": "VideoObject",
            "name": s["title"],
            "description": (s.get("desc") or s["title"]).strip()[:300],
            "thumbnailUrl": thumb,
            "uploadDate": s.get("date") or TODAY,
            "contentUrl": watch,
            "embedUrl": f"https://www.youtube.com/embed/{s['id']}",
            "inLanguage": "ur" if lang == "ur" else "en",
            "publisher": {"@id": f"{SITE}/#organization"},
            "creator": {"@id": f"{SITE}/#aaron"},
            "isFamilyFriendly": True,
        },
    })

bs_body = (FRAG / "bible-stories.html").read_text(encoding="utf-8")
bs_body = bs_body.replace("__STORIES__", "\n      ".join(cards)).replace("__COUNT__", str(len(STORIES)))

build_page(
    "bible-stories.html",
    f"{len(STORIES)} Free Animated Bible Stories for Kids (English & Urdu) | The AI Disciple",
    f"A free library of {len(STORIES)} animated Bible story videos for children in English and Urdu, produced by The AI Disciple. Free to watch and free to use in Sunday school, church and home.",
    bs_body,
    [
        {"@type": "CollectionPage", "@id": f"{SITE}/bible-stories.html#webpage",
         "url": f"{SITE}/bible-stories.html",
         "name": "Animated Bible stories in English and Urdu",
         "isPartOf": {"@id": f"{SITE}/#website"}, "dateModified": TODAY,
         "inLanguage": ["en", "ur"],
         "description": f"A free library of {len(STORIES)} animated Bible story films for children, produced with AI in English and Urdu."},
        {"@type": "ItemList", "@id": f"{SITE}/bible-stories.html#list",
         "name": "Bible story film library", "numberOfItems": len(STORIES),
         "itemListElement": story_items},
        {**breadcrumbs([("/", "Home"), ("/bible-stories.html", "Bible Stories")]),
         "@id": f"{SITE}/bible-stories.html#breadcrumb"},
    ],
    og_title=f"{len(STORIES)} free animated Bible stories — English & Urdu",
    og_image=f"{SITE}/assets/img/og-stories.png",
)

# ---------------------------------------------------------------- VIDEOS

video_cards, video_items, chips, playlist_links = [], [], [], []
chips.append('<button type="button" class="chip" data-cat-filter="all" aria-pressed="true">All</button>')

seen_global, pos = set(), 0
for cat in PLAYLISTS["categories"]:
    key, label = cat["key"], cat["label"]
    total, blurb = CAT_META[key]
    pid = cat["playlistId"]
    chips.append(
        f'<button type="button" class="chip" data-cat-filter="{key}" aria-pressed="false">{html.escape(label)}</button>')
    playlist_links.append(
        f'<li><a href="https://www.youtube.com/playlist?list={pid}" target="_blank" rel="noopener">'
        f'<span class="cat-links__name">{html.escape(label)}</span>'
        f'<span class="cat-links__count">{total} videos</span></a>'
        f'<span class="cat-links__blurb">{html.escape(blurb)}</span></li>')

    seen_local = set()
    picked = 0
    for v in cat["videos"]:
        if picked >= PER_CAT:
            break
        if v["id"] in seen_local or v["id"] in seen_global:
            continue
        seen_local.add(v["id"])
        seen_global.add(v["id"])
        picked += 1
        pos += 1
        title = html.escape(v["title"])
        desc = html.escape((v.get("desc") or "").strip()[:180])
        date = (v.get("published") or "")[:10]
        thumb = f"https://i.ytimg.com/vi/{v['id']}/hqdefault.jpg"
        watch = f"https://www.youtube.com/watch?v={v['id']}"
        lang = "ur" if URDU.search(v["title"]) else "en"
        search_key = html.escape(
            (v["title"] + " " + label + " " + (v.get("desc") or "")).lower()[:300], quote=True)
        video_cards.append(f"""<article class="story" data-cat="{key}" data-search="{search_key}">
        <a class="story__link" href="{watch}" data-video="{v['id']}" data-title="{title}">
          <div class="story__thumb">
            <span class="badge">{html.escape(label)}</span>
            <img src="{thumb}" width="480" height="360" alt="Video: {title}" loading="lazy" decoding="async">
            <span class="story__play"><span><svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5.5v13l11-6.5z"/></svg></span></span>
          </div>
          <div class="story__body">
            <h2 class="story__title">{title}</h2>
            <p class="story__desc">{desc}</p>
            <p class="story__meta"><time datetime="{date}">{date}</time><span>Watch on YouTube</span></p>
          </div>
        </a>
      </article>""")
        video_items.append({
            "@type": "ListItem", "position": pos,
            "item": {
                "@type": "VideoObject",
                "name": v["title"],
                "description": (v.get("desc") or v["title"]).strip()[:300],
                "thumbnailUrl": thumb,
                "uploadDate": date or TODAY,
                "contentUrl": watch,
                "embedUrl": f"https://www.youtube.com/embed/{v['id']}",
                "inLanguage": lang,
                "genre": label,
                "publisher": {"@id": f"{SITE}/#organization"},
                "creator": {"@id": f"{SITE}/#aaron"},
                "isFamilyFriendly": True,
            },
        })

VIDEO_COUNT = len(video_cards)

vid_body = (FRAG / "videos.html").read_text(encoding="utf-8")
vid_body = (vid_body
            .replace("__CHIPS__", "\n      ".join(chips))
            .replace("__VIDEOS__", "\n      ".join(video_cards))
            .replace("__PLAYLIST_LINKS__", "\n        ".join(playlist_links))
            .replace("__COUNT__", str(VIDEO_COUNT)))

build_page(
    "videos.html",
    "Watch the Work — Six Categories of AI-Produced Video | The AI Disciple",
    "Browse The AI Disciple video channel by category: Christian AI guide, Biblical AI research, "
    "live-action Scripture stories, testimonies, animated Bible story cartoons and the main channel. "
    "471 videos produced in nine months in English and Urdu.",
    vid_body,
    [
        {"@type": "CollectionPage", "@id": f"{SITE}/videos.html#webpage",
         "url": f"{SITE}/videos.html",
         "name": "Watch the work — video categories",
         "isPartOf": {"@id": f"{SITE}/#website"}, "dateModified": TODAY,
         "inLanguage": ["en", "ur"],
         "description": "A sample of The AI Disciple video channel, organized into six categories, "
                        "with links to the full playlists on YouTube."},
        {"@type": "ItemList", "@id": f"{SITE}/videos.html#list",
         "name": "The AI Disciple video categories", "numberOfItems": VIDEO_COUNT,
         "itemListElement": video_items},
        {**breadcrumbs([("/", "Home"), ("/videos.html", "Videos")]),
         "@id": f"{SITE}/videos.html#breadcrumb"},
    ],
    og_title="Six categories of AI-produced video",
    og_image=f"{SITE}/assets/img/og-videos.png",
)


# ---------------------------------------------------------------- FOR CHURCHES
FILMS = json.loads((ROOT / "data" / "church_films.json").read_text(encoding="utf-8"))

film_cards, film_items = [], []
for i, f in enumerate(FILMS):
    title = html.escape(f["title"])
    ref = html.escape(f["ref"])
    desc = html.escape(f["desc"])
    series = html.escape(f["series"])
    thumb = f"https://i.ytimg.com/vi/{f['id']}/hqdefault.jpg"
    watch = f"https://www.youtube.com/watch?v={f['id']}"
    film_cards.append(f"""<article class="story">
        <a class="story__link" href="{watch}" data-video="{f['id']}" data-title="{title}">
          <div class="story__thumb">
            <span class="badge">{series}</span>
            <img src="{thumb}" width="480" height="360" alt="Video thumbnail: {title}" loading="lazy" decoding="async">
            <span class="story__play"><span><svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5.5v13l11-6.5z"/></svg></span></span>
          </div>
          <div class="story__body">
            <h3 class="story__title">{title}</h3>
            <p class="story__desc">{desc}</p>
            <p class="story__meta"><span>{ref}</span><span>Watch</span></p>
          </div>
        </a>
      </article>""")
    film_items.append({
        "@type": "ListItem", "position": i + 1,
        "item": {
            "@type": "VideoObject",
            "name": f["title"],
            "description": f["desc"],
            "thumbnailUrl": thumb,
            "uploadDate": "2026-01-05",
            "contentUrl": watch,
            "embedUrl": f"https://www.youtube.com/embed/{f['id']}",
            "inLanguage": f.get("lang", "en"),
            "publisher": {"@id": f"{SITE}/#organization"},
            "creator": {"@id": f"{SITE}/#aaron"},
            "isFamilyFriendly": True,
        },
    })

church_body = (FRAG / "for-churches.html").read_text(encoding="utf-8").replace(
    "__CHURCH_FILMS__", "\n      ".join(film_cards))

church_faqs = [f for f in FAQS if f[0] in (
    "Do you work with churches?",
    "What is a narrated Scripture film?",
    "Can you make videos for our church?",
)]

build_page(
    "for-churches.html",
    "Video and AI for Churches — Narrated Bible Films | The AI Disciple",
    "Narrated Scripture films, teaching series, children's Bible cartoons and AI training for churches and ministries. Watch real examples. Free AI training and free Sunday school material for churches getting started.",
    church_body,
    [
        {"@type": "WebPage", "@id": f"{SITE}/for-churches.html#webpage",
         "url": f"{SITE}/for-churches.html",
         "name": "Video and AI for churches",
         "isPartOf": {"@id": f"{SITE}/#website"}, "dateModified": TODAY,
         "inLanguage": "en-US",
         "about": {"@id": f"{SITE}/#organization"},
         "primaryImageOfPage": f"{SITE}/assets/img/og-church.png",
         "description": "Narrated Bible films, teaching series and AI training produced for churches and ministries by The AI Disciple in Fresno, California."},
        {"@type": "Service", "@id": f"{SITE}/for-churches.html#service",
         "name": "Church and ministry video production",
         "serviceType": "Church video production and AI training",
         "url": f"{SITE}/for-churches.html",
         "provider": {"@id": f"{SITE}/#organization"},
         "audience": {"@type": "Audience", "audienceType": "Churches, ministries and Christian nonprofits"},
         "areaServed": [{"@type": "City", "name": "Fresno"},
                        {"@type": "Country", "name": "United States"}],
         "availableLanguage": ["English", "Urdu", "Swahili"],
         "description": (
             "Narrated Scripture films in which a witness figure tells a Bible event while visuals carry "
             "the scene, produced as a sermon visual aid for pastors. Also multi-week teaching series, "
             "children's Bible cartoons, background and archaeology explainers, testimony and appeal films, "
             "and multilingual versions. Free AI training and free children's Bible material are provided to "
             "churches at no charge.")},
        {"@type": "ItemList", "@id": f"{SITE}/for-churches.html#films",
         "name": "Bible films produced for church use",
         "numberOfItems": len(FILMS), "itemListElement": film_items},
        faq_schema(church_faqs, f"{SITE}/for-churches.html"),
        {**breadcrumbs([("/", "Home"), ("/for-churches.html", "For Churches")]),
         "@id": f"{SITE}/for-churches.html#breadcrumb"},
    ],
    og_title="Narrated Bible films and AI help for churches",
    og_image=f"{SITE}/assets/img/og-church.png",
)

# ---------------------------------------------------------------- FREE TRAINING
training_faqs = [f for f in FAQS if f[0] in (
    "Is the free AI training really free?",
    "How do I get the free AI training videos?",
    "Do I need to be technical to work with you?",
)]

MODULES = [
    ("What AI actually is", "What a language model is really doing when it answers you, and why understanding that one thing changes how you use it."),
    ("Your first hour", "Opening a chat tool for the first time, which free tool to start with, and the first three things worth trying with your own work."),
    ("Asking so you get something usable", "The difference between a question that produces vague filler and one that produces a draft you would actually send."),
    ("Catching a confident mistake", "Why AI invents facts, what a hallucination looks like in professional language, and a simple habit for checking an answer."),
    ("What never to type into it", "Customer records, medical details, passwords, employee information, anything shared in confidence &mdash; and where your typing actually goes."),
    ("Your first real habit", "Turning one repetitive task in your own week into something you do with AI every time."),
]

course_schema = {
    "@type": "Course",
    "@id": f"{SITE}/free-training.html#course",
    "name": "AI Basics for Total Beginners",
    "url": f"{SITE}/free-training.html",
    "description": (
        "A free six-lesson video course in artificial intelligence for complete beginners, covering what AI "
        "is, how to get a usable answer from it, how to recognize a confident mistake, what must never be "
        "entered into a chat window, and how to build a first working habit. Requested through the contact "
        "form; Aaron Tenney emails a private link personally."),
    "inLanguage": "en-US",
    "isAccessibleForFree": True,
    "educationalLevel": "Beginner",
    "teaches": [m[0] for m in MODULES],
    "provider": {"@id": f"{SITE}/#organization"},
    "author": {"@id": f"{SITE}/#aaron"},
    "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD",
               "availability": "https://schema.org/InStock",
               "category": "Free", "url": f"{SITE}/contact.html?interest=training"},
    "hasCourseInstance": {
        "@type": "CourseInstance",
        "courseMode": "online",
        "courseWorkload": "PT2H",
        "inLanguage": "en-US",
        "instructor": {"@id": f"{SITE}/#aaron"},
    },
    "syllabusSections": [
        {"@type": "Syllabus", "position": i + 1, "name": n, "description": strip_tags(d)}
        for i, (n, d) in enumerate(MODULES)
    ],
}

build_page(
    "free-training.html",
    "Free AI Training for Beginners — Request the Videos | The AI Disciple",
    "A free AI course for total beginners, open to anyone. Six short lessons on what AI is, how to get a usable answer, how to catch a mistake and what never to type into it. Request it through the contact form and Aaron emails you a private link.",
    (FRAG / "free-training.html").read_text(encoding="utf-8"),
    [
        {"@type": "WebPage", "@id": f"{SITE}/free-training.html#webpage",
         "url": f"{SITE}/free-training.html",
         "name": "Free AI training for beginners",
         "isPartOf": {"@id": f"{SITE}/#website"}, "dateModified": TODAY,
         "inLanguage": "en-US",
         "primaryImageOfPage": f"{SITE}/assets/img/og-training.png",
         "description": "A free beginner AI video course from The AI Disciple, requested through the contact form and sent as a private link."},
        course_schema,
        faq_schema(training_faqs, f"{SITE}/free-training.html"),
        {**breadcrumbs([("/", "Home"), ("/free-training.html", "Free Training")]),
         "@id": f"{SITE}/free-training.html#breadcrumb"},
    ],
    og_title="Free AI training for total beginners",
    og_image=f"{SITE}/assets/img/og-training.png",
)

# ---------------------------------------------------------------- 404
build_page(
    "404.html", "Page not found | The AI Disciple",
    "That page does not exist. Head back to the homepage or book a free 20-minute AI consultation.",
    """<section class="page-hero"><div class="container container--narrow" style="text-align:center">
      <p class="eyebrow eyebrow--center">Error 404</p>
      <h1>That page isn't here</h1>
      <p class="lede">The link may be old, or the page may have moved. Everything below still works.</p>
      <div class="btn-row" style="justify-content:center;margin-top:var(--space-8)">
        <a class="btn btn--primary btn--lg" href="/">Back to the homepage</a>
        <a class="btn btn--outline btn--lg" href="/contact.html">Book a free call</a>
      </div></div></section>""",
    [], og_title="Page not found",
    extra_head='<meta name="robots" content="noindex, follow">',
)

# ---------------------------------------------------------------- robots / sitemap
PAGES = [
    ("/", "1.0", "weekly"),
    ("/services.html", "0.9", "monthly"),
    ("/for-churches.html", "0.9", "monthly"),
    ("/free-training.html", "0.9", "monthly"),
    ("/contact.html", "0.9", "monthly"),
    ("/about.html", "0.8", "monthly"),
    ("/faq.html", "0.8", "monthly"),
    ("/videos.html", "0.8", "weekly"),
    ("/bible-stories.html", "0.7", "weekly"),
    ("/download.html", "0.6", "monthly"),
]

urls = "\n".join(
    f"  <url>\n    <loc>{SITE}{p}</loc>\n    <lastmod>{TODAY}</lastmod>\n"
    f"    <changefreq>{cf}</changefreq>\n    <priority>{pr}</priority>\n  </url>"
    for p, pr, cf in PAGES
)
(ROOT / "sitemap.xml").write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "\n</urlset>\n",
    encoding="utf-8")

(ROOT / "robots.txt").write_text(f"""# robots.txt for theaidisciple.com
User-agent: *
Allow: /

# AI answer engines and research crawlers are explicitly welcome.
User-agent: GPTBot
Allow: /
User-agent: OAI-SearchBot
Allow: /
User-agent: ChatGPT-User
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: Perplexity-User
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: Claude-User
Allow: /
User-agent: anthropic-ai
Allow: /
User-agent: Google-Extended
Allow: /
User-agent: Applebot-Extended
Allow: /
User-agent: Bingbot
Allow: /
User-agent: cohere-ai
Allow: /
User-agent: Amazonbot
Allow: /
User-agent: meta-externalagent
Allow: /

Sitemap: {SITE}/sitemap.xml
""", encoding="utf-8")

print(f"  built sitemap.xml            ({len(PAGES)} urls)")
print("  built robots.txt")
print(f"\nDone — {len(STORIES)} stories, {len(FAQS)} FAQs.")
