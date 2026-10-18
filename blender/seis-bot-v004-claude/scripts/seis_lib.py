"""seis_lib - geometry toolkit for the SEIS bot Blender model (Blender 5.1, bpy + bmesh only).

WORLD CONVENTIONS (never break these)
  metres; Z up; the figure stands on z = 0 and FACES -Y (front view = numpad 1 looks along +Y);
  the robot's LEFT is +X, its RIGHT is -X; names end in .L (+X) or .R (-X) when a part is one-sided.
  Build the LEFT (+X) side, then mirror_x() it.  Never use negative object scale.

THE FIVE BIG TOOLS
  Sweep(path, keys)          a lofted limb / tube / neck / torso skin: superellipse cross-sections along a
                             spline; sw.mesh() makes the solid, sw.panel() makes armour plates that HUG that skin
                             (so a forearm = one dark core + several overlapping bronze/teal plates).
  grid_surface(f, nu, nv)    any parametric surface P(u,v) -> a mesh, with optional thickness (blades, scrolls).
  plate(outline, frame, ...) a domed plate from a 2-D outline (chest lobes, knee guards, hex pads).
  disc_stack / bolt / slats  small mechanical details.   boolean_cut for vents and sockets.
  finish(obj, mat)           bevel + smooth shading + material; do this on EVERY part (it is what catches highlights).
Every creator returns the Blender object and links it into the collection set with set_collection().
"""
import math
import bpy
import bmesh
from mathutils import Vector, Matrix, Quaternion

PI = math.pi
_COLL = None      # collection new objects are linked into
_MATMOD = None    # the seis_mat module (set by set_matmod, or imported lazily)


# ----------------------------------------------------------------------------------------------- scene housekeeping
def clear_scene():
    """Remove every object / mesh / curve / light / camera / material / collection (a clean slate)."""
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    for coll in (bpy.data.meshes, bpy.data.curves, bpy.data.lights, bpy.data.cameras, bpy.data.materials,
                 bpy.data.images, bpy.data.node_groups, bpy.data.armatures):
        for d in list(coll):
            try:
                coll.remove(d)
            except Exception:
                pass
    for c in list(bpy.data.collections):
        bpy.data.collections.remove(c)


def collection(name, parent=None):
    """Get or create a collection (child of the scene collection unless parent is given)."""
    c = bpy.data.collections.get(name)
    if c is None:
        c = bpy.data.collections.new(name)
        (parent or bpy.context.scene.collection).children.link(c)
    return c


def set_collection(c):
    """All objects created from now on are linked into collection c (a Collection or a name)."""
    global _COLL
    _COLL = collection(c) if isinstance(c, str) else c
    return _COLL


def _link(obj):
    (_COLL or bpy.context.scene.collection).objects.link(obj)
    return obj


def mat(name):
    """Material by name from seis_mat (teal, bronze, red, silver, dark, white, eye, concrete, ...)."""
    global _MATMOD
    if _MATMOD is None:
        import seis_mat as _m
        _MATMOD = _m
    return _MATMOD.get(name)


def set_matmod(m):
    global _MATMOD
    _MATMOD = m


# ----------------------------------------------------------------------------------------------------- small maths
def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x


def lerp(a, b, t):
    return a + (b - a) * t


def smoothstep(a, b, x):
    if a == b:
        return 1.0 if x >= b else 0.0
    t = clamp((x - a) / (b - a))
    return t * t * (3 - 2 * t)


def V(*a):
    return Vector(a[0]) if len(a) == 1 else Vector(a)


def spow(x, p):
    """signed power: sign(x) * |x|**p"""
    return math.copysign(abs(x) ** p, x)


def rot_to(direction, up_hint=(0, 0, 1)):
    """3x3 matrix whose local +Z is `direction` and whose local +Y is as close to up_hint as possible."""
    z = Vector(direction).normalized()
    y = Vector(up_hint) - z * Vector(up_hint).dot(z)
    if y.length < 1e-6:
        y = Vector((1, 0, 0)) - z * z.x
    y.normalize()
    x = y.cross(z)
    return Matrix((x, y, z)).transposed()


class Frame:
    """Orthonormal frame: origin + x/y/z axes.  Frame.at(origin, z=normal, x=hint)."""

    def __init__(self, origin=(0, 0, 0), x=(1, 0, 0), y=(0, 1, 0), z=(0, 0, 1)):
        self.o, self.x, self.y, self.z = Vector(origin), Vector(x), Vector(y), Vector(z)

    @staticmethod
    def at(origin, z, x=(1, 0, 0)):
        z = Vector(z).normalized()
        xv = Vector(x) - z * Vector(x).dot(z)
        if xv.length < 1e-6:
            xv = Vector((0, 1, 0)) - z * z.y
        xv.normalize()
        return Frame(origin, xv, z.cross(xv), z)

    def p(self, lx=0.0, ly=0.0, lz=0.0):
        return self.o + self.x * lx + self.y * ly + self.z * lz

    def d(self, lx=0.0, ly=0.0, lz=0.0):
        return self.x * lx + self.y * ly + self.z * lz

    def matrix(self):
        m = Matrix((self.x, self.y, self.z)).transposed().to_4x4()
        m.translation = self.o
        return m


