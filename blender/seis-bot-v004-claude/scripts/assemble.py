"""assemble - build the whole SEIS bot (standing A-pose) from parts/*.py in ONE scene, rig it, save it.

Headless:
  /Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup --python <W>/src/assemble.py -- \
      [--parts head,shoulder,...] [--no-rig] [--no-studio] [--out FILE.blend] [--render front,three_q] [--w 1000 --h 1300 --samples 64]
Through the Blender MCP add-on (live window):
  python3 <W>/src/mcp_client.py code "ASSEMBLE_ARGS={'out': '<W>/seis_bot_v004_standing.blend'}; exec(open('<W>/src/assemble.py').read())"
"""
import sys
import os
import time
import importlib
import traceback

W = "/PATH/TO/seis-bot-v004-detailed"
HERE = W + "/src"
for p in (HERE, os.path.join(W, "parts")):
    if p not in sys.path:
        sys.path.insert(0, p)

# A long-lived (MCP) Blender keeps imported modules between calls: drop every module that lives in our src/ or parts/
# folders so helper modules (arm_util, foot_kit, ...) are re-read from disk too, not just the part file itself.
for _n, _m in list(sys.modules.items()):
    _f = getattr(_m, "__file__", None) or ""
    if _f.startswith(W + "/src/") or _f.startswith(W + "/parts/"):
        del sys.modules[_n]

import bpy  # noqa: E402
import seis_lib as L  # noqa: E402

ALL_PARTS = ["head", "shoulder", "torso", "pelvis", "arm", "hand", "leg", "foot", "details"]


def _args():
    a = dict(globals().get("ASSEMBLE_ARGS", {}))
    if "--" in sys.argv:
        t = sys.argv[sys.argv.index("--") + 1:]
        i = 0
        while i < len(t):
            k = t[i][2:]
            if k in ("no-rig", "no-studio", "no-cleanup"):
                a[k.replace("-", "_")] = True
            else:
                a[k.replace("-", "_")] = t[i + 1]
                i += 1
            i += 1
    return a


def main():
    a = _args()
    parts = a.get("parts") or [p for p in ALL_PARTS if os.path.exists(os.path.join(W, "parts", p + ".py"))]
    if isinstance(parts, str):
        parts = [p for p in parts.split(",") if p]
    t0 = time.time()
    # importlib caches in a long-lived (MCP) Blender: reload part modules every time
    L.clear_scene()
    root = L.collection("SEIS_BOT")
    report = {"parts": {}, "errors": {}}
    allobjs = []
    for name in parts:
        t1 = time.time()
        c = L.collection("PART_" + name, root)
        L.set_collection(c)
        try:
            m = importlib.import_module(name)
            m = importlib.reload(m)
            res = m.build()
            objs = [o for o in (res or list(c.all_objects)) if o is not None and o.type == "MESH"]
            allobjs += objs
            report["parts"][name] = {"objects": len(objs), "seconds": round(time.time() - t1, 1)}
            print(f"[assemble] {name}: {len(objs)} objects in {time.time() - t1:.1f}s")
        except Exception:
            report["errors"][name] = traceback.format_exc()
            print(f"[assemble] {name} FAILED:\n{report['errors'][name]}")
    # mesh hygiene: NaN vertices, degenerate faces, loose vertices (only touches objects that need it)
    if not a.get("no_cleanup"):
        import seis_cleanup
        rep_c = seis_cleanup.cleanup(allobjs)
        report["cleanup"] = {"objects_touched": len(rep_c),
                             "nan_verts": sum(v["nan_verts"] for v in rep_c.values()),
                             "degenerate_faces": sum(v["degenerate_faces"] for v in rep_c.values()),
                             "loose_verts": sum(v["loose_verts"] for v in rep_c.values())}
        print("[assemble] cleanup:", report["cleanup"])
    if not a.get("no_rig"):
        import seis_rig
        L.set_collection(L.collection("RIG", root))
        rig = seis_rig.build_rig(allobjs)
        report["bones"] = len(rig.data.bones)
        report["unbound"] = rig.get("unbound_objects", "")
        print(f"[assemble] rig: {len(rig.data.bones)} bones; unbound: {rig.get('unbound_objects', '')!r}")
    if not a.get("no_studio"):
        import seis_stage as st
        st.studio(size=1.0)
    out = a.get("out")
    if out:
        os.makedirs(os.path.dirname(out), exist_ok=True)
        bpy.ops.wm.save_as_mainfile(filepath=out)
        print("[assemble] saved", out)
    if a.get("render"):
        import seis_stage as st
        objs = [o for o in allobjs if o.name in bpy.data.objects]
        st.render_views(objs, a.get("render_dir", os.path.join(W, "renders", "assembly")),
                        views=[v for v in a["render"].split(",") if v], w=int(a.get("w", 1000)), h=int(a.get("h", 1300)),
                        samples=int(a.get("samples", 64)), prefix=a.get("prefix", ""))
    report["seconds"] = round(time.time() - t0, 1)
    print("[assemble] DONE", report)
    return report


main()
