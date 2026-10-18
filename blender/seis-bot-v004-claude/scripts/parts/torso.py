"""torso - SEIS bot CHEST + TORSO CORE, ON-MODEL conform round 1 (spec/ONMODEL.md, Bear's 12 video frames).
Front: two glossy TEAL shield plates (pair 0.51 m, each 0.16 m tall) on a vertical spine channel, a broad flat olive-bronze
arch band per side, stepped teal tail tiles, three flat olive-bronze rib blades per side over a red cavity, a spine column
(6 on a black slot, teal blocks, bronze bar, eye recess + knob, lumbar tabs) and a slim 1.0 H waist with four red ab pods per
side between a pewter strut and a dark strut.  The back keeps the still-based layout (recoloured, no wear).
Built in world coordinates of the standing A-pose figure.  Design numbers are METRES unless a name ends in _H (head-heights,
H = 0.2554 m); see parts/torso_kit.py for the chest shell they sit on.
Bones: chest = plates, arches, blades, upper spine, back shell;  abdomen = pods, struts, lower spine, lumbar tabs, belt plug.
"""
import math
import os
import bpy
import bmesh
from mathutils import Vector, Matrix
import seis_lib as L
import seis_spec as S
import torso_kit as K
import torso_hw as HW
from torso_kit import H, sp, spb, nrm, nrm_b, fy, by, rx, frame_f, frame_b

OUT = []


def fin(ob, mat, bone="chest", bevel=0.0018, seg=2, wear=0.0, mirror=False, **kw):
    """wear = GOLD TRIM strength on teal (0 = no gold line, groove + glint only)."""
    L.finish(ob, mat, bevel=bevel, bevel_segments=seg, bone=bone, wear=wear, **kw)
    OUT.append(ob)
    if mirror:
        OUT.append(L.mirror_x(ob))
    return ob


def spm(xm, zm, lift=0.0):
    """world point (m) on the front shell at metres (xm, zm), pushed `lift` m along the shell normal."""
    return sp(xm / H, zm / H, lift / H)


def frm(xm, zm, lift=0.0, ang=0.0):
    return frame_f(xm / H, zm / H, lift / H, ang=ang)


def smooth01(a, b, x):
    return L.smoothstep(a, b, x)


def site(xm, zm, lift=0.0):
    """(world point, outward unit normal) on the front shell at metres (xm, zm), pushed `lift` m out."""
    return spm(xm, zm, lift), nrm(xm / H, zm / H)


def densify(pts, n=8):
    """linear resample of a sparse [(x, z)] path (any units) to n+1 points per segment so a spline through it stays ON the shell"""
    out = []
    for i in range(len(pts) - 1):
        for k in range(n):
            f = k / n
            out.append((pts[i][0] + (pts[i + 1][0] - pts[i][0]) * f, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * f))
    out.append(pts[-1])
    return out


def sfx(mirror):
    return ".L" if mirror else ""


def hexb(nm, p, n, r=0.0028, mat="silver", bone="chest", mirror=True, h=0.0022, wash=True):
    """washer + hex bolt, joined into ONE object, standing on a surface at p with outward normal n"""
    p = Vector(p)
    n = Vector(n)
    parts = []
    if wash:
        parts.append(HW.washer(nm + "_w", p, n, r * 1.55, 0.0008))
        p = p + n * 0.0008
    parts.append(HW.hexbolt(nm + "_b", p, n, r, h))
    ob = L.join(parts, nm + sfx(mirror))
    fin(ob, mat, bone=bone, bevel=0.0003, seg=1, mirror=mirror)


def rivet(nm, p, n, r=0.0021, mat="silver", bone="chest", mirror=True):
    ob = HW.rivet(nm + sfx(mirror), Vector(p), Vector(n), r)
    fin(ob, mat, bone=bone, bevel=0.0, seg=1, mirror=mirror)


# ============================================================================================ core and cavity
CORE = {}
CZ0, CZ1 = 5.02, 6.99
CORE_RX = [(5.0, .565), (5.3, .485), (5.6, .465), (5.85, .545), (6.10, .765), (6.35, .895), (6.64, 1.00), (6.80, .80),
           (6.99, .52)]


def core_rx(z):
    return K.tab_interp(CORE_RX, z)


def tz(z):
    """core sweep parameter of height z (H)"""
    return (z - CZ0) / (CZ1 - CZ0)


def core():
    z0, z1 = CZ0, CZ1
    nst = 16
    keys = []
    for i in range(nst + 1):
        t = i / nst
        z = z0 + (z1 - z0) * t
        top = 1.0 - 0.30 * L.smoothstep(6.80, 6.99, z)
        keys.append({"t": t, "rxp": core_rx(z) * H * top, "rxn": core_rx(z) * H * top,
                     "ryp": (K.ryf(z) - 0.035) * H * top,
                     "ryn": (K.ryb(z) - 0.03) * H * top, "n": K.NEXP})
    path = [Vector((0, K.YC * H, z0 * H)), Vector((0, K.YC * H, (z0 + z1) / 2 * H)), Vector((0, K.YC * H, z1 * H))]
    sw = L.Sweep(path, keys)
    CORE["sw"] = sw
    ob = sw.mesh("torso_core", nring=72, nstations=44, caps=True)
    fin(ob, "darkdisc", bone="chest", bevel=0, seg=1)
    # dark neck plug: runs 0.06 H up into the neck (the head builder's neck sits over it)
    nk = L.Sweep([Vector((0, 0.05 * H, 6.78 * H)), Vector((0, 0.05 * H, 7.0 * H))],
                 [(0, 0.31 * H, 0.28 * H, 2.4), (1, 0.30 * H, 0.27 * H, 2.4)])
    pl = nk.mesh("torso_neck_plug", nring=32, nstations=4, caps=True)
    fin(pl, "dark", bone="chest", bevel=0, seg=1)
    return ob


def win(zc, zh, ac, aw, p=2.6):
    """lens/rounded-end window for Sweep.panel: returns (z0, z1, a0(t), a1(t)) with the angular half-width aw (deg)
    falling to 0 at both ends like a superellipse, so back plates get rounded ends instead of square cuts."""
    def w(t):
        z = CZ0 + t * (CZ1 - CZ0)
        u = min(1.0, abs(z - zc) / zh)
        return aw * (1.0 - u ** p) ** (1.0 / p)

    return (zc - zh, zc + zh, (lambda t: math.radians(ac - w(t))), (lambda t: math.radians(ac + w(t))))


def red_cavity():
    """The deep crimson guts behind everything (f07, f08, f04): ONE satin dark-red skin wrapping the front and both flanks of
    the core (z 1.38-1.62 m), so every gap between arch, blades, tiles, spine blocks and pods shows shaded crimson, never a
    black field or glossy cherry.  A second, higher-gloss red lens sits in the open rib cage behind the blades."""
    sw = CORE["sw"]
    zc, zh, pw = 5.70, 0.66, 5.0
    z0, z1 = zc - zh, zc + zh

    def wfun(t):
        z = CZ0 + t * (CZ1 - CZ0)
        u = min(1.0, abs(z - zc) / zh)
        return max(14.0, 91.0 * (1.0 - u ** pw) ** (1.0 / pw))

    ob = sw.panel("torso_cavity_skin.L", tz(z0), tz(z1), lambda t: math.radians(93.0 - wfun(t)), math.radians(93.0),
                  thickness=0.004, inflate=0.008 * H, height=0.016 * H, hp=1.0, ends=0.15, nu=26, nv=30)
    fin(ob, HW.redshade(), bone="abdomen", bevel=0.0010, seg=1, mirror=True)
    # open rib cage: a glossier red lens on the flank, seen between the blades and from the side (f10)
    z0, z1, f0, f1 = win(5.84, 0.34, 18, 24, 2.0)
    ob = sw.panel("torso_flank_mass.L", tz(z0), tz(z1), f0, f1, thickness=0.004, inflate=0.016 * H, height=0.026 * H,
                  hp=1.0, ends=0.2, nu=22, nv=20)
    fin(ob, "red", bone="chest", bevel=0.0010, seg=2, mirror=True)


