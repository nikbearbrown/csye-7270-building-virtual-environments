# Independent probe (not the agent's): the same 0.2 x 0.2 x 1.8 m column, exported three ways.
import bpy, sys, os
out = sys.argv[sys.argv.index("--") + 1]
def reset():
    bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete()
    for m in list(bpy.data.meshes): bpy.data.meshes.remove(m)
def column(apply_scale):
    bpy.ops.mesh.primitive_cube_add(size=2.0, location=(0, 0, 0.9))   # a 2 m cube...
    o = bpy.context.active_object; o.name = "Column"
    o.scale = (0.1, 0.1, 0.9)   # ...made to look 0.2 x 0.2 x 1.8
    if apply_scale:
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    print(o.name, "dimensions", tuple(round(v, 4) for v in o.dimensions), "scale", tuple(round(v, 4) for v in o.scale))
    return o
for name, yup, apply_scale in [("good", True, True), ("no_yup", False, True), ("no_apply", True, False)]:
    reset(); column(apply_scale)
    bpy.ops.export_scene.gltf(filepath=os.path.join(out, f"column_{name}.glb"), export_format='GLB', export_yup=yup)
    print("exported", name)
