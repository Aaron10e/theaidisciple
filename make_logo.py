#!/usr/bin/env python3
"""Generate every AD monogram asset from one source of geometry.

Run after changing the mark:  python make_logo.py

Writes:
  favicon.svg                      vector tab icon (fixed light colours)
  favicon.ico                      16 + 32 + 48 px raster fallback
  assets/img/apple-touch-icon.png  180px, full bleed (iOS applies its own mask)
  assets/img/logo.png              512px (schema.org)
  assets/img/logo-dark.png         512px dark-theme variant
  assets/img/avatar.png            800px circular, for YouTube and social

The inline header mark lives in build.py's LOGO constant and is printed by
this script so the two can be kept in sync.

Pure geometry, no fonts -- portable to any machine with cairosvg + Pillow.
"""
import io
import pathlib

import cairosvg
from PIL import Image

ROOT = pathlib.Path(__file__).parent

ACCENT_LIGHT = "#0b4f9e"
ACCENT_DARK = "#5f9ae0"
KNOCK_LIGHT = "#faf7f1"
KNOCK_DARK = "#0e1218"

# The screen is always a near-black panel with the letters reversed out white,
# in both themes. Only the monitor frame follows the accent colour.
SCREEN = "#0b0e14"
GLYPH = "#ffffff"

# ---------------------------------------------------------------- geometry
# The letters. A: apex (29,27), feet (12,75) and (46,75), crossbar 68% down.
# D: stem at x=59, bowl on two cubic curves so it springs out of the stem
#    rather than meeting a flat horizontal -- a true semicircle reads rigid.
#    Top and bottom overshoot the A by 0.7 so the round form looks optically
#    the same height as the pointed one.
A_PATH = "M12,75 L29,27 L46,75 M17.4,59.6 L40.6,59.6"
D_STEM = "M59,26.3 L59,75.7"
D_BOWL = "M59,26.3 C77,26.3 86,36 86,51 C86,66 77,75.7 59,75.7"
STROKE = 8.5

# The monitor. A 92x58 panel is 1.59:1 -- close enough to 16:10 to read as a
# display without looking like a letterbox. The stand is a stem and a foot,
# nothing more; anything with a neck taper or a hinge turns to mush by 24px.
SCR = (4.0, 15.0, 96.0, 73.0)      # x0, y0, x1, y1
SCR_R = 6.0                        # corner radius
BEZEL = 4.0                        # frame stroke weight
INSET = 6.0                        # padding from frame to letters
STEM_TO = 81.5
FOOT_Y = 84.5
FOOT_X = (33.0, 67.0)

# Visual bounds of the letter artwork, stroke included.
_BB = (12 - STROKE / 2, 26.3 - STROKE / 2, 86 + STROKE / 2, 75.7 + STROKE / 2)


def letters(colour=GLYPH, box=None):
    """The AD, scaled and centred into `box` (defaults to the screen area)."""
    if box is None:
        box = (SCR[0] + INSET, SCR[1] + INSET, SCR[2] - INSET, SCR[3] - INSET)
    x0, y0, x1, y1 = box
    bw, bh = _BB[2] - _BB[0], _BB[3] - _BB[1]
    s = min((x1 - x0) / bw, (y1 - y0) / bh)
    tx = x0 + ((x1 - x0) - bw * s) / 2 - _BB[0] * s
    ty = y0 + ((y1 - y0) - bh * s) / 2 - _BB[1] * s
    return (f'<g transform="translate({tx:.2f},{ty:.2f}) scale({s:.4f})"'
            f' fill="none" stroke="{colour}" stroke-width="{STROKE}"'
            f' stroke-linecap="round" stroke-linejoin="round">'
            f'<path d="{A_PATH}"/><path d="{D_STEM}"/>'
            f'<path d="{D_BOWL}"/></g>')