def flank_wall():
    """dark teal back wall on the upper flank, flush behind the pauldron horn and tucked under the chest-plate end (critic cross 2:
    no black socket + red patch between horn lip and plate)."""
    z0, z1, f0, f1 = win(6.40, 0.32, 28, 30, 2.4)
    ob = CORE["sw"].panel("torso_flank_wall.L", tz(z0), tz(z1), f0, f1, thickness=0.004, inflate=0.012 * H, height=0.020 * H, hp=1.0,
                          ends=0.2, nu=20, nv=20)
    fin(ob, "teal", bone="chest", bevel=0.0012, seg=2, wear=0.0, mirror=True)


def yoke():
    """Collar yoke: two overlapping dark-teal shells on the shoulder-top of the core between the neck and the pauldron hubs
    (f08: the area above the chest plates is glossy dark shell, not a flat black dome), each with a gunmetal seam slab under
    it, a stepped bearing ring around the neck base and four washered bolts on each shell."""
    sw = CORE["sw"]
    zc, zh = 6.84, 0.17
    z0, z1, f0, f1 = win(zc, zh, 70, 52, 2.6)
    base = sw.panel("torso_yoke_seam.L", tz(z0 - 0.02), tz(z1 + 0.02), f0, f1, thickness=0.004, inflate=0.0035 * H,
                    height=0.014 * H, hp=1.0, ends=0.2, nu=18, nv=22)
    fin(base, "dark", bone="chest", bevel=0.0006, seg=1, mirror=True)
    z0, z1, f0, f1 = win(zc, zh - 0.02, 70, 48, 2.6)
    ob = sw.panel("torso_yoke_plate.L", tz(z0), tz(z1), f0, f1, thickness=0.005, inflate=0.0075 * H, height=0.020 * H, hp=1.0,
                  ends=0.2, nu=24, nv=24)
    fin(ob, "teal", bone="chest", bevel=0.0013, seg=2, wear=0.0, mirror=True)
    # dark seam line along the lower edge of each yoke shell
    pts = [sw.point(tz(zc - zh + 0.05), math.radians(24 + 92 * k / 6.0), 0.0075 * H + 0.010 * H) for k in range(7)]
    sl = L.tube("torso_yoke_seam_line.L", pts, 0.0014, nring=5, n_per_seg=3, round_ends=True)
    fin(sl, "dark", bone="chest", bevel=0, seg=1, mirror=True)
    # neck bearing ring (stepped) around the neck base
    rg = HW.ring_stack("torso_neck_bearing", (0, 0.05 * H, 1.742), (0, 0, 1),
                       [(0.0905, 0.0030), (0.0845, 0.0058), (0.0780, 0.0082)], segments=48)
    fin(rg, "gunmetal", bone="chest", bevel=0.0005, seg=1)
    rg2 = HW.ring_stack("torso_neck_bearing_outer", (0, 0.05 * H, 1.738), (0, 0, 1), [(0.0995, 0.0020), (0.0955, 0.0036)],
                        segments=48)
    fin(rg2, "dark", bone="chest", bevel=0.0004, seg=1)


# ============================================================================================ teal shield plates
# arch centre line, metres (f08 2x crop measured against the 0.299 m crown-to-yoke scale); z descending
ARCH_M = [(0.285, 1.712), (0.275, 1.698), (0.235, 1.660), (0.186, 1.629), (0.147, 1.594), (0.111, 1.545), (0.084, 1.492),
          (0.062, 1.438), (0.047, 1.385), (0.040, 1.358)]
_ARCH_T = sorted([(z, x) for (x, z) in ARCH_M])


def arch_x(zm):
    """x (m) of the arch centre line at height zm (smooth Hermite through ARCH_M, clamped)."""
    return K.tab_interp(_ARCH_T, zm)


ZT, ZB, XI = 1.705, 1.543, 0.036        # plate top (0.11 m below the yoke bottom 1.82), point (0.27 m below), inner edge
ARCH_HW = 0.0145                          # arch band half width (0.029 m wide at the hub; spec 0.021, widened to read like f08)
RISE = 0.0095


def plate_geom(u, v, m):
    zt, zb = ZT - m + 0.0035 * math.sin(math.pi * v) ** 0.9, ZB + m + 0.012 * v     # top edge slightly convex; bottom rises outward
    z = zt - (zt - zb) * u
    xo = arch_x(z) - ARCH_HW - 0.002 - m
    xi = XI + m
    return xo + (xi - xo) * v, z, xo - xi, zt, zb


def plate_lift(u, v, m=0.0):
    x, z, width, zt, zb = plate_geom(u, v, m)
    d = min(min(v, 1 - v) * max(width, 0.0), (zt - z), (z - zb) * 0.8)
    return 0.003 + RISE * (smooth01(0.0, 0.030, d) ** 0.6)


def plate_lift_xz(xm, zm):
    """approximate surface lift of the plate pillow at metres (xm, zm) (to seat grooves)."""
    zt, zb = ZT - 0.004, ZB + 0.004
    u = (zt - zm) / (zt - zb)
    u = min(1, max(0, u))
    xo = arch_x(zm) - ARCH_HW - 0.002 - 0.004
    xi = XI + 0.004
    v = min(1, max(0, (xm - xo) / (xi - xo))) if xo > xi else 0.5
    return plate_lift(u, v, 0.004)


def shield_plates():
    # black groove slab under the shield
    def f_base(u, v):
        x, z, *_ = plate_geom(u, v, 0.0)
        return tuple(spm(x, z, 0.0025))

    base = K.orient_grid("torso_plate_base.L", f_base, 30, 12, 0.006, (0, -1, 0))
    fin(base, "dark", bevel=0.0010, seg=1, mirror=True)

    def f_teal(u, v):
        x, z, *_ = plate_geom(u, v, 0.004)
        return tuple(spm(x, z, plate_lift(u, v, 0.004)))

    pl = K.orient_grid("torso_chest_plate.L", f_teal, 40, 22, 0.006, (0, -1, 0))
    fin(pl, "teal", bevel=0.0013, seg=2, wear=0.0, mirror=True)


def plate_edge_glint():
    """thin pewter glint line along the top edge of each plate (f07: black groove + 1-3 px white bevel glint, not gold)"""
    pts = []
    for k in range(10):
        v = 0.04 + 0.92 * k / 9.0
        x, z, *_ = plate_geom(0.0, v, 0.0045)
        pts.append(spm(x, z, plate_lift_xz(x, z) + 0.0004))
    g = L.tube("torso_plate_glint.L", pts, 0.0010, nring=5, n_per_seg=2, round_ends=True)
    fin(g, "silver", bevel=0, seg=1, mirror=True)


