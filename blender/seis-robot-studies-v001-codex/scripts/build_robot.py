"""Build the two SEIS mascot studies in a fresh Blender process.

Run with Blender --background --factory-startup --python-exit-code 1
--python build_robot.py -- --variant compact|slim [--render].
EXPORT contains original meshes and one rigid-part FK skeleton.
No downloaded meshes, procedural texture dependencies, or paid services.
"""
import argparse
import json
import math
from pathlib import Path
import sys
import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
args = argparse.ArgumentParser()
args.add_argument('--variant', choices=['compact', 'slim'], required=True)
args.add_argument('--render', action='store_true')
opt = args.parse_args(sys.argv[sys.argv.index('--') + 1:])
v = opt.variant
PREFIX = 'SEIS_' + v.title()
SPECS = {
    'slim': dict(head=1.52, head_size=(.78,.58,.62), torso=.95,
                 torso_size=(.40,.30,.42), shoulder=(.25,0,1.065),
                 elbow=(.34,-.015,.86), wrist=(.365,-.035,.68),
                 hip=(.125,0,.69), knee=(.145,-.01,.40), ankle=(.16,0,.105),
                 foot=(.18,.27,.11), palm=.085, limb=.025),
    'compact': dict(head=1.16, head_size=(.82,.60,.55), torso=.735,
                    torso_size=(.36,.29,.34), shoulder=(.235,0,.86),
                    elbow=(.31,-.01,.66), wrist=(.36,-.045,.48),
                    hip=(.12,0,.50), knee=(.145,-.015,.325), ankle=(.17,.015,.145),
                    foot=(.23,.30,.18), palm=.105, limb=.033)
}
s = SPECS[v]

# Only discard the factory scene in this dedicated, background build process.
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 1.0
export = bpy.data.collections.new('EXPORT')
present = bpy.data.collections.new('PRESENTATION')
work = bpy.data.collections.new('WORK')
for c in (export,present,work): scene.collection.children.link(c)

def material(name, rgba, metallic=0.0, rough=.4):
    m=bpy.data.materials.new('MAT_SEIS_'+name)
    m.diffuse_color=(*rgba,1)
    m.use_nodes=True
    bs=m.node_tree.nodes.get('Principled BSDF')
    bs.inputs['Base Color'].default_value=(*rgba,1)
    bs.inputs['Metallic'].default_value=metallic
    bs.inputs['Roughness'].default_value=rough
    return m

white=material('White_Shell',(.83,.84,.81),.18,.31)
facewhite=material('White_Face',(.94,.94,.91),.02,.49)
dark=material('Graphite_Joints',(.028,.032,.038),.7,.29)
steel=material('Gray_Metal',(.27,.31,.34),.8,.3)
black=material('Black_Ink',(.002,.002,.002),0,.95)
red=material('Red_Accent',(.63,.008,.027),.15,.3)
rubber=material('Black_Soles',(.012,.014,.016),0,.75)
parts=[]
bone_for={}

def active(o):
    bpy.ops.object.select_all(action='DESELECT')
    o.select_set(True)
    bpy.context.view_layer.objects.active=o

def finish(o,name,mat,bone,bevel=0):
    o.name=PREFIX+'_'+name
    for c in list(o.users_collection): c.objects.unlink(o)
    export.objects.link(o)
    active(o)
    bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
    if bevel:
        mod=o.modifiers.new('Manufactured_Edge','BEVEL')
        mod.width=bevel; mod.segments=3
        bpy.ops.object.modifier_apply(modifier=mod.name)
    o.data.name=o.name
    o.data.materials.append(mat)
    o['asset_id']='seis_robot_'+v+'_v001'
    o['part_id']=name
    o['export_role']='rigid_part'
    if not o.data.uv_layers:
        uv=o.data.uv_layers.new(name='UVMap')
        for poly in o.data.polygons:
            axis=max(range(3),key=lambda k:abs(poly.normal[k]))
            dims=[k for k in range(3) if k!=axis]
            for li in poly.loop_indices:
                co=o.data.vertices[o.data.loops[li].vertex_index].co
                uv.data[li].uv=(co[dims[0]],co[dims[1]])
    tri=o.modifiers.new('Final_Triangles','TRIANGULATE')
    bpy.ops.object.modifier_apply(modifier=tri.name)
    parts.append(o); bone_for[o.name]=bone
    return o

def box(name,loc,dims,mat,bone,bevel=.01):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc)
    o=bpy.context.object; o.dimensions=dims
    return finish(o,name,mat,bone,bevel)

