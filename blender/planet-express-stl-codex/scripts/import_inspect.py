import bpy,json,math,struct
from pathlib import Path
from mathutils import Vector
ROOT=Path('/Users/bear/Downloads/planet-express-stl-build')
SOURCE=Path('/Users/bear/Documents/CoWork/bear-textbooks/books/Planet_Express_Ship_-_FUTURAMA')
# Run in a new empty Blender scene; preserve the previous saved deliverable.
scene=bpy.context.scene;scene.name='Planet Express • source layout'
scene.unit_settings.system='NONE'
source_col=bpy.data.collections.new('SOURCE STL • original coordinates');scene.collection.children.link(source_col)
def mat(name,color,metal=0):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=.38;return m
teal=mat('Hull teal • provisional',(.05,.42,.28),.15);red=mat('Red trim • provisional',(.65,.035,.018),.1);silver=mat('Machinery silver • provisional',(.48,.54,.58),.65);dark=mat('Dark fittings • provisional',(.04,.07,.09),.35);glass=mat('Glazing • provisional',(.14,.36,.46),.3);cream=mat('Logo base • provisional',(.82,.78,.59))
rows=[]
for p in sorted(SOURCE.glob('*.stl')):
 raw=p.read_bytes();count=struct.unpack_from('<I',raw,80)[0];verts=[];faces=[];lookup={}
 for i in range(count):
  vals=struct.unpack_from('<9f',raw,84+50*i+12);face=[]
  for j in range(0,9,3):
   v=vals[j:j+3]
   if v not in lookup:lookup[v]=len(verts);verts.append(v)
   face.append(lookup[v])
  faces.append(tuple(face))
 data=bpy.data.meshes.new(p.stem);data.from_pydata(verts,[],faces);data.update();o=bpy.data.objects.new(p.stem,data);scene.collection.objects.link(o)
 for c in list(o.users_collection):c.objects.unlink(o)
 source_col.objects.link(o)
 name=p.stem.lower();material=teal
 if 'red_' in name or 'ring' in name:material=red
 if any(k in name for k in ['silver','gear','stair','turret']):material=silver
 if 'nozzle' in name:material=dark
 if 'window' in name and 'frame' not in name or 'dome' in name:material=glass
 if 'logo' in name:material=cream
 o.data.materials.append(material)
 # Do not alter source mesh positions or topology.
 o['source_file']=p.name;o['source_units']='STL units unspecified; coordinates preserved.'
 o.data.calc_loop_triangles();co=[o.matrix_world@Vector(c) for c in o.bound_box]
 rows.append({'object':o.name,'triangles':len(o.data.loop_triangles),'vertices':len(o.data.vertices),'bounds':[[min(v[k] for v in co) for k in range(3)],[max(v[k] for v in co) for k in range(3)]]})
world=bpy.data.worlds.new('Studio navy');scene.world=world;world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(.035,.045,.06,1);world.node_tree.nodes['Background'].inputs[1].default_value=.5
studio=bpy.data.collections.new('Inspection studio');scene.collection.children.link(studio)
def aim(o,p):o.rotation_euler=(Vector(p)-o.location).to_track_quat('-Z','Y').to_euler()
for name,loc,power,size in [('Key',(0,-150,240),1400000,180),('Fill',(240,80,200),1500000,160),('Rim',(-100,180,170),1700000,160)]:
 d=bpy.data.lights.new(name,'AREA');d.energy=power;d.shape='DISK';d.size=size;o=bpy.data.objects.new(name,d);studio.objects.link(o);o.location=loc;aim(o,(40,30,20))
for name,loc,target,scale in [('source-layout',(265,-330,240),(50,30,32),310),('source-top',(45,35,500),(45,35,0),300),('source-side',(480,25,32),(0,25,32),280)]:
 d=bpy.data.cameras.new(name);d.type='ORTHO';d.ortho_scale=scale;d.clip_end=2000;o=bpy.data.objects.new(name,d);studio.objects.link(o);o.location=loc;aim(o,target)
scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=True;scene.view_settings.view_transform='AgX';scene.render.resolution_x=1600;scene.render.resolution_y=1100;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
scene.camera=bpy.data.objects['source-layout']
(ROOT/'source-audit.json').write_text(json.dumps(rows,indent=2))
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'planet-express-source-layout.blend'),compress=True)
for name in ['source-layout','source-top','source-side']:
 scene.camera=bpy.data.objects[name];scene.render.filepath=str(ROOT/'renders'/f'{name}.png');bpy.ops.render.render(write_still=True)
print('IMPORTED',len(rows),'STL objects; source geometry and transforms preserved.',flush=True)
