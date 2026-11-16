#!/usr/bin/env python3
"""make_textures.py - generates every test texture for shader_lessons_godot from code.

PROVENANCE: code-authored. No outside art, no photographs, no files from the Eat 3D DVD (the DVD's
default_color.dds / default_cube.dds / normal / spec maps were never available). Every pixel below is
computed by this script from simple formulas. Re-running it reproduces the files byte for byte.

Run (from anywhere):   python3 /abs/path/to/shader_lessons_godot/tools/make_textures.py
Needs: python3, numpy, Pillow.   Writes into ../textures/   and prints a self-check report.

Files written
  diffuse_checker.png   512x512 sRGB   8x8 checker, 4 orientation cells on the camera-facing side of the test sphere (red = column 0 row 3, green = +u neighbour, yellow = +v neighbour, magenta = column 7 row 3)
  spec_rg.png           512x512 data   R = rim mask (rows), G = specular mask (checker), B = 0         (lessons 07, 08, 11, 12 use R=rim, G=spec)
  spec_uber.png         512x512 data   R = specular mask (rows), B = reflection mask (columns), G = 0    (lesson 15 uses R=spec, B=reflection)
  normal_gl.png         512x512 data   tangent-space normal map, OpenGL / Maya convention: green = +slope toward the TOP of the image
  normal_dx.png         512x512 data   the same height field, DirectX convention: green inverted
  blend_map.png         512x512 data   R / G / B regions for the blend lesson (13)
  cube_px.png ... cube_nz.png   256x256 sRGB   six faces of the reflection cube map, written per the OpenGL cube-map face table
"""
import sys
from pathlib import Path
import numpy as np
from PIL import Image

OUT = Path(__file__).resolve().parents[1] / "textures"
OUT.mkdir(parents=True, exist_ok=True)
N = 512
CELL = N // 8   # 64 px


def save(name, arr):
    arr = np.clip(np.rint(arr), 0, 255).astype(np.uint8)
    Image.fromarray(arr, "RGB").save(OUT / name, optimize=False)


yy, xx = np.mgrid[0:N, 0:N]
cx = xx // CELL           # cell column 0..7 (u direction)
cy = yy // CELL           # cell row 0..7 (v direction, 0 = top of the image)
parity = (cx + cy) % 2

# ---------------------------------------------------------------- diffuse checker (sRGB bytes)
SAND = np.array([226, 200, 140], float)
STEEL = np.array([70, 110, 150], float)
diffuse = np.where(parity[..., None] == 0, SAND, STEEL).astype(float)
marks = {(0, 3): (205, 60, 50), (1, 3): (60, 165, 75), (0, 4): (235, 205, 60), (7, 3): (190, 60, 170)}  # (col,row): on the test sphere these four cells face the camera
for (c, r), col in marks.items():
    diffuse[(cx == c) & (cy == r)] = col
save("diffuse_checker.png", diffuse)

# ---------------------------------------------------------------- specular masks (linear data bytes)
rim_rows = np.where(cy % 2 == 0, 255.0, 64.0)                    # R: bright rows, dim rows
spec_checker = np.where(parity == 0, 255.0, 0.0)                 # G: the SAND cells shine, the STEEL cells are matte
spec_rg = np.stack([rim_rows, spec_checker, np.zeros_like(rim_rows)], axis=-1)
save("spec_rg.png", spec_rg)

spec_rows = np.where(cy % 2 == 1, 255.0, 77.0)                   # uber R: specular mask (odd rows shine)
refl_cols = np.where(cx % 2 == 0, 255.0, 38.0)                   # uber B: reflection mask (even columns reflect)
spec_uber = np.stack([spec_rows, np.zeros_like(spec_rows), refl_cols], axis=-1)
save("spec_uber.png", spec_uber)

