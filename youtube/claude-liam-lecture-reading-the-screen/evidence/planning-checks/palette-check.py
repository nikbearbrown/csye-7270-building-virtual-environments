#!/usr/bin/env python3
"""palette-check.py: GATE T risk check for the meadow's colours (and what the film's effects turn them into).

GATE T (brutalist.art/runtime/scripts/type_check.py, ink_mask) counts a pixel as "text" when its Euclidean RGB distance from INK (#3D3929)
or MUTE (#5D584F) is below 48. A capture that is full of such pixels fails as a field of text blobs. This script lists, for every colour the
captures use and for the colours the film's shaders turn them into (inverted, grayscale, tinted by the pool), the smallest distance to INK or MUTE.
Anything under 60 is printed as RISK. Run: python3 palette-check.py
"""
INK = (0x3D, 0x39, 0x29)
MUTE = (0x5D, 0x58, 0x4F)


def hexrgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def dist(a, b):
    return sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5


def worst(c):
    return min(dist(c, INK), dist(c, MUTE))


WORLD = {
    "grass A": "#8CBD73", "grass B": "#9ECC80", "sand path": "#E0CC9E", "tree": "#55916B", "rose flower": "#D9738C",
    "mustard flower / block": "#E6B840", "violet flower / block": "#8C73CC", "test sprite teal": "#5FA391", "cream (eyes, frames)": "#FAF9F5",
    "hud back": "#CFC6E8", "hud fill": "#E6B840", "stage": "#D9D5CA",
}
WATER = (0.2 * 255, 0.5 * 255, 0.8 * 255)


def luma(c):
    return 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]


rows = []
for name, h in WORLD.items():
    c = hexrgb(h)
    inv = tuple(255 - v for v in c)
    g = luma(c)
    gray = (g, g, g)
    tint = tuple(0.5 * a + 0.5 * b for a, b in zip(c, WATER))
    tint_gray = (luma(tint),) * 3
    rows.append((name, h, worst(c), worst(inv), worst(gray), worst(tint)))

print(f"{'colour':26} {'hex':8} {'plain':>6} {'inverted':>9} {'gray':>6} {'pool tint':>10}   (min distance to INK or MUTE; GATE T counts < 48 as text)")
flag = 0
for name, h, a, b, c, d in rows:
    marks = []
    for label, v in (("plain", a), ("inverted", b), ("gray", c), ("pool tint", d)):
        if v < 60:
            marks.append(f"RISK {label} {v:.0f}")
            flag += 1
    print(f"{name:26} {h:8} {a:6.0f} {b:9.0f} {c:6.0f} {d:10.0f}   {'; '.join(marks)}")
print()
print("stage colour read through a window that inverts it (only if a window sits over bare stage; the meadow covers the whole canvas, so it never does):",
      f"{worst(tuple(255 - v for v in hexrgb('#D9D5CA'))):.0f}")
print(f"{flag} risky entries (distance < 60).")
