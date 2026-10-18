"""arm_detail - tidy small-part primitives for parts/arm.py (round-2 detail pass).  Own helper; no shared file edited.

Every function returns ONE finished Blender object (closed mesh, material, bone), already linked into the active
collection.  Parts are built straight in bmesh (no modifiers, no booleans) so a hundred of them cost almost nothing.

  hex_bolt     washer + hex head with a chamfered top          round_rivet   low dome head
  stepped      stack of stepped discs (bearing / washer)       band          hollow ring band (clamp, collar, bearing race)
  clamp        band around a hose with a lug and a hex bolt    hose          round tube through points, rounded ends
"""
import math
import bpy
import bmesh
from mathutils import Vector
import seis_lib as L

PI = math.pi


def _link(ob):
    (L._COLL or bpy.context.scene.collection).objects.link(ob)
    return ob


def _add_revolve(bm, fr, profile, segs, closed=False, rot=0.0):
    """Solid of revolution about fr.z added to bm.  profile = [(r, z), ...] from the axis out and back to the axis
    (closed=False) or a closed loop of points (closed=True, a hollow ring)."""
    cols = []
    for (r, z) in profile:
        if r <= 1e-9:
            v = bm.verts.new(fr.p(0.0, 0.0, z))
            cols.append([v] * segs)
        else:
            cols.append([bm.verts.new(fr.p(r * math.cos(rot + 2 * PI * k / segs), r * math.sin(rot + 2 * PI * k / segs), z))
                         for k in range(segs)])
    n = len(profile)
    for j in range(n if closed else n - 1):
        j2 = (j + 1) % n
        for k in range(segs):
            k2 = (k + 1) % segs
            vs = [cols[j][k], cols[j][k2], cols[j2][k2], cols[j2][k]]
            uniq = []
            for v in vs:
                if v not in uniq:
                    uniq.append(v)
            if len(uniq) >= 3:
                try:
                    bm.faces.new(uniq)
                except ValueError:
                    pass


def _finish(name, bm, mat, bone, wear=None, angle=38.0):
    bmesh.ops.remove_doubles(bm, verts=bm.verts[:], dist=1e-7)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    lim = math.radians(angle)
    for e in bm.edges:
        e.smooth = (len(e.link_faces) != 2) or e.calc_face_angle(0.0) < lim
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    me.shade_smooth()
    ob = bpy.data.objects.new(name, me)
    _link(ob)
    L.set_material(ob, mat)
    ob["bone"] = bone
    if wear is not None:
        ob["wear"] = float(wear) if wear > 0 else 1e-6
    return ob


def hex_bolt(name, fr, r, mat, bone, h=None, washer=True, sink=0.0006):
    """Hex head bolt (across-corners radius r) standing on a washer, base at the frame origin (sunk `sink` into it)."""
    h = h or 2.1 * r
    fr = L.Frame(fr.p(0, 0, -sink), fr.x, fr.y, fr.z)
    bm = bmesh.new()
    zw = 0.0
    if washer:
        zw = 0.28 * h
        _add_revolve(bm, fr, [(0, 0), (1.55 * r, 0), (1.55 * r, 0.7 * zw), (1.40 * r, zw), (0, zw)], 14)
    _add_revolve(bm, fr, [(0, zw), (r, zw), (r, 0.78 * h + 0.22 * zw), (0.80 * r, h), (0, h)], 6)
    return _finish(name, bm, mat, bone, wear=0)


def round_rivet(name, fr, r, mat, bone, sink=0.0004, flat=0.58):
    fr = L.Frame(fr.p(0, 0, -sink), fr.x, fr.y, fr.z)
    prof = [(0, 0), (r, 0)]
    for a in (14, 32, 52, 72):
        a_ = math.radians(a)
        prof.append((r * math.cos(a_), flat * r * math.sin(a_) + 0.14 * r))
    prof.append((0, flat * r + 0.14 * r))
    bm = bmesh.new()
    _add_revolve(bm, fr, prof, 10)
    return _finish(name, bm, mat, bone, wear=0)


def stepped(name, fr, rings, mat, bone, segs=28, wear=0, hollow=0.0):
    """Stepped discs standing on the frame origin, rings = [(radius, height), ...] from the base outward-to-inward
    (each ring sits on top of the previous one).  hollow > 0 makes it a bearing race with that inner radius."""
    z = 0.0
    prof = []
    if hollow > 0:
        prof.append((hollow, 0.0))
    else:
        prof.append((0, 0.0))
    first = True
    for (r, h) in rings:
        prof.append((r, z))
        z += h
        prof.append((r, z))
    if hollow > 0:
        prof.append((hollow, z))
        bm = bmesh.new()
        _add_revolve(bm, fr, prof, segs, closed=True)
    else:
        prof.append((0, z))
        bm = bmesh.new()
        _add_revolve(bm, fr, prof, segs)
    return _finish(name, bm, mat, bone, wear=wear)


def band(name, fr, rin, rout, hw, mat, bone, segs=36, wear=0, step=None):
    """Hollow ring band about fr.z, half width hw.  step=(rout2, hw2) adds a stepped second tier (a bearing race)."""
    prof = [(rin, -hw), (rout, -hw), (rout, hw)]
    if step:
        r2, h2 = step
        prof += [(r2, hw), (r2, hw + h2), (rin, hw + h2)]
    else:
        prof += [(rin, hw)]
    bm = bmesh.new()
    _add_revolve(bm, fr, prof, segs, closed=True)
    return _finish(name, bm, mat, bone, wear=wear)


def hose(name, pts, r, mat, bone, nring=8):
    ob = L.tube(name, pts, r, nring=nring, caps=True, round_ends=True)
    L.finish(ob, mat, bevel=0, bone=bone, weighted=False)
    ob["wear"] = 1e-6
    return ob


def clamp(name, p, tangent, nrm, r_hose, mat, bone, bolt_mat=None):
    """A P-clamp: a band round a hose at point p (hose axis `tangent`), plus a lug and a tiny hex bolt on the `nrm` side."""
    fr = L.Frame.at(p, tangent, nrm)           # z along the hose, x towards nrm
    bm = bmesh.new()
    _add_revolve(bm, fr, [(r_hose + 0.0002, -0.0022), (r_hose + 0.0017, -0.0022), (r_hose + 0.0017, 0.0022),
                          (r_hose + 0.0002, 0.0022)], 14, closed=True)
    # lug block on the nrm side (x axis of the frame) with a hex bolt head on top
    ctr = r_hose + 0.0017 + 0.0012
    hw_, hl_, hh_ = 0.0028, 0.0022, 0.0013
    corners = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            for sz in (-1, 1):
                corners.append(bm.verts.new(fr.p(ctr + sx * hh_, sy * hw_, sz * hl_)))
    idx = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]
    for q in idx:
        bm.faces.new([corners[i] for i in q])
    # hex head on the lug (axis = frame x)
    hfr = L.Frame(fr.p(ctr + hh_ - 0.0003, 0, 0), fr.y, fr.z, fr.x)
    _add_revolve(bm, hfr, [(0, 0), (0.0021, 0), (0.0021, 0.0013), (0.0016, 0.0018), (0, 0.0018)], 6)
    return _finish(name, bm, mat, bone, wear=0)
