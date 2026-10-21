import bpy,json,math
from pathlib import Path
from mathutils import Vector
ROOT=Path('/Users/bear/Downloads/enterprise-build')
def stats():
    meshes=[o for o in bpy.context.scene.objects if o.type=='MESH'];tris=0
    for o in meshes:o.data.calc_loop_triangles();tris+=len(o.data.loop_triangles)
    coords=[o.matrix_world@Vector(c) for o in meshes for c in o.bound_box]
    return {'blender':bpy.app.version_string,'mesh_objects':len(meshes),'triangles':tris,'materials':len({m.name for o in meshes for m in o.data.materials if m}),'dimensions_m':[round(max(v[k] for v in coords)-min(v[k] for v in coords),4) for k in range(3)],'finite_vertices':all(math.isfinite(c) for o in meshes for v in o.data.vertices for c in v.co)}
report={'native_reopen':stats()}
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(ROOT/'enterprise-ncc-1701.glb'))
report['glb_reimport']=stats()
report['dimensions_match']=all(abs(a-b)<.01 for a,b in zip(report['native_reopen']['dimensions_m'],report['glb_reimport']['dimensions_m']))
report['passed']=report['dimensions_match'] and report['native_reopen']['finite_vertices'] and report['glb_reimport']['finite_vertices'] and report['native_reopen']['mesh_objects']==report['glb_reimport']['mesh_objects']
(ROOT/'verification.json').write_text(json.dumps(report,indent=2));print('VERIFICATION',json.dumps(report),flush=True)
