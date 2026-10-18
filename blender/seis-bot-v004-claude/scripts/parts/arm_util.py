"""arm_util - helpers for parts/arm.py (skin-hugging patches, rings, outlines).  Only this module and arm.py use it."""
import math
import bpy
import bmesh
from mathutils import Vector, Matrix
import seis_lib as L
import seis_spec as S

PI = math.pi
H = S.H


def hz(h):
    return h * H


def sstep(a, b, x):
    return L.smoothstep(a, b, x)


def tz(sw, z):
    """arc-length fraction t of a (mostly vertical, z decreasing) Sweep at world height z (m)."""
    path = sw.path
    a, b = 0.0, 1.0
    dec = path.at(1.0).z < path.at(0.0).z
    for _ in range(36):
        m = 0.5 * (a + b)
        if (path.at(m).z > z) == dec:
            a = m
        else:
            b = m
    return 0.5 * (a + b)


def skin_n(sw, t, th, e=0.0015):
    """(point on skin, outward unit normal)"""
    t = L.clamp(t)
    p = sw.point(t, th)
    t1, t2 = L.clamp(t + 0.002), L.clamp(t - 0.002)
    a = sw.point(t1, th) - sw.point(t2, th)
    b = sw.point(t, th + 0.01) - sw.point(t, th - 0.01)
    n = a.cross(b)
    if n.length < 1e-14:
        n = Vector((0, 0, 1))
    n.normalize()
    Pt, T, X, Y = sw.frame(t)
    s = sw.sec(t)
    c = Pt + X * s["ox"] + Y * s["oy"]
    if (p - c).dot(n) < 0:
        n = -n
    return p, n