# ---------------------------------------------------------------------------------------------------------- splines
def catmull(points, n_per_seg=12, alpha=0.5, closed=False):
    """Centripetal Catmull-Rom through points -> dense list of Vectors."""
    P = [Vector(p) for p in points]
    if len(P) < 2:
        return P
    if len(P) == 2:
        return [P[0].lerp(P[1], i / n_per_seg) for i in range(n_per_seg + 1)]
    if closed:
        P = [P[-1]] + P + [P[0], P[1]]
    else:
        P = [P[0] * 2 - P[1]] + P + [P[-1] * 2 - P[-2]]
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        t0 = 0.0
        t1 = t0 + max((p1 - p0).length, 1e-9) ** alpha
        t2 = t1 + max((p2 - p1).length, 1e-9) ** alpha
        t3 = t2 + max((p3 - p2).length, 1e-9) ** alpha
        for k in range(n_per_seg):
            t = t1 + (t2 - t1) * k / n_per_seg
            a1 = p0 * ((t1 - t) / (t1 - t0)) + p1 * ((t - t0) / (t1 - t0))
            a2 = p1 * ((t2 - t) / (t2 - t1)) + p2 * ((t - t1) / (t2 - t1))
            a3 = p2 * ((t3 - t) / (t3 - t2)) + p3 * ((t - t2) / (t3 - t2))
            b1 = a1 * ((t2 - t) / (t2 - t0)) + a2 * ((t - t0) / (t2 - t0))
            b2 = a2 * ((t3 - t) / (t3 - t1)) + a3 * ((t - t1) / (t3 - t1))
            out.append(b1 * ((t2 - t) / (t2 - t1)) + b2 * ((t - t1) / (t2 - t1)))
    if not closed:
        out.append(P[-2].copy())
    return out


class Path:
    """Arc-length parametrised spline: at(t), tangent(t), t in [0, 1]."""

    def __init__(self, pts, closed=False, n_per_seg=16):
        self.pts = catmull(pts, n_per_seg, closed=closed)
        self.s = [0.0]
        for i in range(1, len(self.pts)):
            self.s.append(self.s[-1] + (self.pts[i] - self.pts[i - 1]).length)
        self.length = self.s[-1] or 1e-9

    def at(self, t):
        t = clamp(t)
        target = t * self.length
        lo, hi = 0, len(self.s) - 1
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if self.s[mid] <= target:
                lo = mid
            else:
                hi = mid
        seg = self.s[hi] - self.s[lo]
        f = 0.0 if seg < 1e-12 else (target - self.s[lo]) / seg
        return self.pts[lo].lerp(self.pts[hi], f)

    def tangent(self, t):
        e = 0.5 / max(len(self.pts), 50)
        a, b = self.at(clamp(t - e)), self.at(clamp(t + e))
        d = b - a
        return d.normalized() if d.length > 1e-12 else Vector((0, 0, 1))


# ---------------------------------------------------------------------------------------------------------- sweeps
_SECKEYS = ("rxp", "rxn", "ryp", "ryn", "n", "ox", "oy", "twist")


def _norm_key(k):
    """(t, rx, ry[, n]) tuple or dict -> dict with rxp/rxn/ryp/ryn/n/ox/oy/twist."""
    if not isinstance(k, dict):
        d = {"t": k[0], "rx": k[1], "ry": k[2]}
        if len(k) > 3:
            d["n"] = k[3]
        k = d
    out = {"t": k["t"]}
    sc = k.get("scale", 1.0)
    out["rxp"] = k.get("rxp", k.get("rx", 0.05)) * sc
    out["rxn"] = k.get("rxn", k.get("rx", out["rxp"] / sc)) * sc
    out["ryp"] = k.get("ryp", k.get("ry", 0.05)) * sc
    out["ryn"] = k.get("ryn", k.get("ry", out["ryp"] / sc)) * sc
    out["n"] = k.get("n", 2.0)
    out["ox"] = k.get("ox", 0.0)
    out["oy"] = k.get("oy", 0.0)
    out["twist"] = k.get("twist", 0.0)
    return out


def _hermite(p0, p1, m0, m1, f):
    f2, f3 = f * f, f * f * f
    return (2 * f3 - 3 * f2 + 1) * p0 + (f3 - 2 * f2 + f) * m0 + (-2 * f3 + 3 * f2) * p1 + (f3 - f2) * m1


