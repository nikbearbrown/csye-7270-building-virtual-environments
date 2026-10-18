"""pelvis_kit - private helpers for parts/pelvis.py (does not touch the shared toolkit).

All positions are given in head-heights (H units) through P(x, y, z); the figure faces -Y.
"""
import math
import bpy
import bmesh
from mathutils import Vector, Matrix

import seis_lib as L
import seis_spec as S

H = S.H
PI = math.pi
spow = L.spow


def P(x, y, z):
    return Vector((x * H, y * H, z * H))


def mk(name, verts, faces, recalc=True, smooth=True):
    """Mesh object from raw lists, normals recalculated to point out (closed shells)."""
    me = bpy.data.meshes.new(name)
    me.from_pydata([tuple(v) for v in verts], [], [tuple(f) for f in faces])
    me.update()
    if recalc:
        bm = bmesh.new()
        bm.from_mesh(me)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
        bm.to_mesh(me)
        bm.free()
    if smooth:
        me.shade_smooth()
    ob = bpy.data.objects.new(name, me)
    return L._link(ob)


def fin(ob, mat, bone="root", bevel=0.002, seg=2, wear=None, angle=38.0, **kw):
    L.finish(ob, mat, bevel=bevel, bevel_segments=seg, bone=bone, wear=wear, angle=angle, **kw)
    return ob


def mirror(ob):
    """Mirror a '.L' object to '.R' (real geometry)."""
    return L.mirror_x(ob)


def join(objs, name):
    return L.join(objs, name)


# ------------------------------------------------------------------------------------------------ closed lofts
def loft_rings(name, rings, closed_u=False, cap=True):
    """Mesh through a list of rings (each a list of Vectors, closed around).  closed_u wraps the first ring to the last
    (a torus).  cap adds n-gon end caps otherwise."""
    n = len(rings[0])
    verts = []
    for r in rings:
        verts.extend(r)
    faces = []
    nr = len(rings)
    last = nr if closed_u else nr - 1
    for i in range(last):
        i2 = (i + 1) % nr
        for k in range(n):
            k2 = (k + 1) % n
            faces.append((i * n + k, i2 * n + k, i2 * n + k2, i * n + k2))
    if not closed_u and cap:
        faces.append(tuple(range(n - 1, -1, -1)))
        faces.append(tuple((nr - 1) * n + k for k in range(n)))
    return mk(name, verts, faces)


def rrect_pt(t, a, b, n=3.4):
    """Point of a superellipse profile at angle t, half sizes a (radial) and b (vertical)."""
    return a * spow(math.cos(t), 2.0 / n), b * spow(math.sin(t), 2.0 / n)


def plan_pt(a, A, B, n):
    """Superellipse plan point, front = -y.  a in radians, A,B half sizes (H units)."""
    return A * spow(math.cos(a), 2.0 / n), -B * spow(math.sin(a), 2.0 / n)


def plan_normal(a, A, B, n):
    e = 1e-3
    x1, y1 = plan_pt(a + e, A, B, n)
    x0, y0 = plan_pt(a - e, A, B, n)
    tx, ty = x1 - x0, y1 - y0
    ln = math.hypot(tx, ty) or 1.0
    nx, ny = ty / ln, -tx / ln
    x, y = plan_pt(a, A, B, n)
    if nx * x + ny * y < 0:
        nx, ny = -nx, -ny
    return nx, ny


