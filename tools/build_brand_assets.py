#!/usr/bin/env python3
"""Generate the branding assets for Stadium Gate Monitor.

Part of one identity system shared across Abdulelah Alkhathami's public
repositories: flat geometry inflated by a lighting filter into frosted
translucent solids, a cyan-aqua-lime-blue gradient family, a single key light
from the upper left, soft contact shadows and a fine analog grain.

The canonical rules live in
https://github.com/Abdulel3h/Abdulel3h/blob/main/docs/github-brand-system.md

Dependency-free and deterministic: two runs produce byte-identical files.
Never hand-edit the generated SVGs; edit this file and regenerate with:

    python3 tools/build_brand_assets.py
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

BLACK = "#030706"
SURFACE = "#06100E"
BORDER = "#123029"
WHITE = "#F4FFF9"
MUTED = "#8FA8A1"
DIM = "#5E7A74"
CYAN = "#46F6FF"
AQUA = "#22E3C5"
LIME = "#C8FF54"
BLUE = "#3B65FF"

SANS = 'ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
MONO = 'ui-monospace, SFMono-Regular, "SF Mono", "Cascadia Mono", "Segoe UI Mono", Consolas, monospace'

# Key light: upper left, cinematic.
AZIMUTH = 228
ELEVATION = 58


# --------------------------------------------------------------------------
# Material system
# --------------------------------------------------------------------------

def _gloss(name: str, bump: float, exponent: int, constant: float, rim: float) -> str:
    """A lighting filter that inflates flat geometry into a glossy translucent solid.

    The blurred alpha channel acts as a height field, so any silhouette gains a
    soft bevel, diffuse shading, a cyan rim on the shadow side and a controlled
    specular highlight.
    """
    return f"""
    <filter id="{name}" x="-35%" y="-35%" width="170%" height="170%" color-interpolation-filters="sRGB">
      <feGaussianBlur in="SourceAlpha" stdDeviation="{bump}" result="bump"/>
      <feDiffuseLighting in="bump" surfaceScale="{bump * .5:.2f}" diffuseConstant="1.15" lighting-color="#CFEFFF" result="dif">
        <feDistantLight azimuth="{AZIMUTH}" elevation="{ELEVATION - 10}"/>
      </feDiffuseLighting>
      <feComposite in="dif" in2="SourceAlpha" operator="in" result="difc"/>
      <feBlend in="SourceGraphic" in2="difc" mode="multiply" result="mul"/>
      <feComposite in="mul" in2="SourceGraphic" operator="arithmetic" k2=".72" k3=".38" result="shaded"/>
      <feOffset in="SourceAlpha" dx="{rim:.1f}" dy="{rim * 1.1:.1f}" result="ro"/>
      <feComposite in="SourceAlpha" in2="ro" operator="out" result="rmask"/>
      <feGaussianBlur in="rmask" stdDeviation="{rim * .55:.2f}" result="rsoft"/>
      <feFlood flood-color="{CYAN}" flood-opacity=".9" result="rcol"/>
      <feComposite in="rcol" in2="rsoft" operator="in" result="rim0"/>
      <feComposite in="rim0" in2="SourceAlpha" operator="in" result="rim"/>
      <feComposite in="rim" in2="shaded" operator="arithmetic" k2=".72" k3="1" result="base"/>
      <feSpecularLighting in="bump" surfaceScale="{bump * .75:.2f}" specularConstant="{constant}" specularExponent="{exponent}" lighting-color="#EAFEFF" result="spec">
        <feDistantLight azimuth="{AZIMUTH}" elevation="{ELEVATION}"/>
      </feSpecularLighting>
      <feComposite in="spec" in2="SourceAlpha" operator="in" result="specc"/>
      <feComposite in="specc" in2="base" operator="arithmetic" k2="1" k3="1"/>
    </filter>"""


def defs() -> str:
    """Gradients, filters and clip geometry shared by every asset."""
    return f"""  <defs>
    <linearGradient id="glass" x1="0" y1="0" x2=".85" y2="1">
      <stop stop-color="{CYAN}"/><stop offset=".40" stop-color="{AQUA}"/>
      <stop offset=".76" stop-color="{LIME}"/><stop offset="1" stop-color="{BLUE}"/>
    </linearGradient>
    <linearGradient id="glassBack" x1="1" y1="0" x2="0" y2="1">
      <stop stop-color="{AQUA}"/><stop offset=".55" stop-color="{BLUE}"/>
      <stop offset="1" stop-color="#1B3E8F"/>
    </linearGradient>
    <linearGradient id="glassLime" x1="0" y1="1" x2="1" y2="0">
      <stop stop-color="{AQUA}"/><stop offset=".55" stop-color="{LIME}"/>
      <stop offset="1" stop-color="#EFFFC9"/>
    </linearGradient>
    <linearGradient id="glassCold" x1="0" y1="0" x2=".6" y2="1">
      <stop stop-color="#E8FBFF"/><stop offset=".45" stop-color="{CYAN}" stop-opacity=".92"/>
      <stop offset="1" stop-color="{BLUE}"/>
    </linearGradient>
    <linearGradient id="inkFade" x1="0" y1="0" x2="1" y2="0">
      <stop stop-color="{WHITE}"/><stop offset=".62" stop-color="{AQUA}"/><stop offset="1" stop-color="{CYAN}"/>
    </linearGradient>
    <linearGradient id="hair" x1="0" y1="0" x2="1" y2="0">
      <stop stop-color="{AQUA}" stop-opacity=".55"/><stop offset="1" stop-color="{AQUA}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="ribbon" x1="0" y1="0" x2="1" y2="0">
      <stop stop-color="{AQUA}" stop-opacity="0"/><stop offset=".3" stop-color="{AQUA}" stop-opacity=".8"/>
      <stop offset=".7" stop-color="{LIME}"/><stop offset="1" stop-color="{CYAN}"/>
    </linearGradient>
    <radialGradient id="core" cx="36%" cy="30%" r="70%">
      <stop stop-color="#FFFFFF"/><stop offset=".18" stop-color="{CYAN}"/>
      <stop offset=".58" stop-color="{AQUA}"/><stop offset="1" stop-color="{BLUE}" stop-opacity=".9"/>
    </radialGradient>
    <radialGradient id="coreLime" cx="36%" cy="30%" r="70%">
      <stop stop-color="#FFFFFF"/><stop offset=".2" stop-color="{LIME}"/>
      <stop offset=".62" stop-color="{AQUA}"/><stop offset="1" stop-color="#17705F"/>
    </radialGradient>
    <radialGradient id="haze">
      <stop stop-color="{AQUA}" stop-opacity=".26"/><stop offset=".55" stop-color="{AQUA}" stop-opacity=".08"/>
      <stop offset="1" stop-color="{AQUA}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="hazeLime">
      <stop stop-color="{LIME}" stop-opacity=".30"/><stop offset="1" stop-color="{LIME}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="vignette" cx="50%" cy="42%" r="78%">
      <stop stop-color="{SURFACE}"/><stop offset=".55" stop-color="#040B09"/><stop offset="1" stop-color="{BLACK}"/>
    </radialGradient>
    <radialGradient id="pool" cx="50%" cy="50%" r="50%">
      <stop stop-color="#0E4B43" stop-opacity=".85"/><stop offset="1" stop-color="#0E4B43" stop-opacity="0"/>
    </radialGradient>
{_gloss('glossL', 15, 26, .82, 7)}
{_gloss('glossM', 10, 34, .90, 5)}
{_gloss('glossS', 6, 44, 1.00, 3)}
    <filter id="shade" x="-70%" y="-140%" width="240%" height="380%"><feGaussianBlur stdDeviation="20"/></filter>
    <filter id="bloom" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="16"/></filter>
    <filter id="bloomS" x="-90%" y="-90%" width="280%" height="280%"><feGaussianBlur stdDeviation="6"/></filter>
    <filter id="frost" x="-15%" y="-40%" width="130%" height="180%" color-interpolation-filters="sRGB">
      <feGaussianBlur stdDeviation="1.4"/>
    </filter>
    <filter id="grain" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB">
      <feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="3" seed="17" result="n"/>
      <feColorMatrix in="n" type="saturate" values="0"/>
      <feComponentTransfer><feFuncA type="table" tableValues="0 .11"/></feComponentTransfer>
    </filter>
  </defs>"""


# --------------------------------------------------------------------------
# Motion
#
# Every animation is CSS. SMIL would keep running - and keep the browser
# repainting - even for readers who asked for reduced motion, because no media
# query can switch it off.
#
# An SVG loaded through <img> is re-rasterised whole on every animation frame,
# filters included, so a smooth 60fps loop costs about a core per card. Stepped
# timing fixes the update rate instead: the two system pieces run a slow loop at
# a few updates a second, and the cards animate once, when they are first
# painted, then rest at zero cost.
# --------------------------------------------------------------------------

# One loop length and one step grid per asset. Sharing the grid matters: a
# repaint costs the same whether one element moved or five, so every animation
# in a file has to land on the same frames. Five animations stepping on five
# different phases would cost five times as much as one.
LOOP_DUR = 12.0    # the looping hero and flow
LOOP_GRID = 60     # 5 updates a second
CARD_DUR = 5.4     # one activation, played when a card is first painted
CARD_GRID = 40     # ~7.4 updates a second


def keyframes(name: str, grid: int, stops: list[tuple[float, str]]) -> str:
    """A keyframe rule pinned to the asset's step grid.

    `stops` are (fraction of the loop, declarations). Fractions snap to the
    grid, and an interval where nothing changes collapses to a single step, so
    a held pose costs no repaints at all.
    """
    snapped = [(max(0, min(grid, round(fraction * grid))), declaration)
               for fraction, declaration in stops]
    rules = []
    for index, (step, declaration) in enumerate(snapped):
        percent = step / grid * 100
        if index + 1 < len(snapped):
            span = max(1, snapped[index + 1][0] - step)
            count = 1 if snapped[index + 1][1] == declaration else span
            rules.append(f"{percent:.4g}% {{ {declaration}; animation-timing-function: steps({count}); }}")
        else:
            rules.append(f"{percent:.4g}% {{ {declaration}; }}")
    return f"    @keyframes {name} {{ {' '.join(rules)} }}\n"


def on_grid(seconds: float, duration: float, grid: int) -> float:
    """Snap a delay to the step grid so a delayed animation shares the frames."""
    step = duration / grid
    return round(seconds / step) * step


def rule(selector: str, declarations: str) -> str:
    return f"    {selector} {{ {declarations}; }}\n"


def travelling(css_class: str, path: str, name: str, duration: float,
               repeat: str = "infinite", delay: float = 0) -> str:
    """Bind a particle to a path. `offset-distance` is what the keyframes move."""
    hold = f" animation-delay: {delay:g}s;" if delay else ""
    return (f'    .{css_class} {{ offset-path: path("{path}"); offset-rotate: 0deg; '
            f'offset-distance: 0%; opacity: 0; animation: {name} {duration:g}s {repeat};{hold} }}\n')


def style(extra: str = "") -> str:
    return f"""  <style>
    .s {{ font-family: {SANS}; }}
    .m {{ font-family: {MONO}; }}
    .eyebrow {{ letter-spacing: .22em; }}
    .track {{ letter-spacing: .12em; }}
    .still {{ display: none; }}
    .mv {{ transform-box: fill-box; transform-origin: 50% 50%; }}
{extra}    @media (prefers-reduced-motion: reduce) {{
      * {{ animation: none !important; }}
      .motion {{ display: none !important; }}
      .still {{ display: inline !important; }}
    }}
  </style>"""


# --------------------------------------------------------------------------
# Primitives
# --------------------------------------------------------------------------

def tube(d: str, width: float, gradient: str = "glass", gloss: str = "glossL",
         opacity: float = .86, sheen: bool = True, cls: str = "") -> str:
    """A chunky translucent tube along a path."""
    inner = ""
    if sheen:
        inner = (f'<path d="{d}" fill="none" stroke="#F2FFFC" stroke-width="{width * .26:.1f}" '
                 f'stroke-linecap="round" opacity=".14" transform="translate({-width * .09:.1f} {-width * .11:.1f})"/>')
    cls = f' class="{cls}"' if cls else ""
    return (f'<g{cls} filter="url(#{gloss})" opacity="{opacity:g}">'
            f'<path d="{d}" fill="none" stroke="url(#{gradient})" stroke-width="{width:g}" '
            f'stroke-linecap="round" stroke-linejoin="round"/>{inner}</g>')


def solid(d: str, gradient: str = "glass", gloss: str = "glossL",
          opacity: float = .88, cls: str = "") -> str:
    """A chunky translucent filled form."""
    cls = f' class="{cls}"' if cls else ""
    return (f'<g{cls} filter="url(#{gloss})" opacity="{opacity:g}">'
            f'<path d="{d}" fill="url(#{gradient})"/></g>')


def sphere(cx: float, cy: float, r: float, gradient: str = "core",
           gloss: str = "glossM", opacity: float = 1.0, cls: str = "") -> str:
    cls = f' class="{cls}"' if cls else ""
    return (f'<g{cls} filter="url(#{gloss})" opacity="{opacity:g}">'
            f'<circle cx="{cx:g}" cy="{cy:g}" r="{r:g}" fill="url(#{gradient})"/></g>')


def contact_shadow(cx: float, cy: float, rx: float, ry: float, opacity: float = .9) -> str:
    """Light pool plus the occlusion that sits in it, so the form feels grounded."""
    return (f'<ellipse cx="{cx:g}" cy="{cy:g}" rx="{rx * 1.55:g}" ry="{ry * 2.1:g}" fill="url(#pool)" opacity=".5"/>'
            f'<ellipse cx="{cx:g}" cy="{cy:g}" rx="{rx:g}" ry="{ry:g}" fill="#010403" opacity="{opacity:g}" filter="url(#shade)"/>')


def text(x: float, y: float, value: str, size: float, fill: str = WHITE, weight: int = 400,
         cls: str = "s", anchor: str = "start", opacity: float | None = None,
         extra: str = "") -> str:
    op = f' opacity="{opacity:g}"' if opacity is not None else ""
    anc = f' text-anchor="{anchor}"' if anchor != "start" else ""
    wt = f' font-weight="{weight}"' if weight != 400 else ""
    return (f'<text class="{cls}" x="{x:g}" y="{y:g}" font-size="{size:g}" fill="{fill}"{wt}{anc}{op}{extra}>'
            f'{value}</text>')


def studio(width: int, height: int, label: str, index: str, radius: int = 30) -> str:
    """Black studio field, hairline frame and the editorial slug line."""
    border = "" if radius == 0 else (
        f'<rect x=".75" y=".75" width="{width - 1.5}" height="{height - 1.5}" rx="{radius - .75}" '
        f'fill="none" stroke="{BORDER}" stroke-width="1.5"/>')
    return f"""
  <rect width="{width}" height="{height}" rx="{radius}" fill="url(#vignette)"/>
  {border}
  {text(60, 50, label, 15, DIM, 500, cls="m eyebrow")}
  {text(width - 60, 50, index, 15, DIM, 500, cls="m eyebrow", anchor="end")}"""


def grain(width: int, height: int, radius: int = 30, opacity: float = .55) -> str:
    return (f'<rect width="{width}" height="{height}" rx="{radius}" filter="url(#grain)" '
            f'opacity="{opacity:g}" pointer-events="none"/>')


def write_svg(path: str, width: int, height: int, title: str, desc: str, body: str,
              css: str = "") -> None:
    destination = ROOT / path
    destination.parent.mkdir(parents=True, exist_ok=True)
    document = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="t d">
  <title id="t">{title}</title>
  <desc id="d">{desc}</desc>
{defs()}
{style(css)}
{body}
</svg>
"""
    # Optional parts leave blank indented lines behind; keep the output tidy.
    tidy = "\n".join(line.rstrip() for line in document.splitlines() if line.strip())
    destination.write_text(tidy + "\n", encoding="utf-8")


