"""run_part - build ONE part module in a clean Blender and render it, so a builder can iterate quickly.

    /Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup \
        --python <W>/src/run_part.py -- <module> [options]

    <module>          a file <W>/parts/<module>.py that defines  build()  (see PART CONTRACT below)
    --views a,b,c     views to render (front back left right top three_q three_q_r three_q_back low); default front,three_q,left
    --w N --h N       image size (default 700 x 900);  --samples N (default 24; use 48-96 for a close look)
    --focal N         lens in mm (default 85);  --margin F   framing margin (default 1.12)
    --clay            ALSO render matte grey form-check images (prefix clay_)
    --context         add the grey mannequin from seis_spec (scale and neighbours) to the scene
    --ghost a,b       build these other part modules first (they stay in the scene, the camera frames only this part)
    --frame part|body frame the part (default) or the whole figure
    --out DIR         output folder (default <W>/parts/_out/<module>/)
    --save            write DIR/<module>.blend as well
    --cpu             render on the CPU instead of the Apple GPU (use this if several renders run at once)

PART CONTRACT.  parts/<module>.py:
    import seis_lib as L, seis_spec as S
    def build():                       # build the whole region in WORLD coordinates of the standing A-pose figure
        ...                            # use L.* creators, finish() every object, name objects  <region>_<what>[.L|.R]
        return [objects]               # (optional) the objects that make up the part; default = everything created
The harness has already created and selected the collection PART_<module>, so new objects land there.
Materials: L.finish(obj, "teal") etc.  (see seis_mat.py).
"""
import sys
import os
import math
import time
import importlib

HERE = os.path.dirname(os.path.abspath(__file__))
W = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(W, "parts"))

import bpy  # noqa: E402
import seis_lib as L  # noqa: E402
import seis_stage as st  # noqa: E402


def parse(argv):
    a = argv[argv.index("--") + 1:] if "--" in argv else []
    o = {"module": None, "views": "front,three_q,left", "w": 700, "h": 900, "samples": 24, "focal": 85.0,
         "margin": 1.12, "clay": False, "context": False, "ghost": "", "frame": "part", "out": None, "save": False,
         "cpu": False}
    i = 0
    while i < len(a):
        t = a[i]
        if t in ("--clay", "--context", "--save", "--cpu"):
            o[t[2:]] = True
        elif t.startswith("--"):
            k = t[2:]
            v = a[i + 1]
            i += 1
            o[k] = type(o[k])(v) if k in o and o[k] is not None and not isinstance(o[k], bool) else v
        else:
            o["module"] = t
        i += 1
    return o


def objects_in(coll):
    out = []
    for o in coll.all_objects:
        if o.type == "MESH":
            out.append(o)
    return out


BONES = {"root", "abdomen", "chest", "neck", "head"}
for _side in ("L", "R"):
    for _b in ("pauldron", "upperarm", "forearm", "hand", "thigh", "shin", "foot", "toes"):
        BONES.add(f"{_b}.{_side}")
    for _f in ("thumb", "index", "middle", "ring", "pinky"):
        for _i in (1, 2, 3):
            BONES.add(f"{_f}{_i}.{_side}")


def audit(objs):
    """Print an audit table: triangles, objects missing material/bone, unknown bones, open meshes, tiny/degenerate."""
    import bmesh
    tris = 0
    no_mat, no_bone, bad_bone, open_m, below, dup = [], [], [], [], [], []
    seen = set()
    for ob in objs:
        me = ob.data
        me.calc_loop_triangles()
        tris += len(me.loop_triangles)
        if not me.materials or me.materials[0] is None:
            no_mat.append(ob.name)
        b = ob.get("bone")
        if not b:
            no_bone.append(ob.name)
        elif b not in BONES:
            bad_bone.append(f"{ob.name}:{b}")
        bm = bmesh.new()
        bm.from_mesh(me)
        nm = sum(1 for e in bm.edges if e.is_boundary)
        bm.free()
        if nm:
            open_m.append(f"{ob.name}({nm})")
        lo, hi = L.bbox_world([ob])
        if lo.z < -0.01:
            below.append(f"{ob.name}(z={lo.z:.3f})")
        if ob.name in seen:
            dup.append(ob.name)
        seen.add(ob.name)
    print(f"AUDIT objects={len(objs)} triangles={tris}")
    for label, lst in (("no material", no_mat), ("no bone", no_bone), ("unknown bone", bad_bone),
                       ("open (boundary edges)", open_m), ("below floor", below), ("duplicate names", dup)):
        print(f"AUDIT {label}: {len(lst)}" + (("  e.g. " + ", ".join(lst[:8])) if lst else ""))


def main():
    o = parse(sys.argv)
    mod_name = o["module"]
    out = o["out"] or os.path.join(W, "parts", "_out", mod_name)
    os.makedirs(out, exist_ok=True)
    t0 = time.time()
    L.clear_scene()
    st.studio(size=1.0)
    stage_names = {ob.name for ob in bpy.data.objects}
    if o["context"]:
        import seis_proxy
        L.set_collection("CONTEXT")
        seis_proxy.build()
    for g in [x for x in o["ghost"].split(",") if x]:
        gm = importlib.import_module(g)
        L.set_collection("GHOST_" + g)
        gm.build()
    coll = L.collection("PART_" + mod_name)
    L.set_collection(coll)
    m = importlib.import_module(mod_name)
    importlib.reload(m)
    res = m.build()
    objs = [ob for ob in (res or objects_in(coll)) if ob is not None]
    objs = [ob for ob in objs if ob.type == "MESH"] or objects_in(coll)
    lo, hi = L.bbox_world(objs)
    nv = sum(len(ob.data.vertices) for ob in objs)
    nf = sum(len(ob.data.polygons) for ob in objs)
    print(f"PART {mod_name}: {len(objs)} objects, {nv} verts, {nf} faces; bbox lo={tuple(round(x, 4) for x in lo)} hi={tuple(round(x, 4) for x in hi)} size={tuple(round(h_ - l_, 4) for l_, h_ in zip(lo, hi))}")
    audit(objs)
    frame_objs = objs
    if o["frame"] == "body":
        frame_objs = [ob for ob in bpy.data.objects if ob.type == "MESH" and ob.name not in stage_names]
    w, h = int(o["w"]), int(o["h"])
    views = [v for v in o["views"].split(",") if v]
    outs = st.render_views(frame_objs, out, views=views, w=w, h=h, samples=int(o["samples"]), focal=float(o["focal"]),
                           margin=float(o["margin"]), gpu=not o["cpu"], prefix="")
    if o["clay"]:
        outs += st.render_views(frame_objs, out, views=views, w=w, h=h, samples=int(o["samples"]), focal=float(o["focal"]),
                                margin=float(o["margin"]), gpu=not o["cpu"], prefix="clay_", clay=True)
    if o["save"]:
        bpy.ops.wm.save_as_mainfile(filepath=os.path.join(out, mod_name + ".blend"), copy=True)
    print("RENDERS", *outs, sep="\n  ")
    print(f"DONE in {time.time() - t0:.1f}s")


main()
