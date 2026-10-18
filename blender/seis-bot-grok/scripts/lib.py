# Geometry helpers for the robot build (Blender 4.2, bpy)
import bpy, bmesh, math
from mathutils import Vector as V, Matrix, Quaternion
from mathutils.bvhtree import BVHTree

PARTS = []   # (obj, bone)
PATHS = {}
MATS = {}
COLL = None

def se(a, p):
    c, s = math.cos(a), math.sin(a)
    e = 2.0 / p
    return math.copysign(abs(c) ** e, c), math.copysign(abs(s) ** e, s)

def tube_bm(rings, nseg=32, arc=None, caps=True, loop=False):
    bm = bmesh.new()
    closed = arc is None
    if closed:
        angs = [2 * math.pi * i / nseg for i in range(nseg)]
    else:
        angs = [arc[0] + (arc[1] - arc[0]) * i / (nseg - 1) for i in range(nseg)]
    rows = []
    for r in rings:
        c = V(r['c']); u = V(r.get('u', (1, 0, 0))).normalized(); v = V(r.get('v', (0, 1, 0))).normalized()
        rx, ry = r['rx'], r['ry']; ryb = r.get('ryb', ry); p = r.get('p', 2.0); bend = r.get('bend', 0.0)
        row = []
        for a in angs:
            x, y = se(a, p)
            X = rx * x
            Y = (ryb if y > 0 else ry) * y + bend * x * x
            row.append(bm.verts.new(c + u * X + v * Y))
        rows.append(row)
    n = len(angs)
    nr = len(rows)
    pairs = [(i, i + 1) for i in range(nr - 1)]
    if loop:
        pairs.append((nr - 1, 0))
    for i, k in pairs:
        for j in range(n if closed else n - 1):
            j2 = (j + 1) % n
            try:
                bm.faces.new((rows[i][j], rows[i][j2], rows[k][j2], rows[k][j]))
            except ValueError:
                pass
    if closed and caps and not loop:
        for row, rr in ((rows[0], rings[0]), (rows[-1], rings[-1])):
            cv = bm.verts.new(V(rr['c']))
            for j in range(n):
                try:
                    bm.faces.new((row[j], row[(j + 1) % n], cv))
                except ValueError:
                    pass
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6)
    bmesh.ops.dissolve_degenerate(bm, dist=1e-7, edges=bm.edges)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return bm

def mk(name, bm, mat, bone, sub=1, solid=None, smooth=True, bevel=None):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me)
    COLL.objects.link(ob)
    me.materials.append(MATS[mat])
    if smooth:
        me.shade_smooth()
    if solid:
        m = ob.modifiers.new('Solidify', 'SOLIDIFY'); m.thickness = solid; m.offset = 1.0
        m.use_even_offset = True
    if bevel:
        m = ob.modifiers.new('Bevel', 'BEVEL'); m.width = bevel; m.segments = 2
        m.limit_method = 'ANGLE'; m.angle_limit = math.radians(35)
    if sub:
        m = ob.modifiers.new('Subsurf', 'SUBSURF'); m.levels = sub; m.render_levels = sub
    PARTS.append((ob, bone))
    return ob

def vloft(name, data, mat, bone, p=2.4, nseg=32, sub=1, **kw):
    """data: (z, cx, cy, rx, ryf, ryb)"""
    rings = [dict(c=(cx, cy, z), rx=rx, ry=ryf, ryb=ryb, p=p) for (z, cx, cy, rx, ryf, ryb) in data]
    return mk(name, tube_bm(rings, nseg), mat, bone, sub=sub, **kw)

def spline(pts, n=40, closed=False):
    """Catmull-Rom resample"""
    P = [V(p) for p in pts]
    m = len(P)
    out = []
    segs = m if closed else m - 1
    for i in range(n if closed else n):
        t = i / (n if closed else (n - 1)) * segs
        k = min(int(t), segs - 1); f = t - k
        def g(j):
            if closed: return P[j % m]
            return P[max(0, min(m - 1, j))]
        p0, p1, p2, p3 = g(k - 1), g(k), g(k + 1), g(k + 2)
        out.append(0.5 * ((2 * p1) + (-p0 + p2) * f + (2 * p0 - 5 * p1 + 4 * p2 - p3) * f * f + (-p0 + 3 * p1 - 3 * p2 + p3) * f ** 3))
    return out

