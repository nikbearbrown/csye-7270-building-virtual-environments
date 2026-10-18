"""arm_stats - print per-object triangle counts of the LEFT arm (own helper).  Blender -b --factory-startup --python parts/arm_stats.py"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); W = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(W, "src")); sys.path.insert(0, HERE)
os.environ["ARM_SIDE"] = "L"
import seis_lib as L
L.clear_scene()
import arm
objs = arm.build()
rows = []
for o in objs:
    o.data.calc_loop_triangles()
    rows.append((len(o.data.loop_triangles), o.name))
rows.sort(reverse=True)
tot = sum(r[0] for r in rows)
print("STATS objects", len(rows), "tris", tot)
for t, n in rows[:40]:
    print("STATS", t, n)
small = sum(t for t, n in rows if t < 400)
print("STATS small(<400) total", small, "count", sum(1 for t, n in rows if t < 400))
