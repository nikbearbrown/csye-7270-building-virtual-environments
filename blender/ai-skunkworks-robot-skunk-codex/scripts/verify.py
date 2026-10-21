import bpy,json,struct,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(R/'ai-skunkworks-robot-skunk.blend'))
col=bpy.data.collections['SKUNK • editable parts'];report={'reopened_with':bpy.app.version_string,'native_mesh_objects':sum(o.type=='MESH' for o in col.objects),'native_curve_objects':sum(o.type=='CURVE' for o in col.objects),'comparison_cameras':[o.name for o in bpy.data.objects if o.type=='CAMERA'],'native_materials':len({m.name for o in col.objects for m in getattr(o.data,'materials',[]) if m})}
assert all(math.isfinite(x) for o in col.objects for row in o.matrix_world for x in row)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.gltf(filepath=str(R/'ai-skunkworks-robot-skunk.glb'))
meshes=[o for o in bpy.context.scene.objects if o.type=='MESH'];tri=0;pts=[]
for o in meshes:
 o.data.calc_loop_triangles();tri+=len(o.data.loop_triangles);pts.extend(o.matrix_world@v.co for v in o.data.vertices)
report.update({'glb_import_meshes':len(meshes),'glb_import_triangles':tri,'glb_dimensions':[max(p[i] for p in pts)-min(p[i] for p in pts) for i in range(3)],'glb_materials':len({m.name for o in meshes for m in o.data.materials if m})})
a=json.loads((R/'audit.json').read_text());assert len(meshes)==a['evaluated_geometry_objects'];assert tri==a['evaluated_triangles'];assert all(abs(x-y)<.0001 for x,y in zip(report['glb_dimensions'],a['dimensions']))
with (R/'ai-skunkworks-robot-skunk.glb').open('rb') as f:
 h=f.read(12);n,t=struct.unpack('<II',f.read(8));doc=json.loads(f.read(n));report['glb_images']=len(doc.get('images',[]));report['glb_animations']=len(doc.get('animations',[]));report['glb_skins']=len(doc.get('skins',[]))
report['result']='PASS: native reopened; GLB geometry count, triangle count and bounds match evaluated native character'
(R/'verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
