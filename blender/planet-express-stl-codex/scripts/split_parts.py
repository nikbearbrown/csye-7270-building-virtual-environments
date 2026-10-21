import bpy,json
from pathlib import Path
for o in list(bpy.data.objects):
 if o.type!='MESH' or not o.name.startswith('GOODesign_'):continue
 parent=list(range(len(o.data.vertices)))
 def root(x):
  while parent[x]!=x:parent[x]=parent[parent[x]];x=parent[x]
  return x
 for e in o.data.edges:
  a,b=map(root,e.vertices);parent[b]=a
 groups={}
 for v in o.data.vertices:groups.setdefault(root(v.index),[]).append(v.index)
 if len(groups)==1:continue
 groups=sorted(groups.values(),key=lambda g: (-len(g),min(o.data.vertices[i].co.x for i in g)))
 for j,g in enumerate(groups):
  remap={v:i for i,v in enumerate(g)};faces=[tuple(remap[v] for v in p.vertices) for p in o.data.polygons if p.vertices[0] in remap]
  me=bpy.data.meshes.new(o.name+f'.part{j+1}');me.from_pydata([o.data.vertices[v].co for v in g],[],faces);me.update();part=bpy.data.objects.new(me.name,me)
  for c in o.users_collection:c.objects.link(part)
  part.matrix_world=o.matrix_world.copy();part.hide_render=o.hide_render
  for m in o.data.materials:me.materials.append(m)
  part['source_file']=o.get('source_file');part['component']=j+1
 bpy.data.objects.remove(o,do_unlink=True)
bpy.ops.wm.save_as_mainfile(filepath='/Users/bear/Downloads/planet-express-stl-build/planet-express-components.blend',compress=True)
print('Separated connected components; no mesh decimation.')
