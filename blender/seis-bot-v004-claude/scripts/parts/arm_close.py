"""arm_close - close-up / custom-angle renders of the arm part (my own helper; run_part.py is untouched).

  Blender -b --factory-startup --python parts/arm_close.py -- [--side L|R|both] [--focus sub1,sub2] [--views front,dir:0.6:-0.8:0.1]
          [--w 700 --h 900 --samples 32 --margin 1.12 --focal 85 --out DIR --prefix p_ --clay --cpu --context]
--focus   only objects whose name contains one of the substrings are used to frame the camera (all still render).
--views   named views of seis_stage, or dir:x:y:z = direction from subject to camera.
"""
import sys
import os
import importlib

HERE = os.path.dirname(os.path.abspath(__file__))
W = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(W, "src"))
sys.path.insert(0, HERE)

import bpy  # noqa: E402
import seis_lib as L  # noqa: E402
import seis_stage as st  # noqa: E402


def parse():
    a = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    o = {"side": "L", "focus": "", "views": "front", "w": 700, "h": 900, "samples": 32, "margin": 1.12,
         "focal": 85.0, "out": os.path.join(HERE, "_out", "arm"), "prefix": "", "clay": False, "cpu": False,
         "context": False, "card": 0.0}
    i = 0
    while i < len(a):
        t = a[i]
        if t in ("--clay", "--cpu", "--context"):
            o[t[2:]] = True
        else:
            k = t[2:]
            o[k] = type(o[k])(a[i + 1])
            i += 1
        i += 1
    return o


def main():
    o = parse()
    os.environ["ARM_SIDE"] = o["side"] if o["side"] != "both" else ""
    L.clear_scene()
    st.studio(size=1.0)
    if o["context"]:
        import seis_proxy
        L.set_collection("CONTEXT")
        seis_proxy.build()
    coll = L.collection("PART_arm")
    L.set_collection(coll)
    m = importlib.import_module("arm")
    objs = [ob for ob in m.build() if ob is not None]
    subs = [s for s in o["focus"].split(",") if s]
    frame = [ob for ob in objs if any(s in ob.name for s in subs)] if subs else objs
    views = []
    for v in o["views"].split(","):
        if v.startswith("dir:"):
            x, y, z = [float(q) for q in v[4:].split(":")]
            views.append((v.replace(":", "_"), ((x, y, z), (0, 0, 1))))
        else:
            views.append((v, v))
    os.makedirs(o["out"], exist_ok=True)
    for tag, v in views:
        for clay in ([False, True] if o["clay"] else [False]):
            st.set_clay(clay)
            cam = st.camera_for(frame, v, focal=o["focal"], margin=o["margin"], aspect=o["w"] / o["h"])
            if o["card"] > 0:
                from mathutils import Vector
                ld = bpy.data.lights.get("evalcard") or bpy.data.lights.new("evalcard", "AREA")
                ld.energy, ld.shape, ld.size, ld.size_y = o["card"], "RECTANGLE", 3.0, 3.0
                co = bpy.data.objects.get("evalcard") or bpy.data.objects.new("evalcard", ld)
                if co.name not in bpy.context.scene.collection.objects:
                    bpy.context.scene.collection.objects.link(co)
                tgt = Vector((0, 0, 0))
                lo, hi = L.bbox_world(frame)
                tgt = (lo + hi) / 2
                co.location = cam.location + (cam.location - tgt).normalized() * 0.3 + Vector((0.0, 0.0, 0.25))
                co.rotation_euler = (tgt - co.location).to_track_quat("-Z", "Y").to_euler()
            pre = ("clay_" if clay else "") + o["prefix"]
            p = os.path.join(o["out"], f"{pre}{tag}.png")
            st.render(p, o["w"], o["h"], o["samples"], gpu=not o["cpu"])
            print("RENDER", p)
    st.set_clay(False)


main()
