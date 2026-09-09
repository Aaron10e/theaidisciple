#!/usr/bin/env python3
"""Generate every AD monogram asset from one source of geometry.

Run after changing the mark:  python make_logo.py

Writes:
  favicon.svg                    vector tab icon (fixed light colours)
  favicon.ico                    16 + 32 + 48 px raster fallback
  assets/img/apple-touch-icon.png  180px, full bleed (iOS applies its own mask)
  assets/img/logo.png            512px, rounded, transparent corners (schema.org)
  assets/img/logo-dark.png       512px dark-theme variant
  assets/img/avatar.png          800px circular, for YouTube and social profiles

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

# ---------------------------------------------------------------- geometry
# A: apex (29,27), feet (12,75) and (46,75), crossbar at 68% down the legs.
# D: stem at x=59, bowl on two cubic curves so it springs out of the stem
#    rather than meeting a flat horizontal -- a true semicircle reads rigid.
#    Top and bottom overshoot the A by 0.7 so the round form looks optically
#    the same height as the pointed one.
A_PATH = "M12,75 L29,27 L46,75 M17.4,59.6 L40.6,59.6"
D_STEM = "M59,26.3 L59,75.7"
D_BOWL = "M59,26.3 C77,26.3 86,36 86,51 C86,66 77,75.7 59,75.7"
STROKE = 8.5
RADIUS = 26


def letters(knock):
    return (f'<g fill="none" stroke="{knock}" stroke-width="{STROKE}"'
            f' stroke-linecap="round" stroke-linejoin="round">'
            f'<path d="{A_PATH}"/><path d="{D_STEM}"/><path d="{D_BOWL}"/></g>')


def mark(accent, knock, radius=RADIUS, shape="squircle"):
    if shape == "circle":
        bg = f'<circle cx="50" cy="50" r="50" fill="{accent}"/>'
    elif shape == "square":
        bg = f'<rect width="100" height="100" fill="{accent}"/>'
    else:
        bg = f'<rect width="100" height="100" rx="{radius}" ry="{radius}" fill="{accent}"/>'
    return bg + letters(knock)


def doc(inner, size=None, title="The AI Disciple"):
    dim = f' width="{size}" height="{size}"' if size else ""
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"'
            f'{dim} role="img"><title>{title}</title>{inner}</svg>')


def png(svg_text, px):
    return cairosvg.svg2png(bytestring=svg_text.encode("utf-8"),
                            output_width=px, output_height=px)


# --------------------------------------------------------- inline header mark
# Uses CSS variables so it follows the theme. --logo-knock is a dedicated
# token rather than --color-bg because the footer sits on --color-surface-2,
# and knocking out to the wrong surface would tint the letters.
LOGO_INLINE = (
    '<svg class="brand__mark" viewBox="0 0 100 100" aria-hidden="true">'
    f'<rect width="100" height="100" rx="{RADIUS}" ry="{RADIUS}" fill="var(--color-accent)"/>'
    f'<g fill="none" stroke="var(--logo-knock)" stroke-width="{STROKE}"'
    ' stroke-linecap="round" stroke-linejoin="round">'
    f'<path d="{A_PATH}"/><path d="{D_STEM}"/><path d="{D_BOWL}"/></g></svg>'
)


def main():
    img = ROOT / "assets" / "img"
    img.mkdir(parents=True, exist_ok=True)

    light = mark(ACCENT_LIGHT, KNOCK_LIGHT)
    dark = mark(ACCENT_DARK, KNOCK_DARK)

    (ROOT / "favicon.svg").write_text(doc(light, 100), encoding="utf-8")
    print("  favicon.svg")

    # .ico -- browsers pick the size they need
    frames = [Image.open(io.BytesIO(png(doc(light), s))).convert("RGBA")
              for s in (48, 32, 16)]
    frames[0].save(ROOT / "favicon.ico", format="ICO",
                   sizes=[(48, 48), (32, 32), (16, 16)])
    print("  favicon.ico            48/32/16")

    # iOS masks the corners itself, so ship it full bleed
    (img / "apple-touch-icon.png").write_bytes(
        png(doc(mark(ACCENT_LIGHT, KNOCK_LIGHT, shape="square")), 180))
    print("  apple-touch-icon.png   180")

    (img / "logo.png").write_bytes(png(doc(light), 512))
    print("  logo.png               512")
    (img / "logo-dark.png").write_bytes(png(doc(dark), 512))
    print("  logo-dark.png          512")

    # Social profiles crop to a circle, so give them a circular master
    (img / "avatar.png").write_bytes(
        png(doc(mark(ACCENT_LIGHT, KNOCK_LIGHT, shape="circle")), 800))
    print("  avatar.png             800 circular")

    print("\nInline header mark for build.py LOGO:\n")
    print(LOGO_INLINE)


if __name__ == "__main__":
    main()