def slab(cx: float, cy: float, half_w: float, half_d: float, thickness: float,
         gradient: str, opacity: float = .82) -> str:
    """An axonometric chunky slab; the gloss filter bevels and inflates it."""
    outline = (f"M{cx:g} {cy - half_d:g}L{cx + half_w:g} {cy:g}L{cx + half_w:g} {cy + thickness:g}"
               f"L{cx:g} {cy + half_d + thickness:g}L{cx - half_w:g} {cy + thickness:g}"
               f"L{cx - half_w:g} {cy:g}Z")
    top = (f"M{cx:g} {cy - half_d:g}L{cx + half_w:g} {cy:g}L{cx:g} {cy + half_d:g}"
           f"L{cx - half_w:g} {cy:g}Z")
    right = (f"M{cx + half_w:g} {cy:g}L{cx + half_w:g} {cy + thickness:g}"
             f"L{cx:g} {cy + half_d + thickness:g}L{cx:g} {cy + half_d:g}Z")
    return (f'<g filter="url(#glossL)" opacity="{opacity:g}">'
            f'<path d="{outline}" fill="url(#{gradient})"/>'
            f'<path d="{top}" fill="#EAFFFB" opacity=".22"/>'
            f'<path d="{right}" fill="#02110E" opacity=".35"/></g>')

