"""head_facets - round 3: the muzzle and cheek planes as HARD, PLANAR facets (f07/f08: crisp angular silver planes cut by thin
black lines, a narrow pointed muzzle 0.084 m wide at its lower edge, a V-crest nose bridge, chevron cheek planes).

Each facet is a flat polygon (landmarks read from the on-model f08 crop, mapped through head_face.f8) whose vertices are put on a
least-squares plane over the egg face (FACE chart) plus a relief that raises the centre-line crest (pointed chin / nose ridge).
A hairline gap is left between neighbours (shrink) and the dark core / base shows through it as the black cut line.
Everything is built for the robot's left (+x) and mirrored; the centre-line vertices coincide so the crest closes."""
import math
import bmesh
import bpy
from mathutils import Vector
import numpy as np
import seis_lib as L
from head_lib import FACE, shrink, both, loop_tube, on_surface, ccw
import head_face as F

f8 = F.f8
SHIFT_K = 0.35      # how much of the plane-vs-egg overshoot is moved forward (1.0 = every corner clears the egg, but the face becomes a visor)

# centre-line crest relief (metres above the egg face) by f08 pixel row y: nose bridge -> muzzle -> pointed chin
CREST = [(400, 0.0010), (540, 0.0020), (650, 0.0030), (790, 0.0040), (880, 0.0045), (925, 0.0040)]


def crest(y_px):
    if y_px <= CREST[0][0]:
        return CREST[0][1]
    for (y0, h0), (y1, h1) in zip(CREST, CREST[1:]):
        if y_px <= y1:
            t = (y_px - y0) / (y1 - y0)
            return h0 + (h1 - h0) * t
    return CREST[-1][1]


def facet(name, px_poly, base=0.0030, crest_k=1.0, width_px=60.0, thickness=0.006, gap=0.0007, mat="pewter",
          bevel=0.0011):
    """px_poly: f08 crop pixel polygon (right half); returns the object (left side)."""
    poly = [f8(X, Y) for X, Y in px_poly]
    poly = shrink(poly, gap)
    pts3 = []
    for (x, z) in poly:
        P, N = FACE.map(x, z)
        ypx = F.YC8 + (F.S.hh(8.3) - z) / F.S8
        w = max(width_px * F.S8, 1e-4)
        rel = base + crest_k * crest(ypx) * max(0.0, 1.0 - abs(x) / w)
        pts3.append(P + N * rel)
    # least-squares plane y = a + b x + c z through the facet corners
    A = np.array([[1.0, p.x, p.z] for p in pts3])
    yv = np.array([p.y for p in pts3])
    coef, *_ = np.linalg.lstsq(A, yv, rcond=None)
    top = [Vector((p.x, float(coef[0] + coef[1] * p.x + coef[2] * p.z), p.z)) for p in pts3]
    # a flat facet must not sink into the egg: move the plane forward (-y) until every corner is at least as proud as wanted
    shift = -SHIFT_K * max(0.0, max(top[i].y - pts3[i].y for i in range(len(top))))
    top = [Vector((p.x, p.y + shift, p.z)) for p in top]
    bm = bmesh.new()
    tv = [bm.verts.new(p) for p in top]
    bv = [bm.verts.new(p + Vector((0.0, thickness, 0.0))) for p in top]   # pushed back (+y) into the head
    bm.faces.new(tv)
    bm.faces.new(list(reversed(bv)))
    n = len(tv)
    for i in range(n):
        j = (i + 1) % n
        bm.faces.new((tv[i], bv[i], bv[j], tv[j]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    L._link(ob)
    L.finish(ob, mat, bevel=bevel, bevel_segments=2, bone="head", wear=0.0, weighted=False)
    return ob


def build(out):
    # nose bridge (V crest), upper muzzle, mid muzzle, lower muzzle with the pointed chin
    facets = [
        ("head_facet_bridge", [(390, 400), (446, 400), (452, 545), (390, 545)], 0.0016, 1.0, 62.0, 0.0007),
        ("head_facet_muzzle_up_c", [(390, 545), (430, 545), (436, 660), (440, 800), (390, 800)], 0.0016, 1.0, 160.0, 0.0002),
        ("head_facet_muzzle_up_w", [(430, 545), (452, 545), (466, 660), (480, 692), (550, 818), (440, 800), (436, 660)], 0.0016, 1.0, 160.0, 0.0002),
        ("head_facet_chin_c", [(390, 800), (440, 800), (446, 915), (390, 925)], 0.0016, 1.0, 160.0, 0.0002),
        ("head_facet_chin_w", [(440, 800), (550, 818), (540, 880), (518, 908), (446, 915)], 0.0016, 1.0, 160.0, 0.0002),
        # cheek planes: under the eye, running down to the muzzle corner in a chevron; the outer plane meets the pod arc
        ("head_facet_cheek_in", [(484, 694), (472, 668), (545, 684), (612, 672), (606, 722), (558, 792), (550, 818)], 0.0022, 0.0, 60.0, 0.0008),
        ("head_facet_cheek_out", [(612, 672), (656, 640), (664, 700), (632, 762), (586, 812), (558, 792), (606, 722)], 0.0020, 0.0, 60.0, 0.0008),
    ]
    for nm, poly, base, ck, wpx, gp in facets:
        ob = facet(nm + ".L", poly, base=base, crest_k=ck, width_px=wpx, gap=gp)
        both(ob, out)
    return out