class Sweep:
    """A swept superellipse skin.

    path   list of 3-D points (Catmull-Rom through them)
    keys   cross-section keys at arc-length fractions t in [0,1]; each is (t, rx, ry) / (t, rx, ry, n) or a dict:
             rx, ry          half-width (local x, ~ lateral) and half-depth (local y, ~ front-back)
             rxp,rxn,ryp,ryn separate radii for the +x / -x / +y / -y halves (D shapes, flat backs)
             n               superellipse exponent (2 ellipse, 3-4 rounded box, 6+ near box)
             ox, oy          section centre offset, twist (deg)
           Values are smoothly interpolated between keys (Catmull-Rom) unless smooth=False.
    front  world direction local +y points at (default -Y, the robot's front); side  local +x (default +X).
    """

    def __init__(self, path, keys, front=(0, -1, 0), side=(1, 0, 0), smooth=True, n_per_seg=16, nframes=120):
        self.path = path if isinstance(path, Path) else Path(path, n_per_seg=n_per_seg)
        self.keys = sorted((_norm_key(k) for k in keys), key=lambda d: d["t"])
        self.smooth = smooth
        self.front, self.side = Vector(front).normalized(), Vector(side).normalized()
        self._build_frames(nframes)

    # --- frames (rotation minimising, so a bent limb does not twist)
    def _build_frames(self, n):
        P = self.path
        ts = [i / n for i in range(n + 1)]
        pts = [P.at(t) for t in ts]
        tans = [P.tangent(t) for t in ts]
        t0 = tans[0]
        y0 = self.front - t0 * self.front.dot(t0)
        if y0.length < 1e-6:
            y0 = Vector((0, 1, 0)) - t0 * t0.y
        y0.normalize()
        x0 = y0.cross(t0)
        self.sign = 1.0 if x0.dot(self.side) >= 0 else -1.0
        r = y0
        ys = [r]
        for i in range(n):
            v1 = pts[i + 1] - pts[i]
            c1 = v1.dot(v1)
            if c1 < 1e-18:
                ys.append(ys[-1])
                continue
            rl = r - (2 / c1) * v1.dot(r) * v1
            tl = tans[i] - (2 / c1) * v1.dot(tans[i]) * v1
            v2 = tans[i + 1] - tl
            c2 = v2.dot(v2)
            r = rl - (2 / c2) * v2.dot(rl) * v2 if c2 > 1e-18 else rl
            r = (r - tans[i + 1] * r.dot(tans[i + 1])).normalized()
            ys.append(r)
        self._ts, self._pts, self._tans, self._ys = ts, pts, tans, ys
        # right-handed (x, y, T)?  x = sign * (y x T)
        self.handed = self.sign > 0

    def frame(self, t):
        """(P, T, X, Y) at t."""
        t = clamp(t)
        n = len(self._ts) - 1
        f = t * n
        i = min(int(f), n - 1)
        u = f - i
        Pt = self._pts[i].lerp(self._pts[i + 1], u)
        T = self._tans[i].lerp(self._tans[i + 1], u).normalized()
        Y = self._ys[i].lerp(self._ys[i + 1], u)
        Y = (Y - T * Y.dot(T)).normalized()
        X = Y.cross(T) * self.sign
        return Pt, T, X, Y

    # --- section
    def sec(self, t):
        ks = self.keys
        if t <= ks[0]["t"]:
            return dict(ks[0])
        if t >= ks[-1]["t"]:
            return dict(ks[-1])
        i = 0
        while ks[i + 1]["t"] < t:
            i += 1
        a, b = ks[i], ks[i + 1]
        span = b["t"] - a["t"]
        f = (t - a["t"]) / span if span > 1e-12 else 0.0
        out = {"t": t}
        for name in _SECKEYS:
            va, vb = a[name], b[name]
            if self.smooth:
                # Catmull-Rom tangents (non-uniform spacing), one-sided at the ends
                if i > 0:
                    pa = ks[i - 1]
                    m0 = (vb - pa[name]) / max(b["t"] - pa["t"], 1e-9)
                else:
                    m0 = (vb - va) / max(span, 1e-9)
                if i + 2 < len(ks):
                    pb = ks[i + 2]
                    m1 = (pb[name] - va) / max(pb["t"] - a["t"], 1e-9)
                else:
                    m1 = (vb - va) / max(span, 1e-9)
                val = _hermite(va, vb, m0 * span, m1 * span, f)
            else:
                val = lerp(va, vb, f)
            out[name] = max(1.2, val) if name == "n" else val
        for name in ("rxp", "rxn", "ryp", "ryn"):
            out[name] = max(out[name], 1e-5)
        return out

    def local_xy(self, t, theta, inflate=0.0, sec=None):
        s = sec or self.sec(t)
        c, sn = math.cos(theta), math.sin(theta)
        e = 2.0 / max(s["n"], 1.0)
        rx = s["rxp"] if c >= 0 else s["rxn"]
        ry = s["ryp"] if sn >= 0 else s["ryn"]
        x = (rx + inflate) * spow(c, e)
        y = (ry + inflate) * spow(sn, e)
        tw = math.radians(s["twist"])
        if tw:
            x, y = x * math.cos(tw) - y * math.sin(tw), x * math.sin(tw) + y * math.cos(tw)
        return x + s["ox"], y + s["oy"]

    def point(self, t, theta, off=0.0):
        """World point on the skin at (t, theta) pushed `off` metres along the local outward direction."""
        Pt, T, X, Y = self.frame(t)
        s = self.sec(t)
        x, y = self.local_xy(t, theta, off, s)
        return Pt + X * x + Y * y

    def normal(self, t, theta):
        """Surface normal at (t, theta) by finite differences (sign not guaranteed; see outward())."""
        e1, e2 = 0.002, 0.002
        a = self.point(clamp(t + e1), theta) - self.point(clamp(t - e1), theta)
        b = self.point(t, theta + e2) - self.point(t, theta - e2)
        n = a.cross(b)
        if n.length < 1e-12:
            return Vector((0, 0, 1))
        return n.normalized()

    def outward(self, t, theta):
        """Unit normal pointing away from the centre line."""
        n = self.normal(t, theta)
        c = self.frame(t)[0] + self.frame(t)[2] * self.sec(t)["ox"] + self.frame(t)[3] * self.sec(t)["oy"]
        if (self.point(t, theta) - c).dot(n) < 0:
            n = -n
        return n

    # --- solid mesh
    def mesh(self, name, nring=40, nstations=None, caps=True, round_start=None, round_end=None, closed_path=False):
        """The swept solid.  round_start/round_end = (depth, steps) adds a domed end of that depth (m)."""
        ks_t = [k["t"] for k in self.keys]
        nst = nstations or max(16, int(self.path.length / 0.02))
        ts = sorted(set([i / nst for i in range(nst + 1)] + ks_t))
        rings = []        # list of lists of Vectors
        Pend0, Pend1 = None, None
        if round_start:
            depth, steps = round_start
            Pt, T, X, Y = self.frame(0.0)
            s0 = self.sec(0.0)
            for j in range(steps, 0, -1):
                ph = (j / (steps + 1)) * (PI / 2)
                sc, off = math.cos(ph), depth * math.sin(ph)
                rings.append(self._ring(0.0, nring, scale=sc, shift=-T * off, sec=s0))
            Pend0 = Pt - T * depth
        for t in ts:
            rings.append(self._ring(t, nring))
        if round_end:
            depth, steps = round_end
            Pt, T, X, Y = self.frame(1.0)
            s1 = self.sec(1.0)
            for j in range(1, steps + 1):
                ph = (j / (steps + 1)) * (PI / 2)
                sc, off = math.cos(ph), depth * math.sin(ph)
                rings.append(self._ring(1.0, nring, scale=sc, shift=T * off, sec=s1))
            Pend1 = Pt + T * depth
        return _mesh_from_rings(name, rings, nring, closed_rings=True, caps=caps, flip=not self.handed,
                                pole_start=Pend0, pole_end=Pend1)

    def _ring(self, t, nring, scale=1.0, shift=None, sec=None):
        Pt, T, X, Y = self.frame(t)
        s = sec or self.sec(t)
        ring = []
        for k in range(nring):
            th = 2 * PI * k / nring
            x, y = self.local_xy(t, th, 0.0, s)
            c = Vector((s["ox"], s["oy"]))
            x, y = c.x + (x - c.x) * scale, c.y + (y - c.y) * scale
            p = Pt + X * x + Y * y
            if shift is not None:
                p = p + shift
            ring.append(p)
        return ring

    # --- armour panels that hug the skin
    def panel(self, name, t0, t1, a0, a1, thickness=0.008, inflate=0.004, height=0.0, hp=1.0, ends=0.0,
              nu=18, nv=14, round_edge=True):
        """A plate over the angular window [a0, a1] (radians, or callables of t) for t in [t0, t1].

        inflate  gap above the skin;  height  extra dome height at the middle;  hp  dome sharpness (1 soft, 3 sharp)
        ends     fraction (0-0.5) of the length over which the plate eases back to the skin at both ends
        thickness  solid thickness (0 = open surface).  Angles run counter-clockwise looking along the path (+x = 0).
        """
        f0 = a0 if callable(a0) else (lambda t, _a=a0: _a)
        f1 = a1 if callable(a1) else (lambda t, _a=a1: _a)

        def fn(u, v):
            t = t0 + (t1 - t0) * u
            th = f0(t) + (f1(t) - f0(t)) * v
            dome = height * (math.sin(PI * v) ** hp) * (math.sin(PI * u) ** hp if ends else 1.0)
            if ends:
                dome *= smoothstep(0.0, ends, u) * smoothstep(1.0, 1.0 - ends, u)
            off = inflate + dome
            return self.point(t, th, 0.0) + self.outward(t, th) * off

        return grid_surface(name, fn, nu, nv, thickness=thickness, flip=not self.handed)


