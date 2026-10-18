"""hand_geo - bmesh helpers for the SEIS bot hand (own helper module; the shared seis_lib is not edited).

A `Part` accumulates several closed solids (lofts, cylinders, spheres, rings) in ONE local coordinate system, each face
carrying a material slot index, then `Part.make()` transforms them to the world frame, creates ONE object with the
material slots, bevels it with seis_lib.finish and moves its origin to the joint.

Local finger frame: +x = palm normal (towards the palm / thigh), +y = towards the little finger, +z = along the finger.
"""
import math
import bpy
import bmesh
from mathutils import Vector, Matrix

import seis_lib as L

SLOTS = ["teal", "dark", "bronze", "silver", "darkdisc"]
TEAL, DARK, BRONZE, SILVER, DISC = 0, 1, 2, 3, 4


def ring8(w, t, c, ox=0.0, oy=0.0):
    """Chamfered-rectangle section, 8 points, CCW in (x, y).  x = thickness axis, y = width axis.
    Edge ids: 0 = palm face (x=+t/2), 2 = +y side, 4 = dorsal face (x=-t/2), 6 = -y side."""
    hx, hy = t / 2, w / 2
    c = min(c, hx * 0.95, hy * 0.95)
    return [(hx + ox, -hy + c + oy), (hx + ox, hy - c + oy), (hx - c + ox, hy + oy), (-hx + c + ox, hy + oy),
            (-hx + ox, hy - c + oy), (-hx + ox, -hy + c + oy), (-hx + c + ox, -hy + oy), (hx - c + ox, -hy + oy)]


def ring_super(a, b, n=24, power=2.0, ox=0.0, oy=0.0):
    """Superellipse section (a along y, b along x), CCW in (x, y)."""
    pts = []
    e = 2.0 / power
    for i in range(n):
        th = 2 * math.pi * i / n
        c, s = math.cos(th), math.sin(th)
        pts.append((ox + b * math.copysign(abs(c) ** e, c), oy + a * math.copysign(abs(s) ** e, s)))
    return pts


