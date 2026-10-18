"""head_face - the silver mask, brow, keystone, recessed eyes, speaker cups + discs, chin yoke, ear fins."""
import math
import bpy
from mathutils import Vector
import seis_lib as L
import seis_spec as S
from head_lib import (oval, flat_plate, SK, CREST, SPH, FACE, chart_plate, chart_grid, prof, ends, both, add, loop_tube, almond, shrink,
                      on_surface, ccw, pxz, pxl, lattice, curve_strip, PX_S, polar_tiles)

Z = S.hh
GAPF = 0.0010
GROOVES = []
YOKE_SW = None


def mirror_poly(poly):
    return [(-x, z) for x, z in poly]


def panel(out, name, poly, mat="pewter", rise=0.0028, thick=0.004, steps=1, gap=GAPF, mirror=True, wear=0.0,
          bevel=0.0010, lift=0.0, flat=1.0, groove=False, step=0.004, power=1.5):
    poly = shrink(poly, gap) if gap else poly
    ob = flat_plate(name + (".L" if mirror else ""), poly, FACE, rise=rise, thickness=thick, lift=lift, step=step)
    L.finish(ob, mat, bevel=bevel, bevel_segments=2, bone="head", wear=wear, weighted=False)
    if groove:
        pts3 = on_surface(FACE, shrink(poly, 0.0006), 0.0006)
        gl = loop_tube(name + "_groove", pts3, 0.00055, nring=4)
        L.finish(gl, "dark", bevel=0, bone="head", apply=False)
        GROOVES.append((gl, mirror))
    if mirror:
        both(ob, out)
    else:
        out.append(ob)
    return ob


S8 = 0.000285      # metres per pixel in spec/crops/onmodel_head/f08_head_neck_front.png (cranium 670 px = 0.19 m)
XC8, YC8 = 390.0, 60.0


def f8(X, Y):
    """f08 on-model crop pixel -> (x, z) metres, right half = robot's left (+x)"""
    return ((X - XC8) * S8, S.hh(8.3) - (Y - YC8) * S8)


def f8l(pts):
    return [f8(X, Y) for X, Y in pts]


