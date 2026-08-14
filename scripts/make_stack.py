#!/usr/bin/env python3
"""Draw stack.svg — official brand marks, same 620px column as the rest.

Icons are the Devicon originals (MIT), inlined so the README never calls a
CDN. Next.js, Three.js and Expo are black-on-transparent; they invert in
dark mode so they don't vanish on GitHub's dark surface.

Re-run this file after changing the list. No GitHub token required.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import generate_stats as g  # noqa: E402

ICON_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons")

# file in scripts/icons/, label, invert in dark mode
STACK = [
    ("typescript",   "typescript",    False),
    ("javascript",   "javascript",    False),
    ("python",       "python",        False),
    ("vue",          "vue",           False),
    ("react",        "react",         False),
    ("react-native", "react-native",  False),
    ("nextjs",       "next.js",       True),
    ("node",         "node",          False),
    ("threejs",      "three.js",      True),
    ("expo",         "expo",          True),
    ("firebase",     "firebase",      False),
    ("docker",       "docker",        False),
    ("git",          "git",           False),
]

COLS = 7
ICON = 32
PAD_TOP = 10
GAP = 14
ROW_GAP = 22
LABEL_SIZE = 9
DESCENDER = 8
INK = ".ink{fill:#24292f}@media(prefers-color-scheme:dark){.ink{filter:invert(1)}}"


def nest(slug, x, y, ink):
    """Inner <svg> of a Devicon file, IDs prefixed so gradients don't collide."""
    raw = open(os.path.join(ICON_DIR, f"{slug}.svg"), encoding="utf-8").read()
    vb = re.search(r'viewBox="([^"]+)"', raw)
    body = re.search(r"<svg[^>]*>(.*)</svg>", raw, re.S)
    if not vb or not body:
        raise SystemExit(f"bad svg: {slug}")
    inner = body.group(1)
    for i in sorted(set(re.findall(r'\bid="([^"]+)"', inner)), key=len, reverse=True):
        inner = inner.replace(f'id="{i}"', f'id="{slug}-{i}"')
        inner = inner.replace(f"url(#{i})", f"url(#{slug}-{i})")
    cls = ' class="ink"' if ink else ""
    fill = ' fill="#111"' if ink else ""
    return (f'<svg x="{x:.1f}" y="{y:.1f}" width="{ICON}" height="{ICON}" '
            f'viewBox="{vb.group(1)}"{cls}{fill}>{inner}</svg>')


def draw():
    n = len(STACK)
    rows = (n + COLS - 1) // COLS
    row_h = ICON + GAP
    H = PAD_TOP + rows * row_h + (rows - 1) * ROW_GAP + DESCENDER
    cell = g.WIDTH / COLS

    head = g.head(g.WIDTH, H).replace("</style>", INK + "</style>")
    p = [head]
    for i, (slug, name, ink) in enumerate(STACK):
        r, c = divmod(i, COLS)
        count = COLS if r < rows - 1 else n - r * COLS
        offset = (g.WIDTH - count * cell) / 2 if r == rows - 1 else 0
        cx = offset + (c + 0.5) * cell
        iy = PAD_TOP + r * (row_h + ROW_GAP)
        p.append("<g>"
                 + nest(slug, cx - ICON / 2, iy, ink)
                 + g.label(cx, iy + ICON + GAP, name, LABEL_SIZE, "m-f", "middle")
                 + "</g>")
    p.append("</svg>")
    return "".join(p)


def main():
    out = os.path.join(os.environ.get("OUT_DIR", "."), "stack.svg")
    changed = g.write(out, draw())
    print(("wrote " if changed else "unchanged ") + out)


if __name__ == "__main__":
    main()
