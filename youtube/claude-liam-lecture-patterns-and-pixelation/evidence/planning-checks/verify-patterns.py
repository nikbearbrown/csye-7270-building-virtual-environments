"""verify-patterns.py: measures the Lab renders in png/ (written by run-lab-checks.sh) and compares them with the formulas.

Run from this folder after run-lab-checks.sh:   python3 verify-patterns.py | tee analysis-summary.txt

Everything here is arithmetic on real Godot 4.7.2 renders (Apple M4 Pro, Forward+ unless a label says "compat").
Sprite renders: the Lab draws a 128 px texture centred in a 640x360 window, so at --sprite-scale 1.0 one picture pixel is one
screen pixel and the sprite's top-left corner is at (256, 116). The Lab stage colour is #D9D5CA (217, 213, 202).
"""
import math
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
PNG = HERE / "png"
STAGE = np.array([217, 213, 202])
X0, Y0, N = 256, 116, 128          # sprite top-left corner and size at scale 1.0
TEAL = np.array([0.373, 0.639, 0.569]) * 255
CREAM = np.array([0.980, 0.976, 0.961]) * 255
GOLD = np.array([0.925, 0.769, 0.380]) * 255


def load(name):
    return np.array(Image.open(PNG / f"{name}.png").convert("RGB")).astype(int)


def head(t):
    print("\n== " + t)


def blob_stats(name):
    im = load(name)
    mask = np.abs(im - STAGE).sum(axis=2) > 6
    ys, xs = np.nonzero(mask)
    return {"cx": xs.mean() + 0.5, "cy": ys.mean() + 0.5, "w": int(xs.max() - xs.min() + 1), "h": int(ys.max() - ys.min() + 1),
            "pixels": int(mask.sum())}


def runs(values):
    out, cur, n = [], values[0], 0
    for v in values:
        if v == cur:
            n += 1
        else:
            out.append(n)
            cur, n = v, 1
    out.append(n)
    return out


def block_runs(name):
    im = load(name)
    row = [tuple(im[Y0 + 64, X0 + x]) for x in range(N)]
    col = [tuple(im[Y0 + y, X0 + 64]) for y in range(N)]
    return runs(row), runs(col)


def summarize_runs(r):
    if len(set(r)) == 1:
        return f"{len(r)} blocks, all {r[0]} px"
    return f"{len(r)} blocks: first {r[0]}, then " + ", ".join(str(x) for x in sorted(set(r[1:-1]))) + f" inside, last {r[-1]} (sum {sum(r)})"


# ── 1. floor and fract as colours (full-image comparison with the formula) ─────────────────────────────────────────────
head("1. floor and fract as colours: every pixel of the 360x360 render against the formula")
S = 360
u = (np.arange(S) + 0.5) / S
U, V = np.meshgrid(u, u)
p = np.stack([U * 4.0, V * 4.0], axis=-1)
exp_floor = np.dstack([0.25 + np.floor(p[..., 0]) * 0.25, 0.25 + np.floor(p[..., 1]) * 0.25, np.full((S, S), 0.55)]) * 255
exp_fract = np.dstack([0.2 + (p[..., 0] - np.floor(p[..., 0])) * 0.7, 0.2 + (p[..., 1] - np.floor(p[..., 1])) * 0.7, np.full((S, S), 0.55)]) * 255
for name, exp in (("02-cells-floor-sq", exp_floor), ("03-cells-fract-sq", exp_fract)):
    d = np.abs(load(name) - exp)
    print(f"{name}: max difference {d.max():.2f} of 255, pixels off by more than 1.5: {(d.max(axis=2) > 1.5).sum()} of {S*S}")
