# ACT III probe: the three facts B19/B23 state about Blender, read from a real factory-startup Blender 5.1.2.
#   Blender -b --factory-startup --python-exit-code 1 --python units_axes.py
import bpy
from mathutils import Vector
s = bpy.context.scene
u = s.unit_settings
print("unit_settings: system=%s scale_length=%s length_unit=%s" % (u.system, u.scale_length, u.length_unit))
print("scene.gravity:", tuple(round(v, 2) for v in s.gravity))
x, y = Vector((1, 0, 0)), Vector((0, 1, 0))
print("X cross Y =", tuple(x.cross(y)), "(right-handed if this is +Z)")
import addon_utils
op = bpy.ops.export_scene.gltf.get_rna_type().properties["export_yup"]
print("glTF exporter option %r default = %s" % (op.name, op.default))
print("glTF exporter option description:", op.description)
