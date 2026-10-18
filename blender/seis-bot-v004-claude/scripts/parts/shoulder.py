"""shoulder - SEIS bot ON-MODEL shoulder (conform round 1, 2026-10-18, from spec/ONMODEL.md + Bear's 12 video frames).

Per side (built LEFT +X, mirrored to the right):
  * the PAULDRON is a hollow RAM-HORN: a C-shaped onion of 3 concentric bands (thin dark lip, wide glossy teal middle
    band, dark inner lining) with thin champagne lines between them, open toward the neck, rounded into one smooth
    dome at the rear, its front rim slanted so the lower end becomes a beak/tongue that points down-forward (f07,
    f09-f12).  Apex 0.042 m below the chin, outer edge at 2.9 H_m span.
  * the HUB: a dull olive disc 0.057 m in a black cavity 0.14 m wide, no ribs (f07).  Hub centres 0.457 m apart.
  * the COLLAR: pale champagne-silver Y-fork 0.123 x 0.060 m, two lozenge pads 0.096 x 0.021 m held by dark C-hooks
    that curl into the shoulder (f07).
  * the TRAPEZIUS COWL: dark wings with teal rims, rising only to chin level.
  * a short deltoid collar under the dome (the red stadium window belongs to the arm module).
  * the REAR trapezius tiers, claw blades and bat-wing yoke (stills only; recoloured, thin gold, no wear).
The underarm loops, the 6-rib half drum, the hook rod and the fan-ribbed hub of round 0 are DELETED (ONMODEL).

Dimensions are in METRES for the 2.12 m figure unless a name ends _H (head-heights, H = 0.2554 m).
"""
import math
import bpy
import bmesh
from mathutils import Vector, Matrix

import seis_lib as L
import seis_spec as S
import shoulder_kit as K

try:                                    # the real chest shell (parts/torso_kit.py), so the collar follows the torso
    import torso_kit as _TK
except Exception:                       # pragma: no cover
    _TK = None

H = S.H
JL = S.J("shoulder.L")
PI = math.pi


def rad(a):
    return math.radians(a)


def W(x, y, z):
    """world point from ABSOLUTE head-height coordinates (x, y, z)."""
    return Vector((x * H, y * H, z * H))


