"""Pixel comparisons between Lab renders (png/*.png) that the film's claims rest on. Prints and writes png-analysis.txt.
Needs Pillow. Run after lab-batch.sh."""
from pathlib import Path
from PIL import Image, ImageChops
here = Path(__file__).resolve().parent
P = here / "png"
out = []

def load(n):
    return Image.open(P / f"{n}.png").convert("RGB")

def diff(a, b, tol=0):
    A, B = load(a), load(b)
    if A.size != B.size:
        return f"{a} vs {b}: sizes differ {A.size} {B.size}"
    d = ImageChops.difference(A, B)
    px = d.load(); W, H = d.size
    bad = 0; mx = 0
    for y in range(H):
        for x in range(W):
            m = max(px[x, y]); mx = max(mx, m)
            if m > tol: bad += 1
    return f"{a} vs {b}: size {W}x{H}, pixels differing by more than {tol}/255: {bad} of {W*H}; largest single-channel difference {mx}/255"

out.append("== B07: three spellings of one shader -> one picture")
out.append(diff("02-spacing-neat", "02-spacing-squeezed"))
out.append(diff("02-spacing-neat", "02-spacing-spread"))
out.append(diff("02-spacing-neat", "02-spacing-oneline"))
out.append("== B08: the commented-out line changes the picture; the active line is the pastel one")
out.append(diff("03-comment-on", "03-comment-off", tol=0))
out.append(diff("03-comment-on", "05-pastel"))
out.append("== B20/B24: the same picture reached through a function, and with UV passed in")
out.append(diff("05-pastel", "09-soften-function"))
out.append(diff("05-pastel", "10-pass-uv-in"))
out.append("== B28/B29: if/else and the ternary draw the same picture")
out.append(diff("16-split-if", "17-split-ternary"))

def lit_columns(n, row_frac=0.5):
    im = load(n); W, H = im.size; y = int(row_frac * (H - 1))
    cols = [x for x in range(W) if im.getpixel((x, y))[1] > 150 and im.getpixel((x, y))[0] < 120]
    return W, H, cols

out.append("== B32: where does the teal line land? (teal columns on the middle row)")
for n in ("19-float-equals-640", "19-float-equals-1280", "19-float-equals-1920", "19-float-equals-641", "19-float-equals-1001", "19-float-equals-321",
          "20-float-range-640", "20-float-range-1280", "20-float-range-1920"):
    W, H, cols = lit_columns(n)
    out.append(f"{n}: image {W}x{H}; teal columns: {len(cols)}" + (f" ({cols[0]}..{cols[-1]})" if cols else ""))

out.append("== B30: stripe rows (teal rows down the middle column of 18-stripes)")
im = load("18-stripes"); W, H = im.size; x = W // 2
rows = [y for y in range(H) if im.getpixel((x, y))[1] > 150 and im.getpixel((x, y))[0] < 120]
groups = []
for y in rows:
    if groups and y == groups[-1][1] + 1: groups[-1][1] = y
    else: groups.append([y, y])
out.append(f"image {W}x{H}; {len(groups)} stripes; rows " + ", ".join(f"{a}-{b} (height {b-a+1}, centre {(a+b)/2/H:.3f} of height)" for a, b in groups))

(here / "png-analysis.txt").write_text("\n".join(out) + "\n")
print("\n".join(out))