def mark(accent, stand=True, glyph=GLYPH, screen=SCREEN):
    """Monitor outline with the letters on the screen. Transparent behind."""
    x0, y0, x1, y1 = SCR
    parts = []
    if stand:
        parts.append(f'<path d="M50,{y1} L50,{STEM_TO}" stroke="{accent}"'
                     f' stroke-width="{BEZEL}"/>')
        parts.append(f'<path d="M{FOOT_X[0]},{FOOT_Y} L{FOOT_X[1]},{FOOT_Y}"'
                     f' stroke="{accent}" stroke-width="{BEZEL}"'
                     f' stroke-linecap="round"/>')
    parts.append(f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}"'
                 f' rx="{SCR_R}" ry="{SCR_R}" fill="{screen}"'
                 f' stroke="{accent}" stroke-width="{BEZEL}"/>')
    parts.append(letters(glyph))
    return "".join(parts)


def tile(accent, shape="square", pad=0.80, bg=SCREEN):
    """The mark shrunk onto a filled backdrop, for app icons and avatars."""
    if shape == "circle":
        back = f'<circle cx="50" cy="50" r="50" fill="{bg}"/>'
    else:
        back = f'<rect width="100" height="100" fill="{bg}"/>'
    off = 50 * (1 - pad)
    return (back + f'<g transform="translate({off:.2f},{off:.2f})'
            f' scale({pad})">{mark(accent)}</g>')


def doc(inner, size=None, title="The AI Disciple"):
    dim = f' width="{size}" height="{size}"' if size else ""
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"'
            f'{dim} role="img"><title>{title}</title>{inner}</svg>')


def png(svg_text, px):
    return cairosvg.svg2png(bytestring=svg_text.encode("utf-8"),
                            output_width=px, output_height=px)


# --------------------------------------------------------- inline header mark
# The frame follows --color-accent so it inverts with the theme. The screen and
# the letters are deliberately fixed: the panel is black and the letters white
# in both themes, which is the whole point of the mark.
LOGO_INLINE = (
    '<svg class="brand__mark" viewBox="0 0 100 100" aria-hidden="true">'
    + mark("var(--color-accent)").replace(
        f'stroke="{ACCENT_LIGHT}"', 'stroke="var(--color-accent)"')
    + '</svg>'
)


def main():
    img = ROOT / "assets" / "img"
    img.mkdir(parents=True, exist_ok=True)

    light = mark(ACCENT_LIGHT)
    dark = mark(ACCENT_DARK)

    (ROOT / "favicon.svg").write_text(doc(light, 100), encoding="utf-8")
    print("  favicon.svg")

    # .ico -- browsers pick the size they need. The 16px frame drops the stand:
    # at that size it is two grey pixels that only blur the panel edge.
    frames = []
    for s in (48, 32, 16):
        art = mark(ACCENT_LIGHT, stand=(s > 16))
        frames.append(Image.open(io.BytesIO(png(doc(art), s))).convert("RGBA"))
    frames[0].save(ROOT / "favicon.ico", format="ICO",
                   sizes=[(48, 48), (32, 32), (16, 16)])
    print("  favicon.ico            48/32/16 (16 drops the stand)")

    # iOS masks the corners itself, so ship it full bleed on the panel black
    (img / "apple-touch-icon.png").write_bytes(
        png(doc(tile(ACCENT_DARK, "square", 0.78)), 180))
    print("  apple-touch-icon.png   180")

    (img / "logo.png").write_bytes(png(doc(light), 512))
    print("  logo.png               512")
    (img / "logo-dark.png").write_bytes(png(doc(dark), 512))
    print("  logo-dark.png          512")

    # Social profiles crop to a circle, so give them a circular master
    (img / "avatar.png").write_bytes(
        png(doc(tile(ACCENT_DARK, "circle", 0.72)), 800))
    print("  avatar.png             800 circular")

    print("\nInline header mark for build.py LOGO:\n")
    print(LOGO_INLINE)


if __name__ == "__main__":
    main()