def _mesh_from_rings(name, rings, nring, closed_rings=True, caps=True, flip=False, pole_start=None, pole_end=None):
    verts, faces = [], []
    for r in rings:
        verts.extend(r)
    nr = len(rings)
    for i in range(nr - 1):
        for k in range(nring):
            k2 = (k + 1) % nring
            a, b = i * nring + k, i * nring + k2
            c, d = (i + 1) * nring + k2, (i + 1) * nring + k
            faces.append((a, b, c, d))
    if pole_start is not None:
        verts.append(pole_start)
        ip = len(verts) - 1
        for k in range(nring):
            faces.append((ip, (k + 1) % nring, k)[::1])
    elif caps:
        faces.append(tuple(range(nring - 1, -1, -1)))
    if pole_end is not None:
        verts.append(pole_end)
        ip = len(verts) - 1
        base = (nr - 1) * nring
        for k in range(nring):
            faces.append((ip, base + k, base + (k + 1) % nring))
    elif caps:
        faces.append(tuple((nr - 1) * nring + k for k in range(nring)))
    if flip:
        faces = [tuple(reversed(f)) for f in faces]
    return new_mesh(name, verts, faces)


# ------------------------------------------------------------------------------------------------ mesh construction
def new_mesh(name, verts, faces, smooth=True):
    me = bpy.data.meshes.new(name)
    me.from_pydata([tuple(v) for v in verts], [], [tuple(f) for f in faces])
    me.update()
    if smooth:
        me.shade_smooth()
    ob = bpy.data.objects.new(name, me)
    return _link(ob)


