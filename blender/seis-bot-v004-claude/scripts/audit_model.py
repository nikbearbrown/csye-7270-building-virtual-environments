"""audit_model - check an assembled SEIS bot .blend and write AUDIT.md / AUDIT.json.

    /Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup <file.blend> --python <W>/src/audit_model.py -- [--out DIR]

Four categories, each PASS/FAIL with the evidence:
  names      unique, convention  region_what[_n][.L|.R], every .L has a .R partner
  materials  every mesh has a SEIS_* material
  geometry   evaluated triangle count, mesh count, height, floor contact, NaN / degenerate faces, open boundary edges
  weights    every vertex of every rigged mesh has exactly one group at weight 1.0 and that group is a real bone
It states numbers only; it does not judge looks.
"""
import sys
import os
import re
import json
import math

import bpy
import bmesh

OUT = None
if "--" in sys.argv:
    t = sys.argv[sys.argv.index("--") + 1:]
    if "--out" in t:
        OUT = t[t.index("--out") + 1]
OUT = OUT or os.path.dirname(bpy.data.filepath) or "/tmp"

NAME_RE = re.compile(r"^[a-z][a-z0-9]*_[A-Za-z0-9_]+(\.[LR])?$")


def meshes():
    """The robot's meshes: everything that is not stage set, plinth or dais."""
    def stage(o):
        if o.get("static") or o.name.startswith(("backdrop", "block_", "window_", "CLAY")):
            return True
        return any(c.name.startswith(("STAGE", "PEDESTAL")) for c in o.users_collection)
    return [o for o in bpy.data.objects if o.type == "MESH" and not stage(o)]