# ---------------------------------------------------------------- normal map from a height field
# height h (in pixel units) = a round dome in every 64 px cell:  h = H * 0.5 * (1 + cos(pi * r)),  r = distance to the cell centre / 32, 0 outside r = 1.
H = 20.0
lx = (xx % CELL) + 0.5 - CELL / 2.0       # pixel offset from the cell centre, x to the right
ly = (yy % CELL) + 0.5 - CELL / 2.0       # pixel offset from the cell centre, y DOWN the image (rows)
dist = np.hypot(lx, ly)
r = np.minimum(dist / (CELL / 2.0), 1.0)
dh_dr = np.where(dist / (CELL / 2.0) < 1.0, -H * 0.5 * np.pi * np.sin(np.pi * r), 0.0)   # per unit r
safe = np.where(dist > 1e-9, dist, 1.0)
dh_dx = dh_dr * (lx / safe) / (CELL / 2.0)       # analytic slope along +x (to the right)
dh_drow = dh_dr * (ly / safe) / (CELL / 2.0)     # analytic slope along +row (DOWN the image)
# surface z = h(x, y_up) with y_up = -row:   normal = (-dh/dx, -dh/dy_up, 1) = (-dh/dx, +dh/drow, 1)
nx, ny, nz = -dh_dx, +dh_drow, np.ones_like(dh_dx)
ln = np.sqrt(nx * nx + ny * ny + nz * nz)
nx, ny, nz = nx / ln, ny / ln, nz / ln
gl = np.rint(np.stack([(nx * 0.5 + 0.5) * 255, (ny * 0.5 + 0.5) * 255, (nz * 0.5 + 0.5) * 255], axis=-1))   # round to the 8-bit file value FIRST
dx = gl.copy()
dx[..., 1] = 255.0 - gl[..., 1]                  # DirectX convention: green inverted, exactly 255 minus the GL file byte
save("normal_gl.png", gl)
save("normal_dx.png", dx)

# ---------------------------------------------------------------- blend map (linear data bytes)
u = (xx + 0.5) / N
v = (yy + 0.5) / N


def ramp(x, a, b):
    return np.clip((x - a) / (b - a), 0.0, 1.0)


# three vertical bands in u (red | green | blue) with 0.06-wide soft joins, plus a pure-blue disc (visible on the front of the test sphere) and a pure-green disc (also on the camera side)
wr = 1.0 - ramp(u, 0.30, 0.36)
wb = ramp(u, 0.64, 0.70)
wg = 1.0 - wr - wb
disc_b = (np.hypot(u - 0.17, v - 0.30) < 0.10).astype(float)
disc_g = (np.hypot(u - 0.94, v - 0.68) < 0.05).astype(float)
R = wr * (1 - disc_b) * (1 - disc_g)
B = np.clip(wb * (1 - disc_g) + disc_b, 0, 1)
G = np.clip(wg * (1 - disc_b) + disc_g, 0, 1)
save("blend_map.png", np.stack([R, G, B], axis=-1) * 255.0)

# ---------------------------------------------------------------- cube map faces (sRGB bytes), OpenGL face table
S = 256
SUN_TOWARD = np.array([-0.5, 0.8, 0.6]); SUN_TOWARD /= np.linalg.norm(SUN_TOWARD)   # same place the lesson light comes FROM