def grid_surface(name, f, nu, nv, thickness=0.0, flip=False, closed_u=False, closed_v=False, offset=-1.0,
                 smooth=True):
    """Mesh of the parametric surface f(u, v) -> (x, y, z), u, v in [0, 1].  thickness > 0 adds a solid skin
    (offset -1 = grow inward against the normal, 0 = centred, +1 = outward).  The winding makes normals follow
    d/du x d/dv; pass flip=True to reverse."""
    verts = []
    for i in range(nu + 1):
        for j in range(nv + 1):
            verts.append(Vector(f(i / nu, j / nv)))
    W = nv + 1
    faces = []
    for i in range(nu):
        for j in range(nv):
            faces.append((i * W + j, (i + 1) * W + j, (i + 1) * W + j + 1, i * W + j + 1))
    if flip:
        faces = [tuple(reversed(q)) for q in faces]
    ob = new_mesh(name, verts, faces, smooth)
    if thickness > 0:
        m = ob.modifiers.new("Solidify", "SOLIDIFY")
        m.thickness = thickness
        m.offset = offset
        m.use_even_offset = True
        m.use_rim = True
        apply_modifiers(ob)
    return ob


def apply_modifiers(ob):
    dg = bpy.context.evaluated_depsgraph_get()
    ev = ob.evaluated_get(dg)
    me_new = bpy.data.meshes.new_from_object(ev, depsgraph=dg)
    old = ob.data
    ob.modifiers.clear()
    ob.data = me_new
    me_new.name = ob.name
    if old.users == 0:
        bpy.data.meshes.remove(old)
    return ob


# --------------------------------------------------------------------------------------------------------- outlines
def outline_ellipse(rx, ry, n=48, power=2.0):
    return [(rx * spow(math.cos(2 * PI * i / n), 2 / power), ry * spow(math.sin(2 * PI * i / n), 2 / power)) for i in range(n)]


def outline_rrect(w, h, r, n=8):
    """Rounded rectangle, counter-clockwise, w x h total, corner radius r."""
    r = min(r, w / 2, h / 2)
    pts = []
    for cx, cy, a0 in ((w / 2 - r, h / 2 - r, 0), (-w / 2 + r, h / 2 - r, 90), (-w / 2 + r, -h / 2 + r, 180),
                       (w / 2 - r, -h / 2 + r, 270)):
        for i in range(n + 1):
            a = math.radians(a0 + 90 * i / n)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def outline_teardrop(w, h, n=40, point=0.35):
    """Egg/teardrop pointing +y: width w, height h, pointed end at the top."""
    pts = []
    for i in range(n):
        a = 2 * PI * i / n
        y = math.sin(a)
        k = 1.0 - point * (y * 0.5 + 0.5) ** 2 if y > 0 else 1.0
        x = math.cos(a) * (w / 2) * (1 - point * max(0.0, y) ** 3) * k
        pts.append((x, y * h / 2))
    return pts