def build(out):
    GROOVES.clear()
    # ------------------------------------------------------------------ mask facets, laid out on the ON-MODEL frame 08.
    # base shell under everything, so a groove between two facets shows a dark core (groove tubes) and never a black void
    fbase = f8l([(395, 330), (470, 330), (640, 300), (655, 420), (665, 520), (640, 560), (660, 640), (600, 780), (575, 880),
                 (560, 905), (395, 905)])
    base = chart_plate("head_mask_base.L", [(max(x, 0.0), z) for x, z in fbase], FACE, rise=0.0006, thickness=0.004, steps=1,
                       flat_top=0.9, lift=-0.0012, step=0.006)
    L.finish(base, "pewter_shade", bevel=0.0004, bone="head")
    both(base, out)
    # forehead inner panel (beside the keystone) and outer panel with the diagonal recessed slot
    panel(out, "head_mask_forehead_in", f8l([(408, 350), (470, 352), (458, 430), (455, 505), (422, 505), (410, 430)]),
          rise=0.0022, thick=0.004, bevel=0.0010, groove=True)
    panel(out, "head_mask_forehead_out", f8l([(486, 352), (626, 330), (668, 340), (696, 372), (700, 430), (690, 505), (650, 524), (612, 526),
                                              (548, 522), (500, 542), (470, 506), (468, 430)]),
          rise=0.0008, thick=0.004, bevel=0.0008, groove=True, lift=0.0002)
    # fine hatch lines beside the nose bridge (3 short grooves each side)
    for i in range(3):
        y0 = 430 + 28 * i
        pts = on_surface(FACE, f8l([(430, y0), (452, y0 + 34)]), 0.0022)
        gl = L.tube(f"head_bridge_hatch_{i}.L", pts, 0.00055, nring=4)
        L.finish(gl, "dark", bevel=0, bone="head", apply=False)
        both(gl, out)
    # fine V cut lines on the forehead outer panel (f07/f08: two short diagonal grooves running from the keystone toward the brow)
    for i, (p0, p1) in enumerate((((510, 392), (572, 458)), ((540, 380), (626, 436)))):
        pts = on_surface(FACE, f8l([p0, p1]), 0.0034)
        gl = L.tube(f"head_forehead_vcut_{i}.L", pts, 0.00055, nring=4)
        L.finish(gl, "dark", bevel=0, bone="head", apply=False)
        both(gl, out)
    # brow shelf: an angled ridge over each eye socket, dipping toward the nose bridge (shallow V)
    panel(out, "head_mask_brow", f8l([(462, 536), (498, 506), (548, 494), (612, 496), (658, 516), (664, 548), (606, 524),
                                      (548, 530), (498, 548)]), rise=0.0042, thick=0.006, steps=1, gap=0.0010, bevel=0.0014)
    # central muzzle: narrow nose bridge widening to the chin (0.09 m at the lip), one plate; chevron cut lines on the cheeks
    # (round 3: the muzzle and the cheek planes are hard planar facets, built in head_facets.py)
    # (the silver cheek arc is built round the speaker pod in cups(), concentric with it)

    # ------------------------------------------------------------------ stepped silver keystone (end of the cap)
    kx, kz0 = 0.0, f8(390, 336)[1]
    for i, ((y0, y1), hw) in enumerate([((336, 372), 78), ((372, 402), 52), ((402, 430), 30)]):
        z0, z1 = f8(390, y0)[1], f8(390, y1)[1]
        w = hw * S8
        o = chart_plate(f"head_keystone_step_{i}", shrink([(-w, z0), (w, z0), (w * 0.88, z1), (-w * 0.88, z1)], 0.0007), FACE,
                        rise=0.0036 + 0.0006 * i, thickness=0.004, steps=2, step=0.004)
        L.finish(o, "pewter", bevel=0.0010, bone="head", wear=0.0)
        out.append(o)
    kb = chart_plate("head_keystone_base", [(-0.022, f8(390, 330)[1]), (0.022, f8(390, 330)[1]), (0.010, f8(390, 440)[1]),
                                              (-0.010, f8(390, 440)[1])], FACE, rise=0.0006, thickness=0.004, steps=1,
                     flat_top=0.9, lift=-0.0010, step=0.004)
    L.finish(kb, "dark", bevel=0.0004, bone="head")
    out.append(kb)

    # ------------------------------------------------------------------ eye sockets (recessed) + round-oval red bulb
    cx, cz = f8(543, 614)
    ang = 8.0
    sock = oval(cx, cz, 0.0415, 0.0360, ang, n=32, power=2.3)
    blk = chart_plate("head_eye_socket.L", sock, FACE, rise=0.0006, thickness=0.010, steps=1, flat_top=0.9, lift=-0.0006,
                      step=0.003)
    L.finish(blk, "dark", bevel=0.0004, bone="head")
    both(blk, out)
    bulb = chart_plate("head_eye_bulb.L", oval(cx, cz, 0.0362, 0.0312, ang, n=32, power=2.1), FACE, rise=0.0038,
                       thickness=0.002, steps=5, power=1.2, lift=-0.0006, step=0.0025, flat_top=0.0, shrink_to=0.30)
    L.finish(bulb, "eye_lens", bevel=0.0003, bone="head")
    both(bulb, out)
    glow = chart_plate("head_eye_glow.L", oval(cx - 0.0003, cz + 0.0006, 0.0300, 0.0252, ang, n=28, power=2.0), FACE, rise=0.0032,
                       thickness=0.002, steps=4, power=1.2, lift=-0.0002, step=0.0025, flat_top=0.0, shrink_to=0.30)
    L.finish(glow, "eye_lens", bevel=0.0003, bone="head")
    both(glow, out)
    hot = chart_plate("head_eye_hot.L", oval(cx - 0.0014, cz + 0.0020, 0.0100, 0.0078, ang, n=20, power=2.0), FACE,
                      rise=0.0010, thickness=0.001, steps=2, lift=0.0030, step=0.002)
    L.finish(hot, "eyecore", bevel=0.0002, bone="head")
    both(hot, out)

    left = [g for g, m in GROOVES if m]
    if left:
        gj = L.join(left, "head_mask_grooves.L")
        L.finish(gj, "dark", bevel=0, bone="head", apply=False)
        both(gj, out)
    for g, m in GROOVES:
        if not m:
            out.append(g)
    # chevron cut lines from the inner eye corner down to the muzzle corner (cheek planes)
    for sx_ in (1,):
        pts = on_surface(FACE, f8l([(468, 668), (500, 710), (540, 765), (566, 815)]), 0.0050)
        gl = L.tube("head_chevron_cut.L", pts, 0.00065, nring=4)
        L.finish(gl, "dark", bevel=0, bone="head", apply=False)
        both(gl, out)
    # tiny pale slot under the muzzle lip
    z_lip = f8(390, 906)[1]
    ps = L.box("head_lip_slot", (0.016, 0.0016, 0.0016), L.Frame((0.0, FACE.y(0.0, z_lip) - 0.0006, z_lip - 0.0022)))
    L.finish(ps, "pewter", bevel=0.0004, bone="head", wear=0.0)
    out.append(ps)
    jc = L.sphere("head_jaw_core", 1.0, frame=L.Frame((0.0, -0.004, 1.868)), scale=(0.046, 0.070, 0.040), segments=40, rings=24)
    L.finish(jc, "dark", bevel=0, bone="head")
    out.append(jc)
    cups(out)
    glow_behind(out)
    global YOKE_SW
    YOKE_SW = yoke(out)
    fins(out)
    return out