def sphere(name,loc,dims,mat,bone):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=20,ring_count=12,radius=1,location=loc)
    o=bpy.context.object; o.scale=tuple(q/2 for q in dims)
    o=finish(o,name,mat,bone)
    for p in o.data.polygons:p.use_smooth=True
    return o

def rod(name,a,b,r,mat,bone,vertices=16):
    a,b=Vector(a),Vector(b); delta=b-a
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=r,depth=delta.length,
                                      end_fill_type='NGON',location=(a+b)/2)
    o=bpy.context.object
    o.rotation_euler=delta.to_track_quat('Z','Y').to_euler()
    o=finish(o,name,mat,bone,.0015)
    for p in o.data.polygons:p.use_smooth=True
    return o

def joint(name,loc,r,bone,axis='X'):
    p=Vector(loc); d=Vector((r*.72,0,0) if axis=='X' else (0,r*.72,0))
    rod(name+'_Hub',p-d,p+d,r,dark,bone,24)
    # Two end caps make the joint legible from either side.
    for k,side in enumerate((-1,1)):
        q=p+d*side
        n=d.normalized()*side
        rod(name+'_Rim_'+str(k),q,q+n*.009,r*.75,steel,bone,24)
        rod(name+'_Bolt_'+str(k),q+n*.01,q+n*.013,r*.38,red,bone,20)

# Oversized cuboid head with a white uninterrupted face, raised oval eyes.
hz=s['head']; hw,hd,hh=s['head_size']
box('Head_Shell',(0,0,hz),(hw,hd,hh),white,'head',.025)
box('Face_Plate',(0,-hd/2-.002,hz),(hw-.045,.009,hh-.045),facewhite,'head',.017)
front=-hd/2-.011
for side,x in [('l',.175),('r',-.175)]:
    sphere('Eye_'+side,(x,front-.002,hz+.095),(.073,.012,.122),black,'head')
    rod('Temple_'+side,(math.copysign(hw/2-.005,x),0,hz-.015),
        (math.copysign(hw/2+.022,x),0,hz-.015),.085,dark,'head',24)
    rod('TempleCap_'+side,(math.copysign(hw/2+.024,x),0,hz-.015),
        (math.copysign(hw/2+.029,x),0,hz-.015),.059,steel,'head',24)
box('Head_Underside',(0,.015,hz-hh/2+.002),(hw*.62,hd*.67,.025),dark,'head',.008)
for ix,x in enumerate((-.28,.28)):
    for iz,z in enumerate((hz-hh*.37,hz+hh*.37)):
        rod('Face_Fastener_'+str(ix)+str(iz),(x,front+.004,z),
            (x,front-.002,z),.006,steel,'head',12)

top=hz+hh/2
rod('Antenna_Base',(-.235,.02,top-.006),(-.235,.02,top+.022),.035,dark,'head')
rod('Antenna_Mast',(-.235,.02,top+.02),(-.315,.02,top+.218),.008,steel,'head',12)
sphere('Antenna_Red_Tip',(-.315,.02,top+.222),(.049,.049,.049),red,'head')

# Black waveform, separate mesh with portable morph targets. Basis lies inside
# the white shell; Speaking=1 moves the fine trace onto the face. No screen.
verts=[]; faces=[]; amps=[]
N=97; R=6; width=.43; mouthz=hz-.106
for i in range(N):
    t=i/(N-1); x=(t-.5)*width
    env=math.sin(math.pi*t)**2
    amp=.024*env*(math.sin(t*math.pi*20)+.48*math.sin(t*math.pi*38+.8))
    amps.append(amp)
    for j in range(R):
        angle=2*math.pi*j/R
        verts.append((x,front+.035+.0022*math.cos(angle),mouthz+.0022*math.sin(angle)))
    if i:
        for j in range(R):
            a=(i-1)*R+j;b=(i-1)*R+(j+1)%R;c=i*R+(j+1)%R;d=i*R+j
            faces.extend([(a,b,c),(a,c,d)])
faces.extend([tuple(reversed(range(R))),tuple((N-1)*R+j for j in range(R))])
me=bpy.data.meshes.new(PREFIX+'_Waveform_Mouth')
me.from_pydata(verts,[],faces);me.update()
mouth=bpy.data.objects.new(PREFIX+'_Waveform_Mouth',me)
export.objects.link(mouth)
mouth=finish(mouth,'Waveform_Mouth',black,'head')
basis=mouth.shape_key_add(name='Basis')
speech=mouth.shape_key_add(name='Speaking')
emphasis=mouth.shape_key_add(name='Emphasis')
for i in range(N):
    for j in range(R):
        k=i*R+j
        speech.data[k].co.y-=.040
        speech.data[k].co.z+=amps[i]
        emphasis.data[k].co.z+=amps[i]*.65