def outline_poly(points, round_r=0.0, n=6):
    """Closed polygon (counter-clockwise) with optional corner rounding."""
    P = [Vector(p) for p in points]
    if round_r <= 0:
        return [tuple(p) for p in P]
    out = []
    m = len(P)
    for i in range(m):
        a, b, c = P[i - 1], P[i], P[(i + 1) % m]
        d1, d2 = (a - b), (c - b)
        r = min(round_r, d1.length * 0.45, d2.length * 0.45)
        p1 = b + d1.normalized() * r
        p2 = b + d2.normalized() * r
        for k in range(n + 1):
            f = k / n
            q = (p1 * (1 - f) + b * f) * (1 - f) + (b * (1 - f) + p2 * f) * f
            out.append((q.x, q.y))
    return out


# ------------------------------------------------------------------------------------------------------ domed plates
def plate(name, outline, frame=None, rise=0.012, thickness=0.01, steps=7, inset=None, power=1.6, flat_top=0.0,
          edge_chamfer=0.0):
    """Domed plate: a 2-D outline in the xy plane of `frame` (default world XY, dome toward +z).

    Built by repeatedly insetting the outline face and lifting each ring, so it has a clean concentric
    topology.  rise = dome height; inset = total inset distance (default 45 % of the smaller half-width);
    power > 1 gives a flatter top with rounded shoulders; thickness extrudes backwards (-z) for a solid;
    flat_top fraction keeps that share of the area flat.  Outline should be roughly convex."""
    frame = frame or Frame()
    pts = [Vector((p[0], p[1], 0.0)) for p in outline]
    xs = [p.x for p in pts]
    ys = [p.y for p in pts]
    if inset is None:
        inset = 0.22 * min(max(xs) - min(xs), max(ys) - min(ys)) * (1 - flat_top)
    bm = bmesh.new()
    vs = [bm.verts.new(p) for p in pts]
    f = bm.faces.new(vs)
    bmesh.ops.recalc_face_normals(bm, faces=[f])
    if f.normal.z < 0:
        f.normal_flip()
    cur = [f]
    prev_depth = 0.0
    for i in range(1, steps + 1):
        frac = i / steps
        d_inset = inset / steps
        depth = rise * (1 - (1 - frac) ** power) - prev_depth
        prev_depth += depth
        r = bmesh.ops.inset_region(bm, faces=cur, thickness=d_inset, depth=depth, use_even_offset=True,
                                   use_boundary=True, use_outset=False)
        cur = r["faces"]
    # side wall + back
    if thickness > 0:
        bm.faces.ensure_lookup_table()
        boundary = [e for e in bm.edges if e.is_boundary]
        ret = bmesh.ops.extrude_edge_only(bm, edges=boundary)
        newv = [e for e in ret["geom"] if isinstance(e, bmesh.types.BMVert)]
        bmesh.ops.translate(bm, vec=(0, 0, -thickness), verts=newv)
        bm.edges.ensure_lookup_table()
        bnd2 = [e for e in bm.edges if e.is_boundary]
        try:
            bmesh.ops.contextual_create(bm, geom=bnd2)
        except Exception:
            pass
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    M = frame.matrix()
    bmesh.ops.transform(bm, matrix=M, verts=bm.verts[:])
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    me.shade_smooth()
    return _link(bpy.data.objects.new(name, me))


# ------------------------------------------------------------------------------------------------------- primitives
def _prim(name, bm):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    me.shade_smooth()
    return _link(bpy.data.objects.new(name, me))


def box(name, size, frame=None, center=True):
    """Box of size (sx, sy, sz) in `frame` (default world)."""
    frame = frame or Frame()
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co = Vector((v.co.x * size[0], v.co.y * size[1], v.co.z * size[2]))
        if not center:
            v.co += Vector((size[0] / 2, size[1] / 2, size[2] / 2))
    bmesh.ops.transform(bm, matrix=frame.matrix(), verts=bm.verts[:])
    return _prim(name, bm)


def cylinder(name, radius, depth, frame=None, segments=48, radius2=None, caps=True):
    """Cylinder/cone along the frame's z, centred on the origin (radius2 = top radius for a cone frustum)."""
    frame = frame or Frame()
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=caps, cap_tris=False, segments=segments, radius1=radius,
                          radius2=radius if radius2 is None else radius2, depth=depth)
    bmesh.ops.transform(bm, matrix=frame.matrix(), verts=bm.verts[:])
    return _prim(name, bm)


def sphere(name, radius, frame=None, scale=(1, 1, 1), segments=40, rings=24):
    frame = frame or Frame()
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=segments, v_segments=rings, radius=radius)
    for v in bm.verts:
        v.co = Vector((v.co.x * scale[0], v.co.y * scale[1], v.co.z * scale[2]))
    bmesh.ops.transform(bm, matrix=frame.matrix(), verts=bm.verts[:])
    return _prim(name, bm)


