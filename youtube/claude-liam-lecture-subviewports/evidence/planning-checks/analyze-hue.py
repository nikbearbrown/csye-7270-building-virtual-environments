"""Independent check of the film's hsv_to_rgb: the Lab rendered 06-hsv-strip.gdshader on a 640 x 360 rectangle (UV.x = (x + 0.5) / 640).
Python's colorsys (standard library) gives the reference colour for each column; the comparison is over all 640 columns."""
import colorsys
from pathlib import Path
from PIL import Image
here = Path(__file__).resolve().parent
im = Image.open(here / "png/06-hsv-strip-rect.png").convert("RGB")
W, H = im.size
worst = 0.0
at = 0
for x in range(W):
    h = (x + 0.5) / W
    ref = colorsys.hsv_to_rgb(h, 1.0, 1.0)
    got = [c / 255.0 for c in im.getpixel((x, H // 2))]
    d = max(abs(a - b) for a, b in zip(ref, got))
    if d > worst:
        worst, at = d, x
print(f"06-hsv-strip-rect.png {W}x{H}: {W} columns compared with colorsys.hsv_to_rgb; largest channel difference {worst:.4f} at column {at} (one 8-bit step is 0.0039)")
