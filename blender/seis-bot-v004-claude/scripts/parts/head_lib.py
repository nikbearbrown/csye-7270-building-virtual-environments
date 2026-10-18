"""head_lib - helpers private to the SEIS head/neck builder (parts/head.py).

Skull      one ellipsoid-ish egg; the same formula drives the dome, the crest stripes and the panels, so they hug it.
Charts     2-D coordinate systems on that egg (front view x,z / crest xi,psi / spherical phi,theta) that return a
           surface point P and an outward normal N, so flat 2-D outlines can be projected onto the curved shell.
chart_plate(...)   a domed, bevel-ready plate from a closed 2-D outline, projected through a chart.
chart_grid(...)    a parametric patch (stripe, band, dome) projected through a chart, with thickness.
"""
import math
import bpy
import bmesh
from mathutils import Vector

import seis_lib as L
import seis_spec as S
import head_mat  # noqa: F401  registers the head-private 'pewter' material

PI = math.pi
Z_TOP = S.hh(8.3)


# ------------------------------------------------------------------------------------------------------- the egg
class Skull:
    a = 0.0955       # half width
    bf = 0.104       # half depth, front
    br = 0.118       # half depth, rear (the egg is fuller at the back)
    c = 0.170        # half height (above the centre)
    cl = 0.140       # half height below the centre (the egg is blunter below)
    yc = 0.004
    zc = Z_TOP - 0.170

    def b(self, k):
        return self.bf if k >= 0 else self.br

    def cz(self, dz):
        return self.c if dz >= 0 else self.cl

    def pt_sph(self, phi, th, off=0.0):
        """phi azimuth from the front (+ toward +X), th elevation."""
        k = math.cos(phi) * math.cos(th)
        p = Vector((self.a * math.sin(phi) * math.cos(th), self.yc - self.b(k) * k, self.zc + (self.c if th >= 0 else self.cl) * math.sin(th)))
        return p + self.normal(p) * off if off else p

    def pt_chart(self, xi, psi, off=0.0):
        """xi = x / a in (-1, 1); psi runs from the front horizon (0) up over the crown (90) to the rear (180)."""
        xi = max(-0.999, min(0.999, xi))
        r = math.sqrt(1 - xi * xi)
        k = math.cos(psi)
        p = Vector((self.a * xi, self.yc - self.b(k) * r * k, self.zc + (self.c if math.sin(psi) >= 0 else self.cl) * r * math.sin(psi)))
        return p + self.normal(p) * off if off else p

    def normal(self, p):
        dy = p.y - self.yc
        b = self.b(-dy)
        n = Vector((p.x / self.a ** 2, dy / b ** 2, (p.z - self.zc) / self.cz(p.z - self.zc) ** 2))
        return n.normalized() if n.length > 1e-9 else Vector((0, -1, 0))


SK = Skull()


# ------------------------------------------------------------------------------------------------------- charts
class SphChart:
    """(s, t) in metres  ->  phi = s / RS, theta = t / RT on the egg."""
    RS = 0.10
    RT = 0.15

    def map(self, s, t):
        p = SK.pt_sph(s / self.RS, t / self.RT)
        return p, SK.normal(p)

    def st(self, phi, th):
        return phi * self.RS, th * self.RT


class CrestChart:
    """(s, t) in metres -> xi = s / a, psi = t / RT.  Good over the whole upper egg, front to rear."""
    RT = 0.15

    def map(self, s, t):
        p = SK.pt_chart(s / SK.a, t / self.RT)
        return p, SK.normal(p)

    def st(self, xi, psi_deg):
        return xi * SK.a, math.radians(psi_deg) * self.RT


