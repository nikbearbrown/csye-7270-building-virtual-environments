# ACT III probe (B24): which Godot axis carries which Blender extent. A box with THREE different extents, so a swap cannot hide.
#   Blender -b --factory-startup --python-exit-code 1 --python extents_probe.py -- godot_probe
import bpy, sys, os
out = sys.argv[sys.argv.index("--") + 1]
for name, yup in (("yup_on", True), ("yup_off", False)):
    bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete()
    bpy.ops.mesh.primitive_cube_add(size=2.0, location=(0, 0, 0.9))
    o = bpy.context.active_object
    o.scale = (0.1, 0.3, 0.9)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    bpy.context.view_layer.update()
    print("Blender extents X, Y, Z =", tuple(round(v, 4) for v in o.dimensions), "-> exporting", name)
    bpy.ops.export_scene.gltf(filepath=os.path.join(out, "box_%s.glb" % name), export_format='GLB', export_yup=yup)
