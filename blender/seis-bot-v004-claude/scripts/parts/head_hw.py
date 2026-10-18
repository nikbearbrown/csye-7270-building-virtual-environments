"""head_hw - round-2 hardware for the head and neck: bearing races, hinge pins with washers, clevis straps, bezels, cup screws,
ear brackets, a dome strap.  Everything is small and tidy (fasteners 4-6 mm): detail on top of the clean on-model look.
All objects are separate meshes with a material and a bone (head / neck)."""
import math
from mathutils import Vector
import seis_lib as L
import head_lib as H
import head_face as F
import head_neck as N
from head_lib import both, loop_tube, FACE, SK, CREST, prof, ends, oval, on_surface

OUT = None
SKIP = ("head_eye_screw", "head_keystone_bolt", "head_forehead_bolt", "head_cheek_bolt", "head_ear_strut_bolt")


def _frame(p, n, xh=(0, 0, 1)):
    return L.Frame.at(p, n, xh)


def bolt(name, p, n, r=0.0026, h=0.0024, mat="gunmetal", bone="head", hexagon=True, mirror=True, bevel=0.0004):
    if name.startswith(SKIP):
        return None
    if hexagon:
        b = L.bolt(name, p, n, r, h, hexagon=True, xhint=(0, 0, 1))
        L.finish(b, mat, bevel=bevel, bevel_segments=1, bone=bone, wear=0.0)
    else:
        fr = L.Frame.at(p, n, (0, 0, 1))
        b = L.cylinder(name, r, h, L.Frame(fr.p(0, 0, h / 2), fr.x, fr.y, fr.z), segments=10, radius2=r * 0.86)
        L.finish(b, mat, bevel=0, bone=bone, wear=0.0)
    if mirror:
        both(b, OUT)
    else:
        OUT.append(b)
    return b


def washer_pin(name, p, n, r_w=0.0050, r_p=0.0030, mat="pewter", pin_mat=None, bone="head", mirror=True):
    """a stepped disc: thin washer + pin head (one object)"""
    ds = L.disc_stack(name, p, n, [(r_w, 0.0012), (r_p, 0.0030)], segments=12, xhint=(0, 0, 1))
    L.finish(ds, mat, bevel=0.0004, bevel_segments=1, bone=bone, wear=0.0)
    if mirror:
        both(ds, OUT)
    else:
        OUT.append(ds)
    return ds


def neck_tangent(z, ang):
    e = 1e-3
    return (N.neck_pt(z, ang + e, 0.0) - N.neck_pt(z, ang - e, 0.0)).normalized()


def neck_normal(z, ang):
    return (N.neck_pt(z, ang, 0.01) - N.neck_pt(z, ang, 0.0)).normalized()


