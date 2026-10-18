"""torso_kit - helpers for parts/torso.py (the SEIS bot chest + torso core).

All design numbers are in HEAD-HEIGHTS (H = 0.2554 m) in world axes (x right-to-left, y depth with the front at -Y,
z height above the floor); every helper converts to metres.  The CHEST SHELL is the analytic front/back surface that all
plates sit on, so a plate placed with sp(x, z, lift) always hugs the same skin that the dark core is swept from.
"""
import math
import bpy
import bmesh
from mathutils import Vector, Matrix
import seis_lib as L
import seis_spec as S

H = S.H
YC = 0.03          # shell centre line depth (H)
NEXP = 3.6         # superellipse exponent of the chest/abdomen plan section (flatter front for the wide on-model plates)

# z (H)   half-width   front radius   back radius      ON-MODEL conform r1: waist 1.0 H between struts, chest plates +-1.0 H at the top
KNOTS = [(5.00, .60, .52, .54),
         (5.30, .52, .47, .49),
         (5.60, .50, .46, .48),
         (5.85, .58, .52, .54),
         (6.10, .80, .60, .62),
         (6.35, .93, .64, .68),
         (6.64, 1.06, .62, .68),
         (6.85, .90, .56, .62),
         (6.98, .64, .50, .56)]


def _hermite_tab(tab, z, col):
    if z <= tab[0][0]:
        return tab[0][col]
    if z >= tab[-1][0]:
        return tab[-1][col]
    for i in range(len(tab) - 1):
        z0, z1 = tab[i][0], tab[i + 1][0]
        if z0 <= z <= z1:
            f = (z - z0) / (z1 - z0)
            p0, p1 = tab[i][col], tab[i + 1][col]
            m0 = (p1 - tab[i - 1][col]) / (z1 - tab[i - 1][0]) if i > 0 else (p1 - p0) / (z1 - z0)
            m1 = (tab[i + 2][col] - p0) / (tab[i + 2][0] - z0) if i + 2 < len(tab) else (p1 - p0) / (z1 - z0)
            return L._hermite(p0, p1, m0 * (z1 - z0), m1 * (z1 - z0), f)
    return tab[-1][col]


def rx(z):
    return _hermite_tab(KNOTS, z, 1)


def ryf(z):
    return _hermite_tab(KNOTS, z, 2)


def ryb(z):
    return _hermite_tab(KNOTS, z, 3)


def fy(x, z):
    """front shell depth y (H) at (x, z)."""
    t = min(1.0, abs(x) / rx(z))
    return YC - ryf(z) * (1.0 - t ** NEXP) ** (1.0 / NEXP)


def by(x, z):
    t = min(1.0, abs(x) / rx(z))
    return YC + ryb(z) * (1.0 - t ** NEXP) ** (1.0 / NEXP)


def nrm(x, z):
    """outward (front) unit normal of the front shell at (x, z) (H-space direction)."""
    e = 0.004
    fx = (fy(x + e, z) - fy(x - e, z)) / (2 * e)
    fz = (fy(x, z + e) - fy(x, z - e)) / (2 * e)
    return Vector((fx, -1.0, fz)).normalized()


def nrm_b(x, z):
    e = 0.004
    gx = (by(x + e, z) - by(x - e, z)) / (2 * e)
    gz = (by(x, z + e) - by(x, z - e)) / (2 * e)
    return Vector((-gx, 1.0, -gz)).normalized()


def sp(x, z, lift=0.0):
    """world point (metres) on the FRONT shell pushed `lift` H along its normal."""
    n = nrm(x, z)
    return (Vector((x, fy(x, z), z)) + n * lift) * H


def spb(x, z, lift=0.0):
    n = nrm_b(x, z)
    return (Vector((x, by(x, z), z)) + n * lift) * H


def frame_f(x, z, lift=0.0, xhint=(1, 0, 0), ang=0.0):
    """Frame on the front shell (z axis = outward normal, y ~ up).  ang rotates it about the normal (degrees)."""
    n = nrm(x, z)
    fr = L.Frame.at(sp(x, z, lift), n, xhint)
    if ang:
        a = math.radians(ang)
        fx = fr.x * math.cos(a) + fr.y * math.sin(a)
        fy_ = -fr.x * math.sin(a) + fr.y * math.cos(a)
        fr = L.Frame(fr.o, fx, fy_, fr.z)
    return fr


