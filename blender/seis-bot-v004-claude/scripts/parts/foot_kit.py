"""foot_kit - helpers private to the foot module (the shared seis_lib is not edited)."""
import math
import bpy
import bmesh
from mathutils import Vector, Matrix
import seis_lib as L
import seis_spec as S

H = S.H
A = S.J("ankle.L")          # left ankle joint (world)
AX = A.x


def h(x):
    return x * H


def P(lx, f, z):
    """world point from: lx = metres outboard (+X) of the ankle axis, f = metres FORWARD (toward -Y) of the ankle, z = height"""
    return Vector((AX + lx, -f, z))


def interp(pts, x, smooth=True):
    """piecewise interpolation through (x, y) pairs (smoothstep between pairs)."""
    if x <= pts[0][0]:
        return pts[0][1]
    if x >= pts[-1][0]:
        return pts[-1][1]
    for i in range(len(pts) - 1):
        x0, y0 = pts[i]
        x1, y1 = pts[i + 1]
        if x0 <= x <= x1:
            t = (x - x0) / (x1 - x0)
            if smooth:
                t = t * t * (3 - 2 * t)
            return y0 + (y1 - y0) * t
    return pts[-1][1]


class Reg:
    """collects the objects of one side so they can be mirrored together"""

    def __init__(self):
        self.items = []

    def add(self, ob, name, mat, bone, bevel=0.002, seg=2, wear=None, angle=38.0, weighted=True):
        ob.name = f"foot_{name}.L"
        ob.data.name = ob.name
        L.finish(ob, mat, bevel=bevel, bevel_segments=seg, wear=wear, bone=bone, angle=angle, weighted=weighted)
        ob.name = f"foot_{name}.L"
        self.items.append(ob)
        return ob

    def mirror_all(self):
        out = list(self.items)
        for ob in self.items:
            m = L.mirror_x(ob)
            out.append(m)
        return out


def join_named(objs, name):
    objs = [o for o in objs if o is not None]
    if not objs:
        return None
    r = L.join(objs, name)
    r.data.name = name
    return r


def xf_mesh(ob, m4):
    ob.data.transform(m4)
    ob.data.update()
    return ob


def rotate_about(ob, pivot, axis, ang):
    """rigid rotate the mesh of ob (already in world coords) about a world pivot"""
    M = Matrix.Translation(pivot) @ Matrix.Rotation(ang, 4, axis) @ Matrix.Translation(-Vector(pivot))
    return xf_mesh(ob, M)


def weld(ob, dist=1e-5):
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    bmesh.ops.remove_doubles(bm, verts=bm.verts[:], dist=dist)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    bm.to_mesh(ob.data)
    bm.free()
    ob.data.update()
    return ob


def rbox(name, c, size, frame=None):
    """box centred c (world) with size (x,y,z) in world axes or a frame"""
    fr = frame or L.Frame(origin=c)
    return L.box(name, size, fr)


def domed_box(name, center, size, rise=0.0, cuts=3, pitch=0.0, taper=0.0, nose=0.0):
    """box with a domed top.  center world (x,y,z); size (sx, sy, sz) world axes; rise = dome height at the middle of the
    top face; taper = fraction the top face is narrower than the bottom in x (a sloped wall)."""
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.subdivide_edges(bm, edges=bm.edges[:], cuts=cuts, use_grid_fill=True)
    sx, sy, sz = size
    for v in bm.verts:
        x, y, z = v.co.x * sx, v.co.y * sy, v.co.z * sz
        if v.co.z > 0.01:
            k = (1 - (2 * v.co.x) ** 2) * (1 - (2 * v.co.y) ** 2)
            z += rise * max(0.0, k) ** 0.7
        if nose and v.co.z > 0.01:
            q = max(0.0, -2 * v.co.y)          # +1 at the FRONT (-y) edge
            z -= nose * q ** 2.2
        if taper:
            f = (v.co.z + 0.5)
            x *= 1 - taper * f
        v.co = Vector((x, y, z))
    bmesh.ops.transform(bm, matrix=Matrix.Translation(Vector(center)), verts=bm.verts[:])
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    me.shade_smooth()
    return L._link(bpy.data.objects.new(name, me))


def split_at_plane(ob, plane_co, plane_no, names):
    """Cut a closed mesh with a plane and return (outer_obj, inner_obj): the two halves, each capped with a flat
    n-gon.  outer = the side the normal points to.  The source object is deleted.  Used to split the swept boot
    upper into foot and toe-cap pieces that fit each other exactly."""
    out = []
    for keep_outer, nm in zip((True, False), names):
        bm = bmesh.new()
        bm.from_mesh(ob.data)
        geom = bm.verts[:] + bm.edges[:] + bm.faces[:]
        bmesh.ops.bisect_plane(bm, geom=geom, dist=1e-7, plane_co=plane_co, plane_no=plane_no,
                               clear_inner=keep_outer, clear_outer=not keep_outer)
        bnd = [e for e in bm.edges if e.is_boundary]
        if bnd:
            bmesh.ops.holes_fill(bm, edges=bnd, sides=len(bnd) + 2)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
        me = bpy.data.meshes.new(nm)
        bm.to_mesh(me)
        bm.free()
        me.shade_smooth()
        out.append(L._link(bpy.data.objects.new(nm, me)))
    bpy.data.objects.remove(ob, do_unlink=True)
    return out[0], out[1]


def sweep_mesh_centered(sw, name, nring=40, nstations=None, round_start=None, round_end=None):
    """Same as Sweep.mesh(caps=True) but the dome poles sit on the SECTION CENTRE (ox, oy) rather than on the path.
    The stock mesh() puts the pole on the path, which is the sole line when the section is offset upward (oy), and that
    drags a triangular dent into the nose of the boot."""
    import math as _m
    PI = _m.pi
    ks_t = [k["t"] for k in sw.keys]
    nst = nstations or max(16, int(sw.path.length / 0.02))
    ts = sorted(set([i / nst for i in range(nst + 1)] + ks_t))
    rings = []
    P0 = P1 = None
    if round_start:
        depth, steps = round_start
        Pt, T, X, Y = sw.frame(0.0)
        s0 = sw.sec(0.0)
        for j in range(steps, 0, -1):
            ph = (j / (steps + 1)) * (PI / 2)
            rings.append(sw._ring(0.0, nring, scale=_m.cos(ph), shift=-T * depth * _m.sin(ph), sec=s0))
        P0 = Pt + X * s0["ox"] + Y * s0["oy"] - T * depth
    for t in ts:
        rings.append(sw._ring(t, nring))
    if round_end:
        depth, steps = round_end
        Pt, T, X, Y = sw.frame(1.0)
        s1 = sw.sec(1.0)
        for j in range(1, steps + 1):
            ph = (j / (steps + 1)) * (PI / 2)
            rings.append(sw._ring(1.0, nring, scale=_m.cos(ph), shift=T * depth * _m.sin(ph), sec=s1))
        P1 = Pt + X * s1["ox"] + Y * s1["oy"] + T * depth
    return L._mesh_from_rings(name, rings, nring, closed_rings=True, caps=True, flip=not sw.handed, pole_start=P0, pole_end=P1)
