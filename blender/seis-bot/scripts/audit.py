# blender -b robot_standing.blend -P audit.py -- out.json
import bpy, bmesh, re, sys, json
from mathutils import Vector
argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
arm = bpy.data.objects.get('RobotRig')
pat = re.compile(r'^[A-Z][A-Za-z0-9]*_[A-Za-z0-9_]+(\.(L|R|side\.L|side\.R))?$')
res = {'naming': [], 'material': [], 'nonmanifold': [], 'zero_area': [], 'parenting': []}
robot = [o for o in bpy.data.objects if o.type == 'MESH' and o.users_collection and o.users_collection[0].name == 'Robot']
names = set()
for o in robot:
    if not pat.match(o.name) or re.search(r'\.\d{3}$', o.name) or o.name in names:
        res['naming'].append(o.name)
    names.add(o.name)
    if len(o.material_slots) == 0 or any(s.material is None for s in o.material_slots):
        res['material'].append(o.name)
    bm = bmesh.new(); bm.from_mesh(o.data)
    nm = sum(1 for e in bm.edges if not e.is_manifold)
    za = sum(1 for f in bm.faces if f.calc_area() < 1e-12)
    if nm: res['nonmanifold'].append((o.name, nm))
    if za: res['zero_area'].append((o.name, za))
    bm.free()
    if not (arm and o.parent == arm and o.parent_type == 'BONE' and o.parent_bone in arm.data.bones):
        res['parenting'].append(o.name)
dg = bpy.context.evaluated_depsgraph_get()
tris = 0; zmax = -9; zmin = 9; xs = []; ys = []
for o in robot:
    ev = o.evaluated_get(dg); me = ev.to_mesh()
    me.calc_loop_triangles(); tris += len(me.loop_triangles)
    for v in me.vertices:
        p = o.matrix_world @ v.co
        zmax = max(zmax, p.z); zmin = min(zmin, p.z); xs.append(p.x); ys.append(p.y)
    ev.to_mesh_clear()
summary = {
    'blender': bpy.app.version_string, 'file': bpy.data.filepath,
    'active_pose': arm.animation_data.action.name if arm and arm.animation_data and arm.animation_data.action else None,
    'mesh_objects': len(robot), 'evaluated_triangles': tris, 'bones': len(arm.data.bones) if arm else 0,
    'materials': sorted({s.material.name for o in robot for s in o.material_slots if s.material}),
    'bbox_m': {'x': [round(min(xs), 3), round(max(xs), 3)], 'y': [round(min(ys), 3), round(max(ys), 3)], 'z': [round(zmin, 3), round(zmax, 3)]},
    'height_m': round(zmax - zmin, 3), 'units': bpy.context.scene.unit_settings.system, 'up': 'Z', 'front': '-Y',
}
checks = {k: ('PASS' if not v else 'FAIL') for k, v in res.items()}
summary['checks'] = checks
summary['failures'] = {k: v[:20] for k, v in res.items() if v}
summary['failure_counts'] = {k: len(v) for k, v in res.items()}
summary['result'] = 'PASS' if all(c == 'PASS' for c in checks.values()) else 'FAIL'
txt = json.dumps(summary, indent=2)
print('AUDIT_BEGIN'); print(txt); print('AUDIT_END')
if argv:
    open(argv[0], 'w').write(txt)
