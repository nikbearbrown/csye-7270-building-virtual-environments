"""Rebuild SEIS Bot v005 from reference-specific native geometry modules.
Blender 5.1.2, metre scale, -Y facing; all mesh originals in EXPORT.
"""
import os,sys,json,math
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
if 'SEIS_OUTPUT' not in os.environ:os.environ['SEIS_OUTPUT']=str(HERE.parent if HERE.name=='scripts' else HERE/'output')
import bpy
from mathutils import Vector
import model_utils as U
from torso import build_torso
from shoulders_back import build_shoulders_back
from limbs import build_limbs
from head import build_head

for name,fn in [('torso',build_torso),('shoulders_back',build_shoulders_back),('limbs',build_limbs),('head',build_head)]:
    print('BUILD',name,flush=True);fn(U)
U.enhance_materials()

# Every articulated shell binds after applied transforms; this is an editable FK
# study rather than a game export or production animation rig.
print('BUILD rig',flush=True)
for suf,side,sgn in [('l','L',1),('r','R',-1)]:
    U.BONES['clavicle_'+suf]=((sgn*.085,0,1.79),(sgn*.373,0,1.77),'chest')
    a,b,parent=U.BONES['upper_arm_'+suf];U.BONES['upper_arm_'+suf]=(a,b,'clavicle_'+suf)
    for name in U.PARTS:
        if name.startswith('Shoulder_'+side+'_'):U.PARTS[name]='clavicle_'+suf
for name in list(U.PARTS):
    ob=bpy.data.objects[name];bpy.ops.object.select_all(action='DESELECT');ob.select_set(True);bpy.context.view_layer.objects.active=ob
    bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
# Reference body has a short mechanical waist. Compress only the abdominal
# interval; translate the thorax/head rigidly, retaining all their local detail.
def compact_z(z):
    return z-.052*max(0,min(1,(z-1.15)/.25))
for name in U.PARTS:
    ob=bpy.data.objects[name]
    for v in ob.data.vertices:
        wz=v.co.z+ob.location.z;v.co.z=compact_z(wz)-ob.location.z
    ob.data.update()
for name,(head,tail,parent) in list(U.BONES.items()):
    U.BONES[name]=(tuple(head[:2])+(compact_z(head[2]),),tuple(tail[:2])+(compact_z(tail[2]),),parent)
from cleanup_geometry import clean
try:
    clean(U)
except Exception:
    bpy.ops.wm.save_as_mainfile(filepath=str(U.ROOT/'cleanup-diagnostic.blend'))
    raise
arm=bpy.data.armatures.new('SEIS_Bot_Armature');rig=bpy.data.objects.new('SEIS_Bot_Rig',arm);U.EXP.objects.link(rig)
bpy.context.view_layer.objects.active=rig;bpy.ops.object.select_all(action='DESELECT');rig.select_set(True);bpy.ops.object.mode_set(mode='EDIT')
for name,(head,tail,parent) in U.BONES.items():
    bone=arm.edit_bones.new(name);bone.head=head;bone.tail=tail;bone.use_deform=True
for name,(head,tail,parent) in U.BONES.items():
    if parent:arm.edit_bones[name].parent=arm.edit_bones[parent]
bpy.ops.object.mode_set(mode='OBJECT');rig.show_in_front=True;rig.display_type='WIRE'
for name,bone in U.PARTS.items():
    ob=bpy.data.objects[name];group=ob.vertex_groups.new(name=bone);group.add(list(range(len(ob.data.vertices))),1,'REPLACE')
    mod=ob.modifiers.new('Rigid_Articulation','ARMATURE');mod.object=rig;ob.parent=rig
rig['notes']='Rigid FK assembly. No facial animation, soft skin, IK or collision solver.'
scene=bpy.context.scene
floor=U.material('MAT_Studio_Ground','c6c9c5',0,.68)
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,.009));ground=bpy.context.object;ground.name='Studio_Ground';ground.data.name=ground.name
for c in list(ground.users_collection):c.objects.unlink(ground)
U.PRES.objects.link(ground);ground.data.materials.append(floor)
world=bpy.data.worlds.new('Neutral_Studio');scene.world=world;world.use_nodes=True
world.node_tree.nodes['Background'].inputs[0].default_value=(.74,.77,.78,1);world.node_tree.nodes['Background'].inputs[1].default_value=.25
def light(name,loc,energy,size,color,target,sy=None):
    d=bpy.data.lights.new(name,'AREA');d.energy=energy;d.color=color;d.shape='RECTANGLE';d.size=size;d.size_y=sy or size
    o=bpy.data.objects.new(name,d);U.PRES.objects.link(o);o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
