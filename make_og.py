#!/usr/bin/env python3
"""Regenerate Open Graph cards (1200x630) in the site's ink + cobalt style.

Uses the real brand fonts (Zodiak display, Satoshi body) and the AD seal mark,
so the cards match the site instead of approximating it.
"""
from PIL import Image, ImageDraw, ImageFont
import pathlib, json, io

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "assets" / "img"
# Prefer a fonts/ folder beside this script; fall back to the build sandbox.
FONTS = next((p for p in (ROOT / "fonts", pathlib.Path("/home/user/workspace/fonts"))
              if p.is_dir()), ROOT / "fonts")

W, H = 1200, 630
INK = (16, 20, 28)
COBALT = (95, 154, 224)        # --color-on-ink-accent
CREAM = (250, 247, 241)
MUTED = (154, 161, 174)        # --color-on-ink-muted

DISPLAY = str(FONTS / "Zodiak-700.ttf")
SANS = str(FONTS / "Satoshi-400.ttf")
SANS_M = str(FONTS / "Satoshi-500.ttf")
SANS_B = str(FONTS / "Satoshi-700.ttf")


def brand_mark(px):
    """Render the AD seal at px, transparent behind the badge.

    Geometry comes from make_logo so the cards can never drift from the
    favicon and the header mark. Cards sit on ink, so use the dark-theme
    pairing: cobalt badge, ink letters."""
    import cairosvg
    import make_logo
    svg = make_logo.doc(make_logo.mark(make_logo.ACCENT_DARK, make_logo.KNOCK_DARK))
    buf = io.BytesIO()
    cairosvg.svg2png(bytestring=svg.encode(), write_to=buf,
                     output_width=px, output_height=px, background_color=None)
    buf.seek(0)
    return Image.open(buf).convert("RGBA")


def gradient():
    """Cobalt-tinted glow from the top-left, on ink."""
    g = Image.new("RGB", (W, H), INK)
    px = g.load()
    for y in range(H):
        fy = (y / H) ** 0.9
        for x in range(0, W, 2):
            t = max(0.0, 1 - ((x / W) ** 0.9 + fy) / 1.35)
            c = (int(INK[0] + 14 * t), int(INK[1] + 30 * t), int(INK[2] + 58 * t))
            px[x, y] = c
            if x + 1 < W:
                px[x + 1, y] = c
    return g


def wrap(draw, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


BASE = gradient()
MARK_IMG = brand_mark(122)


def card(name, eyebrow, title, sub):
    img = BASE.copy()
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 6], fill=COBALT)

    f_eye = ImageFont.truetype(SANS_B, 24)
    f_sub = ImageFont.truetype(SANS, 30)
    f_name = ImageFont.truetype(SANS_B, 28)
    f_meta = ImageFont.truetype(SANS, 22)

    x = 80
    img.paste(MARK_IMG, (W - 80 - MARK_IMG.width, 76), MARK_IMG)

    d.text((x, 92), eyebrow.upper(), font=f_eye, fill=COBALT)

    # shrink the headline until it fits two lines in the space available
    maxw = W - x - 260
    for size, lead in ((66, 82), (60, 75), (54, 68)):
        f_title = ImageFont.truetype(DISPLAY, size)
        lines = wrap(d, title, f_title, maxw)
        if len(lines) <= 2:
            break
    y = 152
    for line in lines:
        d.text((x, y), line, font=f_title, fill=CREAM)
        y += lead

    y += 14
    for line in wrap(d, sub, f_sub, W - 2 * x - 120)[:2]:
        d.text((x, y), line, font=f_sub, fill=MUTED)
        y += 42

    d.rectangle([x, 512, x + 4, 582], fill=COBALT)
    d.text((x + 20, 520), "The AI Disciple", font=f_name, fill=CREAM)
    d.text((x + 20, 557), "Aaron Tenney  \u00b7  Fresno, California", font=f_meta, fill=MUTED)
    dom = "theaidisciple.com"
    d.text((W - 80 - d.textlength(dom, font=f_meta), 557), dom, font=f_meta, fill=COBALT)

    img.save(OUT / name, optimize=True)
    print("  wrote", name)


CARDS = json.loads((ROOT / "og_cards.json").read_text())
for name, c in CARDS.items():
    card(name, c["eyebrow"], c["title"], c["sub"])