def chaikin(pts, it=3):
    P = [V(p) for p in pts]
    for _ in range(it):
        Q = []
        for i in range(len(P)):
            a, b = P[i], P[(i + 1) % len(P)]
            Q += [a * 0.75 + b * 0.25, a * 0.25 + b * 0.75]
        P = Q
    return P

def sweep_rings(pts, width, thick, p=2.0, normals=None, ref=(0, 0, 1), bend=0.0, loop=False):
    rings = []; N = len(pts)
    for i, pt in enumerate(pts):
        t = i / (N - 1)
        if loop:
            T = (pts[(i + 1) % N] - pts[(i - 1) % N]).normalized()
        else:
            T = (pts[min(i + 1, N - 1)] - pts[max(i - 1, 0)]).normalized()
        nv = V(normals[i]) if normals else V(ref)
        v = (nv - T * nv.dot(T)).normalized()
        u = T.cross(v).normalized()
        w = width(t) if callable(width) else width
        th = thick(t) if callable(thick) else thick
        b = bend(t) if callable(bend) else bend
        rings.append(dict(c=pt, u=u, v=v, rx=w, ry=th, p=p, bend=b))
    return rings

def sweep(name, pts, width, thick, mat, bone, p=2.0, normals=None, ref=(0, 0, 1), bend=0.0, nseg=16, sub=1, loop=False, caps=True):
    keep = [0]
    for i in range(1, len(pts)):
        if (V(pts[i]) - V(pts[keep[-1]])).length > 1e-4:
            keep.append(i)
    if loop and len(keep) > 2 and (V(pts[keep[-1]]) - V(pts[keep[0]])).length < 1e-4:
        keep.pop()
    pts = [V(pts[i]) for i in keep]
    if normals: normals = [normals[i] for i in keep]
    rings = sweep_rings(pts, width, thick, p, normals, ref, bend, loop)
    PATHS[name] = [(V(r['c']), V(r['v']), r['ry']) for r in rings]
    return mk(name, tube_bm(rings, nseg, loop=loop, caps=caps), mat, bone, sub=sub)

def rod(name, a, b, r, mat, bone, nseg=16, sub=1, p=2.0, r2=None):
    a, b = V(a), V(b)
    d = (b - a).normalized()
    ref = V((0, 0, 1)) if abs(d.z) < 0.9 else V((1, 0, 0))
    rr = r2 if r2 is not None else r
    rings = []
    for t, rad in ((0, r * 0.8), (0.03, r), (0.97, rr), (1, rr * 0.8)):
        rings.append((a.lerp(b, t), rad))
    u = d.cross(ref).normalized(); v = d.cross(u).normalized()
    return mk(name, tube_bm([dict(c=c, u=u, v=v, rx=rad, ry=rad, p=p) for c, rad in rings], nseg), mat, bone, sub=sub)

def disc(name, c, axis, r, h, mat, bone, nseg=32, bevel=0.15, sub=1, p=2.0):
    c = V(c); d = V(axis).normalized()
    ref = V((0, 0, 1)) if abs(d.z) < 0.9 else V((1, 0, 0))
    u = d.cross(ref).normalized(); v = d.cross(u).normalized()
    rings = []
    for t, s in ((-0.5, 1 - bevel), (-0.5 + bevel * 0.3, 1.0), (0.5 - bevel * 0.3, 1.0), (0.5, 1 - bevel)):
        rings.append(dict(c=c + d * h * t, u=u, v=v, rx=r * s, ry=r * s, p=p))
    return mk(name, tube_bm(rings, nseg), mat, bone, sub=sub)

# ---------- projection
def bvh(obj):
    dg = bpy.context.evaluated_depsgraph_get()
    ev = obj.evaluated_get(dg)
    me = ev.to_mesh()
    bm = bmesh.new(); bm.from_mesh(me); bm.transform(obj.matrix_world)
    t = BVHTree.FromBMesh(bm)
    bm.free(); ev.to_mesh_clear()
    return t

def bvh_multi(objs):
    dg = bpy.context.evaluated_depsgraph_get()
    bm = bmesh.new()
    for obj in objs:
        ev = obj.evaluated_get(dg)
        me = ev.to_mesh()
        me.transform(obj.matrix_world)
        bm.from_mesh(me)
        ev.to_mesh_clear()
    t = BVHTree.FromBMesh(bm); bm.free()
    return t