class FaceChart:
    """Front-view chart: (x, z) in metres -> the face shell (egg front, receding below the eye line, nose ridge)."""
    zeye = Z_TOP - 0.171

    def y(self, x, z):
        a, c = SK.a, SK.c
        arg = 1 - (x / a) ** 2 - ((z - SK.zc) / SK.cz(z - SK.zc)) ** 2
        y0 = SK.yc - SK.bf * math.sqrt(max(arg, 0.0004))
        tt = self.zeye - z
        y0 += 0.12 * 0.5 * (tt + math.sqrt(tt * tt + 0.012 ** 2))   # the lower face slopes back toward the chin (smooth knee)
        nose = 0.0065 * math.exp(-(x / 0.020) ** 2) * L.smoothstep(2.03, 1.99, z) * L.smoothstep(1.855, 1.88, z)
        return y0 - nose

    def map(self, x, z):
        e = 0.0008
        f = self.y(x, z)
        fx = (self.y(x + e, z) - self.y(x - e, z)) / (2 * e)
        fz = (self.y(x, z + e) - self.y(x, z - e)) / (2 * e)
        n = Vector((fx, -1.0, fz)).normalized()
        return Vector((x, f, z)), n


SPH = SphChart()
CREST = CrestChart()
FACE = FaceChart()


# ------------------------------------------------------------------------------------------------ outline helpers
def resample_closed(pts, step):
    out = []
    n = len(pts)
    for i in range(n):
        a, b = Vector(pts[i]), Vector(pts[(i + 1) % n])
        m = max(1, int(round((b - a).length / step)))
        for k in range(m):
            out.append(a.lerp(b, k / m))
    return out


def ccw(pts):
    area = 0.0
    n = len(pts)
    for i in range(n):
        x0, y0 = pts[i][0], pts[i][1]
        x1, y1 = pts[(i + 1) % n][0], pts[(i + 1) % n][1]
        area += x0 * y1 - x1 * y0
    return pts if area > 0 else list(reversed(pts))


def rounded(pts, r, n=4):
    return L.outline_poly(pts, r, n)


# --------------------------------------------------------------------------------------------------- chart plate
def chart_plate(name, outline, chart, rise=0.003, thickness=0.004, steps=3, inset=None, power=1.6, step=0.005,
                flat_top=0.0, lift=0.0, shrink_to=0.55):
    """Domed plate from a closed convex-ish 2-D outline (chart coordinates, metres) projected through `chart`.
    Rings are scaled copies of the outline about its centroid (robust for acute corners); ring heights follow a dome.
    lift raises the whole plate off the surface, rise is the dome height."""
    pts = ccw([(p[0], p[1]) for p in outline])
    pts = [(p.x, p.y) for p in resample_closed(pts, step)]
    n = len(pts)
    cx = sum(p[0] for p in pts) / n
    cy = sum(p[1] for p in pts) / n
    sh = 1.0 - (1.0 - shrink_to) * (1 - flat_top)
    rings = []
    for k in range(steps + 1):
        fr = k / steps
        sc = 1.0 - (1.0 - sh) * fr
        z = rise * (1 - (1 - fr) ** power)
        rings.append([(cx + (p[0] - cx) * sc, cy + (p[1] - cy) * sc, z) for p in pts])
    verts = [v for r in rings for v in r]
    faces = []
    for k in range(steps):
        for i in range(n):
            j = (i + 1) % n
            faces.append((k * n + i, k * n + j, (k + 1) * n + j, (k + 1) * n + i))
    ctop = len(verts)
    verts.append((cx, cy, rise))
    for i in range(n):
        j = (i + 1) % n
        faces.append((steps * n + i, steps * n + j, ctop))
    if thickness > 0:
        b0 = len(verts)
        verts.extend((p[0], p[1], -thickness) for p in pts)
        cb = len(verts)
        verts.append((cx, cy, -thickness))
        for i in range(n):
            j = (i + 1) % n
            faces.append((j, i, b0 + i, b0 + j))
            faces.append((cb, b0 + j, b0 + i))
    mapped = []
    for (s_, t_, pz) in verts:
        P, N = chart.map(s_, t_)
        mapped.append(P + N * (pz + lift))
    me = bpy.data.meshes.new(name)
    me.from_pydata([tuple(v) for v in mapped], [], faces)
    me.update()
    bm = bmesh.new()
    bm.from_mesh(me)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    bm.to_mesh(me)
    bm.free()
    me.shade_smooth()
    ob = bpy.data.objects.new(name, me)
    L._link(ob)
    return ob


