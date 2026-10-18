import bpy,math,sys,argparse
from pathlib import Path
from mathutils import Vector
p=argparse.ArgumentParser();p.add_argument('--quick',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
R=Path(__file__).resolve().parents[1];s=bpy.context.scene;c=s.camera
rig=bpy.data.objects['SEIS_Engineer_Rig'];mouth=bpy.data.objects['SEIS_Engineer_Waveform_Mouth']
def reset():
    for pb in rig.pose.bones:pb.rotation_euler=(0,0,0)
    rig['tool_deployed']=1.0;rig['screen_orient']=0.0;rig.update_tag()
    mouth.data.shape_keys.key_blocks['Speaking'].value=1
    s.frame_set(1);bpy.context.view_layer.update()
def shot(name,loc,target=(0,0,1.40),scale=3.48):
    c.location=loc;c.rotation_euler=(Vector(target)-c.location).to_track_quat('-Z','Y').to_euler()
    c.data.ortho_scale=scale;s.render.filepath=str(R/'renders'/('engineer-'+name+'.png'))
    bpy.ops.render.render(write_still=True)
reset()
for name,loc in [('front',(0,-7,1.40)),('side',(7,0,1.40)),('back',(0,7,1.40)),('top',(0,-.001,8))]:
    if a.quick:break
    shot(name,loc)
if not a.quick:
    mouth.data.shape_keys.key_blocks['Speaking'].value=0
    shot('silent',(3.8,-6,3.0))
    reset();rig['tool_deployed']=0.0;rig.update_tag();bpy.context.view_layer.update()
    shot('hand-mode',(-3.8,-6,3.0))
reset()
rig.pose.bones['forearm_r'].rotation_euler.x=math.radians(-85)
rig.pose.bones['upperarm_r'].rotation_euler.z=math.radians(12)
rig.pose.bones['head'].rotation_euler.x=math.radians(20)
rig['tool_deployed']=0;rig['screen_orient']=1;rig.update_tag()
bpy.context.view_layer.update()
shot('wrist-playbook',(-3.4,-6,5.1))
if not a.quick:
    # True physical screen in raised forearm pose, camera above the operator's wrist.
    dg=bpy.context.evaluated_depsgraph_get()
    obj=bpy.data.objects['SEIS_Engineer_Tool_Screen'];ev=obj.evaluated_get(dg)
    target=sum((ev.matrix_world@Vector(v) for v in ev.bound_box),Vector())/8
    shot('wrist-detail',target+Vector((-.8,1.2,3.6)),target,.68)
    reset()
    shot('connector-detail',(-2.5,-4,1.8),(-.63,-.02,1.37),.94)
    rig['tool_deployed']=0;rig.update_tag();bpy.context.view_layer.update()
    shot('hand-detail',(-2.5,-4,1.8),(-.63,-.02,1.37),.94)
    reset()
    for o in bpy.data.collections['EXPORT'].objects:
        if o.type=='MESH':
            w=o.modifiers.new('Review_Wireframe','WIREFRAME');w.thickness=.0008;w.use_replace=True;w.use_even_offset=False
    shot('wireframe',(3.8,-6,3.0))
print('Views rendered from the saved model; original .blend not modified.')

