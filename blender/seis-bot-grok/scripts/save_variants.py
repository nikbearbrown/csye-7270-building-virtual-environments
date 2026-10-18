# blender -b robot.blend -P save_variants.py : writes robot_standing.blend and robot_seated.blend
import bpy
arm = bpy.data.objects['RobotRig']; sc = bpy.context.scene
peds = [o for o in bpy.data.objects if o.name.startswith('Pedestal')]
for act, fn, cam in (('Standing', 'robot_standing.blend', 'Cam_Stand_Front'), ('Thinker', 'robot_seated.blend', 'Cam_Front')):
    arm.animation_data.action = bpy.data.actions[act]; sc.frame_set(1)
    for p in peds: p.hide_render = p.hide_viewport = (act == 'Standing')
    sc.camera = bpy.data.objects[cam]
    sc.render.resolution_x = 2400; sc.render.resolution_y = 3000; sc.render.resolution_percentage = 50
    bpy.ops.wm.save_as_mainfile(filepath='/workspace/robot/v4/' + fn, copy=True)
    print('WROTE', fn)
