"""shoulder_kit - small hardware helpers for the shoulder module (round 2): fasteners, washers, bearing stacks,
clevis plates, hoses and hose clamps.  Everything returns ONE Blender object with a material and a bone, ready to
append to the module's object list.  Sizes are metres; 3-6 mm fasteners; tidy, never noisy.
"""
import math
import bpy
import bmesh
from mathutils import Vector, Matrix

import seis_lib as L

PI = math.pi


def _frame(center, normal, xhint=(1, 0, 0)):
    return L.Frame.at(Vector(center), z=Vector(normal), x=xhint)


def _prim_bm():
    return bmesh.new()


def _add_cyl(bm, fr, z0, z1, r0, r1=None, seg=6, rot=0.0):
    """closed frustum in frame fr from local z0 to z1 (appended to bm)."""
    r1 = r0 if r1 is None else r1
    d = z1 - z0
    m = fr.matrix() @ Matrix.Translation((0, 0, z0 + d / 2)) @ Matrix.Rotation(rot, 4, "Z")
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=seg, radius1=r0, radius2=r1, depth=d, matrix=m)


def _add_dome(bm, fr, z0, r, h, seg=14, rings=5):
    """flat-topped dome (half ellipsoid) standing on local z0."""
    m = fr.matrix() @ Matrix.Translation((0, 0, z0))
    res = bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=rings * 2, radius=1.0)
    for v in res["verts"]:
        v.co = Vector((v.co.x * r, v.co.y * r, max(v.co.z, 0.0) * h))
    bmesh.ops.transform(bm, matrix=m, verts=res["verts"])
    bmesh.ops.remove_doubles(bm, verts=bm.verts[:], dist=1e-7)


def _finish_bm(name, bm):
    me = bpy.data.meshes.new(name)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    bm.to_mesh(me)
    bm.free()
    me.shade_smooth()
    return L._link(bpy.data.objects.new(name, me))


def hex_bolt(name, center, normal, r=0.0030, h=0.0028, mat="gunmetal", bone="chest", washer=True, xhint=(1, 0, 0),
             wear=None):
    """hex-head bolt (r = across-corner radius) on a thin washer."""
    fr = _frame(center, normal, xhint)
    bm = _prim_bm()
    if washer:
        _add_cyl(bm, fr, 0.0, h * 0.35, r * 1.75, seg=18)
        _add_cyl(bm, fr, h * 0.35, h * 0.35 + h, r, seg=6, rot=PI / 6)
    else:
        _add_cyl(bm, fr, 0.0, h, r, seg=6, rot=PI / 6)
    ob = _finish_bm(name, bm)
    L.finish(ob, mat, bevel=0.0004, bevel_segments=1, bone=bone, wear=wear)
    return ob


def round_head(name, center, normal, r=0.0028, mat="gunmetal", bone="chest", xhint=(1, 0, 0), wear=None):
    """domed round-head rivet / screw."""
    fr = _frame(center, normal, xhint)
    bm = _prim_bm()
    _add_cyl(bm, fr, 0.0, r * 0.25, r * 1.05, seg=16)
    _add_dome(bm, fr, r * 0.25, r, r * 0.62, seg=14, rings=3)
    ob = _finish_bm(name, bm)
    L.finish(ob, mat, bevel=0, bone=bone, wear=wear)
    return ob


def washer_stack(name, center, normal, rings, mat="gunmetal", bone="chest", seg=40, xhint=(1, 0, 0), wear=None,
                 bevel=0.0006):
    """stepped concentric discs: rings = [(radius, height), ...] from the base up, ONE object."""
    fr = _frame(center, normal, xhint)
    bm = _prim_bm()
    z = 0.0
    for (r, h) in rings:
        _add_cyl(bm, fr, z, z + h, r, seg=seg)
        z += h
    ob = _finish_bm(name, bm)
    L.finish(ob, mat, bevel=bevel, bevel_segments=2, bone=bone, wear=wear)
    return ob