def ring_around(name, A, B, n_plan, zfun, prof_a, prof_b, nu=112, nv=24, n_prof=3.4, yoff=0.0, mod=None):
    """A closed rolled band that follows a superellipse plan (A x B half sizes in H) at heights zfun(x, y).
    prof_a(x, y) radial half size, prof_b(x, y) vertical half size (H units)."""
    rings = []
    for i in range(nu):
        a = 2 * PI * i / nu
        x, y = plan_pt(a, A, B, n_plan)
        y += yoff
        e = 1e-3
        x1, y1 = plan_pt(a + e, A, B, n_plan)
        x0, y0 = plan_pt(a - e, A, B, n_plan)
        tx, ty = x1 - x0, y1 - y0
        ln = math.hypot(tx, ty) or 1.0
        nx, ny = ty / ln, -tx / ln
        if nx * x + ny * (y - yoff) < 0:
            nx, ny = -nx, -ny
        zc = zfun(x, y)
        pa, pb = prof_a(x, y), prof_b(x, y)
        ring = []
        for j in range(nv):
            t = 2 * PI * j / nv
            r, v = rrect_pt(t, pa, pb, n_prof)
            if mod:
                r = mod(a, t, r, v, pa, pb)
            ring.append(P(x + nx * r, y + ny * r, zc + v))
        rings.append(ring)
    return loft_rings(name, rings, closed_u=True)


# ------------------------------------------------------------------------------------------------ small mechanics
def gear(name, c, normal, r_out, r_in, teeth, thick, xhint=(1, 0, 0), hole=0.0):
    """Spur gear as a solid prism with `teeth` trapezoid teeth; c world centre, normal = axis."""
    fr = L.Frame.at(c, normal, xhint)
    m = teeth * 4
    pts = []
    for i in range(m):
        a = 2 * PI * i / m
        k = i % 4
        r = r_out if k in (1, 2) else r_in
        pts.append((r * math.cos(a), r * math.sin(a)))
    verts, faces = [], []
    for z in (-thick / 2, thick / 2):
        for (x, y) in pts:
            verts.append(fr.p(x, y, z))
    for i in range(m):
        i2 = (i + 1) % m
        faces.append((i, i2, m + i2, m + i))
    faces.append(tuple(range(m - 1, -1, -1)))
    faces.append(tuple(m + k for k in range(m)))
    ob = mk(name, verts, faces)
    return ob


def ring_disc(name, c, normal, r_out, r_in, depth, xhint=(1, 0, 0), seg=48):
    """Flat ring (annulus) of depth, along the frame z; centre c at the middle of the depth."""
    fr = L.Frame.at(c, normal, xhint)
    verts, faces = [], []
    for z in (-depth / 2, depth / 2):
        for r in (r_out, r_in):
            for i in range(seg):
                a = 2 * PI * i / seg
                verts.append(fr.p(r * math.cos(a), r * math.sin(a), z))
    # layout: [z0 out][z0 in][z1 out][z1 in]
    def idx(zi, ri, i):
        return (zi * 2 + ri) * seg + (i % seg)
    for i in range(seg):
        faces.append((idx(0, 0, i), idx(0, 0, i + 1), idx(1, 0, i + 1), idx(1, 0, i)))       # outer wall
        faces.append((idx(0, 1, i + 1), idx(0, 1, i), idx(1, 1, i), idx(1, 1, i + 1)))       # inner wall
        faces.append((idx(1, 0, i), idx(1, 0, i + 1), idx(1, 1, i + 1), idx(1, 1, i)))       # top
        faces.append((idx(0, 0, i + 1), idx(0, 0, i), idx(0, 1, i), idx(0, 1, i + 1)))       # bottom
    return mk(name, verts, faces)


def hex_bolts(name, specs, radius=0.0055, height=0.0035):
    """Join many hex bolts into ONE mesh.  specs = [(world_centre, normal), ...]."""
    parts = []
    for i, (c, n) in enumerate(specs):
        parts.append(L.bolt(f"{name}_b{i}", c, n, radius=radius, height=height, hexagon=True))
    return L.join(parts, name)


def round_rivets(name, specs, radius=0.0035, height=0.0025):
    parts = []
    for i, (c, n) in enumerate(specs):
        parts.append(L.bolt(f"{name}_r{i}", c, n, radius=radius, height=height, hexagon=False))
    return L.join(parts, name)