# --------------------------------------------------------------------------
# Project identity
# --------------------------------------------------------------------------

NAME = "Stadium Gate Monitor"
EYEBROW = "Computer vision · crowd flow"
LINE = "Four streams, one threshold."
DETAIL = "YOLO person detection · gate zones · crowding decision rules"
DETAIL_SHORT = "YOLO detection · gate zones · crowding rules"
STATUS = "Prototype"
STATUS_SHORT = "Prototype"
OWNER = "Abdulelah Alkhathami"
CHIPS = ["Person detection", "Gate zones", "Crowding rules"]
NAME_SIZE_COVER = 54
NAME_SIZE_SOCIAL = 62
DESC = (    "Stadium Gate Monitor — four translucent streams converge through one illuminated slot "
    "and leave as a single ordered flow.")


# --------------------------------------------------------------------------
# Sculpture
# --------------------------------------------------------------------------

FLOWS = [
    ("M-236-140C-130-134-86-70-12-16", 24, "glassBack", .62),
    ("M-236-58C-142-54-96-28-14-8", 26, "glass", .72),
    ("M-236 58C-142 54-96 28-14 8", 26, "glass", .7),
    ("M-236 140C-130 134-86 70-12 16", 24, "glassBack", .6),
]
OUTFLOW = "M14 -4C86 4 158-4 232 3"