def frame_b(x, z, lift=0.0, xhint=(1, 0, 0), ang=0.0):
    n = nrm_b(x, z)
    fr = L.Frame.at(spb(x, z, lift), n, xhint)
    if ang:
        a = math.radians(ang)
        fx = fr.x * math.cos(a) + fr.y * math.sin(a)
        fy_ = -fr.x * math.sin(a) + fr.y * math.cos(a)
        fr = L.Frame(fr.o, fx, fy_, fr.z)
    return fr


def smooth(a, b, x):
    return L.smoothstep(a, b, x)


# ---------------------------------------------------------------------------------------------- generic tools
def tab_interp(pts, z):
    """pts = [(z, value)] sorted by ascending z; smooth interpolation"""
    tab = [(p[0], p[1]) for p in pts]
    return _hermite_tab(tab, z, 1)


def orient_grid(name, f, nu, nv, thickness, outward, offset=-1.0):
    """grid_surface whose normals point along `outward` (a world direction at the surface centre)."""
    p0 = Vector(f(0.5, 0.5))
    du = Vector(f(0.52, 0.5)) - Vector(f(0.48, 0.5))
    dv = Vector(f(0.5, 0.52)) - Vector(f(0.5, 0.48))
    flip = du.cross(dv).dot(Vector(outward)) < 0
    return L.grid_surface(name, f, nu, nv, thickness=thickness, flip=flip, offset=offset)


def ring_mesh(name, pts, ups, w, hgt, n_sec=12, sec_n=3.0, closed=True, wf=None):
    """Swept closed (or open) band: pts world points, ups = surface normals; w, hgt = half width / half height (m)
    (floats or callables of the index fraction).  Returns an object with consistent outward faces."""
    P = [Vector(p) for p in pts]
    N = len(P)
    rings = []
    for i in range(N):
        a = P[(i + 1) % N] if (closed or i < N - 1) else P[i]
        b = P[(i - 1) % N] if (closed or i > 0) else P[i]
        T = (a - b).normalized()
        U = (Vector(ups[i]) - T * Vector(ups[i]).dot(T)).normalized()
        Lat = T.cross(U).normalized()
        f = i / max(1, N - 1)
        ww = w(f) if callable(w) else w
        hh_ = hgt(f) if callable(hgt) else hgt
        ring = []
        for k in range(n_sec):
            th = 2 * math.pi * k / n_sec
            c, s = math.cos(th), math.sin(th)
            e = 2.0 / sec_n
            ring.append(P[i] + Lat * (ww * L.spow(c, e)) + U * (hh_ * L.spow(s, e)))
        rings.append(ring)
    verts, faces = [], []
    for r in rings:
        verts.extend(r)
    nr = len(rings)
    last = nr if closed else nr - 1
    for i in range(last):
        i2 = (i + 1) % nr
        for k in range(n_sec):
            k2 = (k + 1) % n_sec
            faces.append((i * n_sec + k, i2 * n_sec + k, i2 * n_sec + k2, i * n_sec + k2))
    if not closed:
        faces.append(tuple(range(n_sec - 1, -1, -1)))
        faces.append(tuple((nr - 1) * n_sec + k for k in range(n_sec)))
    ob = L.new_mesh(name, verts, faces)
    _fix_orientation(ob)
    return ob


def _fix_orientation(ob):
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    bm.normal_update()
    vol = bm.calc_volume(signed=True)
    if vol < 0:
        bmesh.ops.reverse_faces(bm, faces=bm.faces[:])
        bm.to_mesh(ob.data)
        ob.data.update()
    bm.free()


def sweep_on_shell(name, pts_xz, half_w, half_h, n=3.2, embed=0.55, nring=18, lift=0.0, caps=True, wf=None,
                   hf=None, round_ends=None):
    """Band running along a path of (x, z) points ON the front shell.  half_w/half_h in H (floats or (t) callables)."""
    hw0 = half_w if not callable(half_w) else half_w(0.5)
    hh0 = half_h if not callable(half_h) else half_h(0.5)
    pts = []
    for (x, z) in pts_xz:
        h_here = half_h(0.5) if callable(half_h) else half_h
        pts.append(sp(x, z, lift + h_here * (1.0 - embed) - h_here * embed * 0.0))
    ts = [0, 0.25, 0.5, 0.75, 1.0]
    keys = []
    for t in ts:
        a = (half_w(t) if callable(half_w) else half_w) * H
        b = (half_h(t) if callable(half_h) else half_h) * H
        keys.append((t, a, b, n))
    sw = L.Sweep(pts, keys)
    ob = sw.mesh(name, nring=nring, nstations=max(10, int(sw.path.length / 0.012)), caps=caps,
                 round_start=round_ends, round_end=round_ends)
    return ob, sw


