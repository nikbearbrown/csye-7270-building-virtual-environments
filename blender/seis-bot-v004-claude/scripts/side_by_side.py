"""side_by_side - put your render next to a reference crop so ONE Read shows both.

    python3 <W>/src/side_by_side.py OUT.jpg  LEFT.png  RIGHT.jpg [MORE ...]  [--h 900]

Each input is scaled to the same height (default 900 px) and labelled with its file name; they are joined left to right.
Typical use:  render (left)  |  reference crop (right).
"""
import sys
from PIL import Image, ImageDraw


def main():
    a = sys.argv[1:]
    h = 900
    if "--h" in a:
        i = a.index("--h")
        h = int(a[i + 1])
        del a[i:i + 2]
    out, files = a[0], a[1:]
    ims = []
    for f in files:
        im = Image.open(f).convert("RGB")
        w = max(1, round(im.width * h / im.height))
        ims.append((f, im.resize((w, h), Image.LANCZOS)))
    W = sum(i.width for _, i in ims) + 8 * (len(ims) - 1)
    canvas = Image.new("RGB", (W, h), (20, 20, 24))
    x = 0
    d = ImageDraw.Draw(canvas)
    for f, im in ims:
        canvas.paste(im, (x, 0))
        d.rectangle((x, 0, x + min(im.width, 6 + 7 * len(f.split("/")[-1])), 16), fill=(0, 0, 0))
        d.text((x + 3, 2), f.split("/")[-1], fill=(255, 255, 255))
        x += im.width + 8
    canvas.save(out, quality=90)
    print(out, canvas.size)


main()
