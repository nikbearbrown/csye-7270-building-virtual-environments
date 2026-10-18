import bpy,sys,math,json,os
from pathlib import Path
from mathutils import Vector,Matrix
root=Path(os.environ.get('SEIS_OUTPUT',str(Path(bpy.data.filepath).parent)))
scene=bpy.context.scene;rig=bpy.data.objects['SEIS_Bot_Rig']
if sys.platform=='darwin':
    prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='METAL';prefs.get_devices()
    for device in prefs.devices:device.use=device.type=='METAL'
    scene.cycles.device='GPU'
else:scene.cycles.device='CPU'
def desired_bone(name,head,tail):
    b=rig.data.bones[name];pb=rig.pose.bones[name]
    a=b.tail_local-b.head_local;v=Vector(tail)-Vector(head)
    rot=a.rotation_difference(v)
    m=rot.to_matrix()@b.matrix_local.to_3x3()
    pb.matrix=Matrix.Translation(head)@m.to_4x4()
    bpy.context.view_layer.update()

def child_head(name):
    b=rig.data.bones[name]
    if b.parent:return rig.pose.bones[b.parent.name].matrix@b.parent.matrix_local.inverted()@b.head_local
    return b.head_local.copy()

def aim(name,head,direction):
    length=rig.data.bones[name].length;tail=Vector(head)+Vector(direction).normalized()*length
    desired_bone(name,head,tail);return tail

def bend_to(upper,lower,shoulder,wrist,elbow_hint):
    s=Vector(shoulder);w=Vector(wrist);axis=(w-s).normalized();d=(w-s).length
    a=rig.data.bones[upper].length;b=rig.data.bones[lower].length
    along=(a*a-b*b+d*d)/(2*d)
    hint=Vector(elbow_hint)-s;perp=(hint-axis*hint.dot(axis)).normalized()
    elbow=s+axis*along+perp*math.sqrt(max(0,a*a-along*along))
    desired_bone(upper,s,elbow);desired_bone(lower,elbow,w)
    return w

def thinker():
    # Every rigid segment retains its rest length. No body or bone scaling.
    pelvis=Vector((0,.13,.585))
    spine_dir=Vector((0,-.14,.99)).normalized()
    tail=aim('pelvis',pelvis,spine_dir)
    tail=aim('chest',tail,spine_dir)
    tail=aim('neck',tail,spine_dir)
    aim('head',tail,(.07,-.26,.96))
    for suf,s in [('r',-1),('l',1)]:
        h=child_head('thigh_'+suf)
        k=aim('thigh_'+suf,h,(s*.08,-.985,-.03))
        a=aim('shin_'+suf,k,(s*.015,.06,-.998))
        aim('foot_'+suf,a,(0,-.13,-.089))
        sh=child_head('upper_arm_'+suf)
        if suf=='r':
            chin=rig.pose.bones['head'].matrix@rig.data.bones['head'].matrix_local.inverted()@Vector((0,-.13,1.89-.052))
            wr=bend_to('upper_arm_r','forearm_r',sh,chin+Vector((-.065,-.060,-.130)),(-.39,-.37,.96))
            aim('hand_r',wr,(.030,.025,.085))
        else:
            el=aim('upper_arm_l',sh,(.025,-.09,-.367))
            wr=aim('forearm_l',el,(-.13,-.18,-.21))
            aim('hand_l',wr,(-.075,-.025,-.065))
    bpy.context.view_layer.update()
    # Pale plinth like the seated reference images.
    bpy.ops.mesh.primitive_cube_add(size=1,location=(0,.19,.247));seat=bpy.context.object;seat.name='Thinker_Stone_Platform';seat.dimensions=(.60,.46,.486)
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    for c in list(seat.users_collection):c.objects.unlink(seat)
    bpy.data.collections['PRESENTATION'].objects.link(seat)
    seat.data.materials.append(bpy.data.materials['MAT_Studio_Ground'])
    bevel=seat.modifiers.new('Soft_Stone_Edges','BEVEL');bevel.width=.006;bevel.segments=4
    cam=bpy.data.objects['CAM_Hero'];cam.location=(2.8,-4.5,2.18);cam.rotation_euler=(Vector((0,-.04,.86))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=1.93
    scene.camera=cam


thinker()
preview='--preview' in sys.argv
scene.render.resolution_x=1000 if preview else 2560
scene.render.resolution_y=1400 if preview else 3328
scene.render.resolution_percentage=100
scene.cycles.samples=32 if preview else 160
scene.render.filepath=str(root/'renders'/('preview-thinker.png' if preview else 'thinker.png'))
if not preview:bpy.ops.wm.save_as_mainfile(filepath=str(root/'seis_bot_v005_thinker.blend'))
bpy.ops.render.render(write_still=True)