def plate_groove():
    """the near-black groove that outlines each shield on its outer (arch) side and along its bottom point (f07, f08)"""
    pts = []
    for k in range(11):
        x, z, *_ = plate_geom(k / 10.0, 0.0, 0.0035)
        pts.append(spm(x, z, 0.0030))
    for k in range(1, 11):
        x, z, *_ = plate_geom(1.0, k / 10.0, 0.0035)
        pts.append(spm(x, z, 0.0030))
    g = L.tube("torso_plate_groove.L", pts, 0.0020, nring=6, n_per_seg=2, round_ends=True)
    fin(g, "dark", bevel=0, seg=1, mirror=True)


def plate_hardware():
    """thin champagne-gold hairline along the inner (spine) edge of each plate + 4 washered hex bolts at the plate corners"""
    pts = []
    for k in range(9):
        u = k / 8.0
        x, z, *_ = plate_geom(u, 1.0, 0.0035)
        pts.append(spm(x, z, plate_lift_xz(x, z) - 0.0004))
    g = L.tube("torso_plate_trim.L", pts, 0.0019, nring=6, n_per_seg=2, round_ends=True)
    fin(g, "gold", bevel=0, seg=1, mirror=True)


def plate_fluting():
    """5-6 slanted dark grooves across the top-outer corner of each plate (f07, f08), teal-silver faces between."""
    x0, pitch = 0.150, 0.0175
    flutes = []
    for i in range(6):
        xt = x0 + pitch * i
        zt = ZT - 0.0045
        xe = xt - 0.030
        ze = ZT - 0.060
        # keep the groove on the plate: stop short of the arch band
        xmax = arch_x(ze) - ARCH_HW - 0.010
        xe = min(xe, xmax)
        xt = min(xt, arch_x(zt) - ARCH_HW - 0.010)
        pts = []
        for k in range(7):
            f = k / 6.0
            x = xt + (xe - xt) * f
            z = zt + (ze - zt) * f
            pts.append(spm(x, z, plate_lift_xz(x, z) - 0.0006))
        flutes.append(L.tube(f"torso_flute_{i}.L", pts, 0.0025, nring=6, n_per_seg=2, round_ends=True))
    for fl in flutes:
        fin(fl, "dark", bevel=0, seg=1, mirror=True)


def tail_tiles():
    """4 stepped teal parallelogram tiles down the arch's inner side to the spine (f07, f08, f04), each on a black seam slab,
    each held by one small rivet."""
    rows = [(1.527, 0.033), (1.489, 0.033), (1.451, 0.033), (1.413, 0.031)]
    for i, (zc, h_) in enumerate(rows):
        inner = 0.041
        outer = arch_x(zc) - ARCH_HW - 0.003
        w = max(0.014, outer - inner)
        cx = inner + w / 2
        s_ = 0.012
        outline = [(-w / 2, -h_ / 2), (w / 2, -h_ / 2 + s_), (w / 2, h_ / 2 + s_), (-w / 2, h_ / 2)]
        fr = frm(cx, zc, 0.0025)
        slab = K.pillow(f"torso_tail_base_{i}.L", [(x * 1.12, y * 1.12) for x, y in outline], fr, rise=0.0, thickness=0.006)
        fin(slab, "dark", bevel=0.0008, seg=1, mirror=True)
        fr2 = frm(cx, zc, 0.0035)
        t = K.pillow(f"torso_tail_tile_{i}.L", outline, fr2, rise=0.0040, thickness=0.004, steps=4)
        fin(t, "teal", bevel=0.0012, seg=2, wear=1.0, mirror=True)
        # light edge line along the upper edge of each tile (f07: pale line, not gold)
        ea = fr2.p(-w / 2 + 0.002, h_ / 2 - 0.001, 0.0040 + 0.0006)
        eb = fr2.p(w / 2 - 0.002, h_ / 2 + s_ - 0.001, 0.0040 + 0.0006)
        el = L.tube(f"torso_tail_line_{i}.L", [ea, eb], 0.0009, nring=5, n_per_seg=2, round_ends=True)
        fin(el, "silver", bevel=0, seg=1, mirror=True)


# ============================================================================================ arch band, crescent
def offset_path(pts, d):
    """pts [(x, z)] metres; returns the path pushed `d` m sideways (perpendicular, towards +x/+z when d > 0)."""
    out = []
    for i in range(len(pts)):
        x0, z0 = pts[max(0, i - 1)]
        x1, z1 = pts[min(len(pts) - 1, i + 1)]
        dx, dz = x1 - x0, z1 - z0
        ln = math.hypot(dx, dz)
        nx, nz = -dz / ln, dx / ln
        if nx < 0:
            nx, nz = -nx, -nz
        out.append((pts[i][0] + nx * d, pts[i][1] + nz * d))
    return out


def arches():
    """ONE broad flat olive-bronze band (0.0256 m at the hub tapering to 0.0206 m; spec 0.021 wide, widened a little so it reads like
    f08) with a dark seam ribbon either side, hugging the hub from above and sweeping down and in to the spine 0.43 m below the
    chin (f07, f08); a hinge plate + stepped bearing ring + pin at the outer end, a foot plate at the spine end, 5 washered bolts
    along the band; plus a second ribbed crescent of 6 ticks over the hub."""
    pts = [(x / H, z / H) for (x, z) in ARCH_M]
    hwf = lambda t: (ARCH_HW - 0.0030 * t) / H
    ob, sw = K.sweep_on_shell("torso_arch.L", pts, hwf, 0.0062 / H, n=5.0, embed=0.30, nring=20, lift=0.002 / H)
    fin(ob, HW.olive(), bevel=0.0013, seg=2, mirror=True)
    # bright champagne UPPER edge only (f07/f08: cream upper edge, dark olive face): a thin gold ribbon along the outer lip
    pe = offset_path(ARCH_M, ARCH_HW - 0.0012)
    ge, _ = K.sweep_on_shell("torso_arch_edge.L", [(x / H, z / H) for (x, z) in pe], 0.0017 / H, 0.0034 / H, n=3.0,
                             embed=0.30, nring=8, lift=0.0042 / H)
    fin(ge, "gold", bevel=0, seg=1, mirror=True)
    # dark seam ribbons: real gaps with a dark core either side of the band
    for k, sgn in enumerate((1, -1)):
        pp = offset_path(ARCH_M, sgn * (ARCH_HW + 0.0016))
        sm, _ = K.sweep_on_shell(f"torso_arch_seam_{k}.L", [(x / H, z / H) for (x, z) in pp], 0.0022 / H, 0.0030 / H, n=3.0,
                                 embed=0.30, nring=10, lift=0.0004 / H)
        fin(sm, "dark", bevel=0, seg=1, mirror=True)
    # second ribbed crescent: a narrower band outboard of the arch over the hub, with 6 transverse ticks
    off = 0.026
    cp = []
    for i in range(6):
        x, z = ARCH_M[i]
        x0, z0 = ARCH_M[max(0, i - 1)]
        x1, z1 = ARCH_M[min(len(ARCH_M) - 1, i + 1)]
        dx, dz = x1 - x0, z1 - z0
        ln = math.hypot(dx, dz)
        nx, nz = -dz / ln, dx / ln
        if nx < 0:
            nx, nz = -nx, -nz
        cp.append(((x + nx * off) / H, (z + nz * off) / H))
    c2, _ = K.sweep_on_shell("torso_crescent.L", cp, 0.0075 / H, 0.0040 / H, n=4.0, embed=0.25, nring=14, lift=0.002 / H)
    fin(c2, "teal", bevel=0.0010, seg=2, wear=0.0, mirror=True)
    ticks = []
    for k in range(6):
        t = (k + 0.5) / 6.0
        i = min(len(cp) - 2, int(t * (len(cp) - 1)))
        f = t * (len(cp) - 1) - i
        px = (cp[i][0] + (cp[i + 1][0] - cp[i][0]) * f)
        pz = (cp[i][1] + (cp[i + 1][1] - cp[i][1]) * f)
        a_ = sp(px - 0.026, pz - 0.0, 0.0085 / H)
        b_ = sp(px + 0.026, pz + 0.0, 0.0085 / H)
        ticks.append(L.tube(f"torso_tick_{k}.L", [a_, b_], 0.0013, nring=5, n_per_seg=2))
    for tk in ticks:
        fin(tk, "dark", bevel=0, seg=1, mirror=True)
    return sw


