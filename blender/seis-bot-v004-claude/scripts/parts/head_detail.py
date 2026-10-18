"""head_detail - fasteners, hinge bearings, cables, hoses and clamps for the head and neck (built after the rest)."""
import math
from mathutils import Vector
import seis_lib as L
import seis_spec as S
import head_lib as H
import head_face as F
import head_neck as N
from head_lib import both, loop_tube, FACE, SK

OUT = None


# round 3 (ONMODEL: clean glossy finish, no rivet rows on the head): these fasteners are NOT built any more
SKIP = ("head_yoke_bolt", "head_yoke_centre_bolt", "head_arc_bolt", "head_hinge_bolt", "head_ear_rivet")


def hexbolt(name, p, n, r=0.0035, h=0.003, mat="pewter", side=True, bone="head"):
    if name.startswith(SKIP):
        return None
    b = L.bolt(name, p, n, r, h, hexagon=True, xhint=(0, 0, 1))
    L.finish(b, mat, bevel=0.0005, bevel_segments=1, bone=bone, wear=0.0)
    if side:
        both(b, OUT)
    else:
        OUT.append(b)
    return b


def clamp_ring(name, c, axis, r, bone, mat="gunmetal", w=0.0035):
    fr = L.Frame.at(c, axis, (0, 0, 1))
    pts = [c + (fr.x * math.cos(2 * math.pi * i / 20) + fr.y * math.sin(2 * math.pi * i / 20)) * r for i in range(14)]
    t = loop_tube(name, pts, 0.0017, nring=5, ry=w / 2)
    L.finish(t, mat, bevel=0, bone=bone, wear=0.0)
    return t


def build(out):
    global OUT
    OUT = out
    # ------------------------------------------------------------------ yoke bolts (arms + centre)
    sw = F.YOKE_SW
    D, n = F.DISC_C, F.DISC_N
    fr = L.Frame.at(D, n, (0, 0, 1))
    hv, uv = -fr.y, fr.x
    k = 0
    for a in (-70, -35, 0, 35, 65):
        r = math.radians(a)
        P = D + (hv * math.cos(r) + uv * math.sin(r)) * 0.0445 + n * 0.0118
        hexbolt(f"head_yoke_bolt_{k}.L", P, n, 0.0030, 0.0028, mat="pewter")
        k += 1
    for j, t in enumerate((0.40, 0.60)):
        P = sw.point(t, math.pi / 2, 0.0006)
        nn = sw.outward(t, math.pi / 2)
        hexbolt(f"head_yoke_centre_bolt_{j}", P, nn, 0.0030, 0.0028, side=False)

    # ------------------------------------------------------------------ brow rivets, cheek rivets (on the face shell)
    for j, (X, Y) in enumerate(()):
        x, z = H.pxz(X, Y)
        P, nrm = FACE.map(x, z)
        rv = L.cylinder(f"head_rivet_{j}.L", 0.0020, 0.0026, L.Frame(P + nrm * (0.0072 if j < 2 else 0.0030), *_axes(nrm)), segments=12)
        L.finish(rv, "pewter", bevel=0.0005, bevel_segments=1, bone="head", wear=0.0)
        both(rv, out)

    # cheek-arc fasteners: three small bolts along the arc, a washer at each end
    D2 = D
    for j, ang in enumerate((125, 160, 195, 230)):
        r_ = math.radians(ang)
        P = D2 + (hv * math.cos(r_) + uv * math.sin(r_)) * 0.0470 + n * 0.0098
        hexbolt(f"head_arc_bolt_{j}.L", P, n, 0.0024, 0.0022, mat="gunmetal")
    # ------------------------------------------------------------------ ear-shell hinge bearing (outer face, lower front) + 6 bolts
    # (ear hinge bearing removed in round 3: f06/f10/f12 show a plain cupped shell)
    e = 0.002
    # a row of small rivets along the shell's front edge (outer face)
    for i in range(7):
        u = 0.14 + 0.72 * i / 6
        Pq = F.ear_pt(u, 0.06, 0.0006)
        nq = (F.ear_pt(u, 0.06 + e) - F.ear_pt(u, 0.06 - e)).cross(F.ear_pt(u + e, 0.06) - F.ear_pt(u - e, 0.06)).normalized()
        if nq.x < 0:
            nq = -nq
        hexbolt(f"head_ear_rivet_{i}.L", Pq, nq, 0.0017, 0.0020, mat="pewter")

    # ------------------------------------------------------------------ neck: hex bolts on every slab, cables, clamps
    for i in range(N.SLAB_N):
        z = N.SLAB_Z0 + N.SLAB_PITCH * i + N.SLAB_H * 0.5
        for j, ang in enumerate((0.78, 1.42)):
            P = N.neck_pt(z, ang, N.SLAB_OUT * 0.96)
            nn = N.neck_pt(z, ang, 0.01) - N.neck_pt(z, ang, 0.0)
            hexbolt(f"neck_slab_bolt_{i}_{j}.L", P, nn.normalized(), 0.0024, 0.0026, bone="neck", mat="gunmetal")
    # one dark-red cable per side runs down the side of the neck from behind the ear pod (frame 10), with clamps;
    # two thin dark cables beside it at the back of the neck
    for j, (ang0, mat) in enumerate(((1.95, "red"), (2.55, "dark"), (2.85, "dark"))):
        pts = []
        for zz, tw in ((1.842, 0.0), (1.818, 0.05), (1.796, -0.04), (1.772, 0.03), (1.745, 0.0)):
            pts.append(N.neck_pt(zz, ang0 + tw, N.SLAB_OUT + 0.0042))
        cb = L.tube(f"neck_cable_{j}.L", pts, 0.0030 if j else 0.0034, nring=8)
        L.finish(cb, mat, bevel=0, bone="neck")
        both(cb, out)
        for jj in (1, 3):
            c = pts[jj]
            tg = (pts[jj + 1] - pts[jj - 1]).normalized()
            cr = clamp_ring(f"neck_cable_clamp_{j}_{jj}.L", c, tg, 0.0042, "neck")
            both(cr, out)

    return out


def _axes(nrm):
    fr = L.Frame.at((0, 0, 0), nrm, (0, 0, 1))
    return (fr.x, fr.y, fr.z)


def _neck_sweep():
    path = [Vector((0.0, N.yc(z), z)) for z in (N.NECK_Z0, 1.78, 1.84, N.NECK_Z1)]
    keys = [(0.0, N.rx_(N.NECK_Z0), N.ry_(N.NECK_Z0), 2.6), (0.5, N.rx_(1.8), N.ry_(1.8), 2.6),
            (1.0, N.rx_(N.NECK_Z1), N.ry_(N.NECK_Z1), 2.6)]
    return L.Sweep(path, keys)