def sculpture(cx: float, cy: float, scale: float = 1.0) -> str:
    """Four streams converge through one slot and leave as a single ordered flow."""
    inbound = "".join(tube(d, w, g, "glossS", o, sheen=False) for d, w, g, o in FLOWS)
    sparks = "".join(
        f'<g class="motion"><circle class="stream stream-{i}" r="6" fill="{CYAN}" filter="url(#bloomS)"/></g>'
        for i in range(len(FLOWS))
    )
    return f"""<g transform="translate({cx:g} {cy:g}) scale({scale:g})">
    <ellipse rx="280" ry="186" fill="url(#haze)" opacity=".62"/>
    {contact_shadow(0, 160, 168, 11, .8)}
    <g class="streams">{inbound}</g>
    {sparks}
    {tube(OUTFLOW, 40, "glassLime", "glossM", .85)}
    <g class="mv gate" filter="url(#glossL)" opacity=".95">
      <rect x="-26" y="-116" width="52" height="86" rx="20" fill="url(#glassCold)"/>
      <rect x="-26" y="30" width="52" height="86" rx="20" fill="url(#glassCold)"/>
    </g>
    <g class="gate-light">
      <path d="M0-30V30" stroke="{LIME}" stroke-width="15" stroke-linecap="round" filter="url(#bloomS)"/>
      <path d="M0-30V30" stroke="{LIME}" stroke-width="7" stroke-linecap="round"/>
      <path d="M0-30V30" stroke="#F4FFF9" stroke-width="3" stroke-linecap="round"/>
    </g>
  </g>"""

