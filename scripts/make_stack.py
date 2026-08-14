#!/usr/bin/env python3
"""Draw stack.svg — official Simple Icons, same column as the rest of the page.

Brand-coloured marks stay their colour in both themes. Next.js, Three.js and
Expo are drawn in the page's ink so they don't vanish on GitHub's dark surface.

Sources live in scripts/icons/ (Simple Icons, CC0). Re-run this file after
changing the list; it does not need a GitHub token.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import generate_stats as g  # noqa: E402

ICON_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons")

# slug in scripts/icons/, label under the mark, brand hex or None to use ink
STACK = [
    ("typescript", "typescript", "#3178C6"),
    ("javascript", "javascript", "#F7DF1E"),
    ("python",     "python",     "#3776AB"),
    ("vuedotjs",   "vue",        "#4FC08D"),
    ("react",      "react",      "#61DAFB"),
    ("react",      "react-native","#61DAFB"),
    ("nextdotjs",  "next.js",    None),
    ("nodedotjs",  "node",       "#5FA04E"),
    ("threedotjs", "three.js",   None),
    ("expo",       "expo",       None),
    ("firebase",   "firebase",   "#DD2C00"),
    ("docker",     "docker",     "#2496ED"),
    ("git",        "git",        "#F05032"),
]

COLS = 7
ICON = 32
PAD_TOP = 10
GAP = 14          # icon bottom → label baseline
ROW_GAP = 22      # label baseline → next row's icon
LABEL_SIZE = 9
DESCENDER = 8     # room under the last baseline so p/y/g don't clip


def path_of(slug):
    with open(os.path.join(ICON_DIR, f"{slug}.svg"), encoding="utf-8") as f:
        svg = f.read()
    found = re.search(r'<path d="([^"]+)"', svg)
    if not found:
        raise SystemExit(f"no path in {slug}.svg")
    return found.group(1)


def mark(x, y, slug, d, color):
    """Place a 24×24 Simple Icon with its origin at (x, y)."""
    s = ICON / 24
    fill = 'class="e-f"' if color is None else f'fill="{color}"'
    parts = []
    # JS letters are holes in the yellow square. Ink behind them so they
    # read as the official dark-on-yellow mark instead of empty cutouts.
    if slug == "javascript":
        parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{ICON}" '
                     f'height="{ICON}" class="e-f"/>')
    parts.append(f'<g transform="translate({x:.1f} {y:.1f}) scale({s:.4f})">'
                 f'<path d="{d}" {fill}/></g>')
    return "".join(parts)


def draw():
    n = len(STACK)
    rows = (n + COLS - 1) // COLS
    row_h = ICON + GAP
    H = PAD_TOP + rows * row_h + (rows - 1) * ROW_GAP + DESCENDER
    cell = g.WIDTH / COLS

    p = [g.head(g.WIDTH, H)]
    for i, (slug, name, color) in enumerate(STACK):
        r, c = divmod(i, COLS)
        count = COLS if r < rows - 1 else n - r * COLS
        # last row centres leftover cells
        offset = (g.WIDTH - count * cell) / 2 if r == rows - 1 else 0
        cx = offset + (c + 0.5) * cell
        iy = PAD_TOP + r * (row_h + ROW_GAP)
        lx = cx
        ly = iy + ICON + GAP
        p.append("<g>"
                 + mark(cx - ICON / 2, iy, slug, path_of(slug), color)
                 + g.label(lx, ly, name, LABEL_SIZE, "m-f", "middle")
                 + "</g>")
    p.append("</svg>")
    return "".join(p)


def main():
    out = os.path.join(os.environ.get("OUT_DIR", "."), "stack.svg")
    svg = draw()
    changed = g.write(out, svg)
    print(("wrote " if changed else "unchanged ") + out)


if __name__ == "__main__":
    main()