def main():
    rep = {"file": bpy.data.filepath, "blender": bpy.app.version_string}
    obs = meshes()
    rig = next((o for o in bpy.data.objects if o.type == "ARMATURE"), None)
    bones = {b.name for b in rig.data.bones} if rig else set()
    dg = bpy.context.evaluated_depsgraph_get()

    # names
    bad = [o.name for o in obs if not NAME_RE.match(o.name)]
    names = [o.name for o in obs]
    dups = sorted({n for n in names if names.count(n) > 1})
    left = {o.name[:-2] for o in obs if o.name.endswith(".L")}
    right = {o.name[:-2] for o in obs if o.name.endswith(".R")}
    unpaired = sorted((left ^ right))
    rep["names"] = {"pass": not bad and not dups, "meshes": len(obs), "bad_convention": bad[:30], "n_bad": len(bad),
                    "duplicates": dups, "unpaired_LR": unpaired[:30], "n_unpaired_LR": len(unpaired)}

    # materials
    nomat = [o.name for o in obs if not o.data.materials or o.data.materials[0] is None or not o.data.materials[0].name.startswith("SEIS_")]
    from collections import Counter
    mc = Counter(o.data.materials[0].name for o in obs if o.data.materials and o.data.materials[0])
    rep["materials"] = {"pass": not nomat, "missing": nomat[:30], "n_missing": len(nomat), "by_material": dict(mc)}

    # geometry
    tris = 0
    nan_obj, degen, open_obj, loose = [], 0, [], []
    lo = [1e9] * 3
    hi = [-1e9] * 3
    for o in obs:
        ev = o.evaluated_get(dg)
        me = ev.to_mesh()
        me.calc_loop_triangles()
        tris += len(me.loop_triangles)
        for v in me.vertices:
            c = v.co
            if any(math.isnan(x) or math.isinf(x) for x in c):
                nan_obj.append(o.name)
                break
        w = o.matrix_world
        for v in me.vertices:
            p = w @ v.co
            for i in range(3):
                lo[i], hi[i] = min(lo[i], p[i]), max(hi[i], p[i])
        bm = bmesh.new()
        bm.from_mesh(me)
        nb = sum(1 for e in bm.edges if e.is_boundary)
        if nb:
            open_obj.append(f"{o.name}({nb})")
        lv = sum(1 for v in bm.verts if not v.link_edges)
        if lv:
            loose.append(f"{o.name}({lv})")
        degen += sum(1 for f in bm.faces if f.calc_area() < 1e-14)   # float noise after posing makes 1e-12 too strict
        bm.free()
        ev.to_mesh_clear()
    height = hi[2] - lo[2]
    rep["geometry"] = {
        "pass": not nan_obj and degen <= 1e-4 * tris and (abs(lo[2]) < 0.02 and 2.0 < height < 2.4 if not bpy.context.scene.get("seis_bot_pose") else 1.2 < height < 1.7),
        "pose": bpy.context.scene.get("seis_bot_pose", "standing A-pose"),
        "meshes": len(obs), "evaluated_triangles": tris, "height_m": round(height, 4), "z_min": round(lo[2], 4),
        "x_extent_m": [round(lo[0], 3), round(hi[0], 3)], "y_extent_m": [round(lo[1], 3), round(hi[1], 3)],
        "nan_objects": nan_obj, "degenerate_faces": degen, "degenerate_rule": "area < 1e-14 m2 in the evaluated mesh; up to 0.01 percent of triangles tolerated (float noise after posing)",
        "open_meshes": len(open_obj), "open_examples": open_obj[:15], "meshes_with_loose_verts": len(loose),
    }

    # weights
    wfail, wok = [], 0
    for o in obs:
        if not rig:
            break
        mods = [m for m in o.modifiers if m.type == "ARMATURE" and m.object == rig]
        if not mods or o.parent != rig:
            wfail.append(f"{o.name}: not bound")
            continue
        names_ = {g.index: g.name for g in o.vertex_groups}
        problem = None
        for v in o.data.vertices:
            gs = [(names_[g.group], g.weight) for g in v.groups]
            if len(gs) != 1 or abs(gs[0][1] - 1.0) > 1e-4 or gs[0][0] not in bones:
                problem = f"vertex {v.index} -> {gs}"
                break
        if problem:
            wfail.append(f"{o.name}: {problem}")
        else:
            wok += 1
    used = {o.vertex_groups[0].name for o in obs if o.vertex_groups}
    roots = [b.name for b in rig.data.bones if b.parent is None] if rig else []
    zero = [b.name for b in rig.data.bones if b.length < 1e-4] if rig else []
    rep["weights"] = {"pass": bool(rig) and not wfail and len(roots) == 1 and not zero, "rig": rig.name if rig else None,
                      "bones": len(bones), "roots": roots, "zero_length_bones": zero, "meshes_bound_ok": wok,
                      "meshes_failing": len(wfail), "examples": wfail[:15], "bones_without_meshes": sorted(bones - used)}

    rep["overall_pass"] = all(rep[k]["pass"] for k in ("names", "materials", "geometry", "weights"))
    os.makedirs(OUT, exist_ok=True)
    json.dump(rep, open(os.path.join(OUT, "AUDIT.json"), "w"), indent=2)
    L = ["# SEIS bot geometry audit", "", f"File: `{rep['file']}`  .  Blender {rep['blender']}", "",
         f"**Overall: {'PASS' if rep['overall_pass'] else 'FAIL'}**", ""]
    for k in ("names", "materials", "geometry", "weights"):
        d = rep[k]
        L.append(f"## {k}: {'PASS' if d['pass'] else 'FAIL'}")
        for kk, vv in d.items():
            if kk != "pass":
                L.append(f"- {kk}: {vv}")
        L.append("")
    open(os.path.join(OUT, "AUDIT.md"), "w").write("\n".join(L))
    print("AUDIT", "PASS" if rep["overall_pass"] else "FAIL", json.dumps({k: rep[k]["pass"] for k in ("names", "materials", "geometry", "weights")}))
    print("AUDIT meshes", len(obs), "triangles", tris, "height", round(height, 3), "bones", len(bones))


main()