def _seg_dist(p, a, b):
    ab = (b[0] - a[0], b[1] - a[1])
    l2 = ab[0] * ab[0] + ab[1] * ab[1]
    t = 0.0 if l2 < 1e-18 else max(0.0, min(1.0, ((p[0] - a[0]) * ab[0] + (p[1] - a[1]) * ab[1]) / l2))
    qx, qy = a[0] + t * ab[0], a[1] + t * ab[1]
    return math.hypot(p[0] - qx, p[1] - qy)


def flat_plate(name, outline, chart, rise=0.003, thickness=0.004, rim=0.004, edge=0.45, lift=0.0, step=0.004, maxlen=0.0042):
    """Plate from a closed 2-D outline (chart metres) whose TOP is a properly subdivided surface (so it follows the chart's
    curvature instead of a fan to one centre vertex).  Height = rise * (edge + (1-edge) * smoothstep(dist_to_rim / rim)).
    A flat bottom (hidden) and vertical walls close it."""
    pts = ccw([(p[0], p[1]) for p in outline])
    ring = [(p.x, p.y) for p in resample_closed(pts, step)]
    n = len(ring)
    bm = bmesh.new()
    vs = [bm.verts.new((x, y, 0.0)) for x, y in ring]
    try:
        bm.faces.new(vs)
    except ValueError:
        pass
    bmesh.ops.triangulate(bm, faces=bm.faces[:])
    bm.verts.index_update()
    tri0 = [tuple(v.index for v in f.verts) for f in bm.faces]      # coarse triangulation of the outline (for the hidden bottom)
    for _ in range(7):
        longe = [e for e in bm.edges if e.calc_length() > maxlen and not e.is_boundary]
        if not longe:
            break
        bmesh.ops.subdivide_edges(bm, edges=longe, cuts=1, use_grid_fill=True)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    bm.verts.index_update()
    top_v = [(v.co.x, v.co.y) for v in bm.verts]
    top_f = [tuple(v.index for v in f.verts) for f in bm.faces]
    # boundary verts of the mesh (ordered by walking boundary edges)
    bedges = [e for e in bm.edges if e.is_boundary]
    for v in bm.verts:
        v.index = v.index
    bm.verts.ensure_lookup_table()
    nxt = {}
    for e in bedges:
        a, b = e.verts[0].index, e.verts[1].index
        # orient along the face winding
        lf = e.link_faces[0]
        for i in range(len(lf.verts)):
            if lf.verts[i].index == a and lf.verts[(i + 1) % len(lf.verts)].index == b:
                nxt[a] = b
                break
        else:
            nxt[b] = a
    bm.free()
    nv = len(top_v)
    segs = list(zip(ring, ring[1:] + ring[:1]))
    verts = []
    for (x, y) in top_v:
        d = min(_seg_dist((x, y), a, b) for a, b in segs)
        h = rise * (edge + (1 - edge) * L.smoothstep(0.0, rim, d))
        verts.append((x, y, h))
    verts += [(x, y, -thickness) for (x, y) in top_v]
    faces = [f for f in top_f]
    faces += [tuple(reversed([i + nv for i in f])) for f in tri0]
    for a, b in nxt.items():
        faces.append((a, nv + a, nv + b, b))       # wall (top a -> bottom a -> bottom b -> top b)
    mapped = []
    for (s_, t_, pz) in verts:
        P, N = chart.map(s_, t_)
        mapped.append(tuple(P + N * (pz + lift)))
    me = bpy.data.meshes.new(name)
    me.from_pydata(mapped, [], faces)
    me.update()
    bm = bmesh.new()
    bm.from_mesh(me)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    bm.to_mesh(me)
    bm.free()
    me.shade_smooth()
    ob = bpy.data.objects.new(name, me)
    L._link(ob)
    return ob


