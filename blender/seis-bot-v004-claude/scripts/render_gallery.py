"""render_gallery - render the SEIS bot gallery from an assembled .blend (standing or seated).

    blender -b --factory-startup <file.blend> --python <W>/src/render_gallery.py -- --out DIR [--set full|close|all]
            [--w 1600 --h 2000] [--cw 1600 --ch 2000] [--samples 128] [--only front,head_front] [--clay]

full views : front three_q three_q_r left right back three_q_back top low   (whole figure; 4:5 portrait)
close views: head_front head_three_q shoulder_three_q chest_front hand_left knee_front foot_three_q (3:4 portrait)
Also works in a live Blender through the MCP:  ARGS = {...}; exec(open(this file).read())
"""
import sys
import os
import math

W = "/PATH/TO/seis-bot-v004-detailed"
for p in (W + "/src", W + "/parts"):
    if p not in sys.path:
        sys.path.insert(0, p)
import bpy
from mathutils import Vector
import seis_lib as L
import seis_spec as S
import seis_stage as st

FULL = ["front", "three_q", "three_q_r", "left", "right", "back", "three_q_back", "top", "low"]
# close-ups: name -> (view, centre joint/point (world), half-height in metres)
CLOSE = {
    "head_front": ("front", lambda: S.J("head_pivot") + Vector((0, 0, S.hh(0.25))), 0.30),
    "head_three_q": ("three_q", lambda: S.J("head_pivot") + Vector((0, 0, S.hh(0.25))), 0.30),
    "shoulder_three_q": ("three_q", lambda: S.J("shoulder.L") + Vector((0, 0, S.hh(0.1))), 0.42),
    "chest_front": ("front", lambda: S.J("spine_chest"), 0.55),
    "hand_left": ("three_q", lambda: S.J("wrist.L") + Vector((0, 0, -S.hh(0.3))), 0.26),
    "knee_front": ("front", lambda: S.J("knee.L"), 0.55),
    "foot_three_q": ("three_q", lambda: S.J("ankle.L") + Vector((0, 0, S.hh(0.2))), 0.34),
}


def _args():
    a = dict(globals().get("ARGS", {}))
    if "--" in sys.argv:
        t = sys.argv[sys.argv.index("--") + 1:]
        for i in range(0, len(t) - 1, 2):
            a[t[i][2:].replace("-", "_")] = t[i + 1]
    return a


def main():
    a = _args()
    out = a.get("out", W + "/renders/gallery")
    os.makedirs(out, exist_ok=True)
    which = a.get("set", "all")
    only = set(a["only"].split(",")) if a.get("only") else None
    w, h = int(a.get("w", 1600)), int(a.get("h", 2000))
    cw, ch = int(a.get("cw", 1600)), int(a.get("ch", 2000))
    samples = int(a.get("samples", 128))
    prefix = a.get("prefix", "")
    rig = next((o for o in bpy.data.objects if o.type == "ARMATURE"), None)
    body = [o for o in bpy.data.objects if o.type == "MESH" and not o.name.startswith(("backdrop", "window_"))]
    stage = a.get("stage", "cove")
    fstop = float(a["fstop"]) if a.get("fstop") else None
    if stage == "workshop":
        # swap the white cove for the on-model brick-workshop rig
        sc_ = bpy.data.collections.get("STAGE")
        if sc_:
            for o in list(sc_.objects):
                bpy.data.objects.remove(o, do_unlink=True)
        st.workshop(size=1.0)
    elif "STAGE" not in bpy.data.collections:
        st.studio(size=1.0)
    made = []
    clay = a.get("clay") in (True, "1", "true", "True")
    st.set_clay(clay)
    if which in ("full", "all"):
        for v in FULL:
            if only and v not in only:
                continue
            st.camera_for(body, v, focal=85.0, margin=1.10, aspect=w / h, fstop=fstop)
            made.append(st.render(os.path.join(out, f"{prefix}{v}.png"), w, h, samples))
    if which in ("close", "all"):
        for name, (view, centre, half) in CLOSE.items():
            if only and name not in only:
                continue
            c = centre()
            # frame a box around the centre so the camera helper fits it
            box = [c + Vector((x, y, z)) for x in (-half * 0.7, half * 0.7) for y in (-half * 0.7, half * 0.7) for z in (-half, half)]
            tmp = bpy.data.objects.new("_frame", None)
            bpy.context.scene.collection.objects.link(tmp)
            # build a throw-away mesh to carry the bbox
            me = bpy.data.meshes.new("_frame")
            me.from_pydata([tuple(p) for p in box], [], [])
            fo = bpy.data.objects.new("_frame_m", me)
            bpy.context.scene.collection.objects.link(fo)
            st.camera_for([fo], view, focal=105.0, margin=1.04, aspect=cw / ch, target=c, fstop=fstop)
            made.append(st.render(os.path.join(out, f"{prefix}{name}.png"), cw, ch, samples))
            bpy.data.objects.remove(fo, do_unlink=True)
            bpy.data.objects.remove(tmp, do_unlink=True)
    st.set_clay(False)
    print("[gallery]", *made, sep="\n  ")


main()