speech.value=1
emphasis.value=0
mouth['instructions']='Speaking: 0 = silent/hidden, 1 = visible black waveform. Emphasis: 0 to 1 increases amplitude. No audio attached.'

# Body and leg assembly.
tz=s['torso']; tw,td,th=s['torso_size']
box('Torso_Shell',(0,0,tz),(tw,td,th),white,'spine_01',.035)
box('Chest_Plate',(0,-td/2-.008,tz),(tw*.83,.018,th*.80),facewhite,'spine_01',.018)
box('Back_Panel',(0,td/2+.003,tz),(tw*.68,.014,th*.7),steel,'spine_01',.009)
for i in range(3):
    box('Back_Vent_'+str(i),(0,td/2+.014,tz-.045+i*.045),(tw*.45,.006,.012),dark,'spine_01',.003)
neckbottom=tz+th/2
necktop=hz-hh/2
rod('Neck_Shaft',(0,0,neckbottom),(0,0,necktop+.015),.039,steel,'neck_01')
for i in range(3):
    z=neckbottom+.015+(necktop-neckbottom-.03)*i/2
    rod('Neck_Ring_'+str(i),(0,0,z-.009),(0,0,z+.009),.057,dark,'neck_01')

# A real extruded digit, converted to mesh, not a raster label.
cu=bpy.data.curves.new(PREFIX+'_Six_Text','FONT')
cu.body='6';cu.align_x='CENTER';cu.size=.32;cu.extrude=.0012;cu.bevel_depth=.0005
font=ROOT.parents[2]/'07-fonts'/'Lato'/'Lato-Bold.ttf'
if not font.exists():
    font=Path('<seis-ai-lab>/07-fonts/Lato/Lato-Bold.ttf')
cu.font=bpy.data.fonts.load(str(font))
o=bpy.data.objects.new(PREFIX+'_Chest_Six',cu);export.objects.link(o)
o.rotation_euler.x=math.pi/2
active(o);bpy.ops.object.convert(target='MESH')
o=bpy.context.object
bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
zspan=max(p.co.z for p in o.data.vertices)-min(p.co.z for p in o.data.vertices)
ratio=th*.62/zspan
o.scale=(ratio,ratio,ratio)
bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
zmin=min(p.co.z for p in o.data.vertices);zmax=max(p.co.z for p in o.data.vertices)
o.location=(0,-td/2-.022,tz-(zmin+zmax)/2)
finish(o,'Chest_Six',red,'spine_01')

hips=s['hip'][2]
box('Pelvis',(0,0,hips+.015),(tw*.72,td*.74,.105),dark,'pelvis',.025)
bonepts={}
for side,sign in [('l',1),('r',-1)]:
    def pt(key):
        a=s[key];return Vector((sign*a[0],a[1],a[2]))
    sh,el,wr=pt('shoulder'),pt('elbow'),pt('wrist')
    hip,kn,ank=pt('hip'),pt('knee'),pt('ankle')
    bonepts[side]=(sh,el,wr,hip,kn,ank)
    joint('Shoulder_'+side,sh,.061,'upperarm_'+side)
    joint('Elbow_'+side,el,.038 if v=='slim' else .044,'forearm_'+side)
    joint('Wrist_'+side,wr,.029,'hand_'+side)
    rod('Upperarm_Core_'+side,sh,el,s['limb']*.65,steel,'upperarm_'+side)
    rod('Upperarm_Cuff_'+side,sh.lerp(el,.36),sh.lerp(el,.74),s['limb'],white,'upperarm_'+side)
    rod('Forearm_Core_'+side,el,wr,s['limb']*.62,steel,'forearm_'+side)
    rod('Forearm_Shell_'+side,el.lerp(wr,.26),el.lerp(wr,.86),s['limb']*1.35,white,'forearm_'+side,12)
    # Rigid hands: palm, three block fingers and an opposing thumb.
    pw=s['palm']; ph=pw*1.05
    pc=wr+Vector((0,-.005,-ph*.6))
    box('Palm_'+side,pc,(pw,.066,ph),white,'hand_'+side,.009)
    for fi,dx in enumerate((-pw*.31,0,pw*.31)):
        a=pc+Vector((dx,-.006,-ph*.54))
        sphere('Knuckle_'+side+str(fi),a,(pw*.24,pw*.24,pw*.24),dark,'hand_'+side)
        b=a+Vector((0,-.008,-.035))
        box('Finger_'+side+str(fi),b,(pw*.23,.034,.047),steel,'hand_'+side,.004)
        box('Fingertip_'+side+str(fi),b+Vector((0,-.015,-.027)),(pw*.22,.035,.027),white,'hand_'+side,.005)
    a=pc+Vector((-sign*pw*.58,0,0))
    b=a+Vector((-sign*.022,-.007,-.04))
    rod('Thumb_'+side,a,b,.014,steel,'hand_'+side,12)
    sphere('Thumbtip_'+side,b,(.028,.03,.036),white,'hand_'+side)
    joint('Hip_'+side,hip,.045,'thigh_'+side)
    joint('Knee_'+side,kn,.042 if v=='slim' else .047,'shin_'+side)
    joint('Ankle_'+side,ank,.031,'foot_'+side)
    rod('Thigh_Core_'+side,hip,kn,s['limb']*.63,steel,'thigh_'+side)
    rod('Thigh_Shell_'+side,hip.lerp(kn,.25),hip.lerp(kn,.75),s['limb']*.90,white,'thigh_'+side,12)
    rod('Shin_Core_'+side,kn,ank,s['limb']*.65,steel,'shin_'+side)
    rod('Shin_Shell_'+side,kn.lerp(ank,.25),kn.lerp(ank,.81),s['limb']*.95,white,'shin_'+side,12)
    fw,fd,fh=s['foot']
    fc=(ank.x,-.055,fh/2+.008)
    box('Foot_'+side,fc,(fw,fd,fh),white,'foot_'+side,.027)
    box('Sole_'+side,(ank.x,-.055,.014),(fw+.007,fd+.012,.028),rubber,'foot_'+side,.008)
    box('Toe_Bumper_'+side,(ank.x,-.055-fd/2+.004,fh*.37),(fw*.70,.025,fh*.38),steel,'foot_'+side,.008)