def bearing_ring(name, center, normal, r_out, r_in, h, mat="gunmetal", bone="chest", seg=48, xhint=(1, 0, 0), notches=0,
                 wear=None):
    """a hollow bearing ring (washer with a bore), optional notched rim."""
    fr = _frame(center, normal, xhint)
    verts, faces = [], []
    n = seg
    for k in range(n):
        a = 2 * PI * k / n
        c, s = math.cos(a), math.sin(a)
        ro = r_out
        if notches and (k % max(1, n // notches)) == 0:
            ro = r_out * 0.94
        for (rr, zz) in ((ro, 0.0), (ro, h), (r_in, h), (r_in, 0.0)):
            verts.append(fr.p(rr * c, rr * s, zz))
    for k in range(n):
        k2 = (k + 1) % n
        for j in range(4):
            j2 = (j + 1) % 4
            faces.append((k * 4 + j, k2 * 4 + j, k2 * 4 + j2, k * 4 + j2))
    ob = L.new_mesh(name, verts, faces)
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    bm.to_mesh(ob.data)
    bm.free()
    L.finish(ob, mat, bevel=0.0005, bevel_segments=2, bone=bone, wear=wear)
    return ob


def pin(name, a, b, r=0.0045, mat="silver", bone="chest", cap=1.6, seg=16, wear=None):
    """a clevis pin from point a to b with a head disc at b and a thin cotter washer at a."""
    a, b = Vector(a), Vector(b)
    d = (b - a)
    fr = L.Frame.at(a, z=d, x=(1, 0, 0))
    bm = _prim_bm()
    _add_cyl(bm, fr, 0.0, d.length, r, seg=seg)
    _add_cyl(bm, fr, d.length - 0.0014, d.length + 0.0008, r * cap, seg=seg)
    _add_cyl(bm, fr, 0.0, 0.0009, r * 1.35, seg=seg)
    ob = _finish_bm(name, bm)
    L.finish(ob, mat, bevel=0.0004, bevel_segments=1, bone=bone, wear=wear)
    return ob


def clevis_plate(name, center, normal, length, width, thick, hole_r=0.0, mat="gunmetal", bone="chest", xhint=(0, 0, 1),
                 round_r=None, wear=None):
    """a flat bracket plate (rounded ends), thick extruded along `normal`, optional through hole is NOT cut (a pin is)."""
    fr = _frame(center, normal, xhint)
    rr = round_r if round_r is not None else width * 0.5
    ol = L.outline_rrect(width, length, rr, n=5)
    bm = _prim_bm()
    vs = [bm.verts.new((p[0], p[1], 0.0)) for p in ol]
    f = bm.faces.new(vs)
    res = bmesh.ops.extrude_face_region(bm, geom=[f])
    vv = [e for e in res["geom"] if isinstance(e, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, vec=(0, 0, thick), verts=vv)
    bmesh.ops.translate(bm, vec=(0, 0, -thick / 2), verts=bm.verts[:])
    bmesh.ops.transform(bm, matrix=fr.matrix(), verts=bm.verts[:])
    ob = _finish_bm(name, bm)
    L.finish(ob, mat, bevel=0.0007, bevel_segments=2, bone=bone, wear=wear)
    return ob


# ------------------------------------------------------------------------------------------------- hoses + clamps
_HOSE = None


def hose_material():
    """dark maroon rubber hose (own material, not a shared one)."""
    global _HOSE
    if _HOSE is not None and _HOSE.name in bpy.data.materials:
        return _HOSE
    m = bpy.data.materials.new("SEIS_shoulder_hose")
    m.use_nodes = True
    b = [n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED"][0]
    b.inputs["Base Color"].default_value = (0.040, 0.004, 0.006, 1.0)
    b.inputs["Roughness"].default_value = 0.42
    b.inputs["Metallic"].default_value = 0.0
    b.inputs["Coat Weight"].default_value = 0.25
    m.diffuse_color = (0.04, 0.004, 0.006, 1.0)
    _HOSE = m
    return m


def hose(name, pts, r=0.0045, bone="chest", n_per_seg=6, nring=10):
    ob = L.tube(name, pts, r, nring=nring, n_per_seg=n_per_seg, round_ends=True)
    L.finish(ob, hose_material(), bevel=0, bone=bone)
    return ob


def clamps_on(prefix, pts, r, ts, bone="chest", mat="gunmetal", w=0.0038, n_per_seg=6):
    """thin clamp rings around a hose at parameters ts (arc-length fractions); returns the list of objects."""
    path = L.Path(pts, n_per_seg=n_per_seg)
    out = []
    for i, t in enumerate(ts):
        p = path.at(t)
        tg = path.tangent(t)
        fr = L.Frame.at(p, z=tg, x=(1, 0, 0))
        bm = _prim_bm()
        _add_cyl(bm, fr, -w / 2, w / 2, r * 1.38, seg=20)
        ob = _finish_bm(f"{prefix}_{i + 1}", bm)
        L.finish(ob, mat, bevel=0.0005, bevel_segments=1, bone=bone)
        out.append(ob)
        # clamp screw tab
        nrm = fr.x
        bt = hex_bolt(f"{prefix}_{i + 1}_screw", p + nrm * (r * 1.38 + 0.0012), nrm, r=0.0017, h=0.0016, mat=mat, bone=bone,
                      washer=False)
        out.append(bt)
    return out


_OLIVE = None


def olive_material():
    """dull olive hub metal (#3A3A20), satin."""
    global _OLIVE
    if _OLIVE is not None and _OLIVE.name in bpy.data.materials:
        return _OLIVE
    m = bpy.data.materials.new("SEIS_shoulder_olive")
    m.use_nodes = True
    b = [n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED"][0]
    c = (0.050, 0.050, 0.014, 1.0)
    b.inputs["Base Color"].default_value = c
    b.inputs["Roughness"].default_value = 0.38
    b.inputs["Metallic"].default_value = 0.65
    m.diffuse_color = c
    _OLIVE = m
    return m