def hit(tree, o, d):
    loc, n, i, dist = tree.ray_cast(V(o), V(d).normalized(), 10.0)
    return loc, n

def front_map(y0=-1.5):
    return lambda a, b: (V((a, y0, b)), V((0, 1, 0)))

def back_map(y0=1.5):
    return lambda a, b: (V((a, y0, b)), V((0, -1, 0)))

def side_map(s, x0=1.5):
    return lambda a, b: (V((s * x0, a, b)), V((-s, 0, 0)))

def top_map(z0=3.0):
    return lambda a, b: (V((a, b, z0)), V((0, 0, -1)))

def cyl_map(axis_pt_fn, R=0.6):
    """(phi, z): phi=0 front(-Y), positive towards +X"""
    def f(phi, z):
        cx, cy = axis_pt_fn(z)
        d = V((math.sin(phi), -math.cos(phi), 0))
        return V((cx, cy, z)) + d * R, -d
    return f

def radial_map(center, plane='yz'):
    """(theta, x) in YZ plane around center: theta=0 -> forward(-Y), 90 -> up"""
    c = V(center)
    def f(th, x):
        d = V((0, -math.cos(th), math.sin(th)))
        o = V((x, c.y, c.z)) + d * 0.6
        return o, -d
    return f

def surf_path(tree, mapper, pts2d, offset=0.0, n=None, closed=False, nearest=False):
    if n:
        pts2d = [(p.x, p.y) for p in spline([V((a, b, 0)) for a, b in pts2d], n, closed)]
    P, N = [], []
    for a, b in pts2d:
        o, d = mapper(a, b)
        loc, nn = hit(tree, o, d)
        if loc is None and nearest:
            hh = tree.ray_cast(o + d * 3.0, -d, 10.0)
            loc, nn = hh[0], hh[1]
            if loc is not None: nn = -nn if nn.dot(d) > 0 else nn
        if loc is None:
            continue
        P.append(loc + nn * offset); N.append(nn)
    return P, N

def plate(name, tree, mapper, outline, mat, bone, offset=0.003, thick=0.01, rings=(0.3, 0.55, 0.75, 0.88, 0.95, 1.0), sub=1, nout=64, disp=None, merge=6e-5):
    ol = [V((p[0], p[1], 0)) for p in outline]
    if len(ol) < nout:
        ol = spline(ol, nout, closed=True)
    cen = sum(ol, V()) / len(ol)
    bm = bmesh.new(); rows = []
    def proj(a, b):
        o, d = mapper(a, b)
        loc, nn = hit(tree, o, d)
        if loc is None:
            loc, nn, i_, d_ = tree.find_nearest(o + d * 0.3)
        return loc + nn * (offset + (disp(a, b) if disp else 0.0))
    for s in rings:
        row = []
        for p in ol:
            q = cen + (p - cen) * s
            row.append(bm.verts.new(proj(q.x, q.y)))
        rows.append(row)
    cv = bm.verts.new(proj(cen.x, cen.y))
    n = len(ol)
    for j in range(n):
        bm.faces.new((rows[0][j], rows[0][(j + 1) % n], cv))
    for i in range(len(rows) - 1):
        for j in range(n):
            j2 = (j + 1) % n
            bm.faces.new((rows[i][j], rows[i][j2], rows[i + 1][j2], rows[i + 1][j]))
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=merge)
    bmesh.ops.dissolve_degenerate(bm, dist=1e-5, edges=bm.edges)
    bad = [e for e in bm.edges if len(e.link_faces) > 2]
    if bad: bmesh.ops.delete(bm, geom=list({f for e in bad for f in e.link_faces}), context='FACES')
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    # make normals point away from projection direction (outward)
    o, d = mapper(cen.x, cen.y)
    if sum((f.normal.dot(d) for f in bm.faces)) > 0:
        bmesh.ops.reverse_faces(bm, faces=bm.faces)
    ob = mk(name, bm, mat, bone, sub=0)
    m = ob.modifiers.new('Solidify', 'SOLIDIFY'); m.thickness = thick; m.offset = 1.0; m.use_even_offset = False
    m.use_rim = True
    if sub:
        m = ob.modifiers.new('Subsurf', 'SUBSURF'); m.levels = sub; m.render_levels = sub
    return ob

def rim(name, tree, mapper, outline, mat, bone, offset, width, thick, n=80, p=2.0):
    P, N = surf_path(tree, mapper, [(q[0], q[1]) for q in outline], offset, n=n, closed=True)
    return sweep(name, P, width, thick, mat, bone, p=p, normals=N, loop=True, nseg=12)