def patch(sw, name, fn, nu, nv, thickness=0.006, holes=(), offset=-1.0, closed_v=False):
    """Surface hugging the Sweep skin.  fn(u, v) -> (t, theta, off) with u, v in [0, 1].
    The surface is the skin point at (t, theta) pushed `off` metres along the outward normal.
    holes: callables (u, v) -> bool; quads whose centre is inside are dropped (the ragged edge is hidden by a bezel).
    thickness > 0 solidifies INWARD, so the result is a closed solid."""
    verts, normals = [], []
    for i in range(nu + 1):
        for j in range(nv + 1):
            t, th, off = fn(i / nu, j / nv)
            p, n = skin_n(sw, t, th)
            verts.append(p + n * off)
            normals.append(n)
    W = nv + 1
    faces = []
    for i in range(nu):
        for j in range(nv):
            uc, vc = (i + 0.5) / nu, (j + 0.5) / nv
            if any(h(uc, vc) for h in holes):
                continue
            faces.append((i * W + j, (i + 1) * W + j, (i + 1) * W + j + 1, i * W + j + 1))
    # orientation: make face normal agree with the skin outward normal
    f0 = faces[len(faces) // 2]
    fn0 = (verts[f0[1]] - verts[f0[0]]).cross(verts[f0[3]] - verts[f0[0]])
    if fn0.dot(normals[f0[0]]) < 0:
        faces = [tuple(reversed(f)) for f in faces]
    used = sorted({v for f in faces for v in f})
    remap = {v: k for k, v in enumerate(used)}
    ob = L.new_mesh(name, [verts[v] for v in used], [tuple(remap[v] for v in f) for f in faces])
    if thickness > 0:
        m = ob.modifiers.new("Solidify", "SOLIDIFY")
        m.thickness = thickness
        m.offset = offset
        m.use_even_offset = True
        m.use_rim = True
        L.apply_modifiers(ob)
    return ob


def rr_in(a, b, ha, hb, r):
    """inside test of a rounded rectangle centred (0,0) with half sizes ha, hb, corner radius r (in a,b units)"""
    a, b = abs(a), abs(b)
    if a > ha or b > hb:
        return False
    if a > ha - r and b > hb - r:
        return (a - (ha - r)) ** 2 + (b - (hb - r)) ** 2 <= r * r
    return True


def rr_sdf(a, b, ha, hb, r):
    """signed distance-ish to rounded rect (negative inside)"""
    qa, qb = abs(a) - (ha - r), abs(b) - (hb - r)
    return math.hypot(max(qa, 0), max(qb, 0)) + min(max(qa, qb), 0) - r


class Spot:
    """A place on a Sweep skin: centre (z metres, theta rad).  AB coordinates: A = metres DOWN the limb, B = metres
    ALONG THE SECTION PERIMETER from the centre (toward increasing theta), so a window drawn in AB keeps its true size
    even on a flat, superelliptic face."""

    def __init__(self, sw, z, th):
        self.sw, self.z, self.th = sw, z, th
        self.t = tz(sw, z)
        sec = sw.sec(self.t)
        # perimeter table around th
        self._ths, self._ss = [], []
        N = 1440
        pts = [sw.local_xy(self.t, th + (k - N // 2) * 2 * PI / N, 0.0, sec) for k in range(N + 1)]
        acc = 0.0
        ss = [0.0]
        for k in range(1, N + 1):
            acc += math.hypot(pts[k][0] - pts[k - 1][0], pts[k][1] - pts[k - 1][1])
            ss.append(acc)
        s0 = ss[N // 2]
        self._ss = [s - s0 for s in ss]
        self._ths = [th + (k - N // 2) * 2 * PI / N for k in range(N + 1)]

    def _th_of_s(self, s):
        ss, ths = self._ss, self._ths
        if s <= ss[0]:
            return ths[0]
        if s >= ss[-1]:
            return ths[-1]
        lo, hi = 0, len(ss) - 1
        while hi - lo > 1:
            m = (lo + hi) // 2
            if ss[m] <= s:
                lo = m
            else:
                hi = m
        f = (s - ss[lo]) / max(ss[hi] - ss[lo], 1e-12)
        return ths[lo] + (ths[hi] - ths[lo]) * f

    def _s_of_th(self, th):
        ss, ths = self._ss, self._ths
        f = (th - ths[0]) / (ths[-1] - ths[0]) * (len(ths) - 1)
        i = int(L.clamp(f, 0, len(ths) - 2))
        return ss[i] + (ss[i + 1] - ss[i]) * (f - i)

    def zt(self, A, B):
        z = self.z - A
        return tz(self.sw, z), self._th_of_s(B)

    def AB(self, z, th):
        return self.z - z, self._s_of_th(th)

    def frame(self, off=0.0):
        p, n = skin_n(self.sw, self.t, self.th)
        T = self.sw.frame(self.t)[1]
        x = T.cross(n)
        if x.length < 1e-9:
            x = Vector((1, 0, 0))
        x.normalize()
        return L.Frame(p + n * off, x, n.cross(x), n)


def radial_fill(sw, name, spot, inside, centre=(0.0, 0.0), off=lambda r: 0.0, nu=64, nv=6, rmax=0.2, thickness=0.003):
    """Convex-ish region filled by a polar grid.  inside(A, B) -> bool; the boundary along each ray from `centre`
    is found by bisection.  off(frac) = height above the skin at radial fraction frac (0 centre .. 1 edge)."""
    verts, normals = [], []
    cA, cB = centre
    for i in range(nu):
        a = 2 * PI * i / nu
        dA, dB = math.cos(a), math.sin(a)
        lo, hi = 0.0, rmax
        for _ in range(22):
            m = 0.5 * (lo + hi)
            if inside(cA + dA * m, cB + dB * m):
                lo = m
            else:
                hi = m
        R = lo
        for k in range(nv + 1):
            f = k / nv
            t, th = spot.zt(cA + dA * R * f, cB + dB * R * f)
            p, n = skin_n(sw, t, th)
            if k == 0 and i > 0:
                verts.append(verts[0])
                normals.append(normals[0])
                continue
            verts.append(p + n * off(f))
            normals.append(n)
    W = nv + 1
    faces = []
    for i in range(nu):
        i2 = (i + 1) % nu
        for k in range(nv):
            faces.append((i * W + k, i2 * W + k, i2 * W + k + 1, i * W + k + 1))
    f0 = faces[nv + 1]
    fn0 = (verts[f0[1]] - verts[f0[0]]).cross(verts[f0[3]] - verts[f0[0]])
    if fn0.dot(normals[f0[0]]) < 0:
        faces = [tuple(reversed(f)) for f in faces]
    ob = L.new_mesh(name, verts, faces)
    weld_loose(ob)
    if thickness > 0:
        m = ob.modifiers.new("Solidify", "SOLIDIFY")
        m.thickness = thickness
        m.offset = -1.0
        m.use_even_offset = True
        m.use_rim = True
        L.apply_modifiers(ob)
    return ob


def ring_surface(sw, name, spot, outline, prof, nu=48, thickness=0.004):
    """A frame (bezel) around an outline hugging the skin.
    outline(a) -> (A, B) metres at angle a for the OUTLINE itself; its outward offset by w metres is approximated by
    pushing each point radially from the spot centre by w.  prof = [(v, w, off), ...]: w = outward distance of this
    cross-section station from the outline (negative = inside it), off = height above the skin."""
    verts, normals = [], []
    nv = len(prof) - 1
    for i in range(nu):
        a = 2 * PI * i / nu
        A, B = outline(a)
        ln = math.hypot(A, B) or 1e-9
        for (v, w, off) in prof:
            # push along the outline's own outward normal (numeric)
            e = 1e-3
            A2, B2 = outline(a + e)
            A1, B1 = outline(a - e)
            tx, ty = A2 - A1, B2 - B1
            tl = math.hypot(tx, ty) or 1e-9
            nx, ny = ty / tl, -tx / tl           # outward for a counter-clockwise outline in (A, B)
            if nx * A + ny * B < 0:
                nx, ny = -nx, -ny
            t, th = spot.zt(A + nx * w, B + ny * w)
            p, n = skin_n(sw, t, th)
            verts.append(p + n * off)
            normals.append(n)
    W = nv + 1
    faces = []
    for i in range(nu):
        i2 = (i + 1) % nu
        for j in range(nv):
            faces.append((i * W + j, i2 * W + j, i2 * W + j + 1, i * W + j + 1))
    f0 = faces[0]
    fn0 = (verts[f0[1]] - verts[f0[0]]).cross(verts[f0[3]] - verts[f0[0]])
    if fn0.dot(normals[f0[0]]) < 0:
        faces = [tuple(reversed(f)) for f in faces]
    ob = L.new_mesh(name, verts, faces)
    if thickness > 0:
        m = ob.modifiers.new("Solidify", "SOLIDIFY")
        m.thickness = thickness
        m.offset = -1.0
        m.use_even_offset = False
        m.use_rim = True
        L.apply_modifiers(ob)
    return ob


def superellipse(ha, hb, n=2.6):
    def f(a):
        c, s = math.cos(a), math.sin(a)
        return ha * L.spow(c, 2 / n), hb * L.spow(s, 2 / n)
    return f


def super_in(A, B, ha, hb, n=2.6):
    return abs(A / ha) ** n + abs(B / hb) ** n <= 1.0


def lathe(name, frame, profile, segments=48, smooth=True):
    """Solid of revolution about the frame's z.  profile = [(radius, z), ...] from the axis outwards and back
    (closed polyline, first and last points on the axis r=0)."""
    verts, faces = [], []
    n = len(profile)
    for k in range(segments):
        a = 2 * PI * k / segments
        ca, sa = math.cos(a), math.sin(a)
        for (r, z) in profile:
            verts.append(frame.p(r * ca, r * sa, z))
    for k in range(segments):
        k2 = (k + 1) % segments
        for j in range(n - 1):
            faces.append((k * n + j, k * n + j + 1, k2 * n + j + 1, k2 * n + j))
    ob = L.new_mesh(name, verts, faces, smooth)
    # outward check
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    bm.to_mesh(ob.data)
    bm.free()
    ob.data.update()
    return ob


def weld_loose(ob):
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    bmesh.ops.remove_doubles(bm, verts=bm.verts[:], dist=1e-6)
    loose = [v for v in bm.verts if not v.link_faces]
    if loose:
        bmesh.ops.delete(bm, geom=loose, context="VERTS")
    bm.to_mesh(ob.data)
    bm.free()
    ob.data.update()
    return ob


# ------------------------------------------------------------------ stadium (pill) helpers, added for the on-model conform
def stadium_outline(ha, r):
    """outline(a) -> (A, B) of a vertical pill: half length ha (down the limb), half width r.  a in [0, 2pi)."""
    s = max(ha - r, 1e-6)
    P = 4 * s + 2 * PI * r

    def f(a):
        t = (a % (2 * PI)) / (2 * PI) * P
        if t < 2 * s:                               # right side, going down
            return -s + t, r
        t -= 2 * s
        if t < PI * r:                              # bottom cap
            p = t / r
            return s + r * math.sin(p), r * math.cos(p)
        t -= PI * r
        if t < 2 * s:                               # left side, going up
            return s - t, -r
        t -= 2 * s
        p = t / r                                   # top cap
        return -s - r * math.sin(p), -r * math.cos(p)
    return f


def stadium_in(A, B, ha, r):
    s = max(ha - r, 0.0)
    dA = max(abs(A) - s, 0.0)
    return dA * dA + B * B <= r * r