def _orient_outward(ob, chart, st0):
    """Flip the mesh if its normals point into the surface (compare the topmost face to the chart normal)."""
    me = ob.data
    P, N = chart.map(st0[0], st0[1])
    best, bd = None, -1e9
    for poly in me.polygons:
        d = (poly.center - P).dot(N)
        if d > bd:
            bd, best = d, poly
    # use the face with the largest offset along N: its normal should agree with N
    sel = [p for p in me.polygons]
    top = max(sel, key=lambda p: (p.center - P).dot(N))
    if top.normal.dot(N) < 0:
        bm = bmesh.new()
        bm.from_mesh(me)
        bmesh.ops.reverse_faces(bm, faces=bm.faces[:])
        bm.to_mesh(me)
        bm.free()
        me.update()


# --------------------------------------------------------------------------------------------------- chart grid
def chart_grid(name, chart, st_fn, nu, nv, rise_fn=None, thickness=0.003, lift=0.0, offset=-1.0):
    """Patch: st_fn(u, v) -> (s, t) chart coords, rise_fn(u, v) -> height above the surface (m).  Solidified inward."""
    rise_fn = rise_fn or (lambda u, v: 0.0)

    def fn(u, v):
        s, t = st_fn(u, v)
        P, N = chart.map(s, t)
        return P + N * (lift + rise_fn(u, v))

    # decide winding from the surface normal at the middle
    s0, t0 = st_fn(0.5, 0.5)
    s1, t1 = st_fn(0.55, 0.5)
    s2, t2 = st_fn(0.5, 0.55)
    P0, N0 = chart.map(s0, t0)
    pu = fn(0.55, 0.5) - fn(0.5, 0.5)
    pv = fn(0.5, 0.55) - fn(0.5, 0.5)
    flip = pu.cross(pv).dot(N0) < 0
    return L.grid_surface(name, fn, nu, nv, thickness=thickness, flip=flip, offset=offset)


def prof(v, p=0.4):
    """rounded cross-section profile 0 at the edges, 1 in the middle (p < 1 = full, steep shoulders)."""
    return max(0.0, 1.0 - (2 * v - 1) ** 2) ** p


def ends(u, e=0.15):
    return L.smoothstep(0.0, e, u) * L.smoothstep(1.0, 1.0 - e, u)


# ------------------------------------------------------------------------------------------------------- misc
def frame_on(p, n, xh=(0, 0, 1)):
    return L.Frame.at(p, n, xh)


def add(lst, ob):
    if ob is not None:
        lst.append(ob)
    return ob


def both(ob, lst, name=None):
    """mirror a left (+X) object and register both."""
    lst.append(ob)
    m = L.mirror_x(ob, name)
    lst.append(m)
    return m


# ------------------------------------------------------------------------------------------------ closed loops
def loop_tube(name, pts, r, nring=8, closed=True, ry=None):
    """swept circle (radius r) along a closed polyline of 3-D points (eye rims, cup rims, bead lines)."""
    P = [Vector(p) for p in pts]
    n = len(P)
    verts, faces = [], []
    cen = sum(P, Vector()) / n
    ry = ry or r
    for i in range(n):
        T = (P[(i + 1) % n] - P[i - 1]).normalized()
        out = (P[i] - cen)
        out = (out - T * out.dot(T))
        if out.length < 1e-9:
            out = Vector((0, 0, 1))
        out.normalize()
        B = T.cross(out).normalized()
        for k in range(nring):
            a = 2 * PI * k / nring
            verts.append(P[i] + out * (r * math.cos(a)) + B * (ry * math.sin(a)))
    for i in range(n):
        j = (i + 1) % n if closed else i + 1
        if not closed and i == n - 1:
            break
        for k in range(nring):
            k2 = (k + 1) % nring
            faces.append((i * nring + k, j * nring + k, j * nring + k2, i * nring + k2))
    ob = L.new_mesh(name, verts, faces)
    _fix_normals(ob)
    return ob