def arc_pts(p0, p1, n):
    return [p0.lerp(p1, i / n) for i in range(n + 1)]


def bolts_on(plist, radius=0.0065, height=0.0045, normal_fn=None, hexagon=True, name="bolts"):
    """plist = [(point, normal)] -> one joined mesh of hex bolts."""
    parts = []
    for i, (p, n) in enumerate(plist):
        parts.append(L.bolt(f"{name}_{i}", p, n, radius, height, hexagon=hexagon))
    return L.join(parts, name)


def rr(w, h, r, n=5):
    """rounded-rectangle outline in H -> metres"""
    return [(x * H, y * H) for (x, y) in L.outline_rrect(w, h, r, n)]


def poly(points_h, round_r=0.0, n=4):
    pts = [(x * H, y * H) for (x, y) in points_h]
    if round_r:
        return L.outline_poly(pts, round_r * H, n)
    return pts


# ----------------------------------------------------------------------------------------------- pillow plate
PROF_PILLOW = [(1.0, 0.0), (0.985, 0.28), (0.95, 0.58), (0.89, 0.80), (0.78, 0.93), (0.6, 0.99), (0.35, 1.0),
               (0.0, 1.0)]
PROF_SOFT = [(1.0, 0.0), (0.97, 0.45), (0.9, 0.78), (0.78, 0.93), (0.58, 0.99), (0.3, 1.0), (0.0, 1.0)]
PROF_FLAT = [(1.0, 0.0), (0.0, 0.0)]
PROF_TABLET = [(1.0, 0.0), (0.99, 0.55), (0.96, 0.90), (0.90, 1.0), (0.0, 1.0)]


def pillow(name, outline, frame=None, rise=0.01, thickness=0.01, steps=None, inset=None, power=None, profile=None,
           **kw):
    """Domed plate from a CCW 2-D outline (metres) in the xy plane of `frame` (dome toward +z): concentric rings scaled
    toward the centroid with a height profile, a vertical side wall and a flat back.  Drop-in for L.plate with a much
    lighter, cleaner topology (no insets)."""
    frame = frame or L.Frame()
    n = len(outline)
    cx = sum(p[0] for p in outline) / n
    cy = sum(p[1] for p in outline) / n
    prof = profile or PROF_PILLOW
    verts, faces = [], []
    ring_idx = []
    for (s, hf) in prof:
        if s <= 1e-6:
            verts.append(frame.p(cx, cy, rise * hf))
            ring_idx.append(len(verts) - 1)
        else:
            base = len(verts)
            for (x, y) in outline:
                verts.append(frame.p(cx + (x - cx) * s, cy + (y - cy) * s, rise * hf))
            ring_idx.append(base)
    for r in range(len(prof) - 1):
        a0 = ring_idx[r]
        if prof[r + 1][0] <= 1e-6:
            c = ring_idx[r + 1]
            for i in range(n):
                faces.append((c, a0 + i, a0 + (i + 1) % n))
        else:
            b0 = ring_idx[r + 1]
            for i in range(n):
                j = (i + 1) % n
                faces.append((a0 + i, a0 + j, b0 + j, b0 + i))
    top0 = ring_idx[0]
    if thickness > 0:
        bk = len(verts)
        for (x, y) in outline:
            verts.append(frame.p(x, y, -thickness))
        for i in range(n):
            j = (i + 1) % n
            faces.append((top0 + i, bk + i, bk + j, top0 + j))
        verts.append(frame.p(cx, cy, -thickness))
        c = len(verts) - 1
        for i in range(n):
            j = (i + 1) % n
            faces.append((c, bk + j, bk + i))
    ob = L.new_mesh(name, verts, faces)
    _fix_orientation(ob)
    return ob
