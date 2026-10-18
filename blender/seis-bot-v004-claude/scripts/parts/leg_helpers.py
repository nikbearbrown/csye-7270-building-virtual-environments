"""leg_helpers - helpers private to the leg module (skin-hugging patches in metric coordinates, leaf outlines, bezel
rings, fasteners).  Nothing here edits the shared toolkit; it only calls seis_lib."""
import math
import bpy
import bmesh
from mathutils import Vector
import seis_lib as L

PI = math.pi


def sm(a, b, x):
    return L.smoothstep(a, b, x)


class Skin:
    """Metric coordinates on a Sweep: s = metres along the path from its start, w = metres sideways on the FRONT
    (+) or BACK face (back=True), or an explicit angle th (radians).  off = metres pushed outward."""

    def __init__(self, sw):
        self.sw = sw
        self.len = sw.path.length

    def theta(self, t, w, back=False):
        sec = self.sw.sec(t)
        rx = sec["rxp"] if w >= 0 else sec["rxn"]
        n = sec["n"]
        f = max(-0.9995, min(0.9995, w / rx))
        c = math.copysign(abs(f) ** (n / 2.0), f)
        th = math.acos(max(-1.0, min(1.0, c)))
        return -th if back else th

    def pos(self, s, w=0.0, off=0.0, back=False, th=None):
        t = L.clamp(s / self.len)
        if th is None:
            th = self.theta(t, w, back)
        return self.sw.point(t, th) + self.sw.outward(t, th) * off

    def width(self, s):
        return self.sw.sec(L.clamp(s / self.len))["rxp"]


def _orient_flip(P, nu, nv):
    """True if the (u, v) winding of grid P(u,v) opposes the geometric outward direction (checked at the centre)."""
    return None


def patch(sk, name, suv, off, nu=16, nv=12, thickness=0.006, back=False, thf=None, flip=None):
    """A plate over the skin.  suv(u, v) -> (s, w) or (s, None, theta); off(u, v) -> metres above the skin.
    Solid thickness grows inward."""
    def P(u, v):
        r = suv(u, v)
        if len(r) == 3:
            return sk.pos(r[0], 0.0, off(u, v), back=back, th=r[2])
        return sk.pos(r[0], r[1], off(u, v), back=back)

    if flip is None:
        eps = 0.02
        c = P(0.5, 0.5)
        du = P(0.5 + eps, 0.5) - P(0.5 - eps, 0.5)
        dv = P(0.5, 0.5 + eps) - P(0.5, 0.5 - eps)
        r = suv(0.5, 0.5)
        t = L.clamp(r[0] / sk.len)
        th = r[2] if len(r) == 3 else sk.theta(t, r[1], back)
        n = sk.sw.outward(t, th)
        flip = du.cross(dv).dot(n) < 0
    return L.grid_surface(name, P, nu, nv, thickness=thickness, flip=flip)


def loop_surface(name, P, nu, nv, thickness=0.004, flip=False):
    """Closed-loop strip: u wraps (nu points around), v across (nv+1 rows).  Solidified inward."""
    verts = []
    for i in range(nu):
        for j in range(nv + 1):
            verts.append(Vector(P(i / nu, j / nv)))
    W = nv + 1
    faces = []
    for i in range(nu):
        i2 = (i + 1) % nu
        for j in range(nv):
            faces.append((i * W + j, i2 * W + j, i2 * W + j + 1, i * W + j + 1))
    if flip:
        faces = [tuple(reversed(q)) for q in faces]
    ob = L.new_mesh(name, verts, faces)
    if thickness > 0:
        m = ob.modifiers.new("Solidify", "SOLIDIFY")
        m.thickness = thickness
        m.offset = -1.0
        m.use_even_offset = True
        m.use_rim = True
        L.apply_modifiers(ob)
    return ob


# ------------------------------------------------------------------------------------------------ leaf outlines
def leaf_hw(u, hwmax, peak=0.4, hwmin=0.0015, sharp=0.8):
    k = math.log(0.5) / math.log(max(peak, 0.05))
    return max(hwmin, hwmax * math.sin(PI * (min(max(u, 0.0), 1.0) ** k)) ** sharp)


def leaf_outline(s0, length, w0, hwmax, peak=0.4, n=24, sharp=0.8, hwmin=0.0015, skew=0.0):
    """Closed outline (list of (s, w)) of a leaf: starts at the top tip, runs down the +w side, back up the -w side."""
    pts = []
    for i in range(n + 1):
        u = i / n
        pts.append((s0 + length * u, w0 + skew * (u - 0.5) + leaf_hw(u, hwmax, peak, hwmin, sharp)))
    for i in range(n - 1, 0, -1):
        u = i / n
        pts.append((s0 + length * u, w0 + skew * (u - 0.5) - leaf_hw(u, hwmax, peak, hwmin, sharp)))
    return pts


