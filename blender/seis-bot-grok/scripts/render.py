# blender -b robot.blend -P render.py -- CAM ACTION SCALE SAMPLES OUT
import bpy, sys
argv = sys.argv[sys.argv.index('--') + 1:]
cam, action, scale, samples, out = argv[0], argv[1], int(argv[2]), int(argv[3]), argv[4]
W, H = (int(argv[5]), int(argv[6])) if len(argv) > 6 else (1024, 1365)
sc = bpy.context.scene
arm = bpy.data.objects['RobotRig']
arm.animation_data.action = bpy.data.actions[action]
sc.frame_set(1)
peds = [o for o in bpy.data.objects if o.name.startswith('Pedestal')]
for p in peds: p.hide_render = (action == 'Standing')
sc.camera = bpy.data.objects[cam]
sc.render.resolution_x = W; sc.render.resolution_y = H
sc.render.resolution_percentage = scale
sc.cycles.samples = samples
sc.render.threads_mode = 'FIXED'; sc.render.threads = 8
sc.render.filepath = out
bpy.ops.render.render(write_still=True)
