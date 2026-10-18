# blender -b robot_standing.blend -P export_flat.py -- full|lite
# Fallback export: procedural materials replaced by flat glTF PBR colours (texture bake was too slow on this box).
import bpy, sys, os
mode = sys.argv[sys.argv.index('--') + 1]
OUT = '/workspace/robot/v4'
FLAT = {  # name: (base colour, metallic, roughness, emission strength)
    'Armor_Gunmetal': ((0.05, 0.095, 0.092), 0.9, 0.35, 0), 'Armor_Gunmetal_B': ((0.045, 0.088, 0.086), 0.9, 0.37, 0),
    'Armor_Gunmetal_Flat': ((0.04, 0.08, 0.078), 0.9, 0.33, 0), 'Face_Silver': ((0.38, 0.39, 0.40), 1.0, 0.33, 0),
    'Mech_Dark': ((0.03, 0.03, 0.032), 0.8, 0.45, 0), 'Muscle_Red': ((0.33, 0.02, 0.02), 0.0, 0.5, 0),
    'Paint_Red': ((0.45, 0.03, 0.02), 0.2, 0.45, 0), 'Bronze_Worn': ((0.34, 0.29, 0.2), 0.95, 0.35, 0),
    'Socket_Black': ((0.01, 0.01, 0.01), 0.5, 0.5, 0), 'Decal_White': ((0.85, 0.84, 0.8), 0.0, 0.5, 0),
    'Panel_Groove': ((0.008, 0.009, 0.009), 0.3, 0.7, 0),
    'Eye_Glow': ((1.0, 0.0, 0.0), 0.0, 0.2, 3.0), 'Eye_Core': ((1.0, 0.75, 0.7), 0.0, 0.2, 10.0), 'Eye_SocketGlow': ((0.5, 0.0, 0.0), 0.0, 0.4, 0.6)}
rep = {}
for n, (c, m, r, e) in FLAT.items():
    mat = bpy.data.materials.new('GLB_' + n); mat.use_nodes = True; p = mat.node_tree.nodes['Principled BSDF']
    p.inputs['Base Color'].default_value = (*c, 1); p.inputs['Metallic'].default_value = m; p.inputs['Roughness'].default_value = r
    if e: p.inputs['Emission Color'].default_value = (*c, 1); p.inputs['Emission Strength'].default_value = e
    rep[n] = mat
arm = bpy.data.objects['RobotRig']
robot = [o for o in bpy.data.objects if o.type == 'MESH' and o.parent == arm]
miss = set()
for o in robot:
    for s in o.material_slots:
        if s.material and s.material.name in rep: s.material = rep[s.material.name]
        elif s.material: miss.add(s.material.name)
    if mode == 'lite':
        for md in o.modifiers:
            if md.type == 'SUBSURF': md.levels = md.render_levels = min(md.levels, 1)
print('UNMAPPED', miss)
for o in bpy.data.objects: o.select_set(o == arm or o in robot)
bpy.context.view_layer.objects.active = arm
arm.animation_data.action = bpy.data.actions['Standing']; bpy.context.scene.frame_set(1)
fn = os.path.join(OUT, 'robot_v4.glb' if mode == 'full' else 'robot_v4_lite.glb')
bpy.ops.export_scene.gltf(filepath=fn, export_format='GLB', use_selection=True, export_apply=True,
                          export_animations=True, export_animation_mode='ACTIONS', export_yup=True,
                          export_draco_mesh_compression_enable=(mode == 'full'), export_draco_mesh_compression_level=7,
                          export_draco_position_quantization=14, export_draco_normal_quantization=10)
print('EXPORTED', fn, os.path.getsize(fn) / 1e6, 'MB')