light('Key',(-2.1,-3,3.8),470,2.4,(1,.95,.89),(0,0,1.3),3.5)
light('Fill',(2,-2,2.2),115,1.5,(.88,.94,1),(0,0,1.3),3.2)
light('Rear_Edge',(1.8,1.5,3.4),480,1.8,(1,.97,.91),(0,0,1.4),3)
light('Top',(-.5,.1,4),190,1.8,(1,1,1),(0,0,1.3))
def camera(name,loc,target,ortho):
    d=bpy.data.cameras.new(name);o=bpy.data.objects.new(name,d);U.PRES.objects.link(o);o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();d.type='ORTHO';d.ortho_scale=ortho;d.lens=85
    return o
camera('CAM_Front',(0,-7,1.12),(0,0,1.12),2.41)
camera('CAM_Hero',(3,-6,2.60),(0,0,1.10),2.47)
camera('CAM_Side',(6,0,1.35),(0,0,1.10),2.42)
camera('CAM_Back',(-2.8,6,2.40),(0,0,1.10),2.46)
camera('CAM_Portrait',(.64,-1.6,2.08),(0,-.02,1.908),.67)
camera('CAM_Torso',(.70,-2,1.85),(0,0,1.488),1.10)
camera('CAM_Hand',(.9,-1.8,1.03),(.442,-.01,.925),.30)
camera('CAM_Back_Detail',(-.9,2,1.85),(0,.04,1.468),1.10)
scene.camera=bpy.data.objects['CAM_Hero'];scene.render.engine='CYCLES';scene.cycles.samples=96;scene.cycles.use_denoising=True
if sys.platform=='darwin':
    prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='METAL';prefs.get_devices()
    for d in prefs.devices:d.use=(d.type=='METAL')
    scene.cycles.device='GPU'
else:scene.cycles.device='CPU'
scene.cycles.max_bounces=8
scene.render.resolution_x=2000;scene.render.resolution_y=2600;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGB';scene.render.image_settings.color_depth='8'
scene.view_settings.view_transform='AgX';scene.view_settings.look='AgX - Medium High Contrast'
scene['asset_id']='SEIS_BOT_V005';scene['orientation']='Metres, Z up, facing -Y'
scene['construction']='Native editable hard-surface reconstruction from user-provided AI reference images; not scanned geometry.'
scene['reference_primary']='generated_video_frame_000360-topaz-upscale-4x.png; generated_video_frame_000240-topaz-upscale-4x.png; generated_video_frame_000000-topaz-upscale-4x.png'
scene['materials']='Procedural Cycles PBR with clean enamel and satin metal microtexture; not baked for game export.'
scene['blender_version']=bpy.app.version_string
# Native opening view is the new model, in material mode, rather than the rig.
bpy.ops.object.select_all(action='DESELECT')
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type=='VIEW_3D':
            area.spaces.active.shading.type='MATERIAL';area.spaces.active.region_3d.view_distance=3.2;area.spaces.active.region_3d.view_location=(0,0,1.15)
from asset_finish import refine
refine(scene)
bpy.ops.wm.save_as_mainfile(filepath=str(U.ROOT/'seis_bot_v005_rebuilt.blend'))
print(json.dumps({'objects':len(U.PARTS),'bones':len(U.BONES),'output':str(U.ROOT)}),flush=True)
if '--preview' in sys.argv:
    scene.cycles.samples=32;scene.render.resolution_x=1000;scene.render.resolution_y=1400
    for view in ['Front','Hero','Portrait','Back']:
        scene.camera=bpy.data.objects['CAM_'+view];scene.render.filepath=str(U.ROOT/'renders'/('preview-'+view.lower()+'.png'))
        if view=='Portrait':scene.render.resolution_x=1100;scene.render.resolution_y=1100
        bpy.ops.render.render(write_still=True)