def neck_hw():
    # ---- bearing races: top (under the head) and base (at the collar)
    for nm, z, mat, r in (("neck_race_top", 1.8238, "gunmetal", 0.0026), ("neck_race_base", 1.7452, "gunmetal", 0.0026),
                          ("neck_race_top_lip", 1.8268, "pewter_shade", 0.0016)):
        pts = [N.neck_pt(z, 2 * math.pi * i / 48, N.SLAB_OUT + 0.0006) for i in range(48)]
        t = loop_tube(nm, pts, r, nring=8)
        L.finish(t, mat, bevel=0, bone="neck", wear=0.0)
        OUT.append(t)
    # ---- six round-head screws on the top race (per side), pitch ~ even on the front half
    for j, ang in enumerate((0.45, 0.80, 1.15, 1.50, 1.85, 2.20)):
        P = N.neck_pt(1.8238, ang, N.SLAB_OUT + 0.0020)
        bolt(f"neck_race_screw_{j}.L", P, neck_normal(1.8238, ang), r=0.0021, h=0.0017, mat="pewter", bone="neck", hexagon=False)
    # ---- hinge pins with washers at the side of every slab
    for i in range(N.SLAB_N):
        z = N.SLAB_Z0 + N.SLAB_PITCH * i + N.SLAB_H * 0.5
        ang = 1.62
        P = N.neck_pt(z, ang, N.SLAB_OUT * 0.95)
        washer_pin(f"neck_hinge_pin_{i}.L", P, neck_normal(z, ang), r_w=0.0048, r_p=0.0027, mat="pewter", bone="neck")
    # ---- clevis link straps bridging the dark gaps between slabs (front and rear of each side)
    for g in range(N.SLAB_N - 1):
        zg = N.SLAB_Z0 + N.SLAB_PITCH * (g + 1) - (N.SLAB_PITCH - N.SLAB_H) * 0.5 + N.SLAB_H * 0.0
        zg = N.SLAB_Z0 + N.SLAB_PITCH * g + N.SLAB_H + (N.SLAB_PITCH - N.SLAB_H) * 0.5
        for k, ang in enumerate((0.62, 2.45)):
            P = N.neck_pt(zg, ang, N.SLAB_OUT + 0.0010)
            tg = neck_tangent(zg, ang)
            fr = L.Frame.at(P, Vector((0, 0, 1)), tg)
            bx = L.box(f"neck_clevis_{g}_{k}.L", (0.0125, 0.0032, 0.0100), L.Frame(P, fr.x, fr.y, fr.z))
            L.finish(bx, "gunmetal", bevel=0.0005, bevel_segments=1, bone="neck", wear=0.0)
            both(bx, OUT)
            for sgn in (-1, 1):
                Pb = P + fr.x * (0.0042 * sgn) + neck_normal(zg, ang) * 0.0017
                bolt(f"neck_clevis_bolt_{g}_{k}_{'a' if sgn < 0 else 'b'}.L", Pb, neck_normal(zg, ang), r=0.0015, h=0.0012,
                     mat="pewter", bone="neck", hexagon=False)
    # ---- throat panel corner screws
    for j, (x, z) in enumerate(((0.0330, 1.7458), (0.0330, 1.8195))):
        P, nrm = N.NC.map(x, z)
        bolt(f"neck_throat_screw_{j}.L", P + nrm * 0.0038, nrm, r=0.0021, h=0.0016, mat="pewter", bone="neck", hexagon=False)


def face_hw():
    cx, cz = F.f8(543, 614)
    ang = 8.0
    # ---- eye bezel ring (thin pewter lip round the recessed socket) and two screws on its long axis
    sock = oval(cx, cz, 0.0418, 0.0362, ang, n=36, power=2.3)
    pts = on_surface(FACE, sock, 0.0010)
    bz = loop_tube("head_eye_bezel.L", pts, 0.00095, nring=6)
    L.finish(bz, "pewter_shade", bevel=0, bone="head", wear=0.0)
    both(bz, OUT)
    ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    for j, sgn in enumerate((-1, 1)):
        x, z = cx + sgn * 0.0262 * ca, cz + sgn * 0.0262 * sa
        P, nrm = FACE.map(x, z)
        bolt(f"head_eye_screw_{j}.L", P + nrm * 0.0007, nrm, r=0.0016, h=0.0015, mat="gunmetal", hexagon=False)
    # ---- keystone: two hex bolts on the middle step
    for j, sx in enumerate((-1, 1)):
        x, z = sx * 0.0145, F.f8(390, 388)[1]
        P, nrm = FACE.map(x, z)
        bolt(f"head_keystone_bolt_{j}", P + nrm * 0.0040, nrm, r=0.0026, h=0.0021, mat="pewter", mirror=False)
    # ---- forehead outer panel corner bolts (3 per side) and cheek plate bolts (2 per side)
    for j, (X, Y) in enumerate(((676, 362), (686, 470), (498, 368))):
        x, z = F.f8(X, Y)
        P, nrm = FACE.map(x, z)
        bolt(f"head_forehead_bolt_{j}.L", P + nrm * 0.0013, nrm, r=0.0024, h=0.0020, mat="pewter")
    for j, (X, Y) in enumerate(((606, 672), (562, 770))):
        x, z = F.f8(X, Y)
        P, nrm = FACE.map(x, z)
        bolt(f"head_cheek_bolt_{j}.L", P + nrm * 0.0013, nrm, r=0.0022, h=0.0019, mat="pewter")


