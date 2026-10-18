"""seis_cleanup - conservative mesh hygiene run by assemble.py on every built object (only touches objects that need it):
   1. delete vertices whose coordinates are NaN/inf (their faces go with them)
   2. dissolve degenerate edges/faces (zero length / zero area, tolerance 1e-6 m; faces below 1e-11 m2 = 10 mm2*1e-6)
   3. delete loose vertices (not part of any edge)
Returns a report {object name: what was removed}.  Geometry that is already clean is left byte-for-byte alone."""
import math
import bmesh


def _needs_work(bm):
    for v in bm.verts:
        c = v.co
        if math.isnan(c.x) or math.isnan(c.y) or math.isnan(c.z) or math.isinf(c.x) or math.isinf(c.y) or math.isinf(c.z):
            return True
        if not v.link_edges:
            return True
    for f in bm.faces:
        if f.calc_area() < 1e-11:
            return True
    return False


def cleanup(objs):
    rep = {}
    for ob in objs:
        if ob.type != "MESH":
            continue
        bm = bmesh.new()
        bm.from_mesh(ob.data)
        if not _needs_work(bm):
            bm.free()
            continue
        info = {"nan_verts": 0, "degenerate_faces": 0, "loose_verts": 0}
        bad = [v for v in bm.verts if any(math.isnan(x) or math.isinf(x) for x in v.co)]
        if bad:
            info["nan_verts"] = len(bad)
            bmesh.ops.delete(bm, geom=bad, context="VERTS")
        n0 = len(bm.faces)
        bmesh.ops.dissolve_degenerate(bm, dist=1e-6, edges=bm.edges[:])
        zero = [f for f in bm.faces if f.calc_area() < 1e-11]
        if zero:
            bmesh.ops.delete(bm, geom=zero, context="FACES")
        info["degenerate_faces"] = max(0, n0 - len(bm.faces))
        loose = [v for v in bm.verts if not v.link_edges]
        if loose:
            info["loose_verts"] = len(loose)
            bmesh.ops.delete(bm, geom=loose, context="VERTS")
        bm.to_mesh(ob.data)
        ob.data.update()
        bm.free()
        rep[ob.name] = info
    return rep
