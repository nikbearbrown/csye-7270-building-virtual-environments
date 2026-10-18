"""make_seated - open a standing SEIS bot .blend, pose the Thinker, add the block, save the seated study (+ renders).

 blender -b --factory-startup <standing.blend> --python <W>/src/make_seated.py -- --out <seated.blend> [--render front,three_q,left] [--w 1000 --h 1300 --samples 64] [--render-dir DIR]
"""
import sys, os
W = "/PATH/TO/seis-bot-v004-detailed"
for p in (W + "/src", W + "/parts"):
    if p not in sys.path:
        sys.path.insert(0, p)
import bpy
import seis_lib as L, seated, seis_stage as st

t = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
a = {t[i][2:].replace("-", "_"): t[i + 1] for i in range(0, len(t) - 1, 2)}
rig = bpy.data.objects["SEIS_rig"]
info = seated.apply(rig)
print("[seated]", info)
if a.get("out"):
    os.makedirs(os.path.dirname(a["out"]), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=a["out"])
    print("[seated] saved", a["out"])
if a.get("render"):
    objs = [o for o in bpy.data.objects if o.type == "MESH" and o.parent == rig] + [o for o in bpy.data.objects if o.get("static")]
    st.render_views(objs, a.get("render_dir", W + "/renders/seated"), views=a["render"].split(","),
                    w=int(a.get("w", 1000)), h=int(a.get("h", 1300)), samples=int(a.get("samples", 64)))