def arch_hardware(sw):
    """hinge assembly at the hub end only (plate + stepped bearing ring + pin head); the dotted bolt row and the grey foot clip are
    gone (critic torso 2: the frames show a smooth band)."""
    t = 0.045
    p = sw.point(t, math.pi / 2, 0.0)
    n = sw.outward(t, math.pi / 2)
    hp_ = HW.clevis_plate("torso_arch_hinge_plate.L", p, n, 0.026, 0.026, 0.0018, roundr=0.007)
    fin(hp_, "gunmetal", bone="chest", bevel=0.0006, seg=1, mirror=True)
    pb = p + n * 0.0018
    rg = HW.ring_stack("torso_arch_bearing.L", pb, n, [(0.0105, 0.0016), (0.0078, 0.0030), (0.0048, 0.0042)], segments=28)
    fin(rg, "gunmetal", bone="chest", bevel=0.0004, seg=1, mirror=True)
    pn = HW.pin("torso_arch_pin.L", pb + n * 0.0044, n, 0.0022, 0.0014)
    fin(pn, "dark", bone="chest", bevel=0.0002, seg=1, mirror=True)


# ============================================================================================ rib blades
BLADES = [
    # (x m, z m, lift m) control points: the root is tucked behind the shell under the arch; the blade runs diagonally down and
    # OUT (0.10 m outward, 0.15 m down: f07/f08 blades end level with the top of the ab pods, z ~1.41), bows, and the tip hooks
    # back INWARD.  Three nested, successively lower blades.
    [(0.108, 1.574, -0.014), (0.132, 1.560, -0.002), (0.164, 1.534, 0.012), (0.192, 1.498, 0.024), (0.206, 1.462, 0.030),
     (0.207, 1.436, 0.032), (0.198, 1.418, 0.030), (0.184, 1.409, 0.026)],
    [(0.102, 1.550, -0.014), (0.126, 1.536, -0.002), (0.157, 1.510, 0.012), (0.184, 1.474, 0.024), (0.198, 1.438, 0.030),
     (0.199, 1.412, 0.032), (0.190, 1.394, 0.030), (0.176, 1.385, 0.026)],
    [(0.096, 1.526, -0.014), (0.120, 1.512, -0.002), (0.150, 1.486, 0.012), (0.176, 1.450, 0.024), (0.190, 1.414, 0.030),
     (0.191, 1.388, 0.032), (0.182, 1.370, 0.030), (0.168, 1.361, 0.026)],
]


def blade_pt(x, z, lift):
    xc = min(x / H, 0.88 * rx(z / H))
    y = fy(xc, z / H) * H + 0.55 * max(0.0, x - xc * H) - lift
    return Vector((x, y, z))


def rib_blades():
    """3 flat bowed olive-bronze blades per side, each a 0.034 m wide, 0.006 m thick ribbon with a 0.004 m champagne edge strip,
    running down and out then hooking inward with a pink-red hook cap (f07 rib-loops crop, f08)."""
    for k, ctrl in enumerate(BLADES):
        pts = [blade_pt(x, z, lf) for (x, z, lf) in ctrl]
        dense = L.catmull(pts, n_per_seg=9)
        ups = []
        for p in dense:
            xc = min(p.x / H, 0.88 * rx(p.z / H))
            nn = nrm(xc, p.z / H)
            lam = L.smoothstep(0.10, 0.205, abs(p.x))
            u = (nn * (0.55 - 0.25 * lam) + Vector((0, -1, 0)) * (0.45 - 0.25 * lam) + Vector((1 if p.x > 0 else -1, 0, 0)) * 0.95 * lam).normalized()
            ups.append(u)
        nd = len(dense)
        wfun = lambda f: 0.0172 * (0.55 + 0.45 * math.sin(math.pi * min(1.0, 0.04 + f * 0.96)) ** 0.5) * (1.0 - 0.18 * f ** 3)
        ob = K.ring_mesh(f"torso_blade_{k}.L", dense, ups, wfun, 0.0032, n_sec=14, sec_n=4.0, closed=False)
        fin(ob, HW.olive(), bevel=0.0010, seg=2, mirror=True)
        # champagne edge strip along the upper edge of the blade
        ep = []
        for i, p in enumerate(dense):
            T = (dense[min(nd - 1, i + 1)] - dense[max(0, i - 1)]).normalized()
            U = (ups[i] - T * ups[i].dot(T)).normalized()
            lat = T.cross(U).normalized()
            if lat.dot(Vector((0.5, 0, 0.8))) < 0:
                lat = -lat
            f = i / max(1, nd - 1)
            ep.append(p + lat * (wfun(f) - 0.0008) + U * 0.0018)
        ed = K.ring_mesh(f"torso_blade_edge_{k}.L", ep, ups, 0.0020, 0.0014, n_sec=8, sec_n=3.0, closed=False)
        fin(ed, "gold", bevel=0, seg=1, mirror=True)
        # pink-red hook cap
        tip = L.sphere(f"torso_blade_tip_{k}.L", 0.0040, L.Frame(dense[-1]), scale=(1.1, 1.0, 1.0), segments=12, rings=8)
        fin(tip, "red", bevel=0, seg=1, mirror=True)
        # small pink-red hook curling inward past the blade tip (f07 rib-loops crop)
        ip = Vector((-0.011, -0.003, -0.0045))
        hk = L.tube(f"torso_blade_hook_{k}.L", [dense[-4], dense[-2], dense[-1], dense[-1] + ip], 0.0030, nring=8,
                    n_per_seg=4, round_ends=True)
        fin(hk, "red", bevel=0, seg=1, mirror=True)


def rib_guts():
    """f07/f08: the cavity under the arch is full of dark-red organic rolls, not cables.  Two satin crimson rolls per side run down
    the flank behind the blades (replacing the hose/clamp pairs)."""
    runs = [("roll_a", 0.0105, [(0.138, 1.500), (0.152, 1.470), (0.152, 1.440), (0.138, 1.412)]),
            ("roll_b", 0.0085, [(0.122, 1.488), (0.134, 1.462), (0.132, 1.434), (0.118, 1.410)]),
            ("roll_c", 0.0090, [(0.150, 1.520), (0.166, 1.488), (0.168, 1.452), (0.156, 1.424)]),
            ("roll_d", 0.0070, [(0.110, 1.472), (0.121, 1.446), (0.120, 1.420), (0.108, 1.402)])]
    for j, (nm, r, xz) in enumerate(runs):
        pts = [spm(x, z, 0.0070 + 0.0030 * j) for (x, z) in xz]
        tb = L.tube(f"torso_{nm}.L", pts, r, nring=10, n_per_seg=6, round_ends=True)
        fin(tb, HW.redshade(), bone="chest", bevel=0, seg=1, mirror=True)