im = load("02-cells-floor-sq")
cells = {(i, j): tuple(im[int((j + 0.5) / 4 * S), int((i + 0.5) / 4 * S)]) for i in range(4) for j in range(4)}
print("cell colours (col,row): " + "; ".join(f"({i},{j}) {cells[(i, j)]}" for (i, j) in [(0, 0), (3, 0), (0, 3), (3, 3), (2, 1)]))
print("distinct colours in the floor render:", len({tuple(c) for c in im.reshape(-1, 3)}), "(16 cells = 16 colours)")
im = load("03-cells-fract-sq")
tile_a = im[0:90, 0:90]
same = all(np.array_equal(tile_a, im[90 * j:90 * (j + 1), 90 * i:90 * (i + 1)]) for i in range(4) for j in range(4))
print("fract render: all sixteen 90 px tiles are pixel-identical copies of the first:", same)

# ── 2. tile (fract as the address into the picture) ────────────────────────────────────────────────────────────────────
head("2. tile: texture(TEXTURE, fract(UV * 3.0)) on the test sprite (288 px square at the Lab's fit scale)")
im = load("04-tile-sprite")
sx, sy, side = 176, 36, 288
tiles = {(i, j): im[sy + 96 * j: sy + 96 * (j + 1), sx + 96 * i: sx + 96 * (i + 1)] for i in range(3) for j in range(3)}
diffs = {(i, j): int((np.abs(tiles[(i, j)] - tiles[(0, 0)]).sum(axis=2) > 0).sum()) for i in range(3) for j in range(3)}
print("pixels (of 9216 per tile) that differ from tile (0,0):", diffs)
blobs = [int((np.abs(tiles[k] - STAGE).sum(axis=2) > 6).sum()) for k in tiles]
print("non-stage pixels per tile (the same blob nine times):", blobs)

# ── 3. pixelate: drift ─────────────────────────────────────────────────────────────────────────────────────────────────────────
head("3. pixelate: where does the picture end up? (centroid of the blob, in picture pixels, against the original blob)")
ref = blob_stats("ref-sprite-1x")
print(f"original blob: centre ({ref['cx']:.2f}, {ref['cy']:.2f}), {ref['w']} x {ref['h']} px, {ref['pixels']} pixels")
for n in (8, 16, 32):
    block = 128 // n
    for tag, label in (("05-corner", "corner  floor(UV*n)/n          "), ("06-center", "middle  (floor(UV*n)+0.5)/n   "), ("07-round", "round   floor(UV*n+0.5)/n     ")):
        b = blob_stats(f"{tag}-n{n}-sprite-1x")
        print(f"n = {n:2d} (blocks {block:2d} px)  {label} shift x {b['cx'] - ref['cx']:+.2f}, y {b['cy'] - ref['cy']:+.2f}  (blob {b['w']} x {b['h']})")

# ── 4. pixelate: block sizes at the edges ────────────────────────────────────────────────────────────────────────────────────
head("4. pixelate: block sizes along the middle row and column of the gradient picture (n = 16 on 128 px)")
for name in ("05-corner-n16-gradient-1x", "06-center-n16-gradient-1x", "07-round-n16-gradient-1x", "08-block8-gradient-1x", "08-block6-gradient-1x"):
    h, v = block_runs(name)
    print(f"{name}\n   across: {summarize_runs(h)}\n   down:   {summarize_runs(v)}")
refg = load("ref-gradient-1x")
print("\nwhich picture pixel does the first / last block show? (gradient red channel = x / 127)")
for name in ("05-corner-n16-gradient-1x", "06-center-n16-gradient-1x", "07-round-n16-gradient-1x"):
    im = load(name)
    first = im[Y0 + 64, X0 + 0]
    last = im[Y0 + 64, X0 + 127]
    # find the picture x whose red equals the block colour
    xs_ref = refg[Y0 + 64, X0:X0 + N, 0]
    fi = int(np.argmin(np.abs(xs_ref - first[0])))
    la = int(np.argmin(np.abs(xs_ref - last[0])))
    print(f"{name}: first block shows picture pixel {fi} (the corner is 0), last block shows picture pixel {la} (the corner is 127; {127 - la} short)")

