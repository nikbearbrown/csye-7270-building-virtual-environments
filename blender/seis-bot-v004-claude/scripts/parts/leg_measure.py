"""leg_measure - prints left-leg x/y extents per height band. blender -b --factory-startup --python parts/leg_measure.py"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); W = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(W, "src")); sys.path.insert(0, HERE)
import bpy, seis_lib as L
L.clear_scene(); L.set_collection(L.collection("PART_leg"))
import leg
res = [o for o in leg.build() if o.name.endswith(".L") and o.type == "MESH"]
import mathutils
pts = []
for o in res:
    mw = o.matrix_world
    for v in o.data.vertices:
        p = mw @ v.co; pts.append((p.x, p.y, p.z, o.name))
H = 0.2554
for z in [1.18, 1.10, 1.0, 0.9, 0.8, 0.7, 0.6, 0.55, 0.5, 0.45, 0.4, 0.35, 0.3, 0.25, 0.2, 0.15, 0.1]:
    b = [p for p in pts if abs(p[2] - z) < 0.01 and "plug" not in p[3]]
    if b:
        print("z=%.2f m (%.2f H): x %.3f..%.3f w=%.3f | y %.3f..%.3f d=%.3f" % (z, z / H, min(p[0] for p in b), max(p[0] for p in b), max(p[0] for p in b) - min(p[0] for p in b), min(p[1] for p in b), max(p[1] for p in b), max(p[1] for p in b) - min(p[1] for p in b)))
