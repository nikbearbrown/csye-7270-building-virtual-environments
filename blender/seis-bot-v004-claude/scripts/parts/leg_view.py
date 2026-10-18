"""leg_view - close-up renders of the leg (my own driver; run_part only frames the whole part).

/Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup --python parts/leg_view.py -- NAME zlo zhi view[,view] [w h samples] [clay] [left|both]
zlo/zhi in head-heights above the floor.  Output parts/_out/leg/NAME_<view>.png
"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
W = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(W, "src"))
sys.path.insert(0, HERE)
import bpy
import seis_lib as L
import seis_stage as st
import seis_spec as S
from mathutils import Vector

a = sys.argv[sys.argv.index("--") + 1:]
name, zlo, zhi, views = a[0], float(a[1]), float(a[2]), a[3].split(",")
w = int(a[4]) if len(a) > 4 else 800
hh = int(a[5]) if len(a) > 5 else 800
samples = int(a[6]) if len(a) > 6 else 32
clay = "clay" in a
side = "both" if "both" in a else "left"
L.clear_scene()
st.studio(size=1.0)
coll = L.collection("PART_leg")
L.set_collection(coll)
import leg
res = leg.build()
objs = [o for o in res if o.type == "MESH"]
if side == "left":
    objs = [o for o in objs if o.name.endswith(".L")]
sel = []
for o in objs:
    lo, hi = L.bbox_world([o])
    if hi.z / S.H >= zlo and lo.z / S.H <= zhi:
        sel.append(o)
# frame a synthetic box: use only the chosen objects but clip z by a bbox of two empties
e1 = bpy.data.objects.new("e1", None)
e2 = bpy.data.objects.new("e2", None)
cx = sum(o.location.x for o in [])  # unused
xs = [L.bbox_world([o])[0].x for o in sel] + [L.bbox_world([o])[1].x for o in sel]
ys = [L.bbox_world([o])[0].y for o in sel] + [L.bbox_world([o])[1].y for o in sel]
box = L.box("framebox", (max(xs) - min(xs), max(ys) - min(ys), (zhi - zlo) * S.H),
            L.Frame(((max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2, (zhi + zlo) / 2 * S.H)))
box.hide_render = True
out = os.path.join(W, "parts", "_out", "leg")
os.makedirs(out, exist_ok=True)
outs = st.render_views([box], out, views=views, w=w, h=hh, samples=samples, prefix=name + "_", clay=clay)
print("RENDERS", *outs, sep="\n  ")
