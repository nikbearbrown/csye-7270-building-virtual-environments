"""arm_ctx - render the arm in context with the other parts (ghosts), framed on ONE arm.  Own helper.
 Blender -b --factory-startup --python parts/arm_ctx.py -- --views front,dir:.. --out DIR [--prefix p_] [--w 700 --h 900 --samples 24 --margin 1.15 --focal 85 --ghost a,b]
"""
import sys, os, importlib
HERE = os.path.dirname(os.path.abspath(__file__)); W = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(W, "src")); sys.path.insert(0, HERE)
import bpy
import seis_lib as L
import seis_stage as st

a = sys.argv[sys.argv.index("--") + 1:]
o = {"views": "front", "out": os.path.join(HERE, "_out", "arm"), "prefix": "", "w": 700, "h": 900, "samples": 24,
     "margin": 1.15, "focal": 85.0, "ghost": "foot,hand,head,leg,pelvis,shoulder,torso", "focus": ""}
i = 0
while i < len(a):
    k = a[i][2:]; o[k] = type(o[k])(a[i + 1]); i += 2
L.clear_scene()
st.studio(size=1.0)
for g in [x for x in o["ghost"].split(",") if x]:
    gm = importlib.import_module(g)
    L.set_collection("GHOST_" + g)
    gm.build()
coll = L.collection("PART_arm"); L.set_collection(coll)
m = importlib.import_module("arm")
objs = [ob for ob in m.build() if ob is not None]
subs = [s for s in o["focus"].split(",") if s]
frame = [ob for ob in objs if ob.name.endswith(".L") and (not subs or any(s in ob.name for s in subs))]
os.makedirs(o["out"], exist_ok=True)
for v in o["views"].split(","):
    tag, view = v, v
    if v.startswith("dir:"):
        x, y, z = [float(q) for q in v[4:].split(":")]
        tag, view = v.replace(":", "_"), ((x, y, z), (0, 0, 1))
    cam = st.camera_for(frame, view, focal=o["focal"], margin=o["margin"], aspect=o["w"] / o["h"])
    p = os.path.join(o["out"], f"{o['prefix']}{tag}.png")
    st.render(p, o["w"], o["h"], o["samples"], gpu=True)
    print("RENDER", p)
