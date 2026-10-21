import bpy,math,json
from mathutils import Matrix,Vector
from pathlib import Path
R=Path('/Users/bear/Downloads/planet-express-stl-build')
scene=bpy.context.scene
for o in bpy.data.objects:
 if o.type=='MESH':o.matrix_world=Matrix.Identity(4)
def xf(name,deg,t):
 o=bpy.data.objects['GOODesign_'+name];o.matrix_world=Matrix.Translation(Vector(t))@Matrix.Rotation(math.radians(deg),4,'X')
xf('Hull_Front',90,(0,-9.845,72.287))
xf('Hull_Rear',-90,(0,17.179,79.218))
bpy.data.objects['GOODesign_Wing_Top'].location.x=-125
# Temporarily inspect principal hull and existing in-place fittings.
keep={'Hull_Front','Hull_Rear','Ring','Window','Window_Frame','Turret_A','Dome','Wing_Top','Cargo_A','Cargo_B','Stair_A','Stair_B','Stand_Cover'}
for o in bpy.data.objects:
 if o.type=='MESH':o.hide_render=o.name.removeprefix('GOODesign_') not in keep
for name,loc,target,scale in [('draft-hero',(230,-280,180),(0,24,30),290),('draft-side',(400,32,38),(0,32,38),280)]:
 if name in bpy.data.objects:o=bpy.data.objects[name]
 else:
  d=bpy.data.cameras.new(name);o=bpy.data.objects.new(name,d);scene.collection.objects.link(o)
 o.data.type='ORTHO';o.data.ortho_scale=scale;o.data.clip_end=2000;o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();scene.camera=o;scene.render.filepath=str(R/'renders'/f'{name}.png');bpy.ops.render.render(write_still=True)
print('Hull orientation draft rendered; source file unchanged.')
