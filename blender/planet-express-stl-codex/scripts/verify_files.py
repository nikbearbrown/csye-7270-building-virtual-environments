import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path('/Users/bear/Downloads/planet-express-stl-build')
def stats(native):
 obs=[o for o in bpy.context.scene.objects if o.type=='MESH' and (not native or o.get('export_part'))];co=[];tri=0
 for o in obs:o.data.calc_loop_triangles();tri+=len(o.data.loop_triangles);co.extend(o.matrix_world@v.co for v in o.data.vertices)
 return {'meshes':len(obs),'triangles':tri,'dimensions':[round(max(v[k] for v in co)-min(v[k] for v in co),6) for k in range(3)],'materials':len({m.name for o in obs for m in o.data.materials if m}),'finite':all(math.isfinite(x) for o in obs for v in o.data.vertices for x in v.co)}
r={'blender':bpy.app.version_string,'native_mm':stats(True)}
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(R/'planet-express-ship.glb'));r['glb_m']=stats(False)
r['dimensions_match']=all(abs(a*.001-b)<.0001 for a,b in zip(r['native_mm']['dimensions'],r['glb_m']['dimensions']))
r['passed']=r['dimensions_match'] and r['native_mm']['meshes']==r['glb_m']['meshes'] and r['native_mm']['triangles']==r['glb_m']['triangles'] and r['native_mm']['finite'] and r['glb_m']['finite']
(R/'verification.json').write_text(json.dumps(r,indent=2));print('VERIFICATION',json.dumps(r),flush=True)
