import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); W = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(W, "src")); sys.path.insert(0, HERE)
import bpy
import seis_lib as L
L.clear_scene()
import shoulder as M
res = M.build()
for ob in res:
    if not ob.name.endswith(".L") and ob.name.endswith(".R"): continue
    lo, hi = L.bbox_world([ob])
    if ob.name.endswith('.L') and lo.z < 1.535 and hi.x > 0.28:
        print("PROBE", ob.name, [round(v,3) for v in lo], [round(v,3) for v in hi], ob.data.materials[0].name)