# ============================================================================================ spine column
SBLK = (1.5135, 1.4855, 1.4575)


def spine():
    # red channel the 6 stands in, visible either side of the black slot (f07 crop 12)
    fr = frm(0.0, 1.5765, 0.0010)
    red = K.pillow("torso_slot_red", K.rr(0.064 / H, 0.093 / H, 0.004), fr, rise=0.0, thickness=0.004)
    fin(red, "red", bevel=0.0006, seg=1)
    # black slot 0.051 x 0.093 m
    fr = frm(0.0, 1.5765, 0.0030)
    slot = K.pillow("torso_slot", K.rr(0.051 / H, 0.093 / H, 0.012), fr, rise=0.0006, thickness=0.004)
    fin(slot, "dark", bevel=0.0007, seg=1)
    # pale slot bar and pale-teal block above the 6
    fr = frm(0.0, 1.639, 0.0040)
    bar = K.pillow("torso_slot_bar", K.rr(0.040 / H, 0.0065 / H, 0.002), fr, rise=0.0014, thickness=0.004, steps=3)
    fin(bar, "silver", bevel=0.0008, seg=1)
    fr = frm(0.0, 1.6245, 0.0040)
    pb = K.pillow("torso_slot_block", K.rr(0.036 / H, 0.0155 / H, 0.004), fr, rise=0.0022, thickness=0.004, steps=3)
    fin(pb, "teal", bevel=0.0010, seg=1)
    # dark channel running the whole column
    ch, _s = K.sweep_on_shell("torso_spine_channel_front", densify([(0.0, 6.04), (0.0, 5.70), (0.0, 5.12)], 8), 0.050, 0.010, n=4.0, embed=0.3, nring=10, lift=0.004)
    fin(ch, "dark", bone="abdomen", bevel=0.0007, seg=1)
    # two thin dark rails flank the column from the slot down to the pill (f08: vertical grooves either side of the spine)
    rp = [spm(0.0305, z, 0.0040) for z in (1.532, 1.46, 1.38, 1.30, 1.245)]
    rl = L.tube("torso_spine_rail.L", rp, 0.0016, nring=6, n_per_seg=6, round_ends=True)
    fin(rl, "gunmetal", bone="abdomen", bevel=0, seg=1, mirror=True)
    # three teal blocks (0.046 wide, 0.0235 tall, 0.0045 gaps) in ONE column under the 6 (f07, f08)
    for i, zc in enumerate(SBLK):
        fr = frm(0.0, zc, 0.0040)
        b = K.pillow(f"torso_sblock_{i}", K.rr(0.046 / H, 0.0235 / H, 0.003), fr, rise=0.0030, thickness=0.004, steps=3)
        fin(b, "teal", bevel=0.0010, seg=1, wear=1.0)
        pa, _n = site(-0.021, zc + 0.0118, 0.0040 + 0.0033)
        pb_, _n2 = site(0.021, zc + 0.0118, 0.0040 + 0.0033)
        rm = L.tube(f"torso_sblock_rim_{i}", [pa, pb_], 0.0009, nring=5, n_per_seg=2, round_ends=True)
        fin(rm, "silver", bevel=0, seg=1)
    # small bronze block, long bronze bar 0.024 x 0.075, small bronze block, eye recess + knob
    def cblock(nm, zc, w, h_, lift, rise, mat=None, bone="chest"):
        mat = mat or HW.olive()
        fr = frm(0.0, zc, lift)
        b = K.pillow(nm, K.rr(w / H, h_ / H, 0.003), fr, rise=rise, thickness=0.004, steps=3)
        fin(b, mat, bone=bone, bevel=0.0009, seg=2)

    cblock("torso_sbronze_a", 1.4335, 0.026, 0.026, 0.0045, 0.0032)
    cblock("torso_sbar", 1.3665, 0.024, 0.075, 0.0045, 0.0040, bone="abdomen")
    cblock("torso_sbronze_b", 1.311, 0.026, 0.018, 0.0045, 0.0032, bone="abdomen")
    # eye-shaped recess with a round grey knob
    fr = frm(0.0, 1.2915, 0.0040)
    eye = [(0.021 * math.cos(a), 0.0075 * math.sin(a)) for a in [2 * math.pi * k / 24 for k in range(24)]]
    rec = K.pillow("torso_eye_recess", eye, fr, rise=0.0006, thickness=0.004, steps=2)
    fin(rec, "dark", bone="abdomen", bevel=0.0006, seg=1)
    knob = L.sphere("torso_eye_knob", 0.0052, L.Frame(spm(0.0, 1.2915, 0.0052)), scale=(1, 0.7, 1), segments=16, rings=10)
    fin(knob, "gunmetal", bone="abdomen", bevel=0, seg=1)
    pts = [spm(0.021 * math.cos(a), 1.2915 + 0.0075 * math.sin(a) * 1.0, 0.0050) for a in [2 * math.pi * k / 20 for k in range(21)]]
    lip = L.tube("torso_eye_lip", pts, 0.0010, nring=5, n_per_seg=1, round_ends=False)
    fin(lip, "silver", bone="abdomen", bevel=0, seg=1)
    # lumbar side tabs: 3 teal pairs, span 0.10 m
    for i, zc in enumerate((1.396, 1.360, 1.325)):
        for sx in (1, -1):
            fr = frm(sx * 0.038, zc, 0.0040)
            t = K.pillow(f"torso_tab_{i}_{'L' if sx > 0 else 'R'}", K.rr(0.025 / H, 0.0215 / H, 0.003), fr, rise=0.0030,
                         thickness=0.004, steps=3)
            fin(t, "teal", bone="abdomen", bevel=0.0010, seg=1, wear=1.0)
            pa, _n = site(sx * 0.038 - 0.0115, zc + 0.0108, 0.0040 + 0.0033)
            pb_, _n2 = site(sx * 0.038 + 0.0115, zc + 0.0108, 0.0040 + 0.0033)
            rm = L.tube(f"torso_tab_rim_{i}_{'L' if sx > 0 else 'R'}", [pa, pb_], 0.0008, nring=5, n_per_seg=2, round_ends=True)
            fin(rm, "silver", bone="abdomen", bevel=0, seg=1)


