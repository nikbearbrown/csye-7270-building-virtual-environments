"""Measures the stripes the Lab drew with 04-stripes.gdshader on a plain 640 x 360 rectangle (TEXTURE is white there):
the on-fraction of the top row should equal `width`, and the number of complete stripes should equal `count`."""
from pathlib import Path
from PIL import Image
here = Path(__file__).resolve().parent
stage = (217, 213, 202)
for cnt, wid in (("6.0", "0.5"), ("10.0", "0.25"), ("3.0", "0.8")):
    im = Image.open(here / f"png/stripes-{cnt}-{wid}.png").convert("RGB")
    W, H = im.size
    on = [sum(abs(a - b) for a, b in zip(im.getpixel((x, 0)), stage)) > 30 for x in range(W)]
    runs, prev, run_len, complete = 0, False, 0, 0
    for v in on:
        if v and not prev:
            runs += 1
            run_len = 0
        if v:
            run_len += 1
        if prev and not v and run_len > 8:
            complete += 1
        prev = v
    print(f"count={cnt} width={wid}: top row on-fraction {sum(on) / W:.3f}; stripes {runs} (complete {complete}; the extra sliver is the right edge where UV.x reaches 1)")
