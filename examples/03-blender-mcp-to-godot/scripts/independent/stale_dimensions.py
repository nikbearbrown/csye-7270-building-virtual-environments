# Blender 5.1.2: obj.dimensions is not updated until the depsgraph is, so a script
# that sets scale and prints dimensions straight away prints the old size.
import bpy
bpy.ops.mesh.primitive_cube_add(size=2.0)
o = bpy.context.active_object
o.scale = (0.1, 0.1, 0.9)
print("BEFORE view_layer.update():", tuple(round(v, 4) for v in o.dimensions))
bpy.context.view_layer.update()
print("AFTER  view_layer.update():", tuple(round(v, 4) for v in o.dimensions))
