"""foot - SEIS bot foot, ON-MODEL conform ROUND 2 (spec/ONMODEL.md FOOT rows + CRITIC-round2 FOOT + Bear's detail delivery spec).
Built LEFT (+X), mirrored.

What the frames show (f01/f02, right heel + instep only): a smooth swept glossy teal boot, its shin crest sweeping forward
into the instep in one curve, silver-gold edge piping, a near-black wedge heel behind the shin with a scooped arch at its base.
No lames, straps, tread tiles, buckles, red toe pods or five chunky toes.  NO flat black sole plate: the boot's own rounded
underside is the sole (only a narrow dark tread strip tucked UNDER the rounding, never wider than the boot).

Round 2 = round 1 silhouette (kept) + width 0.136 m (was 0.12) + the flat sole slab deleted + DETAIL put back on top of the
clean look: overlapping instep / quarter / toe-tip plates with dark-core panel gaps, heel cap plate, a clevis + stepped
bearing + washer + 6 round-head bolts at the ankle hinge (outer and inner), a toe flex hinge (pin caps, two clevis plates,
hex bolts), hex / round-head fasteners at plate corners, and two thin hoses with clamps and a ferrule into the heel.

P(lx, f, z) = world point: lx metres outboard of the ankle axis, f metres forward (-Y) of it, z height.  Sizes in H heads.
"""
import math
import bpy
import bmesh
from mathutils import Vector, Matrix
import seis_lib as L
import seis_spec as S
from foot_kit import H, AX, A, h, P, interp, Reg, join_named, split_at_plane, sweep_mesh_centered
import foot_detail as D

PI = math.pi
SOLE_T = 0.0015                         # tread strip height / start of the upper's underside
TOE_PIVOT_F = h(0.60)                  # toe flex line (the toes bone hinges here)
CUT_F = h(0.62)                        # split plane between the foot piece and the toe cap
ARCH_F, ARCH_R = -0.235, 0.125              # scooped arch centre (H forward of the ankle) and radius (H)
TOE_SPRING = math.radians(9.0)
F_REAR, F_TIP = -0.28, 0.93           # tread strip extent in H

# ------------------------------------------------------------------ the swept upper: shin crest -> instep -> blunt toe
# rows = (f_H, top_H, half_width_H [, superellipse n])   (0.266 H = 0.068 m half width -> boot 0.136 m wide, ONMODEL 0.14)
ROWS = [(-0.12, 0.60, 0.266, 3.2), (-0.06, 0.64, 0.278, 3.2), (0.0, 0.66, 0.286, 3.2), (0.10, 0.65, 0.288, 3.1),
        (0.20, 0.62, 0.288, 3.0), (0.30, 0.55, 0.286, 2.9), (0.42, 0.40, 0.282, 2.8), (0.52, 0.325, 0.278, 2.7),
        (0.62, 0.272, 0.274, 2.7), (0.75, 0.240, 0.266, 2.6), (0.88, 0.226, 0.250, 2.5), (0.955, 0.218, 0.230, 2.5)]
HW_TAB = [(r[0], r[2]) for r in ROWS]
TREAD_K = 0.58                          # tread strip half width = this x the boot half width (it hides under the rounding)


def boot_hwH(fH):
    return interp(HW_TAB, fH)


def sole_hwH(fH):
    if fH < -0.20:
        u = min(0.985, (-0.20 - fH) / (-0.20 - F_REAR))
        return TREAD_K * 0.262 * (1.0 - u ** 2.2) ** (1 / 2.2)
    if fH > 0.955:
        u = min(0.985, (fH - 0.955) / (F_TIP - 0.955))
        return TREAD_K * 0.230 * (1.0 - u ** 3.0) ** (1 / 3.0)
    return TREAD_K * boot_hwH(fH)


def spring(f):
    d = f - TOE_PIVOT_F
    return d * math.tan(TOE_SPRING) if d > 0 else 0.0


def sole_slab(name, f0, f1, nu=24, nv=10):
    def fn(u, v):
        fH = f0 + (f1 - f0) * u
        f = h(fH)
        x = h(sole_hwH(fH)) * (2 * v - 1)
        return P(x, f, SOLE_T + spring(f))
    return L.grid_surface(name, fn, nu, nv, thickness=SOLE_T, offset=-1.0)


