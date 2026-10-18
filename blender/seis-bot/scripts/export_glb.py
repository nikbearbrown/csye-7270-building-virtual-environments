# blender -b robot_baked.blend -P export_glb.py -- full|lite
# full: all subdivision levels, Draco geometry compression, full-res baked JPEG textures
# lite: subdivision capped at 1, textures halved, no Draco (opens in any glTF viewer)
import bpy, sys, os
mode = sys.argv[sys.argv.index('--') + 1]
OUT = '/workspace/robot/v4'
arm = bpy.data.objects['RobotRig']
robot = [o for o in bpy.data.objects if o.type == 'MESH' and o.parent == arm]
if mode == 'lite':
    for o in robot:
        for m in o.modifiers:
            if m.type == 'SUBSURF': m.levels = m.render_levels = min(m.levels, 1)
    for img in bpy.data.images:
        if img.size[0] > 512 and img.has_data or (img.filepath and img.size[0] > 512):
            img.scale(img.size[0] // 2, img.size[1] // 2)
for o in bpy.data.objects:
    o.select_set(o == arm or o in robot)
bpy.context.view_layer.objects.active = arm
arm.animation_data.action = bpy.data.actions['Standing']; bpy.context.scene.frame_set(1)
fn = os.path.join(OUT, 'robot_v2.glb' if mode == 'full' else 'robot_v2_lite.glb')
bpy.ops.export_scene.gltf(filepath=fn, export_format='GLB', use_selection=True, export_apply=True,
                          export_animations=True, export_animation_mode='ACTIONS', export_yup=True,
                          export_image_format='JPEG', export_jpeg_quality=82, export_image_quality=82,
                          export_draco_mesh_compression_enable=(mode == 'full'), export_draco_mesh_compression_level=7,
                          export_draco_position_quantization=16, export_draco_normal_quantization=10, export_draco_texcoord_quantization=12)
print('EXPORTED', fn, os.path.getsize(fn) / 1e6, 'MB')
