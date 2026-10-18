import bpy,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
objs=list(bpy.data.collections['EXPORT'].all_objects)
problems=[]
for o in objs:
 if o.type!='MESH':problems.append(o.name+': unexpected object type')
 if any(abs(s-1)>1e-6 for s in o.scale):problems.append(o.name+': scale not applied')
 if any(abs(r)>1e-6 for r in o.rotation_euler):problems.append(o.name+': rotation not applied')
 if not o.data.materials:problems.append(o.name+': no material')
 if not o.get('body_group'):problems.append(o.name+': missing anatomical group')
 if any(not math.isfinite(c) for v in o.data.vertices for c in v.co):problems.append(o.name+': nonfinite geometry')
report={'status':'PASS' if not problems else 'FAIL','problems':problems,'mesh_count':len(objs),'triangle_count':sum(len(p.vertices)-2 for o in objs for p in o.data.polygons),'static_model':not any(o.type=='ARMATURE' for o in objs),'chest_six_present':bool(bpy.data.objects.get('Chest_Six_Lato')),'body_groups':sorted(set(o.get('body_group') for o in objs)),'scope':'Finite geometry, applied transforms, materials, anatomical group inventory. Not a topology, rig, game-engine, or design-approval check.'}
(ROOT/'reports'/'geometry-checks.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
if problems:raise RuntimeError(problems)