SCULPTURE_CSS = (
    "".join(
        travelling(f"stream-{i}", d, "streamIn", CARD_DUR, repeat="1 both",
                   delay=on_grid(i * .3, CARD_DUR, CARD_GRID))
        for i, (d, _w, _g, _o) in enumerate(FLOWS))
    + rule(".streams", f"animation: streamsWake {CARD_DUR:g}s 1 both")
    + rule(".gate-light", f"animation: gateWake {CARD_DUR:g}s 1 both")
    + keyframes("streamIn", CARD_GRID, [
        (0, "offset-distance: 0%; opacity: 0"),
        (.1, "offset-distance: 8%; opacity: 1"),
        (.6, "offset-distance: 100%; opacity: 1"),
        (.68, "offset-distance: 100%; opacity: 0"),
        (1, "offset-distance: 100%; opacity: 0")])
    + keyframes("streamsWake", CARD_GRID, [
        (0, "opacity: .55"), (.4, "opacity: 1"), (1, "opacity: 1")])
    + keyframes("gateWake", CARD_GRID, [
        (0, "opacity: .45"), (.5, "opacity: .45"), (.64, "opacity: 1"), (1, "opacity: 1")])
)


# --------------------------------------------------------------------------
# Assets
# --------------------------------------------------------------------------

