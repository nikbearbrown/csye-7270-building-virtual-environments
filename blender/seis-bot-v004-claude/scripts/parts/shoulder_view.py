"""shoulder_view - my own close-up render harness for the shoulder part (helper, not a shared file).

  blender -b --factory-startup --python parts/shoulder_view.py -- [--context] [--clay] [--left] [--w 800 --h 1000]
          [--samples 32] [--focal 85] [--out DIR] [--ghost a,b]
          NAME:dx,dy,dz:tx,ty,tz:fov  ...

  dx,dy,dz   direction from the subject TO the camera;  tx,ty,tz  target as OFFSET IN H from the LEFT shoulder joint
  fov        visible height of the frame in H (head-heights).
  --left     hide the right-hand copies (.R) from the render.
"""
import sys
import os
import math
import time
import importlib

HERE = os.path.dirname(os.path.abspath(__file__))
W = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(W, "src"))
sys.path.insert(0, HERE)

import bpy  # noqa: E402
from mathutils import Vector  # noqa: E402
import seis_lib as L  # noqa: E402
import seis_stage as st  # noqa: E402
import seis_spec as S  # noqa: E402


def main():
    a = sys.argv[sys.argv.index("--") + 1:]
    o = {"w": 800, "h": 1000, "samples": 32, "focal": 85.0, "out": os.path.join(HERE, "_out", "shoulder_cu"),
         "ghost": "", "hide": "", "context": False, "clay": False, "left": False, "cpu": False, "module": "shoulder"}
    views = []
    i = 0
    while i < len(a):
        t = a[i]
        if t in ("--context", "--clay", "--left", "--cpu"):
            o[t[2:]] = True
        elif t.startswith("--"):
            k = t[2:]
            v = a[i + 1]
            i += 1
            o[k] = type(o[k])(v) if k in o and not isinstance(o[k], bool) else v
        else:
            views.append(t)
        i += 1
    os.makedirs(o["out"], exist_ok=True)
    t0 = time.time()
    L.clear_scene()
    st.studio(size=1.0)
    if o["context"]:
        import seis_proxy
        L.set_collection("CONTEXT")
        seis_proxy.build()
    for g in [x for x in o["ghost"].split(",") if x]:
        gm = importlib.import_module(g)
        L.set_collection("GHOST_" + g)
        gm.build()
    coll = L.collection("PART_shoulder")
    L.set_collection(coll)
    m = importlib.import_module(o["module"])
    t1 = time.time()
    res = m.build()
    print(f"BUILD {time.time() - t1:.1f}s objects={len(res)}")
    if o["left"]:
        for ob in res:
            if ob.name.endswith(".R"):
                ob.hide_render = True
    for h_ in [x for x in o["hide"].split(",") if x]:
        for ob in res:
            if h_ in ob.name:
                ob.hide_render = True
    J = S.J("shoulder.L")
    H = S.H
    sw = 36.0
    for v in views:
        name, d, tgt, fov = v.split(":")
        d = Vector([float(x) for x in d.split(",")]).normalized()
        tg = Vector([float(x) for x in tgt.split(",")]) * H + J
        fov_m = float(fov) * H
        dist = (fov_m / 2) / (sw / 2 / o["focal"])
        cam = bpy.data.objects.get("cam")
        if cam is None:
            cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
            bpy.context.scene.collection.objects.link(cam)
        cam.data.lens = o["focal"]
        cam.data.sensor_width = sw
        cam.data.sensor_height = sw
        cam.data.sensor_fit = "VERTICAL"
        cam.data.clip_start = 0.02
        cam.data.clip_end = 300
        cam.location = tg + d * dist
        cam.rotation_euler = (-d).to_track_quat("-Z", "Y").to_euler()
        bpy.context.scene.camera = cam
        st.set_clay(o["clay"])
        st.render(os.path.join(o["out"], f"{'clay_' if o['clay'] else ''}{name}.png"), int(o["w"]), int(o["h"]),
                  int(o["samples"]), gpu=not o["cpu"])
    st.set_clay(False)
    print(f"VIEWDONE {time.time() - t0:.1f}s")


main()