def ellipse(cx, cz, rx, rz, n=48, rot=0.0):
    out = []
    for i in range(n):
        t = 2 * math.pi * i / n
        x, z = rx * math.cos(t), rz * math.sin(t)
        c, s = math.cos(rot), math.sin(rot)
        out.append((cx + x * c - z * s, cz + x * s + z * c))
    return out

def lens(cx, cz, w, h, n=64, k=1.0, rot=0.0):
    out = []
    for i in range(n):
        t = 2 * math.pi * i / n
        z = h * math.cos(t)
        st = math.sin(t)
        x = w * math.copysign(abs(st) ** (2 * k - 1 if k > 0.5 else 1), st) * abs(st)
        if k <= 0.5:
            x = w * st
        c, s = math.cos(rot), math.sin(rot)
        out.append((cx + x * c - z * s, cz + x * s + z * c))
    return out

def rrect(cx, cz, w, h, r=0.3, n=48):
    """rounded rect via superellipse"""
    out = []
    for i in range(n):
        t = 2 * math.pi * i / n
        x, y = se(t, 5.0)
        out.append((cx + w * x, cz + h * y))
    return out

def mirror_pts(pts, s):
    return [(s * a, b) for a, b in pts]


def bolt(name, pos, n, bone, r=0.0035, h=0.0028, mat='silver'):
    n = V(n).normalized()
    return disc(name, V(pos) + n * (h * 0.35), n, r, h, mat, bone, nseg=6, bevel=0.25, sub=0)

def outline_pts(outline, k):
    ol = spline([V((p[0], p[1], 0)) for p in outline], 128, closed=True)
    return [(ol[int(i * 128 / k)].x, ol[int(i * 128 / k)].y) for i in range(k)]

def bolts_outline(prefix, tree, mapper, outline, k, bone, offset=0.0, r=0.0035, mat='silver', shrink=1.0):
    ol = outline_pts(outline, k)
    cx = sum(p[0] for p in ol) / k; cz = sum(p[1] for p in ol) / k
    out = []
    for i, (a, b) in enumerate(ol):
        a = cx + (a - cx) * shrink; b = cz + (b - cz) * shrink
        o, d = mapper(a, b)
        loc, nn = hit(tree, o, d)
        if loc is None: continue
        nm_ = prefix[:-2] + '_Bolt%02d' % i + prefix[-2:] if prefix[-2:] in ('.L', '.R') else '%s_Bolt%02d' % (prefix, i)
        out.append(bolt(nm_, loc + nn * offset, nn, bone, r=r, mat=mat))
    return out

def ball(name, pos, r, mat, bone):
    return disc(name, pos, (0, 0, 1), r, 2 * r, mat, bone, nseg=10, bevel=0.9, sub=1)


def bolts_along(name, k, bone, r=0.003, t0=0.1, t1=0.9, mat='silver', side=1.0):
    P = PATHS[name]; n = len(P); out = []
    base, sd = (name[:-2], name[-2:]) if name[-2:] in ('.L', '.R') else (name, '')
    for j in range(k):
        t = t0 + (t1 - t0) * (j / (k - 1) if k > 1 else 0.5)
        c, v, th = P[min(n - 1, int(t * (n - 1)))]
        out.append(bolt('%s_Rivet%02d%s' % (base, j, sd), c + v * th * side, v * side, bone, r=r, mat=mat))
    return out

