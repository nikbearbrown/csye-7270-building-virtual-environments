import bpy
from mathutils import Matrix,Vector
s=bpy.context.scene;states={o:(o.hide_render,o.matrix_world.copy()) for o in s.objects if o.type=='MESH'}
for o in states:o.hide_render=o.name!='GOODesign_Silver_Parts_A.part1'
o=bpy.data.objects['GOODesign_Silver_Parts_A.part1'];o.matrix_world=Matrix.Identity(4)
c=bpy.data.objects['Hardware inspection'];c.location=(140,95,-50);c.rotation_euler=(Vector((113.45,99.7,1))-c.location).to_track_quat('-Z','Y').to_euler();c.data.ortho_scale=45;s.camera=c
engine=s.render.engine;s.render.engine='BLENDER_WORKBENCH';s.display.shading.light='STUDIO';s.display.shading.color_type='MATERIAL';s.render.filepath='/Users/bear/Downloads/planet-express-stl-build/renders/vent-underside.png';bpy.ops.render.render(write_still=True);s.render.engine=engine
for o,(h,m) in states.items():o.hide_render=h;o.matrix_world=m
