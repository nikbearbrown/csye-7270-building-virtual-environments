import bpy,os,json
from pathlib import Path
ROOT=Path(os.environ.get('ENTERPRISE_OUTPUT','/Users/bear/Downloads/enterprise-build'))
scene=bpy.context.scene
audit=json.loads((ROOT/'audit.json').read_text())
views=os.environ.get('ENTERPRISE_VIEWS','hero,side,front,top,aft,underside,detail').split(',')
for view in views:
    cam=bpy.data.objects[audit['cameras'][view]];scene.camera=cam
    scene.render.resolution_x=int(cam['resolution'][0]);scene.render.resolution_y=int(cam['resolution'][1])
    scene.render.resolution_percentage=int(os.environ.get('ENTERPRISE_RESOLUTION','100'))
    scene.cycles.samples=int(os.environ.get('ENTERPRISE_SAMPLES','32'))
    scene.render.filepath=str(ROOT/'renders'/f'{view}.png')
    bpy.ops.render.render(write_still=True)
    print('RENDER FINISHED',view,flush=True)
scene.camera=bpy.data.objects[audit['cameras']['hero']]
scene.render.resolution_x=1600;scene.render.resolution_y=1000;scene.render.resolution_percentage=100
