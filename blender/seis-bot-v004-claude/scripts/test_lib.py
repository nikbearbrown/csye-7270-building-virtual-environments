import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
import seis_lib as L, seis_stage as st
L.clear_scene()
L.set_collection("TEST")
# forearm-ish sweep along -Z (hanging), front = -Y
path = [(0.0, 0.0, 1.0), (0.01, -0.01, 0.8), (0.02, -0.02, 0.6), (0.03, -0.04, 0.42)]
keys = [(0.0, 0.07, 0.065, 2.8), (0.25, 0.085, 0.075, 3.0), (0.7, 0.06, 0.055, 3.0), (1.0, 0.04, 0.04, 2.5)]
sw = L.Sweep(path, keys)
core = sw.mesh("fore_core", nring=40, round_end=(0.02, 3))
L.finish(core, "dark", bevel=0.0)
import math
p1 = sw.panel("fore_pl_front", 0.05, 0.95, math.radians(50), math.radians(130), thickness=0.008, inflate=0.006, height=0.012, hp=1.5, ends=0.2)
L.finish(p1, "teal", bevel=0.0012)
p2 = sw.panel("fore_pl_out", 0.15, 0.9, math.radians(-40), math.radians(40), thickness=0.008, inflate=0.006, height=0.01, hp=1.5, ends=0.2)
L.finish(p2, "bronze", bevel=0.0012)
# dome plate (red)
fr = L.Frame.at((0.12, -0.06, 1.1), (0, -1, 0), (1, 0, 0))
pl = L.plate("red_plate", L.outline_teardrop(0.10, 0.20), fr, rise=0.02, thickness=0.01)
L.finish(pl, "red", bevel=0.0015)
d = L.disc_stack("disc", (-0.12, -0.05, 1.1), (-1, -0.2, 0), [(0.05, 0.006), (0.04, 0.012), (0.026, 0.008), (0.012, 0.016)])
L.finish(d, "dark", bevel=0.001)
st.studio(size=0.6)
objs = [o for o in bpy.data.objects if o.type == "MESH" and o.name not in ("backdrop", "backdrop_wall")]
outs = st.render_views(objs, sys.argv[-1], views=("front","three_q"), w=700, h=900, samples=24)
outs += st.render_views(objs, sys.argv[-1], views=("three_q",), w=700, h=900, samples=24, prefix="clay_", clay=True)
print("OUT", outs)
