#!/usr/bin/env python3
"""Audit ducati-scrambler-custom.blend: real triangle/material/mesh counts.
Run: blender --background ducati-scrambler-custom.blend --python scripts/audit_blend.py
"""
import bpy

meshes = [o for o in bpy.data.objects if o.type == 'MESH']
total_tris = 0
per_obj = []
for o in meshes:
    m = o.data
    m.calc_loop_triangles()
    n = len(m.loop_triangles)
    total_tris += n
    per_obj.append((o.name, n))
per_obj.sort(key=lambda t: -t[1])

mats = [(m.name, m.users) for m in bpy.data.materials]
dims = {}
import mathutils
for o in meshes:
    if o.name == 'ground':
        continue
    ws = [o.matrix_world @ mathutils.Vector(c) for c in o.bound_box]
    xs = [v.x for v in ws]; ys = [v.y for v in ws]; zs = [v.z for v in ws]
    dims[o.name] = (round(max(xs) - min(xs), 3), round(max(ys) - min(ys), 3),
                    round(max(zs) - min(zs), 3))
mn = [1e9]*3; mx = [-1e9]*3
for o in meshes:
    if o.name == 'ground':
        continue
    for c in o.bound_box:
        w = o.matrix_world @ mathutils.Vector(c)
        for i in range(3):
            mn[i] = min(mn[i], w[i]); mx[i] = max(mx[i], w[i])
overall = tuple(round(mx[i] - mn[i], 3) for i in range(3))

print("=== AUDIT ===")
print("mesh objects:", len(meshes))
print("total triangles:", total_tris)
print("materials:", len(mats), [n for n, _ in mats])
print("overall dims (x,y,z) m:", overall)
print("top 12 objects by tris:")
for n, t in per_obj[:12]:
    print(f"  {t:7d}  {n}")