# ============================================================================================ abdomen
def pods_and_struts():
    """4 tall red pillow pods per side (0.036 wide x 0.040 tall, 0.0025 gaps) in black sockets, satin crimson; a darker second red
    column half hidden behind the strut (f07); an olive-bronze strut 0.020 wide with a dark second strut outboard."""
    zc0, pitch = 1.420, 0.042
    for i in range(4):
        zc = zc0 - pitch * i
        fr = frm(0.074, zc, 0.0040)
        sock = K.pillow(f"torso_pod_socket_{i}.L", K.rr(0.043 / H, 0.0455 / H, 0.010), fr, rise=0.0, thickness=0.008, steps=2)
        fin(sock, "dark", bone="abdomen", bevel=0.0008, seg=1, mirror=True)
        fr2 = frm(0.074, zc, 0.0052)
        pod = K.pillow(f"torso_pod_{i}.L", K.rr(0.0335 / H, 0.0405 / H, 0.0165), fr2, rise=0.0160, thickness=0.006, steps=7,
                       power=1.8)
        fin(pod, HW.podred(), bone="abdomen", bevel=0.0009, seg=2, mirror=True)
        # darker second red column behind the strut
        fr3 = frm(0.1005, zc, 0.0040)
        p2 = K.pillow(f"torso_pod_back_{i}.L", K.rr(0.0200 / H, 0.0395 / H, 0.008), fr3, rise=0.0075, thickness=0.006, steps=5,
                      power=1.8)
        fin(p2, HW.redshade(), bone="abdomen", bevel=0.0007, seg=1, mirror=True)
        # pewter lip along the top of each socket
        pa, _n = site(0.074 - 0.0185, zc + 0.0232, 0.0058)
        pb_, _n2 = site(0.074 + 0.0185, zc + 0.0232, 0.0058)
        lp = L.tube(f"torso_pod_lip_{i}.L", [pa, pb_], 0.0012, nring=5, n_per_seg=2, round_ends=True)
        fin(lp, "silver", bone="abdomen", bevel=0, seg=1, mirror=True)
    S1 = [(0.113 / H, 1.470 / H), (0.109 / H, 1.375 / H), (0.106 / H, 1.280 / H)]
    ob, sw = K.sweep_on_shell("torso_strut_in.L", densify(S1, 6), 0.0100 / H, 0.0045 / H, n=4.5, embed=0.3, nring=12, lift=0.002 / H)
    fin(ob, HW.olive(), bone="abdomen", bevel=0.0010, seg=2, mirror=True)
    S2 = [(0.1235 / H, 1.46 / H), (0.1215 / H, 1.37 / H), (0.1195 / H, 1.280 / H)]
    o2, _ = K.sweep_on_shell("torso_strut_out.L", densify(S2, 6), 0.0055 / H, 0.0045 / H, n=4.0, embed=0.3, nring=10, lift=0.0 / H)
    fin(o2, "gunmetal", bone="abdomen", bevel=0.0008, seg=1, mirror=True)
    # strut end caps (top and bottom of each strut)
    for e, zc in enumerate((1.476, 1.276)):
        fr = frm(0.113 if e == 0 else 0.106, zc, 0.0040)
        cap = K.pillow(f"torso_strut_cap_{e}.L", K.rr(0.0235 / H, 0.0085 / H, 0.003), fr, rise=0.0030, thickness=0.004, steps=3)
        fin(cap, HW.olive(), bone="abdomen", bevel=0.0009, seg=2, mirror=True)
        fr = frm(0.1235 if e == 0 else 0.1195, zc + (0.004 if e == 0 else -0.004), 0.0030)
        cap2 = K.pillow(f"torso_strut_cap_out_{e}.L", K.rr(0.0130 / H, 0.0070 / H, 0.002), fr, rise=0.0020, thickness=0.004, steps=3)
        fin(cap2, "gunmetal", bone="abdomen", bevel=0.0007, seg=1, mirror=True)
    # strut clamp bands (3 per strut), flush straps, no bolts
    for i, t in enumerate((0.16, 0.50, 0.84)):
        p = sw.point(t, math.pi / 2, 0.0)
        n = sw.outward(t, math.pi / 2)
        cb = HW.clamp_band(f"torso_strut_clamp_{i}.L", p, n, (1, 0, 0), 0.0300, 0.0060, 0.0022)
        fin(cb, "gunmetal", bone="abdomen", bevel=0.0004, seg=1, mirror=True)
    # waist skirt: a slim overlapping teal plate under the pods meeting the belt lip
    fr = frm(0.083, 1.262, 0.0038, ang=0)
    skirt = K.pillow("torso_abs_skirt.L", K.rr(0.078 / H, 0.014 / H, 0.005), fr, rise=0.0030, thickness=0.004, steps=4)
    fin(skirt, "teal", bone="abdomen", bevel=0.0010, seg=1, wear=0.0, mirror=True)
    # teal pill 0.03 x 0.057 m into the belt (f07 spine bottom)
    fr = frm(0.0, 1.2535, 0.0045)
    pill = K.pillow("torso_spine_pill", K.rr(0.030 / H, 0.057 / H, 0.012), fr, rise=0.0035, thickness=0.004, steps=4)
    fin(pill, "teal", bone="abdomen", bevel=0.0010, seg=2, wear=1.0)
    pa, _n = site(-0.012, 1.2535 - 0.0285, 0.0045 + 0.0035)
    pb_, _n2 = site(0.012, 1.2535 - 0.0285, 0.0045 + 0.0035)
    fin(L.tube("torso_spine_pill_rim", [pa, pb_], 0.0009, nring=5, n_per_seg=2, round_ends=True), "silver", bone="abdomen",
        bevel=0, seg=1)


def belt_plug():
    # dark interface plug through the belt top, 0.05 H into the pelvis
    z0, z1 = 5.09, 5.22
    keys = [(0, 0.56 * H, 0.46 * H, 2.6), (1, 0.52 * H, 0.45 * H, 2.6)]
    sw = L.Sweep([Vector((0, 0.03 * H, z0 * H)), Vector((0, 0.03 * H, z1 * H))], keys)
    ob = sw.mesh("torso_belt_plug", nring=40, nstations=6, caps=True)
    fin(ob, "dark", bone="abdomen", bevel=0, seg=1)


# ============================================================================================ the white 6
def six():
    """The white 6, 0.074 m tall x 0.036 m wide, stroke ~0.0115 m, centre 1.5765 m, thin black outline, standing on the
    black slot (f07 crop 12).  Lato Bold glyph scaled non-uniformly to the measured width."""
    font = "/PATH/TO/fonts/Lato/Lato-Bold.ttf"
    target_h = 0.074
    target_w = 0.036

    def flat(offset, nm):
        cu = bpy.data.curves.new(nm, "FONT")
        cu.body = "6"
        cu.resolution_u = 8
        cu.offset = offset
        try:
            if os.path.exists(font):
                cu.font = bpy.data.fonts.load(font)
        except Exception:
            pass
        ob = bpy.data.objects.new(nm, cu)
        L._link(ob)
        bpy.context.view_layer.update()
        dg = bpy.context.evaluated_depsgraph_get()
        me = bpy.data.meshes.new_from_object(ob.evaluated_get(dg), depsgraph=dg)
        bpy.data.objects.remove(ob, do_unlink=True)
        bpy.data.curves.remove(cu)
        return me

    def prism(me, cx, cy, sx, sy, z0, z1, nm):
        bm = bmesh.new()
        bm.from_mesh(me)
        for v in bm.verts:
            v.co = Vector(((v.co.x - cx) * sx, (v.co.y - cy) * sy, z0))
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
        for f in bm.faces:
            if f.normal.z > 0:
                f.normal_flip()
        ret = bmesh.ops.extrude_face_region(bm, geom=bm.faces[:])
        nv = [g for g in ret["geom"] if isinstance(g, bmesh.types.BMVert)]
        bmesh.ops.translate(bm, vec=Vector((0, 0, z1 - z0)), verts=nv)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
        m2 = bpy.data.meshes.new(nm)
        bm.to_mesh(m2)
        bm.free()
        m2.shade_smooth()
        return bpy.data.objects.new(nm, m2)

    me = flat(0.0, "torso_six_src")
    xs = [v.co.x for v in me.vertices]
    ys = [v.co.y for v in me.vertices]
    cx, cy = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
    sy = target_h / (max(ys) - min(ys))
    sx = target_w / (max(xs) - min(xs))
    fr = frm(0.0, 1.5765, 0.0034)
    mo = flat(0.012, "torso_six_outline_src")
    ob2 = prism(mo, cx, cy, sx, sy, -0.0008, 0.0004, "torso_six_outline")
    L._link(ob2)
    L.transform_mesh(ob2, fr.matrix())
    fin(ob2, "dark", bone="chest", bevel=0.0002, seg=1)
    ob = prism(me, cx, cy, sx, sy, -0.0004, 0.0036, "torso_six")
    L._link(ob)
    L.transform_mesh(ob, fr.matrix())
    fin(ob, "white", bone="chest", bevel=0.0004, seg=1)