def build_hero() -> None:
    """Wide README hero, 1200 x 360."""
    width, height = 1200, 360
    body = f"""{studio(width, height, EYEBROW, STATUS)}
  {sculpture(912, 192, .80)}
  {text(60, 146, NAME, 54, WHITE, 700, extra=' letter-spacing="-1.4"')}
  {text(60, 200, LINE, 27, "url(#inkFade)", 600)}
  {text(60, 254, DETAIL, 17, MUTED)}
  <path d="M62 292H430" stroke="url(#hair)" stroke-width="1.5"/>
  {text(60, 322, "abdulelah.de", 15, AQUA, 600, cls="m track")}
  {grain(width, height)}"""
    write_svg("assets/branding/hero.svg", width, height, f"{NAME} — {LINE}", DESC, body,
              css=SCULPTURE_CSS)


def build_hero_mobile() -> None:
    """Portrait README hero for viewports at or below 600px, 760 x 620."""
    width, height = 760, 620
    body = f"""{studio(width, height, EYEBROW, STATUS_SHORT, radius=26)}
  {sculpture(380, 236, .78)}
  {text(56, 444, NAME, 56, WHITE, 700, extra=' letter-spacing="-1.4"')}
  {text(56, 500, LINE, 31, "url(#inkFade)", 600)}
  {text(56, 552, DETAIL_SHORT, 22, MUTED)}
  {grain(width, height, radius=26)}"""
    write_svg("assets/branding/hero-mobile.svg", width, height, f"{NAME} — {LINE}", DESC, body,
              css=SCULPTURE_CSS)


def build_cover() -> None:
    """Editable editorial cover, 1280 x 640."""
    width, height = 1280, 640
    chips = "".join(
        f'<g transform="translate({64 + index * 224} 500)">'
        f'<rect width="206" height="64" rx="18" fill="#081915" stroke="{BORDER}"/>'
        f'{text(24, 40, chip, 17, "#C3D8D2", 600)}</g>'
        for index, chip in enumerate(CHIPS)
    )
    body = f"""{studio(width, height, EYEBROW, STATUS, radius=0)}
  {sculpture(944, 300, .96)}
  {text(64, 150, OWNER, 20, AQUA, 600, cls="m eyebrow")}
  {text(64, 262, NAME, NAME_SIZE_COVER, WHITE, 700, extra=' letter-spacing="-2.4"')}
  {text(64, 330, LINE, 38, "url(#inkFade)", 600, extra=' letter-spacing="-.8"')}
  {text(64, 392, DETAIL, 20, MUTED)}
  {chips}
  {text(64, 608, "abdulelah.de", 18, DIM, 500, cls="m eyebrow")}
  {grain(width, height, radius=0, opacity=.5)}"""
    write_svg("assets/branding/cover.svg", width, height, f"{NAME} — {LINE}", DESC, body,
              css=SCULPTURE_CSS)


def build_social_preview() -> None:
    """The 1280 x 640 card GitHub shows when the repository is shared.

    Composed to survive a thumbnail: fewer elements, larger type.
    """
    width, height = 1280, 640
    body = f"""{studio(width, height, OWNER, STATUS, radius=0)}
  {sculpture(950, 320, .92)}
  {text(64, 196, EYEBROW, 22, AQUA, 600, cls="m eyebrow")}
  {text(64, 310, NAME, NAME_SIZE_SOCIAL, WHITE, 700, extra=' letter-spacing="-2.8"')}
  {text(64, 380, LINE, 42, "url(#inkFade)", 600, extra=' letter-spacing="-.9"')}
  {text(64, 442, DETAIL_SHORT, 24, MUTED)}
  {text(64, 592, "abdulelah.de", 20, DIM, 500, cls="m eyebrow")}
  {grain(width, height, radius=0, opacity=.5)}"""
    write_svg("assets/branding/social-preview.svg", width, height, f"{NAME} — {LINE}", DESC, body,
              css=SCULPTURE_CSS)


def main() -> None:
    build_hero()
    build_hero_mobile()
    build_cover()
    build_social_preview()
    print(f"Generated the {NAME} branding assets.")


if __name__ == "__main__":
    main()