class Skin:
    """Superellipse sweep along the foot (path runs forward).  rows = (f_H, top_H, hw_H); the section spans from the path
    (sole top) up to `top`, so the bottom stays flat on the sole and the toe spring is baked into the path."""

    def __init__(self, rows, nexp=3.2, spring_on=True):
        pts = []
        for row in rows:
            fm = h(row[0])
            pts.append(P(0, fm, SOLE_T - 0.0015 + (spring(fm) if spring_on else 0.0)))
        acc = [0.0]
        for a, b in zip(pts[:-1], pts[1:]):
            acc.append(acc[-1] + (b - a).length)
        tot = acc[-1]
        keys = []
        for row, a in zip(rows, acc):
            f, top, hw = row[:3]
            hg = max(h(top) - SOLE_T + 0.0015, 0.004)
            keys.append({"t": a / tot, "rx": h(hw), "ry": hg / 2, "oy": hg / 2, "n": row[3] if len(row) > 3 else nexp})
        self.fs = [h(r[0]) for r in rows]
        self.ts = [a / tot for a in acc]
        self.sw = L.Sweep(L.Path(pts), keys, front=(0, 0, 1), side=(1, 0, 0))

    def t_of(self, f):
        return min(1.0, max(0.0, interp(list(zip(self.fs, self.ts)), f, smooth=False)))

    def pt(self, fH, th, off=0.0):
        return self.sw.point(self.t_of(h(fH)), th, off)

    def nrm(self, fH, th):
        return self.sw.outward(self.t_of(h(fH)), th)


def gold_line(sk, fa, fb, th, r, off=0.0007, n=18, name="gl", endfade=True):
    """thin round gold strip following the skin at angle th between fa and fb (H); radius tapers to nothing at both ends"""
    pts = [sk.pt(fa + (fb - fa) * i / (n - 1), th, off) for i in range(n)]
    rad = (lambda t: r * max(0.12, math.sin(PI * t) ** 0.45)) if endfade else r
    return L.tube(name, pts, rad, nring=8)


def window_loop(sk, fa, fb, a0, a1, off, n=14):
    """closed-ish rectangle loop of points around the (f, theta) window on skin sk"""
    pts = []
    for i in range(n):
        pts.append(sk.pt(fa + (fb - fa) * i / (n - 1), a0, off))
    for i in range(1, n):
        pts.append(sk.pt(fb, a0 + (a1 - a0) * i / (n - 1), off))
    for i in range(1, n):
        pts.append(sk.pt(fb - (fb - fa) * i / (n - 1), a1, off))
    for i in range(1, n):
        pts.append(sk.pt(fa, a1 - (a1 - a0) * i / (n - 1), off))
    pts.append(sk.pt(fa, a0, off))
    return pts