def cup_hw():
    D, n = H.DISC_C, H.DISC_N
    fr = L.Frame.at(D, n, (0, 0, 1))
    for j in range(6):
        a = 2 * math.pi * (j + 0.5) / 6
        P = D - n * 0.0138 + (fr.x * math.cos(a) + fr.y * math.sin(a)) * 0.0294
        bolt(f"head_cup_screw_{j}.L", P, n, r=0.0017, h=0.0016, mat="pewter", hexagon=False)
    # a thin dark seal ring (gasket) between the cup rim and the cheek arc
    pts = [D + (fr.x * math.cos(2 * math.pi * i / 40) + fr.y * math.sin(2 * math.pi * i / 40)) * 0.0388 + n * 0.0012 for i in range(40)]
    gk = loop_tube("head_cup_gasket.L", pts, 0.0015, nring=6)
    L.finish(gk, "dark", bevel=0, bone="head", wear=0.0, apply=False)
    both(gk, OUT)


def ear_hw():
    e = 0.002
    for j, u in enumerate((0.15, 0.85)):
        v = 0.10
        Ps = F.ear_pt(u, v, -0.0052)                  # on the shell's inner liner
        # strut from the skull surface out to the shell (horizontal, along x)
        dy = Ps.y - SK.yc
        arg = 1.0 - (dy / SK.b(-dy)) ** 2 - ((Ps.z - SK.zc) / SK.cz(Ps.z - SK.zc)) ** 2
        xs = SK.a * math.sqrt(max(arg, 0.0)) if arg > 0 else 0.0
        x0 = max(xs - 0.002, 0.03)
        x1 = Ps.x + 0.001
        if x1 - x0 < 0.004:
            continue
        L_ = x1 - x0
        fr = L.Frame((((x0 + x1) / 2), Ps.y, Ps.z), (1, 0, 0), (0, 1, 0), (0, 0, 1))
        bx = L.box(f"head_ear_strut_{j}.L", (L_, 0.0095, 0.0042), fr)
        L.finish(bx, "pewter_shade", bevel=0.0007, bevel_segments=1, bone="head", wear=0.0)
        both(bx, OUT)
        # bolt head on the shell's outer face above the strut
        Po = F.ear_pt(u, v, 0.0)
        nq = (F.ear_pt(u, v + e) - F.ear_pt(u, v - e)).cross(F.ear_pt(u + e, v) - F.ear_pt(u - e, v)).normalized()
        if nq.x < 0:
            nq = -nq
        bolt(f"head_ear_strut_bolt_{j}.L", Po + nq * 0.0004, nq, r=0.0030, h=0.0022, mat="pewter")


def dome_hw():
    sk = SK
    psi0, w = 196.0, 3.2

    def st(u, v):
        return (-0.88 + 1.76 * v) * sk.a, math.radians(psi0 - w + 2 * w * u) * CREST.RT
    strap = H.chart_grid("head_dome_strap", CREST, st, 6, 30, lambda u, v: 0.0036 * prof(u, 0.5) * ends(v, 0.03) ** 0.5, 0.004)
    L.finish(strap, "pewter", bevel=0.0010, bevel_segments=2, bone="head", wear=0.0, weighted=False)
    OUT.append(strap)
    for j, xi in enumerate((0.0, 0.36, 0.72)):
        for s in ((1, -1) if xi else (1,)):
            P, nrm = CREST.map(s * xi * sk.a, math.radians(psi0) * CREST.RT)
            nm = f"head_dome_strap_bolt_{j}" + (".L" if (xi and s == 1) else ("" if not xi else ".R"))
            b = L.bolt(nm, P + nrm * 0.0034, nrm, 0.0027, 0.0022, hexagon=True, xhint=(0, 0, 1))
            L.finish(b, "gunmetal", bevel=0.0004, bevel_segments=1, bone="head", wear=0.0)
            OUT.append(b)


def build(out):
    global OUT
    OUT = out
    neck_hw()
    face_hw()
    cup_hw()
    ear_hw()
    dome_hw()
    return out
