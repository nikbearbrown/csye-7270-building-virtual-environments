import bpy,math,json
from mathutils import Vector,Matrix
from pathlib import Path
R=Path('/Users/bear/Downloads/planet-express-stl-build');scene=bpy.context.scene
for o in list(bpy.data.objects):
 if o.name.startswith('Detail •'):bpy.data.objects.remove(o,do_unlink=True)
col=bpy.data.collections.get('Added reference details') or bpy.data.collections.new('Added reference details')
if col.name not in scene.collection.children:scene.collection.children.link(col)
dark=bpy.data.materials['Graphite'];ivory=bpy.data.materials['Warm ivory fittings']
def mesh_obj(name,vs,fs,mat):
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new(name,me);col.objects.link(o);me.materials.append(mat);return o
# Antenna is an explicit reference-derived addition, not part of the source kit.
vs=[];fs=[]
for z in [64.3,71.5]:
 for i in range(24):a=i*math.tau/24;vs.append((.28*math.cos(a),-9.37+.28*math.sin(a),z))
for i in range(24):j=(i+1)%24;fs.append((i,j,j+24,i+24))
fs.extend([tuple(range(23,-1,-1)),tuple(range(24,48))]);mesh_obj('Detail • antenna',vs,fs,dark)
# Lettering around both supplied three-color emblems.
for s in [1,-1]:
 basis=Matrix(((0,0,s,0),(s,0,0,0),(0,1,0,0),(0,0,0,1)))
 for word,start,end,bottom in [('PLANET',140,40,False),('EXPRESS',220,320,True)]:
  for i,ch in enumerate(word):
   a=math.radians(start+(end-start)*i/(len(word)-1));u=8.2*math.cos(a);v=8.2*math.sin(a)
   cu=bpy.data.curves.new('Emblem lettering','FONT');cu.body=ch;cu.align_x='CENTER';cu.align_y='CENTER';cu.size=2.15;cu.extrude=.025;cu.resolution_u=8
   o=bpy.data.objects.new(f'Detail • {s} {word} {i}',cu);col.objects.link(o);cu.materials.append(dark)
   o.matrix_world=Matrix.Translation(Vector((s*7.08,79+s*u,60+v)))@basis@Matrix.Rotation(a+(math.pi/2 if bottom else -math.pi/2),4,'Z')
   bpy.context.view_layer.update();me=bpy.data.meshes.new_from_object(o.evaluated_get(bpy.context.evaluated_depsgraph_get()));new=bpy.data.objects.new(o.name+' mesh',me);col.objects.link(new);new.matrix_world=o.matrix_world.copy();bpy.data.objects.remove(o,do_unlink=True)
# Close the boarding stair frame for the flight presentation; keep spare hardware inspectable.
o=bpy.data.objects['GOODesign_Stair_A.part1'];pivot=Vector((0,-30,19));o.matrix_world=Matrix.Translation(pivot)@Matrix.Rotation(math.radians(-20),4,'X')@Matrix.Translation(-pivot)
bpy.data.objects['GOODesign_Stair_B'].hide_render=True
# Organize visible assembly and unused/accessory kit geometry separately.
assembly=bpy.data.collections.get('ASSEMBLY • flight presentation') or bpy.data.collections.new('ASSEMBLY • flight presentation')
spares=bpy.data.collections.get('ACCESSORIES • not fitted for flight') or bpy.data.collections.new('ACCESSORIES • not fitted for flight')
for c in [assembly,spares]:
 if c.name not in scene.collection.children:scene.collection.children.link(c)
for o in list(bpy.data.objects):
 if o.type!='MESH' or not o.name.startswith('GOODesign_'):continue
 dest=spares if o.hide_render else assembly
 for c in list(o.users_collection):c.objects.unlink(o)
 dest.objects.link(o)
spares.hide_render=True;spares.hide_viewport=True
scene.name='Planet Express • GOODesign STL assembly by Codex'
scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=.001;scene.unit_settings.length_unit='MILLIMETERS'
scene['source_creator']='GOODesign / GOODesignLabs';scene['assembly_credit']='Codex for Nik Bear Brown';scene['human_review']='Professor Bear: pending';scene['presentation']='Static flight assembly; accessory fitting and animation rig are not validated.'
scene.render.engine='CYCLES';scene.cycles.samples=64;scene.cycles.use_denoising=True;scene.view_settings.view_transform='AgX';scene.render.resolution_x=1600;scene.render.resolution_y=1100;scene.render.resolution_percentage=100
views=[('hero',(240,-270,180),(0,25,35),285),('port',(-400,25,45),(0,25,45),280),('rear',(-180,260,125),(0,35,35),275),('top',(0,35,400),(0,35,0),280),('front',(0,-400,65),(0,0,35),130),('turret',(100,-60,140),(0,-10,54),72),('engine',(-180,260,90),(0,83,38),145)]
for name,loc,target,scale in views:
 n='View • '+name;c=bpy.data.objects.get(n)
 if not c:
  d=bpy.data.cameras.new(n);c=bpy.data.objects.new(n,d);scene.collection.objects.link(c)
 c.data.type='ORTHO';c.data.ortho_scale=scale;c.data.clip_end=2000;c.location=loc;c.rotation_euler=(Vector(target)-c.location).to_track_quat('-Z','Y').to_euler()
 scene.camera=c;scene.render.filepath=str(R/'renders'/f'{name}.png');bpy.ops.render.render(write_still=True)
scene.camera=bpy.data.objects['View • hero']
bpy.ops.wm.save_as_mainfile(filepath=str(R/'planet-express-ship.blend'),compress=True)
print('Final presentation views rendered and native scene saved.')
