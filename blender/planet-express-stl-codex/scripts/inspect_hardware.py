import bpy
from mathutils import Matrix,Vector
s=bpy.context.scene;state={o:(o.hide_render,o.matrix_world.copy()) for o in s.objects if o.type=='MESH'}
for o in state:
 o.hide_render=not ('Silver_Parts_' in o.name)
 if not o.hide_render:o.matrix_world=Matrix.Identity(4)
d=bpy.data.cameras.new('Hardware inspection');c=bpy.data.objects.new('Hardware inspection',d);s.collection.objects.link(c);c.location=(185,10,120);c.rotation_euler=(Vector((125,105,3))-c.location).to_track_quat('-Z','Y').to_euler();d.type='ORTHO';d.ortho_scale=115;s.camera=c;s.render.filepath='/Users/bear/Downloads/planet-express-stl-build/renders/hardware.png';bpy.ops.render.render(write_still=True)
for o,(h,m) in state.items():o.hide_render=h;o.matrix_world=m
print('Hardware inspection complete')
