"""Native-asset integrity report. It does not claim visual similarity or collision clearance."""
import bpy,json,math,re,os
from pathlib import Path
from mathutils import Vector
root=Path(os.environ.get('SEIS_OUTPUT',str(Path(bpy.data.filepath).parent)))
exp=bpy.data.collections['EXPORT'];deps=bpy.context.evaluated_depsgraph_get();errors=[];counts=[]
lo=Vector((1e9,)*3);hi=Vector((-1e9,)*3);triangles=0;degenerate=0;meshcount=0
rig=bpy.data.objects['SEIS_Bot_Rig'];bones=set(rig.data.bones.keys())
for ob in exp.objects:
    if ob.type!='MESH':continue
    meshcount+=1
    if not re.fullmatch('[A-Za-z0-9_]+',ob.name):errors.append('name '+ob.name)
    if ob.name!=ob.data.name:errors.append('data_name '+ob.name)
    if any(abs(x-1)>1e-6 for x in ob.scale):errors.append('scale '+ob.name)
    if not ob.data.materials:errors.append('material '+ob.name)
    if len(ob.vertex_groups)!=1 or ob.vertex_groups[0].name not in bones:errors.append('bone '+ob.name)
    for v in ob.data.vertices:
        if not all(math.isfinite(x) for x in v.co):errors.append('nonfinite '+ob.name);break
        if len(v.groups)!=1 or abs(v.groups[0].weight-1)>1e-6:errors.append('weight '+ob.name);break
    evaluated=ob.evaluated_get(deps);me=evaluated.to_mesh();me.calc_loop_triangles()
    nt=len(me.loop_triangles);triangles+=nt;bad=0
    for t in me.loop_triangles:
        a,b,c=[me.vertices[i].co for i in t.vertices]
        if (b-a).cross(c-a).length<1e-13:bad+=1
    degenerate+=bad
    if bad:counts.append({'name':ob.name,'degenerate_triangles':bad})
    for v in me.vertices:
        p=ob.matrix_world@v.co
        for k in range(3):lo[k]=min(lo[k],p[k]);hi[k]=max(hi[k],p[k])
    evaluated.to_mesh_clear()
roots=[b.name for b in rig.data.bones if b.parent is None and b.use_deform]
if roots!=['root']:errors.append('root_count '+str(roots))
report={'asset':'SEIS_BOT_V005','blender':bpy.app.version_string,'native_file':Path(bpy.data.filepath).name,'status':'PASS' if not errors and not degenerate else 'REVIEW','errors':errors,'evaluated_meshes':meshcount,'evaluated_triangles':triangles,'degenerate_triangle_count':degenerate,'degenerate_objects':counts,'bones':len(bones),'deform_roots':roots,'material_count':len({s.material.name for o in exp.objects if o.type=='MESH' for s in o.material_slots if s.material}),'bounds_metres':{'min':list(lo),'max':list(hi),'size':list(hi-lo)},'scope':'Names, finite geometry, rigid normalized weights, transforms, materials and triangle integrity. Does not certify visual match, animation clearance or game-engine export.'}
(root/'reports').mkdir(exist_ok=True);(root/'reports/integrity.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