def band_shell(name, J, s, R, a0, a1, b0, b1, mat, bone, thick=0.02, na=12, nb=44, curl_back=0.3, curl_front=0.35, flare=0.15, sub=2):
    """Shoulder band: strip of a sphere around joint J with poles on the Y axis.
    a = angle in XZ plane (deg, 0 = outward, 90 = up), b = angle toward -Y(front, b<0) / +Y(back, b>0)."""
    J = V(J)
    bm = bmesh.new(); grid = []
    for j in range(nb):
        tb = j / (nb - 1); b = b0 + (b1 - b0) * tb
        w = 0.5 + 0.5 * math.sin(math.pi * tb) ** 0.5
        am = (a0 + a1) / 2 + (-curl_back * b if b > 0 else -curl_front * b)
        ah = (a1 - a0) / 2 * w
        Rb = R * (1 + flare * (abs(b) / 90.0) ** 2)
        br = math.radians(b)
        row = []
        for i in range(na):
            a = math.radians(am - ah + 2 * ah * i / (na - 1))
            d = V((s * math.cos(a) * math.cos(br), math.sin(br), math.sin(a) * math.cos(br)))
            row.append(bm.verts.new(J + d * Rb))
        grid.append(row)
    for j in range(nb - 1):
        for i in range(na - 1):
            bm.faces.new((grid[j][i], grid[j][i + 1], grid[j + 1][i + 1], grid[j + 1][i]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    # normals outward from J
    f0 = bm.faces[len(bm.faces) // 2]
    if f0.normal.dot(f0.calc_center_median() - J) < 0:
        bmesh.ops.reverse_faces(bm, faces=bm.faces)
    ob = mk(name, bm, mat, bone, sub=0)
    m = ob.modifiers.new('Solidify', 'SOLIDIFY'); m.thickness = thick; m.offset = -1.0; m.use_even_offset = True
    m = ob.modifiers.new('Subsurf', 'SUBSURF'); m.levels = sub; m.render_levels = sub
    return ob

def ellipsoid(name, c, rx, ry, rz, mat, bone, nseg=24, nz=10, sub=1):
    c = V(c); rings = []
    for i in range(nz + 1):
        t = -1 + 2 * i / nz
        z = t * rz; r = math.sqrt(max(1e-6, 1 - t * t))
        rings.append(dict(c=c + V((0, 0, z)), rx=max(rx * r, 1e-4), ry=max(ry * r, 1e-4), p=2.0))
    return mk(name, tube_bm(rings[1:-1], nseg), mat, bone, sub=sub)

def cowl_shell(name, J, s, R3, a0, a1, b0, b1, mat, bone, thick=0.025, na=14, nb=48, curl_back=0.25, curl_front=0.3, hug=0.25, sub=2, keep=0.0):
    """Smooth shoulder plate on an ellipsoid (radii R3) around J; a = elevation in XZ (0 out, 90 up), b = front(-)/back(+) sweep."""
    J = V(J); Rx, Ry, Rz = R3
    bm = bmesh.new(); grid = []
    def pt(a_deg, b_deg, tb):
        a = math.radians(a_deg); br = math.radians(b_deg)
        k = 1.0 - hug * abs(2 * tb - 1) ** 3
        cb = keep + (1 - keep) * math.cos(br)
        d = V((s * math.cos(a) * cb * Rx, math.sin(br) * Ry, math.sin(a) * cb * Rz))
        return J + d * k
    for j in range(nb):
        tb = j / (nb - 1); b = b0 + (b1 - b0) * tb
        w = 0.55 + 0.45 * math.sin(math.pi * tb) ** 0.5
        am = (a0 + a1) / 2 + (-curl_back * b if b > 0 else -curl_front * b)
        ah = (a1 - a0) / 2 * w
        grid.append([bm.verts.new(pt(am - ah + 2 * ah * i / (na - 1), b, tb)) for i in range(na)])
    for j in range(nb - 1):
        for i in range(na - 1):
            bm.faces.new((grid[j][i], grid[j][i + 1], grid[j + 1][i + 1], grid[j + 1][i]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    f0 = bm.faces[len(bm.faces) // 2]
    if f0.normal.dot(f0.calc_center_median() - J) < 0:
        bmesh.ops.reverse_faces(bm, faces=bm.faces)
    mid = []
    for j in range(2, nb - 2):
        tb = j / (nb - 1); b = b0 + (b1 - b0) * tb
        am = (a0 + a1) / 2 + (-curl_back * b if b > 0 else -curl_front * b)
        p = pt(am, b, tb); mid.append(p)
    ob = mk(name, bm, mat, bone, sub=0)
    m = ob.modifiers.new('Solidify', 'SOLIDIFY'); m.thickness = thick; m.offset = -1.0; m.use_even_offset = False
    m = ob.modifiers.new('Subsurf', 'SUBSURF'); m.levels = sub; m.render_levels = sub
    return ob, mid

def engrave(name, tree, mapper, pts, bone, w=0.0011, n=None, depth=0.0003, mat='groove'):
    P, N = surf_path(tree, mapper, pts, -depth, n=n)
    if len(P) > 3:
        return sweep(name, P, w, 0.0009, mat, bone, normals=N, sub=0, nseg=6)
    return None