def torus(name, major, minor, frame=None, major_seg=64, minor_seg=16):
    frame = frame or Frame()
    verts, faces = [], []
    for i in range(major_seg):
        a = 2 * PI * i / major_seg
        for j in range(minor_seg):
            b = 2 * PI * j / minor_seg
            r = major + minor * math.cos(b)
            verts.append(frame.p(r * math.cos(a), r * math.sin(a), minor * math.sin(b)))
    for i in range(major_seg):
        for j in range(minor_seg):
            i2, j2 = (i + 1) % major_seg, (j + 1) % minor_seg
            faces.append((i * minor_seg + j, i2 * minor_seg + j, i2 * minor_seg + j2, i * minor_seg + j2))
    return new_mesh(name, verts, faces)


def tube(name, pts, radius, taper=None, nring=16, caps=True, n_per_seg=12, round_ends=False):
    """Round pipe/cable through points.  radius const or callable t->r; taper=(r_start_scale, r_end_scale)."""
    path = Path(pts, n_per_seg=n_per_seg)
    ts = [i / 8 for i in range(9)]
    if callable(radius):
        keys = [(t, radius(t), radius(t)) for t in ts]
    else:
        a, b = taper or (1.0, 1.0)
        keys = [(0.0, radius * a, radius * a), (1.0, radius * b, radius * b)]
    sw = Sweep(path, keys)
    return sw.mesh(name, nring=nring, nstations=max(8, int(path.length / 0.01)), caps=caps,
                   round_start=(radius * (taper[0] if taper else 1), 3) if round_ends and not callable(radius) else None,
                   round_end=(radius * (taper[1] if taper else 1), 3) if round_ends and not callable(radius) else None)


def disc_stack(name, center, normal, rings, segments=64, xhint=(1, 0, 0)):
    """Concentric raised/recessed rings such as the speaker discs: rings = [(radius, height), ...] from the base
    outward-to-inward; each ring is a cylinder of that radius standing `height` above the base plane, so
    [(0.05, 0.004), (0.04, 0.010), (0.025, 0.006), (0.012, 0.012)] reads as stepped concentric grooves.
    Returns ONE object (joined)."""
    fr = Frame.at(center, normal, xhint)
    parts = []
    for i, (r, h) in enumerate(rings):
        c = cylinder(f"{name}_r{i}", r, h, Frame(fr.p(0, 0, h / 2), fr.x, fr.y, fr.z), segments=segments)
        parts.append(c)
    return join(parts, name)


def bolt(name, center, normal, radius=0.006, height=0.004, hexagon=True, xhint=(1, 0, 0)):
    fr = Frame.at(center, normal, xhint)
    return cylinder(name, radius, height, Frame(fr.p(0, 0, height / 2), fr.x, fr.y, fr.z), segments=6 if hexagon else 20)


def slats(name, frame, width, height, count, slat_h, depth, round_r=0.002):
    """Vent slats: `count` horizontal bars of width x slat_h x depth stacked along the frame's y over `height`."""
    parts = []
    for i in range(count):
        y = -height / 2 + height * (i + 0.5) / count
        parts.append(box(f"{name}_{i}", (width, slat_h, depth), Frame(frame.p(0, y, 0), frame.x, frame.y, frame.z)))
    return join(parts, name)


# ------------------------------------------------------------------------------------------------ object operations
def join(objs, name=None, keep_mat=True):
    objs = [o for o in objs if o is not None]
    if not objs:
        return None
    if len(objs) == 1:
        if name:
            objs[0].name = name
        return objs[0]
    bpy.ops.object.select_all(action="DESELECT")
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.join()
    res = bpy.context.view_layer.objects.active
    if name:
        res.name = name
        res.data.name = name
    return res


def mirror_x(obj, name=None):
    """Mirrored copy across the YZ plane (x -> -x) as REAL geometry (no negative scale); normals stay outward."""
    me = obj.data.copy()
    bm = bmesh.new()
    bm.from_mesh(me)
    for v in bm.verts:
        v.co.x = -v.co.x
    bmesh.ops.reverse_faces(bm, faces=bm.faces[:])
    bm.to_mesh(me)
    bm.free()
    me.update()
    new = bpy.data.objects.new(name or _flip_side_name(obj.name), me)
    new.location = Vector((-obj.location.x, obj.location.y, obj.location.z))
    new.rotation_mode = obj.rotation_mode
    e = obj.rotation_euler
    new.rotation_euler = (e.x, -e.y, -e.z)
    new.scale = obj.scale
    for m in obj.modifiers:
        pass
    for slot in obj.material_slots:
        new.data.materials.append(slot.material)
    for k in obj.keys():
        v = obj[k]
        new[k] = _flip_side_name(v) if (k == "bone" and isinstance(v, str) and v[-2:] in (".L", ".R")) else v
    _link(new)
    return new