def offset_outline(pts, d):
    """Offset a closed (s, w) outline outward by d metres (d<0 shrinks), using the centroid for the sign."""
    cx = sum(p[0] for p in pts) / len(pts)
    cy = sum(p[1] for p in pts) / len(pts)
    out = []
    m = len(pts)
    for i in range(m):
        a, b, c = pts[i - 1], pts[i], pts[(i + 1) % m]
        tx, ty = c[0] - a[0], c[1] - a[1]
        ln = math.hypot(tx, ty) or 1.0
        nx, ny = ty / ln, -tx / ln
        if (b[0] - cx) * nx + (b[1] - cy) * ny < 0:
            nx, ny = -nx, -ny
        out.append((b[0] + nx * d, b[1] + ny * d))
    return out


def ring(sk, name, outline, d_out, h_fn, thickness=0.004, d_in=0.0, back=False, nv=4):
    """Raised bezel ring around an (s, w) outline: inner edge at d_in, outer edge at d_out; h_fn(v) = height above skin
    (v = 0 inner edge, 1 outer edge)."""
    inner = offset_outline(outline, d_in)
    outer = offset_outline(outline, d_out)
    m = len(outline)

    def P(u, v):
        i = min(int(round(u * m)), m - 1)
        a, b = inner[i], outer[i]
        s = a[0] + (b[0] - a[0]) * v
        w = a[1] + (b[1] - a[1]) * v
        return sk.pos(s, w, h_fn(v), back=back)

    # orientation test at index 0 / v=.5
    eps = 1.0 / m
    c = P(0.0, 0.5)
    du = P(eps, 0.5) - P(-eps if False else 0.0, 0.5)
    dv = P(0.0, 0.8) - P(0.0, 0.2)
    s0 = (inner[0][0] + outer[0][0]) / 2
    w0 = (inner[0][1] + outer[0][1]) / 2
    t = L.clamp(s0 / sk.len)
    n = sk.sw.outward(t, sk.theta(t, w0, back))
    flip = du.cross(dv).dot(n) < 0
    return loop_surface(name, P, m, nv, thickness=thickness, flip=flip)


def leaf_patch(sk, name, s0, length, w0, hwmax, peak, height_fn, base, thickness=0.006, back=False, nu=20, nv=10,
               hwmin=0.0015, sharp=0.8, skew=0.0):
    """Convex leaf plate: width follows leaf_hw; height = base + height_fn(u, v)."""
    def suv(u, v):
        hw = leaf_hw(u, hwmax, peak, hwmin, sharp)
        return (s0 + length * u, w0 + hw * (2 * v - 1) + skew * (u - 0.5))

    return patch(sk, name, suv, lambda u, v: base + height_fn(u, v), nu=nu, nv=nv, thickness=thickness, back=back)


def lens(h, p=1.0, pu=1.0):
    """pillow height profile: h * sin(pi u)^pu * sin(pi v)^p"""
    return lambda u, v: h * (math.sin(PI * u) ** pu) * (math.sin(PI * v) ** p)


# ------------------------------------------------------------------------------------------------ fasteners
def bolts_on(sk, points, kind="hex", radius=0.005, height=0.0035, back=False, name="bolts"):
    """points: list of (s, w, off[, th]) -> one joined mesh of hex bolts / rivets lying on the skin."""
    objs = []
    for i, p in enumerate(points):
        s, w, off = p[0], p[1], p[2]
        th = p[3] if len(p) > 3 else None
        t = L.clamp(s / sk.len)
        th_ = th if th is not None else sk.theta(t, w, back)
        c = sk.sw.point(t, th_) + sk.sw.outward(t, th_) * off
        n = sk.sw.outward(t, th_)
        if kind == "hex":
            o = L.bolt(f"{name}_{i}", c, n, radius=radius, height=height, hexagon=True)
        else:
            o = L.cylinder(f"{name}_{i}", radius, height, L.Frame.at(c + n * (height / 2), n), segments=14)
        objs.append(o)
    return L.join(objs, name)


def bolt_line(sk, s_list, w, off, **kw):
    return bolts_on(sk, [(s, w, off) for s in s_list], **kw)


def world_bolt(name, c, n, r=0.005, h=0.004, seg=6):
    return L.bolt(name, c, n, radius=r, height=h, hexagon=(seg == 6))


def merge_group(objs, name):
    objs = [o for o in objs if o is not None]
    return L.join(objs, name)