def _fix_normals(ob):
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    bm.to_mesh(ob.data)
    bm.free()
    ob.data.update()


def almond(cx, cz, length, height, ang_deg=0.0, n=22, asym=0.25):
    """lens/almond outline (counter-clockwise) in front-view (x, z) metres, rotated by ang_deg about its centre."""
    pts = []
    ca, sa = math.cos(math.radians(ang_deg)), math.sin(math.radians(ang_deg))
    up, lo = [], []
    m = n // 2
    for i in range(m + 1):
        x = length / 2 * math.cos(PI * i / m)            # +L/2 -> -L/2
        f = 1 - (2 * x / length) ** 2
        up.append((x, height / 2 * (max(f, 0) ** 0.85) * (1 + asym * (x / length))))
    for i in range(1, m):
        x = -length / 2 * math.cos(PI * i / m)
        f = 1 - (2 * x / length) ** 2
        lo.append((x, -height / 2 * 0.8 * (max(f, 0) ** 0.85) * (1 + asym * (x / length))))
    for (x, z) in up + lo:
        pts.append((cx + x * ca - z * sa, cz + x * sa + z * ca))
    return pts


def oval(cx, cz, length, height, ang_deg=0.0, n=30, power=2.15, tilt=0.0):
    """round-oval outline (super-ellipse, no pointed ends) in front-view (x, z) metres, rotated ang_deg about its centre.
    tilt shifts the top of the oval toward +x (a slightly egg-like, tilted bulb)."""
    ca, sa = math.cos(math.radians(ang_deg)), math.sin(math.radians(ang_deg))
    pts = []
    for i in range(n):
        a = 2 * PI * i / n
        c, s_ = math.cos(a), math.sin(a)
        x = length / 2 * math.copysign(abs(c) ** (2.0 / power), c)
        z = height / 2 * math.copysign(abs(s_) ** (2.0 / power), s_)
        x += tilt * z
        pts.append((cx + x * ca - z * sa, cz + x * sa + z * ca))
    return pts


def shrink(poly, d):
    """inward offset of a convex polygon (list of (x,y)) by d (vertices move along the corner bisectors)."""
    P = [Vector((p[0], p[1])) for p in ccw(poly)]
    n = len(P)
    out = []
    for i in range(n):
        a, b, c = P[i - 1], P[i], P[(i + 1) % n]
        e1 = (b - a).normalized()
        e2 = (c - b).normalized()
        n1 = Vector((-e1.y, e1.x))
        n2 = Vector((-e2.y, e2.x))
        bis = n1 + n2
        if bis.length < 1e-9:
            out.append((b.x, b.y))
            continue
        bis.normalize()
        k = max(0.3, bis.dot(n1))
        q = b + bis * (d / k)
        out.append((q.x, q.y))
    return out


def on_surface(chart, pts2, lift=0.0):
    out = []
    for (s, t) in pts2:
        P, N = chart.map(s, t)
        out.append(P + N * lift)
    return out


# ------------------------------------------------------------------------------- reference-pixel helpers (013)
PX_S = 0.000354          # metres per pixel in spec/crops/head/front_013_head.jpg (cranium 540 px = 0.191 m)
PX_CX = 407.0            # face centre column
PX_Y0 = 30.0             # crown row


def pxz(X, Y):
    """reference pixel (013 crop) -> (x, z) metres on the right-hand half (robot's left, +x)."""
    return ((X - PX_CX) * PX_S, Z_TOP - (Y - PX_Y0) * PX_S)


def pxl(pts):
    return [pxz(X, Y) for X, Y in pts]