# ------------------------------------------------------------------------------------------------ speaker cups
from head_lib import DISC_C, DISC_N


def cups(out):
    D, n = DISC_C, DISC_N
    fr = L.Frame.at(D, n, (0, 0, 1))          # x = up, y = n x up ..., z = n
    hv, uv = -fr.y, fr.x
    OFF = -hv * 0.0050 - uv * 0.0040      # speaker disc sits toward the front-bottom of the pod: red shows behind and above it
    # cup body (dark, hollow look: rim ring + floor)
    body = L.cylinder("head_cup_body.L", 0.0365, 0.050, L.Frame(D - n * 0.0250, fr.x, fr.y, fr.z), segments=48)
    cutter = L.cylinder("_cut", 0.0322, 0.020, L.Frame(D - n * 0.0060, fr.x, fr.y, fr.z), segments=48)
    L.boolean_cut(body, cutter)
    L.finish(body, "yoke", bevel=0.0006, bone="head")
    both(body, out)
    floor = L.cylinder("head_cup_floor.L", 0.0320, 0.0016, L.Frame(D - n * 0.0152, fr.x, fr.y, fr.z), segments=48)
    L.finish(floor, "red", bevel=0, bone="head")
    both(floor, out)
    ring_pts = []
    for i in range(40):
        a = 2 * math.pi * i / 40
        ring_pts.append(D + (fr.x * math.cos(a) + fr.y * math.sin(a)) * 0.0362)
    rimt = loop_tube("head_cup_rim.L", ring_pts, 0.0030, nring=8)
    L.finish(rimt, "pewter", bevel=0, bone="head", wear=0.0)
    both(rimt, out)
    ring2 = [D - n * 0.0045 + (fr.x * math.cos(2 * math.pi * i / 40) + fr.y * math.sin(2 * math.pi * i / 40)) * 0.0325
             for i in range(40)]
    lip = loop_tube("head_cup_lip.L", ring2, 0.0022, nring=6)
    L.finish(lip, "bronze", bevel=0, bone="head", wear=0.5)
    both(lip, out)
    # the stepped concentric disc, recessed 12 mm
    rings = [(0.0262, 0.0045), (0.0200, 0.0080), (0.0118, 0.0112)]
    dst = L.disc_stack("head_speaker_disc.L", D - n * 0.0145 + OFF, n, rings, segments=48, xhint=(0, 0, 1))
    L.finish(dst, "darkdisc", bevel=0.0004, bevel_segments=1, bone="head")
    both(dst, out)
    for j, (r_, h_) in enumerate(rings[:-1]):
        lp = [D - n * 0.0145 + OFF + n * h_ + (fr.x * math.cos(2 * math.pi * i / 28) + fr.y * math.sin(2 * math.pi * i / 28)) * r_
              for i in range(28)]
        lt = loop_tube(f"head_speaker_edge_{j}.L", lp, 0.00055, nring=4)
        L.finish(lt, "gunmetal", bevel=0, bone="head", wear=0.0)
        both(lt, out)
    # hub cap: a dull dark pad in the middle
    hub = L.cylinder("head_speaker_hub.L", 0.0050, 0.0030, L.Frame(D - n * 0.0145 + OFF + n * 0.0112, fr.x, fr.y, fr.z), segments=24)
    L.finish(hub, "gunmetal", bevel=0.0006, bone="head")
    both(hub, out)
    # silver cheek arc: a round-section band round the FRONT of the pod, concentric with it (brow outer end -> muzzle corner)
    arc_pts = []
    for ang in range(100, 196, 12):
        r_ = math.radians(ang)
        arc_pts.append(D + (hv * math.cos(r_) + uv * math.sin(r_)) * 0.0470 + n * 0.0042)
    asw = L.Sweep(arc_pts, [(0.0, 0.0045, 0.0050, 3.0), (0.5, 0.0075, 0.0060, 3.0), (1.0, 0.0040, 0.0045, 3.0)],
                  front=tuple(n), side=tuple(uv))
    arc = asw.mesh("head_cheek_arc.L", nring=20, round_start=(0.004, 2), round_end=(0.004, 2))
    L.finish(arc, "pewter", bevel=0.0010, bevel_segments=2, bone="head", wear=0.0)
    both(arc, out)
    rim_d = loop_tube("head_speaker_bead.L", [D - n * 0.0125 + OFF + (fr.x * math.cos(2 * math.pi * i / 48) + fr.y *
                                                                  math.sin(2 * math.pi * i / 48)) * 0.0310 for i in range(48)],
                      0.0012, nring=6)
    L.finish(rim_d, "gunmetal", bevel=0, bone="head", wear=0.0)
    both(rim_d, out)