# ============================================================================================ back

def dpanel(name, z0, z1, a0, a1, mat, thick=0.006, infl=0.030, height=0.02, hp=1.2, ends=0.15, bone="chest",
           bevel=0.0016, wear=0.0, mirror=True, nu=14, nv=12):
    sw = CORE["sw"]
    f0 = a0 if callable(a0) else math.radians(a0)
    f1 = a1 if callable(a1) else math.radians(a1)
    ob = sw.panel(name, tz(z0), tz(z1), f0, f1, thickness=thick, inflate=infl * H, height=height * H, hp=hp,
                  ends=ends, nu=nu, nv=nv)
    return fin(ob, mat, bone=bone, bevel=bevel, wear=wear, mirror=mirror)


def wpanel(name, zc, zh, ac, aw, mat, p=2.6, **kw):
    z0, z1, f0, f1 = win(zc, zh, ac, aw, p)
    return dpanel(name, z0, z1, f0, f1, mat, **kw)


def back_shell():
    sw = CORE["sw"]
    # smooth dorsal shield: two big shoulder-blade shields with a bat-wing notch at the spine
    wpanel("torso_back_scapula.L", 6.25, 0.34, 305, 32, "teal", p=2.8, height=0.05, hp=1.1, ends=0.0, nu=22, nv=18)
    # claw blades hanging from the shields (3 per side)
    for i, c in enumerate((289, 305, 322)):
        a0 = (lambda t, c=c: math.radians(c - 1.2 - 5.5 * L.smoothstep(tz(5.55), tz(5.95), t)))
        a1 = (lambda t, c=c: math.radians(c + 1.2 + 5.5 * L.smoothstep(tz(5.55), tz(5.95), t)))
        dpanel(f"torso_back_claw_{i}.L", 5.52, 5.98, a0, a1, HW.olive(), thick=0.004, infl=0.060, height=0.012, hp=1.0,
               ends=0.0, nu=10, nv=4, bevel=0.0012)
    # shingled lames over each shoulder-blade shield (breaks the big flat expanse; each overlaps the one above)
    for i, (zc, zh, ac, aw, infl) in enumerate(((6.50, 0.12, 306, 22, 0.062), (6.30, 0.12, 305, 25, 0.074),
                                                (6.10, 0.12, 304, 26, 0.086))):
        wpanel(f"torso_back_shingle_{i}.L", zc, zh, ac, aw, "teal", p=3.2, infl=infl, height=0.030, hp=1.2, ends=0.0,
               nu=12, nv=14, thick=0.005)
        # dark groove line along the lower edge of each shingle (the plates overlap like scales)
        sw_ = CORE["sw"]
        gl = [sw_.point(tz(zc - zh * 0.78), math.radians(ac + aw * (k / 6.0 * 1.6 - 0.8)), infl * H + 0.030 * H * 0.5 + 0.0008)
              for k in range(7)]
        gt = L.tube(f"torso_back_shingle_groove_{i}.L", gl, 0.0014, nring=5, n_per_seg=3, round_ends=True)
        fin(gt, "dark", bevel=0, seg=1, mirror=True)
    # trapezius yoke: 5 overlapping plates, split on the centre line
    wpanel("torso_yoke_nape", 6.80, 0.18, 270, 20, "teal", p=3.8, infl=0.052, height=0.03, ends=0.0, mirror=False, nu=14, nv=14)
    wpanel("torso_yoke_a.L", 6.74, 0.22, 300, 25, "teal", p=3.6, infl=0.046, height=0.035, ends=0.0, nu=14, nv=14)
    wpanel("torso_yoke_b.L", 6.70, 0.22, 343, 27, "teal", p=3.6, infl=0.040, height=0.035, ends=0.0, nu=14, nv=14)
    # spine channel: dark strip with 3 bronze capsules
    wpanel("torso_spine_channel", 5.85, 0.80, 270, 10, "dark", p=5.0, infl=0.026, height=0.0, ends=0.0, mirror=False,
           bevel=0.0008, wear=0.0, nu=30, nv=6)
    # stacked vertebra blocks down the channel (090): bronze blocks, teal keels, dark gaps between
    for i, zc in enumerate((6.45, 6.32, 6.19, 6.06, 5.93, 5.80, 5.67, 5.54, 5.41)):
        fr = frame_b(0.0, zc, 0.040)
        wv = 0.17 - 0.004 * i
        cap = K.pillow(f"torso_back_vert_{i}", K.rr(wv, 0.100, 0.030), fr, rise=0.026 * H, thickness=0.010, steps=5)
        fin(cap, HW.olive(), bone="chest" if zc > 5.15 + 0.5 else "abdomen", bevel=0.0014, seg=2, wear=0.0)
        fr2 = frame_b(0.0, zc, 0.060)
        keel = K.pillow(f"torso_back_keel_{i}", K.rr(0.050, 0.075, 0.020), fr2, rise=0.020 * H, thickness=0.004, steps=4)
        fin(keel, "teal", bone="chest" if zc > 5.65 else "abdomen", bevel=0.0010, seg=1, wear=0.0)
        # pewter rim line across the top of each vertebra block
        pa = frame_b(-wv * 0.36, zc + 0.052, 0.040).p(0, 0, 0.026 * H * 0.8)
        pb_ = frame_b(wv * 0.36, zc + 0.052, 0.040).p(0, 0, 0.026 * H * 0.8)
        rimb = L.tube(f"torso_back_vert_rim_{i}", [pa, pb_], 0.0012, nring=5, n_per_seg=2, round_ends=True)
        fin(rimb, "silver", bone="chest" if zc > 5.65 else "abdomen", bevel=0, seg=1)
    # red lat pods in teal frames
    wpanel("torso_lat_frame.L", 5.84, 0.68, 318, 31, "teal", p=2.4, infl=0.030, height=0.02, hp=1.0, ends=0.0, nu=28, nv=14)
    wpanel("torso_lat_pod.L", 5.84, 0.61, 318, 24, HW.redshade(), p=2.4, infl=0.032, height=0.075, hp=1.1, ends=0.0, nu=28, nv=14,
           bone="chest", bevel=0.0010, wear=0.0)
    # lower lobes meeting the belt
    for i, (cx, cz, w, h_) in enumerate(((0.0, 5.24, 0.50, 0.20), (0.40, 5.26, 0.42, 0.22))):
        fr = frame_b(cx, cz, 0.020)
        lobe = K.pillow(f"torso_back_lobe_{i}" + (".L" if cx else ""), K.rr(w, h_, 0.08), fr, rise=0.060 * H, thickness=0.01)
        fin(lobe, "teal", bone="abdomen", bevel=0.0016, seg=2, wear=0.0, mirror=bool(cx))
    # bat-wing wishbone arches
    wb = [(0.60, 6.66), (0.47, 6.50), (0.32, 6.36), (0.17, 6.25), (0.07, 6.17)]
    dense = L.catmull([spb(x, z, 0.030) for x, z in wb], n_per_seg=6)
    ups = [nrm_b(min(p.x / H, 0.9 * rx(p.z / H)), p.z / H) for p in dense]
    t = K.ring_mesh("torso_wishbone.L", dense, ups, lambda f: 0.026 - 0.008 * f, 0.0042, n_sec=12, sec_n=3.5, closed=False)
    fin(t, "teal", bevel=0.0014, seg=2, wear=0.0, mirror=True)
    # 3 bronze ribs arching over the flank / back
    for i, th in enumerate((332, 345, 358)):
        pp = [sw.point(tz(6.62 - 1.2 * k / 30.0), math.radians(th), 0.05 * H) for k in range(31)]
        r = L.tube(f"torso_back_rib_{i}.L", pp, 0.016 * H, nring=8, n_per_seg=3)
        fin(r, HW.olive(), bevel=0.0006, seg=1, wear=0.0, mirror=True)
    # nape port: concentric rings
    fr = frame_b(0.0, 6.84, 0.045)
    port = L.disc_stack("torso_nape_port", fr.o, fr.z, [(0.095 * H, 0.012 * H), (0.078 * H, 0.020 * H),
                                                          (0.056 * H, 0.016 * H), (0.036 * H, 0.026 * H)], segments=40)
    fin(port, "bronze", bevel=0.0008, seg=1, wear=0.0)
    hole = L.disc_stack("torso_nape_core", fr.o, fr.z, [(0.022 * H, 0.032 * H)], segments=24)
    fin(hole, "dark", bevel=0.0004, seg=1, wear=0.0)



