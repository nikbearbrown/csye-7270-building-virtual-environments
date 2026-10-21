import bpy
from pathlib import Path
from mathutils import Vector
R=Path('/Users/bear/Downloads/planet-express-stl-build');s=bpy.context.scene
s.render.resolution_x=1600;s.render.resolution_y=600
for name,loc,target,scale in [('compare-front',(0,-400,80),(0,-45,39),75),('compare-rear',(-170,260,100),(0,80,40),100),('compare-turret',(100,-60,140),(0,-9,58),75)]:
 c=bpy.data.objects.get(name)
 if not c:
  d=bpy.data.cameras.new(name);c=bpy.data.objects.new(name,d);s.collection.objects.link(c)
 c.data.type='ORTHO';c.data.ortho_scale=scale;c.data.clip_end=2000;c.location=loc;c.rotation_euler=(Vector(target)-c.location).to_track_quat('-Z','Y').to_euler();s.camera=c;s.render.filepath=str(R/'renders'/f'{name}.png');bpy.ops.render.render(write_still=True)
s.render.resolution_y=1100;s.camera=bpy.data.objects['View • hero'];bpy.ops.wm.save_as_mainfile(filepath=str(R/'planet-express-ship.blend'),compress=True)
print('Comparison cameras rendered and saved.')
