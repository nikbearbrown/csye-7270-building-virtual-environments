import bpy, sys, math
from mathutils import Vector as V, Quaternion, Matrix
R = math.radians
argv = sys.argv[sys.argv.index('--') + 1:]
GS = 0.95
arm = bpy.data.objects['RobotRig']; scene = bpy.context.scene
def q_world(axis, deg): return Quaternion(V(axis), R(deg))
def set_rot(name, q):
    pb = arm.pose.bones[name]; Rm = pb.bone.matrix_local.to_quaternion()
    pb.rotation_quaternion = Rm.inverted() @ q @ Rm
def reset():
    for pb in arm.pose.bones: pb.rotation_quaternion = Quaternion(); pb.location = V()
exec(open('/workspace/robot/v4/poses.py').read())
for k in argv[2:]:
    exec(k)
arm.animation_data.action = None
reset(); pose_thinker(); bpy.context.view_layer.update()
sc = scene; sc.camera = bpy.data.objects[argv[0]]
sc.render.resolution_x = 1200; sc.render.resolution_y = 1500; sc.render.resolution_percentage = 35
sc.cycles.samples = 12; sc.render.threads_mode = 'FIXED'; sc.render.threads = 8
sc.render.filepath = argv[1]; bpy.ops.render.render(write_still=True)
