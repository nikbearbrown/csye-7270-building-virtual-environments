# primitive_defaults.py - prints the default settings of Blender's basic-shape operators (what "a default sphere" means).
#   /Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup --python-exit-code 1 --python primitive_defaults.py
import bpy
print("BLENDER", bpy.app.version_string)
for op, keys in [("primitive_uv_sphere_add", ["segments", "ring_count", "radius"]),
                 ("primitive_cylinder_add", ["vertices", "radius", "depth"]),
                 ("primitive_cone_add", ["vertices", "radius1", "radius2", "depth"]),
                 ("primitive_cube_add", ["size"]), ("primitive_plane_add", ["size"])]:
    props = getattr(bpy.ops.mesh, op).get_rna_type().properties
    print(op, ", ".join("%s=%s" % (k, props[k].default) for k in keys))
