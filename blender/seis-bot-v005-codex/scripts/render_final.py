import bpy,sys,os,math
from pathlib import Path
from mathutils import Vector,Matrix
root=Path(os.environ.get('SEIS_OUTPUT',str(Path(bpy.data.filepath).parent)))
scene=bpy.context.scene;rig=bpy.data.objects['SEIS_Bot_Rig']
if sys.platform=='darwin':
    prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='METAL';prefs.get_devices()
    for device in prefs.devices:device.use=device.type=='METAL'
    scene.cycles.device='GPU'
else:scene.cycles.device='CPU'
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
def render(name,cam,w,h,samples=128):
    scene.camera=bpy.data.objects[cam];scene.render.resolution_x=w;scene.render.resolution_y=h;scene.render.resolution_percentage=100
    scene.cycles.samples=samples;scene.render.filepath=str(root/'renders'/(name+'.png'))
    print('RENDER',name,flush=True);bpy.ops.render.render(write_still=True)
if '--side-preview' in args:
    render('preview-side','CAM_Side',1000,1400,32)
else:
    render('hero','CAM_Hero',3072,4096,192)
    render('front','CAM_Front',2160,2880)
    render('side','CAM_Side',2160,2880)
    render('back','CAM_Back',2160,2880)
    render('portrait','CAM_Portrait',2560,2560,160)
    render('torso-detail','CAM_Torso',2560,2560,160)
    render('hand-detail','CAM_Hand',2160,2160)
    render('back-detail','CAM_Back_Detail',2560,2560)