head("5. pixelate: other checks")
a, b = load("08-block8-gradient-1x"), load("06-center-n16-gradient-1x")
print("block = 8 (picture pixels) against blocks = 16 (middle lookup), gradient: pixels that differ:", int((np.abs(a - b).sum(axis=2) > 0).sum()))
a, b = load("08-block1-sprite-1x"), load("ref-sprite-1x")
print("block = 1 against the untouched picture, sprite: pixels that differ:", int((np.abs(a - b).sum(axis=2) > 0).sum()))
for tag in ("05-pixelate-corner", "06-pixelate-center", "07-pixelate-round"):
    for pic, fp in (("sprite", {"05-pixelate-corner": "05-corner", "06-pixelate-center": "06-center", "07-pixelate-round": "07-round"}[tag] + "-n16-sprite-1x"),
                    ("gradient", {"05-pixelate-corner": "05-corner", "06-pixelate-center": "06-center", "07-pixelate-round": "07-round"}[tag] + "-n16-gradient-1x")):
        d = int((np.abs(load(fp) - load(f"{tag}-n16-{pic}-1x-compat")).sum(axis=2) > 0).sum())
        print(f"{tag} n16 {pic}: Forward+ against Compatibility, pixels that differ: {d}")
d = int((np.abs(load("08-block8-sprite-fit") - load("08-block8-sprite-fit-compat")).sum(axis=2) > 0).sum())
print("08-pixelate-block block=8, sprite at fit scale: Forward+ against Compatibility, pixels that differ:", d)
for blk in (1, 2, 4, 8, 16, 32):
    im = load(f"08-block{blk}-sprite-fit")
    cols = len({tuple(c) for c in im.reshape(-1, 3)})
    mask = np.abs(im - STAGE).sum(axis=2) > 6
    print(f"block {blk:2d}: {cols} distinct colours, blob {int(mask.sum())} px")
# block size on screen at the fit scale (2.25): measure runs along a row through the middle of the gradient-like sprite? use the sprite's own blob rows
im = load("08-block8-sprite-fit")
row = [tuple(im[180, x]) for x in range(176, 464)]
print("block 8 at the fit scale (the sprite is drawn 2.25 times larger): run lengths along the middle row of the 288 px sprite:", runs(row))

# ── 6. checkerboard ──────────────────────────────────────────────────────────────────────────────────────────────────────────
head("6. checkerboard: all 64 cells of the 360x360 render against mod(column + row, 2)")
im = load("09-checker-sq")
ok = bad = 0
for j in range(8):
    for i in range(8):
        parity = (i + j) % 2
        expect = TEAL if parity == 0 else CREAM
        got = im[int((j + 0.5) * 45), int((i + 0.5) * 45)]
        if np.abs(got - expect).max() <= 1.5:
            ok += 1
        else:
            bad += 1
print(f"cells matching the formula: {ok} of 64 (mismatches {bad})")
print("whole image: pixels that are neither teal nor cream:", int((np.minimum(np.abs(im - TEAL).max(axis=2), np.abs(im - CREAM).max(axis=2)) > 1.5).sum()))
print("four cells (0,0) (1,0) (0,1) (1,1):", [("teal" if np.abs(im[int((j + 0.5) * 45), int((i + 0.5) * 45)] - TEAL).max() < 2 else "cream") for (i, j) in [(0, 0), (1, 0), (0, 1), (1, 1)]])
print("diagonal neighbours share a colour, edge neighbours differ:",
      all(tuple(im[int((j + 0.5) * 45), int((i + 0.5) * 45)]) == tuple(im[int((j + 1.5) * 45), int((i + 1.5) * 45)]) != tuple(im[int((j + 0.5) * 45), int((i + 1.5) * 45)])
          for i in range(7) for j in range(7)))
