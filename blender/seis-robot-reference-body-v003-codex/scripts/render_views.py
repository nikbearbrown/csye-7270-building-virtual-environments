import bpy
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parent.parent
scene=bpy.context.scene;cam=scene.camera
views=[
 ('body-front',(0,-6,.97),(0,0,.97),2.18),
 ('body-side',(6,0,.97),(0,0,.97),2.18),
 ('body-back',(0,6,.97),(0,0,.97),2.18),
 ('body-rear-three-quarter',(-3,5,2.6),(0,0,.96),2.18),
 ('body-only-front',(0,-6,.81),(0,0,.81),1.85),
]
for name,loc,target,scale in views:
 for o in bpy.data.collections['EXPORT'].objects:
  o.hide_render=name=='body-only-front' and o.get('body_group')=='head_placeholder'
 cam.location=loc;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=scale
 scene.render.filepath=str(ROOT/'renders'/(name+'.png'));bpy.ops.render.render(write_still=True)
 print('RENDER_COMPLETE',name,flush=True)