class Part:
    def __init__(self):
        self.bm = bmesh.new()

    # -------------------------------------------------------------------------------------------------- solids
    def loft(self, stations, mat=TEAL, c=0.0025, tip=None, ring_fn=None, cap0=True, cap1=True):
        """stations: list of dicts or tuples (z, w, t[, ox]).  Returns (rings, faces_by_edge) where
        faces_by_edge[e][k] is the quad between station k and k+1 on section edge e (ring8 only)."""
        bm = self.bm
        rings = []
        for st in stations:
            if isinstance(st, dict):
                z, w, t = st["z"], st["w"], st["t"]
                ox, oy, cc = st.get("ox", 0.0), st.get("oy", 0.0), st.get("c", c)
            else:
                z, w, t = st[0], st[1], st[2]
                ox = st[3] if len(st) > 3 else 0.0
                oy, cc = 0.0, c
            pts = ring_fn(st) if ring_fn else ring8(w, t, cc, ox, oy)
            rings.append([bm.verts.new((p[0], p[1], z)) for p in pts])
        n = len(rings[0])
        fbe = {e: [] for e in range(n)}
        for k in range(len(rings) - 1):
            for e in range(n):
                f = bm.faces.new((rings[k][e], rings[k][(e + 1) % n], rings[k + 1][(e + 1) % n], rings[k + 1][e]))
                f.material_index = mat
                fbe[e].append(f)
        if cap0:
            f = bm.faces.new(rings[0][::-1])
            f.material_index = mat
        if cap1:
            if tip is None:
                f = bm.faces.new(rings[-1])
                f.material_index = mat
            else:
                ctr = Vector((0, 0, 0))
                for v in rings[-1]:
                    ctr += v.co
                ctr /= n
                ap = bm.verts.new(ctr + Vector(tip))
                for e in range(n):
                    f = bm.faces.new((rings[-1][e], rings[-1][(e + 1) % n], ap))
                    f.material_index = mat
        return rings, fbe

    def recess(self, faces, depth, inset, mat=DISC, floor_mat=None):
        """Inset the connected quad region `faces` by `inset` and push it in by `depth` (a real recess)."""
        bm = self.bm
        r = bmesh.ops.inset_region(bm, faces=list(faces), thickness=inset, depth=-depth, use_even_offset=True,
                                   use_boundary=True)
        for f in faces:
            f.material_index = mat if floor_mat is None else floor_mat
        return r

    def box(self, center, size, mat=TEAL, rot=None):
        """Axis-aligned (in local coords) box, optional rotation Matrix 3x3."""
        res = bmesh.ops.create_cube(self.bm, size=1.0)
        vs = res["verts"]
        M = Matrix.Diagonal(Vector((size[0], size[1], size[2], 1.0)))
        if rot is not None:
            M = rot.to_4x4() @ M
        M = Matrix.Translation(center) @ M
        bmesh.ops.transform(self.bm, matrix=M, verts=vs)
        for f in {f for v in vs for f in v.link_faces}:
            f.material_index = mat
        return vs

    def cyl(self, center, axis, radius, length, mat=DARK, segments=24, radius2=None, xhint=None):
        """Cylinder / frustum from the centre along `axis`."""
        res = bmesh.ops.create_cone(self.bm, cap_ends=True, cap_tris=False, segments=segments, radius1=radius,
                                    radius2=radius if radius2 is None else radius2, depth=length)
        vs = res["verts"]
        fr = L.Frame.at(Vector((0, 0, 0)), axis, xhint or (1, 0, 0))
        M = Matrix.Translation(center) @ fr.matrix()
        bmesh.ops.transform(self.bm, matrix=M, verts=vs)
        for f in {f for v in vs for f in v.link_faces}:
            f.material_index = mat
        return vs

    def sphere(self, center, radii, mat=TEAL, segments=24, rings=14, rot=None):
        res = bmesh.ops.create_uvsphere(self.bm, u_segments=segments, v_segments=rings, radius=1.0)
        vs = res["verts"]
        M = Matrix.Diagonal(Vector((radii[0], radii[1], radii[2], 1.0)))
        if rot is not None:
            M = rot.to_4x4() @ M
        M = Matrix.Translation(center) @ M
        bmesh.ops.transform(self.bm, matrix=M, verts=vs)
        for f in {f for v in vs for f in v.link_faces}:
            f.material_index = mat
        return vs

    def torus(self, center, axis, R, r, mat=BRONZE, major=32, minor=8, xhint=None, squash=1.0):
        fr = L.Frame.at(Vector((0, 0, 0)), axis, xhint or (1, 0, 0))
        verts = []
        for i in range(major):
            a = 2 * math.pi * i / major
            row = []
            for j in range(minor):
                b = 2 * math.pi * j / minor
                rr = R + r * math.cos(b)
                p = Vector((rr * math.cos(a), rr * math.sin(a), r * squash * math.sin(b)))
                row.append(self.bm.verts.new(Vector(center) + fr.p(p.x, p.y, p.z)))
            verts.append(row)
        for i in range(major):
            for j in range(minor):
                i2, j2 = (i + 1) % major, (j + 1) % minor
                f = self.bm.faces.new((verts[i][j], verts[i2][j], verts[i2][j2], verts[i][j2]))
                f.material_index = mat

    def hex_bolt(self, center, normal, radius, height, mat=BRONZE, xhint=(1, 0, 0), segments=6):
        c = Vector(center) + Vector(normal).normalized() * height / 2
        return self.cyl(c, normal, radius, height, mat=mat, segments=segments, xhint=xhint)

    def tube(self, pts, radius, mat=DARK, nring=10):
        """Round cable through points (catmull path), own end caps."""
        path = L.Path(pts, n_per_seg=8)
        n = max(6, int(path.length / 0.004))
        rings = []
        prev_x = None
        for i in range(n + 1):
            t = i / n
            P = path.at(t)
            T = path.tangent(t)
            hint = prev_x if prev_x is not None else Vector((0, 1, 0))
            X = (hint - T * hint.dot(T))
            if X.length < 1e-6:
                X = Vector((1, 0, 0)) - T * T.x
            X.normalize()
            prev_x = X
            Y = T.cross(X)
            rr = radius(t) if callable(radius) else radius
            rings.append([self.bm.verts.new(P + X * rr * math.cos(2 * math.pi * k / nring) + Y * rr * math.sin(2 * math.pi * k / nring)) for k in range(nring)])
        for i in range(n):
            for k in range(nring):
                f = self.bm.faces.new((rings[i][k], rings[i][(k + 1) % nring], rings[i + 1][(k + 1) % nring], rings[i + 1][k]))
                f.material_index = mat
        for rg, flip in ((rings[0], True), (rings[-1], False)):
            f = self.bm.faces.new(rg[::-1] if flip else rg)
            f.material_index = mat

    # -------------------------------------------------------------------------------------------------- hardware (round 2)
    def washer_bolt(self, base, normal, r_wash=0.0033, h_wash=0.0005, r_mid=0.0025, h_mid=0.0005, r_hex=0.0017, h_hex=0.0012,
                    mat_w=TEAL, mat_m=DARK, mat_h=SILVER, xhint=(0, 0, 1), hexagon=True):
        """Stepped bearing washer: wide thin washer, darker step ring, hex (or round) bolt head.  `base` = point on the surface,
        `normal` = outward direction (pointing away from the part)."""
        n = Vector(normal).normalized()
        b = Vector(base)
        self.cyl(b + n * (h_wash / 2 - 0.0002), n, r_wash, h_wash + 0.0002, mat_w, segments=20, xhint=xhint)
        self.cyl(b + n * (h_wash + h_mid / 2 - 0.0002), n, r_mid, h_mid, mat_m, segments=16, xhint=xhint)
        self.cyl(b + n * (h_wash + h_mid + h_hex / 2 - 0.0003), n, r_hex, h_hex, mat_h, segments=6 if hexagon else 14, xhint=xhint)

    def oval_pad(self, zm, hl, wmax, t, ox, mat, n=15, power=2.6, ring_power=2.6):
        """elongated oval pad (stations along z) centred at x=ox; thickness t."""
        sts = []
        for k in range(n):
            u = -1 + 2 * k / (n - 1)
            wv = max(0.0030, wmax * max(0.0, 1 - abs(u) ** power) ** (1 / power))
            sts.append(dict(z=zm + u * hl, w=wv, t=t, ox=ox))
        self.loft(sts, mat, ring_fn=lambda s: ring_super(s["w"] / 2, s["t"] / 2, 22, ring_power, ox=s["ox"]))

    # -------------------------------------------------------------------------------------------------- output
    def make(self, name, frame, origin_world, bone, wear=0.5, bevel=0.0010, segs=2, mats=None, angle=38.0):
        """frame = world Frame of the local coordinate system; origin_world = where the object origin goes."""
        bm = self.bm
        bmesh.ops.transform(bm, matrix=frame.matrix(), verts=bm.verts[:])
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
        me = bpy.data.meshes.new(name)
        bm.to_mesh(me)
        bm.free()
        ob = bpy.data.objects.new(name, me)
        L._link(ob)
        for s in (mats or SLOTS):
            me.materials.append(L.mat(s))
        L.finish(ob, None, bevel=bevel, bevel_segments=segs, angle=angle, wear=wear, bone=bone)
        L.set_origin(ob, origin_world)
        return ob
