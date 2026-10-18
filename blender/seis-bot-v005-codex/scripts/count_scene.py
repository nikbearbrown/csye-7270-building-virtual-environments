"""Blender -b <file.blend> --python count_scene.py -- <out.json>
Counts meshes, evaluated triangles, materials, armature bones and overall dimensions of every mesh in the file, from the file itself."""
import json
import sys

import bpy

out = sys.argv[sys.argv.index("--") + 1]
dg = bpy.context.evaluated_depsgraph_get()
meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]
tris = 0
lo = [1e18] * 3
hi = [-1e18] * 3
for o in meshes:
    e = o.evaluated_get(dg)
    m = e.to_mesh()
    m.calc_loop_triangles()
    tris += len(m.loop_triangles)
    for c in o.bound_box:
        w = o.matrix_world @ __import__("mathutils").Vector(c)
        for k in range(3):
            lo[k] = min(lo[k], w[k])
            hi[k] = max(hi[k], w[k])
    e.to_mesh_clear()
res = {
    "blender": bpy.app.version_string,
    "file": bpy.data.filepath.split("/")[-1],
    "mesh_objects": len(meshes),
    "triangles": tris,
    "materials": len(bpy.data.materials),
    "armatures": len([o for o in bpy.context.scene.objects if o.type == "ARMATURE"]),
    "bones": sum(len(a.bones) for a in bpy.data.armatures),
    "cameras": len([o for o in bpy.context.scene.objects if o.type == "CAMERA"]),
    "lights": len([o for o in bpy.context.scene.objects if o.type == "LIGHT"]),
    "dimensions_m_xyz": [round(hi[k] - lo[k], 4) for k in range(3)] if meshes else None,
}
json.dump(res, open(out, "w"), indent=1)
print("COUNT", json.dumps(res))
