"""Measures the left edge of the leaning white square in png/04-lean-white.png (Lab render, scale 1.0). Prints per-row edge positions."""
from pathlib import Path
from PIL import Image
here = Path(__file__).resolve().parent
im = Image.open(here / "png/04-lean-white.png").convert("RGB"); W, H = im.size
print("04-lean-white.png", W, H)
rows = []
for y in range(H):
    xs = [x for x in range(W) if im.getpixel((x, y))[0] > 245 and im.getpixel((x, y))[2] > 245]
    if xs: rows.append((y, min(xs), max(xs)))
y0, y1 = rows[0][0], rows[-1][0]
print("sprite rows", y0, "to", y1, "height", y1 - y0 + 1)
for frac in (0.02, 0.25, 0.5, 0.75, 0.98):
    y = y0 + int(frac * (y1 - y0)); r = [r for r in rows if r[0] == y][0]
    print(f"row at {frac:.2f} of height (y={y}): left edge x={r[1]}  right edge x={r[2]}")
l0 = [r for r in rows if r[0] == y0][0][1]; l1 = [r for r in rows if r[0] == y1][0][1]
print("left edge, first row", l0, " last row", l1, " shift", l1 - l0, "px over", y1 - y0 + 1, "rows (shader constant: 50 px)")
