import bpy,json
from pathlib import Path
rows={}
for o in bpy.data.objects:
 if o.type!='MESH':continue
 parent=list(range(len(o.data.vertices)))
 def root(x):
  while parent[x]!=x:
   parent[x]=parent[parent[x]];x=parent[x]
  return x
 for e in o.data.edges:
  a,b=map(root,e.vertices);parent[b]=a
 groups={}
 for v in o.data.vertices:groups.setdefault(root(v.index),[]).append(v.co.copy())
 items=[]
 for vs in sorted(groups.values(),key=len,reverse=True):
  items.append({'vertices':len(vs),'min':[round(min(v[k] for v in vs),3) for k in range(3)],'max':[round(max(v[k] for v in vs),3) for k in range(3)]})
 rows[o.name]=items
Path('/Users/bear/Downloads/planet-express-stl-build/components.json').write_text(json.dumps(rows,indent=2))
print(json.dumps(rows))
