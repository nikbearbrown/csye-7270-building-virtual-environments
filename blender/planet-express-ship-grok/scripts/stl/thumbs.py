import bpy, glob, os, math, sys
from mathutils import Vector
A='/home/box/agent-data/agents/b69b3394-2ce6-4d73-a2a8-a63bdefca41d/attachments/'
OUT='/workspace/ships/planet-express/stl/thumbs'; os.makedirs(OUT,exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True); sc=bpy.context.scene
sc.render.engine='CYCLES'; sc.cycles.samples=8; sc.cycles.use_denoising=True; sc.cycles.denoiser='OPENIMAGEDENOISE'; sc.render.resolution_x=400; sc.render.resolution_y=300
w=bpy.data.worlds.new('w'); sc.world=w; w.use_nodes=True; w.node_tree.nodes['Background'].inputs[0].default_value=(0.8,0.8,0.82,1)
m=bpy.data.materials.new('m'); m.use_nodes=True; m.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(0.1,0.5,0.45,1)
cd=bpy.data.cameras.new('c'); cam=bpy.data.objects.new('c',cd); sc.collection.objects.link(cam); sc.camera=cam
l=bpy.data.lights.new('s','SUN'); l.energy=4; lo=bpy.data.objects.new('s',l); sc.collection.objects.link(lo); lo.rotation_euler=(0.7,0.2,0.8)
objs=[]
for f in sorted(glob.glob(A+'*.stl')):
    bpy.ops.wm.stl_import(filepath=f); o=bpy.context.selected_objects[0]; o.name=os.path.basename(f)[:8]; o.data.materials.append(m); objs.append(o)
mode=sys.argv[-1]
def frame(obs,dirv,out):
    pts=[o.matrix_world@Vector(c) for o in obs for c in o.bound_box]
    mn=Vector([min(p[i] for p in pts) for i in range(3)]); mx=Vector([max(p[i] for p in pts) for i in range(3)])
    c=(mn+mx)/2; r=(mx-mn).length/2
    cd.lens=50; d=r/math.tan(math.radians(17))*1.05
    cam.location=c+Vector(dirv).normalized()*d; cam.rotation_euler=(c-cam.location).to_track_quat('-Z','Y').to_euler()
    cd.clip_end=d*10; cd.clip_start=d/100
    sc.render.filepath=out; bpy.ops.render.render(write_still=True)
if mode=='parts':
    for o in objs:
        for p in objs: p.hide_render=(p is not o)
        frame([o],(1,-1.3,0.9),f'{OUT}/{o.name}.png')
else:
    sc.render.resolution_x=1200; sc.render.resolution_y=800
    for nm,dv in (('all_iso',(1,-1.3,0.9)),('all_top',(0.001,0,1)),('all_side',(1,0,0.05)),('all_front',(0,-1,0.1))):
        frame(objs,dv,f'{OUT}/{nm}.png')
