import bpy, json
from mathutils import Vector

deps = bpy.context.evaluated_depsgraph_get()
meshes = [o for o in bpy.data.objects if o.type == 'MESH']
total_tris = 0
mn = [1e9] * 3; mx = [-1e9] * 3
car_mn = [1e9] * 3; car_mx = [-1e9] * 3
for o in meshes:
    ev = o.evaluated_get(deps)
    me = ev.to_mesh()
    me.calc_loop_triangles()
    total_tris += len(me.loop_triangles)
    ev.to_mesh_clear()
    for c in o.bound_box:
        w = o.matrix_world @ Vector(c)
        for i in range(3):
            mn[i] = min(mn[i], w[i]); mx[i] = max(mx[i], w[i])
            if o.name != 'Ground':
                car_mn[i] = min(car_mn[i], w[i]); car_mx[i] = max(car_mx[i], w[i])

mats = sorted(m.name for m in bpy.data.materials if m.users)
out = {
    'mesh_objects_total': len(meshes),
    'mesh_objects_car': len([o for o in meshes if o.name != 'Ground']),
    'triangles_evaluated': total_tris,
    'materials_used': mats,
    'material_count': len(mats),
    'scene_dims_xyz': [round(mx[i] - mn[i], 3) for i in range(3)],
    'car_dims_xyz': [round(car_mx[i] - car_mn[i], 3) for i in range(3)],
    'blender_version': bpy.app.version_string,
}
print('AUDIT_JSON:' + json.dumps(out))
with open('/tmp/prep/audit.json', 'w') as f:
    json.dump(out, f, indent=1)