# ------------------------------------------------------------------------------------------------ small helpers
def prism(name, outline, frame, depth):
    """Solid prism: 2-D outline in the xy plane of `frame`, extruded from z=0 to z=depth (metres)."""
    pts = []
    for p in outline:
        if not pts or (Vector(p) - Vector(pts[-1])).length > 1e-7:
            pts.append(p)
    if (Vector(pts[0]) - Vector(pts[-1])).length < 1e-7:
        pts.pop()
    bm = bmesh.new()
    vs = [bm.verts.new((p[0], p[1], 0.0)) for p in pts]
    f = bm.faces.new(vs)
    r = bmesh.ops.extrude_face_region(bm, geom=[f])
    vv = [e for e in r["geom"] if isinstance(e, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, vec=(0, 0, depth), verts=vv)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    bmesh.ops.transform(bm, matrix=frame.matrix(), verts=bm.verts[:])
    return L._prim(name, bm)


def fin(ob, mat, bone, bevel=0.0015, seg=2, wear=None, **kw):
    L.finish(ob, mat, bevel=bevel, bevel_segments=seg, bone=bone, wear=wear, **kw)
    return ob


def solid_between(name, fo, fi, nu, nv):
    """Closed solid between two parametric surfaces fo(u, v) (outer) and fi(u, v) (inner), u, v in [0, 1]."""
    verts = []
    for i in range(nu + 1):
        for j in range(nv + 1):
            verts.append(Vector(fo(i / nu, j / nv)))
    n0 = len(verts)
    for i in range(nu + 1):
        for j in range(nv + 1):
            verts.append(Vector(fi(i / nu, j / nv)))
    Wd = nv + 1
    faces = []
    for i in range(nu):
        for j in range(nv):
            a, b, c, d = i * Wd + j, (i + 1) * Wd + j, (i + 1) * Wd + j + 1, i * Wd + j + 1
            faces.append((a, b, c, d))
            faces.append((n0 + d, n0 + c, n0 + b, n0 + a))
    for j in range(nv):
        for i in (0, nu):
            a, b = i * Wd + j, i * Wd + j + 1
            faces.append((a, b, n0 + b, n0 + a))
    for i in range(nu):
        for j in (0, nv):
            a, b = i * Wd + j, (i + 1) * Wd + j
            faces.append((a, b, n0 + b, n0 + a))
    ob = L.new_mesh(name, verts, faces)
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    bm.to_mesh(ob.data)
    bm.free()
    return ob


# ================================================================================================ the RAM-HORN pauldron
HX, HZ = 0.2285, 1.592            # hub centre (hubs 0.457 m apart, 0.229 m below the chin yoke)
EX, EZ = 0.2285, 1.649            # centre of the horn's elliptical section
RX0, RZ0 = 0.1535, 0.1400         # max section radii (outer silhouette is 0.95 of this at the front rim)
YB = 0.158                        # rear pole of the dome (y): depth 0.27 m with the beak
S_FRONT = 0.88
A_TOP, A_BOT = 122.0, -102.0      # arc of the C, degrees (0 = outboard, 90 = up); open toward the neck / chest
V_DOME = 0.506
BEAK = 0.055                      # how far the lower end of the C is drawn forward (the beak / tongue)


def env(v):
    """section scale along the horn: quarter-ellipse dome at the rear (v=0), full at V_DOME, easing to S_FRONT at the front."""
    if v < V_DOME:
        return math.sqrt(max(0.0, 1.0 - ((V_DOME - v) / V_DOME) ** 2))
    f = (v - V_DOME) / (1.0 - V_DOME)
    return 1.0 - (1.0 - S_FRONT) * f ** 1.4


def y_front(a_deg):
    """front rim depth: slanted, the lower end swings forward (the tongue)."""
    return -0.098 + 0.052 * math.sin(rad(a_deg))


def tfac(a_deg):
    """wall-thickness factor: full on top and outboard, thinning toward the lower seat (f07: 2-3 fine lines at the seat)."""
    return 1.0 - 0.40 * L.smoothstep(-10.0, -100.0, a_deg)


def pinch(a_deg):
    """teardrop: the lower arc is drawn inboard so the horn ends above the arm's red window instead of hiding it."""
    return 1.0 - 0.16 * L.smoothstep(-5.0, -95.0, a_deg)


def zst(a_deg):
    """the lower half of the horn is drawn 9 percent taller so the shoulder falls into the upper arm (critic: no notch)."""
    return 1.0 + 0.03 * L.smoothstep(5.0, -80.0, a_deg)


def horn_pt(off, a_deg, v, floor=0.004, ro=None):
    """world point on the horn surface `off` metres in from the outer silhouette, arc angle a_deg, depth fraction v."""
    s = env(v)
    t = tfac(a_deg)
    rx = max(s * RX0 * pinch(a_deg) - off * t, floor)
    rz = max(s * RZ0 * zst(a_deg) - off * t, floor)
    if ro is not None:                         # keep an inner surface strictly inside its outer one
        rx = min(rx, ro[0] - 0.003)
        rz = min(rz, ro[1] - 0.003)
    a = rad(a_deg)
    beak = BEAK * L.smoothstep(-30.0, -102.0, a_deg) * L.smoothstep(0.55, 1.0, v)      # the lower front end is drawn forward
    return Vector((EX + rx * math.cos(a), YB + (y_front(a_deg) - YB) * v - beak, EZ + rz * math.sin(a) - 0.25 * beak))


def horn_r(off, a_deg, v):
    s = env(v)
    t = tfac(a_deg)
    return (max(s * RX0 * pinch(a_deg) - off * t, 0.004), max(s * RZ0 * zst(a_deg) - off * t, 0.004))


def horn_band(name, o0, o1, v0, v1, a0, a1, mat, wear=None, nu=None, nv=24, bevel=0.0011, seg=2):
    """one concentric band of the horn between radial offsets o0 (outer face) and o1 (inner face)."""
    if nu is None:
        nu = max(10, int(abs(a1 - a0) * 0.32))
    def ang(u):
        return a0 + (a1 - a0) * u

    def vv_(w):
        return v0 + (v1 - v0) * w

    def fo(u, w):
        return horn_pt(o0, ang(u), vv_(w))

    def fi(u, w):
        a, v = ang(u), vv_(w)
        return horn_pt(o1, a, v, floor=0.0015, ro=horn_r(o0, a, v))

    ob = solid_between(name, fo, fi, nu, nv)
    return fin(ob, mat, "pauldron.L", bevel=bevel, seg=seg, wear=wear)


def horn_line(name, off, a0, a1, v, r, mat="gold", n=40):
    """thin champagne line along a rim: constant depth v, arc a0 -> a1."""
    pts = [horn_pt(off, a0 + (a1 - a0) * k / n, v) for k in range(n + 1)]
    ob = L.tube(name, pts, r, nring=8, n_per_seg=3)
    return fin(ob, mat, "pauldron.L", bevel=0, wear=0)


def horn_edge(name, off, a, v0, v1, r, mat="gold", n=26):
    """thin champagne line along an open end of the C: constant arc angle a, depth v0 -> v1."""
    pts = [horn_pt(off, a, v0 + (v1 - v0) * k / n) for k in range(n + 1)]
    ob = L.tube(name, pts, r, nring=8, n_per_seg=3)
    return fin(ob, mat, "pauldron.L", bevel=0, wear=0)


# radial layout from the outer silhouette (m): lip 0.016 | gap | teal 0.034 | gap | inner band 0.020   (total 0.078)
LIP = (0.000, 0.016)
TEAL = (0.020, 0.0540)
INNER = (0.0580, 0.078)
SEAMS = (74.5, 46.5)                # the two dome grooves = the real seams between the three teal plates
DV = 1.0 / 0.256                    # one metre of depth in v units (dome depth 0.256 m)


def horn_sweep(name, o0, o1, v0, vf, crown, a0, a1, mat, wear=None, bevel=0.0008, seg=2, nu=None, nfront=7, nrear=20, bone="pauldron.L"):
    """one concentric band of the horn as a SOLID swept along the arc a0 -> a1 with a CONVEX front: the cross-section is the
    rectangle off o0..o1 (outer..inner face), depth v0..vf, whose front edge bulges forward by `crown` metres (rolled, tube-like)."""
    if nu is None:
        nu = max(10, int(abs(a1 - a0) * 0.30))
    prof = [(o0, v0 + (vf - 0.012 - v0) * (k / nrear) ** 0.8) for k in range(nrear + 1)]
    for k in range(nfront + 1):
        t = k / nfront
        prof.append((o0 + (o1 - o0) * t, vf + crown * DV * math.sin(PI * t) ** 0.7 - (0.012 if k in (0, nfront) else 0.0)))
    prof += [(o1, v0 + (vf - 0.012 - v0) * (k / nrear) ** 0.8) for k in range(nrear, -1, -1)]
    P = len(prof)
    verts = []
    for i in range(nu + 1):
        a = a0 + (a1 - a0) * i / nu
        for (off, v) in prof:
            verts.append(horn_pt(off, a, v, floor=0.0015))
    faces = []
    for i in range(nu):
        for j in range(P):
            j2 = (j + 1) % P
            faces.append((i * P + j, (i + 1) * P + j, (i + 1) * P + j2, i * P + j2))
    faces.append(tuple(reversed(range(P))))
    faces.append(tuple(nu * P + j for j in range(P)))
    ob = L.new_mesh(name, verts, faces)
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    bm.to_mesh(ob.data)
    bm.free()
    return fin(ob, mat, bone, bevel=bevel, seg=seg, wear=wear)


def horn_normal(off, a_deg):
    """outward-front unit normal of the horn's front face (v = 1) at arc angle a."""
    ta = horn_pt(off, a_deg + 1.0, 1.0) - horn_pt(off, a_deg - 1.0, 1.0)
    rd = horn_pt(TEAL[0], a_deg, 1.0) - horn_pt(TEAL[1], a_deg, 1.0)
    n = ta.cross(rd).normalized()
    if n.y > 0:
        n = -n
    return n


def build_horn(left):
    ga, gb = SEAMS
    # dark liner under everything: the black gaps between the three bands are this, seen through the grooves
    left.append(horn_band("shoulder_horn_liner.L", 0.032, 0.062, 0.02, 0.985, A_TOP - 3, A_BOT + 4, "dark", wear=0, nv=8, nu=28))
    left.append(horn_band("shoulder_horn_liner_rim.L", 0.012, 0.062, 0.92, 0.985, A_TOP - 3, A_BOT + 4, "dark", wear=0, nv=4, nu=28))
    # 3 concentric bands, each a rounded (tube-like) strip: thin pewter lip, wide glossy teal, dark inner band.  Every band is cut
    # into separate plates at the same two seams as the dome (real armour: overlapping plates with hairline gaps).
    segs = ((A_TOP - 6, ga + 0.4, "a"), (ga - 0.4, gb + 0.4, "b"), (gb - 0.4, A_BOT + 7, "c"))
    for a0, a1, t in segs:
        left.append(horn_sweep(f"shoulder_horn_lip_{t}.L", LIP[0], LIP[1], 0.93, 1.000, 0.0055, a0, a1, "gunmetal", wear=None, nfront=5, nrear=3, bevel=0.0006))
    # the teal band = THREE separate overlapping plates (the two seams are the two white dome grooves)
    left.append(horn_sweep("shoulder_horn_teal_top.L", TEAL[0], TEAL[1], 0.012, 0.975, 0.0105, A_TOP - 2, ga + 0.8, "teal", wear=0.6, nrear=10))
    left.append(horn_sweep("shoulder_horn_teal_mid.L", TEAL[0] + 0.0012, TEAL[1], 0.012, 0.975, 0.0105, ga - 0.8, gb + 0.8, "teal", wear=0.6, nrear=10))
    left.append(horn_sweep("shoulder_horn_teal_low.L", TEAL[0], TEAL[1], 0.012, 0.975, 0.0105, gb - 0.8, A_BOT + 3, "teal", wear=0.6, nrear=10))
    for a0, a1, t in ((A_TOP - 4, (ga + gb) / 2 + 0.4, "a"), ((ga + gb) / 2 - 0.4, A_BOT + 5, "b")):
        left.append(horn_sweep(f"shoulder_horn_inner_{t}.L", INNER[0], INNER[1], 0.40, 0.955, 0.0065, a0, a1, "gunmetal", wear=None, nfront=4, nrear=3, bevel=0.0006))
    # champagne: ONE outer lip bead only (critic: no doubled outlines), cut with the lip plates
    for a0, a1, t in segs:
        left.append(horn_line(f"shoulder_horn_gold_lip_{t}.L", 0.0004, a0, a1, 0.998, 0.0020, n=18))
    # the two dome groove lines (thin pewter, the white lines of f09-f12)
    for k, a in enumerate(SEAMS):
        left.append(horn_edge(f"shoulder_horn_groove_{'ab'[k]}.L", TEAL[0] - 0.0006, a, 0.16, 0.985, 0.0012, mat="silver"))


def build_hub(left):
    """socket + bearing stack: black cavity floor, notched socket rim, 8 bolts, bearing ring, washers, dull olive hub 0.057 m
    with stepped face rings and one small centre bolt.  NO ribs on the hub (ONMODEL)."""
    ny = (0, -1, 0)
    fr = L.Frame((HX, -0.056, HZ + 0.012), (1, 0, 0), (0, 0, 1), (0, 1, 0))
    cav = L.cylinder("shoulder_cavity.L", 0.0725, 0.012, fr, segments=56)
    fin(cav, "dark", "pauldron.L", bevel=0.0008, seg=1, wear=0)
    left.append(cav)
    rim = K.bearing_ring("shoulder_socket_rim.L", (HX, -0.0622, HZ + 0.012), ny, 0.0745, 0.0640, 0.0045, mat="gunmetal",
                         bone="pauldron.L", seg=40, notches=20)
    left.append(rim)
    ring = K.bearing_ring("shoulder_hub_ring.L", (HX, -0.0622, HZ), ny, 0.0395, 0.0300, 0.0070, mat="gunmetal", bone="pauldron.L",
                          seg=48, notches=24)
    left.append(ring)
    wsh = K.washer_stack("shoulder_hub_washer.L", (HX, -0.0624, HZ), ny, [(0.0352, 0.0016), (0.0322, 0.0016)], mat="silver",
                         bone="pauldron.L", seg=48)
    left.append(wsh)
    frh = L.Frame((HX, -0.068, HZ), (1, 0, 0), (0, 0, 1), (0, 1, 0))
    hub = L.cylinder("shoulder_hub.L", 0.0285, 0.024, frh, segments=44)
    fin(hub, K.olive_material(), "pauldron.L", bevel=0.0025, seg=3, wear=0)
    left.append(hub)
    face = K.washer_stack("shoulder_hub_face.L", (HX, -0.0800, HZ), ny, [(0.0215, 0.0014), (0.0150, 0.0016)], mat="gunmetal",
                          bone="pauldron.L", seg=40)
    left.append(face)
    left.append(K.hex_bolt("shoulder_hub_cap.L", (HX, -0.0832, HZ), ny, r=0.0062, h=0.0030, mat=K.olive_material(), bone="pauldron.L", washer=False))
    # dark plug running into the chest side (joint contract)
    plug = L.cylinder("shoulder_plug_chest.L", 0.016, 0.085, L.Frame((HX - 0.045, 0.012, HZ), (0, 1, 0), (0, 0, 1), (1, 0, 0)), segments=24)
    fin(plug, "dark", "pauldron.L", bevel=0, wear=0)
    left.append(plug)


def build_tongue(left):
    """silver beak-like tongue: the lower front end of the horn drawn out to a point, pointing down-forward (f09-f12)."""
    n_u, n_v = 26, 8
    a_lo, a_hi = -112.0, -58.0

    def tongue(off):
        def f(u, v):
            a = a_hi + (a_lo - a_hi) * u
            p = horn_pt(off, a, 1.0)
            k = L.smoothstep(0.15, 1.0, u)
            fwd = Vector((0.008 * k, -0.046 * k * k, -0.020 * k))
            side = (v - 0.5) * 2.0
            w = (0.022 * (1.0 - 0.9 * k ** 0.8)) * side
            rim = Vector((EX - p.x, 0.0, EZ - p.z)).normalized()
            return tuple(p + fwd + rim * (w * 0.6))
        return f

    ob = L.grid_surface("shoulder_tongue.L", tongue(0.030), n_u, n_v, thickness=0.009, offset=0.0)
    fin(ob, "silver", "pauldron.L", bevel=0.0018, seg=3, wear=None)
    left.append(ob)
    # second, narrower blade riding on it (overlapping plates)
    ob = L.grid_surface("shoulder_tongue_blade.L", tongue(0.044), n_u, 6, thickness=0.005, offset=0.0)
    fin(ob, "gunmetal", "pauldron.L", bevel=0.0012, seg=2, wear=None)
    left.append(ob)


# ================================================================================================ deltoid collar
def build_cup(left):
    """deltoid collar UNDER the dome: a dark core and THREE overlapping teal lames (shingled, top one outermost) with a pewter
    hem on the lowest.  Round 3: lifted to z 1.60-1.65 so the arm's red stadium window (z 1.505-1.597, arm module) is free."""
    cx = 0.292
    zt, zb = 1.662, 1.614
    path = [Vector((cx, 0.0, zt)), Vector((cx + 0.001, 0.0, (zt + zb) / 2)), Vector((cx + 0.002, 0.0, zb))]
    sw = L.Sweep(path, [(0.0, 0.0500, 0.0490, 3.0), (1.0, 0.0490, 0.0480, 3.0)], front=(0, -1, 0), side=(1, 0, 0))
    core = sw.mesh("shoulder_cup_core.L", nring=44, nstations=8, caps=True)
    fin(core, "dark", "upperarm.L", bevel=0.0012, seg=2, wear=0)
    left.append(core)
    specs = (("a", 0.00, 0.32, 0.0085), ("b", 0.18, 0.50, 0.0072), ("c", 0.36, 0.68, 0.0059), ("d", 0.54, 0.84, 0.0047), ("e", 0.70, 1.00, 0.0035))
    for tag, t0, t1, infl in specs:
        lame = sw.panel(f"shoulder_cup_lame_{tag}.L", t0, t1, -2.35, 2.35, thickness=0.0055, inflate=infl, height=0.0, nu=3, nv=24)
        fin(lame, "teal", "upperarm.L", bevel=0.0013, seg=2, wear=1.0)
        left.append(lame)
    hem = sw.panel("shoulder_cup_hem.L", 0.88, 1.0, -2.35, 2.35, thickness=0.004, inflate=0.0058, height=0.0, nu=3, nv=36)
    fin(hem, "silver", "upperarm.L", bevel=0.0010, seg=2, wear=None)
    left.append(hem)
    plug = L.cylinder("shoulder_plug_arm.L", 0.042, 0.04, L.Frame((cx + 0.002, 0.0, zb - 0.002), (1, 0, 0), (0, 1, 0), (0, 0, 1)), segments=32)
    fin(plug, "dark", "upperarm.L", bevel=0, wear=0)
    left.append(plug)
    # lame fasteners: one round head at each lame's outer end
    for tag, zc, infl in (("a", zt - 0.006, 0.0085), ("c", (zt + zb) / 2, 0.0059), ("e", zb + 0.006, 0.0035)):
        r = 0.0490 + infl
        for k, ang in enumerate((rad(-62), rad(62))):
            n = Vector((math.cos(ang), -math.sin(ang), 0.0)).normalized()
            p = Vector((cx + r * math.cos(ang), -r * math.sin(ang), zc))
            left.append(K.round_head(f"shoulder_cup_screw_{tag}{k + 1}.L", p - n * 0.0006, n, r=0.0027, mat="silver", bone="upperarm.L"))


# ================================================================================================ collar: Y-fork, pads, hooks
def cf(z):
    """front surface y (H) of the grey chest proxy at height z (H) (fallback when torso_kit is unavailable)."""
    t = L.clamp((z - 6.2) / 0.7)
    r = 0.95 + (0.62 - 0.95) * t
    return 0.03 + 0.02 * t - 0.85 * r


def cb(z):
    t = L.clamp((z - 6.2) / 0.7)
    r = 0.95 + (0.62 - 0.95) * t
    return 0.03 + 0.02 * t + 0.85 * r


def surf_y(x, z):
    """front surface y (m) of the chest shell at world (x, z) (m)."""
    if _TK is not None:
        try:
            return _TK.fy(abs(x) / H, z / H) * H
        except Exception:
            pass
    return cf(z / H) * H


def build_collar(left, mid):
    zc = 1.711                                   # 0.11 m below the chin yoke bottom
    yf = surf_y(0.0, zc)
    # Y-fork 0.123 x 0.060, pale champagne-silver
    zt = zc + 0.030
    pts = [(-0.0615, zt), (-0.036, zt), (0.0, zt - 0.020), (0.036, zt), (0.0615, zt), (0.019, zt - 0.040),
           (0.0155, zt - 0.060), (-0.0155, zt - 0.060), (-0.019, zt - 0.040)]
    ol = L.outline_poly(pts, round_r=0.008, n=4)
    fk = prism("shoulder_yfork", ol, L.Frame.at((0, yf + 0.006, 0), z=(0, -1, 0), x=(1, 0, 0)), 0.018)
    fin(fk, "silver", "chest", bevel=0.0016, seg=3, wear=None)
    mid.append(fk)
    # two lozenge pads 0.096 x 0.021 (centre x 0.100), outer ends tilted up
    xa, xb = 0.052, 0.148
    ya = surf_y(0.100, 1.724) - 0.004
    path = [Vector((xa, ya, 1.719)), Vector((0.100, ya, 1.724)), Vector((xb, ya + 0.004, 1.733))]
    sw = L.Sweep(path, [(0.0, 0.0105, 0.020, 2.6), (0.5, 0.0108, 0.021, 2.6), (1.0, 0.0105, 0.020, 2.6)],
                 front=(0, -1, 0), side=(0, 0, 1))
    pad = sw.mesh("shoulder_pad.L", nring=28, nstations=12, caps=True, round_start=(0.010, 2), round_end=(0.010, 2))
    fin(pad, "silver", "chest", bevel=0.0012, seg=2, wear=None)
    left.append(pad)
    # dark C-hook: leaves the pad's outer end, curls up and back into the shoulder (the horn's top end)
    ye = y_front(A_TOP)
    hp = [Vector((xb - 0.004, ya, 1.730)), Vector((0.158, ya + 0.020, 1.750)), Vector((0.168, ya + 0.050, 1.760)),
          Vector((0.171, (ya + ye) / 2, 1.764)), Vector((0.168, ye + 0.012, 1.762))]
    hk = L.tube("shoulder_chook.L", hp, 0.0065, taper=(1.0, 0.8), nring=12, n_per_seg=5, round_ends=True)
    fin(hk, "gunmetal", "chest", bevel=0.0006, seg=1, wear=None)
    left.append(hk)
    # --- hardware: pad base plate, pad screws, clevis plates + pin where the C-hook takes the pad, hook clamps, fork screws
    bp = K.clevis_plate("shoulder_pad_base.L", (0.100, ya + 0.0035, 1.7225), (0, -1, 0), 0.112, 0.026, 0.0030, mat="gunmetal",
                        bone="chest", xhint=(0, 0, 1), round_r=0.011)
    left.append(bp)
    for k, xx in enumerate((0.064, 0.136)):
        zz = 1.7205 + (xx - 0.100) * 0.18
        left.append(K.round_head(f"shoulder_pad_screw_{k + 1}.L", (xx, ya - 0.0105, zz), (0, -1, 0), r=0.0026, mat="gunmetal", bone="chest"))
    pv = Vector((xb + 0.003, ya - 0.0095, 1.731))
    for k, dy in enumerate((-0.0075, 0.0075)):
        pl = K.clevis_plate(f"shoulder_clevis_{k + 1}.L", pv + Vector((0, dy, 0)), (0, 1, 0), 0.030, 0.014, 0.0025, mat="gunmetal",
                            bone="chest", xhint=(1, 0, 0))
        left.append(pl)
    left.append(K.pin("shoulder_clevis_pin.L", pv + Vector((0, -0.0105, 0)), pv + Vector((0, 0.0105, 0)), r=0.0030, mat="silver", bone="chest"))
    hp_path = hp
    left += K.clamps_on("shoulder_chook_clamp", hp_path, 0.0065, (0.55,), bone="chest", mat="silver")
    # fork screws (mid line)
    for k, (xx, zz) in enumerate(((-0.046, zt - 0.007), (0.046, zt - 0.007), (0.0, zt - 0.046))):
        mid.append(K.round_head(f"shoulder_yfork_screw_{k + 1}", (xx, yf + 0.006 - 0.018 - 0.0004, zz), (0, -1, 0), r=0.0030, mat="gunmetal", bone="chest"))


def cowl_plate(name, F0, F1, R0, R1, u0=0.0, u1=1.0, crown=0.012, thick=0.008, nu=10, nv=8, dz=0.0):
    def f(u, v):
        uu = u0 + (u1 - u0) * u
        F = F0.lerp(F1, uu)
        R = R0.lerp(R1, uu)
        q = F.lerp(R, v)
        q = q + Vector((0, 0, crown * math.sin(PI * v) * math.sin(PI * uu) + dz))
        return tuple(q)
    return L.grid_surface(name, f, nu, nv, thickness=thick, offset=0.0)


def build_cowl(left):
    """trapezius cowl: dark wings, now THREE overlapping tiers (inner highest) with teal rims, smooth slope neck -> pauldron,
    top edge 0.03 m lower than round 1 so the neck rises out of the shoulders (critic), black inside."""
    dz = -0.050
    F0, F1 = Vector((0.205, -0.010, 1.728 + dz)), Vector((0.092, -0.014, 1.784 + dz))
    R0, R1 = Vector((0.205, 0.105, 1.742 + dz)), Vector((0.092, 0.095, 1.792 + dz))
    tiers = (("a", 0.00, 0.40, 0.0055), ("b", 0.34, 0.72, 0.0020), ("c", 0.66, 1.00, -0.0010))
    for tag, u0, u1, lift in tiers:
        ob = cowl_plate(f"shoulder_cowl_{tag}.L", F0, F1, R0, R1, u0, u1, crown=0.008, thick=0.008, dz=lift)
        fin(ob, "gunmetal", "chest", bevel=0.0016, seg=2, wear=0)
        left.append(ob)
    for tag, p0, p1 in (("top", F1, R1), ("out", F0, R0), ("rear", R0, R1)):
        pts = [p0.lerp(p1, k / 8) + Vector((0, 0, 0.003)) for k in range(9)]
        rd = L.tube(f"shoulder_cowl_rim_{tag}.L", pts, 0.0050, nring=10, n_per_seg=3, round_ends=True)
        fin(rd, "teal", "chest", bevel=0, wear=0.6)
        left.append(rd)
    # seams between tiers: thin teal ridge strips where one tier overlaps the next
    for tag, uu in (("ab", 0.40), ("bc", 0.72)):
        a, b = F0.lerp(F1, uu), R0.lerp(R1, uu)
        pts = [a.lerp(b, k / 8) + Vector((0, 0, 0.0085 if tag == "ab" else 0.0055)) for k in range(9)]
        rd = L.tube(f"shoulder_cowl_seam_{tag}.L", pts, 0.0028, nring=8, n_per_seg=3, round_ends=True)
        fin(rd, "teal", "chest", bevel=0, wear=0.6)
        left.append(rd)
    # inside: black cavity beneath the wing
    cav = cowl_plate("shoulder_cowl_cavity.L", Vector((0.20, -0.004, 1.690 + dz)), Vector((0.090, -0.008, 1.760 + dz)),
                     Vector((0.20, 0.100, 1.706 + dz)), Vector((0.090, 0.090, 1.770 + dz)), crown=0.0, thick=0.008)
    fin(cav, "dark", "chest", bevel=0, wear=0)
    left.append(cav)
    # fasteners: two per tier on the front edge, one on the neck-side rim
    for tag, uu, zl in (("a", 0.20, 0.0055), ("b", 0.54, 0.0020), ("c", 0.84, -0.0010)):
        for k, vv in enumerate((0.16, 0.84)):
            p = F0.lerp(F1, uu).lerp(R0.lerp(R1, uu), vv)
            p = p + Vector((0, 0, 0.008 * math.sin(PI * vv) * math.sin(PI * uu) + zl + 0.0042))
            left.append(K.hex_bolt(f"shoulder_cowl_bolt_{tag}{k + 1}.L", p, (0, 0, 1), r=0.0030, h=0.0026, mat="silver", bone="chest"))


# ================================================================================================ rear (stills; recoloured)
def wplate(name, pts, y, facing, rise, thick, rr, mat, bone, bevel=0.0018, wear=0.5, flat_top=0.0, inset=None, dome=0.0):
    """plate from (x, z) points in ABSOLUTE head-heights, placed on the plane y (H), facing -y (front) or +y (rear).
    dome > 0 (H) builds a domed plate (L.plate) of that rise instead of a flat prism."""
    if facing < 0:
        fr = L.Frame.at((0, y * H, 0), z=(0, -1, 0), x=(1, 0, 0))
        ol = [(p[0] * H, p[1] * H) for p in pts]
    else:
        fr = L.Frame.at((0, y * H, 0), z=(0, 1, 0), x=(-1, 0, 0))
        ol = [(-p[0] * H, p[1] * H) for p in pts]
    ol = L.outline_poly(ol, round_r=rr * H, n=(2 if dome else 4)) if rr else ol
    if dome:
        sgn = 1.0 if facing > 0 else -1.0
        fr = L.Frame.at((0, (y + sgn * thick) * H, 0), z=fr.z, x=fr.x)
        ob = L.plate(name, ol, fr, rise=dome * H, thickness=thick * H, steps=3, power=1.5, flat_top=flat_top, inset=inset)
    else:
        ob = prism(name, ol, fr, (thick + rise) * H)
    return fin(ob, mat, bone, bevel=bevel, seg=3, wear=wear)


def build_rear(left, mid):
    # nape bolt ring
    z0 = 6.98
    y0 = cb(z0) - 0.03
    base = L.disc_stack("shoulder_nape_ring", W(0, y0, z0), (0, 1, 0), [(0.072 * H, 0.006 * H), (0.056 * H, 0.012 * H)], segments=40)
    fin(base, "bronze", "chest", bevel=0.0008, wear=0)
    mid.append(base)
    core = L.disc_stack("shoulder_nape_core", W(0, y0 + 0.012 * 0.2, z0), (0, 1, 0), [(0.040 * H, 0.016 * H), (0.022 * H, 0.020 * H)], segments=32)
    fin(core, "darkdisc", "chest", bevel=0.0008, wear=0)
    mid.append(core)
    # three angular nape plates
    for k, (cx, zz) in enumerate(((-0.24, 7.02), (0.0, 7.07), (0.24, 7.02))):
        pts = [(cx - 0.13, zz - 0.07), (cx - 0.09, zz + 0.07), (cx + 0.09, zz + 0.07), (cx + 0.13, zz - 0.07)]
        ob = wplate(f"shoulder_nape_{k + 1}", pts, cb(zz) - 0.02, 1, 0.016, 0.03, 0, "teal", "chest", bevel=0.002, wear=0.5)
        mid.append(ob)
    # two big trapezoid plates meeting at a spine slot (left; mirrored), domed, with a raised second tier
    pts = [(0.03, 6.90), (0.50, 6.96), (0.90, 6.76), (0.88, 6.48), (0.03, 6.44)]
    ob = wplate("shoulder_trap_rear.L", pts, cb(6.7) - 0.04, 1, 0.03, 0.03, 0.02, "teal", "chest", bevel=0.0024, wear=0.5, dome=0.045, flat_top=0.3)
    left.append(ob)
    pts2 = [(0.10, 6.84), (0.46, 6.88), (0.78, 6.72), (0.76, 6.52), (0.10, 6.50)]
    ob = wplate("shoulder_trap_rear_t2.L", pts2, cb(6.7) + 0.035, 1, 0.02, 0.02, 0.015, "teal", "chest", bevel=0.002, wear=0.5, dome=0.03, flat_top=0.3)
    left.append(ob)
    # two claw blades laid over the scapular tier, pointing down toward the spine
    for k, cp in enumerate(([(0.14, 6.90), (0.31, 6.88), (0.15, 6.30)], [(0.38, 6.90), (0.55, 6.86), (0.40, 6.46)])):
        ob = wplate(f"shoulder_claw_{k + 1}.L", cp, cb(6.7) + 0.075 + 0.01 * k, 1, 0.014, 0.014, 0.0, "teal", "chest", bevel=0.0026, wear=0.5)
        left.append(ob)
        rid = wplate(f"shoulder_clawridge_{k + 1}.L", [(cp[0][0] + 0.03, cp[0][1] - 0.04), (cp[1][0] - 0.03, cp[1][1] - 0.04), (cp[2][0] + 0.005, cp[2][1] + 0.12)],
                     cb(6.7) + 0.075 + 0.01 * k + 0.014, 1, 0.006, 0.006, 0.0, "bronze", "chest", bevel=0.0012, wear=0)
        left.append(rid)
    # bat-wing back yoke (centre) with cut-out windows and a dark red glimpse behind
    pts = [(-0.40, 6.44), (-0.18, 6.50), (0.0, 6.36), (0.18, 6.50), (0.40, 6.44), (0.34, 6.18), (0.0, 6.02), (-0.34, 6.18)]
    yk = wplate("shoulder_yoke_rear", pts, cb(6.3) - 0.03, 1, 0.03, 0.03, 0.01, "teal", "chest", bevel=0.0024, wear=0.5)
    ybase = cb(6.3) - 0.03
    # round 3: the bat-wing cut-out windows are gone (critic: not in any frame); the yoke is one flat teal plate
    ol = L.outline_poly([(-q[0] * H, q[1] * H) for q in [(-0.022, 6.30), (0.022, 6.30), (0.022, 6.14), (-0.022, 6.14)]], round_r=0.012 * H, n=3)
    cutter = prism("cut", ol, L.Frame.at((0, (ybase - 0.02) * H, 0), z=(0, 1, 0), x=(-1, 0, 0)), 0.2 * H)
    L.boolean_cut(yk, cutter)
    mid.append(yk)
    rp = wplate("shoulder_yoke_glimpse", [(-0.34, 6.44), (0.34, 6.44), (0.30, 6.18), (0.0, 6.06), (-0.30, 6.18)], cb(6.3) + 0.0, 1, 0.010, 0.0, 0.0, "dark", "chest", bevel=0.0006, wear=0)
    mid.append(rp)


def build_rear_hw(left, mid):
    """round-2 hardware on the back: bolts on the nape plates and the bat-wing yoke, bolt ring on the nape bearing, and a pair
    of dark maroon hoses with clamps running from the nape over the trapezius (the brown ribbed strands in f09)."""
    nrm = (0, 1, 0)
    for k, (cx, zz) in enumerate(((-0.24, 7.02), (0.0, 7.07), (0.24, 7.02))):
        ytop = (cb(zz) + 0.026) * H
        for j, sx in enumerate((-0.072, 0.072)):
            mid.append(K.hex_bolt(f"shoulder_nape_bolt_{k + 1}{'ab'[j]}", ((cx + sx) * H, ytop, (zz + 0.045) * H), nrm, r=0.0030, h=0.0026,
                                  mat="gunmetal", bone="chest", xhint=(1, 0, 0)))
    ybase = cb(6.3) - 0.03
    ytop = (ybase + 0.03) * H
    for k, (xx, zz) in enumerate(((-0.33, 6.43), (0.33, 6.43), (-0.28, 6.23), (0.28, 6.23))):
        mid.append(K.round_head(f"shoulder_yoke_rivet_{k + 1}", (xx * H, ytop, zz * H), nrm, r=0.0028, mat="gunmetal", bone="chest"))
    # nape bearing: 6 bolts round the base ring
    z0 = 6.98
    y0 = cb(z0) - 0.03
    for k in range(6):
        a = 2 * PI * (k + 0.5) / 6
        mid.append(K.hex_bolt(f"shoulder_nape_ringbolt_{k + 1}", (0.058 * H * math.cos(a), (y0 + 0.012 * 0.0) * H + 0.0035, z0 * H + 0.058 * H * math.sin(a)),
                              nrm, r=0.0028, h=0.0024, mat="silver", bone="chest", washer=False))
    # hoses: nape -> over the trapezius, one per side
    zc = 7.0
    yb = cb(zc) * H
    pts = [Vector((0.040, yb + 0.012, 1.786)), Vector((0.066, yb + 0.040, 1.772)), Vector((0.098, yb + 0.056, 1.750)),
           Vector((0.130, yb + 0.060, 1.722)), Vector((0.150, yb + 0.056, 1.690))]
    hs = K.hose("shoulder_hose_rear.L", pts, r=0.0048, bone="chest")
    left.append(hs)
    left += K.clamps_on("shoulder_hose_rear_clamp", pts, 0.0048, (0.22, 0.55, 0.85), bone="chest", mat="gunmetal")


def build_hose_front(left):
    """one neck-side hose per shoulder: from under the collar pad, down the inside of the cowl, into the socket ring."""
    pts = [Vector((0.098, -0.030, 1.714)), Vector((0.122, -0.040, 1.696)), Vector((0.152, -0.050, 1.676)), Vector((0.188, -0.0575, 1.656)),
           Vector((0.206, -0.0585, 1.640))]
    hs = K.hose("shoulder_hose_front.L", pts, r=0.0042, bone="chest")
    left.append(hs)
    left += K.clamps_on("shoulder_hose_front_clamp", pts, 0.0042, (0.30, 0.68), bone="chest", mat="silver")


# ================================================================================================ round-3 extras
def build_extras(left, mid):
    """plate-level structure added in conform round 3 (each is a real part of the on-model armour, none is a rivet):
    cavity bezel, a third tongue plate with two ribs, pad end caps, a fourth cowl tier, a Y-fork inlay, rear scapular lames."""
    ny = (0, -1, 0)
    # pewter bezel ring round the black hub cavity (the silver rim of the plate edge, f07/f08)
    left.append(K.bearing_ring("shoulder_cavity_bezel.L", (HX, -0.0618, HZ + 0.012), ny, 0.0772, 0.0735, 0.0030, mat="silver",
                               bone="pauldron.L", seg=56))
    # tongue: a third, shortest plate and two ridge ribs along the silver tongue
    n_u = 20
    a_lo, a_hi = -108.0, -64.0

    def plate_f(off, dy, dz, wscale):
        def f(u, v):
            a = a_hi + (a_lo - a_hi) * u
            p = horn_pt(off, a, 1.0)
            k = L.smoothstep(0.15, 1.0, u)
            fwd = Vector((0.010 * k, -0.040 * k * k + dy, -0.016 * k + dz))
            side = (v - 0.5) * 2.0
            w = 0.016 * wscale * (1.0 - 0.9 * k ** 0.8) * side
            rim = Vector((EX - p.x, 0.0, EZ - p.z)).normalized()
            return tuple(p + fwd + rim * (w * 0.6))
        return f
    ob = L.grid_surface("shoulder_tongue_tip.L", plate_f(0.020, -0.004, 0.0, 1.0), n_u, 5, thickness=0.006, offset=0.0)
    left.append(fin(ob, "silver", "pauldron.L", bevel=0.0014, seg=2, wear=None))
    for k, wv in enumerate((-0.35, 0.35)):
        pts = []
        for i in range(0, 15):
            u = i / 14.0
            a = a_hi + (a_lo - a_hi) * u
            p = horn_pt(0.030, a, 1.0)
            kk = L.smoothstep(0.15, 1.0, u)
            fwd = Vector((0.008 * kk, -0.046 * kk * kk - 0.0060, -0.020 * kk))
            rim = Vector((EX - p.x, 0.0, EZ - p.z)).normalized()
            pts.append(p + fwd + rim * (0.022 * (1.0 - 0.9 * kk ** 0.8) * wv * 0.6))
        rb = L.tube(f"shoulder_tongue_rib_{k + 1}.L", pts, 0.0016, nring=8, n_per_seg=2)
        left.append(fin(rb, "gunmetal", "pauldron.L", bevel=0, wear=None))
    # collar pads: a dark cap at each end of the lozenge (the C-hook takes one, the Y-fork the other)
    ya = surf_y(0.100, 1.724) - 0.004
    for k, (xx, zz) in enumerate(((0.052, 1.7195), (0.148, 1.7330))):
        left.append(K.washer_stack(f"shoulder_pad_cap_{k + 1}.L", (xx, ya - 0.0105, zz), ny, [(0.0105, 0.0020), (0.0082, 0.0018)],
                                   mat="gunmetal", bone="chest", seg=24))
    # Y-fork: a dark slot inlay down the stem (the pale slot bar of f07 under it)
    yf = surf_y(0.0, 1.711)
    zt = 1.741
    inl = prism("shoulder_yfork_inlay", L.outline_rrect(0.0070, 0.036, 0.0035, n=4),
                L.Frame.at((0, yf + 0.006 - 0.0182, zt - 0.040), z=(0, -1, 0), x=(1, 0, 0)), 0.0020)
    mid.append(fin(inl, "gunmetal", "chest", bevel=0.0004, seg=1, wear=None))
    # cowl: a fourth, lowest tier (the outer hem of the wing)
    dz = -0.050
    F0, F1 = Vector((0.205, -0.010, 1.728 + dz)), Vector((0.092, -0.014, 1.784 + dz))
    R0, R1 = Vector((0.205, 0.105, 1.742 + dz)), Vector((0.092, 0.095, 1.792 + dz))
    ob = cowl_plate("shoulder_cowl_d.L", F0, F1, R0, R1, 0.00, 0.14, crown=0.006, thick=0.007, dz=-0.0032)
    left.append(fin(ob, "gunmetal", "chest", bevel=0.0016, seg=2, wear=0))
    # rear scapular lames: four shingled teal plates under the claw blades, stepping toward the spine
    yb = cb(6.62)
    for k in range(4):
        z0 = 6.86 - 0.095 * k
        pts = [(0.10 + 0.035 * k, z0 - 0.07), (0.15 + 0.04 * k, z0 + 0.03), (0.60 - 0.02 * k, z0 + 0.03), (0.66 - 0.03 * k, z0 - 0.07)]
        left.append(wplate(f"shoulder_scap_{k + 1}.L", pts, yb + 0.020 + 0.006 * k, 1, 0.012, 0.012, 0.012, "teal", "chest", bevel=0.0018, wear=0.3))
    # two more clamps on the front hose and one on the rear hose
    pts = [Vector((0.098, -0.030, 1.714)), Vector((0.122, -0.040, 1.696)), Vector((0.152, -0.050, 1.676)), Vector((0.188, -0.0575, 1.656)),
           Vector((0.206, -0.0585, 1.640))]
    left += K.clamps_on("shoulder_hose_front_clamp_x", pts, 0.0042, (0.50, 0.84), bone="chest", mat="silver")


def build(): return _build()


def _build():
    left = []
    mid = []
    build_horn(left)
    build_hub(left)
    build_tongue(left)
    build_cup(left)
    build_collar(left, mid)
    build_cowl(left)
    build_rear(left, mid)
    build_rear_hw(left, mid)
    build_hose_front(left)
    build_extras(left, mid)
    res = list(left) + mid
    for ob in left:
        res.append(L.mirror_x(ob))
    return res