# ============================================================================================ back hardware
def pbolt(nm, z, th, infl, height, v, hp, r=0.0028, mat="silver", bone="chest", mirror=True):
    """washered hex bolt on a core-hugging back panel: z in H, th degrees, panel inflate/height in H, v = 0..1 across the panel"""
    sw = CORE["sw"]
    t = tz(z)
    off = infl * H + height * H * (math.sin(math.pi * v) ** hp) + 0.0006
    p = sw.point(t, math.radians(th), off)
    n = sw.outward(t, math.radians(th))
    hexb(nm, p, n, r, mat=mat, bone=bone, mirror=mirror)


def back_hardware():
    """Round-2 hardware on the back: bolts at the scapula, shingle, yoke and lat-frame corners, rivets on every vertebra block,
    a hose pair running down beside the spine with ferrules and clamps, and a bolt ring on the nape port."""
    sw = CORE["sw"]
    # scapula shields (centre 305 deg): 4 bolts per side near the corners
    for i, (z, th) in enumerate(((6.50, 288), (6.50, 322), (6.02, 286), (6.02, 326))):
        v = (th - 273.0) / 64.0
        pbolt(f"torso_scap_bolt_{i}", z, th, 0.030, 0.05, min(1, max(0, v)), 1.1)
    # shingles: one bolt each
    for i, (z, th, infl, hgt, v) in enumerate(((6.50, 306, 0.062, 0.030, 0.5), (6.30, 305, 0.074, 0.030, 0.5), (6.10, 304, 0.086, 0.030, 0.5))):
        pbolt(f"torso_shingle_bolt_{i}", z, th, infl, hgt, v, 1.2, r=0.0024)
    # lat frames (centre 318): 4 bolts around the frame, on the teal rim
    for i, (z, th) in enumerate(((6.36, 318), (5.32, 318), (5.84, 289), (5.84, 347))):
        pbolt(f"torso_lat_bolt_{i}", z, th, 0.030, 0.02, 0.5, 1.0, r=0.0030)
    # yoke plates: bolts
    for i, (z, th) in enumerate(((6.86, 296), (6.86, 336), (6.66, 300))):
        pbolt(f"torso_nape_yoke_bolt_{i}", z, th, 0.046, 0.035, 0.5, 1.0, r=0.0027)
    # vertebra rivets (one each side of every block) and keel screws
    for i, zc in enumerate((6.45, 6.32, 6.19, 6.06, 5.93, 5.80, 5.67, 5.54, 5.41)):
        wv = 0.17 - 0.004 * i
        pair = []
        for sgn, side in ((1, "L"), (-1, "R")):
            fr = frame_b(sgn * (wv / 2 - 0.022), zc, 0.040)
            p = fr.p(0, 0, 0.026 * H * 0.9)
            pair.append(HW.rivet(f"torso_vert_rivet_{i}_{side}", p, fr.z, 0.0020))
        fin(L.join(pair, f"torso_vert_rivets_{i}"), "gunmetal", bone="chest" if zc > 5.65 else "abdomen", bevel=0, seg=1)
    # hose pair beside the spine (nape port down to the lumbar blocks), ferrules and strap clamps
    for j, (nm, mat, r, xH) in enumerate((("hose", "dark", 0.0040, 0.20), ("cable", HW.redshade(), 0.0030, 0.235))):
        zs = [6.72, 6.44, 6.16, 5.88, 5.60, 5.34]
        pts = [spb(xH + 0.01 * math.sin(k * 0.9), z, 0.050 + 0.004 * j) for k, z in enumerate(zs)]
        tb = L.tube(f"torso_back_{nm}.L", pts, r, nring=8, n_per_seg=6, round_ends=True)
        fin(tb, mat, bone="chest", bevel=0, seg=1, mirror=True)
        for e, idx in enumerate((0, len(pts) - 1)):
            direction = (pts[1] - pts[0]) if idx == 0 else (pts[-1] - pts[-2])
            fe = HW.ferrule(f"torso_back_{nm}_ferrule_{e}.L", pts[idx], direction, r * 1.35, 0.009)
            fin(fe, "silver", bone="chest" if idx == 0 else "abdomen", bevel=0.0004, seg=1, mirror=True)
        for e, k in enumerate((1, 3)):
            p = pts[k]
            n = nrm_b(xH, zs[k])
            cb = HW.clamp_band(f"torso_back_{nm}_clamp_{e}.L", p + n * 0.0, n, (1, 0, 0), 0.0155, 0.0070, 0.0030)
            fin(cb, "gunmetal", bone="chest", bevel=0.0004, seg=1, mirror=True)
    # bolt ring on the nape port (6 hex bolts, washered)
    fr = frame_b(0.0, 6.84, 0.045)
    for k in range(6):
        a = 2 * math.pi * (k + 0.5) / 6
        p = fr.p(0.088 * H * math.cos(a), 0.088 * H * math.sin(a), 0.0)
        hexb(f"torso_nape_bolt_{k}", p, fr.z, 0.0020, mat="silver", bone="chest", mirror=False, wash=False, h=0.0018)


# ============================================================================================ build
def build():
    del OUT[:]
    core()
    red_cavity()
    yoke()
    flank_wall()
    shield_plates()
    plate_hardware()
    plate_edge_glint()
    plate_groove()
    plate_fluting()
    tail_tiles()
    arch_sw = arches()
    arch_hardware(arch_sw)
    rib_blades()
    spine()
    pods_and_struts()
    belt_plug()
    six()
    back_shell()
    back_hardware()
    return list(OUT)