def lattice(TL, TR, BR, BL, rf, cf):
    """quad region (pixel corners) split into rows (fractions rf) and per-row column fractions cf -> list of polygons (x,z)."""
    def P(u, v):
        top = (TL[0] + (TR[0] - TL[0]) * u, TL[1] + (TR[1] - TL[1]) * u)
        bot = (BL[0] + (BR[0] - BL[0]) * u, BL[1] + (BR[1] - BL[1]) * u)
        return (top[0] + (bot[0] - top[0]) * v, top[1] + (bot[1] - top[1]) * v)
    cells = []
    for r in range(len(rf) - 1):
        v0, v1 = rf[r], rf[r + 1]
        cols = cf[r]
        for c in range(len(cols) - 1):
            u0, u1 = cols[c], cols[c + 1]
            cells.append(pxl([P(u0, v0), P(u1, v0), P(u1, v1), P(u0, v1)]))
    return cells


def curve_strip(name, chart, pts2, width, rise=0.004, thickness=0.003, nu=36, nv=6, p=0.4, e=0.08, lift=0.0):
    """strip along a 2-D polyline (chart coordinates) with half-width width(u)/2; rounded cross-section."""
    path = Path3([Vector((x, z, 0.0)) for x, z in pts2])

    def stf(u, v):
        c = path.at(u)
        T = path.tangent(u)
        Nn = Vector((-T.y, T.x, 0.0))
        w = width(u) if callable(width) else width
        q = c + Nn * (v - 0.5) * w
        return q.x, q.y

    return chart_grid(name, chart, stf, nu, nv, lambda u, v: rise * prof(v, p) * ends(u, e) ** 0.5, thickness, lift=lift)


Path3 = L.Path


# ------------------------------------------------------------------------------------ polar "spider web" tiling
def clip_convex(poly, clip):
    """Sutherland-Hodgman: clip polygon `poly` by the convex polygon `clip` (both lists of (x, y), any winding)."""
    clip = ccw(list(clip))
    out = list(poly)
    n = len(clip)
    for i in range(n):
        a, b = clip[i], clip[(i + 1) % n]
        inp, out = out, []
        if not inp:
            break

        def inside(p):
            return (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0]) >= -1e-12

        def inter(p, q):
            x1, y1, x2, y2 = p[0], p[1], q[0], q[1]
            x3, y3, x4, y4 = a[0], a[1], b[0], b[1]
            d = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
            if abs(d) < 1e-15:
                return q
            t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / d
            return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))

        s = inp[-1]
        for e in inp:
            if inside(e):
                if not inside(s):
                    out.append(inter(s, e))
                out.append(e)
            elif inside(s):
                out.append(inter(s, e))
            s = e
    return out


def poly_area(pts):
    a = 0.0
    for i in range(len(pts)):
        x0, y0 = pts[i]
        x1, y1 = pts[(i + 1) % len(pts)]
        a += x0 * y1 - x1 * y0
    return abs(a) / 2


def polar_tiles(F, radii, angles_deg, clip, minarea=60.0, arc_n=4, jitter=0.0):
    """Tiles of a polar grid centred on pixel point F (image y is down; angles counter-clockwise on screen), clipped to
    the convex polygon `clip` (pixel coords).  Returns polygons in pixel coordinates."""
    cells = []
    for i in range(len(radii) - 1):
        for j in range(len(angles_deg) - 1):
            r0, r1 = radii[i], radii[i + 1]
            a0, a1 = angles_deg[j], angles_deg[j + 1]
            pts = []
            for k in range(arc_n + 1):
                a = math.radians(a0 + (a1 - a0) * k / arc_n)
                pts.append((F[0] + r1 * math.cos(a), F[1] - r1 * math.sin(a)))
            for k in range(arc_n, -1, -1):
                a = math.radians(a0 + (a1 - a0) * k / arc_n)
                pts.append((F[0] + r0 * math.cos(a), F[1] - r0 * math.sin(a)))
            c = clip_convex(pts, clip)
            if len(c) >= 3 and poly_area(c) >= minarea:
                cells.append(c)
    return cells


# speaker-cup axis (left side); shared by the skull (which is carved for it) and the face module
DISC_C = Vector((0.070, -0.030, 1.884))
DISC_N = Vector((0.84, -0.54, 0.0)).normalized()