# ------------------------------------------------------------------------------------------------ chin yoke
class PlaneYChart:
    """vertical plane y = y0 (+ slight tilt) for small front details of the chin yoke."""
    def __init__(self, y0, tilt=0.25):
        self.y0, self.tilt = y0, tilt

    def map(self, x, z):
        return Vector((x, self.y0 + self.tilt * (z - 1.82), z)), Vector((0, -1, self.tilt)).normalized()


def yoke(out):
    D, n = DISC_C, DISC_N
    fr = L.Frame.at(D, n, (0, 0, 1))
    hv = -fr.y                      # horizontal axis in the disc plane, pointing outward / rearward
    uv = fr.x                       # up
    Rc = 0.0445
    arc = []
    for a in (-90, -64, -38, -12, 14, 40, 66, 88):
        r = math.radians(a)
        arc.append(D + (hv * math.cos(r) + uv * math.sin(r)) * Rc)
    centre = [Vector((0.0, -0.066, 1.8420)), Vector((0.022, -0.0645, 1.8425)), Vector((0.043, -0.0575, 1.8435)),
              Vector((0.057, -0.045, 1.8375))]
    right = centre + arc
    fullp = [Vector((-p.x, p.y, p.z)) for p in reversed(right[1:])] + right
    key = [(0.0, 0.0140, 0.0115, 3.2), (0.12, 0.0155, 0.0120, 3.2), (0.24, 0.0200, 0.0125, 3.2), (0.36, 0.0240, 0.0130, 3.2),
           (0.5, 0.0280, 0.0135, 3.4), (0.64, 0.0240, 0.0130, 3.2), (0.76, 0.0200, 0.0125, 3.2), (0.88, 0.0155, 0.0120, 3.2),
           (1.0, 0.0140, 0.0115, 3.2)]
    sw = L.Sweep(fullp, key, front=(-DISC_N.x, DISC_N.y, 0.0))
    yk = sw.mesh("head_chin_yoke", nring=28, round_start=(0.006, 2), round_end=(0.006, 2))
    L.finish(yk, "yoke", bevel=0.0016, bevel_segments=2, bone="head")
    out.append(yk)
    # concentric swirl lines: thin pewter ribbons following the yoke band (the lines are its layered edges)
    for j, ang in enumerate((44, 14, -16, -44)):
        pts = [sw.point(k / 48, math.radians(90 + ang), 0.0010) for k in range(49)]
        ln = L.tube(f"head_yoke_swirl_{j}", pts, 0.0006 if j in (0, 3) else 0.0008, nring=6)
        L.finish(ln, "pewter_shade", bevel=0, bone="head", wear=0.0)
        out.append(ln)
    # dark rounded recess at the bottom centre
    rc = L.box("head_yoke_recess", (0.034, 0.004, 0.012), L.Frame((0.0, -0.0795, 1.8500)))
    L.finish(rc, "dark", bevel=0.0030, bevel_segments=3, bone="head")
    out.append(rc)
    return sw


# ------------------------------------------------------------------------------------------------ ear shells
EAR_Z0, EAR_Z1 = 2.067, 1.832           # top 0.057 below the crown, bottom reaching the chin (ONMODEL: 0.254 tall incl. rim)
EAR_FN = None


