"""foot_view - iteration renderer for the foot builder (own helper; run_part is untouched).
  Blender -b --factory-startup --python parts/foot_view.py -- name:dx,dy,dz[:target x,y,z[:zoom]] ... [--w N --h N --samples N --clay --both --out DIR]
Renders only the LEFT foot (.L objects) unless --both.  Output: DIR/v_<name>.png"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
W = os.path.dirname(HERE)
sys.path[:0] = [os.path.join(W, "src"), HERE]
import bpy
from mathutils import Vector
import seis_lib as L
import seis_stage as st


def main():
    a = sys.argv[sys.argv.index("--") + 1:]
    w, h, samples, clay, both = 900, 600, 32, False, False
    ghost = []
    out = os.path.join(HERE, "_out", "foot")
    specs = []
    i = 0
    while i < len(a):
        t = a[i]
        if t == "--w": w = int(a[i + 1]); i += 1
        elif t == "--h": h = int(a[i + 1]); i += 1
        elif t == "--samples": samples = int(a[i + 1]); i += 1
        elif t == "--out": out = a[i + 1]; i += 1
        elif t == "--clay": clay = True
        elif t == "--both": both = True
        elif t == "--ghost": ghost = a[i + 1].split(","); i += 1
        else: specs.append(t)
        i += 1
    L.clear_scene()
    st.studio(size=1.0)
    import importlib
    for g in ghost:
        L.set_collection("GHOST_" + g)
        importlib.import_module(g).build()
    L.set_collection(L.collection("PART_foot"))
    import foot
    objs = foot.build()
    sel = [o for o in objs if both or o.name.endswith(".L")]
    for o in objs:
        if o not in sel:
            o.hide_render = True
    os.makedirs(out, exist_ok=True)
    for sp in specs:
        parts = sp.split(":")
        name = parts[0]
        d = Vector([float(x) for x in parts[1].split(",")])
        tgt = None
        zoom = 1.0
        if len(parts) > 2 and parts[2]:
            tgt = Vector([float(x) for x in parts[2].split(",")])
        if len(parts) > 3:
            zoom = float(parts[3])
        fsel = sel
        if len(parts) > 4 and parts[4]:
            keys = parts[4].split(",")
            fsel = [o for o in sel if any(k in o.name for k in keys)] or sel
        st.camera_for(fsel, (d, (0, 0, 1)), focal=85.0 * zoom, margin=1.08, aspect=w / h, target=tgt)
        st.set_clay(clay)
        st.render(os.path.join(out, f"v_{name}.png"), w, h, samples)
        st.set_clay(False)
    tris = 0
    for o in sel:
        o.data.calc_loop_triangles(); tris += len(o.data.loop_triangles)
    print("VIEWTRIS", tris)


main()
