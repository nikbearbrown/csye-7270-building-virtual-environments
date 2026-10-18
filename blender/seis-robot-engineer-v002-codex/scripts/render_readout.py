import bpy,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1];out=R/'renders/readout-frames';out.mkdir(exist_ok=True)
s=bpy.context.scene;c=s.camera;rig=bpy.data.objects['SEIS_Engineer_Rig']
rig.pose.bones['forearm_r'].rotation_euler.x=math.radians(-85)
rig.pose.bones['upperarm_r'].rotation_euler.z=math.radians(12)
rig.pose.bones['head'].rotation_euler.x=math.radians(20)
rig['tool_deployed']=0;rig['screen_orient']=1;rig.update_tag();bpy.context.view_layer.update()
o=bpy.data.objects['SEIS_Engineer_Tool_Screen'];ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get())
target=sum((ev.matrix_world@Vector(v) for v in ev.bound_box),Vector())/8
c.location=target+Vector((-.8,1.2,3.6));c.rotation_euler=(target-c.location).to_track_quat('-Z','Y').to_euler();c.data.ortho_scale=.68
s.render.resolution_x=720;s.render.resolution_y=720;s.cycles.samples=12
for i in range(24):
    s.frame_set(1+i*4);s.render.filepath=str(out/f'{i:04d}.png');bpy.ops.render.render(write_still=True)
print('Readout frames complete. 24 images, four source frames per image, 6fps output = real-time.')