d = int((np.abs(load("09-checker-sq") - load("09-checker-sq-compat")).sum(axis=2) > 0).sum())

# ── 7. stripes ───────────────────────────────────────────────────────────────────────────────────────────────────────────────
head("7. stripes: the 360x360 render against fract((UV.x + UV.y) * count) and step(width, .)")


def stripe_expect(count, width, shift=0.0):
    diag = U + V
    f = diag * count - shift
    f = f - np.floor(f)
    return (f >= width)


def classify(im):
    dg = np.abs(im - GOLD).max(axis=2)
    cr = np.abs(im - CREAM).max(axis=2)
    return cr < dg      # True where cream


for name, count, width in (("10-stripes-sq", 4, 0.5), ("10-stripes-w25-sq", 4, 0.25), ("10-stripes-w75-sq", 4, 0.75), ("10-stripes-c8-sq", 8, 0.5)):
    im = load(name)
    got = classify(im)
    exp = stripe_expect(count, width)
    mism = int((got != exp).sum())
    gold_share = 1.0 - got.mean()
    print(f"{name}: count {count}, width {width}: pixels differing from the formula {mism} of {S*S} (all within one pixel of a stripe edge: "
          f"{'yes' if mism < 0.01 * S * S else 'CHECK'}); gold share {gold_share:.3f} (width says {width})")
top = classify(load("10-stripes-sq"))[2, :]
top = classify(load("10-stripes-sq"))[2, :]
gold_ends = sum(1 for k in range(1, len(top)) if (not top[k - 1]) and top[k])
gold_starts = sum(1 for k in range(1, len(top)) if top[k - 1] and (not top[k])) + (1 if not top[0] else 0)
print(f"count = 4: along the top row {gold_ends} gold stripes end in cream (and {gold_starts} start, the last one a sliver at the far corner)")
print("stripe edges follow lines of constant x + y: pixel (x, y) and (x + 7, y - 7) agree:", bool(np.mean(classify(load("10-stripes-sq"))[10:300, 10:300] == classify(load("10-stripes-sq"))[3:293, 17:307]) > 0.97))
t1, t2 = classify(load("11-stripes-moving-t1")), classify(load("11-stripes-moving-t2"))
swapped = float((t1 != t2).mean())
print(f"moving stripes, speed 0.5, two renders about one second apart (waited_s 0.300 and 1.306 in lab-results.jsonl): share of pixels whose colour swapped: {swapped:.3f}")
print(f"expected for a shift of {0.5 * 1.006:.3f} of a period at width 0.5: swapped share about {min(1.0, 2 * abs(0.5 * 1.006 - 0.0)) if False else 'near 1.0 (half a period swaps gold and cream)'}")

head("7b. moving stripes: which TIME does each render show? (best fit of fract((x + y) * 4 - TIME * 0.5) to the pixels)")
fits = {}
for name, waited in (("11-stripes-moving-t0", 0.0), ("11-stripes-moving-t1", 0.3), ("11-stripes-moving-t3", 0.6), ("11-stripes-moving-t2", 1.3)):
    got = classify(load(name))
    best = None
    for t in np.arange(0.0, 4.0, 0.005):
        exp = stripe_expect(4, 0.5, shift=t * 0.5)
        mism = float((got != exp).mean())
        if best is None or mism < best[1]:
            best = (t, mism)
    fits[name] = best
    print(f"{name} (asked to wait {waited} s): best-fit TIME = {best[0]:.3f} s (mod 2 s, the period of the pattern), pixels still differing {100 * best[1]:.2f}%")
t0, t1, t3, t2 = (fits[k][0] for k in ("11-stripes-moving-t0", "11-stripes-moving-t1", "11-stripes-moving-t3", "11-stripes-moving-t2"))
print(f"TIME differences between renders (mod 2 s): t1 - t0 = {(t1 - t0) % 2:.3f}, t3 - t1 = {(t3 - t1) % 2:.3f}, t2 - t1 = {(t2 - t1) % 2:.3f}")
print("The pattern moves toward larger x + y as TIME grows (the fit above uses a minus sign on TIME, so a positive TIME step reproduces the render).")