def _flip_side_name(n):
    if n.endswith(".L"):
        return n[:-2] + ".R"
    if n.endswith(".R"):
        return n[:-2] + ".L"
    return n + ".R"


def set_origin(obj, point):
    """Move the object origin to world `point` without moving the geometry."""
    off = obj.matrix_world.inverted() @ Vector(point)
    obj.data.transform(Matrix.Translation(-off))
    obj.location += obj.matrix_world.to_3x3() @ off


def place(obj, loc=None, rot_deg=None, scale=None):
    if loc is not None:
        obj.location = loc
    if rot_deg is not None:
        obj.rotation_euler = tuple(math.radians(a) for a in rot_deg)
    if scale is not None:
        obj.scale = scale
    return obj


def transform_mesh(obj, matrix):
    obj.data.transform(matrix)
    obj.data.update()
    return obj


def boolean_cut(obj, cutter, op="DIFFERENCE", delete_cutter=True, solver="EXACT"):
    """Cut `cutter` out of `obj` (applies the modifier)."""
    m = obj.modifiers.new("Bool", "BOOLEAN")
    m.operation = op
    m.object = cutter
    m.solver = solver
    apply_modifiers(obj)
    if delete_cutter:
        bpy.data.objects.remove(cutter, do_unlink=True)
    return obj


def surface_hit(target, origin, direction, max_dist=10.0):
    """Ray-cast onto `target`; returns (hit_point, normal) in world space or (None, None)."""
    dg = bpy.context.evaluated_depsgraph_get()
    inv = target.matrix_world.inverted()
    o = inv @ Vector(origin)
    d = (inv.to_3x3() @ Vector(direction)).normalized()
    ok, loc, nor, idx = target.ray_cast(o, d, distance=max_dist, depsgraph=dg)
    if not ok:
        return None, None
    return target.matrix_world @ loc, (target.matrix_world.to_3x3() @ nor).normalized()


# -------------------------------------------------------------------------------------------------------- finishing
def mark_sharp_by_angle(obj, angle_deg=35.0):
    me = obj.data
    bm = bmesh.new()
    bm.from_mesh(me)
    lim = math.radians(angle_deg)
    for e in bm.edges:
        if len(e.link_faces) == 2:
            e.smooth = e.calc_face_angle(0.0) < lim
        else:
            e.smooth = True
    bm.to_mesh(me)
    bm.free()


def finish(obj, material=None, bevel=0.0015, bevel_segments=2, angle=38.0, weighted=True, subsurf=0, apply=True,
           sharp_angle=None, wear=None, bone=None):
    """Material + bevel + smooth shading.  bevel (m) is the chamfer width; use ~0.001-0.003 for armour.
    subsurf > 0 adds a Catmull-Clark pass BEFORE the bevel (for organic blobs).  apply=True bakes the modifiers."""
    if material:
        set_material(obj, material)
    if wear is not None:
        obj["wear"] = float(wear) if wear > 0 else 1e-6   # gold-trim strength read by the teal/bronze shaders (0 -> 1e-6: "present but off")
    if bone:
        obj["bone"] = bone               # the rig script parents this object rigidly to that bone
    obj.data.shade_smooth()
    mark_sharp_by_angle(obj, sharp_angle or angle)
    if subsurf:
        m = obj.modifiers.new("Sub", "SUBSURF")
        m.levels = subsurf
        m.render_levels = subsurf
    if bevel and bevel > 0:
        m = obj.modifiers.new("Bevel", "BEVEL")
        m.width = bevel
        m.segments = bevel_segments
        m.limit_method = "ANGLE"
        m.angle_limit = math.radians(angle)
        m.profile = 0.6
    if weighted:
        m = obj.modifiers.new("WN", "WEIGHTED_NORMAL")
        m.keep_sharp = True
        m.weight = 50
        m.mode = "FACE_AREA"
    if apply and obj.modifiers:
        apply_modifiers(obj)
        obj.data.shade_smooth()
    return obj


def set_bone(obj, bone):
    """Declare which rig bone moves this object (e.g. 'forearm.L').  See BIBLE.md for the bone list."""
    obj["bone"] = bone
    return obj


def set_material(obj, material):
    m = mat(material) if isinstance(material, str) else material
    obj.data.materials.clear()
    obj.data.materials.append(m)
    return obj


def bbox_world(objs):
    lo = Vector((1e9, 1e9, 1e9))
    hi = Vector((-1e9, -1e9, -1e9))
    for o in objs:
        for c in o.bound_box:
            w = o.matrix_world @ Vector(c)
            lo = Vector((min(lo.x, w.x), min(lo.y, w.y), min(lo.z, w.z)))
            hi = Vector((max(hi.x, w.x), max(hi.y, w.y), max(hi.z, w.z)))
    return lo, hi