def surf_normal_pts(fn, u, v, e=1e-3):
    a = fn(min(1.0, u + e), v) - fn(max(0.0, u - e), v)
    b = fn(u, min(1.0, v + e)) - fn(u, max(0.0, v - e))
    n = a.cross(b)
    return n.normalized() if n.length > 1e-12 else Vector((0, 0, 1))


# ================================================================================================ round 2 additions
def olive_material():
    """Darker olive-bronze band metal (#5A4C2F family, ONMODEL belt) built as a COPY of the shared bronze so the shared
    material is untouched.  Edge glint stays champagne (the shared bronze edge mix)."""
    name = "SEIS_belt_olive"
    m = bpy.data.materials.get(name)
    if m is not None:
        return m
    src = L.mat("bronze")
    m = src.copy()
    m.name = name
    import seis_mat as SM
    tgt = {tuple(round(c, 3) for c in SM.C_BAND[:3]): SM.hexlin("#4A4430"),
           tuple(round(c, 3) for c in SM.C_BAND_SHADE[:3]): SM.hexlin("#2E2812")}
    for nd in m.node_tree.nodes:
        if nd.type == "MIX":
            for s in nd.inputs:
                if s.identifier in ("A_Color", "B_Color") and not s.is_linked:
                    k = tuple(round(c, 3) for c in s.default_value[:3])
                    if k in tgt:
                        s.default_value = tgt[k]
    m.diffuse_color = SM.hexlin("#4A4430")
    for nd in m.node_tree.nodes:                      # a little less mirror-like than the shared band metal
        if nd.type == "BSDF_PRINCIPLED":
            nd.inputs["Roughness"].default_value = 0.42
    return m


def arc_around(name, A, B, n_plan, a0, a1, zfun, prof_a, prof_b, nu=24, nv=20, n_prof=3.4, yoff=0.0):
    """Like ring_around but an OPEN arc a0..a1 (radians, front = pi/2) with capped ends: one separate plate."""
    rings = []
    for i in range(nu + 1):
        a = a0 + (a1 - a0) * i / nu
        x, y = plan_pt(a, A, B, n_plan)
        y += yoff
        e = 1e-3
        x1, y1 = plan_pt(a + e, A, B, n_plan)
        x0, y0 = plan_pt(a - e, A, B, n_plan)
        tx, ty = x1 - x0, y1 - y0
        ln = math.hypot(tx, ty) or 1.0
        nx, ny = ty / ln, -tx / ln
        if nx * x + ny * (y - yoff) < 0:
            nx, ny = -nx, -ny
        zc = zfun(x, y)
        pa, pb = prof_a(x, y), prof_b(x, y)
        ring = []
        for j in range(nv):
            t = 2 * PI * j / nv
            r, v = rrect_pt(t, pa, pb, n_prof)
            ring.append(P(x + nx * r, y + ny * r, zc + v))
        rings.append(ring)
    return loft_rings(name, rings, closed_u=False, cap=True)


def fastener(name, c, n, r=0.0045, h=0.003, washer=True, hexagon=True):
    """One hex (or round) head fastener with an optional thin washer, ONE mesh.  c = point on the surface, n = outward."""
    parts = []
    nv = Vector(n).normalized()
    if washer:
        parts.append(L.cylinder(name + "_w", r * 1.75, 0.0011, L.Frame.at(c + nv * 0.00055, nv), segments=20))
        c = c + nv * 0.0011
    parts.append(L.bolt(name + "_h", c, nv, radius=r, height=h, hexagon=hexagon))
    return L.join(parts, name)


def clamp_ring(name, c, tangent, r_tube, width=0.0045, grow=0.0016):
    """Bronze band clamp (a short fat torus-like ring) around a hose at point c, with a tiny hex screw boss."""
    tg = Vector(tangent).normalized()
    tor = L.torus(name, r_tube + grow * 0.6, grow * 0.9, L.Frame.at(c, tg), major_seg=24, minor_seg=8)
    return tor


def hose(name, pts, r, nring=10):
    return L.tube(name, pts, r, nring=nring, round_ends=True)