def env(d):
    """colour of the world in direction d (array [...,3], unit vectors) - a simple studio sky: blue dome, checker floor,
    four coloured wall markers on the horizon (+X red, -X cyan, +Z yellow, -Z magenta), and a white sun disc."""
    x, y, z = d[..., 0], d[..., 1], d[..., 2]
    out = np.zeros(d.shape, float)
    # sky
    t = np.clip(y, 0, 1) ** 0.6
    horizon = np.array([205, 220, 235], float)
    zenith = np.array([40, 100, 200], float)
    sky = horizon[None, None, :] * (1 - t[..., None]) + zenith[None, None, :] * t[..., None]
    # floor: checker on the plane y = -1 seen from the origin
    with np.errstate(divide="ignore", invalid="ignore"):
        k = np.where(y < -1e-6, -1.0 / y, 1.0)
    px, pz = x * k, z * k
    chk = ((np.floor(px) + np.floor(pz)) % 2 == 0)
    floor_a = np.array([150, 150, 150], float)
    floor_b = np.array([95, 95, 95], float)
    floor = np.where(chk[..., None], floor_a, floor_b)
    fade = 1.0 - np.exp(-k * 0.25)                    # closer to the horizon -> more horizon colour
    floor = floor * (1 - fade[..., None]) + horizon * fade[..., None]
    out = np.where((y >= 0)[..., None], sky, floor)
    # horizon wall markers (|y| < 0.14): colour by which axis the direction is closest to, within +-35 degrees
    band = np.abs(y) < 0.14
    for axis_vec, col in ((np.array([1, 0, 0.0]), (220, 40, 40)), (np.array([-1, 0, 0.0]), (40, 210, 220)),
                          (np.array([0, 0, 1.0]), (240, 220, 40)), (np.array([0, 0, -1.0]), (220, 50, 200))):
        c = x * axis_vec[0] + z * axis_vec[2]
        horiz = np.sqrt(x * x + z * z)
        ang = np.degrees(np.arccos(np.clip(c / np.maximum(horiz, 1e-9), -1, 1)))
        out = np.where((band & (ang < 35.0))[..., None], np.array(col, float), out)
    # sun
    sun = (x * SUN_TOWARD[0] + y * SUN_TOWARD[1] + z * SUN_TOWARD[2]) > 0.996
    out = np.where(sun[..., None], np.array([255, 252, 240], float), out)
    return out


FACES = {  # name: function (sc, tc) -> direction, per the OpenGL cube map face selection table (spec 8.13): face (+X) uses sc=-rz, tc=-ry, ma=rx ...
    "px": lambda sc, tc: np.stack([np.ones_like(sc), -tc, -sc], -1),
    "nx": lambda sc, tc: np.stack([-np.ones_like(sc), -tc, sc], -1),
    "py": lambda sc, tc: np.stack([sc, np.ones_like(sc), tc], -1),
    "ny": lambda sc, tc: np.stack([sc, -np.ones_like(sc), -tc], -1),
    "pz": lambda sc, tc: np.stack([sc, -tc, np.ones_like(sc)], -1),
    "nz": lambda sc, tc: np.stack([-sc, -tc, -np.ones_like(sc)], -1),
}
jj, ii = np.mgrid[0:S, 0:S]
sc_grid = 2.0 * (ii + 0.5) / S - 1.0     # s across the image, left to right
tc_grid = 2.0 * (jj + 0.5) / S - 1.0     # t DOWN the image
for name, fn in FACES.items():
    d = fn(sc_grid, tc_grid)
    d = d / np.linalg.norm(d, axis=-1, keepdims=True)
    save(f"cube_{name}.png", env(d))

# ---------------------------------------------------------------- self-check
def load(name):
    return np.asarray(Image.open(OUT / name).convert("RGB")).astype(float)


print("make_textures.py self-check")
g = load("normal_gl.png") / 255.0 * 2 - 1
lens = np.linalg.norm(g, axis=-1)
print(f"  normal_gl: decoded vector length min {lens.min():.4f} max {lens.max():.4f} (8-bit rounding only)")
# a dome cell centre is flat; the RIGHT side of a dome must lean right (R > 0.5), the BOTTOM side must lean down (G < 0.5 in the GL map)
row, col = 32, 32 + 16        # cell (0,0): 16 px to the right of the centre
print(f"  normal_gl right of dome centre: R byte {int(load('normal_gl.png')[row, col, 0])} (>127.5 = leans right)")
row, col = 32 + 16, 32
print(f"  normal_gl below dome centre:    G byte {int(load('normal_gl.png')[row, col, 1])} (<127.5 = leans down on screen, GL convention)")
print(f"  normal_dx below dome centre:    G byte {int(load('normal_dx.png')[row, col, 1])} (>127.5, inverted)")
print(f"  diffuse_checker cell colours: (col0,row3) {load('diffuse_checker.png')[3*64+10,10].astype(int)}, (col1,row3) {load('diffuse_checker.png')[3*64+10,74].astype(int)}")
print(f"  files in {OUT}: " + ", ".join(sorted(p.name for p in OUT.glob('*.png'))))
sys.exit(0)