# One single-root skeleton. Each mechanical component has one full-weight bone.
arm=bpy.data.armatures.new(PREFIX+'_Rig')
rig=bpy.data.objects.new(PREFIX+'_Rig',arm);export.objects.link(rig)
rig.show_in_front=True
rig['asset_id']='seis_robot_'+v+'_v001'
rig['rig_type']='Rigid mechanical FK; no painted/deforming surfaces'
active(rig);bpy.ops.object.mode_set(mode='EDIT')
def bone(name,a,b,parent=None):
    e=arm.edit_bones.new(name);e.head=a;e.tail=b;e.use_deform=True
    if parent:e.parent=arm.edit_bones[parent]
    return e
bone('root',(0,0,0),(0,0,.1))
bone('pelvis',(0,0,hips),(0,0,tz-.08),'root')
bone('spine_01',(0,0,tz-.08),(0,0,neckbottom),'pelvis')
bone('neck_01',(0,0,neckbottom),(0,0,necktop),'spine_01')
bone('head',(0,0,necktop),(0,0,hz+.15),'neck_01')
for side,(sh,el,wr,hip,kn,ank) in bonepts.items():
    bone('upperarm_'+side,sh,el,'spine_01')
    bone('forearm_'+side,el,wr,'upperarm_'+side)
    bone('hand_'+side,wr,wr+Vector((0,0,-.10)),'forearm_'+side)
    bone('thigh_'+side,hip,kn,'pelvis')
    bone('shin_'+side,kn,ank,'thigh_'+side)
    bone('foot_'+side,ank,ank+Vector((0,-.13,0)),'shin_'+side)
bpy.ops.object.mode_set(mode='OBJECT')
for o in parts:
    g=o.vertex_groups.new(name=bone_for[o.name])
    g.add(list(range(len(o.data.vertices))),1.0,'REPLACE')
    m=o.modifiers.new('Rigid_Mechanical_Skin','ARMATURE');m.object=rig
    o.parent=rig
for b in rig.pose.bones:b.rotation_mode='XYZ'

# Presentation remains outside EXPORT.
floor_mat=material('Studio_Floor',(.019,.023,.03),.05,.7)
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.003))
floor=bpy.context.object;floor.name='Studio_Floor'
for c in list(floor.users_collection):c.objects.unlink(floor)
present.objects.link(floor);floor.data.materials.append(floor_mat)
world=bpy.data.worlds.new('Studio_World');scene.world=world;world.use_nodes=True
world.node_tree.nodes['Background'].inputs['Color'].default_value=(.035,.041,.052,1)
world.node_tree.nodes['Background'].inputs['Strength'].default_value=.35
def aim(o,target):o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
def light(name,loc,power,size):
    d=bpy.data.lights.new(name,'AREA');d.energy=power;d.shape='DISK';d.size=size
    o=bpy.data.objects.new(name,d);present.objects.link(o);o.location=loc;aim(o,(0,0,.9))