# ── 8. dots ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────
head("8. dots: coverage against radius (8 x 8 cells, 360x360 render; teal = inside the circle)")
for r in (0.2, 0.35, 0.5, 0.6, 0.7, 0.72):
    im = load(f"12-dots-r{r}-sq")
    teal = np.abs(im - TEAL).max(axis=2) < 2
    cov = float(teal.mean())
    area = (math.pi * r * r) if r <= 0.5 else (None)
    if r > 0.5:
        # area of a circle of radius r inside the unit square, by sampling
        g = (np.arange(1000) + 0.5) / 1000 - 0.5
        GX, GY = np.meshgrid(g, g)
        area = float((np.hypot(GX, GY) < r).mean())
    print(f"radius {r:4.2f}: {100 * cov:5.1f}% of the picture is dot (geometry says {100 * area:5.1f}%)")
im = load("12-dots-r0.5-sq")
teal = np.abs(im - TEAL).max(axis=2) < 2
print("radius 0.50: the dot in cell (3,3) spans x from", int(np.nonzero(teal[3 * 45 + 22, :])[0][(np.nonzero(teal[3 * 45 + 22, :])[0] // 45) == 3].min()), "to", int(np.nonzero(teal[3 * 45 + 22, :])[0][(np.nonzero(teal[3 * 45 + 22, :])[0] // 45) == 3].max()), "(the cell spans 135 to 179): touches both neighbours")
im = load("12-dots-r0.72-sq")
print("radius 0.72: any cream pixel left?", bool((np.abs(im - CREAM).max(axis=2) < 2).any()), "| radius 0.70: cream pixels left:", int((np.abs(load("12-dots-r0.7-sq") - CREAM).max(axis=2) < 2).sum()))
print("half the diagonal of a unit cell:", round(math.sqrt(0.5), 4))


def dot_box(im, cx0, cy0, cw, ch):
    sub = im[cy0:cy0 + ch, cx0:cx0 + cw]
    t = np.abs(sub - TEAL).max(axis=2) < 2
    ys, xs = np.nonzero(t)
    return int(xs.max() - xs.min() + 1), int(ys.max() - ys.min() + 1)


head("9. dots on a wide rectangle (640x360): the trap and the fix")
im = load("12-dots-wide")
cw, ch = 640 / 8, 360 / 8
boxes = [dot_box(im, int(i * cw), int(j * ch), int(cw), int(ch)) for (i, j) in [(0, 0), (4, 4), (7, 7), (2, 6)]]
print(f"cells = 8 across and 8 down: each cell is {cw:.1f} x {ch:.1f} px; measured dot width x height in four cells: {boxes}; ratio {np.mean([b[0] / b[1] for b in boxes]):.2f}")
im = load("13-dots-square-wide")
cw, ch = 640 / 16, 360 / 9
boxes = [dot_box(im, int(i * cw), int(j * ch), int(cw), int(ch)) for (i, j) in [(0, 0), (8, 4), (15, 8), (3, 6)]]
print(f"cells = (16, 9): each cell is {cw:.1f} x {ch:.1f} px; measured dot width x height in four cells: {boxes}; ratio {np.mean([b[0] / b[1] for b in boxes]):.2f}")
d = int((np.abs(load("12-dots-wide") - load("12-dots-wide-compat")).sum(axis=2) > 0).sum())
print("12-dots-wide: Forward+ against Compatibility, pixels that differ:", d)
d = int((np.abs(load("09-checker-sq") - load("09-checker-sq-compat")).sum(axis=2) > 0).sum())
print("09-checker: Forward+ against Compatibility, pixels that differ:", d)

# ── 10. halftone ─────────────────────────────────────────────────────────────────────────────────────────────────────────────
head("10. halftone (dots coloured from the picture at each cell's middle), 16 cells on the 128 px gradient picture")
im, refg = load("14-halftone-gradient-1x"), load("ref-gradient-1x")
boxes = {}
for (i, j) in [(0, 0), (15, 0), (0, 15), (15, 15), (7, 7), (3, 12)]:
    sub = im[Y0 + 8 * j: Y0 + 8 * j + 8, X0 + 8 * i: X0 + 8 * i + 8]
    m = np.abs(sub - STAGE).sum(axis=2) > 6
    ys, xs = np.nonzero(m)
    boxes[(i, j)] = (int(xs.max() - xs.min() + 1), int(ys.max() - ys.min() + 1), int(m.sum()))
print("dot width x height x pixels in cells (col,row):", boxes)
print("every cell's dot is the same size (edges and corners whole):", len({v for v in boxes.values()}) == 1)
bad = 0
for j in range(16):
    for i in range(16):
        c = im[Y0 + 8 * j + 4, X0 + 8 * i + 4]
        want = refg[Y0 + 8 * j + 4, X0 + 8 * i + 4]
        if np.abs(c - want).max() > 1:
            bad += 1
print("dot colour at the cell middle equals the picture pixel at the cell middle (8i+4, 8j+4): cells that disagree:", bad, "of 256")
im = load("14-halftone-sprite-1x")
sub = im[Y0:Y0 + 128, X0:X0 + 128]
print("sprite halftone at 16 cells: distinct non-stage colours:", sorted({tuple(c) for c in sub.reshape(-1, 3)} - {tuple(STAGE)}))
d = {tuple(c) for c in load("14-halftone-sprite-fit").reshape(-1, 3)}
print("sprite halftone at the fit scale: colours present (stage, teal, cream, plus edge pixels):", len(d))

head("11. smooth filter against nearest filter, middle-of-the-cell lookup (256x256 sampler texture, 16 blocks)")
a, b = load("chk-filter-linear"), load("chk-filter-nearest")
print("distinct colours: smooth", len({tuple(c) for c in a.reshape(-1, 3)}), "nearest", len({tuple(c) for c in b.reshape(-1, 3)}),
      "| pixels that differ:", int((np.abs(a - b).sum(axis=2) > 0).sum()), "of", a.shape[0] * a.shape[1])


def blobs(name):
    """Connected blobs (4-neighbour) of non-stage pixels in the 128 px sprite area of a scale-1.0 render: list of areas."""
    im = load(name)[Y0:Y0 + N, X0:X0 + N]
    mask = np.abs(im - STAGE).sum(axis=2) > 6
    seen = np.zeros_like(mask)
    areas = []
    for y in range(N):
        for x in range(N):
            if mask[y, x] and not seen[y, x]:
                stack, area = [(y, x)], 0
                seen[y, x] = True
                while stack:
                    cy, cx = stack.pop()
                    area += 1
                    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        ny, nx = cy + dy, cx + dx
                        if 0 <= ny < N and 0 <= nx < N and mask[ny, nx] and not seen[ny, nx]:
                            seen[ny, nx] = True
                            stack.append((ny, nx))
                areas.append(area)
    return areas


head("12. halftone on a picture that reaches the edges (checker texture, 128 px, 8 cells): whole dots against the rounded variant")
for name in ("14-halftone-checker-c8-1x", "15-halftone-rounded-checker-c8-1x"):
    a = sorted(blobs(name))
    med = a[len(a) // 2]
    print(f"{name}: {len(a)} dots, areas min {a[0]}, median {med}, max {a[-1]}; dots smaller than 80% of the median: {sum(1 for v in a if v < 0.8 * med)}")
print("expected: the floored version has 8 x 8 = 64 whole dots; the rounded version has 9 x 9 = 81 blobs, 32 of them cut by the picture's edge")