def build():
    reg = Reg()
    FB, TB = "foot.L", "toes.L"
    CF = CUT_F / H

    # ------------------------------------------------------------------ the swept upper (split at the flex line); its own rounded underside IS the sole
    up = Skin(ROWS, nexp=3.2)
    whole = sweep_mesh_centered(up.sw, "upper_whole", nring=56, nstations=44, round_start=(h(0.04), 3), round_end=(h(0.085), 6))
    toe_up, foot_up = split_at_plane(whole, Vector((AX, -CUT_F, 0.0)), Vector((0, -1, 0)), ("upper_toe", "upper_foot"))
    reg.add(foot_up, "upper", "teal", FB, bevel=0.0016, seg=2, wear=1.0)
    reg.add(toe_up, "toe_cap", "teal", TB, bevel=0.0016, seg=2, wear=1.0)
    sw = up.sw
    IN_F0, IN_F1 = 0.290, 0.560

    # ------------------------------------------------------------------ silver-gold piping only (no lames, no plates): welt, crest pair, toe rim
    welt_r = 0.0020
    for sgn, nm in ((1, "out"), (-1, "in")):
        th = -0.52 if sgn > 0 else PI + 0.52
        pts = [up.pt(-0.16 + (CF - 0.004 + 0.16) * i / 22, th, 0.0004) for i in range(23)]
        reg.add(L.tube("weltp", pts, welt_r, nring=8, round_ends=True), f"welt_pipe_{nm}", "gold", FB, bevel=0, wear=None)
    tubes = []
    for sgn in (1, -1):
        th = -0.52 if sgn > 0 else PI + 0.52
        pts = [up.pt(CF + 0.01 + (0.90 - CF - 0.01) * i / 9, th, 0.0004) for i in range(10)]
        tubes.append(L.tube("toewelt", pts, welt_r, nring=8, round_ends=True))
    reg.add(join_named(tubes, "toe_welt"), "toe_welt_pipe", "gold", TB, bevel=0, wear=None)
    # crest: the gold centre line of the shin continues down the swept boot, a hair of silver pipe beside it each side
    reg.add(gold_line(up, 0.04, 0.60, PI / 2, 0.0021, off=0.0004, n=26, name="crest"), "crest_line", "gold", FB, bevel=0, wear=None)
    for th, nm in ((PI / 2 - 0.16, "out"), (PI / 2 + 0.16, "in")):
        reg.add(gold_line(up, 0.10, 0.52, th, 0.0011, off=0.0003, n=22, name="crestpipe"), f"crest_silver_pipe_{nm}", "silver", FB, bevel=0, wear=None)
    # toe flex seam: a hairline dark core ring only (sits on the toes bone)
    tc = up.t_of(CUT_F)
    ring_d = [sw.point(tc, 2 * PI * k / 72, -0.0006) for k in range(73)]
    reg.add(L.tube("seamcore", ring_d, 0.0017, nring=8, n_per_seg=2), "flex_seam_core", "dark", TB, bevel=0, wear=None)
    # hairline flank seams (soft panel lines, flush)
    for sgn, nm in ((1, "out"), (-1, "in")):
        th = 0.55 if sgn > 0 else PI - 0.55
        pts = [up.pt(0.12 + (CF - 0.05 - 0.12) * i / 16, th, -0.0004) for i in range(17)]
        reg.add(L.tube("hair", pts, 0.0009, nring=6, round_ends=True), f"flank_hairline_{nm}", "dark", FB, bevel=0, wear=None)

    # ------------------------------------------------------------------ near-black wedge heel (scooped arch) + heel cap plate
    hrows = [(-0.425, 0.26, 0.150), (-0.385, 0.38, 0.196), (-0.33, 0.45, 0.226), (-0.25, 0.50, 0.246), (-0.12, 0.48, 0.256),
             (-0.06, 0.34, 0.244), (0.00, 0.20, 0.200)]
    hk = Skin(hrows, nexp=3.4, spring_on=False)
    heel = sweep_mesh_centered(hk.sw, "heel_wedge", nring=64, nstations=26, round_start=(h(0.07), 4))
    cut = L.cylinder("notch", h(ARCH_R), 0.34, L.Frame.at(P(0, h(ARCH_F), SOLE_T), (1, 0, 0), (0, 0, 1)), segments=48)
    L.boolean_cut(heel, cut)
    reg.add(heel, "heel_wedge", "gunmetal", FB, bevel=0.0026, seg=3, wear=0)
    cap = hk.sw.panel("heel_cap", hk.t_of(h(-0.395)), hk.t_of(h(-0.29)), 0.95, PI - 0.95, thickness=0.0026, inflate=0.0012,
                      height=0.0018, hp=1.0, ends=0.14, nu=14, nv=14)
    reg.add(cap, "heel_cap_plate", "gunmetal", FB, bevel=0.0014, seg=2, wear=0)
    hg = L.tube("hg", window_loop(hk, -0.415, -0.275, 0.55 - 0.085, PI - 0.55 + 0.085, 0.0002, n=12), 0.0011, nring=8)
    reg.add(hg, "heel_gap_core", "dark", FB, bevel=0, wear=None)

    # ------------------------------------------------------------------ ankle hinge: low-relief clevis + bearing disc, dull olive, NO screws
    HF = -0.33
    D.ankle_hinge(reg, hk, HF, +1, FB, full=True)
    D.ankle_hinge(reg, hk, HF, -1, FB, full=False)

    # ------------------------------------------------------------------ hoses with clamps into the heel
    D.hoses(reg, hk, FB)
    D.heel_detail(reg, hk, up, FB)

    return reg.mirror_all()
