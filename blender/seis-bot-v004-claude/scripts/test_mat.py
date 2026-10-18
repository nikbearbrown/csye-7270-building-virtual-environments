import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
import seis_lib as L, seis_stage as st
L.clear_scene(); L.set_collection("TEST")
sw = L.Sweep([(0,0,0.9),(0,-0.01,0.65),(0,-0.02,0.45)], [(0,0.075,0.07,3.0),(0.35,0.092,0.082,3.2),(1,0.05,0.045,2.6)])
core = sw.mesh("core", nring=48, round_end=(0.02,3)); L.finish(core, "dark", bevel=0)
for i,(a0,a1) in enumerate([(30,150),(160,260),(280,380)]):
    p = sw.panel(f"pl{i}", 0.04, 0.96, math.radians(a0), math.radians(a1), thickness=0.012, inflate=0.006, height=0.012, hp=1.4, ends=0.25)
    L.finish(p, "teal", bevel=0.003, bevel_segments=3, wear=1.0 if i else 0.0)
b = L.box("bandblock", (0.18,0.12,0.22), L.Frame((0.30,0,0.75))); L.finish(b, "bronze", bevel=0.004, bevel_segments=3)
g = L.box("goldblock", (0.06,0.06,0.22), L.Frame((0.12,0.0,0.75))); L.finish(g, "gold", bevel=0.002, bevel_segments=2)
r = L.plate("redplate", L.outline_teardrop(0.16,0.30), L.Frame.at((-0.30,-0.02,0.75),(0,-1,0),(1,0,0)), rise=0.03, thickness=0.012); L.finish(r, "red", bevel=0.002)
s = L.sphere("pewter", 0.09, L.Frame((0.30,0,0.45))); L.finish(s, "silver", bevel=0)
c = L.box("block", (0.30,0.30,0.20), L.Frame((-0.30,0,0.30))); L.finish(c, "stone", bevel=0.006)
e = L.sphere("eye", 0.02, L.Frame((0.30,-0.1,0.55)), scale=(1.4,0.6,1.2)); L.finish(e, "eye", bevel=0)
h = L.sphere("hand", 0.05, L.Frame((0.0,-0.1,0.25))); L.finish(h, "gunmetal", bevel=0)
st.studio(size=0.5)
objs=[o for o in bpy.data.objects if o.type=="MESH" and not o.name.startswith("backdrop")]
st.render_views(objs, sys.argv[-1], views=("three_q",), w=1000, h=1000, samples=96)