def ear_pt(u, v, lift=0.0):
    """cupped D-shaped shell, left side.  u 0 (top) .. 1 (bottom) along the height, v 0 (front straight edge) .. 1 (rear bulge).
    Convex toward the outside, open toward the head, span 0.233 m tip to tip."""
    su = math.sin(math.pi * min(max(u, 0.0), 1.0))
    z = EAR_Z0 + (EAR_Z1 - EAR_Z0) * u
    w = 0.066 * (math.sin(math.pi * (0.06 + 0.88 * u)) ** 0.55)            # D profile: depth 0.075 at the middle
    y = 0.028 + 0.004 * (2 * u - 1) ** 2 + w * v
    dy = y - SK.yc
    arg = 1.0 - (dy / SK.b(-dy)) ** 2 - ((z - SK.zc) / SK.cz(z - SK.zc)) ** 2
    xh = SK.a * math.sqrt(max(arg, 0.0)) if arg > 0 else 0.0
    xb = max(xh, 0.045) + 0.0050                     # hugs the egg, curling in toward the top and bottom of the D
    bow = 0.0225 * su ** 0.7 * max(0.0, 1 - (2 * v - 1) ** 2) ** 0.55 * (1.0 - 0.25 * v)
    front = 0.005 * su ** 0.5 * (1 - v) ** 2                                 # the front edge stands off the cheek (thin loop in front view)
    return Vector((xb + bow + front + lift, y, z))


def fins(out):
    global EAR_FN
    EAR_FN = ear_pt
    nu, nv = 30, 10

    def outward_sign(fl):
        a = ear_pt(0.5, 0.5)
        pu = ear_pt(0.55, 0.5) - a
        pv = ear_pt(0.5, 0.55) - a
        return pu.cross(pv).x > 0

    flip = not outward_sign(False)
    ob = L.grid_surface("head_ear_shell.L", lambda u, v: ear_pt(u, v), nu, nv, thickness=0.0042, flip=flip, offset=-1.0)
    L.finish(ob, "teal_deep", bevel=0.0013, bevel_segments=2, bone="head", wear=0.0)
    both(ob, out)
    # gold inner liner, a hair inside the shell
    inner = L.grid_surface("head_ear_liner.L", lambda u, v: ear_pt(u, 0.015 + 0.97 * v, -0.0052), nu, nv, thickness=0.0015, flip=flip,
                           offset=-1.0)
    L.finish(inner, "gold", bevel=0.0006, bone="head", wear=0.0)
    both(inner, out)
    # champagne edge bead round the whole rim
    rim = [ear_pt(0.0 + 0.0, 0.0, 0.0)]
    pts = [ear_pt(u / 24, 0.0) for u in range(25)] + [ear_pt(1.0, 0.0)]
    bd = L.tube("head_ear_edge_front.L", [ear_pt(0.02 + 0.96 * i / 24, 0.0) for i in range(25)], 0.0040, nring=8, round_ends=False)
    L.finish(bd, "pewter", bevel=0, bone="head", wear=0.0)
    both(bd, out)
    loop = [ear_pt(0.02 + 0.96 * i / 30, 1.0) for i in range(31)]
    # a crease line along the shell's outer face (the D-shaped ridge seen in f10 / f06) and a second, inner champagne line
    for nm_, vv, rr, mm in (("head_ear_ridge.L", 0.58, 0.0016, "pewter_shade"), ("head_ear_ridge_2.L", 0.30, 0.0011, "dark")):
        rg = L.tube(nm_, [ear_pt(0.10 + 0.80 * i / 26, vv, 0.0010) for i in range(27)], rr, nring=6, round_ends=True)
        L.finish(rg, mm, bevel=0, bone="head", wear=0.0, apply=False)
        both(rg, out)
    bd2 = L.tube("head_ear_edge_rear.L", loop, 0.0030, nring=8, round_ends=False)
    L.finish(bd2, "pewter", bevel=0, bone="head", wear=0.0)
    both(bd2, out)


def glow_behind(out):
    """RED glows behind and above the speaker disc (f06, f10, f12, f04): a red lacquer patch on the head side, between the
    cheek arc and the ear shell"""
    def pf(u, v):
        phi = math.radians(84.0 + (106.0 - 84.0) * u)
        th = math.radians(6.0 - (6.0 + 30.0) * v)
        return phi * SPH.RS, th * SPH.RT
    g = chart_grid("head_side_glow.L", SPH, pf, 14, 12, lambda u, v: 0.0030 * ends(u, 0.25) * ends(v, 0.25), 0.003, lift=0.0010)
    L.finish(g, "red", bevel=0.0008, bone="head")
    both(g, out)
