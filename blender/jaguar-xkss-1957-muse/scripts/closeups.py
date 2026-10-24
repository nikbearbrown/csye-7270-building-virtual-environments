import bpy, os

outdir = os.path.expanduser('~/workspace/xkss-publish/stage-renders')
os.makedirs(outdir, exist_ok=True)
S = bpy.context.scene
S.render.resolution_x, S.render.resolution_y = 1280, 720
S.render.resolution_percentage = 100

def camera(name, loc, target):
    bpy.ops.object.camera_add(location=loc)
    cam = bpy.context.active_object
    cam.name = name
    bpy.ops.object.empty_add(location=target)
    tgt = bpy.context.active_object
    c = cam.constraints.new('TRACK_TO')
    c.target = tgt
    c.track_axis = 'TRACK_NEGATIVE_Z'
    c.up_axis = 'UP_Y'
    cam.data.lens = 55
    return cam

c1 = camera('DetailFront', (-3.4, -1.7, 0.95), (-2.0, 0, 0.55))
S.camera = c1
S.render.filepath = os.path.join(outdir, 'xkss_detail_front.png')
bpy.ops.render.render(write_still=True)

c2 = camera('DetailCockpit', (0.35, -2.4, 2.0), (0.25, 0, 1.0))
S.camera = c2
S.render.filepath = os.path.join(outdir, 'xkss_detail_cockpit.png')
bpy.ops.render.render(write_still=True)
print('CLOSEUPS DONE')
