# blender -b enterprise_futurama_toy.blend -P export.py  -> enterprise_futurama_toy.glb + stats.json (does not save the .blend)
import bpy, json
from mathutils import Vector
H='/workspace/ships/enterprise-futurama'
sc=bpy.context.scene
g=bpy.data.objects.get('Ground'); bpy.data.objects.remove(g)
for o in sc.objects: o.select_set(o.type=='CURVE')
bpy.context.view_layer.objects.active=[o for o in sc.objects if o.type=='CURVE'][0]
bpy.ops.object.convert(target='MESH')
dg=bpy.context.evaluated_depsgraph_get(); tris=0; n=0; mn=Vector((1e9,)*3); mx=Vector((-1e9,)*3)
for o in sc.objects:
    if o.type!='MESH': continue
    ev=o.evaluated_get(dg); me=ev.to_mesh(); n+=1; me.calc_loop_triangles(); tris+=len(me.loop_triangles)
    for v in me.vertices:
        w=ev.matrix_world@v.co; mn=Vector(map(min,mn,w)); mx=Vector(map(max,mx,w))
    ev.to_mesh_clear()
st={'objects':n,'triangles':tris,'size':[round(x,3) for x in (mx-mn)],'bbox_min':[round(x,3) for x in mn],'bbox_max':[round(x,3) for x in mx],'materials':len([m for m in bpy.data.materials if m.users and m.name!='ground'])}
json.dump(st,open(f'{H}/stats.json','w'),indent=1); print('STATS',st)
bpy.ops.export_scene.gltf(filepath=f'{H}/enterprise_futurama_toy.glb',export_format='GLB',export_apply=True)
print('GLB_DONE')
