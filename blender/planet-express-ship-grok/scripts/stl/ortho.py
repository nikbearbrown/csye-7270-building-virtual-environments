import bpy, glob, math
from mathutils import Vector, Matrix
A='/home/box/agent-data/agents/b69b3394-2ce6-4d73-a2a8-a63bdefca41d/attachments/'
bpy.ops.wm.read_factory_settings(use_empty=True); sc=bpy.context.scene
sc.render.engine='CYCLES'; sc.cycles.samples=8; sc.render.resolution_x=1000; sc.render.resolution_y=400
w=bpy.data.worlds.new('w'); sc.world=w; w.use_nodes=True; w.node_tree.nodes['Background'].inputs[0].default_value=(1,1,1,1)
m=bpy.data.materials.new('m'); m.use_nodes=True; m.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(0.1,0.5,0.45,1)
T={'c7d391ae':(Matrix(((0,0,1,13.3),(1,0,0,0),(0,1,0,39.45),(0,0,0,1)))),
   'b060907f':(Matrix(((0,0,-1,-13.8),(-1,0,0,0),(0,1,0,-49.45),(0,0,0,1))))}
for k,M in T.items():
    bpy.ops.wm.stl_import(filepath=glob.glob(A+k+'*.stl')[0]); o=bpy.context.selected_objects[0]; o.matrix_world=M; o.data.materials.append(m)
bpy.ops.object.select_all(action='SELECT'); bpy.context.view_layer.objects.active=o; bpy.ops.object.join(); bpy.ops.object.transform_apply()
bpy.ops.wm.save_as_mainfile(filepath='/workspace/ships/planet-express/stl/hull_assembled_mm.blend')
bpy.ops.wm.stl_export(filepath='/workspace/ships/planet-express/stl/hull_assembled_mm.stl') if hasattr(bpy.ops.wm,'stl_export') else None
cd=bpy.data.cameras.new('c'); cd.type='ORTHO'; cd.ortho_scale=200; cam=bpy.data.objects.new('c',cd); sc.collection.objects.link(cam); sc.camera=cam
for nm,loc,rot in (('side',(0,-300,0),(math.pi/2,0,0)),('top',(0,0,300),(0,0,0)),('bottom',(0,0,-300),(math.pi,0,0)),('front',(300,0,0),(math.pi/2,0,math.pi/2)),('rear',(-300,0,0),(math.pi/2,0,-math.pi/2))):
    cam.location=loc; cam.rotation_euler=rot
    for a,b in ((-1,1),(1,1)):
        pass
    l=bpy.data.lights.new(nm,'SUN'); l.energy=3; lo=bpy.data.objects.new(nm,l); sc.collection.objects.link(lo); lo.rotation_euler=rot
    sc.render.filepath=f'/workspace/ships/planet-express/stl/thumbs/hull_{nm}.png'; bpy.ops.render.render(write_still=True)
