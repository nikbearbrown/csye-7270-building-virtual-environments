"""Render saved study without modifying the .blend. -- --variant compact|slim."""
import bpy,sys,argparse,math
from pathlib import Path
from mathutils import Vector
p=argparse.ArgumentParser();p.add_argument('--variant',required=True)
p.add_argument('--hero-only',action='store_true')
a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
root=Path(__file__).resolve().parents[1]
s=bpy.context.scene;c=s.camera
prefix='SEIS_'+a.variant.title()
mouth=bpy.data.objects[prefix+'_Waveform_Mouth']
rig=bpy.data.objects[prefix+'_Rig']
height=1.682 if a.variant=='compact' else 2.077
target=Vector((0,0,height*.49))
views={'three-quarter':(3.4,-6,2.5),'front':(0,-7,target.z),'side':(7,0,target.z),
       'back':(0,7,target.z),'top':(0,-.001,8)}
def shot(name,loc):
    c.location=loc;c.rotation_euler=(target-c.location).to_track_quat('-Z','Y').to_euler()
    s.render.filepath=str(root/'renders'/f'{a.variant}-{name}.png')
    bpy.ops.render.render(write_still=True)
for name,loc in views.items():
    if a.hero_only and name!='three-quarter':continue
    shot(name,loc)
if not a.hero_only:
    mouth.data.shape_keys.key_blocks['Speaking'].value=0
    shot('silent',views['three-quarter'])
    mouth.data.shape_keys.key_blocks['Speaking'].value=1
    # Local X bends the elbow forward; local Z opens the shoulder to the side.
    rig.pose.bones['upperarm_l'].rotation_euler.z=math.radians(-30)
    rig.pose.bones['forearm_l'].rotation_euler.x=math.radians(-85)
    rig.pose.bones['head'].rotation_euler.z=math.radians(-5)
    bpy.context.view_layer.update()
    shot('bent-pose',views['three-quarter'])
    for b in rig.pose.bones:b.rotation_euler=(0,0,0)
    # A geometric wireframe review, kept only in this unsaved render process.
    for o in bpy.data.collections['EXPORT'].objects:
        if o.type!='MESH':continue
        mod=o.modifiers.new('Review_Wireframe','WIREFRAME')
        mod.thickness=.00065;mod.use_replace=True
    shot('wireframe',views['three-quarter'])