light('Key_Softbox',(-3,-4,5),650,4)
light('Fill_Softbox',(3,-2,3),420,3)
light('Rim_Softbox',(1,3,4),850,3)
camdata=bpy.data.cameras.new('Review_Camera');cam=bpy.data.objects.new('Review_Camera',camdata)
present.objects.link(cam);scene.camera=cam;camdata.type='ORTHO'
height=top+.25
camdata.ortho_scale=height*1.18
cam.location=(3.4,-6,2.5);aim(cam,(0,0,height*.49))
scene.render.engine='BLENDER_EEVEE'
scene.eevee.taa_render_samples=64
scene.render.resolution_x=1200;scene.render.resolution_y=1400;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'
scene.view_settings.view_transform='AgX'
scene.render.film_transparent=False
scene['asset_spec']='White/gray/black SEIS robot, red 6 and antenna. +Z up, -Y forward. Units meters. EXPORT contains originals.'
scene['source_reference']='mascot/waveform-mouth-v1 and Screenshot 2026-10-17 at 1.27.57 PM'
scene['voice_preference']='Desmond (future animation; no audio in this model)'
for area in bpy.context.screen.areas:
    if area.type=='VIEW_3D':
        area.spaces.active.region_3d.view_perspective='CAMERA'
        area.spaces.active.shading.type='MATERIAL'
        area.spaces.active.shading.use_scene_world=True
        area.spaces.active.shading.use_scene_lights=True
        area.spaces.active.overlay.show_overlays=False
active(rig)
scene.render.filepath=str(ROOT/'renders'/f'{v}-three-quarter.png')
blend=ROOT/f'seis_robot_{v}_v001.blend'
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(blend))

dg=bpy.context.evaluated_depsgraph_get()
stats=[]
lo=Vector((1e9,)*3);hi=Vector((-1e9,)*3)
for o in parts:
    ev=o.evaluated_get(dg);me=ev.to_mesh()
    tri=sum(len(p.vertices)-2 for p in me.polygons)
    stats.append(dict(object=o.name,triangles=tri,vertices=len(me.vertices),bone=bone_for[o.name]))
    for pt in ev.bound_box:
        w=ev.matrix_world@Vector(pt)
        lo=Vector(map(min,lo,w));hi=Vector(map(max,hi,w))
    ev.to_mesh_clear()
report=dict(asset_id='seis_robot_'+v+'_v001',blender=bpy.app.version_string,
            source_revision='v001',facing='-Y in Blender, +Z after standard glTF Y-up conversion',
            size_m=list(hi-lo),export_collection='EXPORT',export_contains='originals',
            meshes=len(parts),triangles=sum(o['triangles'] for o in stats),
            materials=len({m.name for o in parts for m in o.data.materials}),textures=0,
            bones=len(arm.bones),max_influences=1,unweighted_vertices=0,
            animations=[],mouth_morph_targets=['Speaking','Emphasis'],objects=stats)
(ROOT/'reports'/f'{v}-asset-manifest.json').write_text(json.dumps(report,indent=2))
print('ASSET_REPORT',json.dumps({k:val for k,val in report.items() if k!='objects'}))
if opt.render:
    views={'three-quarter':(3.4,-6,2.5),'front':(0,-7,height*.49),
           'side':(7,0,height*.49),'back':(0,7,height*.49),'top':(0,-.001,8)}
    for name,loc in views.items():
        cam.location=loc;aim(cam,(0,0,height*.49))
        scene.render.filepath=str(ROOT/'renders'/f'{v}-{name}.png')
        bpy.ops.render.render(write_still=True)
    cam.location=views['three-quarter'];aim(cam,(0,0,height*.49))
    speech.value=0
    scene.render.filepath=str(ROOT/'renders'/f'{v}-silent.png')
    bpy.ops.render.render(write_still=True)
    speech.value=1
    # Review a raised/bent arm using actual rigid-part FK, not a fake render pose.
    rig.pose.bones['upperarm_l'].rotation_euler.z=math.radians(-35)
    rig.pose.bones['forearm_l'].rotation_euler.z=math.radians(-65)
    rig.pose.bones['head'].rotation_euler.z=math.radians(-5)
    bpy.context.view_layer.update()
    scene.render.filepath=str(ROOT/'renders'/f'{v}-bent-pose.png')
    bpy.ops.render.render(write_still=True)
print('BUILT',blend)
